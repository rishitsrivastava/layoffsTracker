
import sqlite3
from pathlib import Path

import requests

from app.config import (
    LAYOFFS_API_BASE_URL,
    REQUEST_TIMEOUT_SECONDS,
    SQLITE_PATH,
)


def _connect():
    Path(SQLITE_PATH).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(SQLITE_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS processed_articles (
            url TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    return connection


def is_processed(url: str) -> bool:
    with _connect() as connection:
        row = connection.execute(
            "SELECT 1 FROM processed_articles WHERE url = ?",
            (url,),
        ).fetchone()
        return row is not None


def mark_processed(url: str, status: str) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO processed_articles (url, status)
            VALUES (?, ?)
            ON CONFLICT(url) DO UPDATE SET
                status = excluded.status,
                processed_at = CURRENT_TIMESTAMP
            """,
            (url, status),
        )
        connection.commit()


def get_existing_source_urls() -> set[str]:
    response = requests.get(
        f"{LAYOFFS_API_BASE_URL.rstrip('/')}/layoffs",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    records = response.json()
    if not isinstance(records, list):
        raise ValueError("Expected the layoffs API to return a JSON array")

    urls = set()
    for record in records:
        for source in record.get("sources") or []:
            if isinstance(source, str):
                urls.add(source)

    return urls


def save_unverified_candidate(extraction, article: dict) -> dict:
    payload = {
        "companyName": extraction.company_name,
        "employeesAffected": extraction.employees_affected,
        "sources": [article["url"]],
        "country": "India",
        "location": extraction.location,
        "headquarters": extraction.headquarters,
        "layoffDate": extraction.layoff_date,
        "reason": extraction.reason,
        "verificationStatus": "UNVERIFIED",
        "locationStatus": "UNKNOWN",
        "latitude": None,
        "longitude": None,
    }

    response = requests.post(
        f"{LAYOFFS_API_BASE_URL.rstrip('/')}/layoffs",
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    if response.content:
        try:
            return response.json()
        except ValueError:
            pass

    return {"status": "saved"}
