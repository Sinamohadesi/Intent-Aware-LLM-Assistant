# Research Evaluation Results

## 1. Single-Turn Evaluation

| Metric | Result |
|---|---:|
| Intent Accuracy | 100.00% |
| Missing Information Precision | 91.30% |
| Missing Information Recall | 100.00% |
| Missing Information F1 | 95.45% |
| Missing Information Exact Match | 86.67% |

## 2. Multi-Turn Evaluation

| Metric | Result |
|---|---:|
| Missing Information Accuracy | 100.00% |
| Clarification Decision Accuracy | 100.00% |
| Complete Conversation Accuracy | 100.00% |

## 3. Adaptive System vs Direct-Answer Baseline

| Metric | Adaptive | Baseline | Difference |
|---|---:|---:|---:|
| Missing Information Accuracy | 100.00% | 50.00% | +50.00 pp |
| Clarification Decision Accuracy | 100.00% | 40.00% | +60.00 pp |
| Complete Conversation Accuracy | 100.00% | 25.00% | +75.00 pp |
| Continuation-Turn State Accuracy | 100.00% | 16.67% | +83.33 pp |
| Premature Direct-Answer Rate | 0.00% | 100.00% | — |
| Complete-Input Handling Accuracy | 100.00% | 100.00% | — |

## 4. Robustness Evaluation

| Metric | Result |
|---|---:|
| Missing Information Accuracy | 96.15% |
| Clarification Decision Accuracy | 96.15% |
| Complete Conversation Accuracy | 90.00% |
| Continuation-Turn State Accuracy | 93.75% |

### Robustness Categories

| Category | Missing Accuracy | Clarification Accuracy |
|---|---:|---:|
| paraphrase | 100.00% | 100.00% |
| informal | 100.00% | 100.00% |
| typo | 100.00% | 100.00% |
| irrelevant_context | 100.00% | 100.00% |
| reordered | 100.00% | 100.00% |
| fragmented | 100.00% | 100.00% |
| complete_input | 100.00% | 100.00% |
| research_interest | 100.00% | 100.00% |
| short_fragments | 100.00% | 100.00% |
| long_form | 50.00% | 50.00% |

## 5. No-State Ablation

| Metric | Full System | No-State | Change |
|---|---:|---:|---:|
| Missing Information Accuracy | 100.00% | 50.00% | -50.00 pp |
| Clarification Decision Accuracy | 100.00% | 70.00% | -30.00 pp |
| Complete Conversation Accuracy | 100.00% | 25.00% | -75.00 pp |
| Continuation-Turn Missing Accuracy | 100.00% | 16.67% | -83.33 pp |

## 6. No-Clarification Ablation

| Metric | Full System | No-Clarification | Change |
|---|---:|---:|---:|
| Missing Information Accuracy | 100.00% | 100.00% | 0.00 pp |
| Clarification Decision Accuracy | 100.00% | 40.00% | -60.00 pp |
| Complete Conversation Accuracy | 100.00% | 25.00% | -75.00 pp |
| Premature Direct-Answer Rate | 0.00% | 100.00% | +100.00 pp |
| Continuation-Turn State Accuracy | 100.00% | 100.00% | 0.00 pp |

## 7. Ranking V2 Regression

| University | Match Score |
|---|---:|
| Technical University of Munich | 95.45 |
| University of Stuttgart | 90.91 |
| Saarland University | 81.82 |

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
