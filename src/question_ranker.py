QUESTION_PRIORITY = [
    "country",
    "field",
    "requirements"
]


def rank_questions(
    missing_information
):

    if not isinstance(
        missing_information,
        list
    ):

        return []


    unique_fields = []


    for field in missing_information:

        if (
            isinstance(field, str)
            and field not in unique_fields
        ):

            unique_fields.append(
                field
            )


    ranked_fields = []


    for field in QUESTION_PRIORITY:

        if field in unique_fields:

            ranked_fields.append(
                field
            )


    for field in unique_fields:

        if field not in ranked_fields:

            ranked_fields.append(
                field
            )


    return ranked_fields