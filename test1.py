from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://3607b9cc-3e8d-4a76-ada5-843a14f7b744.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="Z0cX0VR7CQPt6PewtS_kAZ2VZ6vQHQX9PbhJRKhzLHWKCFe15nfB_A",
)

print(qdrant_client.get_collections())