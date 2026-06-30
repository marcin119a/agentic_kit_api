from __future__ import annotations

import asyncio
import json
import sqlite3
import threading
from pathlib import Path

from agents import SessionABC
from agents.items import TResponseInputItem


class PassengerSQLiteSession(SessionABC):
    def __init__(
        self,
        session_id: str,
        passenger_id: str,
        db_path: str | Path = ":memory:",
    ) -> None:
        self.session_id = session_id
        self.passenger_id = passenger_id
        self.session_settings = None

        self._lock = threading.Lock()
        self._db = sqlite3.connect(str(db_path), check_same_thread=False)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._create_tables()

    def _create_tables(self) -> None:
        with self._lock:
            self._db.executescript(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages (session_id, id);

                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    passenger_id TEXT NOT NULL,
                    fact TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_facts_passenger
                ON facts (passenger_id, id);
                """
            )
            self._db.commit()

    async def _run(self, func):
        return await asyncio.to_thread(func)

    def _facts_as_item(self, facts: list[str]) -> TResponseInputItem | None:
        if not facts:
            return None

        facts_text = "\n".join(f"- {fact}" for fact in facts)

        return {
            "role": "developer",
            "content": (
                f"Wiedza o pasażerze passenger_id={self.passenger_id}:\n"
                f"{facts_text}"
            ),
        }

    async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:
        def query():
            with self._lock:
                facts = self._db.execute(
                    """
                    SELECT fact
                    FROM facts
                    WHERE passenger_id = ?
                    ORDER BY id
                    """,
                    (self.passenger_id,),
                ).fetchall()

                if limit is None:
                    messages = self._db.execute(
                        """
                        SELECT data
                        FROM messages
                        WHERE session_id = ?
                        ORDER BY id
                        """,
                        (self.session_id,),
                    ).fetchall()
                else:
                    messages = self._db.execute(
                        """
                        SELECT data
                        FROM messages
                        WHERE session_id = ?
                        ORDER BY id DESC
                        LIMIT ?
                        """,
                        (self.session_id, limit),
                    ).fetchall()
                    messages.reverse()

            items: list[TResponseInputItem] = []

            fact_item = self._facts_as_item([row[0] for row in facts])
            if fact_item:
                items.append(fact_item)

            items.extend(json.loads(row[0]) for row in messages)
            return items

        return await self._run(query)

    async def add_items(self, items: list[TResponseInputItem]) -> None:
        if not items:
            return

        def query():
            with self._lock:
                self._db.executemany(
                    """
                    INSERT INTO messages (session_id, data)
                    VALUES (?, ?)
                    """,
                    [
                        (self.session_id, json.dumps(item))
                        for item in items
                    ],
                )
                self._db.commit()

        await self._run(query)

    async def pop_item(self) -> TResponseInputItem | None:
        def query():
            with self._lock:
                row = self._db.execute(
                    """
                    DELETE FROM messages
                    WHERE id = (
                        SELECT id
                        FROM messages
                        WHERE session_id = ?
                        ORDER BY id DESC
                        LIMIT 1
                    )
                    RETURNING data
                    """,
                    (self.session_id,),
                ).fetchone()

                self._db.commit()

            return json.loads(row[0]) if row else None

        return await self._run(query)

    async def clear_session(self) -> None:
        def query():
            with self._lock:
                self._db.execute(
                    """
                    DELETE FROM messages
                    WHERE session_id = ?
                    """,
                    (self.session_id,),
                )
                self._db.commit()

        await self._run(query)

    async def remember_fact(self, fact: str) -> None:
        def query():
            with self._lock:
                self._db.execute(
                    """
                    INSERT INTO facts (passenger_id, fact)
                    VALUES (?, ?)
                    """,
                    (self.passenger_id, fact),
                )
                self._db.commit()

        await self._run(query)

    def close(self) -> None:
        with self._lock:
            self._db.close()