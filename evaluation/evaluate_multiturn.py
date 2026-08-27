import os
import sys


ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


from src.main import process_query, reset_conversation


TEST_CASES = [
    {
        "name": "Basic three-turn conversation",

        "turns": [
            {
                "input": "Help me choose a university",

                "expected_missing": [
                    "country",
                    "field",
                    "requirements"
                ],

                "expected_clarification": True
            },

            {
                "input": "Germany and Artificial Intelligence",

                "expected_missing": [
                    "requirements"
                ],

                "expected_clarification": True
            },

            {
                "input":
                    "No tuition preference, IELTS 6.5, top universities",

                "expected_missing": [],

                "expected_clarification": False
            }
        ]
    },

    {
        "name": "Country first",

        "turns": [
            {
                "input": "I want to study in Germany",

                "expected_missing": [
                    "field",
                    "requirements"
                ],

                "expected_clarification": True
            },

            {
                "input": "Artificial Intelligence",

                "expected_missing": [
                    "requirements"
                ],

                "expected_clarification": True
            },

            {
                "input": "Low tuition and IELTS 6.5",

                "expected_missing": [],

                "expected_clarification": False
            }
        ]
    },

    {
        "name": "Field first",

        "turns": [
            {
                "input": "I want to study Data Science",

                "expected_missing": [
                    "country",
                    "requirements"
                ],

                "expected_clarification": True
            },

            {
                "input": "Netherlands",

                "expected_missing": [
                    "requirements"
                ],

                "expected_clarification": True
            },

            {
                "input": "Top universities, IELTS 7",

                "expected_missing": [],

                "expected_clarification": False
            }
        ]
    },

    {
        "name": "Complete request in one turn",

        "turns": [
            {
                "input":
                    "Recommend universities in Germany for Artificial Intelligence with low tuition",

                "expected_missing": [],

                "expected_clarification": False
            }
        ]
    }
]


def compare_lists(
    predicted,
    expected
):

    return set(
        predicted
    ) == set(
        expected
    )


def evaluate_multiturn():

    total_turns = 0

    correct_missing = 0

    correct_clarification = 0

    complete_conversations = 0


    print()
    print(
        "================================="
    )

    print(
        "Multi-turn Clarification Evaluation"
    )

    print(
        "================================="
    )


    for test_case in TEST_CASES:

        reset_conversation()

        conversation_correct = True


        print()
        print(
            f"Test: {test_case['name']}"
        )


        for turn_number, turn in enumerate(
            test_case["turns"],
            start=1
        ):

            total_turns += 1


            result = process_query(
                turn["input"]
            )


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


            expected_missing = turn[
                "expected_missing"
            ]


            expected_clarification = turn[
                "expected_clarification"
            ]


            missing_correct = compare_lists(
                predicted_missing,
                expected_missing
            )


            clarification_correct = (
                predicted_clarification
                == expected_clarification
            )


            if missing_correct:

                correct_missing += 1

            else:

                conversation_correct = False


            if clarification_correct:

                correct_clarification += 1

            else:

                conversation_correct = False


            print(
                f"Turn {turn_number}:"
            )

            print(
                f"  Input: "
                f"{turn['input']}"
            )

            print(
                f"  Predicted missing: "
                f"{predicted_missing}"
            )

            print(
                f"  Expected missing: "
                f"{expected_missing}"
            )

            print(
                f"  Clarification: "
                f"{predicted_clarification}"
            )

            print(
                f"  Missing correct: "
                f"{missing_correct}"
            )

            print(
                f"  Clarification correct: "
                f"{clarification_correct}"
            )


        if conversation_correct:

            complete_conversations += 1


    missing_accuracy = (
        correct_missing
        / total_turns
    ) * 100


    clarification_accuracy = (
        correct_clarification
        / total_turns
    ) * 100


    conversation_accuracy = (
        complete_conversations
        / len(TEST_CASES)
    ) * 100


    print()
    print(
        "================================="
    )

    print(
        "Final Results"
    )

    print(
        "================================="
    )


    print(
        f"Total Conversations: "
        f"{len(TEST_CASES)}"
    )


    print(
        f"Total Turns: "
        f"{total_turns}"
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
        "================================="
    )

    print()


if __name__ == "__main__":

    evaluate_multiturn()