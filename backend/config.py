import os
from pathlib import Path
from dotenv import load_dotenv

# Locate base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

class Settings:
    # LLM Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    
    # Server Settings
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1").strip()
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "20"))
    
    # Storage Paths
    BASE_DIR: Path = BASE_DIR
    STORAGE_DIR: Path = BASE_DIR / "storage"
    UPLOADS_DIR: Path = BASE_DIR / "storage" / "uploads"
    INDEXES_DIR: Path = BASE_DIR / "storage" / "indexes"
    EXPORTS_DIR: Path = BASE_DIR / "storage" / "exports"
    DB_PATH: Path = BASE_DIR / "storage" / "research_iq.db"
    
    # RAG Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    CHUNK_SIZE: int = 750
    CHUNK_OVERLAP: int = 150
    DEFAULT_TOP_K: int = 6
    RRF_K: int = 60
    SIMILARITY_THRESHOLD: float = 0.25

    @classmethod
    def reload(cls):
        """Reload configuration from .env file."""
        if ENV_PATH.exists():
            load_dotenv(dotenv_path=ENV_PATH, override=True)
        cls.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
        cls.GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
        cls.APP_HOST = os.getenv("APP_HOST", "127.0.0.1").strip()
        cls.APP_PORT = int(os.getenv("APP_PORT", "8000"))
        cls.MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "20"))

    @classmethod
    def save_settings(cls, groq_api_key: str = None, groq_model: str = None):
        """Update and save settings to the .env file."""
        if groq_api_key is not None:
            cls.GROQ_API_KEY = groq_api_key.strip()
        if groq_model is not None:
            cls.GROQ_MODEL = groq_model.strip()

        lines = []
        if ENV_PATH.exists():
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()

        keys_set = set()
        new_lines = []
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("GROQ_API_KEY="):
                new_lines.append(f"GROQ_API_KEY={cls.GROQ_API_KEY}\n")
                keys_set.add("GROQ_API_KEY")
            elif line_str.startswith("GROQ_MODEL="):
                new_lines.append(f"GROQ_MODEL={cls.GROQ_MODEL}\n")
                keys_set.add("GROQ_MODEL")
            else:
                new_lines.append(line)

        if "GROQ_API_KEY" not in keys_set:
            new_lines.append(f"GROQ_API_KEY={cls.GROQ_API_KEY}\n")
        if "GROQ_MODEL" not in keys_set:
            new_lines.append(f"GROQ_MODEL={cls.GROQ_MODEL}\n")

        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
        cls.reload()

# Ensure directories exist
Settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
Settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
Settings.INDEXES_DIR.mkdir(parents=True, exist_ok=True)
Settings.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
