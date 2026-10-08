import os
import chromadb

client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"), port=8000)
print("Heartbeat:", client.heartbeat())

collection = client.get_or_create_collection(name="notes")

collection.add(
    ids=["1", "2", "3"],
    documents=[
        "Docker packages apps into containers",
        "Vector databases search by meaning",
        "Pasta is made from wheat flour",
    ],
    metadatas=[{"topic": "devops"}, {"topic": "ai"}, {"topic": "food"}],
)

results = collection.query(query_texts=["how do I ship my app?"], n_results=2)
print(results["documents"])