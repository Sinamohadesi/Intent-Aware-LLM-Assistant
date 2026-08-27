import json

from src.llm import ask_llm
from evaluation.normalizer import normalize_intent
from src.clarification import generate_clarification
from src.university_search import UniversitySearch
from src.ranking_engine import RankingEngine
from src.user_profile import UserProfile
from src.state_manager import StateManager
from src.memory import ConversationMemory


university_search = UniversitySearch()
ranking_engine = RankingEngine()
state_manager = StateManager()
conversation_memory = ConversationMemory()


REQUIRED_INFORMATION = {
    "recommendation": [
        "country",
        "field",
        "requirements",
    ]
}


# --------------------------------
# Persistent memory helpers
# --------------------------------

def save_assistant_result(
    result
):

    try:

        content = json.dumps(
            result,
            ensure_ascii=False,
        )

        conversation_memory.add_message(
            "assistant",
            content,
        )

    except Exception:

        pass


def restore_state_from_history(
    history
):

    global state_manager

    state_manager = StateManager()

    if not isinstance(
        history,
        list,
    ):
        return False

    # Search backwards for the latest
    # assistant result containing state.

    for message in reversed(
        history
    ):

        if message.get(
            "role"
        ) != "assistant":
            continue

        content = message.get(
            "content",
            ""
        )

        try:

            data = json.loads(
                content
            )

        except Exception:
            continue

        saved_state = data.get(
            "state"
        )

        if not isinstance(
            saved_state,
            dict
        ):
            continue

        intent = saved_state.get(
            "intent"
        )

        if intent:

            state_manager.update_intent(
                intent
            )

        collected_information = (
            saved_state.get(
                "collected_information",
                {}
            )
        )

        if isinstance(
            collected_information,
            dict
        ):

            state_manager.update_information(
                collected_information,
                allow_overwrite=True,
            )

        missing_information = (
            saved_state.get(
                "missing_information",
                []
            )
        )

        if isinstance(
            missing_information,
            list
        ):

            state_manager.set_missing_information(
                missing_information
            )

        return True

    return False


def restore_conversation(
    session_id
):

    global conversation_memory

    if not session_id:

        raise ValueError(
            "Session ID is required."
        )

    conversation_memory.close()

    conversation_memory = (
        ConversationMemory(
            session_id=session_id
        )
    )

    history = (
        conversation_memory.get_history()
    )

    state_restored = (
        restore_state_from_history(
            history
        )
    )

    return {
        "session_id":
            conversation_memory.session_id,
        "history_count":
            len(history),
        "state_restored":
            state_restored,
        "state":
            state_manager.get_state(),
    }


def reset_conversation():

    global state_manager
    global conversation_memory

    state_manager = StateManager()

    conversation_memory.close()

    conversation_memory = (
        ConversationMemory()
    )


# --------------------------------
# Ranking merge
# --------------------------------

def merge_rankings_with_universities(
    universities,
    rankings
):

    rankings_by_name = {
        item.get("name"): item
        for item in rankings
    }

    ranked_universities = []

    for university in universities:

        university_result = (
            university.copy()
        )

        ranking_result = (
            rankings_by_name.get(
                university.get(
                    "name"
                ),
                {},
            )
        )

        university_result[
            "match_score"
        ] = ranking_result.get(
            "match_score",
            0.0,
        )

        university_result[
            "reasons"
        ] = ranking_result.get(
            "reasons",
            [],
        )

        university_result[
            "score_breakdown"
        ] = ranking_result.get(
            "breakdown",
            {},
        )

        ranked_universities.append(
            university_result
        )

    ranked_universities.sort(
        key=lambda item: item.get(
            "match_score",
            0.0,
        ),
        reverse=True,
    )

    return ranked_universities


# --------------------------------
# Main processing
# --------------------------------

def process_query(
    user_input
):

    # -----------------------------
    # 1. Store user message
    # -----------------------------

    try:

        conversation_memory.add_message(
            "user",
            user_input,
        )

    except Exception:

        pass


    # -----------------------------
    # 2. Analyze current message
    # -----------------------------

    llm_response = ask_llm(
        user_input
    )

    try:

        llm_data = json.loads(
            llm_response
        )

    except Exception:

        llm_data = {}


    # -----------------------------
    # 3. Normalize extraction
    # -----------------------------

    intent_data = normalize_intent(
        llm_response
    )

    intent = intent_data.get(
        "intent",
        "",
    )


    # -----------------------------
    # 4. Update short-term state
    # -----------------------------

    state_manager.update_intent(
        intent
    )

    collected_information = (
        intent_data.get(
            "collected_information",
            {},
        )
    )

    if collected_information:

        state_manager.update_information(
            collected_information
        )

    state = (
        state_manager.get_state()
    )

    result = {
        "intent": intent,
        "needs_clarification": False,
        "state": state,
    }


    # -----------------------------
    # 5. Recommendation workflow
    # -----------------------------

    if intent == "recommendation":

        information = state.get(
            "collected_information",
            {},
        )

        required_fields = (
            REQUIRED_INFORMATION.get(
                intent,
                [],
            )
        )

        missing_information = [
            field
            for field in required_fields
            if not information.get(
                field
            )
        ]

        state_manager.set_missing_information(
            missing_information
        )

        state = (
            state_manager.get_state()
        )

        result[
            "state"
        ] = state


        # -----------------------------
        # 6. Clarification
        # -----------------------------

        if missing_information:

            clarification = (
                generate_clarification(
                    intent,
                    missing_information,
                )
            )

            result[
                "needs_clarification"
            ] = True

            result[
                "questions"
            ] = clarification.get(
                "questions",
                [],
            )

            save_assistant_result(
                result
            )

            return result


        # -----------------------------
        # 7. Search universities
        # -----------------------------

        universities = (
            university_search.search(
                information.get(
                    "country"
                ),
                information.get(
                    "field"
                ),
            )
        )


        # -----------------------------
        # 8. Build structured profile
        # -----------------------------

        user_profile = (
            UserProfile.from_information(
                information
            )
        )

        ranking_profile = (
            user_profile.to_dict()
        )


        # -----------------------------
        # 9. Rank universities
        # -----------------------------

        rankings = (
            ranking_engine.rank(
                universities,
                ranking_profile,
            )
        )

        ranked_universities = (
            merge_rankings_with_universities(
                universities,
                rankings,
            )
        )

        result[
            "answer"
        ] = {
            "final_answer":
                "Recommended universities ranked by compatibility.",
            "universities":
                ranked_universities,
            "requirements":
                information,
            "ranking_profile":
                ranking_profile,
        }

        save_assistant_result(
            result
        )

        return result


    # -----------------------------
    # 10. Other intents
    # -----------------------------

    result[
        "answer"
    ] = llm_data

    save_assistant_result(
        result
    )

    return result


# --------------------------------
# CLI
# --------------------------------

if __name__ == "__main__":

    try:

        print(
            f"Memory Session: "
            f"{conversation_memory.session_id}"
        )

        print(
            "Commands: "
            "sessions | stop | resume <session_id> | exit"
        )

        while True:

            query = input(
                "User: "
            )

            command = (
                query.strip()
            )

            lowered_command = (
                command.lower()
            )


            # -------------------------
            # Exit
            # -------------------------

            if lowered_command == "exit":

                break


            # -------------------------
            # New conversation
            # -------------------------

            if lowered_command == "stop":

                reset_conversation()

                print(
                    "\nConversation reset. "
                    "New memory session started."
                )

                print(
                    f"Memory Session: "
                    f"{conversation_memory.session_id}\n"
                )

                continue


            # -------------------------
            # List saved sessions
            # -------------------------

            if lowered_command == "sessions":

                sessions = (
                    conversation_memory.list_sessions(
                        limit=10
                    )
                )

                if not sessions:

                    print(
                        "\nNo saved sessions found.\n"
                    )

                    continue

                print(
                    "\nSaved memory sessions:\n"
                )

                for index, session in enumerate(
                    sessions,
                    start=1
                ):

                    print(
                        f"{index}. "
                        f"{session['session_id']}"
                    )

                    print(
                        f"   Created: "
                        f"{session['created_at']}"
                    )

                print()

                continue


            # -------------------------
            # Resume old conversation
            # -------------------------

            if lowered_command.startswith(
                "resume "
            ):

                session_id = (
                    command[
                        len("resume "):
                    ].strip()
                )

                try:

                    restored = (
                        restore_conversation(
                            session_id
                        )
                    )

                    print(
                        "\nConversation restored."
                    )

                    print(
                        json.dumps(
                            restored,
                            indent=4,
                            ensure_ascii=False,
                        )
                    )

                    print()

                except Exception as error:

                    print(
                        f"\nRestore failed: "
                        f"{error}\n"
                    )

                continue


            # -------------------------
            # Normal user message
            # -------------------------

            result = process_query(
                query
            )

            print(
                json.dumps(
                    result,
                    indent=4,
                    ensure_ascii=False,
                )
            )


    finally:

        conversation_memory.close()