from src.llm import call_llm


MEMORY_SYSTEM_PROMPT = """
You are a conversation summarization system.

Your task is to summarize the conversation for future memory use.

Extract only useful information.

Include:

- main topic
- user goal
- known information
- missing information
- important preferences

Do not invent information.

Return concise plain text.
"""


def summarize_conversation(history):

    if history is None:

        history = ""


    if not isinstance(
        history,
        str
    ):

        history = str(
            history
        )


    prompt = f"""
Conversation:

{history}

Create a concise memory summary.
"""


    summary = call_llm(
        prompt=prompt,
        system_prompt=MEMORY_SYSTEM_PROMPT,
        json_mode=False,
        temperature=0.2
    )


    return summary.strip()