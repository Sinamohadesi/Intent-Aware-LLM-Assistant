import json

from src.llm import call_llm


ANSWER_SYSTEM_PROMPT = """
You are a university recommendation assistant.

Your task is to generate a concise final recommendation
based only on the information provided to you.

Do not invent missing information.

Return ONLY valid JSON.

Required JSON format:

{
    "final_answer": "",
    "recommended_action": "",
    "details": {
        "country": "",
        "field": "",
        "requirements": ""
    }
}
"""


def generate_answer(state):

    if not isinstance(state, dict):

        state = {}


    collected_information = state.get(
        "collected_information",
        {}
    )


    if not isinstance(
        collected_information,
        dict
    ):

        collected_information = {}


    prompt = f"""
User information:

{json.dumps(
    collected_information,
    indent=4,
    ensure_ascii=False
)}

Generate the final recommendation response.
"""


    response = call_llm(
        prompt=prompt,
        system_prompt=ANSWER_SYSTEM_PROMPT,
        json_mode=True,
        temperature=0.2
    )


    try:

        return json.loads(
            response
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        return {
            "final_answer": response,
            "recommended_action": "",
            "details": collected_information
        }