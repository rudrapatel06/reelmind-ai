from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

from core.config import settings
from ingestion.saver import process_and_save_reel, unsave_reel
from storage.database import init_db, get_db, engine
from storage.models import Reel
from core.orchestrator import orchestrate_knowledge_extraction
from embeddings.generator import generate_embedding
from retrieval.engine import semantic_search, remove_from_vector_db

app = FastAPI(title="REELMIND AI Knowledge Engine")

@app.on_event("startup")
def on_startup():
    init_db()
    with engine.connect() as conn:
        for col in ["summary TEXT", "topics JSON", "keywords JSON", "intent TEXT"]:
            try:
                conn.execute(text(f"ALTER TABLE reels ADD COLUMN {col}"))
                conn.commit()
            except Exception: pass

class SaveRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    template_path = os.path.join("templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>UI Template not found.</h1>"

@app.post("/api/save")
def save_reel(request: SaveRequest, db: Session = Depends(get_db)):
    if "instagram.com/reel/" not in request.url:
        return {"status": "error", "error": "Invalid Instagram Reel URL."}
    try:
        ig_result = process_and_save_reel(request.url)
        if ig_result["status"] == "success":
            existing = db.query(Reel).filter(Reel.url == request.url).first()
            if not existing:
                new_reel = Reel(url=request.url, category="PENDING")
                db.add(new_reel)
                db.commit()
                db.refresh(new_reel)
                reel_id = new_reel.id
            else:
                reel_id = existing.id
            analysis = orchestrate_knowledge_extraction(db, reel_id, ig_result["caption"], request.url)
            return {"status": "success", "category": analysis.get("category"), "summary": analysis.get("summary")}
        return ig_result
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/search")
def search_reels(q: str, db: Session = Depends(get_db)):
    if not q: return []
    print(f"SEARCHING FOR: {q}")
    query_vector = generate_embedding(q)
    results = semantic_search(query_vector, n_results=15)
    
    filtered_results = []
    for r in results:
        similarity = 1 - r['score']
        print(f"DEBUG: Found '{r['metadata'].get('summary')[:30]}...' with similarity {similarity:.2f}")
        # Lowered threshold to 25% for testing
        if similarity > 0.25:
            filtered_results.append(r)
    
    filtered_results.sort(key=lambda x: x['score'])
    return filtered_results

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    results = db.query(Reel.category).distinct().all()
    output = []
    for (cat,) in results:
        count = db.query(Reel).filter(Reel.category == cat).count()
        output.append({"name": cat, "count": count})
    return output

@app.get("/api/reels/{category}")
def get_reels_by_category(category: str, db: Session = Depends(get_db)):
    reels = db.query(Reel).filter(Reel.category == category).all()
    return [r.to_dict() for r in reels]

@app.post("/api/unsave")
def api_unsave_reel(request: SaveRequest, db: Session = Depends(get_db)):
    try:
        reel = db.query(Reel).filter(Reel.url == request.url).first()
        if reel:
            remove_from_vector_db(reel.id)
            unsave_reel(request.url)
            db.delete(reel)
            db.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/api/reindex")
def reindex_all(db: Session = Depends(get_db)):
    reels = db.query(Reel).all()
    count = 0
    from embeddings.generator import generate_embedding, prepare_text_for_embedding
    from retrieval.engine import add_to_vector_db
    for reel in reels:
        print(f"RE-INDEXING REEL {reel.id}...")
        if not reel.summary:
            try:
                orchestrate_knowledge_extraction(db, reel.id, "Archived Reel", reel.url)
                count += 1
            except: continue
        else:
            analysis = {"summary": reel.summary, "topics": reel.topics, "keywords": reel.keywords, "category": reel.category}
            text_to_embed = prepare_text_for_embedding(analysis)
            emb = generate_embedding(text_to_embed)
            add_to_vector_db(reel.id, emb, {"url": reel.url, "category": reel.category, "summary": reel.summary[:200]})
            count += 1
    return {"status": "success", "indexed": count}
