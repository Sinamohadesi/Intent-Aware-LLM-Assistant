import json
import os
import sys


# --------------------------------
# Project root
# --------------------------------

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


from src.llm import ask_llm
from evaluation.normalizer import normalize_category
from evaluation.field_normalizer import normalize_fields


DATASET_PATH = os.path.join(
    ROOT_DIR,
    "evaluation",
    "dataset.json"
)


# --------------------------------
# Intent accuracy
# --------------------------------

def calculate_accuracy(results):

    if not results:
        return 0.0


    correct = 0


    for item in results:

        if item["predicted"] == item["expected"]:
            correct += 1


    return (
        correct / len(results)
    ) * 100


# --------------------------------
# Missing-information metrics
# --------------------------------

def calculate_missing_metrics(results):

    if not results:

        return {
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "exact_match": 0.0
        }


    true_positive = 0
    false_positive = 0
    false_negative = 0

    exact_matches = 0


    for item in results:

        predicted = set(
            normalize_fields(
                item["predicted_missing"]
            )
        )


        expected = set(
            normalize_fields(
                item["expected_missing"]
            )
        )


        true_positive += len(
            predicted & expected
        )


        false_positive += len(
            predicted - expected
        )


        false_negative += len(
            expected - predicted
        )


        if predicted == expected:
            exact_matches += 1


    if true_positive + false_positive == 0:

        precision = (
            100.0
            if true_positive + false_negative == 0
            else 0.0
        )

    else:

        precision = (
            true_positive
            / (
                true_positive
                + false_positive
            )
        ) * 100


    if true_positive + false_negative == 0:

        recall = 100.0

    else:

        recall = (
            true_positive
            / (
                true_positive
                + false_negative
            )
        ) * 100


    if precision + recall == 0:

        f1 = 0.0

    else:

        f1 = (
            2
            * precision
            * recall
            / (
                precision
                + recall
            )
        )


    exact_match = (
        exact_matches
        / len(results)
    ) * 100


    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "exact_match": exact_match
    }


# --------------------------------
# Evaluation
# --------------------------------

def evaluate():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(
            file
        )


    intent_results = []
    missing_results = []

    failed_samples = []


    for index, sample in enumerate(
        dataset,
        start=1
    ):

        response = ask_llm(
            sample["input"]
        )


        try:

            data = json.loads(
                response
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            failed_samples.append(
                {
                    "sample": index,
                    "input": sample["input"],
                    "reason": "Invalid JSON response"
                }
            )

            continue


        # -----------------------------
        # Intent evaluation
        # -----------------------------

        predicted_intent = normalize_category(
            data.get(
                "intent",
                ""
            )
        )


        expected_intent = normalize_category(
            sample.get(
                "expected_intent",
                ""
            )
        )


        intent_results.append(
            {
                "predicted": predicted_intent,
                "expected": expected_intent
            }
        )


        # -----------------------------
        # Missing information evaluation
        # -----------------------------

        missing_results.append(
            {
                "predicted_missing":
                    data.get(
                        "missing_information",
                        []
                    ),

                "expected_missing":
                    sample.get(
                        "expected_missing",
                        []
                    )
            }
        )


    missing_metrics = calculate_missing_metrics(
        missing_results
    )


    # --------------------------------
    # Report
    # --------------------------------

    print()
    print("==============================")
    print("Evaluation Report")
    print("==============================")


    print(
        f"Dataset Samples: {len(dataset)}"
    )


    print(
        f"Successfully Evaluated: {len(intent_results)}"
    )


    print(
        f"Failed Samples: {len(failed_samples)}"
    )


    print()


    print(
        f"Intent Accuracy: "
        f"{calculate_accuracy(intent_results):.2f}%"
    )


    print()


    print("Missing Information Metrics:")


    print(
        f"Precision: "
        f"{missing_metrics['precision']:.2f}%"
    )


    print(
        f"Recall: "
        f"{missing_metrics['recall']:.2f}%"
    )


    print(
        f"F1 Score: "
        f"{missing_metrics['f1']:.2f}%"
    )


    print(
        f"Exact Match: "
        f"{missing_metrics['exact_match']:.2f}%"
    )


    if failed_samples:

        print()
        print("Failed Samples:")


        for item in failed_samples:

            print(
                f"- Sample {item['sample']}: "
                f"{item['reason']}"
            )


    print("==============================")
    print()


if __name__ == "__main__":

    evaluate()