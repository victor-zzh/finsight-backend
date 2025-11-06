from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os
from typing import List, Dict, Any
from openai import OpenAI
from config import DB_BATCH_SIZE

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def create_collection_if_not_exists(collection_name: str = "financial_chunks"):
    """Create Qdrant collection if it doesn't exist"""
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

def embed_text(text: str) -> List[float]:
    """Generate embeddings using OpenAI"""
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def embed_and_store_chunks(chunks: List[Dict[str, Any]]):
    """Embed chunks and store in Qdrant"""
    create_collection_if_not_exists()

    points = []
    for chunk in chunks:
        vector = embed_text(chunk["content"])
        point = {
            "id": chunk["id"],  # Assuming UUID from chunks table
            "vector": vector,
            "payload": {
                "ts_code": chunk["ts_code"],
                "year": chunk["year"],
                "period": chunk["period"],
                "doc_id": chunk["doc_id"],
                "content": chunk["content"],
                "chunk_index": chunk["chunk_index"],
            }
        }
        points.append(point)

    # Batch upsert
    for i in range(0, len(points), DB_BATCH_SIZE):
        batch = points[i:i + DB_BATCH_SIZE]
        qdrant_client.upsert(collection_name="financial_chunks", points=batch)
