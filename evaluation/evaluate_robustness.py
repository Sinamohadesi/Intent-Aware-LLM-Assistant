import os
import sys
from collections import defaultdict


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

from evaluation.field_normalizer import (
    normalize_fields
)


# ==================================================
# ROBUSTNESS TEST CASES
# ==================================================

ROBUSTNESS_TEST_CASES = [

    # ------------------------------------------------
    # 1. Paraphrased request
    # ------------------------------------------------

    {
        "name": "Paraphrased Recommendation Request",
        "category": "paraphrase",
        "turns": [
            {
                "input":
                    "I'm trying to figure out where I should study.",
                "expected_missing": [
                    "country",
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "I'd prefer Germany and I want to study Artificial Intelligence.",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "IELTS 6.5 and preferably low tuition.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 2. Informal / conversational language
    # ------------------------------------------------

    {
        "name": "Informal Language",
        "category": "informal",
        "turns": [
            {
                "input":
                    "I need some uni suggestions.",
                "expected_missing": [
                    "country",
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "Germany, AI.",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "Cheap tuition and IELTS 6.5.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 3. Typographical noise
    # ------------------------------------------------

    {
        "name": "Typographical Noise",
        "category": "typo",
        "turns": [
            {
                "input":
                    "I want universty recomendations in Germny.",
                "expected_missing": [
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "Artifical Inteligence",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "IELTS 6.5, low tution",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 4. Irrelevant text around useful information
    # ------------------------------------------------

    {
        "name": "Irrelevant Context",
        "category": "irrelevant_context",
        "turns": [
            {
                "input":
                    "I've been thinking about my future a lot lately. "
                    "Anyway, I want to study in Germany.",
                "expected_missing": [
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "My friend studies engineering, but for me "
                    "Artificial Intelligence is the interesting option.",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "I don't really care about city size. "
                    "My IELTS is 6.5 and I want low tuition.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 5. Information in unusual order
    # ------------------------------------------------

    {
        "name": "Reordered Information",
        "category": "reordered",
        "turns": [
            {
                "input":
                    "Low tuition is important to me.",
                "expected_missing": [
                    "country",
                    "field"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "The subject is Artificial Intelligence.",
                "expected_missing": [
                    "country"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "Germany.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 6. Fragmented requirements across turns
    # ------------------------------------------------

    {
        "name": "Fragmented User Information",
        "category": "fragmented",
        "turns": [
            {
                "input":
                    "Germany.",
                "expected_missing": [
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "Artificial Intelligence.",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "IELTS 6.5.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 7. Complete request in one turn
    # ------------------------------------------------

    {
        "name": "Dense Complete Request",
        "category": "complete_input",
        "turns": [
            {
                "input":
                    "Recommend universities in Germany for Artificial "
                    "Intelligence. My IELTS is 6.5, I prefer low tuition, "
                    "and I am interested in Machine Learning and "
                    "Computer Vision.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 8. Research interests mixed with field
    # ------------------------------------------------

    {
        "name": "Research Interest Disambiguation",
        "category": "research_interest",
        "turns": [
            {
                "input":
                    "I want to study Artificial Intelligence in Germany.",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "I'm especially interested in Machine Learning "
                    "and Computer Vision.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 9. Short fragments
    # ------------------------------------------------

    {
        "name": "Minimal Fragments",
        "category": "short_fragments",
        "turns": [
            {
                "input":
                    "Germany",
                "expected_missing": [
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "AI",
                "expected_missing": [
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "low tuition",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    },

    # ------------------------------------------------
    # 10. Natural long-form request
    # ------------------------------------------------

    {
        "name": "Natural Long Form",
        "category": "long_form",
        "turns": [
            {
                "input":
                    "I'm planning to apply for a master's degree and "
                    "I'm currently looking mainly at Germany. I haven't "
                    "decided which universities make the most sense yet.",
                "expected_missing": [
                    "field",
                    "requirements"
                ],
                "expected_clarification": True
            },
            {
                "input":
                    "My main academic direction is Artificial Intelligence, "
                    "especially programs related to machine learning.",
                "expected_missing": [],
                "expected_clarification": False
            }
        ]
    }
]


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
# EVALUATION
# ==================================================

def evaluate_robustness():

    total_conversations = len(
        ROBUSTNESS_TEST_CASES
    )

    total_turns = 0

    missing_correct = 0
    clarification_correct = 0

    complete_conversations = 0

    continuation_turns = 0
    continuation_correct = 0

    failed_turns = []

    category_stats = defaultdict(
        lambda: {
            "turns": 0,
            "missing_correct": 0,
            "clarification_correct": 0
        }
    )

    print()
    print(
        "=================================================="
    )

    print(
        "Robustness Evaluation"
    )

    print(
        "Intent-Aware Adaptive Assistant"
    )

    print(
        "=================================================="
    )

    # ------------------------------------------------
    # Run conversations
    # ------------------------------------------------

    for conversation_index, test_case in enumerate(
        ROBUSTNESS_TEST_CASES,
        start=1
    ):

        reset_conversation()

        conversation_correct = True

        category = test_case[
            "category"
        ]

        print()
        print(
            "--------------------------------------------------"
        )

        print(
            f"Conversation {conversation_index}: "
            f"{test_case['name']}"
        )

        print(
            f"Category: {category}"
        )

        print(
            "--------------------------------------------------"
        )

        for turn_number, turn in enumerate(
            test_case["turns"],
            start=1
        ):

            total_turns += 1

            category_stats[
                category
            ]["turns"] += 1

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
            # Run adaptive system
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

                        "category":
                            category,

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
            # Read system state
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
            # Compare
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
            # Global metrics
            # --------------------------------

            if missing_match:

                missing_correct += 1

                category_stats[
                    category
                ][
                    "missing_correct"
                ] += 1

            else:

                conversation_correct = False

            if clarification_match:

                clarification_correct += 1

                category_stats[
                    category
                ][
                    "clarification_correct"
                ] += 1

            else:

                conversation_correct = False

            # --------------------------------
            # Continuation metrics
            # --------------------------------

            if turn_number > 1:

                continuation_turns += 1

                if missing_match:

                    continuation_correct += 1

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
                "Predicted:"
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
        # Conversation-level result
        # --------------------------------

        if conversation_correct:

            complete_conversations += 1

    # ==================================================
    # FINAL METRICS
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

    continuation_accuracy = percentage(
        continuation_correct,
        continuation_turns
    )

    # ==================================================
    # FINAL REPORT
    # ==================================================

    print()
    print(
        "=================================================="
    )

    print(
        "Robustness Evaluation Results"
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
        f"Failed Turns: "
        f"{len(failed_turns)}"
    )

    print()

    print(
        "--------------------------------------------------"
    )

    print(
        "Overall Metrics"
    )

    print(
        "--------------------------------------------------"
    )

    print(
        f"Missing Information Accuracy: "
        f"{missing_accuracy:.2f}%"
    )

    print(
        f"Clarification Decision Accuracy: "
        f"{clarification_accuracy:.2f}%"
    )

    print(
        f"Complete Conversation Accuracy: "
        f"{conversation_accuracy:.2f}%"
    )

    print(
        f"Continuation-Turn State Accuracy: "
        f"{continuation_accuracy:.2f}%"
    )

    # ==================================================
    # CATEGORY RESULTS
    # ==================================================

    print()
    print(
        "--------------------------------------------------"
    )

    print(
        "Results by Robustness Category"
    )

    print(
        "--------------------------------------------------"
    )

    for category, stats in category_stats.items():

        turns = stats[
            "turns"
        ]

        category_missing_accuracy = percentage(
            stats[
                "missing_correct"
            ],
            turns
        )

        category_clarification_accuracy = percentage(
            stats[
                "clarification_correct"
            ],
            turns
        )

        print()

        print(
            f"{category}:"
        )

        print(
            f"  Turns: "
            f"{turns}"
        )

        print(
            f"  Missing Accuracy: "
            f"{category_missing_accuracy:.2f}%"
        )

        print(
            f"  Clarification Accuracy: "
            f"{category_clarification_accuracy:.2f}%"
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
                f"Category: "
                f"{failure['category']}"
            )

            print(
                f"Input: "
                f"{failure['input']}"
            )

            print(
                f"Error: "
                f"{failure['error']}"
            )

    print()
    print(
        "=================================================="
    )

    print(
        "Robustness Summary"
    )

    print(
        "=================================================="
    )

    print(
        f"Missing Information Accuracy: "
        f"{missing_accuracy:.2f}%"
    )

    print(
        f"Clarification Decision Accuracy: "
        f"{clarification_accuracy:.2f}%"
    )

    print(
        f"Complete Conversation Accuracy: "
        f"{conversation_accuracy:.2f}%"
    )

    print(
        f"Continuation-Turn State Accuracy: "
        f"{continuation_accuracy:.2f}%"
    )

    print(
        "=================================================="
    )

    print()


if __name__ == "__main__":

    evaluate_robustness()