import sqlite3
import uuid
from datetime import datetime, timezone


class ConversationMemory:

    VALID_ROLES = {
        "user",
        "assistant",
        "system",
    }

    def __init__(
        self,
        db_path="memory.db",
        session_id=None,
    ):

        self.db_path = db_path

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=30,
        )

        self.connection.row_factory = (
            sqlite3.Row
        )

        self.cursor = (
            self.connection.cursor()
        )

        self._create_tables()

        if session_id:

            if not self.session_exists(
                session_id
            ):

                raise ValueError(
                    f"Memory session not found: "
                    f"{session_id}"
                )

            self.session_id = session_id

        else:

            self.session_id = (
                self._create_session()
            )


    # --------------------------------
    # Database schema
    # --------------------------------

    def _create_tables(
        self
    ):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            memory_sessions (
                session_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            memory_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        self.connection.commit()


    # --------------------------------
    # Session management
    # --------------------------------

    def _create_session(
        self
    ):

        session_id = str(
            uuid.uuid4()
        )

        created_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self.cursor.execute(
            """
            INSERT INTO memory_sessions (
                session_id,
                created_at
            )
            VALUES (?, ?)
            """,
            (
                session_id,
                created_at,
            )
        )

        self.connection.commit()

        return session_id


    def session_exists(
        self,
        session_id
    ):

        self.cursor.execute(
            """
            SELECT 1
            FROM memory_sessions
            WHERE session_id = ?
            LIMIT 1
            """,
            (
                session_id,
            )
        )

        return (
            self.cursor.fetchone()
            is not None
        )


    def get_session_id(
        self
    ):

        return self.session_id


    # --------------------------------
    # Message storage
    # --------------------------------

    def add_message(
        self,
        role,
        content
    ):

        if role not in self.VALID_ROLES:

            raise ValueError(
                f"Invalid message role: {role}"
            )

        if content is None:

            content = ""

        content = str(
            content
        )

        created_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self.cursor.execute(
            """
            INSERT INTO memory_messages (
                session_id,
                role,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                self.session_id,
                role,
                content,
                created_at,
            )
        )

        self.connection.commit()


    # --------------------------------
    # History retrieval
    # --------------------------------

    def get_history(
        self
    ):

        self.cursor.execute(
            """
            SELECT
                role,
                content,
                created_at
            FROM memory_messages
            WHERE session_id = ?
            ORDER BY id ASC
            """,
            (
                self.session_id,
            )
        )

        rows = (
            self.cursor.fetchall()
        )

        return [
            {
                "role": row["role"],
                "content": row["content"],
                "created_at":
                    row["created_at"],
            }
            for row in rows
        ]


    def get_history_text(
        self
    ):

        history = (
            self.get_history()
        )

        lines = []

        for message in history:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            lines.append(
                f"{role}: {content}"
            )

        return "\n".join(
            lines
        )


    # --------------------------------
    # Session discovery
    # --------------------------------

    def list_sessions(
        self,
        limit=10
    ):

        try:

            limit = int(
                limit
            )

        except (TypeError, ValueError):

            limit = 10

        if limit <= 0:

            limit = 10

        self.cursor.execute(
            """
            SELECT
                session_id,
                created_at
            FROM memory_sessions
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (
                limit,
            )
        )

        rows = (
            self.cursor.fetchall()
        )

        return [
            {
                "session_id":
                    row["session_id"],
                "created_at":
                    row["created_at"],
            }
            for row in rows
        ]


    # --------------------------------
    # Cleanup
    # --------------------------------

    def close(
        self
    ):

        if self.connection:

            self.connection.close()

            self.connection = None