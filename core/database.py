"""
SQLite database layer for Andishkadeh Management & Market.

This module provides the persistent storage foundation for:
- Users
- Modules
- Chapters
- Lessons
- Lesson progress
- Quiz attempts

The database is intentionally independent from Telegram handlers.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


# ==========================================================
# Database path
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "data"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_PATH = DATABASE_DIR / "bot.db"


# ==========================================================
# Connection
# ==========================================================

def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection.

    Foreign keys are enabled for every connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ==========================================================
# Database initialization
# ==========================================================

def init_database() -> None:
    """
    Create all required database tables.
    """

    with get_connection() as connection:

        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(module_id, chapter_id),

                FOREIGN KEY(module_id)
                    REFERENCES modules(module_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(
                    module_id,
                    chapter_id,
                    lesson_id
                ),

                FOREIGN KEY(module_id)
                    REFERENCES modules(module_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(module_id, chapter_id)
                    REFERENCES chapters(
                        module_id,
                        chapter_id
                    )
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS lesson_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                telegram_id INTEGER NOT NULL,

                module_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,

                started INTEGER NOT NULL DEFAULT 0,
                completed INTEGER NOT NULL DEFAULT 0,

                started_at TEXT,
                completed_at TEXT,

                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(
                    telegram_id,
                    module_id,
                    chapter_id,
                    lesson_id
                ),

                FOREIGN KEY(telegram_id)
                    REFERENCES users(telegram_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                telegram_id INTEGER NOT NULL,

                module_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,

                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL DEFAULT 0,
                score REAL NOT NULL DEFAULT 0,

                started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,

                FOREIGN KEY(telegram_id)
                    REFERENCES users(telegram_id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_users_telegram_id
            ON users(telegram_id);

            CREATE INDEX IF NOT EXISTS idx_lesson_progress_user
            ON lesson_progress(telegram_id);

            CREATE INDEX IF NOT EXISTS idx_lesson_progress_lesson
            ON lesson_progress(
                module_id,
                chapter_id,
                lesson_id
            );

            CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user
            ON quiz_attempts(telegram_id);

            CREATE INDEX IF NOT EXISTS idx_quiz_attempts_lesson
            ON quiz_attempts(
                module_id,
                chapter_id,
                lesson_id
            );
            """
        )


# ==========================================================
# User
# ==========================================================

def upsert_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> None:
    """
    Create or update a Telegram user.
    """

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO users (
                telegram_id,
                username,
                first_name,
                last_name
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(telegram_id)
            DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                telegram_id,
                username,
                first_name,
                last_name,
            ),
        )


# ==========================================================
# Module
# ==========================================================

def upsert_module(
    module_id: str,
    title: str,
) -> None:
    """Create or update a module."""

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO modules (
                module_id,
                title
            )
            VALUES (?, ?)

            ON CONFLICT(module_id)
            DO UPDATE SET
                title = excluded.title,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                module_id,
                title,
            ),
        )


# ==========================================================
# Chapter
# ==========================================================

def upsert_chapter(
    module_id: str,
    chapter_id: str,
    title: str,
) -> None:
    """Create or update a chapter."""

    upsert_module(
        module_id,
        module_id,
    )

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO chapters (
                module_id,
                chapter_id,
                title
            )
            VALUES (?, ?, ?)

            ON CONFLICT(
                module_id,
                chapter_id
            )
            DO UPDATE SET
                title = excluded.title,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                module_id,
                chapter_id,
                title,
            ),
        )


# ==========================================================
# Lesson
# ==========================================================

def upsert_lesson(
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    title: str,
) -> None:
    """Create or update a lesson."""

    upsert_chapter(
        module_id,
        chapter_id,
        chapter_id,
    )

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO lessons (
                module_id,
                chapter_id,
                lesson_id,
                title
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(
                module_id,
                chapter_id,
                lesson_id
            )
            DO UPDATE SET
                title = excluded.title,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                module_id,
                chapter_id,
                lesson_id,
                title,
            ),
        )


# ==========================================================
# Lesson progress
# ==========================================================

def mark_lesson_started(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> None:
    """Mark a lesson as started."""

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO lesson_progress (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
                started,
                started_at
            )
            VALUES (?, ?, ?, ?, 1, CURRENT_TIMESTAMP)

            ON CONFLICT(
                telegram_id,
                module_id,
                chapter_id,
                lesson_id
            )
            DO UPDATE SET
                started = 1,
                started_at = COALESCE(
                    lesson_progress.started_at,
                    CURRENT_TIMESTAMP
                ),
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
            ),
        )


def mark_lesson_completed(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> None:
    """Mark a lesson as completed."""

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO lesson_progress (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
                started,
                completed,
                started_at,
                completed_at
            )
            VALUES (
                ?, ?, ?, ?, 1, 1,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )

            ON CONFLICT(
                telegram_id,
                module_id,
                chapter_id,
                lesson_id
            )
            DO UPDATE SET
                started = 1,
                completed = 1,
                started_at = COALESCE(
                    lesson_progress.started_at,
                    CURRENT_TIMESTAMP
                ),
                completed_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
            ),
        )


# ==========================================================
# Quiz attempts
# ==========================================================

def save_quiz_attempt(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float,
) -> int:
    """
    Save a completed quiz attempt.

    Returns:
        The database ID of the saved attempt.
    """

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO quiz_attempts (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
                total_questions,
                correct_answers,
                score,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
                total_questions,
                correct_answers,
                score,
            ),
        )

        return int(
            cursor.lastrowid
        )


# ==========================================================
# Queries
# ==========================================================

def get_lesson_progress(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return progress for one lesson."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM lesson_progress
            WHERE telegram_id = ?
              AND module_id = ?
              AND chapter_id = ?
              AND lesson_id = ?
            """,
            (
                telegram_id,
                module_id,
                chapter_id,
                lesson_id,
            ),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def get_user_progress(
    telegram_id: int,
    module_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return all lesson progress for a user."""

    with get_connection() as connection:

        if module_id is None:

            rows = connection.execute(
                """
                SELECT *
                FROM lesson_progress
                WHERE telegram_id = ?
                ORDER BY
                    module_id,
                    chapter_id,
                    lesson_id
                """,
                (
                    telegram_id,
                ),
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT *
                FROM lesson_progress
                WHERE telegram_id = ?
                  AND module_id = ?
                ORDER BY
                    chapter_id,
                    lesson_id
                """,
                (
                    telegram_id,
                    module_id,
                ),
            ).fetchall()

    return [
        dict(row)
        for row in rows
    ]


def get_quiz_attempts(
    telegram_id: int,
    module_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return quiz attempts for a user."""

    with get_connection() as connection:

        if module_id is None:

            rows = connection.execute(
                """
                SELECT *
                FROM quiz_attempts
                WHERE telegram_id = ?
                ORDER BY id DESC
                """,
                (
                    telegram_id,
                ),
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT *
                FROM quiz_attempts
                WHERE telegram_id = ?
                  AND module_id = ?
                ORDER BY id DESC
                """,
                (
                    telegram_id,
                    module_id,
                ),
            ).fetchall()

    return [
        dict(row)
        for row in rows
    ]


# ==========================================================
# Database health
# ==========================================================

def database_health_check() -> bool:
    """
    Check whether SQLite is available and usable.
    """

    try:

        with get_connection() as connection:

            connection.execute(
                "SELECT 1"
            ).fetchone()

        return True

    except sqlite3.Error:
        return False


# ==========================================================
# Initialization helper
# ==========================================================

if __name__ == "__main__":
    init_database()

    print(
        f"SQLite database initialized: "
        f"{DATABASE_PATH}"
    )
