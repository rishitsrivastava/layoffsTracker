
from app.config import DRY_RUN, MAX_ARTICLES_PER_RUN
from app.extractor import extract_layoff
from app.feeds import discover_articles, fetch_article_text
from app.persistence import (
    get_existing_source_urls,
    is_processed,
    mark_processed,
    save_unverified_candidate,
)


def main():
    print("Starting LayoffsIndia ingestion worker...")

    articles = discover_articles()
    print(f"Discovered {len(articles)} articles.")

    existing_source_urls = get_existing_source_urls()

    stats = {
        "saved": 0,
        "duplicates": 0,
        "not_layoff": 0,
        "not_india": 0,
        "failed": 0,
    }

    for article in articles:
        url = article.get("url")

        if not url:
            continue

        try:
            if is_processed(url):
                stats["duplicates"] += 1
                continue

            if url in existing_source_urls:
                mark_processed(url, "DUPLICATE")
                stats["duplicates"] += 1
                continue

            print(f"\nProcessing: {article.get('title', url)}")

            article_text = fetch_article_text(article)
            extraction = extract_layoff(article, article_text)

            print("Extraction result:")
            print(extraction.model_dump_json(indent=2))

            if not extraction.is_layoff_event:
                mark_processed(url, "NOT_A_LAYOFF")
                stats["not_layoff"] += 1
                continue

            if not extraction.company_name:
                print("Skipping: company name could not be extracted.")
                stats["failed"] += 1
                continue

            if (extraction.country or "").strip().lower() != "india":
                mark_processed(url, "NOT_CONFIRMED_INDIA")
                stats["not_india"] += 1
                continue

            if DRY_RUN:
                print("DRY RUN — candidate not saved")
                print(extraction.model_dump_json(indent=2))
                stats["saved"] += 1
                continue

            save_unverified_candidate(article, extraction)
            mark_processed(url, "SAVED_UNVERIFIED")
            existing_source_urls.add(url)
            stats["saved"] += 1

        except Exception as exc:
            stats["failed"] += 1
            print(
                f"[FAILED] {article.get('title', 'Unknown article')}"
            )
            print(f"  URL: {article.get('url', 'Unknown URL')}")
            print(f"  Error: {type(exc).__name__}: {exc}")

    print("\nIngestion run complete.")
    for name, count in stats.items():
        print(f"{name}: {count}")


if __name__ == "__main__":
    main()
