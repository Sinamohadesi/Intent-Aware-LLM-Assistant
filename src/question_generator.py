from src.clarification import generate_clarification


def generate_questions(
    intent,
    missing_information
):

    clarification = generate_clarification(
        intent=intent,
        missing_information=missing_information
    )


    return clarification.get(
        "questions",
        []
    )