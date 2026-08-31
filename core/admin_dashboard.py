"""
Admin Dashboard data layer for Andishkadeh Management & Market.
This module provides read-only administrative statistics from SQLite.
Responsibilities:
- List registered users
- Read detailed user information
- Read user progress
- Read user quiz statistics
- Read latest activity
- Read module statistics
- Provide dashboard summaries
This layer does NOT handle Telegram UI.
Telegram handlers should use this module as their data source.
"""
from __future__ import annotations
from typing import Any
from core.database import (
    get_connection,
    init_database,
)
# ==========================================================
# Initialization
# ==========================================================
def initialize_admin_dashboard() -> None:
    """Initialize the database required by the admin dashboard."""
    init_database()
# ==========================================================
# Users
# ==========================================================
def get_total_users() -> int:
    """Return total number of registered users."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        ).fetchone()
    return int(row[0])
def get_users(
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """
    Return registered users.
    Users are ordered by most recently updated.
    """
    if limit <= 0:
        raise ValueError(
            "limit must be greater than zero."
        )
    if offset < 0:
        raise ValueError(
            "offset cannot be negative."
        )
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                telegram_id,
                username,
                first_name,
                last_name,
                created_at,
                updated_at
            FROM users
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                limit,
                offset,
            ),
        ).fetchall()
    return [
        dict(row)
        for row in rows
    ]
def get_user(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return basic information for one user."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                id,
                telegram_id,
                username,
                first_name,
                last_name,
                created_at,
                updated_at
            FROM users
            WHERE telegram_id = ?
            """,
            (
                telegram_id,
            ),
        ).fetchone()
    if row is None:
        return None
    return dict(row)
# ==========================================================
# User progress
# ==========================================================
def get_user_progress_summary(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any]:
    """
    Return lesson progress summary for a user.
    """
    query = """
        SELECT
            COUNT(*) AS total_records,
            COALESCE(
                SUM(started),
                0
            ) AS started_lessons,
            COALESCE(
                SUM(completed),
                0
            ) AS completed_lessons
        FROM lesson_progress
        WHERE telegram_id = ?
    """
    parameters: list[Any] = [
        telegram_id
    ]
    if module_id is not None:
        query += """
            AND module_id = ?
        """
        parameters.append(module_id)
    with get_connection() as connection:
        row = connection.execute(
            query,
            parameters,
        ).fetchone()
    started = int(
        row["started_lessons"]
    )
    completed = int(
        row["completed_lessons"]
    )
    return {
        "telegram_id": telegram_id,
        "module_id": module_id,
        "records": int(
            row["total_records"]
        ),
        "started_lessons": started,
        "completed_lessons": completed,
    }
def get_user_progress_details(
    telegram_id: int,
    module_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return detailed lesson progress for a user."""
    query = """
        SELECT
            id,
            telegram_id,
            module_id,
            chapter_id,
            lesson_id,
            started,
            completed,
            started_at,
            completed_at,
            updated_at
        FROM lesson_progress
        WHERE telegram_id = ?
    """
    parameters: list[Any] = [
        telegram_id
    ]
    if module_id is not None:
        query += """
            AND module_id = ?
        """
        parameters.append(module_id)
    query += """
        ORDER BY
            updated_at DESC,
            id DESC
    """
    with get_connection() as connection:
        rows = connection.execute(
            query,
            parameters,
        ).fetchall()
    return [
        dict(row)
        for row in rows
    ]
# ==========================================================
# Quiz statistics
# ==========================================================
def get_user_quiz_summary(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any]:
    """
    Return quiz performance summary for a user.
    """
    query = """
        SELECT
            COUNT(*) AS attempts,
            COALESCE(
                SUM(total_questions),
                0
            ) AS total_questions,
            COALESCE(
                SUM(correct_answers),
                0
            ) AS correct_answers,
            COALESCE(
                AVG(score),
                0
            ) AS average_score,
            COALESCE(
                MAX(score),
                0
            ) AS best_score,
            COALESCE(
                MIN(score),
                0
            ) AS lowest_score
        FROM quiz_attempts
        WHERE telegram_id = ?
    """
    parameters: list[Any] = [
        telegram_id
    ]
    if module_id is not None:
        query += """
            AND module_id = ?
        """
        parameters.append(module_id)
    with get_connection() as connection:
        row = connection.execute(
            query,
            parameters,
        ).fetchone()
    attempts = int(
        row["attempts"]
    )
    total_questions = int(
        row["total_questions"]
    )
    correct_answers = int(
        row["correct_answers"]
    )
    accuracy = (
        round(
            correct_answers
            / total_questions
            * 100,
            2,
        )
        if total_questions > 0
        else 0.0
    )
    return {
        "telegram_id": telegram_id,
        "module_id": module_id,
        "attempts": attempts,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": (
            total_questions
            - correct_answers
        ),
        "accuracy": accuracy,
        "average_score": round(
            float(row["average_score"]),
            2,
        ),
        "best_score": round(
            float(row["best_score"]),
            2,
        ),
        "lowest_score": round(
            float(row["lowest_score"]),
            2,
        ),
    }
def get_user_quiz_attempts(
    telegram_id: int,
    module_id: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Return recent quiz attempts for a user."""
    if limit <= 0:
        raise ValueError(
            "limit must be greater than zero."
        )
    query = """
        SELECT
            id,
            telegram_id,
            module_id,
            chapter_id,
            lesson_id,
            total_questions,
            correct_answers,
            score,
            started_at,
            completed_at
        FROM quiz_attempts
        WHERE telegram_id = ?
    """
    parameters: list[Any] = [
        telegram_id
    ]
    if module_id is not None:
        query += """
            AND module_id = ?
        """
        parameters.append(module_id)
    query += """
        ORDER BY id DESC
        LIMIT ?
    """
    parameters.append(limit)
    with get_connection() as connection:
        rows = connection.execute(
            query,
            parameters,
        ).fetchall()
    return [
        dict(row)
        for row in rows
    ]
# ==========================================================
# Latest activity
# ==========================================================
def get_latest_completed_lesson(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return the latest completed lesson."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                id,
                module_id,
                chapter_id,
                lesson_id,
                completed_at,
                updated_at
            FROM lesson_progress
            WHERE telegram_id = ?
              AND completed = 1
            ORDER BY
                completed_at DESC,
                id DESC
            LIMIT 1
            """,
            (
                telegram_id,
            ),
        ).fetchone()
    if row is None:
        return None
    return dict(row)
def get_latest_quiz_attempt(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return the latest quiz attempt."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                id,
                module_id,
                chapter_id,
                lesson_id,
                total_questions,
                correct_answers,
                score,
                started_at,
                completed_at
            FROM quiz_attempts
            WHERE telegram_id = ?
            ORDER BY
                id DESC
            LIMIT 1
            """,
            (
                telegram_id,
            ),
        ).fetchone()
    if row is None:
        return None
    return dict(row)
# ==========================================================
# Complete user dashboard
# ==========================================================
def get_user_dashboard(
    telegram_id: int,
) -> dict[str, Any] | None:
    """
    Return complete administrative information for one user.
    Combines:
    - Basic profile
    - Progress
    - Quiz statistics
    - Latest completed lesson
    - Latest quiz attempt
    """
    user = get_user(
        telegram_id
    )
    if user is None:
        return None
    progress = get_user_progress_summary(
        telegram_id
    )
    statistics = get_user_quiz_summary(
        telegram_id
    )
    latest_lesson = get_latest_completed_lesson(
        telegram_id
    )
    latest_quiz = get_latest_quiz_attempt(
        telegram_id
    )
    return {
        "user": user,
        "progress": progress,
        "statistics": statistics,
        "latest_completed_lesson": latest_lesson,
        "latest_quiz_attempt": latest_quiz,
    }
# ==========================================================
# Global dashboard
# ==========================================================
def get_dashboard_summary() -> dict[str, Any]:
    """
    Return global statistics for the admin dashboard.
    """
    with get_connection() as connection:
        users = connection.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        ).fetchone()[0]
        started_lessons = connection.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress
            WHERE started = 1
            """
        ).fetchone()[0]
        completed_lessons = connection.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress
            WHERE completed = 1
            """
        ).fetchone()[0]
        quiz_attempts = connection.execute(
            """
            SELECT COUNT(*)
            FROM quiz_attempts
            """
        ).fetchone()[0]
        total_questions = connection.execute(
            """
            SELECT COALESCE(
                SUM(total_questions),
                0
            )
            FROM quiz_attempts
            """
        ).fetchone()[0]
        correct_answers = connection.execute(
            """
            SELECT COALESCE(
                SUM(correct_answers),
                0
            )
            FROM quiz_attempts
            """
        ).fetchone()[0]
        average_score = connection.execute(
            """
            SELECT COALESCE(
                AVG(score),
                0
            )
            FROM quiz_attempts
            """
        ).fetchone()[0]
        best_score = connection.execute(
            """
            SELECT COALESCE(
                MAX(score),
                0
            )
            FROM quiz_attempts
            """
        ).fetchone()[0]
    total_questions = int(
        total_questions
    )
    correct_answers = int(
        correct_answers
    )
    accuracy = (
        round(
            correct_answers
            / total_questions
            * 100,
            2,
        )
        if total_questions > 0
        else 0.0
    )
    return {
        "users": int(users),
        "started_lessons": int(
            started_lessons
        ),
        "completed_lessons": int(
            completed_lessons
        ),
        "quiz_attempts": int(
            quiz_attempts
        ),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": (
            total_questions
            - correct_answers
        ),
        "accuracy": accuracy,
        "average_score": round(
            float(average_score),
            2,
        ),
        "best_score": round(
            float(best_score),
            2,
        ),
    }
# ==========================================================
# Module dashboard
# ==========================================================
def get_module_dashboard(
    module_id: str,
) -> dict[str, Any]:
    """
    Return global statistics for one module.
    """
    with get_connection() as connection:
        lesson_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM lessons
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]
        chapter_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM chapters
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]
        attempts = connection.execute(
            """
            SELECT COUNT(*)
            FROM quiz_attempts
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]
        total_questions = connection.execute(
            """
            SELECT COALESCE(
                SUM(total_questions),
                0
            )
            FROM quiz_attempts
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]
        correct_answers = connection.execute(
            """
            SELECT COALESCE(
                SUM(correct_answers),
                0
            )
            FROM quiz_attempts
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]
        average_score = connection.execute(
            """
            SELECT COALESCE(
                AVG(score),
                0
            )
            FROM quiz_attempts
            WHERE module_id = ?
            """,
            (
                module_id,
            ),
        ).fetchone()[0]
    total_questions = int(
        total_questions
    )
    correct_answers = int(
        correct_answers
    )
    accuracy = (
        round(
            correct_answers
            / total_questions
            * 100,
            2,
        )
        if total_questions > 0
        else 0.0
    )
    return {
        "module_id": module_id,
        "chapters": int(
            chapter_count
        ),
        "lessons": int(
            lesson_count
        ),
        "quiz_attempts": int(
            attempts
        ),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": (
            total_questions
            - correct_answers
        ),
        "accuracy": accuracy,
        "average_score": round(
            float(average_score),
            2,
        ),
    }
# ==========================================================
# Recent users
# ==========================================================
def get_recent_users(
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return recently updated users."""
    return get_users(
        limit=limit,
        offset=0,
    )
# ==========================================================
# Health check
# ==========================================================
def admin_dashboard_health_check() -> bool:
    """Check whether the admin dashboard can access SQLite."""
    try:
        initialize_admin_dashboard()
        with get_connection() as connection:
            connection.execute(
                "SELECT 1"
            ).fetchone()
        return True
    except Exception:
        return False
# ==========================================================
# Manual test
# ==========================================================
if __name__ == "__main__":
    initialize_admin_dashboard()
    print(
        "Admin Dashboard initialized successfully."
    )
    print(
        get_dashboard_summary()
    )
