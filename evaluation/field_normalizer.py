FIELD_ALIASES = {
    "country": "country",
    "location": "country",
    "region": "country",
    "preferred_country": "country",

    "field": "field",
    "study_field": "field",
    "academic_field": "field",
    "program": "field",
    "programme": "field",
    "major": "field",

    "requirements": "requirements",
    "requirement": "requirements",
    "preferences": "requirements",
    "preference": "requirements",
    "constraints": "requirements",
    "constraint": "requirements"
}


VALID_FIELDS = {
    "country",
    "field",
    "requirements"
}


def normalize_field(field):

    if not isinstance(field, str):
        return None


    normalized = (
        field
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


    normalized = FIELD_ALIASES.get(
        normalized,
        normalized
    )


    if normalized not in VALID_FIELDS:
        return None


    return normalized


def normalize_fields(fields):

    if not isinstance(fields, list):
        return []


    normalized_fields = []


    for field in fields:

        normalized = normalize_field(
            field
        )


        if (
            normalized
            and normalized not in normalized_fields
        ):

            normalized_fields.append(
                normalized
            )


    return normalized_fields