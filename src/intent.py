from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class IntentResult:

    intent: str = ""

    confidence: float = 0.0

    required_information: Dict[str, Any] = field(
        default_factory=dict
    )

    missing_information: List[str] = field(
        default_factory=list
    )


    @classmethod
    def from_dict(
        cls,
        data
    ):

        if not isinstance(
            data,
            dict
        ):

            data = {}


        intent = data.get(
            "intent",
            ""
        )


        confidence = data.get(
            "confidence",
            0.0
        )


        required_information = data.get(
            "required_information",
            {}
        )


        missing_information = data.get(
            "missing_information",
            []
        )


        if not isinstance(
            required_information,
            dict
        ):

            required_information = {}


        if not isinstance(
            missing_information,
            list
        ):

            missing_information = []


        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0.0


        return cls(
            intent=str(intent),
            confidence=confidence,
            required_information=required_information,
            missing_information=missing_information
        )


    def to_dict(self):

        return {
            "intent":
                self.intent,

            "confidence":
                self.confidence,

            "required_information":
                self.required_information,

            "missing_information":
                self.missing_information
        }