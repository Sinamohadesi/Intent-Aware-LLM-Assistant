import re
from typing import Any, Dict, List


class UserProfile:

    def __init__(
        self,
        country: str = "",
        field: str = "",
        ielts: float | None = None,
        tuition_preference: str = "",
        ranking_preference: str = "",
        research_interests: List[str] | None = None,
    ):

        self.country = country
        self.field = field
        self.ielts = ielts
        self.tuition_preference = tuition_preference
        self.ranking_preference = ranking_preference
        self.research_interests = (
            research_interests
            if research_interests is not None
            else []
        )

    @staticmethod
    def normalize_text(
        value: Any
    ) -> str:

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def extract_ielts(
        requirements: str
    ) -> float | None:

        text = requirements.lower()

        match = re.search(
            r"ielts\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            text
        )

        if not match:
            return None

        try:
            return float(
                match.group(1)
            )

        except ValueError:
            return None

    @staticmethod
    def extract_tuition_preference(
        requirements: str
    ) -> str:

        text = requirements.lower()

        tuition_terms = [
            "no tuition",
            "free tuition",
            "low tuition",
            "cheap",
            "affordable",
        ]

        for term in tuition_terms:

            if term in text:
                return term

        return ""

    @staticmethod
    def extract_ranking_preference(
        requirements: str
    ) -> str:

        text = requirements.lower()

        if "top" in text:
            return "top"

        if "research" in text:
            return "research"

        return ""

    @staticmethod
    def extract_research_interests(
        requirements: str
    ) -> List[str]:

        text = requirements.lower()

        known_interests = {
            "machine learning": "Machine Learning",
            "computer vision": "Computer Vision",
            "natural language processing":
                "Natural Language Processing",
            "nlp":
                "Natural Language Processing",
            "robotics": "Robotics",
            "autonomous systems":
                "Autonomous Systems",
            "data science":
                "Data Science",
            "deep learning":
                "Deep Learning",
        }

        interests = []

        for keyword, normalized_name in (
            known_interests.items()
        ):

            if keyword in text:

                if normalized_name not in interests:
                    interests.append(
                        normalized_name
                    )

        return interests

    @classmethod
    def from_information(
        cls,
        information: Dict[str, Any]
    ) -> "UserProfile":

        country = cls.normalize_text(
            information.get(
                "country",
                ""
            )
        )

        field = cls.normalize_text(
            information.get(
                "field",
                ""
            )
        )

        requirements = cls.normalize_text(
            information.get(
                "requirements",
                ""
            )
        )

        return cls(
            country=country,
            field=field,
            ielts=cls.extract_ielts(
                requirements
            ),
            tuition_preference=(
                cls.extract_tuition_preference(
                    requirements
                )
            ),
            ranking_preference=(
                cls.extract_ranking_preference(
                    requirements
                )
            ),
            research_interests=(
                cls.extract_research_interests(
                    requirements
                )
            ),
        )

    def to_dict(
        self
    ) -> Dict[str, Any]:

        return {
            "country": self.country,
            "field": self.field,
            "ielts": self.ielts,
            "tuition_preference":
                self.tuition_preference,
            "ranking_preference":
                self.ranking_preference,
            "research_interests":
                self.research_interests,
        }