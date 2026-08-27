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


from src.llm import call_llm
from evaluation.normalizer import normalize_category
from evaluation.field_normalizer import normalize_fields


DATASET_PATH = os.path.join(
    ROOT_DIR,
    "evaluation",
    "dataset.json"
)


# --------------------------------
# Direct-answer baseline prompt
# --------------------------------

BASELINE_SYSTEM_PROMPT = """
You are a simple direct-answer university recommendation assistant.

Your purpose is to act as a baseline system for a research experiment.

You must analyze ONLY the CURRENT user message.

You do NOT have:
- conversation state
- persistent memory
- adaptive clarification
- previous-turn information
- state restoration

You must NOT ask the user a follow-up question.

Even when important information is missing, you must still attempt
to produce a direct answer based only on the current message.

For university recommendation requests:

Intent:
"recommendation"

The relevant information fields are:

- country
- field
- requirements


Definitions:

country:
The country or region where the user wants to study.

field:
The main academic field, degree subject, major, or program
the user wants to study.

requirements:
Additional preferences, constraints, qualifications,
research interests, or requirements.

Examples:
- tuition preference
- IELTS score
- ranking preference
- language requirement
- intake
- budget
- research interests
- specialization preferences
- Machine Learning
- Computer Vision
- Natural Language Processing
- Robotics
- Deep Learning


Important rules:

1. Analyze ONLY the current user message.

2. Do not invent information that the user did not provide.

3. Put explicitly provided information inside
   "required_information".

4. Put absent fields inside "missing_information".

5. Do NOT ask clarification questions.

6. Always choose:
   "action": "direct_answer"

7. "clarification_attempted" must always be false.

8. If information is incomplete, acknowledge uncertainty or missing
   context briefly inside "answer", but still provide a direct response.

9. Research interests should normally be treated as requirements,
   not automatically as the main academic field.

10. Return ONLY valid JSON.

11. Do not include markdown or text outside the JSON object.


Example 1

User:
Help me choose a university

Output:

{
    "intent": "recommendation",
    "confidence": 0.90,
    "required_information": {},
    "missing_information": [
        "country",
        "field",
        "requirements"
    ],
    "action": "direct_answer",
    "clarification_attempted": false,
    "answer": "Based on the limited information available, I can only provide a general university recommendation rather than a personalized shortlist."
}


Example 2

User:
Germany and Artificial Intelligence

Output:

{
    "intent": "recommendation",
    "confidence": 0.95,
    "required_information": {
        "country": "Germany",
        "field": "Artificial Intelligence"
    },
    "missing_information": [
        "requirements"
    ],
    "action": "direct_answer",
    "clarification_attempted": false,
    "answer": "For Artificial Intelligence in Germany, several universities may be relevant, but the recommendation cannot be fully personalized because additional requirements were not provided."
}


Example 3

User:
Recommend universities in Germany for Artificial Intelligence with low tuition

Output:

{
    "intent": "recommendation",
    "confidence": 0.95,
    "required_information": {
        "country": "Germany",
        "field": "Artificial Intelligence",
        "requirements": "low tuition"
    },
    "missing_information": [],
    "action": "direct_answer",
    "clarification_attempted": false,
    "answer": "Based on the provided preferences, German universities offering Artificial Intelligence with relatively low tuition should be prioritized."
}


Required JSON structure:

{
    "intent": "",
    "confidence": 0.0,
    "required_information": {},
    "missing_information": [],
    "action": "direct_answer",
    "clarification_attempted": false,
    "answer": ""
}
"""


# --------------------------------
# Baseline model call
# --------------------------------

def ask_baseline(prompt):

    return call_llm(
        prompt=prompt,
        system_prompt=BASELINE_SYSTEM_PROMPT,
        json_mode=True,
        temperature=0.0
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
# Baseline policy metrics
# --------------------------------

def calculate_policy_metrics(results):

    if not results:

        return {
            "direct_answer_rate": 0.0,
            "incomplete_direct_answer_rate": 0.0,
            "clarification_attempt_rate": 0.0
        }

    direct_answers = 0
    clarification_attempts = 0

    incomplete_samples = 0
    incomplete_direct_answers = 0

    for item in results:

        if item["action"] == "direct_answer":
            direct_answers += 1

        if item["clarification_attempted"]:
            clarification_attempts += 1

        expected_missing = normalize_fields(
            item["expected_missing"]
        )

        if expected_missing:

            incomplete_samples += 1

            if item["action"] == "direct_answer":
                incomplete_direct_answers += 1

    direct_answer_rate = (
        direct_answers
        / len(results)
    ) * 100

    clarification_attempt_rate = (
        clarification_attempts
        / len(results)
    ) * 100

    if incomplete_samples == 0:

        incomplete_direct_answer_rate = 0.0

    else:

        incomplete_direct_answer_rate = (
            incomplete_direct_answers
            / incomplete_samples
        ) * 100

    return {
        "direct_answer_rate":
            direct_answer_rate,

        "incomplete_direct_answer_rate":
            incomplete_direct_answer_rate,

        "clarification_attempt_rate":
            clarification_attempt_rate
    }


# --------------------------------
# Evaluation
# --------------------------------

def evaluate_baseline():

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
    policy_results = []

    failed_samples = []

    print()
    print(
        "======================================"
    )

    print(
        "Direct-Answer Baseline Evaluation"
    )

    print(
        "======================================"
    )

    for index, sample in enumerate(
        dataset,
        start=1
    ):

        response = ask_baseline(
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
        # Missing information
        # -----------------------------

        predicted_missing = data.get(
            "missing_information",
            []
        )

        expected_missing = sample.get(
            "expected_missing",
            []
        )

        missing_results.append(
            {
                "predicted_missing":
                    predicted_missing,

                "expected_missing":
                    expected_missing
            }
        )

        # -----------------------------
        # Baseline policy
        # -----------------------------

        action = str(
            data.get(
                "action",
                ""
            )
        ).strip().lower()

        clarification_attempted = bool(
            data.get(
                "clarification_attempted",
                False
            )
        )

        policy_results.append(
            {
                "action":
                    action,

                "clarification_attempted":
                    clarification_attempted,

                "expected_missing":
                    expected_missing
            }
        )

        # -----------------------------
        # Per-sample report
        # -----------------------------

        print()
        print(
            f"Sample {index}:"
        )

        print(
            f"  Input: "
            f"{sample['input']}"
        )

        print(
            f"  Intent: "
            f"{predicted_intent}"
        )

        print(
            f"  Missing: "
            f"{predicted_missing}"
        )

        print(
            f"  Action: "
            f"{action}"
        )

        print(
            f"  Clarification attempted: "
            f"{clarification_attempted}"
        )

    # --------------------------------
    # Calculate final metrics
    # --------------------------------

    missing_metrics = calculate_missing_metrics(
        missing_results
    )

    policy_metrics = calculate_policy_metrics(
        policy_results
    )

    # --------------------------------
    # Final report
    # --------------------------------

    print()
    print(
        "======================================"
    )

    print(
        "Baseline Final Results"
    )

    print(
        "======================================"
    )

    print(
        f"Dataset Samples: "
        f"{len(dataset)}"
    )

    print(
        f"Successfully Evaluated: "
        f"{len(intent_results)}"
    )

    print(
        f"Failed Samples: "
        f"{len(failed_samples)}"
    )

    print()

    print(
        f"Intent Accuracy: "
        f"{calculate_accuracy(intent_results):.2f}%"
    )

    print()

    print(
        "Missing Information Metrics:"
    )

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

    print()

    print(
        "Direct-Answer Policy Metrics:"
    )

    print(
        f"Direct Answer Rate: "
        f"{policy_metrics['direct_answer_rate']:.2f}%"
    )

    print(
        f"Incomplete-Prompt Direct Answer Rate: "
        f"{policy_metrics['incomplete_direct_answer_rate']:.2f}%"
    )

    print(
        f"Clarification Attempt Rate: "
        f"{policy_metrics['clarification_attempt_rate']:.2f}%"
    )

    if failed_samples:

        print()
        print(
            "Failed Samples:"
        )

        for item in failed_samples:

            print(
                f"- Sample {item['sample']}: "
                f"{item['reason']}"
            )

    print(
        "======================================"
    )

    print()


if __name__ == "__main__":

    evaluate_baseline()