# REELMIND 🧠
### Production-Grade AI Knowledge Engine for Instagram

REELMIND is a high-performance personal AI system that transforms saved Instagram reels into a structured, semantic knowledge library. Unlike simple bookmarking tools, REELMIND understands the **meaning, intent, and subjects** of your content using deep-learning models.

---

## ✨ Features (V2 - Knowledge Engine)

- **Semantic Discovery**: Search your reels by "concepts" and "intent" rather than just keywords (powered by ChromaDB and Sentence-Transformers).
- **Deep AI Analysis**: Every reel is processed by Llama-3 (via Groq) to extract:
  - 📝 **Concise Summary**
  - 🏷️ **Pillar Topics**
  - 🔑 **Subject Keywords**
  - 🎯 **Creator Intent**
- **Automated Collection**: One-click Playwright automation saves reels and captures full metadata.
- **Smart Re-indexing**: A built-in sync engine that updates your semantic index as your library grows.
- **Premium Dashboards**: State-of-the-art Dark Mode UI with Jakarta Sans typography and real-time similarity scoring.

---

## 🚀 Tech Stack

- **AI Brain**: Groq Cloud (Llama-3.1-8b-instant)
- **Embeddings**: Sentence-Transformers (Local all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (Semantic Retrieval)
- **RDBMS**: SQLite + SQLAlchemy (Metadata)
- **Automation**: Playwright (Headless Chromium)
- **API**: FastAPI (High-performance Python)

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A [Groq API Key](https://console.groq.com/)

### 2. Installation
```bash
# Clone and install
git clone https://github.com/rudrapatel06/reelmind-ai.git
pip install -r requirements.txt

# Setup Playwright
playwright install chromium
```

### 3. Configuration
Copy `.env.example` to `.env` and add your `GROQ_API_KEY`.

### 4. Usage
1. Run `python ingestion/login.py` to link your Instagram account.
2. Run `python -m uvicorn api.main:app --reload` to start the engine.
3. Access the dashboard at `http://127.0.0.1:8000`.

---

## 🔒 Privacy

- **Local-First**: All your vectors, databases, and session cookies stay on your machine.
- **Secure Integration**: Your Instagram password is never stored; only local session tokens are used.

---

## 📄 License
MIT License - Developed by [Rudra Patel](https://github.com/rudrapatel06)
