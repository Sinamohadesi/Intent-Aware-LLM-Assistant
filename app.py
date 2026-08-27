import json

import streamlit as st

import src.main as core


st.set_page_config(
    page_title="Intent-Aware LLM Assistant",
    page_icon="🎓",
    layout="centered",
)


st.title("Intent-Aware LLM Assistant")

st.caption(
    "University Recommendation with Adaptive Clarification"
)


# --------------------------------
# Helper functions
# --------------------------------

def result_to_ui_content(
    result
):

    if not isinstance(
        result,
        dict
    ):

        return result


    # -----------------------------
    # Clarification
    # -----------------------------

    if result.get(
        "needs_clarification"
    ):

        return {
            "type": "questions",
            "questions": result.get(
                "questions",
                []
            )
        }


    # -----------------------------
    # Final answer
    # -----------------------------

    answer = result.get(
        "answer",
        {}
    )


    if (
        isinstance(
            answer,
            dict
        )
        and "universities" in answer
    ):

        return {
            "type": "recommendations",
            "final_answer": answer.get(
                "final_answer",
                ""
            ),
            "universities": answer.get(
                "universities",
                []
            )
        }


    if answer:

        return answer


    return "No answer available."


def persistent_history_to_ui(
    history
):

    ui_messages = []


    if not isinstance(
        history,
        list
    ):

        return ui_messages


    for message in history:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )


        # -------------------------
        # User messages
        # -------------------------

        if role == "user":

            ui_messages.append(
                {
                    "role": "user",
                    "content": content
                }
            )

            continue


        # -------------------------
        # Assistant messages
        # -------------------------

        if role == "assistant":

            try:

                result = json.loads(
                    content
                )

                assistant_content = (
                    result_to_ui_content(
                        result
                    )
                )

            except Exception:

                assistant_content = content


            ui_messages.append(
                {
                    "role": "assistant",
                    "content": assistant_content
                }
            )


    return ui_messages


def load_current_memory_history():

    history = (
        core.conversation_memory.get_history()
    )

    st.session_state.messages = (
        persistent_history_to_ui(
            history
        )
    )


# --------------------------------
# Session state
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "restored_session_id" not in st.session_state:

    st.session_state.restored_session_id = None


if "session_notice" not in st.session_state:

    st.session_state.session_notice = None


# --------------------------------
# Sidebar - Persistent Memory
# --------------------------------

with st.sidebar:

    st.header(
        "Conversation Memory"
    )


    current_session_id = (
        core.conversation_memory.session_id
    )


    st.markdown(
        "**Current Session**"
    )


    st.code(
        current_session_id,
        language=None
    )


    st.divider()


    # -----------------------------
    # Saved sessions
    # -----------------------------

    st.subheader(
        "Saved Sessions"
    )


    try:

        saved_sessions = (
            core.conversation_memory.list_sessions(
                limit=10
            )
        )

    except Exception:

        saved_sessions = []


    if saved_sessions:

        session_options = {
            (
                f"{index}. "
                f"{session['session_id'][:8]}... "
                f"| {session['created_at']}"
            ):
            session["session_id"]

            for index, session in enumerate(
                saved_sessions,
                start=1
            )
        }


        selected_label = st.selectbox(
            "Choose a session",
            options=list(
                session_options.keys()
            )
        )


        selected_session_id = (
            session_options.get(
                selected_label
            )
        )


        if st.button(
            "Resume Selected Session",
            use_container_width=True
        ):

            try:

                restored = (
                    core.restore_conversation(
                        selected_session_id
                    )
                )


                load_current_memory_history()


                st.session_state[
                    "restored_session_id"
                ] = selected_session_id


                if restored.get(
                    "state_restored"
                ):

                    st.session_state[
                        "session_notice"
                    ] = (
                        "Conversation restored successfully."
                    )

                else:

                    st.session_state[
                        "session_notice"
                    ] = (
                        "Session restored. "
                        "No saved conversation state was available."
                    )


                st.rerun()


            except Exception as error:

                st.error(
                    f"Restore failed: {error}"
                )


    else:

        st.info(
            "No saved sessions found."
        )


    st.divider()


    # -----------------------------
    # New session
    # -----------------------------

    if st.button(
        "Start New Conversation",
        use_container_width=True
    ):

        core.reset_conversation()

        st.session_state.messages = []

        st.session_state[
            "restored_session_id"
        ] = None

        st.session_state[
            "session_notice"
        ] = (
            "New conversation started."
        )

        st.rerun()


# --------------------------------
# Session notification
# --------------------------------

if st.session_state.session_notice:

    st.success(
        st.session_state.session_notice
    )

    st.session_state.session_notice = None


# --------------------------------
# Reset conversation
# --------------------------------

if st.button(
    "Reset Conversation"
):

    core.reset_conversation()

    st.session_state.messages = []

    st.session_state[
        "restored_session_id"
    ] = None

    st.rerun()


# --------------------------------
# Render chat history
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        content = message["content"]


        if isinstance(
            content,
            str
        ):

            st.markdown(
                content
            )


        elif isinstance(
            content,
            dict
        ):

            message_type = content.get(
                "type"
            )


            # -------------------------
            # Clarification questions
            # -------------------------

            if message_type == "questions":

                questions = content.get(
                    "questions",
                    []
                )


                for question in questions:

                    st.markdown(
                        f"- {question}"
                    )


            # -------------------------
            # University recommendations
            # -------------------------

            elif message_type == "recommendations":

                final_answer = content.get(
                    "final_answer",
                    ""
                )


                universities = content.get(
                    "universities",
                    []
                )


                if final_answer:

                    st.markdown(
                        final_answer
                    )


                for index, university in enumerate(
                    universities,
                    start=1
                ):

                    name = university.get(
                        "name",
                        "Unknown University"
                    )


                    match_score = university.get(
                        "match_score",
                        0
                    )


                    country = university.get(
                        "country",
                        ""
                    )


                    field = university.get(
                        "field",
                        ""
                    )


                    tuition = university.get(
                        "tuition",
                        ""
                    )


                    ielts = university.get(
                        "ielts",
                        ""
                    )


                    reasons = university.get(
                        "reasons",
                        []
                    )


                    st.markdown(
                        f"### {index}. {name}"
                    )


                    st.markdown(
                        f"**Match Score:** "
                        f"{match_score}%"
                    )


                    if country:

                        st.markdown(
                            f"- **Country:** "
                            f"{country}"
                        )


                    if field:

                        st.markdown(
                            f"- **Field:** "
                            f"{field}"
                        )


                    if tuition:

                        st.markdown(
                            f"- **Tuition:** "
                            f"{tuition}"
                        )


                    if ielts != "":

                        st.markdown(
                            f"- **IELTS:** "
                            f"{ielts}"
                        )


                    if reasons:

                        st.markdown(
                            "**Why it matches:**"
                        )


                        for reason in reasons:

                            st.markdown(
                                f"- {reason}"
                            )


                    st.divider()


            else:

                st.json(
                    content
                )


# --------------------------------
# User input
# --------------------------------

user_input = st.chat_input(
    "Type your message..."
)


if user_input:

    # -----------------------------
    # Render/store user message
    # only in Streamlit state.
    #
    # process_query() handles
    # persistent SQLite storage.
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_input
        )


    # -----------------------------
    # Process through canonical
    # backend
    # -----------------------------

    result = (
        core.process_query(
            user_input
        )
    )


    assistant_content = (
        result_to_ui_content(
            result
        )
    )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_content
        }
    )


    st.rerun()