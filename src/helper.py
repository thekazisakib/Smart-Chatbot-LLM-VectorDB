from langchain.document_loaders import JSONLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


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

if __name__ == "__main__":
    jewel_loader = JSONLoader(r'C:\Ml Project\Smart-Chatbot-LLM-VectorDB\data\jewel_changi_content.json')
    jewel_data = jewel_loader.load()
    print("Loaded jewel_changi_content.json:")
    print(jewel_data)



#Create text chunks
def text_split(documents):
    valid_documents = [doc for doc in documents if doc.page_content and doc.page_content.strip()]
    if not valid_documents:
        print("No valid documents found. Ensure your input data is correct.")
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(valid_documents)
    return text_chunks



#download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings