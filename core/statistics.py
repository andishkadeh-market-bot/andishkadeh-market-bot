"""
Statistics layer for Andishkadeh Management & Market.

Provides statistics for:
- Quiz attempts
- Quiz scores
- User performance
- Lesson performance
- Module performance
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
    """Initialize the database used by the statistics system."""

    init_database()


# ==========================================================
# Save quiz result
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
    Save a quiz result.

    If score is not provided, it is calculated automatically.
    """

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
        score = round(
            correct_answers
            / total_questions
            * 100,
            2,
        )

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
# User statistics
# ==========================================================

def get_user_statistics(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any]:
    """
    Return overall quiz statistics for a user.
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
        "attempts": int(row["attempts"]),
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


# ==========================================================
# Lesson statistics
# ==========================================================

def get_lesson_statistics(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any]:
    """
    Return quiz statistics for one lesson.
    """

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
                ) AS best_score
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
        "attempts": int(row["attempts"]),
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
    }


# ==========================================================
# Module statistics
# ==========================================================

def get_module_statistics(
    telegram_id: int,
    module_id: str,
) -> dict[str, Any]:
    """
    Return detailed quiz statistics for a module.
    """

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
                chapter_id=lesson["chapter_id"],
                lesson_id=lesson["lesson_id"],
            )
        )

    statistics["lessons"] = lesson_statistics

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
    """
    Return quiz attempts using optional filters.
    """

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
    """Return the highest-scoring quiz attempt."""

    attempts = get_attempts(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    if not attempts:
        return None

    return max(
        attempts,
        key=lambda attempt: (
            float(attempt["score"]),
            int(attempt["correct_answers"]),
        ),
    )


# ==========================================================
# Score helpers
# ==========================================================

def calculate_score(
    correct_answers: int,
    total_questions: int,
) -> float:
    """Calculate a quiz score as a percentage."""

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
# Health check
# ==========================================================

def statistics_health_check() -> bool:
    """Check whether the statistics layer is operational."""

    try:

        initialize_statistics_system()

        with get_connection() as connection:

            connection.execute(
                "SELECT COUNT(*) FROM quiz_attempts"
            ).fetchone()

        return True

    except Exception:
        return False
