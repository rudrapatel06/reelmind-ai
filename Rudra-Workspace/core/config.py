import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reelmind.db")
    # Local Chroma DB folder, no host/port needed


settings = Settings()

# --- FFmpeg Auto-Pathing Fix ---
try:
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    if ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] += os.pathsep + ffmpeg_dir
except ImportError:
    pass
