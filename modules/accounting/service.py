"""
Accounting Service
Andishkadeh Management & Market

Professional service layer for the Accounting module.

Responsibilities:
- Curriculum access
- Chapter and lesson navigation
- Lesson content retrieval
- Quiz retrieval
- Comprehensive quiz aggregation
- Statistics
- Data normalization
- Backward compatibility
- Safe handling of incomplete data

Data source:
    modules.accounting.data
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any

from modules.accounting import data


logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = "accounting"
MODULE_TITLE = "🧾 حسابداری تخصصی"

DEFAULT_DESCRIPTION = (
    "مسیر جامع و حرفه‌ای حسابداری از مبانی و چرخه حسابداری "
    "تا صورت‌های مالی، حسابداری شرکت‌ها، بهای تمام‌شده، "
    "حسابداری مدیریت، مالیاتی، حسابرسی، استانداردها و تحلیل مالی."
)


# ==========================================================
# Generic Data Helpers
# ==========================================================

def _as_list(value: Any) -> list[Any]:
    """Return a safe list representation."""
    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return []


def _as_dict(value: Any) -> dict[str, Any]:
    """Return a safe dictionary representation."""
    if isinstance(value, dict):
        return value

    return {}


def _text(value: Any, default: str = "") -> str:
    """Convert a value safely to text."""
    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


def _item_id(item: dict[str, Any]) -> str:
    """
    Extract an item's identifier.

    Supports multiple historical naming conventions.
    """

    return _text(
        item.get("id")
        or item.get("chapter_id")
        or item.get("lesson_id")
        or item.get("code")
    )


# ==========================================================
# Raw Curriculum Access
# ==========================================================

def _get_raw_chapters() -> list[dict[str, Any]]:
    """
    Locate accounting chapters from the data module.

    Supports common data variable names so the service
    remains compatible with different data.py versions.
    """

    possible_names = (
        "ACCOUNTING_CHAPTERS",
        "CHAPTERS",
        "accounting_chapters",
        "chapters",
        "CURRICULUM",
        "curriculum",
    )

    for name in possible_names:
        value = getattr(data, name, None)

        if isinstance(value, list):
            return [
                item
                for item in value
                if isinstance(item, dict)
            ]

        if isinstance(value, dict):
            result: list[dict[str, Any]] = []

            for key, item in value.items():

                if isinstance(item, dict):
                    normalized = dict(item)

                    normalized.setdefault(
                        "id",
                        str(key),
                    )

                    result.append(
                        normalized
                    )

            if result:
                return result

    return []


def _get_raw_quiz() -> list[dict[str, Any]]:
    """
    Locate a global accounting quiz collection.
    """

    possible_names = (
        "ACCOUNTING_QUIZ",
        "QUIZ",
        "QUIZ_QUESTIONS",
        "ACCOUNTING_QUIZ_QUESTIONS",
        "quiz_questions",
    )

    for name in possible_names:

        value = getattr(
            data,
            name,
            None,
        )

        if isinstance(value, list):

            return [
                item
                for item in value
                if isinstance(item, dict)
            ]

    return []


# ==========================================================
# Normalization
# ==========================================================

def _normalize_chapter(
    chapter: dict[str, Any],
) -> dict[str, Any]:
    """Normalize chapter structure."""

    result = deepcopy(chapter)

    chapter_id = _item_id(result)

    result["id"] = chapter_id

    result.setdefault(
        "title",
        chapter_id or "فصل بدون عنوان",
    )

    result.setdefault(
        "description",
        "",
    )

    lessons = (
        result.get("lessons")
        or result.get("items")
        or result.get("topics")
        or []
    )

    if isinstance(
        lessons,
        dict,
    ):

        normalized_lessons = []

        for lesson_id, lesson in lessons.items():

            if isinstance(
                lesson,
                dict,
            ):

                lesson_copy = deepcopy(
                    lesson
                )

                lesson_copy.setdefault(
                    "id",
                    str(lesson_id),
                )

                normalized_lessons.append(
                    lesson_copy
                )

        lessons = normalized_lessons

    result["lessons"] = [
        _normalize_lesson(
            lesson
        )
        for lesson in _as_list(lessons)
        if isinstance(
            lesson,
            dict,
        )
    ]

    return result


def _normalize_lesson(
    lesson: dict[str, Any],
) -> dict[str, Any]:
    """Normalize lesson structure."""

    result = deepcopy(lesson)

    lesson_id = _item_id(result)

    result["id"] = lesson_id

    result.setdefault(
        "title",
        lesson_id or "درس بدون عنوان",
    )

    result.setdefault(
        "description",
        "",
    )

    result.setdefault(
        "content",
        result.get("text")
        or result.get("body")
        or result.get("lesson_content")
        or "",
    )

    result.setdefault(
        "specialized_tips",
        [],
    )

    result.setdefault(
        "exam_tips",
        [],
    )

    result.setdefault(
        "examples",
        [],
    )

    result.setdefault(
        "keywords",
        [],
    )

    result.setdefault(
        "quiz",
        [],
    )

    return result


def _normalize_question(
    question: dict[str, Any],
) -> dict[str, Any]:
    """Normalize a quiz question."""

    result = deepcopy(question)

    options = (
        result.get("options")
        or result.get("choices")
        or result.get("answers")
        or []
    )

    normalized_options: list[str] = []

    for option in _as_list(options):

        if isinstance(
            option,
            dict,
        ):

            value = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or ""
            )

        else:
            value = option

        normalized_options.append(
            _text(value)
        )

    result["options"] = normalized_options

    correct = (
        result.get("correct_index")
        if result.get("correct_index") is not None
        else result.get("answer_index")
        if result.get("answer_index") is not None
        else result.get("correct_answer")
        if result.get("correct_answer") is not None
        else result.get("answer")
    )

    if isinstance(
        correct,
        int,
    ):
        result["correct_index"] = correct

    else:

        try:
            result["correct_index"] = int(
                correct
            )

        except (
            TypeError,
            ValueError,
        ):
            result["correct_index"] = -1

    result.setdefault(
        "question",
        result.get("text")
        or result.get("title")
        or "",
    )

    return result


# ==========================================================
# Public Module Information
# ==========================================================

def get_module_title() -> str:
    """Return accounting module title."""

    title = getattr(
        data,
        "MODULE_TITLE",
        None,
    )

    return _text(
        title,
        MODULE_TITLE,
    )


def get_module_info() -> dict[str, str]:
    """Return accounting module metadata."""

    description = getattr(
        data,
        "MODULE_DESCRIPTION",
        None,
    )

    return {
        "id": MODULE_ID,
        "title": get_module_title(),
        "description": _text(
            description,
            DEFAULT_DESCRIPTION,
        ),
    }


# ==========================================================
# Chapters
# ==========================================================

def get_accounting_chapters() -> list[dict[str, Any]]:
    """
    Return all accounting chapters.
    """

    chapters = [
        _normalize_chapter(
            chapter
        )
        for chapter in _get_raw_chapters()
    ]

    return chapters


def get_chapters() -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_accounting_chapters()


def get_accounting_chapter(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """
    Return a single accounting chapter.
    """

    target = str(
        chapter_id
    ).strip()

    for chapter in get_accounting_chapters():

        if str(
            chapter.get("id", "")
        ).strip() == target:

            return chapter

    return None


def get_chapter(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """Compatibility alias."""

    return get_accounting_chapter(
        chapter_id
    )


# ==========================================================
# Lessons
# ==========================================================

def get_accounting_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return lessons belonging to a chapter.
    """

    chapter = get_accounting_chapter(
        chapter_id
    )

    if chapter is None:
        return []

    return [
        _normalize_lesson(
            lesson
        )
        for lesson in _as_list(
            chapter.get("lessons")
        )
        if isinstance(
            lesson,
            dict,
        )
    ]


def get_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_accounting_lessons(
        chapter_id
    )


def get_accounting_lesson(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """
    Return a single lesson.
    """

    target = str(
        lesson_id
    ).strip()

    for lesson in get_accounting_lessons(
        chapter_id
    ):

        if str(
            lesson.get("id", "")
        ).strip() == target:

            return lesson

    return None


def get_lesson(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """Compatibility alias."""

    return get_accounting_lesson(
        chapter_id,
        lesson_id,
    )


# ==========================================================
# Lesson Content
# ==========================================================

def get_lesson_content(
    chapter_id: str | int,
    lesson_id: str | int,
) -> str:
    """
    Return complete lesson content.
    """

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return ""

    return _text(
        lesson.get("content")
        or lesson.get("text")
        or lesson.get("body")
        or lesson.get("description")
    )


def get_specialized_tips(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return specialized accounting tips."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _as_list(
        lesson.get(
            "specialized_tips"
        )
    )


def get_exam_tips(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return examination tips."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _as_list(
        lesson.get(
            "exam_tips"
        )
    )


def get_examples(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return practical examples."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _as_list(
        lesson.get(
            "examples"
        )
    )


def get_keywords(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return lesson keywords."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _as_list(
        lesson.get(
            "keywords"
        )
    )


# ==========================================================
# Quiz
# ==========================================================

def get_accounting_quiz(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return quiz questions for one lesson.
    """

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    quiz = (
        lesson.get("quiz")
        or lesson.get("questions")
        or lesson.get("test")
        or []
    )

    return [
        _normalize_question(
            question
        )
        for question in _as_list(quiz)
        if isinstance(
            question,
            dict,
        )
    ]


def get_quiz(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_accounting_quiz(
        chapter_id,
        lesson_id,
    )


def get_all_quiz_questions() -> list[dict[str, Any]]:
    """
    Aggregate every valid accounting quiz question.

    The questions are returned in curriculum order.
    """

    questions: list[
        dict[str, Any]
    ] = []

    for chapter in get_accounting_chapters():

        chapter_id = chapter.get(
            "id"
        )

        if not chapter_id:
            continue

        for lesson in get_accounting_lessons(
            chapter_id
        ):

            lesson_id = lesson.get(
                "id"
            )

            if not lesson_id:
                continue

            questions.extend(
                get_accounting_quiz(
                    chapter_id,
                    lesson_id,
                )
            )

    # If curriculum quizzes are unavailable,
    # fall back to a global quiz collection.
    if not questions:

        questions.extend(
            _normalize_question(
                question
            )
            for question in _get_raw_quiz()
            if isinstance(
                question,
                dict,
            )
        )

    return questions


def get_all_quiz() -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_all_quiz_questions()


# ==========================================================
# Chapter Quiz
# ==========================================================

def get_accounting_chapter_quiz(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """
    Aggregate all questions from one chapter.
    """

    questions: list[
        dict[str, Any]
    ] = []

    for lesson in get_accounting_lessons(
        chapter_id
    ):

        lesson_id = lesson.get(
            "id"
        )

        if not lesson_id:
            continue

        questions.extend(
            get_accounting_quiz(
                chapter_id,
                lesson_id,
            )
        )

    return questions


def get_chapter_quiz(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_accounting_chapter_quiz(
        chapter_id
    )


# ==========================================================
# Statistics
# ==========================================================

def get_curriculum_stats() -> dict[str, int]:
    """
    Return curriculum statistics.
    """

    chapters = get_accounting_chapters()

    lesson_count = 0

    for chapter in chapters:

        lesson_count += len(
            get_accounting_lessons(
                chapter.get("id", "")
            )
        )

    quiz_questions = len(
        get_all_quiz_questions()
    )

    return {
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": quiz_questions,
    }


def get_accounting_statistics() -> dict[str, int]:
    """Compatibility alias."""

    return get_curriculum_stats()


def get_statistics() -> dict[str, int]:
    """Compatibility alias."""

    return get_curriculum_stats()


# ==========================================================
# Curriculum Validation
# ==========================================================

def validate_curriculum() -> dict[str, Any]:
    """
    Validate the accounting curriculum.

    Returns diagnostic information instead of raising errors.
    """

    chapters = get_accounting_chapters()

    invalid_chapters = []
    invalid_lessons = []
    invalid_questions = []

    for chapter in chapters:

        chapter_id = chapter.get(
            "id"
        )

        if not chapter_id:
            invalid_chapters.append(
                chapter
            )

        for lesson in get_accounting_lessons(
            chapter_id or ""
        ):

            lesson_id = lesson.get(
                "id"
            )

            if not lesson_id:
                invalid_lessons.append(
                    lesson
                )

            for question in get_accounting_quiz(
                chapter_id or "",
                lesson_id or "",
            ):

                options = question.get(
                    "options",
                    [],
                )

                correct_index = question.get(
                    "correct_index",
                    -1,
                )

                if (
                    not question.get(
                        "question"
                    )
                    or len(options) < 2
                    or not (
                        isinstance(
                            correct_index,
                            int,
                        )
                        and 0 <= correct_index < len(options)
                    )
                ):

                    invalid_questions.append(
                        question
                    )

    stats = get_curriculum_stats()

    return {
        "valid": not (
            invalid_chapters
            or invalid_lessons
            or invalid_questions
        ),
        "chapters": stats["chapters"],
        "lessons": stats["lessons"],
        "quiz_questions": stats[
            "quiz_questions"
        ],
        "invalid_chapters": len(
            invalid_chapters
        ),
        "invalid_lessons": len(
            invalid_lessons
        ),
        "invalid_questions": len(
            invalid_questions
        ),
    }


def accounting_health_check() -> bool:
    """
    Lightweight health check for the accounting module.
    """

    try:

        required = (
            get_module_title,
            get_module_info,
            get_accounting_chapters,
            get_accounting_chapter,
            get_accounting_lessons,
            get_accounting_lesson,
            get_accounting_quiz,
            get_all_quiz_questions,
            get_curriculum_stats,
        )

        return all(
            callable(function)
            for function in required
        )

    except Exception:
        logger.exception(
            "Accounting service health check failed."
        )

        return False


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "get_module_title",
    "get_module_info",

    "get_accounting_chapters",
    "get_chapters",

    "get_accounting_chapter",
    "get_chapter",

    "get_accounting_lessons",
    "get_lessons",

    "get_accounting_lesson",
    "get_lesson",

    "get_lesson_content",
    "get_specialized_tips",
    "get_exam_tips",
    "get_examples",
    "get_keywords",

    "get_accounting_quiz",
    "get_quiz",
    "get_all_quiz_questions",
    "get_all_quiz",

    "get_accounting_chapter_quiz",
    "get_chapter_quiz",

    "get_curriculum_stats",
    "get_accounting_statistics",
    "get_statistics",

    "validate_curriculum",
    "accounting_health_check",
]
