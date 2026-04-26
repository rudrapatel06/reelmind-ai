import os
import json
from groq import Groq
from core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def analyze_reel(caption: str) -> dict:
    """
    Perform deep structural analysis of a reel caption.
    Returns a dict with summary, topics, keywords, intent, and category.
    """
    if not caption:
        return {
            "summary": "No caption provided.",
            "topics": [],
            "keywords": [],
            "intent": "unknown",
            "category": "UNCATEGORIZED"
        }

    prompt = f"""
    You are an Expert Knowledge Engineer. Analyze the following Instagram reel caption and extract structured information.
    
    CAPTION:
    "{caption}"
    
    TASK:
    1. SUMMARY: A concise 1-sentence summary of what the reel is about.
    2. TOPICS: A list of 2-4 main subject matters (e.g., "Performance Cars", "Cinematic Photography").
    3. KEYWORDS: A list of 5-8 specific tags/keywords.
    4. INTENT: The likely intent of the creator (e.g., Educational, Entertainment, Commercial, Inspirational).
    5. CATEGORY: One broad, capitalized category name (e.g., CAR, MOVIE, TECH, WEALTH, LIFESTYLE).
    
    FORMAT: Return ONLY valid JSON.
    {{
      "summary": "...",
      "topics": ["...", "..."],
      "keywords": ["...", "..."],
      "intent": "...",
      "category": "..."
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    except Exception as e:
        print(f"AI Analysis error: {e}")
        return {
            "summary": "Analysis failed.",
            "topics": [],
            "keywords": [],
            "intent": "unknown",
            "category": "UNCATEGORIZED"
        }
