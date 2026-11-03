
from app.config import DRY_RUN
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
        "dry_run": 0,
        "duplicates": 0,
        "not_layoff": 0,
        "not_india": 0,
        "needs_review": 0,
        "failed": 0,
    }

    for article in articles:
        url = article.get("url")

        if not url:
            continue

        try:
            # 1. Skip previously processed articles.
            if is_processed(url):
                stats["duplicates"] += 1
                continue

            # 2. Skip articles already represented in the backend.
            if url in existing_source_urls:
                mark_processed(url, "DUPLICATE")
                stats["duplicates"] += 1
                continue

            print(f"\nProcessing: {article.get('title', url)}")

            # 3. Download and extract article text.
            article_text = fetch_article_text(article)

            # 4. Extract structured information using Ollama.
            extraction = extract_layoff(article, article_text)

            print("\nExtraction result:")
            print(extraction.model_dump_json(indent=2))

            # 5. Reject articles that do not report a specific event.
            if not extraction.is_layoff_event:
                mark_processed(url, "NOT_A_LAYOFF")
                stats["not_layoff"] += 1
                continue

            # 6. Company name is required for an identifiable candidate.
            if not extraction.company_name:
                print("Skipping: company name requires manual review.")

                mark_processed(url, "NEEDS_REVIEW")
                stats["needs_review"] += 1
                continue

            # 7. Country must explicitly identify India.
            if (extraction.country or "").strip().lower() != "india":
                print("Skipping: India impact is not established.")

                mark_processed(url, "NOT_CONFIRMED_INDIA")
                stats["not_india"] += 1
                continue

            # 8. Dry run: display candidate without saving it.
            if DRY_RUN:
                print("\nDRY RUN — candidate not saved.")
                print(extraction.model_dump_json(indent=2))

                stats["dry_run"] += 1
                continue

            # 9. Persist candidate as UNVERIFIED.
            save_unverified_candidate(article, extraction)

            mark_processed(url, "SAVED_UNVERIFIED")
            existing_source_urls.add(url)

            stats["saved"] += 1

        except Exception as exc:
            stats["failed"] += 1

            print(
                f"\n[FAILED] {article.get('title', 'Unknown article')}"
            )
            print(f"URL: {url}")
            print(f"Error: {type(exc).__name__}: {exc}")

            # Do not mark technical failures as processed.
            # They can be retried during the next run.

    print("\nIngestion run complete.")

    for name, count in stats.items():
        print(f"{name}: {count}")


if __name__ == "__main__":
    main()
