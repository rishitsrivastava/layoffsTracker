import os
from pathlib import Path
from dotenv import load_dotenv

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/");

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b");

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true";