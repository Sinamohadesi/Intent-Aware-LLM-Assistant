from typing import Any, Dict, List


class RankingEngine:

    WEIGHTS = {
        "country": 20,
        "field": 25,
        "ielts": 20,
        "tuition": 15,
        "ranking": 20,
        "research_interests": 10,
    }

    def normalize_text(
        self,
        value: Any
    ) -> str:

        if value is None:
            return ""

        return str(value).strip().lower()

    def is_ielts_compatible(
        self,
        user_ielts: Any,
        required_ielts: Any
    ) -> bool:

        try:
            user_score = float(user_ielts)
            required_score = float(required_ielts)

        except (TypeError, ValueError):
            return False

        return user_score >= required_score

    def matches_tuition_preference(
        self,
        preference: Any,
        university_tuition: Any
    ) -> bool:

        normalized_preference = self.normalize_text(
            preference
        )

        normalized_tuition = self.normalize_text(
            university_tuition
        )

        if not normalized_preference:
            return False

        if not normalized_tuition:
            return False

        low_cost_terms = [
            "low",
            "cheap",
            "affordable",
            "no tuition",
            "free",
        ]

        no_tuition_terms = [
            "no tuition",
            "free",
        ]

        if any(
            term in normalized_preference
            for term in no_tuition_terms
        ):
            return any(
                term in normalized_tuition
                for term in no_tuition_terms
            )

        if any(
            term in normalized_preference
            for term in low_cost_terms
        ):
            return any(
                term in normalized_tuition
                for term in low_cost_terms
            )

        return (
            normalized_preference
            in normalized_tuition
        )

    def matches_ranking_preference(
        self,
        preference: Any,
        university_ranking: Any
    ) -> bool:

        normalized_preference = self.normalize_text(
            preference
        )

        normalized_ranking = self.normalize_text(
            university_ranking
        )

        if not normalized_preference:
            return False

        if not normalized_ranking:
            return False

        if "top" in normalized_preference:
            return "top" in normalized_ranking

        if "research" in normalized_preference:
            return "research" in normalized_ranking

        return (
            normalized_preference
            in normalized_ranking
        )

    def match_research_interests(
        self,
        research_interests: List[str],
        university_keywords: List[str]
    ) -> Dict[str, Any]:

        normalized_interests = [
            self.normalize_text(
                interest
            )
            for interest in research_interests
            if self.normalize_text(
                interest
            )
        ]

        normalized_keywords = {
            self.normalize_text(
                keyword
            )
            for keyword in university_keywords
            if self.normalize_text(
                keyword
            )
        }

        matched_interests = []

        for original_interest, normalized_interest in zip(
            research_interests,
            normalized_interests
        ):

            if normalized_interest in normalized_keywords:

                if original_interest not in matched_interests:
                    matched_interests.append(
                        original_interest
                    )

        total_interests = len(
            normalized_interests
        )

        matched_count = len(
            matched_interests
        )

        if total_interests == 0:

            match_ratio = 0.0

        else:

            match_ratio = (
                matched_count
                / total_interests
            )

        points = round(
            self.WEIGHTS[
                "research_interests"
            ]
            * match_ratio,
            2
        )

        return {
            "matched": matched_count > 0,
            "points": points,
            "matched_interests":
                matched_interests,
            "matched_count":
                matched_count,
            "total_interests":
                total_interests,
        }

    def calculate_score(
        self,
        university: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:

        earned_score = 0.0
        available_score = 0.0

        breakdown = {}
        reasons = []

        # -----------------------------
        # Country
        # -----------------------------

        user_country = self.normalize_text(
            user_profile.get(
                "country"
            )
        )

        university_country = self.normalize_text(
            university.get(
                "country"
            )
        )

        if user_country:

            available_score += self.WEIGHTS[
                "country"
            ]

            matched = (
                user_country
                == university_country
            )

            if matched:

                earned_score += self.WEIGHTS[
                    "country"
                ]

                reasons.append(
                    "Country matches the user's preference."
                )

            breakdown["country"] = {
                "matched": matched,
                "points": (
                    self.WEIGHTS["country"]
                    if matched
                    else 0
                ),
            }

        # -----------------------------
        # Field
        # -----------------------------

        user_field = self.normalize_text(
            user_profile.get(
                "field"
            )
        )

        university_field = self.normalize_text(
            university.get(
                "field"
            )
        )

        if user_field:

            available_score += self.WEIGHTS[
                "field"
            ]

            matched = (
                user_field
                == university_field
            )

            if matched:

                earned_score += self.WEIGHTS[
                    "field"
                ]

                reasons.append(
                    "Field of study matches the user's preference."
                )

            breakdown["field"] = {
                "matched": matched,
                "points": (
                    self.WEIGHTS["field"]
                    if matched
                    else 0
                ),
            }

        # -----------------------------
        # IELTS
        # -----------------------------

        user_ielts = user_profile.get(
            "ielts"
        )

        if user_ielts is not None:

            available_score += self.WEIGHTS[
                "ielts"
            ]

            matched = self.is_ielts_compatible(
                user_ielts,
                university.get(
                    "ielts"
                )
            )

            if matched:

                earned_score += self.WEIGHTS[
                    "ielts"
                ]

                reasons.append(
                    "IELTS score meets the university requirement."
                )

            breakdown["ielts"] = {
                "matched": matched,
                "points": (
                    self.WEIGHTS["ielts"]
                    if matched
                    else 0
                ),
            }

        # -----------------------------
        # Tuition
        # -----------------------------

        tuition_preference = (
            user_profile.get(
                "tuition_preference"
            )
        )

        if self.normalize_text(
            tuition_preference
        ):

            available_score += self.WEIGHTS[
                "tuition"
            ]

            matched = (
                self.matches_tuition_preference(
                    tuition_preference,
                    university.get(
                        "tuition"
                    )
                )
            )

            if matched:

                earned_score += self.WEIGHTS[
                    "tuition"
                ]

                reasons.append(
                    "Tuition matches the user's cost preference."
                )

            breakdown["tuition"] = {
                "matched": matched,
                "points": (
                    self.WEIGHTS["tuition"]
                    if matched
                    else 0
                ),
            }

        # -----------------------------
        # Ranking preference
        # -----------------------------

        ranking_preference = (
            user_profile.get(
                "ranking_preference"
            )
        )

        if self.normalize_text(
            ranking_preference
        ):

            available_score += self.WEIGHTS[
                "ranking"
            ]

            matched = (
                self.matches_ranking_preference(
                    ranking_preference,
                    university.get(
                        "ranking"
                    )
                )
            )

            if matched:

                earned_score += self.WEIGHTS[
                    "ranking"
                ]

                reasons.append(
                    "University ranking matches the user's preference."
                )

            breakdown["ranking"] = {
                "matched": matched,
                "points": (
                    self.WEIGHTS["ranking"]
                    if matched
                    else 0
                ),
            }

        # -----------------------------
        # Research interests
        # -----------------------------

        research_interests = (
            user_profile.get(
                "research_interests",
                []
            )
        )

        if (
            isinstance(
                research_interests,
                list
            )
            and research_interests
        ):

            available_score += self.WEIGHTS[
                "research_interests"
            ]

            research_result = (
                self.match_research_interests(
                    research_interests,
                    university.get(
                        "keywords",
                        []
                    )
                )
            )

            earned_score += (
                research_result[
                    "points"
                ]
            )

            breakdown[
                "research_interests"
            ] = research_result

            matched_interests = (
                research_result.get(
                    "matched_interests",
                    []
                )
            )

            if matched_interests:

                reasons.append(
                    "Research interests match: "
                    + ", ".join(
                        matched_interests
                    )
                    + "."
                )

        # -----------------------------
        # Final normalized score
        # -----------------------------

        if available_score == 0:

            match_score = 0.0

        else:

            match_score = round(
                (
                    earned_score
                    / available_score
                )
                * 100,
                2
            )

        return {
            "name": university.get(
                "name",
                ""
            ),
            "match_score":
                match_score,
            "earned_score":
                round(
                    earned_score,
                    2
                ),
            "available_score":
                round(
                    available_score,
                    2
                ),
            "reasons":
                reasons,
            "breakdown":
                breakdown,
        }

    def rank(
        self,
        universities: List[Dict[str, Any]],
        user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        results = []

        for university in universities:

            if not isinstance(
                university,
                dict
            ):
                continue

            result = self.calculate_score(
                university,
                user_profile
            )

            results.append(
                result
            )

        results.sort(
            key=lambda item: item[
                "match_score"
            ],
            reverse=True
        )

        return results