import chromadb
from chromadb.config import Settings
import os

# Persistent directory for the vector database
CHROMA_PATH = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)
# COLLECTION V2: Using Cosine Similarity
# We use a new name to force Chroma to use the 'cosine' space metric
collection = client.get_or_create_collection(
    name="reels_v2",
    metadata={"hnsw:space": "cosine"}
)

def add_to_vector_db(reel_id: int, embedding: list, metadata: dict):
    """Add a reel's vector to ChromaDB."""
    collection.add(
        ids=[str(reel_id)],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def semantic_search(query_embedding: list, n_results: int = 5):
    """Perform similarity search in the vector space."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Format results for the frontend
    output = []
    if results['ids']:
        for i in range(len(results['ids'][0])):
            output.append({
                "id": results['ids'][0][i],
                "score": results['distances'][0][i],
                "metadata": results['metadatas'][0][i]
            })
    return output

def remove_from_vector_db(reel_id: int):
    """Delete entry from ChromaDB."""
    collection.delete(ids=[str(reel_id)])
