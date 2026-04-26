from sentence_transformers import SentenceTransformer
import torch

# Load a lightweight, high-performance local model
# all-MiniLM-L6-v2 is fast and produces 384-dimensional vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> list:
    """Generate a semantic vector from text."""
    if not text:
        return [0.0] * 384
    
    with torch.no_grad():
        embedding = model.encode(text, convert_to_numpy=True)
    
    return embedding.tolist()

def prepare_text_for_embedding(analysis: dict) -> str:
    """Concatenate fields for rich semantic representation."""
    parts = [
        analysis.get('summary', ''),
        ", ".join(analysis.get('topics', [])),
        ", ".join(analysis.get('keywords', [])),
        analysis.get('category', '')
    ]
    return " | ".join([p for p in parts if p])
