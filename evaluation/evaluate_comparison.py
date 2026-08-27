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


from src.main import (
    process_query,
    reset_conversation
)

from evaluation.evaluate_baseline import (
    ask_baseline
)

from evaluation.evaluate_multiturn import (
    TEST_CASES
)

from evaluation.field_normalizer import (
    normalize_fields
)


# --------------------------------
# Helpers
# --------------------------------

def compare_missing(
    predicted,
    expected
):

    predicted_normalized = set(
        normalize_fields(
            predicted
        )
    )

    expected_normalized = set(
        normalize_fields(
            expected
        )
    )

    return (
        predicted_normalized
        ==
        expected_normalized
    )


def percentage(
    correct,
    total
):

    if total == 0:
        return 0.0

    return (
        correct / total
    ) * 100


# --------------------------------
# Main comparison
# --------------------------------

def evaluate_comparison():

    # --------------------------------
    # Global counters
    # --------------------------------

    total_turns = 0

    adaptive_missing_correct = 0
    baseline_missing_correct = 0

    adaptive_action_correct = 0
    baseline_action_correct = 0

    adaptive_complete_conversations = 0
    baseline_complete_conversations = 0

    # --------------------------------
    # Continuation-turn metrics
    # --------------------------------

    continuation_turns = 0

    adaptive_continuation_missing_correct = 0
    baseline_continuation_missing_correct = 0

    # --------------------------------
    # Incomplete-input behavior
    # --------------------------------

    clarification_required_turns = 0

    adaptive_premature_direct_answers = 0
    baseline_premature_direct_answers = 0

    # --------------------------------
    # Complete-input behavior
    # --------------------------------

    complete_input_turns = 0

    adaptive_complete_input_correct = 0
    baseline_complete_input_correct = 0

    # --------------------------------
    # Failure handling
    # --------------------------------

    baseline_failed_samples = []

    print()
    print(
        "=================================================="
    )

    print(
        "Comparative Evaluation"
    )

    print(
        "Intent-Aware Adaptive Assistant"
    )

    print(
        "vs"
    )

    print(
        "Direct-Answer Baseline"
    )

    print(
        "=================================================="
    )

    # --------------------------------
    # Conversations
    # --------------------------------

    for conversation_index, test_case in enumerate(
        TEST_CASES,
        start=1
    ):

        reset_conversation()

        adaptive_conversation_correct = True
        baseline_conversation_correct = True

        print()
        print(
            "--------------------------------------------------"
        )

        print(
            f"Conversation {conversation_index}: "
            f"{test_case['name']}"
        )

        print(
            "--------------------------------------------------"
        )

        for turn_number, turn in enumerate(
            test_case["turns"],
            start=1
        ):

            total_turns += 1

            user_input = turn["input"]

            expected_missing = turn[
                "expected_missing"
            ]

            expected_clarification = turn[
                "expected_clarification"
            ]

            # ==========================================
            # Intent-Aware Adaptive Assistant
            # ==========================================

            adaptive_result = process_query(
                user_input
            )

            adaptive_state = adaptive_result.get(
                "state",
                {}
            )

            adaptive_missing = adaptive_state.get(
                "missing_information",
                []
            )

            adaptive_clarification = adaptive_result.get(
                "needs_clarification",
                False
            )

            adaptive_missing_match = compare_missing(
                adaptive_missing,
                expected_missing
            )

            adaptive_action_match = (
                adaptive_clarification
                ==
                expected_clarification
            )

            if adaptive_missing_match:
                adaptive_missing_correct += 1

            else:
                adaptive_conversation_correct = False

            if adaptive_action_match:
                adaptive_action_correct += 1

            else:
                adaptive_conversation_correct = False

            # ==========================================
            # Direct-Answer Baseline
            # ==========================================

            baseline_response = ask_baseline(
                user_input
            )

            try:

                baseline_data = json.loads(
                    baseline_response
                )

            except (
                json.JSONDecodeError,
                TypeError
            ):

                baseline_failed_samples.append(
                    {
                        "conversation":
                            conversation_index,

                        "turn":
                            turn_number,

                        "input":
                            user_input
                    }
                )

                baseline_missing = []
                baseline_clarification = False

                baseline_missing_match = False
                baseline_action_match = False

                baseline_conversation_correct = False

            else:

                baseline_missing = baseline_data.get(
                    "missing_information",
                    []
                )

                baseline_clarification = bool(
                    baseline_data.get(
                        "clarification_attempted",
                        False
                    )
                )

                baseline_missing_match = compare_missing(
                    baseline_missing,
                    expected_missing
                )

                baseline_action_match = (
                    baseline_clarification
                    ==
                    expected_clarification
                )

                if baseline_missing_match:

                    baseline_missing_correct += 1

                else:

                    baseline_conversation_correct = False

                if baseline_action_match:

                    baseline_action_correct += 1

                else:

                    baseline_conversation_correct = False

            # ==========================================
            # Continuation-turn evaluation
            # ==========================================

            if turn_number > 1:

                continuation_turns += 1

                if adaptive_missing_match:

                    adaptive_continuation_missing_correct += 1

                if baseline_missing_match:

                    baseline_continuation_missing_correct += 1

            # ==========================================
            # Incomplete-prompt evaluation
            # ==========================================

            if expected_clarification:

                clarification_required_turns += 1

                if not adaptive_clarification:

                    adaptive_premature_direct_answers += 1

                if not baseline_clarification:

                    baseline_premature_direct_answers += 1

            # ==========================================
            # Complete-prompt evaluation
            # ==========================================

            if not expected_clarification:

                complete_input_turns += 1

                if not adaptive_clarification:

                    adaptive_complete_input_correct += 1

                if not baseline_clarification:

                    baseline_complete_input_correct += 1

            # ==========================================
            # Per-turn output
            # ==========================================

            print()
            print(
                f"Turn {turn_number}"
            )

            print(
                f"Input:"
            )

            print(
                f"  {user_input}"
            )

            print()

            print(
                "Expected:"
            )

            print(
                f"  Missing: "
                f"{expected_missing}"
            )

            print(
                f"  Clarification: "
                f"{expected_clarification}"
            )

            print()

            print(
                "Adaptive:"
            )

            print(
                f"  Missing: "
                f"{adaptive_missing}"
            )

            print(
                f"  Clarification: "
                f"{adaptive_clarification}"
            )

            print(
                f"  Missing correct: "
                f"{adaptive_missing_match}"
            )

            print(
                f"  Action correct: "
                f"{adaptive_action_match}"
            )

            print()

            print(
                "Baseline:"
            )

            print(
                f"  Missing: "
                f"{baseline_missing}"
            )

            print(
                f"  Clarification: "
                f"{baseline_clarification}"
            )

            print(
                f"  Missing correct: "
                f"{baseline_missing_match}"
            )

            print(
                f"  Action correct: "
                f"{baseline_action_match}"
            )

        # --------------------------------
        # Conversation-level success
        # --------------------------------

        if adaptive_conversation_correct:

            adaptive_complete_conversations += 1

        if baseline_conversation_correct:

            baseline_complete_conversations += 1

    # ==========================================
    # Final metrics
    # ==========================================

    total_conversations = len(
        TEST_CASES
    )

    adaptive_missing_accuracy = percentage(
        adaptive_missing_correct,
        total_turns
    )

    baseline_missing_accuracy = percentage(
        baseline_missing_correct,
        total_turns
    )

    adaptive_action_accuracy = percentage(
        adaptive_action_correct,
        total_turns
    )

    baseline_action_accuracy = percentage(
        baseline_action_correct,
        total_turns
    )

    adaptive_conversation_accuracy = percentage(
        adaptive_complete_conversations,
        total_conversations
    )

    baseline_conversation_accuracy = percentage(
        baseline_complete_conversations,
        total_conversations
    )

    adaptive_continuation_accuracy = percentage(
        adaptive_continuation_missing_correct,
        continuation_turns
    )

    baseline_continuation_accuracy = percentage(
        baseline_continuation_missing_correct,
        continuation_turns
    )

    adaptive_premature_rate = percentage(
        adaptive_premature_direct_answers,
        clarification_required_turns
    )

    baseline_premature_rate = percentage(
        baseline_premature_direct_answers,
        clarification_required_turns
    )

    adaptive_complete_input_accuracy = percentage(
        adaptive_complete_input_correct,
        complete_input_turns
    )

    baseline_complete_input_accuracy = percentage(
        baseline_complete_input_correct,
        complete_input_turns
    )

    # ==========================================
    # Summary
    # ==========================================

    print()
    print(
        "=================================================="
    )

    print(
        "Comparative Evaluation Results"
    )

    print(
        "=================================================="
    )

    print()

    print(
        f"Total Conversations: "
        f"{total_conversations}"
    )

    print(
        f"Total Turns: "
        f"{total_turns}"
    )

    print(
        f"Continuation Turns: "
        f"{continuation_turns}"
    )

    print(
        f"Clarification-Required Turns: "
        f"{clarification_required_turns}"
    )

    print(
        f"Complete-Input Turns: "
        f"{complete_input_turns}"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "1. Missing Information Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Adaptive: "
        f"{adaptive_missing_accuracy:.2f}%"
    )

    print(
        f"Baseline: "
        f"{baseline_missing_accuracy:.2f}%"
    )

    print(
        f"Difference: "
        f"{adaptive_missing_accuracy - baseline_missing_accuracy:+.2f} pp"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "2. Clarification Decision Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Adaptive: "
        f"{adaptive_action_accuracy:.2f}%"
    )

    print(
        f"Baseline: "
        f"{baseline_action_accuracy:.2f}%"
    )

    print(
        f"Difference: "
        f"{adaptive_action_accuracy - baseline_action_accuracy:+.2f} pp"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "3. Complete Conversation Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Adaptive: "
        f"{adaptive_conversation_accuracy:.2f}%"
    )

    print(
        f"Baseline: "
        f"{baseline_conversation_accuracy:.2f}%"
    )

    print(
        f"Difference: "
        f"{adaptive_conversation_accuracy - baseline_conversation_accuracy:+.2f} pp"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "4. Continuation-Turn State Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Adaptive: "
        f"{adaptive_continuation_accuracy:.2f}%"
    )

    print(
        f"Baseline: "
        f"{baseline_continuation_accuracy:.2f}%"
    )

    print(
        f"Difference: "
        f"{adaptive_continuation_accuracy - baseline_continuation_accuracy:+.2f} pp"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "5. Premature Direct-Answer Rate"
    )

    print(
        "Lower is better."
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Adaptive: "
        f"{adaptive_premature_rate:.2f}%"
    )

    print(
        f"Baseline: "
        f"{baseline_premature_rate:.2f}%"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "6. Complete-Input Handling Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Adaptive: "
        f"{adaptive_complete_input_accuracy:.2f}%"
    )

    print(
        f"Baseline: "
        f"{baseline_complete_input_accuracy:.2f}%"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "7. Baseline Failures"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Failed Baseline Calls: "
        f"{len(baseline_failed_samples)}"
    )

    if baseline_failed_samples:

        for failure in baseline_failed_samples:

            print(
                f"- Conversation "
                f"{failure['conversation']}, "
                f"Turn "
                f"{failure['turn']}: "
                f"{failure['input']}"
            )

    print()

    print(
        "=================================================="
    )

    print(
        "Research Interpretation"
    )

    print(
        "=================================================="
    )

    if (
        adaptive_action_accuracy
        >
        baseline_action_accuracy
    ):

        print(
            "The adaptive system made more appropriate "
            "clarification decisions than the direct-answer baseline."
        )

    if (
        adaptive_continuation_accuracy
        >
        baseline_continuation_accuracy
    ):

        print(
            "The adaptive system handled multi-turn context "
            "more reliably through explicit state tracking."
        )

    if (
        adaptive_premature_rate
        <
        baseline_premature_rate
    ):

        print(
            "The adaptive system reduced premature answers "
            "when important information was still missing."
        )

    if (
        adaptive_complete_input_accuracy
        ==
        baseline_complete_input_accuracy
    ):

        print(
            "Both systems remained capable of answering "
            "when the request was already complete."
        )

    print(
        "=================================================="
    )

    print()


if __name__ == "__main__":

    evaluate_comparison()