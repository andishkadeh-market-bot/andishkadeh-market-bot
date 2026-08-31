“”“Service layer for the General Exam module.

Andishkadeh Management & Market

Responsibilities:

* Create exam sessions
* Manage answers
* Calculate scores
* Save statistics
* Update lesson progress
    “””

from future import annotations

from typing import Any

from modules.exam.data import (
GENERAL_EXAM_QUESTIONS,
get_general_exam_questions,
)
from modules.statistics.service import record_quiz_result
from modules.progress.service import (
complete_lesson,
start_lesson,
)

==========================================================

Constants

==========================================================

MODULE_ID = “general_exam”
CHAPTER_ID = “general”
LESSON_ID = “general_quiz”

PASSING_SCORE = 60.0

==========================================================

Question helpers

==========================================================

def get_questions() -> list[dict[str, Any]]:
“”“Return the general exam questions.”””

return get_general_exam_questions()

def get_question_count() -> int:
“”“Return the number of questions in the exam.”””

return len(GENERAL_EXAM_QUESTIONS)

def get_question(
question_index: int,
) -> dict[str, Any]:
“”“Return one question by zero-based index.”””

questions = get_general_exam_questions()
if question_index < 0:
    raise IndexError(
        "question_index cannot be negative."
    )
if question_index >= len(questions):
    raise IndexError(
        "question_index is out of range."
    )
return questions[question_index]

==========================================================

Session creation

==========================================================

def create_exam_session(
telegram_id: int,
) -> dict[str, Any]:
“””
Create a fresh general-exam session.

The session is represented as a plain dictionary so
Telegram handlers can store it in context.user_data.
"""
if telegram_id <= 0:
    raise ValueError(
        "telegram_id must be greater than zero."
    )
questions = get_general_exam_questions()
if not questions:
    raise ValueError(
        "The general exam contains no questions."
    )
start_lesson(
    telegram_id=telegram_id,
    module_id=MODULE_ID,
    chapter_id=CHAPTER_ID,
    lesson_id=LESSON_ID,
)
return {
    "telegram_id": telegram_id,
    "module_id": MODULE_ID,
    "chapter_id": CHAPTER_ID,
    "lesson_id": LESSON_ID,
    "questions": questions,
    "current_index": 0,
    "answers": [],
    "correct_answers": 0,
    "completed": False,
    "score": 0.0,
}

==========================================================

Answer handling

==========================================================

def submit_answer(
session: dict[str, Any],
answer_index: int,
) -> dict[str, Any]:
“””
Register one answer in an exam session.

Returns information about the submitted answer and
whether the exam has finished.
"""
if not isinstance(session, dict):
    raise TypeError(
        "session must be a dictionary."
    )
if session.get("completed"):
    raise ValueError(
        "The exam session is already completed."
    )
questions = session.get("questions")
if not isinstance(questions, list) or not questions:
    raise ValueError(
        "The exam session contains no questions."
    )
current_index = int(
    session.get("current_index", 0)
)
if current_index < 0 or current_index >= len(questions):
    raise IndexError(
        "Current question index is out of range."
    )
if not isinstance(answer_index, int):
    raise TypeError(
        "answer_index must be an integer."
    )
question = questions[current_index]
options = question["options"]
if answer_index < 0 or answer_index >= len(options):
    raise ValueError(
        "answer_index is out of range."
    )
correct_index = int(
    question["correct_index"]
)
is_correct = (
    answer_index == correct_index
)
if is_correct:
    session["correct_answers"] = (
        int(session.get("correct_answers", 0))
        + 1
    )
session["answers"].append(
    {
        "question_index": current_index,
        "answer_index": answer_index,
        "correct_index": correct_index,
        "correct": is_correct,
    }
)
session["current_index"] = (
    current_index + 1
)
finished = (
    session["current_index"]
    >= len(questions)
)
if finished:
    result = finish_exam(session)
    return {
        "finished": True,
        "correct": is_correct,
        "question_index": current_index,
        "correct_index": correct_index,
        "result": result,
    }
return {
    "finished": False,
    "correct": is_correct,
    "question_index": current_index,
    "correct_index": correct_index,
    "next_question_index": session["current_index"],
}

==========================================================

Exam completion

==========================================================

def calculate_exam_score(
correct_answers: int,
total_questions: int,
) -> float:
“”“Calculate the exam score as a percentage.”””

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

def finish_exam(
session: dict[str, Any],
) -> dict[str, Any]:
“””
Finish an exam session.

Saves the result through Statistics and marks the
exam lesson as completed through Progress.
"""
if not isinstance(session, dict):
    raise TypeError(
        "session must be a dictionary."
    )
if session.get("completed"):
    return {
        "score": float(
            session.get("score", 0.0)
        ),
        "correct_answers": int(
            session.get("correct_answers", 0)
        ),
        "total_questions": len(
            session.get("questions", [])
        ),
        "passed": (
            float(
                session.get("score", 0.0)
            )
            >= PASSING_SCORE
        ),
    }
questions = session.get("questions")
if not isinstance(questions, list) or not questions:
    raise ValueError(
        "The exam session contains no questions."
    )
telegram_id = int(
    session["telegram_id"]
)
correct_answers = int(
    session.get("correct_answers", 0)
)
total_questions = len(questions)
score = calculate_exam_score(
    correct_answers=correct_answers,
    total_questions=total_questions,
)
record_quiz_result(
    telegram_id=telegram_id,
    module_id=MODULE_ID,
    chapter_id=CHAPTER_ID,
    lesson_id=LESSON_ID,
    total_questions=total_questions,
    correct_answers=correct_answers,
    score=score,
)
complete_lesson(
    telegram_id=telegram_id,
    module_id=MODULE_ID,
    chapter_id=CHAPTER_ID,
    lesson_id=LESSON_ID,
)
session["completed"] = True
session["score"] = score
return {
    "score": score,
    "correct_answers": correct_answers,
    "wrong_answers": (
        total_questions
        - correct_answers
    ),
    "total_questions": total_questions,
    "passed": score >= PASSING_SCORE,
}

==========================================================

Session helpers

==========================================================

def get_current_question(
session: dict[str, Any],
) -> dict[str, Any] | None:
“”“Return the current question in a session.”””

if not isinstance(session, dict):
    return None
if session.get("completed"):
    return None
questions = session.get("questions")
if not isinstance(questions, list):
    return None
current_index = int(
    session.get("current_index", 0)
)
if current_index < 0 or current_index >= len(questions):
    return None
return questions[current_index]

def cancel_exam(
session: dict[str, Any],
) -> None:
“”“Cancel an unfinished exam session.”””

if not isinstance(session, dict):
    return
session["cancelled"] = True
session["completed"] = False

def is_exam_finished(
session: dict[str, Any],
) -> bool:
“”“Return whether an exam session is finished.”””

if not isinstance(session, dict):
    return False
return bool(
    session.get("completed", False)
)

def is_exam_cancelled(
session: dict[str, Any],
) -> bool:
“”“Return whether an exam session was cancelled.”””

if not isinstance(session, dict):
    return False
return bool(
    session.get("cancelled", False)
)

==========================================================

Health check

==========================================================

def exam_service_health_check() -> bool:
“”“Validate the general exam service.”””

try:
    questions = get_general_exam_questions()
    if not questions:
        return False
    for question in questions:
        options = question.get(
            "options"
        )
        correct_index = question.get(
            "correct_index"
        )
        if not isinstance(options, list):
            return False
        if len(options) != 4:
            return False
        if not isinstance(
            correct_index,
            int,
        ):
            return False
        if not (
            0
            <= correct_index
            < len(options)
        ):
            return False
    return True
except Exception:
    return False
