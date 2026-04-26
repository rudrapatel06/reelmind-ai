from sqlalchemy.orm import Session
from storage.models import Reel
from processing.structurer import analyze_reel
from embeddings.generator import generate_embedding, prepare_text_for_embedding
from retrieval.engine import add_to_vector_db

def orchestrate_knowledge_extraction(db: Session, reel_id: int, caption: str, url: str):
    """
    Main pipeline:
    1. AI Analysis
    2. Embedding Generation
    3. SQLite Update
    4. Vector DB Sync
    """
    # 1. AI Analysis
    print(f"Running AI analysis for Reel {reel_id}...")
    analysis = analyze_reel(caption)
    
    # 2. Embedding Generation
    print("Generating semantic embedding...")
    text_to_embed = prepare_text_for_embedding(analysis)
    embedding = generate_embedding(text_to_embed)
    
    # 3. Update SQLite
    reel = db.query(Reel).filter(Reel.id == reel_id).first()
    if reel:
        reel.summary = analysis.get('summary')
        reel.topics = analysis.get('topics')
        reel.keywords = analysis.get('keywords')
        reel.intent = analysis.get('intent')
        reel.category = analysis.get('category', reel.category)
        db.commit()
    
    # 4. Sync with Vector DB (Chroma)
    print("Syncing with Vector Database...")
    metadata = {
        "url": url,
        "category": analysis.get('category'),
        "summary": analysis.get('summary')[:200] # Chroma metadata likes strings
    }
    add_to_vector_db(reel_id, embedding, metadata)
    
    return analysis
