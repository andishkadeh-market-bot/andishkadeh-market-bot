"""
Andishkadeh Management & Market
Banking Specialized Module - Service Layer

File:
    modules/banking/service.py

Purpose:
    Complete business/service layer for the Banking module.

Responsibilities:
    - Module information
    - Chapter retrieval
    - Lesson retrieval
    - Lesson content
    - Educational sections
    - Lesson navigation
    - Lesson progress
    - Chapter progress
    - Module progress
    - Quiz retrieval
    - Lesson quizzes
    - Chapter quizzes
    - Comprehensive banking quiz
    - Random quiz pool
    - Quiz answer validation
    - Quiz result recording
    - User statistics
    - Lesson statistics
    - Chapter statistics
    - Banking module statistics
    - Search
    - Curriculum statistics
    - Health checks
    - Compatibility helpers

Design:

    handlers.py
        ↓
    service.py
        ↓
    data.py
        ↓
    core.progress / core.statistics
        ↓
    SQLite

This service layer intentionally contains no Telegram code.
"""

from __future__ import annotations

import logging
import random
from copy import deepcopy
from typing import Any

from . import data

from core.progress import (
    complete_lesson as progress_complete_lesson,
    get_chapter_progress,
    get_lesson_status,
    get_module_progress,
    get_progress_percentage,
    is_lesson_completed,
    is_lesson_started,
    is_module_completed,
    start_lesson as progress_start_lesson,
)

from core.statistics import (
    calculate_score,
    get_attempts,
    get_best_attempt,
    get_latest_attempt,
    get_lesson_attempts,
    get_lesson_statistics,
    get_module_statistics,
    get_recent_attempts,
    get_user_statistics,
    record_quiz_attempt,
    record_quiz_result,
)

from core.database import (
    get_connection,
    init_database,
)


logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = str(
    getattr(
        data,
        "MODULE_ID",
        "banking",
    )
)

MODULE_TITLE = str(
    getattr(
        data,
        "MODULE_TITLE",
        "🏦 بانکداری تخصصی",
    )
)

MODULE_DESCRIPTION = str(
    getattr(
        data,
        "MODULE_DESCRIPTION",
        (
            "آموزش تخصصی و کاربردی بانکداری، "
            "قوانین بانکی، عملیات بانکی، "
            "بانکداری اسلامی، مبارزه با پولشویی، "
            "اعتبارسنجی و مدیریت بانک."
        ),
    )
)


# ==========================================================
# Internal Helpers
# ==========================================================

def _copy(value: Any) -> Any:
    """
    Return a deep copy.

    This prevents handlers or callers from accidentally
    modifying the original curriculum stored in data.py.
    """

    try:
        return deepcopy(value)

    except Exception:
        logger.exception(
            "Failed to deepcopy Banking data."
        )

        return value


def _as_dict(value: Any) -> dict[str, Any]:
    """Return a safe dictionary."""

    if isinstance(value, dict):
        return _copy(value)

    return {}


def _as_list(value: Any) -> list[Any]:
    """Return a safe list."""

    if isinstance(value, list):
        return _copy(value)

    if isinstance(value, tuple):
        return _copy(list(value))

    return []


def _normalize_id(
    value: Any,
) -> str:
    """Normalize an identifier."""

    if value is None:
        return ""

    return str(value)


def _chapter_id(
    chapter: dict[str, Any],
) -> str:
    """Extract normalized chapter ID."""

    value = (
        chapter.get("id")
        or chapter.get("chapter_id")
    )

    return _normalize_id(value)


def _chapter_title(
    chapter: dict[str, Any],
) -> str:
    """Extract normalized chapter title."""

    value = (
        chapter.get("title")
        or chapter.get("name")
        or chapter.get("chapter_title")
        or _chapter_id(chapter)
    )

    return str(value)


def _lesson_id(
    lesson: dict[str, Any],
) -> str:
    """Extract normalized lesson ID."""

    value = (
        lesson.get("id")
        or lesson.get("lesson_id")
    )

    return _normalize_id(value)


def _lesson_title(
    lesson: dict[str, Any],
) -> str:
    """Extract normalized lesson title."""

    value = (
        lesson.get("title")
        or lesson.get("name")
        or lesson.get("lesson_title")
        or _lesson_id(lesson)
    )

    return str(value)


def _get_value(
    item: Any,
    *keys: str,
    default: Any = None,
) -> Any:
    """
    Return the first available dictionary value.
    """

    if not isinstance(item, dict):
        return default

    for key in keys:

        if key in item and item[key] is not None:
            return item[key]

    return default


def _get_chapter_lessons(
    chapter: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Extract lessons from a chapter.

    Supported structures:
        lessons
        chapter_lessons
        content
    """

    for key in (
        "lessons",
        "chapter_lessons",
        "content",
    ):

        value = chapter.get(key)

        if isinstance(value, list):
            return _as_list(value)

    return []


def _question_text(
    question: dict[str, Any],
) -> str:
    """
    Extract question text.
    """

    value = _get_value(
        question,
        "question",
        "text",
        "title",
        "prompt",
        default="",
    )

    return str(value).strip()


def _question_options(
    question: dict[str, Any],
) -> list[Any]:
    """
    Extract question options.
    """

    value = _get_value(
        question,
        "options",
        "answers",
        "choices",
        default=[],
    )

    return _as_list(value)


def _question_correct_index(
    question: dict[str, Any],
) -> int | None:
    """
    Extract normalized correct option index.

    Supports:
        correct_index
        answer_index
        correct
        answer
        correct_answer
    """

    value = _get_value(
        question,
        "correct_index",
        "answer_index",
        "correct_option",
        default=None,
    )

    if value is not None:

        try:
            return int(value)

        except (TypeError, ValueError):
            pass

    # Some datasets use "correct" as integer.
    value = question.get(
        "correct"
    )

    if isinstance(
        value,
        int,
    ):
        return value

    # Some datasets use a textual answer.
    textual_answer = _get_value(
        question,
        "answer",
        "correct_answer",
        "correct_option",
        default=None,
    )

    if textual_answer is not None:

        options = _question_options(
            question
        )

        for index, option in enumerate(
            options
        ):

            if isinstance(option, dict):

                option_value = _get_value(
                    option,
                    "text",
                    "label",
                    "answer",
                    "title",
                    "value",
                    default="",
                )

            else:

                option_value = option

            if str(option_value).strip() == str(
                textual_answer
            ).strip():

                return index

    return None


def _normalize_question(
    question: Any,
    index: int = 0,
) -> dict[str, Any] | None:
    """
    Normalize one quiz question.
    """

    if not isinstance(
        question,
        dict,
    ):
        return None

    normalized = _copy(question)

    normalized["index"] = index

    text = _question_text(
        normalized
    )

    options = _question_options(
        normalized
    )

    correct_index = _question_correct_index(
        normalized
    )

    normalized["question"] = text
    normalized["options"] = options
    normalized["correct_index"] = correct_index

    return normalized


def _normalize_questions(
    questions: list[Any],
) -> list[dict[str, Any]]:
    """
    Normalize a list of quiz questions.
    """

    result: list[dict[str, Any]] = []

    for index, question in enumerate(
        questions
    ):

        normalized = _normalize_question(
            question,
            index=index,
        )

        if normalized is None:
            continue

        if not normalized.get(
            "question"
        ):
            continue

        if not normalized.get(
            "options"
        ):
            continue

        result.append(
            normalized
        )

    return result


def _unique_questions(
    questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove duplicate questions.
    """

    result = []

    seen: set[str] = set()

    for question in questions:

        text = _question_text(
            question
        ).casefold()

        if not text:
            continue

        if text in seen:
            continue

        seen.add(text)

        result.append(
            _copy(question)
        )

    return result


# ==========================================================
# Curriculum Loading
# ==========================================================

def _get_raw_curriculum() -> list[dict[str, Any]]:
    """
    Load curriculum from data.py.

    Supports multiple possible data.py structures so the
    service remains compatible while the module evolves.
    """

    possible_names = (
        "BANKING_CURRICULUM",
        "CURRICULUM",
        "CHAPTERS",
        "BANKING_CHAPTERS",
    )

    for name in possible_names:

        value = getattr(
            data,
            name,
            None,
        )

        if isinstance(
            value,
            list,
        ):

            return _as_list(
                value
            )

    provider = getattr(
        data,
        "get_curriculum",
        None,
    )

    if callable(provider):

        try:

            result = provider()

            if isinstance(
                result,
                list,
            ):

                return _as_list(
                    result
                )

        except Exception:

            logger.exception(
                "Banking curriculum provider failed."
            )

    provider = getattr(
        data,
        "get_chapters",
        None,
    )

    if callable(provider):

        try:

            result = provider()

            if isinstance(
                result,
                list,
            ):

                return _as_list(
                    result
                )

        except Exception:

            logger.exception(
                "Banking get_chapters provider failed."
            )

    return []


# ==========================================================
# Module Information
# ==========================================================

def get_module_info() -> dict[str, Any]:
    """
    Return complete Banking module metadata.
    """

    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "title": MODULE_TITLE,
        "description": MODULE_DESCRIPTION,
        "type": "specialized_banking",
    }


def get_module_id() -> str:
    """Return Banking module ID."""

    return MODULE_ID


def get_module_title() -> str:
    """Return Banking module title."""

    return MODULE_TITLE


def get_module_description() -> str:
    """Return Banking module description."""

    return MODULE_DESCRIPTION


# ==========================================================
# Chapters
# ==========================================================

def get_chapters() -> list[dict[str, Any]]:
    """
    Return all Banking chapters.

    Every chapter is normalized to:

        {
            "id": "...",
            "chapter_id": "...",
            "title": "...",
            "lessons": [...]
        }
    """

    curriculum = _get_raw_curriculum()

    result: list[dict[str, Any]] = []

    for chapter in curriculum:

        if not isinstance(
            chapter,
            dict,
        ):
            continue

        chapter_id = _chapter_id(
            chapter
        )

        if not chapter_id:
            continue

        normalized = _copy(
            chapter
        )

        normalized["id"] = chapter_id
        normalized["chapter_id"] = chapter_id
        normalized["title"] = _chapter_title(
            chapter
        )

        normalized["lessons"] = (
            _get_chapter_lessons(
                chapter
            )
        )

        result.append(
            normalized
        )

    return result


def get_all_chapters() -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_chapters()


def get_chapter(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """
    Return one chapter by ID.
    """

    target = str(
        chapter_id
    )

    for chapter in get_chapters():

        if target in {
            str(
                chapter.get(
                    "id",
                    "",
                )
            ),
            str(
                chapter.get(
                    "chapter_id",
                    "",
                )
            ),
        }:

            return _copy(
                chapter
            )

    return None


def chapter_exists(
    chapter_id: str | int,
) -> bool:
    """Check chapter existence."""

    return (
        get_chapter(
            chapter_id
        )
        is not None
    )


def get_chapter_index(
    chapter_id: str | int,
) -> int:
    """
    Return zero-based chapter index.
    """

    target = str(
        chapter_id
    )

    for index, chapter in enumerate(
        get_chapters()
    ):

        if _chapter_id(
            chapter
        ) == target:

            return index

    return -1


# ==========================================================
# Lessons
# ==========================================================

def get_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return all lessons of a chapter.
    """

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return []

    result: list[dict[str, Any]] = []

    for lesson in _get_chapter_lessons(
        chapter
    ):

        if not isinstance(
            lesson,
            dict,
        ):
            continue

        lesson_id = _lesson_id(
            lesson
        )

        if not lesson_id:
            continue

        normalized = _copy(
            lesson
        )

        normalized["id"] = lesson_id
        normalized["lesson_id"] = lesson_id
        normalized["title"] = _lesson_title(
            lesson
        )
        normalized["chapter_id"] = str(
            chapter_id
        )
        normalized["module_id"] = MODULE_ID

        result.append(
            normalized
        )

    return result


def get_all_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """Compatibility alias."""

    return get_lessons(
        chapter_id
    )


def get_lesson(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """
    Return one lesson from a chapter.
    """

    target_chapter = str(
        chapter_id
    )

    target_lesson = str(
        lesson_id
    )

    for lesson in get_lessons(
        target_chapter
    ):

        if target_lesson in {
            str(
                lesson.get(
                    "id",
                    "",
                )
            ),
            str(
                lesson.get(
                    "lesson_id",
                    "",
                )
            ),
        }:

            return _copy(
                lesson
            )

    return None


def lesson_exists(
    chapter_id: str | int,
    lesson_id: str | int,
) -> bool:
    """Check lesson existence."""

    return (
        get_lesson(
            chapter_id,
            lesson_id,
        )
        is not None
    )


def get_lesson_index(
    chapter_id: str | int,
    lesson_id: str | int,
) -> int:
    """
    Return zero-based lesson index.
    """

    target = str(
        lesson_id
    )

    for index, lesson in enumerate(
        get_lessons(
            chapter_id
        )
    ):

        if _lesson_id(
            lesson
        ) == target:

            return index

    return -1


# ==========================================================
# Lesson Navigation
# ==========================================================

def get_previous_lesson(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """Return previous lesson in the same chapter."""

    index = get_lesson_index(
        chapter_id,
        lesson_id,
    )

    if index <= 0:
        return None

    lessons = get_lessons(
        chapter_id
    )

    return _copy(
        lessons[index - 1]
    )


def get_next_lesson(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """Return next lesson in the same chapter."""

    index = get_lesson_index(
        chapter_id,
        lesson_id,
    )

    if index < 0:
        return None

    lessons = get_lessons(
        chapter_id
    )

    if index + 1 >= len(
        lessons
    ):
        return None

    return _copy(
        lessons[index + 1]
    )


def get_first_lesson(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """Return first lesson of a chapter."""

    lessons = get_lessons(
        chapter_id
    )

    if not lessons:
        return None

    return _copy(
        lessons[0]
    )


def get_last_lesson(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """Return last lesson of a chapter."""

    lessons = get_lessons(
        chapter_id
    )

    if not lessons:
        return None

    return _copy(
        lessons[-1]
    )


# ==========================================================
# Lesson Content
# ==========================================================

def get_lesson_content(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """
    Return complete lesson content.
    """

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    return _copy(
        lesson
    )


def get_lesson_details(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """Compatibility alias."""

    return get_lesson_content(
        chapter_id,
        lesson_id,
    )


def get_lesson_text(
    chapter_id: str | int,
    lesson_id: str | int,
) -> str:
    """
    Return the primary educational text.
    """

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return ""

    for key in (
        "content",
        "text",
        "lesson_text",
        "description",
        "body",
        "explanation",
    ):

        value = lesson.get(
            key
        )

        if isinstance(
            value,
            str,
        ) and value.strip():

            return value.strip()

    return ""


def get_lesson_section(
    chapter_id: str | int,
    lesson_id: str | int,
    section: str,
) -> Any:
    """
    Return a specific educational section.
    """

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    return _copy(
        lesson.get(
            section
        )
    )


def get_summary(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return lesson summary."""

    for key in (
        "summary",
        "lesson_summary",
        "review",
    ):

        value = get_lesson_section(
            chapter_id,
            lesson_id,
            key,
        )

        if value:
            return value

    return None


def get_exam_notes(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return exam notes."""

    for key in (
        "exam_notes",
        "exam_tips",
        "test_notes",
        "exam_points",
    ):

        value = get_lesson_section(
            chapter_id,
            lesson_id,
            key,
        )

        if value:
            return value

    return None


def get_specialized_notes(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return specialized/technical notes."""

    for key in (
        "specialized_notes",
        "technical_notes",
        "expert_notes",
        "professional_notes",
    ):

        value = get_lesson_section(
            chapter_id,
            lesson_id,
            key,
        )

        if value:
            return value

    return None


def get_examples(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return practical examples."""

    for key in (
        "examples",
        "practical_examples",
        "applications",
    ):

        value = get_lesson_section(
            chapter_id,
            lesson_id,
            key,
        )

        if isinstance(
            value,
            list,
        ):

            return _as_list(
                value
            )

    return []


def get_references(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return references."""

    for key in (
        "references",
        "sources",
        "resources",
    ):

        value = get_lesson_section(
            chapter_id,
            lesson_id,
            key,
        )

        if isinstance(
            value,
            list,
        ):

            return _as_list(
                value
            )

    return []


# ==========================================================
# Quiz - Lesson
# ==========================================================

def get_quiz_questions(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return normalized quiz questions for a lesson.

    Special compatibility modes:

        lesson_id == "chapter"
            → all questions of the chapter

        lesson_id in ("general", "all", "comprehensive")
            → all Banking questions
    """

    lesson_target = str(
        lesson_id
    )

    if lesson_target == "chapter":

        return get_chapter_quiz_questions(
            chapter_id
        )

    if lesson_target in {
        "general",
        "all",
        "comprehensive",
        "banking",
    }:

        return get_comprehensive_quiz_questions()

    lesson = get_lesson(
        chapter_id,
        lesson_target,
    )

    if lesson is None:
        return []

    for key in (
        "questions",
        "quiz_questions",
        "quiz",
    ):

        value = lesson.get(
            key
        )

        if isinstance(
            value,
            list,
        ):

            return _normalize_questions(
                value
            )

    return []


def get_quiz_question(
    chapter_id: str | int,
    lesson_id: str | int,
    question_index: int,
) -> dict[str, Any] | None:
    """
    Return one lesson quiz question.
    """

    if question_index < 0:
        return None

    questions = get_quiz_questions(
        chapter_id,
        lesson_id,
    )

    if question_index >= len(
        questions
    ):
        return None

    return _copy(
        questions[
            question_index
        ]
    )


def get_question_count(
    chapter_id: str | int,
    lesson_id: str | int,
) -> int:
    """Return question count."""

    return len(
        get_quiz_questions(
            chapter_id,
            lesson_id,
        )
    )


# ==========================================================
# Quiz - Chapter
# ==========================================================

def get_chapter_quiz_questions(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """
    Collect all quiz questions belonging to a chapter.
    """

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return []

    result: list[dict[str, Any]] = []

    for lesson in get_lessons(
        chapter_id
    ):

        lesson_id = _lesson_id(
            lesson
        )

        if not lesson_id:
            continue

        questions = []

        for key in (
            "questions",
            "quiz_questions",
            "quiz",
        ):

            value = lesson.get(
                key
            )

            if isinstance(
                value,
                list,
            ):

                questions = value
                break

        normalized = _normalize_questions(
            questions
        )

        for question in normalized:

            question["module_id"] = MODULE_ID
            question["chapter_id"] = str(
                chapter_id
            )
            question["lesson_id"] = lesson_id
            question["lesson_title"] = _lesson_title(
                lesson
            )

            result.append(
                question
            )

    return _unique_questions(
        result
    )


# ==========================================================
# Quiz - Comprehensive
# ==========================================================

def get_comprehensive_quiz_questions() -> list[dict[str, Any]]:
    """
    Collect all available Banking questions.
    """

    result: list[dict[str, Any]] = []

    for chapter in get_chapters():

        chapter_id = _chapter_id(
            chapter
        )

        for lesson in get_lessons(
            chapter_id
        ):

            lesson_id = _lesson_id(
                lesson
            )

            if not lesson_id:
                continue

            for question in get_quiz_questions(
                chapter_id,
                lesson_id,
            ):

                normalized = _copy(
                    question
                )

                normalized["module_id"] = MODULE_ID
                normalized["chapter_id"] = chapter_id
                normalized["lesson_id"] = lesson_id
                normalized["chapter_title"] = _chapter_title(
                    chapter
                )
                normalized["lesson_title"] = _lesson_title(
                    lesson
                )

                result.append(
                    normalized
                )

    return _unique_questions(
        result
    )


# ==========================================================
# Random Quiz
# ==========================================================

def get_random_quiz_questions(
    count: int = 10,
    chapter_id: str | int | None = None,
    lesson_id: str | int | None = None,
) -> list[dict[str, Any]]:
    """
    Return random Banking questions.

    If chapter_id and lesson_id are provided:
        questions are selected from that lesson.

    If only chapter_id is provided:
        questions are selected from that chapter.

    Otherwise:
        questions are selected from the whole Banking module.
    """

    if count <= 0:
        return []

    if (
        chapter_id is not None
        and lesson_id is not None
    ):

        pool = get_quiz_questions(
            chapter_id,
            lesson_id,
        )

    elif chapter_id is not None:

        pool = get_chapter_quiz_questions(
            chapter_id
        )

    else:

        pool = get_comprehensive_quiz_questions()

    pool = _unique_questions(
        pool
    )

    if not pool:
        return []

    selected = random.sample(
        pool,
        min(
            count,
            len(pool),
        ),
    )

    return _copy(
        selected
    )


# ==========================================================
# Quiz Answer Validation
# ==========================================================

def check_quiz_answer(
    question: dict[str, Any],
    selected_index: int,
) -> dict[str, Any]:
    """
    Validate a quiz answer.

    Returns:

        {
            "valid": bool,
            "correct": bool,
            "selected_index": int,
            "correct_index": int | None,
            "explanation": ...,
            "question": ...,
        }
    """

    normalized = _normalize_question(
        question
    )

    if normalized is None:

        return {
            "valid": False,
            "correct": False,
            "selected_index": selected_index,
            "correct_index": None,
            "explanation": None,
            "question": "",
        }

    options = normalized.get(
        "options",
        [],
    )

    correct_index = normalized.get(
        "correct_index"
    )

    if not isinstance(
        selected_index,
        int,
    ):

        return {
            "valid": False,
            "correct": False,
            "selected_index": selected_index,
            "correct_index": correct_index,
            "explanation": None,
            "question": normalized.get(
                "question",
                "",
            ),
        }

    if (
        selected_index < 0
        or selected_index >= len(
            options
        )
    ):

        return {
            "valid": False,
            "correct": False,
            "selected_index": selected_index,
            "correct_index": correct_index,
            "explanation": None,
            "question": normalized.get(
                "question",
                "",
            ),
        }

    correct = (
        correct_index is not None
        and selected_index == correct_index
    )

    explanation = _get_value(
        normalized,
        "explanation",
        "answer_explanation",
        "solution",
        "reason",
        default=None,
    )

    return {
        "valid": True,
        "correct": bool(correct),
        "selected_index": selected_index,
        "correct_index": correct_index,
        "selected_option": _copy(
            options[selected_index]
        ),
        "correct_option": (
            _copy(
                options[correct_index]
            )
            if isinstance(
                correct_index,
                int,
            )
            and 0 <= correct_index < len(
                options
            )
            else None
        ),
        "explanation": _copy(
            explanation
        ),
        "question": normalized.get(
            "question",
            "",
        ),
    }


def is_quiz_answer_correct(
    question: dict[str, Any],
    selected_index: int,
) -> bool:
    """Simple boolean answer check."""

    result = check_quiz_answer(
        question,
        selected_index,
    )

    return bool(
        result.get(
            "valid"
        )
        and result.get(
            "correct"
        )
    )


# ==========================================================
# Quiz Result
# ==========================================================

def calculate_quiz_score(
    correct_answers: int,
    total_questions: int,
) -> float:
    """Calculate percentage score."""

    return calculate_score(
        correct_answers=correct_answers,
        total_questions=total_questions,
    )


def record_banking_quiz_result(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """
    Record Banking quiz result.

    For comprehensive/chapter quizzes the same database
    structure is used, while chapter_id/lesson_id identify
    the quiz scope.
    """

    return record_quiz_result(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
    )


def save_quiz_result(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """Compatibility alias."""

    return record_banking_quiz_result(
        telegram_id=telegram_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
    )


# ==========================================================
# Lesson Progress
# ==========================================================

def start_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """
    Mark Banking lesson as started.
    """

    if not lesson_exists(
        chapter_id,
        lesson_id,
    ):
        return False

    progress_start_lesson(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )

    return True


def complete_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """
    Mark Banking lesson as completed.
    """

    if not lesson_exists(
        chapter_id,
        lesson_id,
    ):
        return False

    progress_complete_lesson(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )

    return True


def get_lesson_progress(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any]:
    """Return progress for one Banking lesson."""

    return get_lesson_status(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )


def is_lesson_started_by_user(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Check lesson started status."""

    return is_lesson_started(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )


def is_lesson_completed_by_user(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Check lesson completion status."""

    return is_lesson_completed(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )


# ==========================================================
# Chapter Progress
# ==========================================================

def get_banking_chapter_progress(
    telegram_id: int,
    chapter_id: str,
) -> dict[str, Any]:
    """Return progress for one Banking chapter."""

    return get_chapter_progress(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
    )


def get_chapter_completion_percentage(
    telegram_id: int,
    chapter_id: str,
) -> float:
    """Return chapter completion percentage."""

    progress = get_banking_chapter_progress(
        telegram_id,
        chapter_id,
    )

    return float(
        progress.get(
            "percentage",
            0.0,
        )
    )


# ==========================================================
# Module Progress
# ==========================================================

def get_banking_progress(
    telegram_id: int,
) -> dict[str, Any]:
    """
    Return complete Banking module progress.
    """

    return get_module_progress(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_progress_percentage(
    telegram_id: int,
) -> float:
    """Return Banking completion percentage."""

    return get_progress_percentage(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def is_banking_completed(
    telegram_id: int,
) -> bool:
    """Return whether Banking module is complete."""

    return is_module_completed(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


# ==========================================================
# User Statistics
# ==========================================================

def get_banking_user_statistics(
    telegram_id: int,
) -> dict[str, Any]:
    """
    Return Banking-specific user statistics.
    """

    return get_user_statistics(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_statistics(
    telegram_id: int,
) -> dict[str, Any]:
    """
    Return combined Banking progress + quiz statistics.

    This is the main API for a future:
        🏦 پیشرفت بانکداری
    page.
    """

    progress = get_banking_progress(
        telegram_id
    )

    quiz = get_banking_user_statistics(
        telegram_id
    )

    curriculum = get_curriculum_statistics()

    return {
        "module_id": MODULE_ID,
        "module_title": MODULE_TITLE,

        "curriculum": curriculum,

        "progress": progress,

        "quiz": quiz,

        "summary": {
            "chapters_total": curriculum[
                "chapters"
            ],
            "lessons_total": curriculum[
                "lessons"
            ],
            "questions_total": curriculum[
                "questions"
            ],
            "chapters_completed": sum(
                1
                for chapter in progress.get(
                    "chapters",
                    [],
                )
                if chapter.get(
                    "completed",
                    False,
                )
            ),
            "lessons_completed": progress.get(
                "completed_lessons",
                0,
            ),
            "lessons_started": progress.get(
                "started_lessons",
                0,
            ),
            "quiz_attempts": quiz.get(
                "attempts",
                0,
            ),
            "correct_answers": quiz.get(
                "correct_answers",
                0,
            ),
            "wrong_answers": quiz.get(
                "wrong_answers",
                0,
            ),
            "average_score": quiz.get(
                "average_score",
                0,
            ),
            "best_score": quiz.get(
                "best_score",
                0,
            ),
        },
    }


# ==========================================================
# Lesson Statistics
# ==========================================================

def get_banking_lesson_statistics(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any]:
    """
    Return quiz statistics for one Banking lesson.
    """

    return get_lesson_statistics(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )


def get_banking_lesson_attempts(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return attempts for one Banking lesson."""

    return get_lesson_attempts(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=str(
            chapter_id
        ),
        lesson_id=str(
            lesson_id
        ),
    )


# ==========================================================
# Chapter Statistics
# ==========================================================

def get_banking_chapter_statistics(
    telegram_id: int,
    chapter_id: str,
) -> dict[str, Any]:
    """
    Return combined progress and quiz statistics
    for one Banking chapter.
    """

    chapter_id = str(
        chapter_id
    )

    progress = get_banking_chapter_progress(
        telegram_id,
        chapter_id,
    )

    attempts = get_attempts(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=chapter_id,
    )

    total_questions = sum(
        int(
            attempt.get(
                "total_questions",
                0,
            )
        )
        for attempt in attempts
    )

    correct_answers = sum(
        int(
            attempt.get(
                "correct_answers",
                0,
            )
        )
        for attempt in attempts
    )

    scores = [
        float(
            attempt.get(
                "score",
                0,
            )
        )
        for attempt in attempts
    ]

    average_score = (
        round(
            sum(scores)
            / len(scores),
            2,
        )
        if scores
        else 0.0
    )

    best_score = (
        round(
            max(scores),
            2,
        )
        if scores
        else 0.0
    )

    return {
        "module_id": MODULE_ID,
        "chapter_id": chapter_id,
        "progress": progress,
        "quiz": {
            "attempts": len(
                attempts
            ),
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "wrong_answers": (
                total_questions
                - correct_answers
            ),
            "accuracy": (
                round(
                    correct_answers
                    / total_questions
                    * 100,
                    2,
                )
                if total_questions
                else 0.0
            ),
            "average_score": average_score,
            "best_score": best_score,
        },
    }


# ==========================================================
# Attempts
# ==========================================================

def get_banking_attempts(
    telegram_id: int,
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return Banking quiz attempts.
    """

    return get_attempts(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )


def get_banking_latest_attempt(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return latest Banking quiz attempt."""

    return get_latest_attempt(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_best_attempt(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return best Banking quiz attempt."""

    return get_best_attempt(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_recent_attempts(
    telegram_id: int,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return recent Banking attempts."""

    return get_recent_attempts(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        limit=limit,
    )


# ==========================================================
# Curriculum Statistics
# ==========================================================

def get_curriculum_statistics() -> dict[str, int]:
    """
    Calculate Banking curriculum statistics.

    Returns:

        chapters
        lessons
        questions
    """

    chapters = get_chapters()

    lessons_count = 0
    questions_count = 0

    for chapter in chapters:

        chapter_id = _chapter_id(
            chapter
        )

        lessons = get_lessons(
            chapter_id
        )

        lessons_count += len(
            lessons
        )

        for lesson in lessons:

            lesson_id = _lesson_id(
                lesson
            )

            questions_count += len(
                get_quiz_questions(
                    chapter_id,
                    lesson_id,
                )
            )

    return {
        "chapters": len(
            chapters
        ),
        "lessons": lessons_count,
        "questions": questions_count,
    }


def statistics() -> dict[str, int]:
    """Compatibility alias."""

    return get_curriculum_statistics()


# ==========================================================
# Search
# ==========================================================

def search(
    query: str,
) -> list[dict[str, Any]]:
    """
    Search Banking curriculum.

    Searches:
        - chapter title
        - lesson title
        - lesson content
        - keywords
        - examples
        - technical notes
        - exam notes
        - summaries
    """

    normalized_query = (
        str(
            query or ""
        )
        .strip()
        .casefold()
    )

    if not normalized_query:
        return []

    results: list[
        dict[str, Any]
    ] = []

    for chapter in get_chapters():

        chapter_id = _chapter_id(
            chapter
        )

        chapter_title = _chapter_title(
            chapter
        )

        chapter_parts = [
            chapter_title,
            str(
                chapter.get(
                    "description",
                    "",
                )
            ),
            str(
                chapter.get(
                    "keywords",
                    "",
                )
            ),
        ]

        chapter_haystack = " ".join(
            chapter_parts
        ).casefold()

        for lesson in get_lessons(
            chapter_id
        ):

            lesson_id = _lesson_id(
                lesson
            )

            lesson_title = _lesson_title(
                lesson
            )

            searchable_parts = [
                chapter_title,
                chapter_haystack,
                lesson_title,
                str(
                    lesson.get(
                        "content",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "text",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "keywords",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "technical_notes",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "specialized_notes",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "exam_notes",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "exam_tips",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "summary",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "description",
                        "",
                    )
                ),
                str(
                    lesson.get(
                        "examples",
                        "",
                    )
                ),
            ]

            haystack = " ".join(
                searchable_parts
            ).casefold()

            if (
                normalized_query
                in haystack
            ):

                results.append(
                    {
                        "module_id": MODULE_ID,
                        "chapter_id": chapter_id,
                        "chapter_title": chapter_title,
                        "lesson_id": lesson_id,
                        "lesson_title": lesson_title,
                    }
                )

    return results


def search_lessons(
    query: str,
) -> list[dict[str, Any]]:
    """Compatibility alias for search."""

    return search(
        query
    )


# ==========================================================
# Progress + Curriculum Overview
# ==========================================================

def get_user_learning_overview(
    telegram_id: int,
) -> dict[str, Any]:
    """
    Return a complete learning overview for Banking.
    """

    curriculum = get_curriculum_statistics()

    progress = get_banking_progress(
        telegram_id
    )

    statistics_data = get_banking_user_statistics(
        telegram_id
    )

    chapters = []

    for chapter in get_chapters():

        chapter_id = _chapter_id(
            chapter
        )

        chapter_progress = (
            get_banking_chapter_progress(
                telegram_id,
                chapter_id,
            )
        )

        chapters.append(
            {
                "chapter_id": chapter_id,
                "title": _chapter_title(
                    chapter
                ),
                "progress": chapter_progress,
            }
        )

    return {
        "module": get_module_info(),
        "curriculum": curriculum,
        "progress": progress,
        "statistics": statistics_data,
        "chapters": chapters,
    }


# ==========================================================
# Health Checks
# ==========================================================

def data_health_check() -> bool:
    """
    Validate Banking data structure.

    Quiz questions are allowed to be empty while the
    educational curriculum is still being expanded.
    """

    try:

        if not MODULE_ID:
            logger.error(
                "Banking MODULE_ID is empty."
            )
            return False

        if not MODULE_TITLE:
            logger.error(
                "Banking MODULE_TITLE is empty."
            )
            return False

        chapters = get_chapters()

        if not isinstance(
            chapters,
            list,
        ):
            return False

        seen_chapters: set[str] = set()

        for chapter in chapters:

            if not isinstance(
                chapter,
                dict,
            ):
                return False

            chapter_id = _chapter_id(
                chapter
            )

            if not chapter_id:
                return False

            if chapter_id in seen_chapters:

                logger.error(
                    "Duplicate Banking chapter ID: %s",
                    chapter_id,
                )

                return False

            seen_chapters.add(
                chapter_id
            )

            seen_lessons: set[str] = set()

            for lesson in get_lessons(
                chapter_id
            ):

                lesson_id = _lesson_id(
                    lesson
                )

                if not lesson_id:
                    return False

                if lesson_id in seen_lessons:

                    logger.error(
                        (
                            "Duplicate Banking lesson "
                            "ID '%s' in chapter '%s'."
                        ),
                        lesson_id,
                        chapter_id,
                    )

                    return False

                seen_lessons.add(
                    lesson_id
                )

        stats = get_curriculum_statistics()

        logger.info(
            (
                "Banking data health check: OK "
                "chapters=%s lessons=%s questions=%s"
            ),
            stats["chapters"],
            stats["lessons"],
            stats["questions"],
        )

        return True

    except Exception:

        logger.exception(
            "Banking data health check failed."
        )

        return False


def service_health_check() -> bool:
    """
    Validate the Banking service layer.
    """

    try:

        init_database()

        info = get_module_info()

        if not isinstance(
            info,
            dict,
        ):
            return False

        if not info.get(
            "id"
        ):
            return False

        chapters = get_chapters()

        if not isinstance(
            chapters,
            list,
        ):
            return False

        curriculum_stats = (
            get_curriculum_statistics()
        )

        if not isinstance(
            curriculum_stats,
            dict,
        ):
            return False

        required_keys = {
            "chapters",
            "lessons",
            "questions",
        }

        if not required_keys.issubset(
            curriculum_stats.keys()
        ):
            return False

        return data_health_check()

    except Exception:

        logger.exception(
            "Banking service health check failed."
        )

        return False


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    # Module
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "get_module_info",
    "get_module_id",
    "get_module_title",
    "get_module_description",

    # Chapters
    "get_chapters",
    "get_all_chapters",
    "get_chapter",
    "chapter_exists",
    "get_chapter_index",

    # Lessons
    "get_lessons",
    "get_all_lessons",
    "get_lesson",
    "lesson_exists",
    "get_lesson_index",

    # Navigation
    "get_previous_lesson",
    "get_next_lesson",
    "get_first_lesson",
    "get_last_lesson",

    # Lesson content
    "get_lesson_content",
    "get_lesson_details",
    "get_lesson_text",
    "get_lesson_section",
    "get_summary",
    "get_exam_notes",
    "get_specialized_notes",
    "get_examples",
    "get_references",

    # Quiz
    "get_quiz_questions",
    "get_quiz_question",
    "get_question_count",
    "get_chapter_quiz_questions",
    "get_comprehensive_quiz_questions",
    "get_random_quiz_questions",
    "check_quiz_answer",
    "is_quiz_answer_correct",

    # Quiz result
    "calculate_quiz_score",
    "record_banking_quiz_result",
    "save_quiz_result",

    # Progress
    "start_lesson",
    "complete_lesson",
    "get_lesson_progress",
    "is_lesson_started_by_user",
    "is_lesson_completed_by_user",
    "get_banking_chapter_progress",
    "get_chapter_completion_percentage",
    "get_banking_progress",
    "get_banking_progress_percentage",
    "is_banking_completed",

    # Statistics
    "get_banking_statistics",
    "get_banking_user_statistics",
    "get_banking_lesson_statistics",
    "get_banking_lesson_attempts",
    "get_banking_chapter_statistics",
    "get_banking_attempts",
    "get_banking_latest_attempt",
    "get_banking_best_attempt",
    "get_banking_recent_attempts",

    # Curriculum
    "get_curriculum_statistics",
    "statistics",

    # Search
    "search",
    "search_lessons",

    # Overview
    "get_user_learning_overview",

    # Health
    "data_health_check",
    "service_health_check",
]
