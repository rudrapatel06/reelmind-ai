# REELMIND 🧠
### AI-Powered Personal Knowledge Engine for Instagram

REELMIND is a high-performance automation tool that transforms your saved Instagram reels into an intelligent, categorized, and searchable personal library. It uses a combination of **Playwright** for browser automation, **Groq AI** for lightning-fast content categorization, and **SQLite** for local data persistence.

---

## ✨ Features

- **Automated Saving**: One-click automation to save any Instagram reel to your account.
- **AI Categorization**: Uses Llama-3 (via Groq) to analyze captions and automatically group reels into meaningful "Pillars" (e.g., CAR, MOVIE, WEALTH).
- **Personal Library**: A stunning, professional web dashboard to manage your saved content.
- **Folder Management**: View your reels organized by category with automatic item counts.
- **Automated Unsaving**: The "X" button not only removes the reel from your local library but also commands the robot to unsave it from your Instagram account.
- **Premium UI**: Dark-mode mesh aesthetic with smooth transitions and professional typography.

---

## 🚀 Tech Stack

- **Backend**: FastAPI (Python)
- **Automation**: Playwright (Headless Chromium)
- **AI**: Groq (Llama-3.1-8b-instant)
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Vanilla HTML5, Tailwind CSS, JavaScript (SPA architecture)

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A [Groq API Key](https://console.groq.com/)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/reelmind.git
cd reelmind

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configuration
Copy the `.env.example` to `.env` and add your Groq API Key:
```env
GROQ_API_KEY=your_key_here
```

### 4. Authentication
Before running the app, you must link your Instagram account. Run the login script:
```bash
python ingestion/login.py
```
*This will open a browser for you to log in. Once done, it saves your session locally to `session_data/state.json` so the robot can act on your behalf.*

---

## 💻 Usage

1. **Start the Server**:
```bash
python -m uvicorn api.main:app --reload
```
2. **Access the App**: Open `http://127.0.0.1:8000` in your browser.
3. **Save Reels**: Paste any Instagram Reel URL and click "Capture".
4. **Manage Library**: Click "My Reels" to browse your folders.

---

## 🔒 Privacy & Security

- **Local Storage**: Your Instagram session data and reel database are stored locally on your machine.
- **No Passwords Stored**: We use session states, meaning your password is never saved in the codebase.
- **AI Analysis**: Only the reel captions are sent to Groq for categorization.

---

## 📄 License
MIT License - Created by [Your Name]
