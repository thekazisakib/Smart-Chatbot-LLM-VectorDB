from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

API_KEY = os.environ.get('QDRANT_API_KEY')
ENDPOINT = os.environ.get('QDRANT_ENDPOINT')

embeddings = download_hugging_face_embeddings()

# Initialize Qdrant client
client = QdrantClient(
    url=ENDPOINT,
    api_key=API_KEY
)

# Collection and vector setup
collection_name = "my_collection"
vector_size = 384  

try:
    client.get_collection(collection_name)
except Exception:
    vectors_config = models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    )
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=vectors_config
    )

# Load Qdrant as a retriever
docsearch = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embeddings
)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs = {"prompt": PROMPT}

llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens': 512, 'temperature': 0.8})

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    if not msg.strip():
        return "Please enter a valid input."

    try:
        print(f"User input: {msg}")
        result = qa.run({"query": msg})
        print("Response:", result)
        return str(result)
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
