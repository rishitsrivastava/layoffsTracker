
import json
from pathlib import Path

from app.extractor import extract_layoff


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

    field_results = {
        field: {
            "correct": 0,
            "total": 0,
        }
        for field in FIELDS
    }

    false_positives = 0
    false_negatives = 0
    errors = 0

    print("\nStarting LayoffsIndia extraction evaluation...")
    print(f"Loaded {total} test cases.\n")

    for test_case in test_cases:
        test_id = test_case["id"]
        title = test_case["title"]
        article_text = test_case["article_text"]
        expected = test_case["expected"]

        print("=" * 65)
        print(f"Test: {test_id}")
        print(f"Article: {title}")

        article = {
            "title": title,
            "url": f"https://evaluation.local/{test_id}",
        }

        try:
            predicted = extract_layoff(article, article_text)

        except Exception as exc:
            errors += 1
            print(f"ERROR: {type(exc).__name__}: {exc}")
            continue

        predicted_data = predicted.model_dump()

        print("\nPredicted:")
        print(json.dumps(predicted_data, indent=2))

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

        classification_matches = (
            predicted.is_layoff_event
            == expected["is_layoff_event"]
        )

        if classification_matches:
            classification_correct += 1
        elif (
            predicted.is_layoff_event
            and not expected["is_layoff_event"]
        ):
            false_positives += 1
        else:
            false_negatives += 1

    print("\n" + "=" * 65)
    print("EVALUATION SUMMARY")
    print("=" * 65)

    print(f"Total test cases: {total}")
    print(f"Technical errors: {errors}")

    evaluated = total - errors

    if evaluated:
        print(
            "Classification accuracy: "
            f"{classification_correct}/{evaluated} "
            f"({classification_correct / evaluated * 100:.1f}%)"
        )

    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    print("\nField-level accuracy:")

    for field, result in field_results.items():
        if result["total"] == 0:
            continue

        accuracy = (
            result["correct"] / result["total"]
        ) * 100

        print(
            f"{field}: "
            f"{result['correct']}/{result['total']} "
            f"({accuracy:.1f}%)"
        )

    print("\nEvaluation complete.")


if __name__ == "__main__":
    evaluate()
