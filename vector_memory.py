import os
import uuid
import chromadb
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="jarvis_memory"
)

def embed(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def store_memory(text: str, metadata: dict = None):
    collection.add(
        documents=[text],
        embeddings=[embed(text)],
        metadatas=[metadata or {}],
        ids=[str(uuid.uuid4())]
    )

def recall_memory(query: str, limit: int = 3):
    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=limit
    )
    return results["documents"][0] if results["documents"] else []
