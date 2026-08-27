# Intent-Aware LLM Assistant

## Research Evaluation of Adaptive Clarification and Structured State Tracking in Multi-Turn University Recommendation

---

## Abstract

Large Language Model assistants often respond directly to user requests even when essential information is missing. In multi-turn recommendation tasks, this behavior can lead to premature answers, repeated questions, loss of previously supplied information, and unreliable personalization.

This project investigates an alternative architecture based on explicit intent detection, structured information extraction, short-term conversation state, adaptive clarification, personalized ranking, and persistent session memory.

The system was evaluated on single-turn extraction, multi-turn interaction, comparison with a direct-answer baseline, robustness scenarios, and component-level ablation studies.

On the canonical multi-turn evaluation, the complete adaptive system achieved **100% missing-information accuracy**, **100% clarification-decision accuracy**, and **100% complete-conversation accuracy**.

Compared with a direct-answer baseline, continuation-turn state accuracy improved from **16.67% to 100%**. Removing state reduced continuation-turn missing-information accuracy from **100% to 16.67%**, while disabling adaptive clarification increased premature direct answers from **0% to 100%** without reducing structured information extraction accuracy.

The results indicate that explicit state tracking and adaptive clarification provide distinct and complementary contributions to reliable multi-turn assistant behavior.

---

# 1. Introduction

Modern LLM-based assistants are capable of generating fluent responses across a wide range of domains. However, response fluency does not necessarily imply interaction reliability.

A common failure mode occurs when a user provides an incomplete or underspecified request.

For example:

```text
Help me choose a university.
```

A direct-answer assistant may immediately generate recommendations despite lacking important information such as:

* destination country
* academic field
* language qualifications
* tuition preferences
* ranking preferences
* research interests

An alternative behavior is to first determine whether sufficient information is available.

This project explores that approach through an **Intent-Aware LLM Assistant** designed for multi-turn university recommendation.

The system explicitly separates:

1. intent detection
2. structured information extraction
3. missing-information detection
4. conversation-state management
5. adaptive clarification
6. user-profile construction
7. personalized ranking
8. answer generation
9. persistent conversation memory

The primary objective is not only to build a working application, but to experimentally evaluate whether these architectural decisions improve conversational reliability.

---

# 2. Research Question

The main research question is:

> Does an intent-aware assistant with explicit state tracking and adaptive clarification handle incomplete and multi-turn recommendation requests more reliably than a direct-answer baseline?

The project also investigates two component-level questions:

> How much of multi-turn reliability is attributable to explicit state tracking?

and:

> Is detecting missing information sufficient, or is an explicit clarification policy also necessary?

---

# 3. Hypotheses

The evaluation was designed around the following hypotheses.

### H1 — Adaptive clarification improves incomplete-request handling

An assistant that asks targeted clarification questions should make fewer premature recommendation decisions than a system that always answers directly.

### H2 — Explicit state tracking improves continuation-turn reliability

A system that preserves previously supplied information should outperform a stateless system on later conversation turns.

### H3 — Information extraction and clarification policy provide distinct benefits

A system may correctly recognize that information is missing while still behaving incorrectly if it is forced to answer instead of clarify.

### H4 — The architecture should remain functional under moderate linguistic variation

The system should remain reasonably robust to paraphrases, informal language, typographical errors, fragmented input, and reordered information.

---

# 4. System Architecture

The high-level pipeline is:

```text
User Input
    |
    v
Intent Detection + Structured Extraction
    |
    v
Normalization
    |
    v
State Manager
    |
    v
Missing Information Detection
    |
    +-----------------------------+
    |                             |
    v                             v
Adaptive Clarification      User Profile Builder
    |                             |
    v                             v
Next User Turn               Ranking Engine
                                  |
                                  v
                            University Search
                                  |
                                  v
                            Answer Generation
                                  |
                                  v
                         Persistent Memory
```

A central architectural decision is the separation of short-term state and persistent history.

```text
StateManager
    -> structured state for the current interaction

ConversationMemory
    -> persistent SQLite session/message history
```

Raw historical conversation text is not blindly injected into the reasoning or ranking pipeline.

Instead, structured state is restored from stored assistant outputs when a session is resumed.

---

# 5. Core Components

## 5.1 Intent Detection and Structured Extraction

The assistant identifies the recommendation intent and extracts information relevant to the task.

Core fields include:

* country
* field
* requirements

The requirements field may later be decomposed into:

* IELTS score
* tuition preference
* ranking preference
* research interests
* other constraints

---

## 5.2 Adaptive Clarification

When required information is missing, the system asks only for the missing fields.

Example:

```text
Turn 1
User:
Help me choose a university

Missing:
country
field
requirements
```

After:

```text
Turn 2
User:
Germany and Artificial Intelligence
```

the system retains:

```text
country = Germany
field = Artificial Intelligence
```

and asks only for:

```text
requirements
```

---

## 5.3 State Management

`StateManager` preserves structured information across turns.

This allows the assistant to distinguish between:

```text
Artificial Intelligence
```

as an isolated input and the same input following:

```text
Germany
```

in a previous turn.

---

## 5.4 User Profile Modeling

Collected conversation information is converted into a structured profile.

Example:

```json
{
  "country": "Germany",
  "field": "Artificial Intelligence",
  "ielts": 6.5,
  "tuition_preference": "low tuition",
  "ranking_preference": "top",
  "research_interests": [
    "Machine Learning",
    "Computer Vision"
  ]
}
```

---

## 5.5 Personalized Ranking

The ranking engine uses explicit scoring factors.

Canonical weighting:

| Criterion           | Weight |
| ------------------- | -----: |
| Country match       |     20 |
| Field match         |     25 |
| IELTS compatibility |     20 |
| Tuition preference  |     15 |
| Ranking preference  |     20 |

Research-interest alignment is added as a proportional signal.

Canonical Ranking V2 regression values:

| University                     | Match Score |
| ------------------------------ | ----------: |
| Technical University of Munich |       95.45 |
| University of Stuttgart        |       90.91 |
| Saarland University            |       81.82 |

---

## 5.6 Persistent Memory

Conversation history is stored in SQLite.

The system supports:

* automatic session creation
* message persistence
* session listing
* reopening sessions
* history restoration
* structured state restoration

Persistent memory is deliberately separated from live conversation state.

---

# 6. Experimental Design

The research evaluation consists of five main components:

1. single-turn evaluation
2. canonical multi-turn evaluation
3. direct-answer baseline comparison
4. robustness evaluation
5. component ablation

---

# 7. Single-Turn Evaluation

The single-turn evaluation contains **15 samples**.

Metrics include:

* intent accuracy
* missing-information precision
* missing-information recall
* missing-information F1
* missing-information exact match

Results:

| Metric                          |  Result |
| ------------------------------- | ------: |
| Dataset Samples                 |      15 |
| Successfully Evaluated          |      15 |
| Failed Samples                  |       0 |
| Intent Accuracy                 | 100.00% |
| Missing Information Precision   |  91.30% |
| Missing Information Recall      | 100.00% |
| Missing Information F1          |  95.45% |
| Missing Information Exact Match |  86.67% |

The system achieved perfect intent detection on the controlled dataset and high missing-information extraction performance.

The difference between recall and exact match indicates that some predictions included additional missing-field classifications even when all required missing information was successfully identified.

---

# 8. Multi-Turn Evaluation

The canonical multi-turn evaluation contains:

```text
4 conversations
10 total turns
```

Results:

| Metric                          |  Result |
| ------------------------------- | ------: |
| Missing Information Accuracy    | 100.00% |
| Clarification Decision Accuracy | 100.00% |
| Complete Conversation Accuracy  | 100.00% |

These results establish the full-system reference condition used in later comparative and ablation experiments.

---

# 9. Direct-Answer Baseline

A simpler baseline system was created to provide a fair comparison.

The baseline can still:

* detect intent
* identify missing information

However, it does not use:

* adaptive clarification
* conversation state
* persistent reasoning across turns
* session restoration

Its policy always attempts a direct answer.

Baseline policy results:

| Metric                               |  Result |
| ------------------------------------ | ------: |
| Direct Answer Rate                   | 100.00% |
| Incomplete-Prompt Direct Answer Rate | 100.00% |
| Clarification Attempt Rate           |   0.00% |

This design allows the experiment to separate **information recognition** from **interaction policy**.

---

# 10. Adaptive System vs Direct-Answer Baseline

The two systems were evaluated using the same multi-turn scenarios.

Results:

| Metric                           | Adaptive System | Baseline | Difference |
| -------------------------------- | --------------: | -------: | ---------: |
| Missing Information Accuracy     |         100.00% |   50.00% |  +50.00 pp |
| Clarification Decision Accuracy  |         100.00% |   40.00% |  +60.00 pp |
| Complete Conversation Accuracy   |         100.00% |   25.00% |  +75.00 pp |
| Continuation-Turn State Accuracy |         100.00% |   16.67% |  +83.33 pp |
| Premature Direct-Answer Rate ↓   |           0.00% |  100.00% |          — |
| Complete-Input Handling Accuracy |         100.00% |  100.00% |          — |

The strongest difference occurred on continuation turns.

Importantly, both systems reached **100% complete-input handling accuracy**.

This suggests that the advantage of the adaptive system is not caused by a general inability of the baseline to process university requests.

Instead, the advantage appears specifically when:

* information is incomplete
* information is distributed across turns
* the assistant must decide whether to ask or answer

---

# 11. Robustness Evaluation

The robustness suite contains:

```text
10 conversations
26 total turns
16 continuation turns
```

Test categories include:

* paraphrase
* informal language
* typographical noise
* irrelevant context
* reordered information
* fragmented information
* complete input
* research-interest disambiguation
* short fragments
* long-form natural input

Overall results:

| Metric                           | Result |
| -------------------------------- | -----: |
| Missing Information Accuracy     | 96.15% |
| Clarification Decision Accuracy  | 96.15% |
| Complete Conversation Accuracy   | 90.00% |
| Continuation-Turn State Accuracy | 93.75% |
| Failed Turns                     |      0 |

Most categories achieved 100% accuracy.

The primary weakness appeared in the long-form category:

| Metric                 | Long-Form Result |
| ---------------------- | ---------------: |
| Missing Accuracy       |           50.00% |
| Clarification Accuracy |           50.00% |

This limitation was retained rather than modifying the system after evaluation to artificially improve the reported result.

---

# 12. Ablation Study

Ablation experiments were used to isolate the contribution of individual architectural components.

---

## 12.1 No-State Ablation

In this experiment, conversation state was reset before every turn.

The underlying extraction and clarification logic remained available.

Results:

| Metric                             | Full System | No-State |    Change |
| ---------------------------------- | ----------: | -------: | --------: |
| Missing Information Accuracy       |     100.00% |   50.00% | -50.00 pp |
| Clarification Decision Accuracy    |     100.00% |   70.00% | -30.00 pp |
| Complete Conversation Accuracy     |     100.00% |   25.00% | -75.00 pp |
| Continuation-Turn Missing Accuracy |     100.00% |   16.67% | -83.33 pp |

First-turn missing-information and clarification accuracy remained:

```text
100.00%
```

This result is particularly informative.

Removing state did not reduce initial-turn performance, but it caused a large decline on continuation turns.

This supports the interpretation that explicit state tracking is specifically responsible for preserving previously supplied information across the conversation.

---

## 12.2 No-Clarification Ablation

In this experiment:

```text
State Tracking         ON
Adaptive Clarification OFF
```

The system continued to extract and preserve structured information, but its final policy was forced to answer directly.

Results:

| Metric                           | Full System | No-Clarification |     Change |
| -------------------------------- | ----------: | ---------------: | ---------: |
| Missing Information Accuracy     |     100.00% |          100.00% |    0.00 pp |
| Clarification Decision Accuracy  |     100.00% |           40.00% |  -60.00 pp |
| Complete Conversation Accuracy   |     100.00% |           25.00% |  -75.00 pp |
| Premature Direct-Answer Rate     |       0.00% |          100.00% | +100.00 pp |
| Complete-Input Handling Accuracy |     100.00% |          100.00% |    0.00 pp |
| Continuation-Turn State Accuracy |     100.00% |          100.00% |    0.00 pp |

This ablation provides an important distinction.

The system continued to correctly detect missing information:

```text
100.00%
```

and retained conversation state:

```text
100.00%
```

but its interaction reliability declined because it was no longer allowed to act on that information through clarification.

Therefore:

> Knowing that information is missing is not equivalent to making the correct conversational decision.

---

# 13. Main Findings

## Finding 1 — State tracking contributes specifically to multi-turn reliability

The no-state experiment reduced continuation-turn missing-information accuracy:

```text
100.00% -> 16.67%
```

while first-turn performance remained unchanged.

This provides direct experimental evidence for the contribution of structured state tracking.

---

## Finding 2 — Clarification policy is distinct from information extraction

The no-clarification condition preserved:

```text
Missing Information Accuracy = 100.00%
State Accuracy = 100.00%
```

but reduced:

```text
Clarification Decision Accuracy = 40.00%
```

and increased:

```text
Premature Direct-Answer Rate = 100.00%
```

The result supports a modular interpretation of the architecture.

---

## Finding 3 — Direct answering is sufficient when the request is already complete

Both the adaptive system and baseline achieved:

```text
Complete-Input Handling Accuracy = 100.00%
```

The adaptive architecture therefore does not appear to introduce unnecessary clarification when sufficient information is already available in the canonical evaluation.

---

## Finding 4 — The largest benefit appears on continuation turns

The comparison produced:

```text
Adaptive continuation-turn accuracy = 100.00%
Baseline continuation-turn accuracy = 16.67%
```

representing an improvement of:

```text
+83.33 percentage points
```

---

## Finding 5 — Robustness is promising but incomplete

Overall robustness remained high:

```text
96.15% missing-information accuracy
96.15% clarification-decision accuracy
```

but long-form natural requests exposed an identifiable weakness.

This provides a concrete target for future research.

---

# 14. Limitations

Several limitations should be considered when interpreting the results.

### Small Evaluation Dataset

The evaluation datasets are intentionally controlled and relatively small.

Therefore, results should be interpreted as prototype-level experimental evidence rather than broad estimates of real-world LLM performance.

---

### Single Application Domain

The current implementation focuses on university recommendation.

The architecture may generalize to other tasks, but cross-domain evaluation has not yet been performed.

---

### Limited University Dataset

The recommendation database contains a small number of manually controlled university entries.

The current research emphasis is conversational reliability rather than retrieval coverage.

---

### Deterministic Ranking Weights

Ranking weights are manually defined rather than learned from user behavior or preference data.

---

### Limited Research-Interest Vocabulary

Research-interest extraction currently supports a controlled set of areas.

More flexible semantic matching would improve coverage.

---

### Long-Form Input Weakness

The robustness evaluation revealed reduced performance for long natural-language requests.

This represents the clearest observed robustness limitation.

---

### No Human Evaluation

Current evaluation uses predefined expected outputs.

Human judgments of:

* clarification usefulness
* recommendation usefulness
* conversational naturalness
* user satisfaction

have not yet been collected.

---

### No Formal Latency Evaluation

Inference latency, clarification cost, computational cost, and total conversation duration have not yet been formally measured.

---

# 15. Threats to Validity

The reported results may be affected by:

* small dataset size
* manually designed evaluation cases
* overlap between architecture assumptions and test design
* use of a single primary LLM backend
* deterministic or low-temperature extraction
* a controlled recommendation database

Future experiments should therefore use larger independently constructed datasets and multiple model backends.

---

# 16. Future Work

Several research extensions follow naturally from the current system.

## 16.1 Uncertainty-Aware Clarification

The current architecture mainly asks questions when required fields are missing.

A stronger system could also clarify when information is present but uncertain.

For example:

```text
User:
I want something affordable in Europe.
```

The assistant could estimate uncertainty about:

* country
* acceptable tuition
* program field
* geographic flexibility

before deciding whether to ask a question.

---

## 16.2 Learned Clarification Policy

The current clarification policy is deterministic.

A future system could learn:

> When is the value of asking a question greater than the cost of an additional interaction turn?

Possible approaches include:

* reinforcement learning
* preference optimization
* supervised dialogue learning
* contextual bandits

---

## 16.3 Information-Gain-Based Question Selection

When several pieces of information are missing, the assistant could estimate which clarification question would reduce uncertainty the most.

Instead of using a fixed order, the next question could maximize expected information gain.

---

## 16.4 Long-Term User Modeling

Persistent memory could evolve from session restoration into durable preference modeling.

A future assistant might learn recurring preferences such as:

* preferred countries
* tuition sensitivity
* research interests
* academic ambitions
* ranking priorities

across many sessions.

---

## 16.5 Learned Ranking Weights

Ranking weights could be personalized using:

* user feedback
* accepted recommendations
* rejected recommendations
* long-term preferences

instead of being manually defined.

---

## 16.6 Retrieval-Augmented Recommendation

Future versions could connect to:

* official university websites
* admissions APIs
* scholarship databases
* application deadlines
* tuition information
* research-lab information

through retrieval-augmented generation.

---

## 16.7 Larger-Scale Evaluation

Future evaluation should include:

* hundreds or thousands of conversations
* multiple recommendation domains
* adversarial ambiguity
* multilingual input
* multiple LLM backends
* human evaluation
* statistical significance testing

---

# 17. Direct-PhD Research Extension

The current project provides a foundation for broader research on reliable conversational systems.

A possible research direction is:

> Adaptive clarification for uncertainty-aware and personalized LLM assistants.

The current system uses deterministic rules to decide when clarification is necessary.

A future research system could instead estimate:

```text
Uncertainty
+
Expected Information Gain
+
Interaction Cost
+
User Preference
+
Task Risk
```

and dynamically choose between:

```text
Answer now
Ask clarification
Retrieve more information
Verify information
Defer recommendation
```

This transforms clarification from a fixed rule into an intelligent decision problem.

A possible research question is:

> How can an LLM-based assistant learn when clarification is worth the additional interaction cost while preserving reliable, personalized, and efficient multi-turn decision-making?

This direction connects:

* conversational AI
* LLM reliability
* uncertainty estimation
* personalization
* adaptive decision-making
* user modeling
* recommendation systems

and provides a natural continuation of the current project.

---

# 18. Conclusion

This project investigated whether explicit state tracking and adaptive clarification can improve the reliability of an LLM-based university recommendation assistant.

The experiments show that the full adaptive system performed strongly on the controlled multi-turn evaluation.

Compared with a direct-answer baseline, the system achieved substantial improvements on incomplete and continuation-turn requests while maintaining equivalent handling of already-complete requests.

The ablation experiments further demonstrate that state tracking and adaptive clarification serve different roles.

State tracking preserves information across turns.

Adaptive clarification converts awareness of missing information into an appropriate conversational action.

The robustness evaluation indicates that the architecture remains stable under several forms of linguistic variation, although long-form natural language remains an important limitation.

Overall, the results support the central hypothesis:

> Reliable multi-turn LLM assistance benefits not only from better answer generation, but from explicit mechanisms that determine what the system knows, what it still needs to know, and when it should ask before answering.

---

# Reproducibility

Core evaluation:

```bash
python evaluation/evaluate.py
python evaluation/evaluate_multiturn.py
```

Research evaluation:

```bash
python evaluation/evaluate_baseline.py
python evaluation/evaluate_comparison.py
python evaluation/evaluate_robustness.py
python evaluation/evaluate_ablation_state.py
python evaluation/evaluate_ablation_clarification.py
```

Final result aggregation:

```bash
python evaluation/final_results.py
```

Compile regression:

```bash
python -m compileall src evaluation app.py
```

Application:

```bash
python -m src.main
```

Streamlit interface:

```bash
streamlit run app.py
```

---

## Project Status

```text
Stage 1 — Project Structure                    COMPLETE
Stage 2 — Intent + Structured Extraction       COMPLETE
Stage 3 — Adaptive Clarification + State       COMPLETE
Stage 4 — Cleanup + Regression                 COMPLETE
Stage 5 — Personalized Ranking                 COMPLETE
Stage 6 — User Profile Modeling                COMPLETE
Stage 7 — Persistent Memory                    COMPLETE
Stage 8 — Research Evaluation                  COMPLETE
Stage 9 — Finalization                         IN PROGRESS
```
