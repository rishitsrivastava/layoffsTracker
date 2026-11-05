
import time

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
    run_start = time.perf_counter()

    print("Starting LayoffsIndia ingestion worker...")

    # 1. Discover articles.
    discovery_start = time.perf_counter()
    articles = discover_articles()
    discovery_time = time.perf_counter() - discovery_start

    print(f"Discovered {len(articles)} articles.")
    print(f"[TIMING] Discovery: {discovery_time:.2f}s")

    # 2. Fetch existing source URLs from backend.
    backend_start = time.perf_counter()
    existing_source_urls = get_existing_source_urls()
    backend_lookup_time = time.perf_counter() - backend_start

    print(f"[TIMING] Backend lookup: {backend_lookup_time:.2f}s")

    stats = {
        "saved": 0,
        "dry_run": 0,
        "duplicates": 0,
        "not_layoff": 0,
        "not_india": 0,
        "needs_review": 0,
        "failed": 0,
    }

    # Aggregate timing measurements.
    total_article_time = 0.0
    total_text_extraction_time = 0.0
    total_llm_time = 0.0
    processed_count = 0

    for article in articles:
        url = article.get("url")

        if not url:
            continue

        article_start = time.perf_counter()

        text_extraction_time = 0.0
        llm_time = 0.0

        try:
            # 1. Skip previously processed articles.
            if is_processed(url):
                print(f"[DUPLICATE - SQLITE] {url}")
                stats["duplicates"] += 1
                continue

            # 2. Skip articles already represented in the backend.
            if url in existing_source_urls:
                print(f"[DUPLICATE - BACKEND] {url}")
                mark_processed(url, "DUPLICATE")
                stats["duplicates"] += 1
                continue

            print(f"\nProcessing: {article.get('title', url)}")

            # 3. Download and extract article text.
            text_start = time.perf_counter()

            article_text = fetch_article_text(article)

            text_extraction_time = time.perf_counter() - text_start

            # 4. Extract structured information using Ollama.
            llm_start = time.perf_counter()

            print("[DEBUG] Calling extract_layoff()")

            extraction = extract_layoff(article, article_text)

            print("[DEBUG] Returned from extract_layoff()")

            llm_time = time.perf_counter() - llm_start

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

        finally:
            article_time = time.perf_counter() - article_start

            total_article_time += article_time
            total_text_extraction_time += text_extraction_time
            total_llm_time += llm_time
            processed_count += 1

            print("\n[TIMING] Detailed breakdown")
            print(f"  Text retrieval: {text_extraction_time:.3f}s")
            print(f"  LLM extraction: {llm_time:.3f}s")
            print(f"  Total article:  {article_time:.3f}s")
            print(
                f"  Unaccounted:    "
                f"{article_time - text_extraction_time - llm_time:.3f}s"
            )
            

    # 10. Final statistics.
    total_run_time = time.perf_counter() - run_start

    print("\nIngestion run complete.")

    for name, count in stats.items():
        print(f"{name}: {count}")

    print("\n========== TIMING SUMMARY ==========")
    print(f"Discovery:              {discovery_time:.2f}s")
    print(f"Backend lookup:         {backend_lookup_time:.2f}s")
    print(f"Article processing:     {total_article_time:.2f}s")
    print(f"  Text retrieval total: {total_text_extraction_time:.2f}s")
    print(f"  LLM extraction total: {total_llm_time:.2f}s")
    print(f"Total run:              {total_run_time:.2f}s")

    if processed_count > 0:
        print("\n========== AVERAGES ==========")
        print(
            f"Average text retrieval: "
            f"{total_text_extraction_time / processed_count:.2f}s"
        )
        print(
            f"Average LLM extraction: "
            f"{total_llm_time / processed_count:.2f}s"
        )
        print(
            f"Average article time: "
            f"{total_article_time / processed_count:.2f}s"
        )


if __name__ == "__main__":
    main()
