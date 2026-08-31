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
    - Data validation
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
    """Return a safe deep copy."""

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


def _normalize_id(value: Any) -> str:
    """Normalize an identifier."""

    if value is None:
        return ""

    return str(value).strip()


def _chapter_id(
    chapter: dict[str, Any],
) -> str:
    """Extract normalized chapter ID."""

    return _normalize_id(
        chapter.get("id")
        or chapter.get("chapter_id")
    )


def _chapter_title(
    chapter: dict[str, Any],
) -> str:
    """Extract normalized chapter title."""

    return str(
        chapter.get("title")
        or chapter.get("name")
        or chapter.get("chapter_title")
        or _chapter_id(chapter)
    ).strip()


def _lesson_id(
    lesson: dict[str, Any],
) -> str:
    """Extract normalized lesson ID."""

    return _normalize_id(
        lesson.get("id")
        or lesson.get("lesson_id")
    )


def _lesson_title(
    lesson: dict[str, Any],
) -> str:
    """Extract normalized lesson title."""

    return str(
        lesson.get("title")
        or lesson.get("name")
        or lesson.get("lesson_title")
        or _lesson_id(lesson)
    ).strip()


def _get_value(
    item: Any,
    *keys: str,
    default: Any = None,
) -> Any:
    """Return the first available dictionary value."""

    if not isinstance(item, dict):
        return default

    for key in keys:
        if key in item and item[key] is not None:
            return item[key]

    return default


def _get_chapter_lessons(
    chapter: dict[str, Any],
) -> list[dict[str, Any]]:
    """Extract lessons from a chapter."""

    for key in (
        "lessons",
        "chapter_lessons",
        "content",
    ):
        value = chapter.get(key)

        if isinstance(value, list):
            return _as_list(value)

    return []


def _get_lesson_questions(
    lesson: dict[str, Any],
) -> list[Any]:
    """Extract raw questions from a lesson."""

    for key in (
        "questions",
        "quiz_questions",
        "quiz",
        "tests",
        "test_questions",
    ):
        value = lesson.get(key)

        if isinstance(value, list):
            return _as_list(value)

    return []


def _question_text(
    question: dict[str, Any],
) -> str:
    """Extract question text."""

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
    """Extract question options."""

    value = _get_value(
        question,
        "options",
        "answers",
        "choices",
        "alternatives",
        default=[],
    )

    return _as_list(value)


def _option_text(
    option: Any,
) -> str:
    """Extract visible option text."""

    if isinstance(option, dict):
        value = _get_value(
            option,
            "text",
            "label",
            "answer",
            "title",
            "value",
            default="",
        )

        return str(value).strip()

    return str(option).strip()


def _letter_to_index(
    value: Any,
) -> int | None:
    """
    Convert A/B/C/D or numeric values to zero-based index.
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value

    text = str(value).strip().upper()

    mapping = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    if text in mapping:
        return mapping[text]

    # Support forms such as:
    # "A)", "A.", "گزینه A"
    cleaned = (
        text
        .replace(")", "")
        .replace("(", "")
        .replace(".", "")
        .replace("گزینه", "")
        .strip()
    )

    if cleaned in mapping:
        return mapping[cleaned]

    try:
        return int(cleaned)
    except (TypeError, ValueError):
        return None


def _find_option_index(
    options: list[Any],
    answer: Any,
) -> int | None:
    """Find an answer inside the option list."""

    if answer is None:
        return None

    direct_index = _letter_to_index(answer)

    if direct_index is not None:
        if 0 <= direct_index < len(options):
            return direct_index

    target = str(answer).strip().casefold()

    for index, option in enumerate(options):
        option_text = _option_text(option).casefold()

        if option_text == target:
            return index

    return None


def _question_correct_index(
    question: dict[str, Any],
) -> int | None:
    """
    Resolve the correct answer from all supported schemas.

    Supported:
        correct_index
        answer_index
        correct_option
        correct
        answer
        correct_answer
        answer_letter
    """

    options = _question_options(question)

    # ------------------------------------------------------
    # Explicit numeric/index fields
    # ------------------------------------------------------

    for key in (
        "correct_index",
        "answer_index",
    ):
        if key in question:

            value = question.get(key)

            index = _letter_to_index(value)

            if index is not None:
                if not options or 0 <= index < len(options):
                    return index

    # ------------------------------------------------------
    # Letter/text fields
    # ------------------------------------------------------

    for key in (
        "answer_letter",
        "correct_answer",
        "answer",
        "correct_option",
        "correct",
    ):

        if key not in question:
            continue

        value = question.get(key)

        if isinstance(value, dict):

            value = _get_value(
                value,
                "text",
                "label",
                "answer",
                "value",
                "index",
                default=None,
            )

        index = _find_option_index(
            options,
            value,
        )

        if index is not None:
            return index

    return None


def _normalize_question(
    question: Any,
    index: int = 0,
) -> dict[str, Any] | None:
    """
    Normalize one quiz question.

    Important:
        data.py may store answers as A/B/C/D.
        This function converts them into correct_index.
    """

    if not isinstance(question, dict):
        return None

    normalized = _copy(question)

    options = _question_options(
        normalized
    )

    correct_index = _question_correct_index(
        normalized
    )

    normalized["index"] = index
    normalized["question"] = _question_text(
        normalized
    )
    normalized["options"] = options
    normalized["correct_index"] = correct_index

    if correct_index is not None:
        normalized["correct_letter"] = chr(
            ord("A") + correct_index
        )

    return normalized


def _normalize_questions(
    questions: list[Any],
) -> list[dict[str, Any]]:
    """Normalize a list of questions."""

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
    """Remove duplicate questions."""

    result: list[dict[str, Any]] = []
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

    Supported:
        BANKING_CURRICULUM
        CURRICULUM
        CHAPTERS
        BANKING_CHAPTERS
        get_curriculum()
        get_chapters()
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
            return _as_list(value)

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
                return _as_list(result)

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
                return _as_list(result)

        except Exception:
            logger.exception(
                "Banking get_chapters provider failed."
            )

    return []


# ==========================================================
# Module Information
# ==========================================================

def get_module_info() -> dict[str, Any]:
    """Return complete Banking module metadata."""

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
    """Return all Banking chapters."""

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
        normalized["module_id"] = MODULE_ID

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
    """Return one chapter by ID."""

    target = str(
        chapter_id
    )

    for chapter in get_chapters():

        if _chapter_id(
            chapter
        ) == target:

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
    """Return zero-based chapter index."""

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


def get_next_chapter(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """Return the next chapter."""

    index = get_chapter_index(
        chapter_id
    )

    if index < 0:
        return None

    chapters = get_chapters()

    if index + 1 >= len(chapters):
        return None

    return _copy(
        chapters[index + 1]
    )


def get_previous_chapter(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """Return the previous chapter."""

    index = get_chapter_index(
        chapter_id
    )

    if index <= 0:
        return None

    chapters = get_chapters()

    return _copy(
        chapters[index - 1]
    )


# ==========================================================
# Lessons
# ==========================================================

def get_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """Return all lessons of a chapter."""

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
    """Return one lesson."""

    target_chapter = str(
        chapter_id
    )

    target_lesson = str(
        lesson_id
    )

    for lesson in get_lessons(
        target_chapter
    ):

        if _lesson_id(
            lesson
        ) == target_lesson:

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
    """Return zero-based lesson index."""

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
    """Return previous lesson."""

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
    """Return next lesson."""

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
    """Return first lesson."""

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
    """Return last lesson."""

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
    """Return complete lesson content."""

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
    """Return primary educational text."""

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
        "article",
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
    """Return a specific lesson section."""

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


def _get_first_section(
    chapter_id: str | int,
    lesson_id: str | int,
    keys: tuple[str, ...],
) -> Any:
    """Return first available section."""

    for key in keys:

        value = get_lesson_section(
            chapter_id,
            lesson_id,
            key,
        )

        if value:
            return value

    return None


def get_summary(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return lesson summary."""

    return _get_first_section(
        chapter_id,
        lesson_id,
        (
            "summary",
            "lesson_summary",
            "review",
            "recap",
        ),
    )


def get_exam_notes(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return exam notes."""

    return _get_first_section(
        chapter_id,
        lesson_id,
        (
            "exam_notes",
            "exam_tips",
            "test_notes",
            "exam_points",
        ),
    )


def get_specialized_notes(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return specialized notes."""

    return _get_first_section(
        chapter_id,
        lesson_id,
        (
            "specialized_notes",
            "technical_notes",
            "expert_notes",
            "professional_notes",
        ),
    )


def get_examples(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return practical examples."""

    value = _get_first_section(
        chapter_id,
        lesson_id,
        (
            "examples",
            "practical_examples",
            "applications",
        ),
    )

    if isinstance(value, list):
        return _as_list(value)

    if value:
        return [value]

    return []


def get_references(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return references."""

    value = _get_first_section(
        chapter_id,
        lesson_id,
        (
            "references",
            "sources",
            "resources",
            "bibliography",
        ),
    )

    if isinstance(value, list):
        return _as_list(value)

    if value:
        return [value]

    return []


def get_keywords(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return lesson keywords."""

    value = _get_first_section(
        chapter_id,
        lesson_id,
        (
            "keywords",
            "key_words",
            "tags",
            "topics",
        ),
    )

    if isinstance(value, list):
        return _as_list(value)

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


# ==========================================================
# Quiz - Lesson
# ==========================================================

def get_quiz_questions(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return normalized lesson quiz questions.

    Special modes:
        chapter
        general
        all
        comprehensive
        banking
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

    return _normalize_questions(
        _get_lesson_questions(
            lesson
        )
    )


def get_quiz_question(
    chapter_id: str | int,
    lesson_id: str | int,
    question_index: int,
) -> dict[str, Any] | None:
    """Return one quiz question."""

    try:
        question_index = int(
            question_index
        )
    except (
        TypeError,
        ValueError,
    ):
        return None

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
    """Collect all questions belonging to a chapter."""

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return []

    result: list[
        dict[str, Any]
    ] = []

    chapter_id = str(
        chapter_id
    )

    for lesson in get_lessons(
        chapter_id
    ):

        lesson_id = _lesson_id(
            lesson
        )

        if not lesson_id:
            continue

        questions = _normalize_questions(
            _get_lesson_questions(
                lesson
            )
        )

        for question in questions:

            question["module_id"] = MODULE_ID
            question["chapter_id"] = chapter_id
            question["lesson_id"] = lesson_id
            question["chapter_title"] = (
                _chapter_title(chapter)
            )
            question["lesson_title"] = (
                _lesson_title(lesson)
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
    """Collect all available Banking questions."""

    result: list[
        dict[str, Any]
    ] = []

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

            questions = _normalize_questions(
                _get_lesson_questions(
                    lesson
                )
            )

            for question in questions:

                normalized = _copy(
                    question
                )

                normalized["module_id"] = MODULE_ID
                normalized["chapter_id"] = chapter_id
                normalized["lesson_id"] = lesson_id
                normalized["chapter_title"] = (
                    _chapter_title(chapter)
                )
                normalized["lesson_title"] = (
                    _lesson_title(lesson)
                )

                result.append(
                    normalized
                )

    return _unique_questions(
        result
    )


def get_quiz_pool(
    chapter_id: str | int | None = None,
    lesson_id: str | int | None = None,
) -> list[dict[str, Any]]:
    """Return a quiz pool according to scope."""

    if (
        chapter_id is not None
        and lesson_id is not None
    ):
        return get_quiz_questions(
            chapter_id,
            lesson_id,
        )

    if chapter_id is not None:
        return get_chapter_quiz_questions(
            chapter_id
        )

    return get_comprehensive_quiz_questions()


# ==========================================================
# Random Quiz
# ==========================================================

def get_random_quiz_questions(
    count: int = 10,
    chapter_id: str | int | None = None,
    lesson_id: str | int | None = None,
) -> list[dict[str, Any]]:
    """Return random Banking questions."""

    try:
        count = int(count)
    except (
        TypeError,
        ValueError,
    ):
        return []

    if count <= 0:
        return []

    pool = get_quiz_pool(
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    pool = _unique_questions(
        pool
    )

    if not pool:
        return []

    return _copy(
        random.sample(
            pool,
            min(
                count,
                len(pool),
            ),
        )
    )


def shuffle_quiz_questions(
    questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return a shuffled copy of questions."""

    result = _copy(
        questions
    )

    random.shuffle(
        result
    )

    return result


# ==========================================================
# Quiz Answer Validation
# ==========================================================

def check_quiz_answer(
    question: dict[str, Any],
    selected_index: int | str,
) -> dict[str, Any]:
    """
    Validate one quiz answer.

    selected_index may be:
        0, 1, 2, 3
        A, B, C, D
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
            "selected_option": None,
            "correct_option": None,
            "explanation": None,
            "question": "",
        }

    options = normalized.get(
        "options",
        []
    )

    correct_index = normalized.get(
        "correct_index"
    )

    selected_resolved = _letter_to_index(
        selected_index
    )

    if selected_resolved is None:

        selected_resolved = _find_option_index(
            options,
            selected_index,
        )

    if selected_resolved is None:

        return {
            "valid": False,
            "correct": False,
            "selected_index": selected_index,
            "correct_index": correct_index,
            "selected_option": None,
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
            "explanation": None,
            "question": normalized.get(
                "question",
                "",
            ),
        }

    if (
        selected_resolved < 0
        or selected_resolved >= len(
            options
        )
    ):

        return {
            "valid": False,
            "correct": False,
            "selected_index": selected_resolved,
            "correct_index": correct_index,
            "selected_option": None,
            "correct_option": None,
            "explanation": None,
            "question": normalized.get(
                "question",
                "",
            ),
        }

    correct = (
        correct_index is not None
        and selected_resolved == correct_index
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
        "selected_index": selected_resolved,
        "selected_letter": chr(
            ord("A") + selected_resolved
        ),
        "correct_index": correct_index,
        "correct_letter": (
            chr(
                ord("A") + correct_index
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
        "selected_option": _copy(
            options[selected_resolved]
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
    selected_index: int | str,
) -> bool:
    """Simple boolean answer check."""

    result = check_quiz_answer(
        question,
        selected_index,
    )

    return bool(
        result.get("valid")
        and result.get("correct")
    )


# ==========================================================
# Quiz Validation
# ==========================================================

def validate_quiz_question(
    question: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate the structure of one quiz question.
    """

    normalized = _normalize_question(
        question
    )

    if normalized is None:

        return {
            "valid": False,
            "reason": "question_not_dict",
        }

    text = normalized.get(
        "question",
        ""
    )

    options = normalized.get(
        "options",
        []
    )

    correct_index = normalized.get(
        "correct_index"
    )

    if not text:
        return {
            "valid": False,
            "reason": "empty_question",
            "question": normalized,
        }

    if len(options) < 2:
        return {
            "valid": False,
            "reason": "not_enough_options",
            "question": normalized,
        }

    if correct_index is None:
        return {
            "valid": False,
            "reason": "correct_answer_not_found",
            "question": normalized,
        }

    if not (
        0 <= correct_index < len(options)
    ):
        return {
            "valid": False,
            "reason": "correct_index_out_of_range",
            "question": normalized,
        }

    return {
        "valid": True,
        "reason": "ok",
        "question": normalized,
    }


def validate_quiz_questions(
    questions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate a complete question collection."""

    valid_count = 0
    invalid_count = 0
    invalid_questions: list[
        dict[str, Any]
    ] = []

    for index, question in enumerate(
        questions
    ):

        result = validate_quiz_question(
            question
        )

        if result.get("valid"):
            valid_count += 1
        else:
            invalid_count += 1

            invalid_questions.append(
                {
                    "index": index,
                    "reason": result.get(
                        "reason"
                    ),
                    "question": _copy(
                        question
                    ),
                }
            )

    return {
        "valid": invalid_count == 0,
        "total": len(questions),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "invalid_questions": invalid_questions,
    }


# ==========================================================
# Quiz Result
# ==========================================================

def calculate_quiz_score(
    correct_answers: int,
    total_questions: int,
) -> float:
    """Calculate percentage score."""

    try:
        return float(
            calculate_score(
                correct_answers=correct_answers,
                total_questions=total_questions,
            )
        )
    except Exception:
        if total_questions <= 0:
            return 0.0

        return round(
            correct_answers
            / total_questions
            * 100,
            2,
        )


def record_banking_quiz_result(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """Record Banking quiz result."""

    if score is None:
        score = calculate_quiz_score(
            correct_answers,
            total_questions,
        )

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


def record_banking_quiz_attempt(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> Any:
    """
    Compatibility wrapper around record_quiz_attempt.

    Used when the core statistics layer supports attempt-level
    recording.
    """

    if score is None:
        score = calculate_quiz_score(
            correct_answers,
            total_questions,
        )

    return record_quiz_attempt(
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


# ==========================================================
# Lesson Progress
# ==========================================================

def start_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Mark Banking lesson as started."""

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
    """Mark Banking lesson as completed."""

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
    """Return lesson progress."""

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
    """Check lesson completion."""

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
    """Return Banking chapter progress."""

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
    """Return complete Banking progress."""

    return get_module_progress(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_progress_percentage(
    telegram_id: int,
) -> float:
    """Return Banking completion percentage."""

    return float(
        get_progress_percentage(
            telegram_id=telegram_id,
            module_id=MODULE_ID,
        )
    )


def is_banking_completed(
    telegram_id: int,
) -> bool:
    """Return whether Banking is complete."""

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
    """Return Banking user statistics."""

    return get_user_statistics(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_module_statistics(
    telegram_id: int,
) -> dict[str, Any]:
    """Return Banking module statistics from core."""

    return get_module_statistics(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_statistics(
    telegram_id: int,
) -> dict[str, Any]:
    """Return complete Banking statistics."""

    progress = get_banking_progress(
        telegram_id
    )

    quiz = get_banking_user_statistics(
        telegram_id
    )

    curriculum = get_curriculum_statistics()

    chapters_progress = progress.get(
        "chapters",
        [],
    )

    chapters_completed = sum(
        1
        for chapter in chapters_progress
        if chapter.get(
            "completed",
            False,
        )
    )

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
            "chapters_completed": chapters_completed,
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
    """Return lesson quiz statistics."""

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
    """Return lesson attempts."""

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
    """Return combined chapter progress and quiz statistics."""

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
    """Return Banking quiz attempts."""

    return get_attempts(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )


def get_banking_latest_attempt(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return latest Banking attempt."""

    return get_latest_attempt(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_best_attempt(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return best Banking attempt."""

    return get_best_attempt(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
    )


def get_banking_recent_attempts(
    telegram_id: int,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return recent Banking attempts."""

    try:
        limit = int(limit)
    except (
        TypeError,
        ValueError,
    ):
        limit = 10

    return get_recent_attempts(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        limit=limit,
    )


# ==========================================================
# Curriculum Statistics
# ==========================================================

def get_curriculum_statistics() -> dict[str, int]:
    """Calculate Banking curriculum statistics."""

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


def get_chapter_curriculum_statistics(
    chapter_id: str | int,
) -> dict[str, int]:
    """Return curriculum statistics for one chapter."""

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return {
            "chapters": 0,
            "lessons": 0,
            "questions": 0,
        }

    lessons = get_lessons(
        chapter_id
    )

    questions = sum(
        len(
            get_quiz_questions(
                chapter_id,
                _lesson_id(lesson),
            )
        )
        for lesson in lessons
    )

    return {
        "chapters": 1,
        "lessons": len(lessons),
        "questions": questions,
    }


def statistics() -> dict[str, int]:
    """Compatibility alias."""

    return get_curriculum_statistics()


# ==========================================================
# Search
# ==========================================================

def _flatten_search_value(
    value: Any,
) -> str:
    """Convert arbitrary educational data into searchable text."""

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):

        return " ".join(
            _flatten_search_value(item)
            for item in value.values()
        )

    if isinstance(value, (list, tuple, set)):

        return " ".join(
            _flatten_search_value(item)
            for item in value
        )

    return str(value)


def search(
    query: str,
) -> list[dict[str, Any]]:
    """Search Banking curriculum deeply."""

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
                _flatten_search_value(
                    chapter
                ),
                lesson_title,
                _flatten_search_value(
                    lesson
                ),
            ]

            haystack = " ".join(
                searchable_parts
            ).casefold()

            if normalized_query in haystack:

                results.append(
                    {
                        "module_id": MODULE_ID,
                        "chapter_id": chapter_id,
                        "chapter_title": chapter_title,
                        "lesson_id": lesson_id,
                        "lesson_title": lesson_title,
                        "matched_query": query,
                    }
                )

    return results


def search_lessons(
    query: str,
) -> list[dict[str, Any]]:
    """Compatibility alias."""

    return search(
        query
    )


# ==========================================================
# User Learning Overview
# ==========================================================

def get_user_learning_overview(
    telegram_id: int,
) -> dict[str, Any]:
    """Return complete Banking learning overview."""

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
                "lessons": len(
                    get_lessons(
                        chapter_id
                    )
                ),
                "questions": len(
                    get_chapter_quiz_questions(
                        chapter_id
                    )
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
# Data Health Check
# ==========================================================

def data_health_check() -> bool:
    """
    Validate Banking data structure.

    Empty quizzes are allowed during curriculum expansion.
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

                questions = _normalize_questions(
                    _get_lesson_questions(
                        lesson
                    )
                )

                validation = (
                    validate_quiz_questions(
                        questions
                    )
                )

                if not validation.get(
                    "valid"
                ):

                    logger.error(
                        (
                            "Invalid Banking quiz "
                            "questions in chapter=%s "
                            "lesson=%s: %s"
                        ),
                        chapter_id,
                        lesson_id,
                        validation,
                    )

                    return False

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


# ==========================================================
# Service Health Check
# ==========================================================

def service_health_check() -> bool:
    """Validate the Banking service layer."""

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
    "get_next_chapter",
    "get_previous_chapter",

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
    "get_keywords",

    # Quiz
    "get_quiz_questions",
    "get_quiz_question",
    "get_question_count",
    "get_chapter_quiz_questions",
    "get_comprehensive_quiz_questions",
    "get_quiz_pool",
    "get_random_quiz_questions",
    "shuffle_quiz_questions",

    # Quiz validation
    "check_quiz_answer",
    "is_quiz_answer_correct",
    "validate_quiz_question",
    "validate_quiz_questions",

    # Quiz result
    "calculate_quiz_score",
    "record_banking_quiz_result",
    "save_quiz_result",
    "record_banking_quiz_attempt",

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
    "get_banking_module_statistics",
    "get_banking_lesson_statistics",
    "get_banking_lesson_attempts",
    "get_banking_chapter_statistics",
    "get_banking_attempts",
    "get_banking_latest_attempt",
    "get_banking_best_attempt",
    "get_banking_recent_attempts",

    # Curriculum
    "get_curriculum_statistics",
    "get_chapter_curriculum_statistics",
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
