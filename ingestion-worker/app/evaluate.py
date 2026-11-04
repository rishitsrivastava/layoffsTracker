
import json
from pathlib import Path

from app.extractor import extract_layoff
from app.feeds import fetch_article_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "evaluation_articles.json"
)

FIELDS = [
    "is_layoff_event",
    "company_name",
    "employees_affected",
    "country",
]


def normalize(value):
    if isinstance(value, str):
        return value.strip().casefold()

    return value


def evaluate():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    total = len(test_cases)
    classification_correct = 0
    false_positives = 0
    false_negatives = 0
    errors = 0

    field_results = {
        field: {"correct": 0, "total": 0}
        for field in FIELDS
    }

    print("\nStarting LayoffsIndia real-world evaluation...")
    print(f"Loaded {total} test cases.\n")

    for test_case in test_cases:
        test_id = test_case["id"]
        title = test_case["title"]
        url = test_case["url"]
        expected = test_case["expected"]

        print("\n" + "=" * 70)
        print(f"Test: {test_id}")
        print(f"Article: {title}")
        print(f"URL: {url}")

        article = {
            "title": title,
            "url": url,
            "summary": "",
        }

        try:
            # Download the actual publisher article.
            article_text = fetch_article_text(article)

            if len(article_text) < 200:
                print("\nARTICLE RETRIEVAL DEBUG:")
                print(f"URL: {url}")
                print(f"Retrieved text: {article_text!r}")
                print("Skipping LLM extraction.")
                errors += 1
                continue

            if not article_text.strip():
                raise ValueError("No article text could be retrieved")

            print(f"Article text length: {len(article_text)}")

            # Run the existing Ollama extraction.
            predicted = extract_layoff(article, article_text)
            predicted_data = predicted.model_dump()

            print("\nPredicted:")
            print(json.dumps(predicted_data, indent=2))

        except Exception as exc:
            errors += 1
            print(
                f"\nERROR: {type(exc).__name__}: {exc}"
            )
            print("This test was not included in accuracy calculations.")
            continue

        print("\nComparison:")

        for field in FIELDS:
            expected_value = expected.get(field)
            predicted_value = predicted_data.get(field)

            field_results[field]["total"] += 1

            correct = (
                normalize(expected_value)
                == normalize(predicted_value)
            )

            if correct:
                field_results[field]["correct"] += 1
                status = "PASS"
            else:
                status = "FAIL"

            print(
                f"{field}: {status} "
                f"(expected={expected_value!r}, "
                f"predicted={predicted_value!r})"
            )

        if predicted.is_layoff_event == expected["is_layoff_event"]:
            classification_correct += 1

        elif predicted.is_layoff_event:
            false_positives += 1

        else:
            false_negatives += 1

    evaluated = total - errors

    print("\n" + "=" * 70)
    print("REAL-WORLD EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total articles: {total}")
    print(f"Successfully evaluated: {evaluated}")
    print(f"Technical errors: {errors}")

    if evaluated:
        accuracy = classification_correct / evaluated * 100

        print(
            f"Classification accuracy: "
            f"{classification_correct}/{evaluated} "
            f"({accuracy:.1f}%)"
        )

    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    print("\nField-level accuracy:")

    for field, result in field_results.items():
        if result["total"] == 0:
            print(f"{field}: No results")
            continue

        accuracy = result["correct"] / result["total"] * 100

        print(
            f"{field}: {result['correct']}/{result['total']} "
            f"({accuracy:.1f}%)"
        )

    print("\nEvaluation complete.")


if __name__ == "__main__":
    evaluate()
