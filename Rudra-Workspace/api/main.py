from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

from core.config import settings
from ingestion.saver import process_and_save_reel, unsave_reel
from storage.database import init_db, get_db
from storage.models import Reel

app = FastAPI(title="REELMIND Auto-Saver")

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

class SaveRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the stunning frontend UI."""
    template_path = os.path.join("templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>UI Template not found.</h1>"

@app.post("/api/save")
def save_reel(request: SaveRequest, db: Session = Depends(get_db)):
    """Process, categorize, and save the reel both to IG and local DB."""
    if "instagram.com/reel/" not in request.url:
        return {"status": "error", "error": "Invalid Instagram Reel URL."}
        
    try:
        # 1. Automate Save on Instagram
        result = process_and_save_reel(request.url)
        
        if result["status"] == "success":
            # 2. Save to local Database
            category = result.get("category", "Uncategorized")
            
            # Check if already exists in DB
            existing = db.query(Reel).filter(Reel.url == request.url).first()
            if not existing:
                new_reel = Reel(url=request.url, category=category)
                db.add(new_reel)
                db.commit()
            
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get list of unique categories with counts."""
    results = db.query(Reel.category).distinct().all()
    output = []
    for (cat,) in results:
        count = db.query(Reel).filter(Reel.category == cat).count()
        output.append({"name": cat, "count": count})
    return output

@app.get("/api/reels/{category}")
def get_reels_by_category(category: str, db: Session = Depends(get_db)):
    """Get all reels in a specific category."""
    reels = db.query(Reel).filter(Reel.category == category).all()
    return [r.to_dict() for r in reels]

@app.post("/api/unsave")
def api_unsave_reel(request: SaveRequest, db: Session = Depends(get_db)):
    """Remove reel from IG and local DB."""
    try:
        # 1. Automate Unsave on Instagram
        ig_result = unsave_reel(request.url)
        
        # 2. Remove from local DB
        db.query(Reel).filter(Reel.url == request.url).delete()
        db.commit()
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
