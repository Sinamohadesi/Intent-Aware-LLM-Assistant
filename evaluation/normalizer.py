import json


VALID_INFORMATION_FIELDS = [
    "country",
    "field",
    "requirements"
]


def normalize_intent(intent):

    # --------------------------------
    # 1. Convert input to dictionary
    # --------------------------------

    if isinstance(intent, str):

        try:

            data = json.loads(
                intent
            )

        except (json.JSONDecodeError, TypeError):

            return {
                "intent": normalize_category(intent),
                "collected_information": {},
                "missing_information": []
            }


    elif isinstance(intent, dict):

        data = intent


    else:

        return {
            "intent": "",
            "collected_information": {},
            "missing_information": []
        }


    # --------------------------------
    # 2. Extract collected information
    # --------------------------------

    collected_information = {}


    required_information = data.get(
        "required_information",
        {}
    )


    if isinstance(required_information, dict):

        for field in VALID_INFORMATION_FIELDS:

            value = required_information.get(
                field
            )


            if value not in [
                None,
                ""
            ]:

                collected_information[field] = value


    # --------------------------------
    # 3. Support state-based data
    # --------------------------------

    state = data.get(
        "state",
        {}
    )


    if isinstance(state, dict):

        state_information = state.get(
            "collected_information",
            {}
        )


        if isinstance(state_information, dict):

            for field in VALID_INFORMATION_FIELDS:

                value = state_information.get(
                    field
                )


                if value not in [
                    None,
                    ""
                ]:

                    collected_information[field] = value


    # --------------------------------
    # 4. Support direct fields
    # --------------------------------

    for field in VALID_INFORMATION_FIELDS:

        value = data.get(
            field
        )


        if value not in [
            None,
            ""
        ]:

            collected_information[field] = value


    # --------------------------------
    # 5. Normalize missing information
    # --------------------------------

    missing_information = data.get(
        "missing_information",
        []
    )


    if not isinstance(
        missing_information,
        list
    ):

        missing_information = []


    missing_information = [

        field

        for field in missing_information

        if field in VALID_INFORMATION_FIELDS

    ]


    # --------------------------------
    # 6. Final normalized output
    # --------------------------------

    return {

        "intent": normalize_category(
            data.get(
                "intent",
                ""
            )
        ),

        "collected_information":
            collected_information,

        "missing_information":
            missing_information

    }



def normalize_category(intent):

    intent = str(
        intent
    ).lower().strip()


    recommendation_keywords = [

        "university",
        "college",
        "degree",
        "education",
        "academic",
        "study",
        "recommend",
        "recommendation"

    ]


    for keyword in recommendation_keywords:

        if keyword in intent:

            return "recommendation"


    return intent