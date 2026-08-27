QUESTION_MAP = {
    "country":
        "Which country or region are you interested in?",

    "field":
        "What field of study or academic area are you interested in?",

    "requirements":
        "Do you have any specific requirements or constraints? "
        "(tuition, ranking, language, intake, etc.)"
}


QUESTION_ORDER = [
    "country",
    "field",
    "requirements"
]


def generate_clarification(
    intent,
    missing_information
):

    if not isinstance(
        missing_information,
        list
    ):

        missing_information = []


    unique_missing = []


    for field in missing_information:

        if (
            isinstance(field, str)
            and field not in unique_missing
        ):

            unique_missing.append(
                field
            )


    ordered_missing = []


    for field in QUESTION_ORDER:

        if field in unique_missing:

            ordered_missing.append(
                field
            )


    for field in unique_missing:

        if field not in ordered_missing:

            ordered_missing.append(
                field
            )


    questions = []


    for field in ordered_missing:

        if field in QUESTION_MAP:

            question = QUESTION_MAP[
                field
            ]

        else:

            readable_field = (
                field
                .replace("_", " ")
                .strip()
            )


            question = (
                f"Please provide your "
                f"{readable_field}."
            )


        questions.append(
            question
        )


    return {

        "intent": intent,

        "needs_clarification":
            len(questions) > 0,

        "missing_information":
            ordered_missing,

        "questions":
            questions

    }