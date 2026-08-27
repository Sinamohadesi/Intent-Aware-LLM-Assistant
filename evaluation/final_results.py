import json
import os


# ==================================================
# PATHS
# ==================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

OUTPUT_DIR = os.path.join(
    CURRENT_DIR,
    "results"
)

JSON_OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "final_metrics.json"
)

MARKDOWN_OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "research_results.md"
)


# ==================================================
# CANONICAL STAGE 8 RESULTS
# ==================================================

SINGLE_TURN_RESULTS = {
    "dataset_samples": 15,
    "successfully_evaluated": 15,
    "failed_samples": 0,
    "intent_accuracy": 100.00,
    "missing_precision": 91.30,
    "missing_recall": 100.00,
    "missing_f1": 95.45,
    "missing_exact_match": 86.67,
}


MULTITURN_RESULTS = {
    "total_conversations": 4,
    "total_turns": 10,
    "missing_information_accuracy": 100.00,
    "clarification_decision_accuracy": 100.00,
    "complete_conversation_accuracy": 100.00,
}


BASELINE_RESULTS = {
    "dataset_samples": 15,
    "successfully_evaluated": 15,
    "failed_samples": 0,
    "intent_accuracy": 100.00,
    "missing_precision": 91.30,
    "missing_recall": 100.00,
    "missing_f1": 95.45,
    "missing_exact_match": 86.67,
    "direct_answer_rate": 100.00,
    "incomplete_prompt_direct_answer_rate": 100.00,
    "clarification_attempt_rate": 0.00,
}


COMPARATIVE_RESULTS = {
    "total_conversations": 4,
    "total_turns": 10,
    "continuation_turns": 6,
    "clarification_required_turns": 6,
    "complete_input_turns": 4,

    "missing_information_accuracy": {
        "adaptive": 100.00,
        "baseline": 50.00,
        "difference_pp": 50.00,
    },

    "clarification_decision_accuracy": {
        "adaptive": 100.00,
        "baseline": 40.00,
        "difference_pp": 60.00,
    },

    "complete_conversation_accuracy": {
        "adaptive": 100.00,
        "baseline": 25.00,
        "difference_pp": 75.00,
    },

    "continuation_turn_state_accuracy": {
        "adaptive": 100.00,
        "baseline": 16.67,
        "difference_pp": 83.33,
    },

    "premature_direct_answer_rate": {
        "adaptive": 0.00,
        "baseline": 100.00,
    },

    "complete_input_handling_accuracy": {
        "adaptive": 100.00,
        "baseline": 100.00,
    },

    "failed_baseline_calls": 0,
}


ROBUSTNESS_RESULTS = {
    "total_conversations": 10,
    "total_turns": 26,
    "continuation_turns": 16,
    "failed_turns": 0,

    "overall": {
        "missing_information_accuracy": 96.15,
        "clarification_decision_accuracy": 96.15,
        "complete_conversation_accuracy": 90.00,
        "continuation_turn_state_accuracy": 93.75,
    },

    "categories": {
        "paraphrase": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "informal": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "typo": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "irrelevant_context": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "reordered": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "fragmented": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "complete_input": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "research_interest": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "short_fragments": {
            "missing_accuracy": 100.00,
            "clarification_accuracy": 100.00,
        },

        "long_form": {
            "missing_accuracy": 50.00,
            "clarification_accuracy": 50.00,
        },
    },
}


NO_STATE_ABLATION = {
    "total_conversations": 4,
    "total_turns": 10,
    "first_turns": 4,
    "continuation_turns": 6,
    "failed_turns": 0,

    "overall_missing_information_accuracy": {
        "full_system": 100.00,
        "no_state": 50.00,
        "change_pp": -50.00,
    },

    "overall_clarification_decision_accuracy": {
        "full_system": 100.00,
        "no_state": 70.00,
        "change_pp": -30.00,
    },

    "complete_conversation_accuracy": {
        "full_system": 100.00,
        "no_state": 25.00,
        "change_pp": -75.00,
    },

    "first_turn_missing_accuracy": 100.00,

    "first_turn_clarification_accuracy": 100.00,

    "continuation_turn_missing_accuracy": {
        "full_system": 100.00,
        "no_state": 16.67,
        "change_pp": -83.33,
    },

    "continuation_turn_clarification_accuracy": 50.00,
}


NO_CLARIFICATION_ABLATION = {
    "total_conversations": 4,
    "total_turns": 10,
    "continuation_turns": 6,
    "clarification_required_turns": 6,
    "complete_input_turns": 4,
    "failed_turns": 0,

    "missing_information_accuracy": {
        "full_system": 100.00,
        "no_clarification": 100.00,
        "change_pp": 0.00,
    },

    "clarification_decision_accuracy": {
        "full_system": 100.00,
        "no_clarification": 40.00,
        "change_pp": -60.00,
    },

    "complete_conversation_accuracy": {
        "full_system": 100.00,
        "no_clarification": 25.00,
        "change_pp": -75.00,
    },

    "premature_direct_answer_rate": {
        "full_system": 0.00,
        "no_clarification": 100.00,
        "change_pp": 100.00,
    },

    "complete_input_handling_accuracy": {
        "full_system": 100.00,
        "no_clarification": 100.00,
        "change_pp": 0.00,
    },

    "continuation_turn_state_accuracy": {
        "full_system": 100.00,
        "no_clarification": 100.00,
        "change_pp": 0.00,
    },
}


RANKING_V2_RESULTS = {
    "TUM": 95.45,
    "University of Stuttgart": 90.91,
    "Saarland University": 81.82,
}


# ==================================================
# COMPLETE RESULT OBJECT
# ==================================================

FINAL_RESULTS = {
    "single_turn": SINGLE_TURN_RESULTS,
    "multi_turn": MULTITURN_RESULTS,
    "direct_answer_baseline": BASELINE_RESULTS,
    "comparative_evaluation": COMPARATIVE_RESULTS,
    "robustness": ROBUSTNESS_RESULTS,
    "ablation_no_state": NO_STATE_ABLATION,
    "ablation_no_clarification": NO_CLARIFICATION_ABLATION,
    "ranking_v2": RANKING_V2_RESULTS,
}


# ==================================================
# HELPERS
# ==================================================

def format_percent(value):

    return f"{value:.2f}%"


def format_change(value):

    if value > 0:
        return f"+{value:.2f} pp"

    return f"{value:.2f} pp"


def print_line():

    print(
        "============================================================"
    )


def print_section_line():

    print(
        "------------------------------------------------------------"
    )


# ==================================================
# CONSOLE TABLES
# ==================================================

def print_single_turn_results():

    print()
    print_line()
    print("TABLE 1 — Single-Turn Evaluation")
    print_line()

    print(
        f"Intent Accuracy: "
        f"{format_percent(SINGLE_TURN_RESULTS['intent_accuracy'])}"
    )

    print(
        f"Missing Precision: "
        f"{format_percent(SINGLE_TURN_RESULTS['missing_precision'])}"
    )

    print(
        f"Missing Recall: "
        f"{format_percent(SINGLE_TURN_RESULTS['missing_recall'])}"
    )

    print(
        f"Missing F1: "
        f"{format_percent(SINGLE_TURN_RESULTS['missing_f1'])}"
    )

    print(
        f"Missing Exact Match: "
        f"{format_percent(SINGLE_TURN_RESULTS['missing_exact_match'])}"
    )


def print_comparative_results():

    print()
    print_line()
    print("TABLE 2 — Adaptive System vs Direct-Answer Baseline")
    print_line()

    rows = [
        (
            "Missing Information Accuracy",
            COMPARATIVE_RESULTS[
                "missing_information_accuracy"
            ]
        ),

        (
            "Clarification Decision Accuracy",
            COMPARATIVE_RESULTS[
                "clarification_decision_accuracy"
            ]
        ),

        (
            "Complete Conversation Accuracy",
            COMPARATIVE_RESULTS[
                "complete_conversation_accuracy"
            ]
        ),

        (
            "Continuation-Turn State Accuracy",
            COMPARATIVE_RESULTS[
                "continuation_turn_state_accuracy"
            ]
        ),
    ]

    print(
        f"{'Metric':40}"
        f"{'Adaptive':>12}"
        f"{'Baseline':>12}"
        f"{'Difference':>14}"
    )

    print_section_line()

    for name, values in rows:

        print(
            f"{name:40}"
            f"{format_percent(values['adaptive']):>12}"
            f"{format_percent(values['baseline']):>12}"
            f"{format_change(values['difference_pp']):>14}"
        )

    print_section_line()

    print(
        f"{'Premature Direct-Answer Rate':40}"
        f"{format_percent(COMPARATIVE_RESULTS['premature_direct_answer_rate']['adaptive']):>12}"
        f"{format_percent(COMPARATIVE_RESULTS['premature_direct_answer_rate']['baseline']):>12}"
    )

    print(
        f"{'Complete-Input Handling Accuracy':40}"
        f"{format_percent(COMPARATIVE_RESULTS['complete_input_handling_accuracy']['adaptive']):>12}"
        f"{format_percent(COMPARATIVE_RESULTS['complete_input_handling_accuracy']['baseline']):>12}"
    )


def print_robustness_results():

    print()
    print_line()
    print("TABLE 3 — Robustness Evaluation")
    print_line()

    overall = ROBUSTNESS_RESULTS[
        "overall"
    ]

    print(
        f"Missing Information Accuracy: "
        f"{format_percent(overall['missing_information_accuracy'])}"
    )

    print(
        f"Clarification Decision Accuracy: "
        f"{format_percent(overall['clarification_decision_accuracy'])}"
    )

    print(
        f"Complete Conversation Accuracy: "
        f"{format_percent(overall['complete_conversation_accuracy'])}"
    )

    print(
        f"Continuation-Turn State Accuracy: "
        f"{format_percent(overall['continuation_turn_state_accuracy'])}"
    )

    print()
    print(
        "Category Results:"
    )

    print_section_line()

    for category, values in ROBUSTNESS_RESULTS[
        "categories"
    ].items():

        print(
            f"{category:25}"
            f"Missing: "
            f"{format_percent(values['missing_accuracy']):>8}"
            f"   Clarification: "
            f"{format_percent(values['clarification_accuracy']):>8}"
        )


def print_ablation_results():

    print()
    print_line()
    print("TABLE 4 — Ablation Study")
    print_line()

    print()
    print("A. No-State Ablation")

    print_section_line()

    no_state_rows = [
        (
            "Missing Information Accuracy",
            NO_STATE_ABLATION[
                "overall_missing_information_accuracy"
            ]
        ),

        (
            "Clarification Decision Accuracy",
            NO_STATE_ABLATION[
                "overall_clarification_decision_accuracy"
            ]
        ),

        (
            "Complete Conversation Accuracy",
            NO_STATE_ABLATION[
                "complete_conversation_accuracy"
            ]
        ),

        (
            "Continuation-Turn Missing Accuracy",
            NO_STATE_ABLATION[
                "continuation_turn_missing_accuracy"
            ]
        ),
    ]

    for name, values in no_state_rows:

        print(
            f"{name}: "
            f"Full={format_percent(values['full_system'])}, "
            f"No-State={format_percent(values['no_state'])}, "
            f"Change={format_change(values['change_pp'])}"
        )

    print()
    print("B. No-Clarification Ablation")

    print_section_line()

    no_clarification_rows = [
        (
            "Missing Information Accuracy",
            NO_CLARIFICATION_ABLATION[
                "missing_information_accuracy"
            ]
        ),

        (
            "Clarification Decision Accuracy",
            NO_CLARIFICATION_ABLATION[
                "clarification_decision_accuracy"
            ]
        ),

        (
            "Complete Conversation Accuracy",
            NO_CLARIFICATION_ABLATION[
                "complete_conversation_accuracy"
            ]
        ),

        (
            "Premature Direct-Answer Rate",
            NO_CLARIFICATION_ABLATION[
                "premature_direct_answer_rate"
            ]
        ),

        (
            "Continuation-Turn State Accuracy",
            NO_CLARIFICATION_ABLATION[
                "continuation_turn_state_accuracy"
            ]
        ),
    ]

    for name, values in no_clarification_rows:

        print(
            f"{name}: "
            f"Full={format_percent(values['full_system'])}, "
            f"No-Clarification="
            f"{format_percent(values['no_clarification'])}, "
            f"Change={format_change(values['change_pp'])}"
        )


def print_ranking_results():

    print()
    print_line()
    print("TABLE 5 — Ranking V2 Regression")
    print_line()

    for university, score in RANKING_V2_RESULTS.items():

        print(
            f"{university}: "
            f"{score:.2f}"
        )


# ==================================================
# MARKDOWN REPORT
# ==================================================

def build_markdown_report():

    comparison = COMPARATIVE_RESULTS

    robustness = ROBUSTNESS_RESULTS[
        "overall"
    ]

    no_state = NO_STATE_ABLATION

    no_clarification = NO_CLARIFICATION_ABLATION

    markdown = f"""# Research Evaluation Results

## 1. Single-Turn Evaluation

| Metric | Result |
|---|---:|
| Intent Accuracy | {SINGLE_TURN_RESULTS['intent_accuracy']:.2f}% |
| Missing Information Precision | {SINGLE_TURN_RESULTS['missing_precision']:.2f}% |
| Missing Information Recall | {SINGLE_TURN_RESULTS['missing_recall']:.2f}% |
| Missing Information F1 | {SINGLE_TURN_RESULTS['missing_f1']:.2f}% |
| Missing Information Exact Match | {SINGLE_TURN_RESULTS['missing_exact_match']:.2f}% |

## 2. Multi-Turn Evaluation

| Metric | Result |
|---|---:|
| Missing Information Accuracy | {MULTITURN_RESULTS['missing_information_accuracy']:.2f}% |
| Clarification Decision Accuracy | {MULTITURN_RESULTS['clarification_decision_accuracy']:.2f}% |
| Complete Conversation Accuracy | {MULTITURN_RESULTS['complete_conversation_accuracy']:.2f}% |

## 3. Adaptive System vs Direct-Answer Baseline

| Metric | Adaptive | Baseline | Difference |
|---|---:|---:|---:|
| Missing Information Accuracy | {comparison['missing_information_accuracy']['adaptive']:.2f}% | {comparison['missing_information_accuracy']['baseline']:.2f}% | +{comparison['missing_information_accuracy']['difference_pp']:.2f} pp |
| Clarification Decision Accuracy | {comparison['clarification_decision_accuracy']['adaptive']:.2f}% | {comparison['clarification_decision_accuracy']['baseline']:.2f}% | +{comparison['clarification_decision_accuracy']['difference_pp']:.2f} pp |
| Complete Conversation Accuracy | {comparison['complete_conversation_accuracy']['adaptive']:.2f}% | {comparison['complete_conversation_accuracy']['baseline']:.2f}% | +{comparison['complete_conversation_accuracy']['difference_pp']:.2f} pp |
| Continuation-Turn State Accuracy | {comparison['continuation_turn_state_accuracy']['adaptive']:.2f}% | {comparison['continuation_turn_state_accuracy']['baseline']:.2f}% | +{comparison['continuation_turn_state_accuracy']['difference_pp']:.2f} pp |
| Premature Direct-Answer Rate | {comparison['premature_direct_answer_rate']['adaptive']:.2f}% | {comparison['premature_direct_answer_rate']['baseline']:.2f}% | — |
| Complete-Input Handling Accuracy | {comparison['complete_input_handling_accuracy']['adaptive']:.2f}% | {comparison['complete_input_handling_accuracy']['baseline']:.2f}% | — |

## 4. Robustness Evaluation

| Metric | Result |
|---|---:|
| Missing Information Accuracy | {robustness['missing_information_accuracy']:.2f}% |
| Clarification Decision Accuracy | {robustness['clarification_decision_accuracy']:.2f}% |
| Complete Conversation Accuracy | {robustness['complete_conversation_accuracy']:.2f}% |
| Continuation-Turn State Accuracy | {robustness['continuation_turn_state_accuracy']:.2f}% |

### Robustness Categories

| Category | Missing Accuracy | Clarification Accuracy |
|---|---:|---:|
"""

    for category, values in ROBUSTNESS_RESULTS[
        "categories"
    ].items():

        markdown += (
            f"| {category} "
            f"| {values['missing_accuracy']:.2f}% "
            f"| {values['clarification_accuracy']:.2f}% |\n"
        )

    markdown += f"""
## 5. No-State Ablation

| Metric | Full System | No-State | Change |
|---|---:|---:|---:|
| Missing Information Accuracy | {no_state['overall_missing_information_accuracy']['full_system']:.2f}% | {no_state['overall_missing_information_accuracy']['no_state']:.2f}% | {no_state['overall_missing_information_accuracy']['change_pp']:.2f} pp |
| Clarification Decision Accuracy | {no_state['overall_clarification_decision_accuracy']['full_system']:.2f}% | {no_state['overall_clarification_decision_accuracy']['no_state']:.2f}% | {no_state['overall_clarification_decision_accuracy']['change_pp']:.2f} pp |
| Complete Conversation Accuracy | {no_state['complete_conversation_accuracy']['full_system']:.2f}% | {no_state['complete_conversation_accuracy']['no_state']:.2f}% | {no_state['complete_conversation_accuracy']['change_pp']:.2f} pp |
| Continuation-Turn Missing Accuracy | {no_state['continuation_turn_missing_accuracy']['full_system']:.2f}% | {no_state['continuation_turn_missing_accuracy']['no_state']:.2f}% | {no_state['continuation_turn_missing_accuracy']['change_pp']:.2f} pp |

## 6. No-Clarification Ablation

| Metric | Full System | No-Clarification | Change |
|---|---:|---:|---:|
| Missing Information Accuracy | {no_clarification['missing_information_accuracy']['full_system']:.2f}% | {no_clarification['missing_information_accuracy']['no_clarification']:.2f}% | {no_clarification['missing_information_accuracy']['change_pp']:.2f} pp |
| Clarification Decision Accuracy | {no_clarification['clarification_decision_accuracy']['full_system']:.2f}% | {no_clarification['clarification_decision_accuracy']['no_clarification']:.2f}% | {no_clarification['clarification_decision_accuracy']['change_pp']:.2f} pp |
| Complete Conversation Accuracy | {no_clarification['complete_conversation_accuracy']['full_system']:.2f}% | {no_clarification['complete_conversation_accuracy']['no_clarification']:.2f}% | {no_clarification['complete_conversation_accuracy']['change_pp']:.2f} pp |
| Premature Direct-Answer Rate | {no_clarification['premature_direct_answer_rate']['full_system']:.2f}% | {no_clarification['premature_direct_answer_rate']['no_clarification']:.2f}% | +{no_clarification['premature_direct_answer_rate']['change_pp']:.2f} pp |
| Continuation-Turn State Accuracy | {no_clarification['continuation_turn_state_accuracy']['full_system']:.2f}% | {no_clarification['continuation_turn_state_accuracy']['no_clarification']:.2f}% | {no_clarification['continuation_turn_state_accuracy']['change_pp']:.2f} pp |

## 7. Ranking V2 Regression

| University | Match Score |
|---|---:|
| Technical University of Munich | {RANKING_V2_RESULTS['TUM']:.2f} |
| University of Stuttgart | {RANKING_V2_RESULTS['University of Stuttgart']:.2f} |
| Saarland University | {RANKING_V2_RESULTS['Saarland University']:.2f} |

## 8. Main Findings

1. The adaptive assistant preserved 100% missing-information and clarification-decision accuracy on the canonical multi-turn evaluation.
2. Compared with the direct-answer baseline, the adaptive system improved continuation-turn state accuracy by 83.33 percentage points.
3. The direct-answer baseline produced premature answers on 100% of clarification-required turns, while the adaptive system produced none.
4. Removing state reduced continuation-turn missing-information accuracy from 100% to 16.67%, demonstrating the importance of explicit state tracking.
5. Removing adaptive clarification preserved extraction and state accuracy but reduced clarification-decision accuracy to 40% and increased premature direct answers to 100%.
6. Robustness remained high overall, although long-form natural input exposed a measurable limitation.

## 9. Research Conclusion

The evaluation supports the hypothesis that explicit state tracking and adaptive clarification improve the reliability of multi-turn university recommendation assistants.

State tracking primarily contributes to preserving previously supplied user information across conversation turns, while adaptive clarification converts missing-information awareness into an appropriate conversational action.

The ablation results show that these components provide distinct benefits rather than representing redundant parts of the architecture.

## 10. Current Limitation

The main observed robustness weakness was long-form natural input, where missing-information and clarification accuracy fell to 50% within that robustness category.

This limitation provides a clear direction for future work involving stronger semantic extraction, uncertainty-aware clarification, and more robust handling of complex long-form requests.
"""

    return markdown


# ==================================================
# FILE EXPORT
# ==================================================

def save_json():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    with open(
        JSON_OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            FINAL_RESULTS,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_markdown():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    markdown = build_markdown_report()

    with open(
        MARKDOWN_OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            markdown
        )


# ==================================================
# MAIN
# ==================================================

def main():

    print()
    print_line()
    print(
        "STAGE 8.5 — FINAL RESEARCH RESULTS"
    )
    print_line()

    print_single_turn_results()

    print_comparative_results()

    print_robustness_results()

    print_ablation_results()

    print_ranking_results()

    save_json()

    save_markdown()

    print()
    print_line()

    print(
        "Final result files created successfully."
    )

    print()

    print(
        "JSON:"
    )

    print(
        JSON_OUTPUT_PATH
    )

    print()

    print(
        "Markdown:"
    )

    print(
        MARKDOWN_OUTPUT_PATH
    )

    print_line()
    print()


if __name__ == "__main__":

    main()