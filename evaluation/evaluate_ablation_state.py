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

from evaluation.evaluate_multiturn import (
    TEST_CASES
)

from evaluation.field_normalizer import (
    normalize_fields
)


# ==================================================
# HELPERS
# ==================================================

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


# ==================================================
# NO-STATE ABLATION
# ==================================================

def evaluate_no_state_ablation():

    total_conversations = len(
        TEST_CASES
    )

    total_turns = 0

    missing_correct = 0
    clarification_correct = 0

    complete_conversations = 0

    continuation_turns = 0
    continuation_missing_correct = 0
    continuation_clarification_correct = 0

    first_turns = 0
    first_turn_missing_correct = 0
    first_turn_clarification_correct = 0

    failed_turns = []

    print()
    print(
        "=================================================="
    )

    print(
        "Ablation Evaluation"
    )

    print(
        "NO-STATE CONDITION"
    )

    print(
        "=================================================="
    )

    print()
    print(
        "State is intentionally reset before EVERY turn."
    )

    print(
        "The system therefore cannot use information "
        "from previous turns."
    )

    # ==================================================
    # RUN TEST CASES
    # ==================================================

    for conversation_index, test_case in enumerate(
        TEST_CASES,
        start=1
    ):

        conversation_correct = True

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

            # --------------------------------
            # ABLATION:
            # destroy state before every turn
            # --------------------------------

            reset_conversation()

            total_turns += 1

            user_input = turn[
                "input"
            ]

            expected_missing = turn[
                "expected_missing"
            ]

            expected_clarification = turn[
                "expected_clarification"
            ]

            # --------------------------------
            # Run system without prior state
            # --------------------------------

            try:

                result = process_query(
                    user_input
                )

            except Exception as error:

                failed_turns.append(
                    {
                        "conversation":
                            conversation_index,

                        "turn":
                            turn_number,

                        "input":
                            user_input,

                        "error":
                            str(error)
                    }
                )

                conversation_correct = False

                print()
                print(
                    f"Turn {turn_number}"
                )

                print(
                    f"Input: {user_input}"
                )

                print(
                    f"ERROR: {error}"
                )

                continue

            # --------------------------------
            # Read output
            # --------------------------------

            state = result.get(
                "state",
                {}
            )

            predicted_missing = state.get(
                "missing_information",
                []
            )

            predicted_clarification = result.get(
                "needs_clarification",
                False
            )

            # --------------------------------
            # Compare with expected
            # --------------------------------

            missing_match = compare_missing(
                predicted_missing,
                expected_missing
            )

            clarification_match = (
                predicted_clarification
                ==
                expected_clarification
            )

            # --------------------------------
            # Overall metrics
            # --------------------------------

            if missing_match:

                missing_correct += 1

            else:

                conversation_correct = False

            if clarification_match:

                clarification_correct += 1

            else:

                conversation_correct = False

            # --------------------------------
            # First-turn metrics
            # --------------------------------

            if turn_number == 1:

                first_turns += 1

                if missing_match:

                    first_turn_missing_correct += 1

                if clarification_match:

                    first_turn_clarification_correct += 1

            # --------------------------------
            # Continuation-turn metrics
            # --------------------------------

            if turn_number > 1:

                continuation_turns += 1

                if missing_match:

                    continuation_missing_correct += 1

                if clarification_match:

                    continuation_clarification_correct += 1

            # --------------------------------
            # Output
            # --------------------------------

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
                "No-State Prediction:"
            )

            print(
                f"  Missing: "
                f"{predicted_missing}"
            )

            print(
                f"  Clarification: "
                f"{predicted_clarification}"
            )

            print()

            print(
                f"Missing correct: "
                f"{missing_match}"
            )

            print(
                f"Clarification correct: "
                f"{clarification_match}"
            )

        # --------------------------------
        # Complete-conversation metric
        # --------------------------------

        if conversation_correct:

            complete_conversations += 1

    # ==================================================
    # CALCULATE METRICS
    # ==================================================

    missing_accuracy = percentage(
        missing_correct,
        total_turns
    )

    clarification_accuracy = percentage(
        clarification_correct,
        total_turns
    )

    conversation_accuracy = percentage(
        complete_conversations,
        total_conversations
    )

    first_turn_missing_accuracy = percentage(
        first_turn_missing_correct,
        first_turns
    )

    first_turn_clarification_accuracy = percentage(
        first_turn_clarification_correct,
        first_turns
    )

    continuation_missing_accuracy = percentage(
        continuation_missing_correct,
        continuation_turns
    )

    continuation_clarification_accuracy = percentage(
        continuation_clarification_correct,
        continuation_turns
    )

    # ==================================================
    # FULL SYSTEM CANONICAL REFERENCE
    # ==================================================

    full_missing_accuracy = 100.00
    full_clarification_accuracy = 100.00
    full_conversation_accuracy = 100.00
    full_continuation_accuracy = 100.00

    # ==================================================
    # FINAL REPORT
    # ==================================================

    print()
    print(
        "=================================================="
    )

    print(
        "No-State Ablation Results"
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
        f"First Turns: "
        f"{first_turns}"
    )

    print(
        f"Continuation Turns: "
        f"{continuation_turns}"
    )

    print(
        f"Failed Turns: "
        f"{len(failed_turns)}"
    )

    # --------------------------------
    # Overall
    # --------------------------------

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "1. Overall Missing Information Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Full System: "
        f"{full_missing_accuracy:.2f}%"
    )

    print(
        f"No-State: "
        f"{missing_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{missing_accuracy - full_missing_accuracy:+.2f} pp"
    )

    # --------------------------------

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "2. Overall Clarification Decision Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Full System: "
        f"{full_clarification_accuracy:.2f}%"
    )

    print(
        f"No-State: "
        f"{clarification_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{clarification_accuracy - full_clarification_accuracy:+.2f} pp"
    )

    # --------------------------------

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
        f"Full System: "
        f"{full_conversation_accuracy:.2f}%"
    )

    print(
        f"No-State: "
        f"{conversation_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{conversation_accuracy - full_conversation_accuracy:+.2f} pp"
    )

    # --------------------------------
    # First turn
    # --------------------------------

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "4. First-Turn Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Missing Information Accuracy: "
        f"{first_turn_missing_accuracy:.2f}%"
    )

    print(
        f"Clarification Decision Accuracy: "
        f"{first_turn_clarification_accuracy:.2f}%"
    )

    # --------------------------------
    # Continuation turns
    # --------------------------------

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "5. Continuation-Turn Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Full System State Accuracy: "
        f"{full_continuation_accuracy:.2f}%"
    )

    print(
        f"No-State Missing Accuracy: "
        f"{continuation_missing_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{continuation_missing_accuracy - full_continuation_accuracy:+.2f} pp"
    )

    print()

    print(
        f"No-State Clarification Accuracy: "
        f"{continuation_clarification_accuracy:.2f}%"
    )

    # ==================================================
    # FAILURES
    # ==================================================

    if failed_turns:

        print()
        print(
            "--------------------------------------------------"
        )

        print(
            "Failed Turns"
        )

        print(
            "--------------------------------------------------"
        )

        for failure in failed_turns:

            print()

            print(
                f"Conversation: "
                f"{failure['conversation']}"
            )

            print(
                f"Turn: "
                f"{failure['turn']}"
            )

            print(
                f"Input: "
                f"{failure['input']}"
            )

            print(
                f"Error: "
                f"{failure['error']}"
            )

    # ==================================================
    # RESEARCH INTERPRETATION
    # ==================================================

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
        first_turn_missing_accuracy
        >
        continuation_missing_accuracy
    ):

        print(
            "Removing state had a larger negative effect "
            "on continuation turns than on initial turns."
        )

    if continuation_missing_accuracy < 100:

        print(
            "The result indicates that explicit state tracking "
            "contributes to preserving previously supplied "
            "user information across turns."
        )

    if conversation_accuracy < 100:

        print(
            "Without state persistence, complete multi-turn "
            "conversation reliability decreased."
        )

    print(
        "=================================================="
    )

    print()


if __name__ == "__main__":

    evaluate_no_state_ablation()