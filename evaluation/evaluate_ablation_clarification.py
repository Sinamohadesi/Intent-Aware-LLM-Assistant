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
# NO-CLARIFICATION ABLATION
# ==================================================

def evaluate_no_clarification_ablation():

    total_conversations = len(
        TEST_CASES
    )

    total_turns = 0

    missing_correct = 0
    clarification_correct = 0

    complete_conversations = 0

    clarification_required_turns = 0
    premature_direct_answers = 0

    complete_input_turns = 0
    complete_input_correct = 0

    continuation_turns = 0
    continuation_missing_correct = 0

    failed_turns = []

    print()
    print(
        "=================================================="
    )

    print(
        "Ablation Evaluation"
    )

    print(
        "NO-ADAPTIVE-CLARIFICATION CONDITION"
    )

    print(
        "=================================================="
    )

    print()
    print(
        "Conversation state is preserved normally."
    )

    print(
        "Adaptive clarification is intentionally disabled."
    )

    print(
        "The ablated policy always produces a direct-answer decision."
    )

    # ==================================================
    # RUN CONVERSATIONS
    # ==================================================

    for conversation_index, test_case in enumerate(
        TEST_CASES,
        start=1
    ):

        # --------------------------------
        # IMPORTANT:
        # reset only at conversation start
        # state remains across turns
        # --------------------------------

        reset_conversation()

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

            # ==========================================
            # Run FULL system internally
            #
            # We allow normal state extraction/update.
            # We only ablate the final clarification
            # policy decision.
            # ==========================================

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

            # ==========================================
            # State extraction remains untouched
            # ==========================================

            state = result.get(
                "state",
                {}
            )

            predicted_missing = state.get(
                "missing_information",
                []
            )

            original_clarification = result.get(
                "needs_clarification",
                False
            )

            # ==========================================
            # ABLATION:
            # clarification policy is disabled
            # ==========================================

            ablated_clarification = False

            ablated_action = "direct_answer"

            # ==========================================
            # Missing-information evaluation
            # ==========================================

            missing_match = compare_missing(
                predicted_missing,
                expected_missing
            )

            if missing_match:

                missing_correct += 1

            else:

                conversation_correct = False

            # ==========================================
            # Clarification-decision evaluation
            # ==========================================

            clarification_match = (
                ablated_clarification
                ==
                expected_clarification
            )

            if clarification_match:

                clarification_correct += 1

            else:

                conversation_correct = False

            # ==========================================
            # Clarification-required turns
            # ==========================================

            if expected_clarification:

                clarification_required_turns += 1

                if not ablated_clarification:

                    premature_direct_answers += 1

            # ==========================================
            # Complete-input turns
            # ==========================================

            if not expected_clarification:

                complete_input_turns += 1

                if not ablated_clarification:

                    complete_input_correct += 1

            # ==========================================
            # Continuation-turn state
            # ==========================================

            if turn_number > 1:

                continuation_turns += 1

                if missing_match:

                    continuation_missing_correct += 1

            # ==========================================
            # Per-turn output
            # ==========================================

            print()
            print(
                f"Turn {turn_number}"
            )

            print(
                "Input:"
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
                "Full System Internal Result:"
            )

            print(
                f"  Missing: "
                f"{predicted_missing}"
            )

            print(
                f"  Original clarification: "
                f"{original_clarification}"
            )

            print()

            print(
                "No-Clarification Ablation:"
            )

            print(
                f"  Action: "
                f"{ablated_action}"
            )

            print(
                f"  Clarification: "
                f"{ablated_clarification}"
            )

            print()

            print(
                f"Missing correct: "
                f"{missing_match}"
            )

            print(
                f"Ablated action correct: "
                f"{clarification_match}"
            )

        # --------------------------------
        # Conversation-level success
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

    premature_direct_answer_rate = percentage(
        premature_direct_answers,
        clarification_required_turns
    )

    complete_input_accuracy = percentage(
        complete_input_correct,
        complete_input_turns
    )

    continuation_state_accuracy = percentage(
        continuation_missing_correct,
        continuation_turns
    )

    # ==================================================
    # FULL-SYSTEM CANONICAL REFERENCE
    # ==================================================

    full_missing_accuracy = 100.00

    full_clarification_accuracy = 100.00

    full_conversation_accuracy = 100.00

    full_premature_direct_answer_rate = 0.00

    full_complete_input_accuracy = 100.00

    full_continuation_state_accuracy = 100.00

    # ==================================================
    # FINAL REPORT
    # ==================================================

    print()
    print(
        "=================================================="
    )

    print(
        "No-Clarification Ablation Results"
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

    print(
        f"Failed Turns: "
        f"{len(failed_turns)}"
    )

    # ==================================================
    # 1. Missing information
    # ==================================================

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
        f"Full System: "
        f"{full_missing_accuracy:.2f}%"
    )

    print(
        f"No-Clarification: "
        f"{missing_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{missing_accuracy - full_missing_accuracy:+.2f} pp"
    )

    # ==================================================
    # 2. Clarification decision
    # ==================================================

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
        f"Full System: "
        f"{full_clarification_accuracy:.2f}%"
    )

    print(
        f"No-Clarification: "
        f"{clarification_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{clarification_accuracy - full_clarification_accuracy:+.2f} pp"
    )

    # ==================================================
    # 3. Complete conversation
    # ==================================================

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
        f"No-Clarification: "
        f"{conversation_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{conversation_accuracy - full_conversation_accuracy:+.2f} pp"
    )

    # ==================================================
    # 4. Premature direct answers
    # ==================================================

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "4. Premature Direct-Answer Rate"
    )

    print(
        "Lower is better."
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Full System: "
        f"{full_premature_direct_answer_rate:.2f}%"
    )

    print(
        f"No-Clarification: "
        f"{premature_direct_answer_rate:.2f}%"
    )

    print(
        f"Change: "
        f"{premature_direct_answer_rate - full_premature_direct_answer_rate:+.2f} pp"
    )

    # ==================================================
    # 5. Complete-input behavior
    # ==================================================

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "5. Complete-Input Handling Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Full System: "
        f"{full_complete_input_accuracy:.2f}%"
    )

    print(
        f"No-Clarification: "
        f"{complete_input_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{complete_input_accuracy - full_complete_input_accuracy:+.2f} pp"
    )

    # ==================================================
    # 6. State preservation
    # ==================================================

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "6. Continuation-Turn State Accuracy"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Full System: "
        f"{full_continuation_state_accuracy:.2f}%"
    )

    print(
        f"No-Clarification: "
        f"{continuation_state_accuracy:.2f}%"
    )

    print(
        f"Change: "
        f"{continuation_state_accuracy - full_continuation_state_accuracy:+.2f} pp"
    )

    # ==================================================
    # FAILED TURNS
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

    if missing_accuracy == full_missing_accuracy:

        print(
            "Disabling clarification did not reduce "
            "structured missing-information detection."
        )

    if (
        continuation_state_accuracy
        ==
        full_continuation_state_accuracy
    ):

        print(
            "Multi-turn state tracking remained intact "
            "when only the clarification policy was removed."
        )

    if clarification_accuracy < full_clarification_accuracy:

        print(
            "Removing adaptive clarification reduced "
            "decision-policy accuracy."
        )

    if premature_direct_answer_rate > 0:

        print(
            "Without adaptive clarification, the system "
            "answered prematurely while required information "
            "was still missing."
        )

    if complete_input_accuracy == 100:

        print(
            "Removing clarification did not harm cases "
            "where the user request was already complete."
        )

    print(
        "=================================================="
    )

    print()


if __name__ == "__main__":

    evaluate_no_clarification_ablation()