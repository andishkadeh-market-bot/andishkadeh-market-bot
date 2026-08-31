"""
Service layer for the General Exam module.

Andishkadeh Management & Market

Responsibilities:
- Access the general exam question bank
- Provide exam questions
- Provide question counts
- Validate exam data
- Provide a simple health check
- Keep business logic independent from Telegram handlers
"""

from __future__ import annotations

from typing import Any

from modules.exam.data import (
    GENERAL_EXAM_QUESTIONS,
    data_health_check,
    get_general_exam_question_count,
    get_general_exam_questions,
    validate_question_bank,
)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = "exam"
MODULE_TITLE = "آزمون استخدامی"


# ==========================================================
# Module Information
# ==========================================================

def get_module_id() -> str:
    """Return the General Exam module ID."""
    return MODULE_ID


def get_module_title() -> str:
    """Return the General Exam module title."""
    return MODULE_TITLE


def get_module_info() -> dict[str, str]:
    """Return basic information about the General Exam module."""
    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "title": MODULE_TITLE,
        "description": "بانک سوالات آزمون استخدامی و ارزیابی دانش عمومی",
    }


# ==========================================================
# Questions
# ==========================================================

def get_questions() -> list[dict[str, Any]]:
    """
    Return a safe copy of all general exam questions.
    """
    try:
        questions = get_general_exam_questions()

        if not isinstance(questions, list):
            return []

        return [
            dict(question)
            for question in questions
            if isinstance(question, dict)
        ]

    except Exception:
        return []


def get_exam_questions() -> list[dict[str, Any]]:
    """
    Compatibility alias for handlers.
    """
    return get_questions()


def get_general_exam_questions_service() -> list[dict[str, Any]]:
    """
    Compatibility wrapper for the general exam question bank.
    """
    return get_questions()


# ==========================================================
# Question Access
# ==========================================================

def get_question(
    question_index: int,
) -> dict[str, Any] | None:
    """
    Return one question by zero-based index.
    """
    try:
        index = int(question_index)
    except (TypeError, ValueError):
        return None

    questions = get_questions()

    if index < 0 or index >= len(questions):
        return None

    return dict(questions[index])


def get_question_by_index(
    question_index: int,
) -> dict[str, Any] | None:
    """
    Compatibility alias for question lookup.
    """
    return get_question(question_index)


def get_question_count() -> int:
    """
    Return the number of available exam questions.
    """
    try:
        return int(
            get_general_exam_question_count()
        )
    except Exception:
        return len(
            GENERAL_EXAM_QUESTIONS
        )


def get_exam_question_count() -> int:
    """
    Compatibility alias for question count.
    """
    return get_question_count()


# ==========================================================
# Question Options
# ==========================================================

def get_question_options(
    question_index: int,
) -> list[str]:
    """
    Return the answer options for one question.
    """
    question = get_question(
        question_index
    )

    if question is None:
        return []

    options = question.get(
        "options",
        [],
    )

    if not isinstance(options, list):
        return []

    return [
        str(option)
        for option in options
    ]


def get_correct_index(
    question_index: int,
) -> int | None:
    """
    Return the correct option index for one question.
    """
    question = get_question(
        question_index
    )

    if question is None:
        return None

    value = question.get(
        "correct_index"
    )

    if isinstance(value, int):
        return value

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


# ==========================================================
# Search
# ==========================================================

def search_questions(
    keyword: str,
) -> list[dict[str, Any]]:
    """
    Search questions by question text or option text.
    """
    if keyword is None:
        return []

    normalized = str(
        keyword
    ).strip().casefold()

    if not normalized:
        return []

    results: list[dict[str, Any]] = []

    for index, question in enumerate(
        get_questions()
    ):
        question_text = str(
            question.get(
                "question",
                "",
            )
        )

        options = question.get(
            "options",
            [],
        )

        option_text = ""

        if isinstance(options, list):
            option_text = "\n".join(
                str(option)
                for option in options
            )

        searchable = (
            f"{question_text}\n"
            f"{option_text}"
        ).casefold()

        if normalized in searchable:
            result = dict(question)
            result["index"] = index
            results.append(result)

    return results


# ==========================================================
# Exam Statistics
# ==========================================================

def get_exam_statistics() -> dict[str, int]:
    """
    Return basic statistics about the exam question bank.
    """
    questions = get_questions()

    return {
        "modules": 1,
        "questions": len(questions),
        "question_count": len(questions),
    }


def get_module_statistics() -> dict[str, Any]:
    """
    Return complete module statistics.
    """
    return {
        "module_id": get_module_id(),
        "title": get_module_title(),
        **get_exam_statistics(),
    }


# ==========================================================
# Validation
# ==========================================================

def validate_exam_data() -> dict[str, Any]:
    """
    Validate the General Exam question bank.

    Returns a report instead of raising exceptions.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        valid = bool(
            validate_question_bank()
        )
    except Exception as exc:
        valid = False
        errors.append(
            f"Question bank validation failed: {exc}"
        )

    questions = get_questions()

    if not questions:
        errors.append(
            "No General Exam questions found."
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):
        if not isinstance(
            question,
            dict,
        ):
            errors.append(
                f"Question #{index} is not a dictionary."
            )
            continue

        question_text = question.get(
            "question"
        )

        if not question_text:
            errors.append(
                f"Question #{index} has no question text."
            )

        options = question.get(
            "options"
        )

        if not isinstance(
            options,
            list,
        ):
            errors.append(
                f"Question #{index} has invalid options."
            )
        elif len(options) != 4:
            errors.append(
                (
                    f"Question #{index} must have "
                    f"exactly 4 options."
                )
            )

        correct_index = question.get(
            "correct_index"
        )

        if not isinstance(
            correct_index,
            int,
        ):
            errors.append(
                (
                    f"Question #{index} has "
                    f"an invalid correct_index."
                )
            )
        elif not isinstance(
            options,
            list,
        ) or not (
            0 <= correct_index < len(options)
        ):
            errors.append(
                (
                    f"Question #{index} has a "
                    f"correct_index outside its options."
                )
            )

    if len(questions) < 10:
        warnings.append(
            "The General Exam question bank contains fewer than 10 questions."
        )

    return {
        "valid": valid and not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": get_exam_statistics(),
    }


# ==========================================================
# Health Check
# ==========================================================

def exam_service_health_check() -> bool:
    """
    Check whether the General Exam service is usable.
    """
    try:
        module_info = get_module_info()

        if not module_info.get("id"):
            return False

        if not module_info.get("title"):
            return False

        if not data_health_check():
            return False

        report = validate_exam_data()

        return bool(
            report.get("valid")
        )

    except Exception:
        return False


def service_health_check() -> bool:
    """
    Generic service health-check alias.
    """
    return exam_service_health_check()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "get_module_id",
    "get_module_title",
    "get_module_info",
    "get_questions",
    "get_exam_questions",
    "get_general_exam_questions_service",
    "get_question",
    "get_question_by_index",
    "get_question_count",
    "get_exam_question_count",
    "get_question_options",
    "get_correct_index",
    "search_questions",
    "get_exam_statistics",
    "get_module_statistics",
    "validate_exam_data",
    "exam_service_health_check",
    "service_health_check",
]


# ==========================================================
# Local Test
# ==========================================================

if __name__ == "__main__":
    print(
        "General Exam Service Health:",
        exam_service_health_check(),
    )

    print(
        "Module:",
        get_module_info(),
    )

    print(
        "Statistics:",
        get_exam_statistics(),
    )
