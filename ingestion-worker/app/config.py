
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL", "http://localhost:11434"
).rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

LAYOFFS_API_BASE_URL = os.getenv(
    "LAYOFFS_API_BASE_URL",
    "http://localhost:8080/api/v1",
).rstrip("/")

GOOGLE_NEWS_RSS_URL = os.getenv(
    "GOOGLE_NEWS_RSS_URL",
    "https://news.google.com/rss/search?q=layoffs+India+when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen",
)

NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", "").strip()

MAX_ARTICLES_PER_RUN = int(
    os.getenv("MAX_ARTICLES_PER_RUN", "20")
)
MIN_ARTICLE_TEXT_LENGTH = int(
    os.getenv("MIN_ARTICLE_TEXT_LENGTH", "200")
)
REQUEST_TIMEOUT_SECONDS = int(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "120")
)
SQLITE_PATH = Path(
    os.getenv("SQLITE_PATH", str(PROJECT_ROOT / "data" / "ingestion.sqlite3"))
)
if not SQLITE_PATH.is_absolute():
    SQLITE_PATH = PROJECT_ROOT / SQLITE_PATH

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
