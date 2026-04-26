from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Reel(Base):
    __tablename__ = 'reels'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    
    # NEW FIELDS FOR KNOWLEDGE ENGINE
    summary = Column(Text, nullable=True)
    topics = Column(JSON, nullable=True)
    keywords = Column(JSON, nullable=True)
    intent = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "category": self.category,
            "summary": self.summary,
            "topics": self.topics,
            "keywords": self.keywords,
            "intent": self.intent,
            "created_at": self.created_at.isoformat()
        }
