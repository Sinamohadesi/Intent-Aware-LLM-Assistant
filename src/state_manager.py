import copy
import json


class StateManager:

    def __init__(self):

        self.state = {
            "intent": None,
            "collected_information": {},
            "missing_information": []
        }


    def update_intent(
        self,
        intent
    ):

        if intent:

            self.state[
                "intent"
            ] = intent


    def update_information(
        self,
        information,
        allow_overwrite=False
    ):

        if not isinstance(
            information,
            dict
        ):

            return


        collected_information = (
            self.state[
                "collected_information"
            ]
        )


        for key, value in information.items():

            if value in [
                None,
                ""
            ]:

                continue


            current_value = (
                collected_information.get(
                    key
                )
            )


            # Preserve already collected information
            # unless overwrite is explicitly allowed.

            if (
                current_value not in [
                    None,
                    ""
                ]
                and not allow_overwrite
            ):

                continue


            collected_information[
                key
            ] = value


        self.remove_completed_fields()


    def set_missing_information(
        self,
        missing
    ):

        if not isinstance(
            missing,
            list
        ):

            missing = []


        self.state[
            "missing_information"
        ] = list(
            dict.fromkeys(
                missing
            )
        )


        self.remove_completed_fields()


    def remove_completed_fields(
        self
    ):

        completed_information = (
            self.state[
                "collected_information"
            ]
        )


        self.state[
            "missing_information"
        ] = [

            field

            for field in self.state[
                "missing_information"
            ]

            if not completed_information.get(
                field
            )

        ]


    def is_complete(
        self
    ):

        return (
            len(
                self.state[
                    "missing_information"
                ]
            )
            == 0
        )


    def get_state(
        self
    ):

        return copy.deepcopy(
            self.state
        )


    def reset(
        self
    ):

        self.state = {
            "intent": None,
            "collected_information": {},
            "missing_information": []
        }


    def get_json(
        self
    ):

        return json.dumps(
            self.state,
            indent=4,
            ensure_ascii=False
        )