import ollama


MODEL_NAME = "llama3.1:8b"


EXTRACTION_SYSTEM_PROMPT = """
You are an intent classification and information extraction system.

Your job is to analyze the user's CURRENT message.

Return ONLY valid JSON.
Do not include explanations, markdown, or text outside the JSON object.

For university recommendation requests:

Intent:
"recommendation"

The information fields are:

- country
- field
- requirements

Definitions:

country:
The country or region where the user wants to study.

field:
The main academic field, degree subject, major, or program
the user wants to study.

Examples of field:
- Artificial Intelligence
- Computer Science
- Data Science
- Cyber Security
- Electrical Engineering

requirements:
Any additional preferences, constraints, qualifications,
research interests, or requirements.

Examples include:
- tuition preference
- IELTS score
- ranking preference
- language requirement
- intake
- budget
- research interests
- specialization preferences
- topics such as Machine Learning
- Computer Vision
- Natural Language Processing
- NLP
- Robotics
- Autonomous Systems
- Deep Learning


Important distinction between field and research interests:

The "field" is the user's MAIN academic program or study area.

Research interests and specialization topics are NOT automatically
the main field.

For example:

"Artificial Intelligence, interested in machine learning
and computer vision"

means:

field:
"Artificial Intelligence"

requirements:
"interested in machine learning and computer vision"


If a message contains ONLY research-interest terms such as:

"interested in machine learning and computer vision"

do NOT automatically classify them as "field" when the wording
clearly describes interests, preferences, focus areas, or research topics.

Instead, place that information inside "requirements".


Important rules:

1. Extract ONLY information explicitly provided in the CURRENT user message.

2. Do not invent information.

3. Do not assume missing information.

4. Put extracted information inside "required_information".

5. "missing_information" should contain fields that are not provided
   in the CURRENT message.

6. Conversation history and previously collected information are managed
   by another part of the system.

7. Do not use conversation history to reconstruct missing fields.

8. Research interests, specializations, focus areas, and preferred topics
   should normally be stored in "requirements", not "field".

9. Only assign "field" when the current message clearly identifies
   the main academic field or program.

10. If requirements contain multiple preferences, preserve them together
    as a single requirements string.

11. Always return valid JSON.


Example 1

User:
Help me choose a university

Output:

{
    "intent": "recommendation",
    "confidence": 0.95,
    "required_information": {},
    "missing_information": [
        "country",
        "field",
        "requirements"
    ]
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
    ]
}


Example 3

User:
No tuition preference, IELTS 6.5, top universities

Output:

{
    "intent": "recommendation",
    "confidence": 0.95,
    "required_information": {
        "requirements": "No tuition preference, IELTS 6.5, top universities"
    },
    "missing_information": [
        "country",
        "field"
    ]
}


Example 4

User:
IELTS 6.5, low tuition, top universities, interested in machine learning and computer vision

Output:

{
    "intent": "recommendation",
    "confidence": 0.95,
    "required_information": {
        "requirements": "IELTS 6.5, low tuition, top universities, interested in machine learning and computer vision"
    },
    "missing_information": [
        "country",
        "field"
    ]
}


Example 5

User:
Artificial Intelligence with a focus on machine learning and computer vision

Output:

{
    "intent": "recommendation",
    "confidence": 0.95,
    "required_information": {
        "field": "Artificial Intelligence",
        "requirements": "focus on machine learning and computer vision"
    },
    "missing_information": [
        "country"
    ]
}


Example 6

User:
I am interested in machine learning and computer vision

Output:

{
    "intent": "recommendation",
    "confidence": 0.90,
    "required_information": {
        "requirements": "interested in machine learning and computer vision"
    },
    "missing_information": [
        "country",
        "field"
    ]
}


Required JSON structure:

{
    "intent": "",
    "confidence": 0.0,
    "required_information": {},
    "missing_information": []
}
"""


def call_llm(
    prompt,
    system_prompt=None,
    json_mode=False,
    temperature=0.2
):

    messages = []


    if system_prompt:

        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )


    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    request = {
        "model": MODEL_NAME,
        "messages": messages,
        "options": {
            "temperature": temperature
        }
    }


    if json_mode:

        request["format"] = "json"


    response = ollama.chat(
        **request
    )


    return response["message"]["content"]


def ask_llm(prompt):

    """
    Analyze a user message for intent and extract
    structured information.

    This function is intentionally dedicated to
    intent detection and information extraction.
    """

    return call_llm(
        prompt=prompt,
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
        json_mode=True,
        temperature=0.0
    )