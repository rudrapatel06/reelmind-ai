import json
from groq import Groq
from core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def categorize_reel(caption: str, existing_collections: list[str] = None) -> str:
    """Extract a single category for the Instagram Reel, prioritizing existing collections."""
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set.")
        
    if existing_collections is None:
        existing_collections = []
        
    collections_str = ", ".join(existing_collections) if existing_collections else "None"
        
    prompt = f"""
    You are a professional Content Librarian. Your goal is to accurately categorize Instagram reels based on their captions.
    
    Caption: "{caption}"
    
    User's existing collections: [{collections_str}]
    
    Categorization Rules:
    1. Look for THEME keywords: 
       - Houses, Architecture, Interior -> HOME
       - Movies, Film, Cinema, Actors -> MOVIE
       - Cars, Vehicles, Racing -> CAR
       - Wealth, Money, Success -> WEALTH
       - Tech, Gadgets, AI -> TECH
    2. If the reel fits an existing category, use it EXACTLY.
    3. If not, create a BROAD, capitalized category name (e.g., LIFESTYLE, FOOD, SPORTS).
    4. Avoid using "SOCIAL MEDIA" or "INSTAGRAM" as a category.
    
    Return a JSON object with a single key "category". Output ONLY valid JSON.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {"role": "system", "content": "You are a categorization assistant. Output strictly a JSON object like {\"category\": \"Word\"}."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    try:
        content = response.choices[0].message.content
        data = json.loads(content)
        category = data.get("category", "Uncategorized").strip()
        
        # Capitalize only if it's a new category to maintain original casing for existing ones
        if category.lower() not in [c.lower() for c in existing_collections]:
            category = category.title()
            
        # Ensure it's not too long
        if len(category) > 25:
            category = category[:25]
        return category
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return "Uncategorized"
