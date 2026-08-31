"""
Statistics layer for Andishkadeh Management & Market.
Responsibilities:
- Record quiz results
- Record quiz attempts
- User statistics
- Lesson statistics
- Module statistics
- Attempt history
- Score calculation
- Compatibility with all modules
This layer is independent from Telegram handlers.
"""
from __future__ import annotations
from typing import Any
from core.database import (
    get_connection,
    init_database,
    save_quiz_attempt,
    upsert_user,
)
# ==========================================================
# Initialization
# ==========================================================
def initialize_statistics_system() -> None:
    """Initialize the database used by Statistics."""
    init_database()
# ==========================================================
# Score
# ==========================================================
def calculate_score(
    correct_answers: int,
    total_questions: int,
) -> float:
    """Calculate quiz score as a percentage."""
    if total_questions <= 0:
        raise ValueError(
            "total_questions must be greater than zero."
        )
    if correct_answers < 0:
        raise ValueError(
            "correct_answers cannot be negative."
        )
    if correct_answers > total_questions:
        raise ValueError(
            "correct_answers cannot exceed total_questions."
        )
    return round(
        correct_answers
        / total_questions
        * 100,
        2,
    )
# ==========================================================
# Record quiz result
# ==========================================================
def record_quiz_result(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """
    Save a completed quiz result.
    This is the primary Statistics API.
    """
    if telegram_id <= 0:
        raise ValueError(
            "telegram_id must be positive."
        )
    if not module_id:
        raise ValueError(
            "module_id cannot be empty."
        )
    if not chapter_id:
        raise ValueError(
            "chapter_id cannot be empty."
        )
    if not lesson_id:
        raise ValueError(
            "lesson_id cannot be empty."
        )
    if total_questions <= 0:
        raise ValueError(
            "total_questions must be greater than zero."
        )
    if correct_answers < 0:
        raise ValueError(
            "correct_answers cannot be negative."
        )
    if correct_answers > total_questions:
        raise ValueError(
            "correct_answers cannot exceed total_questions."
        )
    if score is None:
        score = calculate_score(
            correct_answers,
            total_questions,
        )
    score = float(score)
    if score < 0 or score > 100:
        raise ValueError(
            "score must be between 0 and 100."
        )
    upsert_user(
        telegram_id=telegram_id,
    )
    return save_quiz_attempt(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
    )
# ==========================================================
# Compatibility API
# ==========================================================
def record_quiz_attempt(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
    **kwargs: Any,
) -> int:
    """
    Compatibility wrapper for modules that use
    record_quiz_attempt instead of record_quiz_result.
    Both APIs write to the same quiz_attempts table.
    """
    # ------------------------------------------------------
    # Support alternate argument names
    # ------------------------------------------------------
    if "total" in kwargs:
        total_questions = kwargs["total"]
    if "correct" in kwargs:
        correct_answers = kwargs["correct"]
    if "percentage" in kwargs:
        score = kwargs["percentage"]
    return record_quiz_result(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=int(
            total_questions
        ),
        correct_answers=int(
            correct_answers
        ),
        score=(
            float(score)
            if score is not None
            else None
        ),
    )
# ==========================================================
# User statistics
# ==========================================================
def get_user_statistics(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any]:
    """
    Return overall quiz statistics for a user.
    If module_id is supplied, statistics are limited
    to that module.
    """
    with get_connection() as connection:
        if module_id is None:
            row = connection.execute(
                """
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
                """,
                (
                    telegram_id,
                ),
            ).fetchone()
        else:
            row = connection.execute(
                """
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
                  AND module_id = ?
                """,
                (
                    telegram_id,
                    module_id,
                ),
            ).fetchone()
    total_questions = int(
        row["total_questions"]
    )
    correct_answers = int(
        row["correct_answers"]
    )
    wrong_answers = (
        total_questions
        - correct_answers
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
        "attempts": int(
            row["attempts"]
        ),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "accuracy": accuracy,
        "average_score": round(
            float(
                row["average_score"]
            ),
            2,
        ),
        "best_score": round(
            float(
                row["best_score"]
            ),
            2,
        ),
        "lowest_score": round(
            float(
                row["lowest_score"]
            ),
            2,
        ),
    }
# ==========================================================
# Lesson statistics
# ==========================================================
def get_lesson_statistics(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any]:
    """Return statistics for one lesson."""
    with get_connection() as connection:
        row = connection.execute(
            """
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
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "attempts": int(
            row["attempts"]
        ),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": (
            total_questions
            - correct_answers
        ),
        "accuracy": accuracy,
        "average_score": round(
            float(
                row["average_score"]
            ),
            2,
        ),
        "best_score": round(
            float(
                row["best_score"]
            ),
            2,
        ),
        "lowest_score": round(
            float(
                row["lowest_score"]
            ),
            2,
        ),
    }
# ==========================================================
# Module statistics
# ==========================================================
def get_module_statistics(
    telegram_id: int,
    module_id: str,
) -> dict[str, Any]:
    """Return detailed statistics for a module."""
    statistics = get_user_statistics(
        telegram_id=telegram_id,
        module_id=module_id,
    )
    with get_connection() as connection:
        lessons = connection.execute(
            """
            SELECT DISTINCT
                chapter_id,
                lesson_id
            FROM quiz_attempts
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
    lesson_statistics = []
    for lesson in lessons:
        lesson_statistics.append(
            get_lesson_statistics(
                telegram_id=telegram_id,
                module_id=module_id,
                chapter_id=lesson[
                    "chapter_id"
                ],
                lesson_id=lesson[
                    "lesson_id"
                ],
            )
        )
    statistics["lessons"] = (
        lesson_statistics
    )
    return statistics
# ==========================================================
# Attempts
# ==========================================================
def get_attempts(
    telegram_id: int,
    module_id: str | None = None,
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return quiz attempts using optional filters."""
    query = """
        SELECT *
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
        parameters.append(
            module_id
        )
    if chapter_id is not None:
        query += """
            AND chapter_id = ?
        """
        parameters.append(
            chapter_id
        )
    if lesson_id is not None:
        query += """
            AND lesson_id = ?
        """
        parameters.append(
            lesson_id
        )
    query += """
        ORDER BY id DESC
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
# Latest attempt
# ==========================================================
def get_latest_attempt(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any] | None:
    """Return the latest quiz attempt."""
    attempts = get_attempts(
        telegram_id=telegram_id,
        module_id=module_id,
    )
    if not attempts:
        return None
    return attempts[0]
# ==========================================================
# Best attempt
# ==========================================================
def get_best_attempt(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any] | None:
    """Return the highest-scoring attempt."""
    attempts = get_attempts(
        telegram_id=telegram_id,
        module_id=module_id,
    )
    if not attempts:
        return None
    return max(
        attempts,
        key=lambda attempt: (
            float(
                attempt["score"]
            ),
            int(
                attempt[
                    "correct_answers"
                ]
            ),
        ),
    )
# ==========================================================
# Attempts by lesson
# ==========================================================
def get_lesson_attempts(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return all attempts for one lesson."""
    return get_attempts(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )
# ==========================================================
# Recent attempts
# ==========================================================
def get_recent_attempts(
    telegram_id: int,
    limit: int = 10,
    module_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return recent attempts."""
    if limit <= 0:
        return []
    attempts = get_attempts(
        telegram_id=telegram_id,
        module_id=module_id,
    )
    return attempts[
        :limit
    ]
# ==========================================================
# Health check
# ==========================================================
def statistics_health_check() -> bool:
    """
    Verify that the Statistics layer can access
    the quiz_attempts table.
    """
    try:
        initialize_statistics_system()
        with get_connection() as connection:
            connection.execute(
                """
                SELECT COUNT(*)
                FROM quiz_attempts
                """
            ).fetchone()
        return True
    except Exception:
        return False
# ==========================================================
# Public exports
# ==========================================================
__all__ = [
    "initialize_statistics_system",
    "calculate_score",
    "record_quiz_result",
    "record_quiz_attempt",
    "get_user_statistics",
    "get_lesson_statistics",
    "get_module_statistics",
    "get_attempts",
    "get_latest_attempt",
    "get_best_attempt",
    "get_lesson_attempts",
    "get_recent_attempts",
    "statistics_health_check",
]
