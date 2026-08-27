import json
import os


class UniversitySearch:

    def __init__(
        self,
        file_path="data/universities.json"
    ):

        if not os.path.exists(
            file_path
        ):

            raise FileNotFoundError(
                f"University data file not found: "
                f"{file_path}"
            )


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


        if not isinstance(
            data,
            list
        ):

            raise ValueError(
                "University data must be a list."
            )


        self.universities = data


    # --------------------------------
    # Text normalization
    # --------------------------------

    def normalize_text(
        self,
        value
    ):

        if value is None:

            return ""


        return (
            str(value)
            .strip()
            .lower()
        )


    # --------------------------------
    # Search
    # --------------------------------

    def search(
        self,
        country=None,
        field=None
    ):

        normalized_country = (
            self.normalize_text(
                country
            )
        )


        normalized_field = (
            self.normalize_text(
                field
            )
        )


        if (
            not normalized_country
            and not normalized_field
        ):

            return []


        results = []


        for university in self.universities:

            if not isinstance(
                university,
                dict
            ):

                continue


            university_country = (
                university.get(
                    "country",
                    ""
                )
            )


            university_field = (
                university.get(
                    "field",
                    ""
                )
            )


            normalized_university_country = (
                self.normalize_text(
                    university_country
                )
            )


            normalized_university_field = (
                self.normalize_text(
                    university_field
                )
            )


            score = 0


            # Country match
            if normalized_country:

                if (
                    normalized_country
                    == normalized_university_country
                ):

                    score += 2


            # Field match
            if normalized_field:

                if (
                    normalized_field
                    == normalized_university_field
                ):

                    score += 2


            if score == 0:

                continue


            result = university.copy()

            result["score"] = score

            results.append(
                result
            )


        results.sort(
            key=lambda item: item[
                "score"
            ],
            reverse=True
        )


        return results