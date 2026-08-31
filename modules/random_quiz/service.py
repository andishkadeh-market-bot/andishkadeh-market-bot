"""
Service layer for Random Quiz module.

Andishkadeh Management & Market

Responsibilities:
- Build random quiz sessions
- Select random questions
- Manage answers
- Calculate results
- Connect with Quiz Engine
- Connect with Statistics
- Connect with Progress
- Keep user sessions isolated
"""

from __future__ import annotations

import random
from typing import Any

from core.quiz_engine import (
    calculate_score,
)

from core.statistics import (
    record_quiz_result,
)

from core.progress import (
    mark_lesson_completed,
)


# ==========================================================
# Constants
# ==========================================================

RANDOM_QUIZ_MODULE_ID = "random_quiz"

DEFAULT_QUESTION_COUNT = 10

MIN_QUESTION_COUNT = 1

MAX_QUESTION_COUNT = 20


# ==========================================================
# Question validation
# ==========================================================

def _validate_question(
    question: dict[str, Any],
) -> bool:
    """
    Validate the minimum structure of a question.
    """

    if not isinstance(question, dict):
        return False

    if not question.get("id"):
        return False

    if not question.get("question"):
        return False

    options = question.get("options")

    if not isinstance(options, list):
        return False

    if len(options) < 2:
        return False

    correct_answer = question.get(
        "correct_answer"
    )

    if correct_answer is None:
        return False

    return True


# ==========================================================
# Question normalization
# ==========================================================

def _normalize_question(
    question: dict[str, Any],
) -> dict[str, Any]:
    """
    Return a safe normalized question object.
    """

    return {
        "id": question["id"],
        "question": question["question"],
        "options": list(
            question.get("options", [])
        ),
        "correct_answer": question[
            "correct_answer"
        ],
        "module_id": question.get(
            "module_id",
            RANDOM_QUIZ_MODULE_ID,
        ),
        "chapter_id": question.get(
            "chapter_id",
            "random",
        ),
        "lesson_id": question.get(
            "lesson_id",
            "random",
        ),
    }


# ==========================================================
# Question selection
# ==========================================================

def select_random_questions(
    questions: list[dict[str, Any]],
    count: int = DEFAULT_QUESTION_COUNT,
) -> list[dict[str, Any]]:
    """
    Select random questions.

    Questions are validated before selection.
    """

    if not isinstance(questions, list):
        raise TypeError(
            "questions must be a list."
        )

    if count < MIN_QUESTION_COUNT:
        raise ValueError(
            "count must be at least 1."
        )

    if count > MAX_QUESTION_COUNT:
        raise ValueError(
            "count cannot exceed 20."
        )

    valid_questions = [
        _normalize_question(question)
        for question in questions
        if _validate_question(question)
    ]

    if not valid_questions:
        raise ValueError(
            "No valid questions are available."
        )

    selected_count = min(
        count,
        len(valid_questions),
    )

    return random.sample(
        valid_questions,
        selected_count,
    )


# ==========================================================
# Session creation
# ==========================================================

def start_random_quiz(
    telegram_id: int,
    questions: list[dict[str, Any]],
    count: int = DEFAULT_QUESTION_COUNT,
) -> dict[str, Any]:
    """
    Create a random quiz session.

    The returned dictionary is intended to be stored
    inside Telegram context.user_data.
    """

    if telegram_id <= 0:
        raise ValueError(
            "telegram_id must be greater than zero."
        )

    selected_questions = (
        select_random_questions(
            questions=questions,
            count=count,
        )
    )

    return {
        "telegram_id": telegram_id,
        "module_id": RANDOM_QUIZ_MODULE_ID,
        "chapter_id": "random",
        "lesson_id": "random",
        "questions": selected_questions,
        "current_index": 0,
        "answers": [],
        "correct_answers": 0,
        "completed": False,
        "cancelled": False,
    }


# ==========================================================
# Current question
# ==========================================================

def get_random_question(
    session: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Return the current question.
    """

    if not isinstance(session, dict):
        raise TypeError(
            "session must be a dictionary."
        )

    if session.get("completed"):
        return None

    if session.get("cancelled"):
        return None

    questions = session.get(
        "questions",
        [],
    )

    current_index = int(
        session.get(
            "current_index",
            0,
        )
    )

    if current_index >= len(questions):
        return None

    return questions[current_index]


# ==========================================================
# Submit answer
# ==========================================================

def submit_random_answer(
    session: dict[str, Any],
    answer: Any,
) -> dict[str, Any]:
    """
    Submit an answer for the current question.

    Returns:
        A result dictionary containing:
        - correct
        - correct_answer
        - current_index
        - completed
        - score
    """

    if not isinstance(session, dict):
        raise TypeError(
            "session must be a dictionary."
        )

    if session.get("completed"):
        raise ValueError(
            "Quiz has already been completed."
        )

    if session.get("cancelled"):
        raise ValueError(
            "Quiz has been cancelled."
        )

    question = get_random_question(
        session
    )

    if question is None:
        raise ValueError(
            "There is no active question."
        )

    correct_answer = question[
        "correct_answer"
    ]

    is_correct = (
        answer == correct_answer
    )

    session.setdefault(
        "answers",
        [],
    ).append(
        {
            "question_id": question["id"],
            "answer": answer,
            "correct_answer": correct_answer,
            "correct": is_correct,
        }
    )

    if is_correct:
        session["correct_answers"] = (
            int(
                session.get(
                    "correct_answers",
                    0,
                )
            )
            + 1
        )

    session["current_index"] = (
        int(
            session.get(
                "current_index",
                0,
            )
        )
        + 1
    )

    total_questions = len(
        session.get(
            "questions",
            [],
        )
    )

    completed = (
        session["current_index"]
        >= total_questions
    )

    session["completed"] = completed

    score = calculate_score(
        int(
            session.get(
                "correct_answers",
                0,
            )
        ),
        total_questions,
    )

    return {
        "correct": is_correct,
        "correct_answer": correct_answer,
        "current_index": session[
            "current_index"
        ],
        "completed": completed,
        "score": score,
        "correct_answers": int(
            session.get(
                "correct_answers",
                0,
            )
        ),
        "total_questions": total_questions,
    }


# ==========================================================
# Complete quiz
# ==========================================================

def complete_random_quiz(
    session: dict[str, Any],
) -> dict[str, Any]:
    """
    Finalize a completed random quiz.

    Statistics and Progress are updated here.
    """

    if not isinstance(session, dict):
        raise TypeError(
            "session must be a dictionary."
        )

    if session.get("cancelled"):
        raise ValueError(
            "Quiz has been cancelled."
        )

    total_questions = len(
        session.get(
            "questions",
            [],
        )
    )

    correct_answers = int(
        session.get(
            "correct_answers",
            0,
        )
    )

    if total_questions <= 0:
        raise ValueError(
            "Quiz contains no questions."
        )

    if not session.get("completed"):
        raise ValueError(
            "Quiz is not completed yet."
        )

    score = calculate_score(
        correct_answers,
        total_questions,
    )

    telegram_id = int(
        session["telegram_id"]
    )

    module_id = session.get(
        "module_id",
        RANDOM_QUIZ_MODULE_ID,
    )

    chapter_id = session.get(
        "chapter_id",
        "random",
    )

    lesson_id = session.get(
        "lesson_id",
        "random",
    )

    attempt_id = record_quiz_result(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
    )

    try:
        mark_lesson_completed(
            telegram_id=telegram_id,
            module_id=module_id,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )
    except Exception:
        # Statistics must remain saved even if
        # Progress registration fails.
        pass

    session["completed"] = True
    session["score"] = score
    session["attempt_id"] = attempt_id

    return {
        "telegram_id": telegram_id,
        "module_id": module_id,
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": (
            total_questions
            - correct_answers
        ),
        "score": score,
        "attempt_id": attempt_id,
    }


# ==========================================================
# Cancel quiz
# ==========================================================

def cancel_random_quiz(
    session: dict[str, Any],
) -> dict[str, Any]:
    """
    Cancel an active random quiz.

    Cancellation does not save a quiz result.
    """

    if not isinstance(session, dict):
        raise TypeError(
            "session must be a dictionary."
        )

    if session.get("completed"):
        raise ValueError(
            "Completed quiz cannot be cancelled."
        )

    session["cancelled"] = True

    return {
        "telegram_id": session.get(
            "telegram_id"
        ),
        "cancelled": True,
        "completed": False,
    }


# ==========================================================
# Session health
# ==========================================================

def random_quiz_service_health_check() -> bool:
    """
    Verify that the Random Quiz service is operational.
    """

    try:
        score = calculate_score(
            correct_answers=5,
            total_questions=10,
        )

        return score == 50.0

    except Exception:
        return False
