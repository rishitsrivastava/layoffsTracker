from googlenewsdecoder import gnewsdecoder

import requests
import feedparser
import trafilatura

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from googlenewsdecoder import gnewsdecoder

from app.config import (
    GOOGLE_NEWS_RSS_URL,
    NEWSAPI_API_KEY,
    MAX_ARTICLES_PER_RUN,
    REQUEST_TIMEOUT_SECONDS,
)


KEYWORDS = (
    "layoff",
    "layoffs",
    "job cuts",
    "workforce reduction",
    "redundancy",
)


def _is_relevant(title: str) -> bool:
    title = title.lower()
    return any(keyword in title for keyword in KEYWORDS)


def fetch_rss_articles() -> list[dict]:
    feed = feedparser.parse(GOOGLE_NEWS_RSS_URL)
    articles = []

    for entry in feed.entries:
        url = entry.get("link")
        title = entry.get("title", "").strip()

        if not url or not title or not _is_relevant(title):
            continue

        source = entry.get("source", {})
        articles.append({
            "title": title,
            "url": url,
            "published_at": entry.get("published"),
            "source_name": source.get("title") if hasattr(source, "get") else None,
            "summary": entry.get("summary", ""),
        })

    return articles


def fetch_newsapi_articles() -> list[dict]:
    # NewsAPI is optional. RSS discovery still works without it.
    if not NEWSAPI_API_KEY:
        return []

    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": '(layoff OR layoffs OR "job cuts" OR "workforce reduction") AND India',
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": min(MAX_ARTICLES_PER_RUN, 100),
            "apiKey": NEWSAPI_API_KEY,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    articles = []

    for item in response.json().get("articles", []):
        url = item.get("url")
        title = (item.get("title") or "").strip()

        if not url or not title or not _is_relevant(title):
            continue

        articles.append({
            "title": title,
            "url": url,
            "published_at": item.get("publishedAt"),
            "source_name": (item.get("source") or {}).get("name"),
            "summary": item.get("description") or "",
        })

    return articles


def discover_articles() -> list[dict]:
    articles = fetch_rss_articles() + fetch_newsapi_articles()

    unique = {}
    for article in articles:
        unique.setdefault(article["url"], article)

    return list(unique.values())[:MAX_ARTICLES_PER_RUN]




def resolve_article_url(url: str) -> str:
    """Resolve a Google News RSS URL to its publisher URL."""
    if "news.google.com" not in url:
        return url

    try:
        result = gnewsdecoder(url, interval=1)

        if (
            result
            and result.get("success") is True
            and result.get("decoded_url")
        ):
            resolved_url = result["decoded_url"]
            print(f"  Publisher URL: {resolved_url}")
            return resolved_url

        print(f"  Google News URL could not be resolved: {result}")

    except Exception as exc:
        print(f"  Google News URL resolution failed: {exc}")

    return url







def fetch_article_text(article: dict) -> str:
    original_url = article["url"]
    resolved_url = resolve_article_url(original_url)

    print(f"  Resolved URL: {resolved_url}")

    text = ""

    try:
        downloaded = trafilatura.fetch_url(resolved_url)

        if downloaded:
            extracted = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False,
            )
            if extracted:
                text = extracted.strip()

    except Exception as exc:
        print(f"  Article download failed: {exc}")

    if len(text) < 200:
        summary = BeautifulSoup(
            article.get("summary", ""),
            "html.parser",
        ).get_text(" ", strip=True)

        if len(summary) > len(text):
            text = summary

    title = article.get("title", "").strip()
    if title and title not in text:
        text = f"{title}\n\n{text}".strip()

    print(f"  Retrieved text length: {len(text)} characters")
    return text

