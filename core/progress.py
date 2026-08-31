"""
User progress management for Andishkadeh Management & Market.

This module provides a clean application layer over the SQLite
lesson_progress table.

Responsibilities:
- Register users
- Mark lessons as started
- Mark lessons as completed
- Read lesson progress
- Calculate module progress
- Calculate chapter progress
- Find the user's latest completed lesson
"""

from __future__ import annotations

from typing import Any

from core.database import (
    get_connection,
    init_database,
    mark_lesson_completed,
    mark_lesson_started,
    upsert_user,
)


# ==========================================================
# Initialization
# ==========================================================

def initialize_progress_system() -> None:
    """Initialize the database required by the progress system."""

    init_database()


# ==========================================================
# User
# ==========================================================

def register_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> None:
    """Create or update a Telegram user."""

    upsert_user(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )


# ==========================================================
# Lesson events
# ==========================================================

def start_lesson(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> None:
    """
    Mark a lesson as started.

    The user is created automatically when necessary.
    """

    register_user(
        telegram_id=telegram_id,
    )

    mark_lesson_started(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )


def complete_lesson(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> None:
    """
    Mark a lesson as completed.

    Completion automatically implies that the lesson
    has been started.
    """

    register_user(
        telegram_id=telegram_id,
    )

    mark_lesson_completed(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )


# ==========================================================
# Single lesson progress
# ==========================================================

def get_lesson_status(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any]:
    """Return normalized progress for one lesson."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                started,
                completed,
                started_at,
                completed_at,
                updated_at
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
        return {
            "started": False,
            "completed": False,
            "started_at": None,
            "completed_at": None,
            "updated_at": None,
        }

    return {
        "started": bool(row["started"]),
        "completed": bool(row["completed"]),
        "started_at": row["started_at"],
        "completed_at": row["completed_at"],
        "updated_at": row["updated_at"],
    }


def is_lesson_started(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Return whether a lesson has been started."""

    status = get_lesson_status(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    return status["started"]


def is_lesson_completed(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Return whether a lesson has been completed."""

    status = get_lesson_status(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    return status["completed"]


# ==========================================================
# Chapter progress
# ==========================================================

def get_chapter_progress(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
) -> dict[str, Any]:
    """
    Calculate chapter progress.

    Only lessons registered in the lessons table are counted.
    """

    with get_connection() as connection:

        total = connection.execute(
            """
            SELECT COUNT(*)
            FROM lessons
            WHERE module_id = ?
              AND chapter_id = ?
            """,
            (
                module_id,
                chapter_id,
            ),
        ).fetchone()[0]

        completed = connection.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress
            WHERE telegram_id = ?
              AND module_id = ?
              AND chapter_id = ?
              AND completed = 1
            """,
            (
                telegram_id,
                module_id,
                chapter_id,
            ),
        ).fetchone()[0]

        started = connection.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress
            WHERE telegram_id = ?
              AND module_id = ?
              AND chapter_id = ?
              AND started = 1
            """,
            (
                telegram_id,
                module_id,
                chapter_id,
            ),
        ).fetchone()[0]

    percentage = (
        round(
            completed / total * 100,
            2,
        )
        if total > 0
        else 0.0
    )

    return {
        "module_id": module_id,
        "chapter_id": chapter_id,
        "total_lessons": total,
        "started_lessons": started,
        "completed_lessons": completed,
        "remaining_lessons": max(
            total - completed,
            0,
        ),
        "percentage": percentage,
        "completed": (
            total > 0
            and completed >= total
        ),
    }


# ==========================================================
# Module progress
# ==========================================================

def get_module_progress(
    telegram_id: int,
    module_id: str,
) -> dict[str, Any]:
    """
    Calculate complete progress for a module.
    """

    with get_connection() as connection:

        total = connection.execute(
            """
            SELECT COUNT(*)
            FROM lessons
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]

        completed = connection.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress
            WHERE telegram_id = ?
              AND module_id = ?
              AND completed = 1
            """,
            (
                telegram_id,
                module_id,
            ),
        ).fetchone()[0]

        started = connection.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress
            WHERE telegram_id = ?
              AND module_id = ?
              AND started = 1
            """,
            (
                telegram_id,
                module_id,
            ),
        ).fetchone()[0]

        chapters = connection.execute(
            """
            SELECT
                chapter_id,
                title
            FROM chapters
            WHERE module_id = ?
            ORDER BY id
            """,
            (
                module_id,
            ),
        ).fetchall()

    percentage = (
        round(
            completed / total * 100,
            2,
        )
        if total > 0
        else 0.0
    )

    chapter_progress = []

    for chapter in chapters:

        chapter_progress.append(
            get_chapter_progress(
                telegram_id=telegram_id,
                module_id=module_id,
                chapter_id=chapter["chapter_id"],
            )
        )

    return {
        "module_id": module_id,
        "total_lessons": total,
        "started_lessons": started,
        "completed_lessons": completed,
        "remaining_lessons": max(
            total - completed,
            0,
        ),
        "percentage": percentage,
        "completed": (
            total > 0
            and completed >= total
        ),
        "chapters": chapter_progress,
    }


# ==========================================================
# User progress
# ==========================================================

def get_user_progress(
    telegram_id: int,
    module_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return stored lesson progress for a user."""

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


# ==========================================================
# Latest completed lesson
# ==========================================================

def get_last_completed_lesson(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any] | None:
    """Return the most recently completed lesson."""

    with get_connection() as connection:

        if module_id is None:

            row = connection.execute(
                """
                SELECT *
                FROM lesson_progress
                WHERE telegram_id = ?
                  AND completed = 1
                ORDER BY completed_at DESC, id DESC
                LIMIT 1
                """,
                (
                    telegram_id,
                ),
            ).fetchone()

        else:

            row = connection.execute(
                """
                SELECT *
                FROM lesson_progress
                WHERE telegram_id = ?
                  AND module_id = ?
                  AND completed = 1
                ORDER BY completed_at DESC, id DESC
                LIMIT 1
                """,
                (
                    telegram_id,
                    module_id,
                ),
            ).fetchone()

    if row is None:
        return None

    return dict(row)


# ==========================================================
# Progress percentage helper
# ==========================================================

def get_progress_percentage(
    telegram_id: int,
    module_id: str,
) -> float:
    """Return module completion percentage."""

    progress = get_module_progress(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    return float(
        progress["percentage"]
    )


# ==========================================================
# Completion helper
# ==========================================================

def is_module_completed(
    telegram_id: int,
    module_id: str,
) -> bool:
    """Return whether the complete module is finished."""

    progress = get_module_progress(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    return bool(
        progress["completed"]
    )


# ==========================================================
# Health check
# ==========================================================

def progress_health_check() -> bool:
    """Check whether the progress layer can access SQLite."""

    try:

        initialize_progress_system()

        with get_connection() as connection:

            connection.execute(
                "SELECT COUNT(*) FROM lesson_progress"
            ).fetchone()

        return True

    except Exception:
        return False
