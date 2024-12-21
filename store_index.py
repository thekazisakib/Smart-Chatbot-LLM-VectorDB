import os
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.docstore.document import Document
from dotenv import load_dotenv
import uuid

load_dotenv()

QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')
QDRANT_ENDPOINT = os.environ.get('QDRANT_ENDPOINT')

class JSONLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

class DirectoryLoader:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def load_all(self):
        json_data = {}
        for file_name in os.listdir(self.directory_path):
            if file_name.endswith('.json'):
                loader = JSONLoader(os.path.join(self.directory_path, file_name))
                json_data[file_name] = loader.load()
        return json_data

# Load JSON data
json_loader = JSONLoader(r'C:\Ml Project\Smart-Chatbot-LLM-VectorDB\data\jewel_changi_content.json')
jewel_data = json_loader.load()

# Convert list of strings to Document objects
documents = [Document(page_content=item) for item in jewel_data if item]

# Initialize Qdrant client
client = QdrantClient(
    url=QDRANT_ENDPOINT,
    api_key=QDRANT_API_KEY
)

# Define collection parameters
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

# Download Hugging Face embeddings model
from src.helper import download_hugging_face_embeddings
embeddings = download_hugging_face_embeddings()

# Store embeddings in Qdrant
for document in documents:
    if document.page_content:
        text = document.page_content
        vector = embeddings.embed_query(text)
        point_id = str(uuid.uuid4())

        client.upsert(
            collection_name=collection_name,
            points=[
                {
                    'id': point_id,
                    'vector': vector,
                    'payload': {'text': text}
                }
            ]
        )

print(f"Embeddings for {len(documents)} documents stored in Qdrant successfully.")
