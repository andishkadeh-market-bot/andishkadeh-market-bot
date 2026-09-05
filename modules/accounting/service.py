"""
Accounting Service Layer
Andishkadeh Management & Market

ماژول خدمات حسابداری
--------------------

وظایف:
- اتصال امن handlers به data
- مدیریت فصل‌ها و درس‌ها
- دریافت محتوای آموزشی
- دریافت نکات تخصصی و آزمونی
- مدیریت مثال‌ها و کلیدواژه‌ها
- مدیریت آزمون‌های درس، فصل و جامع
- نرمال‌سازی ساختار داده‌ها
- پشتیبانی از پاسخ‌های A/B/C/D و متن گزینه
- جست‌وجوی محتوای حسابداری
- محاسبه آمار و وضعیت دوره
- سازگاری با نسخه‌های مختلف data.py
- جلوگیری از خطای Runtime در صورت ناقص بودن داده‌ها

ساختار آموزشی:
درسنامه
→ زیرموضوع‌ها
→ آموزش مفصل
→ نکات تخصصی
→ نکات آزمونی
→ مثال کاربردی
→ آزمون
→ نتیجه
→ مرور
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

MODULE_KEY = "accounting"

DEFAULT_TITLE = "📒 حسابداری تخصصی"

DEFAULT_DESCRIPTION = (
    "دوره جامع و تخصصی حسابداری با تمرکز بر حسابداری مالی، "
    "حسابداری مدیریت، حسابداری صنعتی، گزارشگری مالی، "
    "تحلیل صورت‌های مالی، مالیات، حسابرسی، استانداردهای "
    "حسابداری، کنترل داخلی و کاربردهای حرفه‌ای حسابداری."
)


# ==========================================================
# Safe Data Access
# ==========================================================

def _data_value(
    name: str,
    default: Any = None,
) -> Any:
    """Safely retrieve an attribute from data.py."""

    try:
        return getattr(
            data,
            name,
            default,
        )

    except Exception:
        logger.exception(
            "Unable to read data attribute: %s",
            name,
        )
        return default


def _call_data_function(
    function_name: str,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Safely call an optional data.py function."""

    function = _data_value(
        function_name,
        None,
    )

    if not callable(function):
        return None

    try:
        return function(
            *args,
            **kwargs,
        )

    except Exception:
        logger.exception(
            "Data function failed: %s",
            function_name,
        )
        return None


# ==========================================================
# Normalization Helpers
# ==========================================================

def _normalize_id(
    value: Any,
) -> str:
    """Normalize identifiers."""

    if value is None:
        return ""

    return str(value).strip()


def _normalize_text(
    value: Any,
) -> str:
    """Normalize text values."""

    if value is None:
        return ""

    return str(value).strip()


def _normalize_list(
    value: Any,
) -> list[Any]:
    """Return a safe list."""

    if value is None:
        return []

    if isinstance(
        value,
        list,
    ):
        return value

    if isinstance(
        value,
        tuple,
    ):
        return list(value)

    return [value]


def _normalize_chapter(
    chapter: Any,
) -> dict[str, Any]:
    """Normalize a chapter object."""

    if not isinstance(
        chapter,
        dict,
    ):
        return {
            "id": "",
            "title": _normalize_text(
                chapter
            ),
            "description": "",
            "lessons": [],
        }

    result = deepcopy(
        chapter
    )

    chapter_id = (
        result.get("id")
        or result.get("chapter_id")
        or result.get("key")
        or ""
    )

    result["id"] = _normalize_id(
        chapter_id
    )

    result["title"] = _normalize_text(
        result.get(
            "title",
            result["id"],
        )
    )

    result["description"] = _normalize_text(
        result.get(
            "description",
            "",
        )
    )

    result["lessons"] = _normalize_list(
        result.get(
            "lessons",
            [],
        )
    )

    return result


def _normalize_lesson(
    lesson: Any,
) -> dict[str, Any]:
    """Normalize a lesson object."""

    if not isinstance(
        lesson,
        dict,
    ):
        return {
            "id": "",
            "title": _normalize_text(
                lesson
            ),
            "content": "",
            "subtopics": [],
            "specialized_tips": [],
            "exam_tips": [],
            "examples": [],
            "keywords": [],
            "quiz": [],
        }

    result = deepcopy(
        lesson
    )

    lesson_id = (
        result.get("id")
        or result.get("lesson_id")
        or result.get("key")
        or ""
    )

    result["id"] = _normalize_id(
        lesson_id
    )

    result["title"] = _normalize_text(
        result.get(
            "title",
            result["id"],
        )
    )

    # ------------------------------------------------------
    # Content aliases
    # ------------------------------------------------------

    content = (
        result.get("content")
        or result.get("text")
        or result.get("description")
        or result.get("body")
        or result.get("lesson_content")
        or result.get("details")
        or result.get("explanation")
        or result.get("article")
        or ""
    )

    result["content"] = _normalize_text(
        content
    )

    # ------------------------------------------------------
    # Educational sections
    # ------------------------------------------------------

    result["subtopics"] = _normalize_list(
        result.get(
            "subtopics",
            result.get(
                "topics",
                result.get(
                    "sub_topics",
                    [],
                ),
            ),
        )
    )

    result["specialized_tips"] = _normalize_list(
        result.get(
            "specialized_tips",
            result.get(
                "professional_tips",
                result.get(
                    "advanced_tips",
                    [],
                ),
            ),
        )
    )

    result["exam_tips"] = _normalize_list(
        result.get(
            "exam_tips",
            result.get(
                "test_tips",
                result.get(
                    "exam_points",
                    [],
                ),
            ),
        )
    )

    result["examples"] = _normalize_list(
        result.get(
            "examples",
            result.get(
                "practical_examples",
                [],
            ),
        )
    )

    result["keywords"] = _normalize_list(
        result.get(
            "keywords",
            result.get(
                "key_terms",
                [],
            ),
        )
    )

    result["quiz"] = _normalize_list(
        result.get(
            "quiz",
            result.get(
                "questions",
                result.get(
                    "quiz_questions",
                    [],
                ),
            ),
        )
    )

    return result


# ==========================================================
# Quiz Answer Normalization
# ==========================================================

def _answer_to_index(
    value: Any,
    options: list[str],
) -> int:
    """
    Convert any supported answer representation
    to a zero-based option index.

    Supported:
    - 0, 1, 2, 3
    - "0", "1", "2", "3"
    - A, B, C, D
    - a, b, c, d
    - الف، ب، ج، د
    - full option text
    """

    if value is None:
        return 0

    # ------------------------------------------------------
    # Boolean
    # ------------------------------------------------------

    if isinstance(
        value,
        bool,
    ):
        return int(value)

    # ------------------------------------------------------
    # Integer / float
    # ------------------------------------------------------

    if isinstance(
        value,
        int,
    ):
        return value

    if isinstance(
        value,
        float,
    ):
        try:
            return int(value)

        except Exception:
            return 0

    # ------------------------------------------------------
    # String
    # ------------------------------------------------------

    text = _normalize_text(
        value
    )

    if not text:
        return 0

    upper = text.upper()

    english_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    if upper in english_map:
        return english_map[upper]

    persian_map = {
        "الف": 0,
        "ب": 1,
        "ج": 2,
        "د": 3,
    }

    if text in persian_map:
        return persian_map[text]

    # ------------------------------------------------------
    # Numeric string
    # ------------------------------------------------------

    try:
        return int(text)

    except Exception:
        pass

    # ------------------------------------------------------
    # Full option text
    # ------------------------------------------------------

    normalized_text = text.casefold()

    for index, option in enumerate(options):

        if (
            _normalize_text(option).casefold()
            == normalized_text
        ):
            return index

    # ------------------------------------------------------
    # Common labels
    # ------------------------------------------------------

    for index, option in enumerate(options):

        option_text = _normalize_text(
            option
        )

        if not option_text:
            continue

        if normalized_text in option_text.casefold():
            return index

    return 0


def _normalize_question(
    question: Any,
) -> dict[str, Any]:
    """
    Normalize one quiz question.

    Output guarantees:
    - question
    - options
    - correct_index
    - explanation
    """

    if not isinstance(
        question,
        dict,
    ):
        return {
            "question": _normalize_text(
                question
            ),
            "options": [],
            "correct_index": 0,
            "explanation": "",
        }

    result = deepcopy(
        question
    )

    # ------------------------------------------------------
    # Question text
    # ------------------------------------------------------

    result["question"] = _normalize_text(
        result.get(
            "question",
            result.get(
                "text",
                result.get(
                    "question_text",
                    result.get(
                        "title",
                        "",
                    ),
                ),
            ),
        )
    )

    # ------------------------------------------------------
    # Options
    # ------------------------------------------------------

    options = (
        result.get("options")
        or result.get("choices")
        or result.get("answers")
        or result.get("variants")
        or []
    )

    normalized_options: list[str] = []

    for option in _normalize_list(
        options
    ):

        if isinstance(
            option,
            dict,
        ):

            option_text = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or option.get("title")
                or ""
            )

        else:
            option_text = option

        normalized_options.append(
            _normalize_text(
                option_text
            )
        )

    result["options"] = normalized_options

    # ------------------------------------------------------
    # Correct answer aliases
    # ------------------------------------------------------

    raw_correct = None

    for key in (
        "correct_index",
        "answer_index",
        "correct_option",
        "correct_answer_index",
        "correct_answer",
        "answer",
        "solution",
    ):

        if key in result:

            value = result.get(
                key
            )

            if value is not None:
                raw_correct = value
                break

    if raw_correct is None:
        raw_correct = 0

    result["correct_index"] = _answer_to_index(
        raw_correct,
        normalized_options,
    )

    # ------------------------------------------------------
    # Explanation
    # ------------------------------------------------------

    result["explanation"] = _normalize_text(
        result.get(
            "explanation",
            result.get(
                "answer_explanation",
                result.get(
                    "solution_text",
                    result.get(
                        "reason",
                        "",
                    ),
                ),
            ),
        )
    )

    return result


# ==========================================================
# Module Information
# ==========================================================

def get_module_id() -> str:
    """Return accounting module id."""

    value = (
        _data_value(
            "MODULE_ID",
            None,
        )
        or _data_value(
            "MODULE_KEY",
            None,
        )
        or MODULE_KEY
    )

    return _normalize_text(
        value
    ) or MODULE_KEY


def get_module_title() -> str:
    """Return accounting module title."""

    title = _data_value(
        "MODULE_TITLE",
        _data_value(
            "ACCOUNTING_TITLE",
            DEFAULT_TITLE,
        ),
    )

    return (
        _normalize_text(title)
        or DEFAULT_TITLE
    )


def get_module_description() -> str:
    """Return accounting module description."""

    description = _data_value(
        "MODULE_DESCRIPTION",
        _data_value(
            "ACCOUNTING_DESCRIPTION",
            DEFAULT_DESCRIPTION,
        ),
    )

    return (
        _normalize_text(description)
        or DEFAULT_DESCRIPTION
    )


def get_module_info() -> dict[str, str]:
    """Return complete module information."""

    return {
        "id": get_module_id(),
        "key": MODULE_KEY,
        "title": get_module_title(),
        "description": get_module_description(),
    }


# ==========================================================
# Chapters
# ==========================================================

def get_accounting_chapters() -> list[dict[str, Any]]:
    """Return normalized accounting chapters."""

    chapters = _call_data_function(
        "get_accounting_chapters"
    )

    if chapters is None:
        chapters = _call_data_function(
            "get_chapters"
        )

    if chapters is None:
        chapters = _data_value(
            "CHAPTERS",
            _data_value(
                "ACCOUNTING_CHAPTERS",
                _data_value(
                    "ACCOUNTING_CURRICULUM",
                    [],
                ),
            ),
        )

    normalized: list[dict[str, Any]] = []

    for chapter in _normalize_list(
        chapters
    ):

        item = _normalize_chapter(
            chapter
        )

        if item["id"]:
            normalized.append(
                item
            )

    return normalized


def get_accounting_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return one accounting chapter."""

    target = _normalize_id(
        chapter_id
    )

    if not target:
        return None

    result = _call_data_function(
        "get_accounting_chapter",
        target,
    )

    if result is None:
        result = _call_data_function(
            "get_chapter",
            target,
        )

    if result is not None:

        normalized = _normalize_chapter(
            result
        )

        if normalized["id"]:
            return normalized

    for chapter in get_accounting_chapters():

        if chapter["id"] == target:
            return chapter

    return None


# Compatibility aliases

get_chapters = get_accounting_chapters
get_chapter = get_accounting_chapter


# ==========================================================
# Lessons
# ==========================================================

def get_accounting_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return lessons belonging to a chapter."""

    target = _normalize_id(
        chapter_id
    )

    if not target:
        return []

    lessons = _call_data_function(
        "get_accounting_lessons",
        target,
    )

    if lessons is None:
        lessons = _call_data_function(
            "get_lessons",
            target,
        )

    if lessons is None:

        chapter = get_accounting_chapter(
            target
        )

        if chapter is not None:
            lessons = chapter.get(
                "lessons",
                [],
            )

    normalized: list[dict[str, Any]] = []

    for lesson in _normalize_list(
        lessons
    ):

        item = _normalize_lesson(
            lesson
        )

        if item["id"]:
            normalized.append(
                item
            )

    return normalized


def get_accounting_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return one accounting lesson."""

    target_chapter = _normalize_id(
        chapter_id
    )

    target_lesson = _normalize_id(
        lesson_id
    )

    if not target_chapter or not target_lesson:
        return None

    result = _call_data_function(
        "get_accounting_lesson",
        target_chapter,
        target_lesson,
    )

    if result is None:
        result = _call_data_function(
            "get_lesson",
            target_chapter,
            target_lesson,
        )

    if result is not None:

        normalized = _normalize_lesson(
            result
        )

        if normalized["id"]:
            return normalized

    for lesson in get_accounting_lessons(
        target_chapter
    ):

        if lesson["id"] == target_lesson:
            return lesson

    return None


# Compatibility aliases

get_lessons = get_accounting_lessons
get_lesson = get_accounting_lesson


# ==========================================================
# Lesson Content
# ==========================================================

def get_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> str:
    """Return detailed lesson content."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return ""

    return _normalize_text(
        lesson.get(
            "content",
            "",
        )
    )


def get_lesson_subtopics(
    chapter_id: str,
    lesson_id: str,
) -> list[Any]:
    """Return lesson subtopics."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _normalize_list(
        lesson.get(
            "subtopics",
            [],
        )
    )


def get_lesson_specialized_tips(
    chapter_id: str,
    lesson_id: str,
) -> list[Any]:
    """Return professional tips."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _normalize_list(
        lesson.get(
            "specialized_tips",
            [],
        )
    )


def get_lesson_exam_tips(
    chapter_id: str,
    lesson_id: str,
) -> list[Any]:
    """Return exam tips."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _normalize_list(
        lesson.get(
            "exam_tips",
            [],
        )
    )


def get_lesson_examples(
    chapter_id: str,
    lesson_id: str,
) -> list[Any]:
    """Return practical examples."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _normalize_list(
        lesson.get(
            "examples",
            [],
        )
    )


def get_lesson_keywords(
    chapter_id: str,
    lesson_id: str,
) -> list[Any]:
    """Return professional keywords."""

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    return _normalize_list(
        lesson.get(
            "keywords",
            [],
        )
    )


# ==========================================================
# Quiz
# ==========================================================

def _validate_questions(
    questions: Any,
) -> list[dict[str, Any]]:
    """Normalize and validate quiz questions."""

    normalized: list[dict[str, Any]] = []

    for question in _normalize_list(
        questions
    ):

        item = _normalize_question(
            question
        )

        options = item.get(
            "options",
            [],
        )

        correct_index = item.get(
            "correct_index",
            -1,
        )

        if not item.get(
            "question"
        ):
            continue

        if len(options) < 2:
            continue

        if not (
            0
            <= correct_index
            < len(options)
        ):
            continue

        normalized.append(
            item
        )

    return normalized


def get_accounting_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return quiz questions for one lesson."""

    target_chapter = _normalize_id(
        chapter_id
    )

    target_lesson = _normalize_id(
        lesson_id
    )

    if not target_chapter or not target_lesson:
        return []

    questions = _call_data_function(
        "get_accounting_quiz",
        target_chapter,
        target_lesson,
    )

    if questions is None:
        questions = _call_data_function(
            "get_quiz",
            target_chapter,
            target_lesson,
        )

    if questions is None:

        lesson = get_accounting_lesson(
            target_chapter,
            target_lesson,
        )

        if lesson is not None:
            questions = lesson.get(
                "quiz",
                [],
            )

    return _validate_questions(
        questions
    )


def get_accounting_chapter_quiz(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return all quiz questions in a chapter."""

    target = _normalize_id(
        chapter_id
    )

    if not target:
        return []

    questions: list[
        dict[str, Any]
    ] = []

    for lesson in get_accounting_lessons(
        target
    ):

        lesson_id = lesson.get(
            "id",
            "",
        )

        if not lesson_id:
            continue

        questions.extend(
            get_accounting_quiz(
                target,
                lesson_id,
            )
        )

    return questions


def get_all_quiz_questions() -> list[dict[str, Any]]:
    """Return all accounting quiz questions."""

    result = _call_data_function(
        "get_all_quiz_questions"
    )

    if result is not None:
        return _validate_questions(
            result
        )

    result = _call_data_function(
        "get_all_quizzes"
    )

    if result is not None:
        return _validate_questions(
            result
        )

    questions: list[
        dict[str, Any]
    ] = []

    for chapter in get_accounting_chapters():

        chapter_id = chapter.get(
            "id",
            "",
        )

        if not chapter_id:
            continue

        questions.extend(
            get_accounting_chapter_quiz(
                chapter_id
            )
        )

    return questions


# Compatibility aliases

get_quiz = get_accounting_quiz
get_chapter_quiz = get_accounting_chapter_quiz
get_quiz_questions = get_accounting_quiz


# ==========================================================
# Quiz Statistics
# ==========================================================

def get_quiz_question_count() -> int:
    """Return total valid quiz questions."""

    return len(
        get_all_quiz_questions()
    )


def get_chapter_quiz_question_count(
    chapter_id: str,
) -> int:
    """Return valid question count for a chapter."""

    return len(
        get_accounting_chapter_quiz(
            chapter_id
        )
    )


def get_lesson_quiz_question_count(
    chapter_id: str,
    lesson_id: str,
) -> int:
    """Return valid question count for a lesson."""

    return len(
        get_accounting_quiz(
            chapter_id,
            lesson_id,
        )
    )


# ==========================================================
# Curriculum Statistics
# ==========================================================

def get_curriculum_stats() -> dict[str, int]:
    """Return accounting curriculum statistics."""

    chapters = get_accounting_chapters()

    lesson_count = 0

    for chapter in chapters:

        chapter_id = chapter.get(
            "id",
            "",
        )

        lesson_count += len(
            get_accounting_lessons(
                chapter_id
            )
        )

    return {
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": get_quiz_question_count(),
    }


def get_module_statistics() -> dict[str, int]:
    """Compatibility alias for curriculum statistics."""

    return get_curriculum_stats()


get_accounting_statistics = get_curriculum_stats


# ==========================================================
# Search
# ==========================================================

def _searchable_value(
    value: Any,
) -> str:
    """Convert arbitrary educational data into searchable text."""

    if value is None:
        return ""

    if isinstance(
        value,
        dict,
    ):

        parts: list[str] = []

        for key in (
            "title",
            "text",
            "description",
            "content",
            "name",
            "label",
            "answer",
        ):

            if key in value:
                parts.append(
                    _normalize_text(
                        value.get(key)
                    )
                )

        return " ".join(
            part
            for part in parts
            if part
        )

    if isinstance(
        value,
        (list, tuple),
    ):

        return " ".join(
            _searchable_value(item)
            for item in value
        )

    return _normalize_text(
        value
    )


def search_accounting(
    query: str,
) -> list[dict[str, Any]]:
    """
    Search across chapters, lessons,
    content, examples, tips and keywords.
    """

    search_term = _normalize_text(
        query
    ).casefold()

    if not search_term:
        return []

    results: list[
        dict[str, Any]
    ] = []

    for chapter in get_accounting_chapters():

        chapter_id = chapter.get(
            "id",
            "",
        )

        chapter_title = _normalize_text(
            chapter.get(
                "title",
                "",
            )
        )

        chapter_description = _normalize_text(
            chapter.get(
                "description",
                "",
            )
        )

        if (
            search_term in chapter_title.casefold()
            or search_term in chapter_description.casefold()
        ):

            results.append(
                {
                    "type": "chapter",
                    "chapter_id": chapter_id,
                    "title": chapter_title,
                    "description": chapter_description,
                }
            )

        for lesson in get_accounting_lessons(
            chapter_id
        ):

            lesson_id = lesson.get(
                "id",
                "",
            )

            title = _normalize_text(
                lesson.get(
                    "title",
                    "",
                )
            )

            content = _normalize_text(
                lesson.get(
                    "content",
                    "",
                )
            )

            searchable_sections = [
                title,
                content,
            ]

            for section_key in (
                "subtopics",
                "specialized_tips",
                "exam_tips",
                "examples",
                "keywords",
            ):

                searchable_sections.append(
                    _searchable_value(
                        lesson.get(
                            section_key,
                            [],
                        )
                    )
                )

            if any(
                search_term in section.casefold()
                for section in searchable_sections
                if section
            ):

                results.append(
                    {
                        "type": "lesson",
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "title": title,
                        "content": content,
                    }
                )

    return results


# Compatibility alias

search = search_accounting


# ==========================================================
# Validation
# ==========================================================

def validate_module() -> dict[str, Any]:
    """
    Validate accounting curriculum structure.

    This function reports problems without crashing
    the application.
    """

    errors: list[str] = []
    warnings: list[str] = []

    try:

        chapters = get_accounting_chapters()

        if not chapters:
            warnings.append(
                "No accounting chapters found."
            )

        chapter_ids: set[str] = set()

        for chapter in chapters:

            chapter_id = chapter.get(
                "id",
                "",
            )

            if not chapter_id:
                errors.append(
                    "Chapter without id."
                )
                continue

            if chapter_id in chapter_ids:
                errors.append(
                    f"Duplicate chapter id: {chapter_id}"
                )

            chapter_ids.add(
                chapter_id
            )

            lessons = get_accounting_lessons(
                chapter_id
            )

            if not lessons:
                warnings.append(
                    f"Chapter has no lessons: {chapter_id}"
                )

            lesson_ids: set[str] = set()

            for lesson in lessons:

                lesson_id = lesson.get(
                    "id",
                    "",
                )

                if not lesson_id:
                    errors.append(
                        f"Lesson without id in chapter: {chapter_id}"
                    )
                    continue

                if lesson_id in lesson_ids:
                    errors.append(
                        f"Duplicate lesson id: "
                        f"{chapter_id}/{lesson_id}"
                    )

                lesson_ids.add(
                    lesson_id
                )

                quiz = get_accounting_quiz(
                    chapter_id,
                    lesson_id,
                )

                if not quiz:
                    warnings.append(
                        f"Lesson has no valid quiz: "
                        f"{chapter_id}/{lesson_id}"
                    )

        return {
            "valid": not errors,
            "module": MODULE_KEY,
            "errors": errors,
            "warnings": warnings,
            "statistics": get_curriculum_stats(),
        }

    except Exception as exc:

        logger.exception(
            "Accounting module validation failed."
        )

        return {
            "valid": False,
            "module": MODULE_KEY,
            "errors": [
                str(exc)
            ],
            "warnings": warnings,
            "statistics": {
                "chapters": 0,
                "lessons": 0,
                "quiz_questions": 0,
            },
        }


# ==========================================================
# Module Health
# ==========================================================

def accounting_health_check() -> bool:
    """
    Validate the accounting service layer.

    Empty curriculum is not considered a Runtime failure.
    """

    try:

        required = (
            get_module_id,
            get_module_title,
            get_module_description,
            get_module_info,
            get_accounting_chapters,
            get_accounting_chapter,
            get_accounting_lessons,
            get_accounting_lesson,
            get_accounting_quiz,
            get_accounting_chapter_quiz,
            get_all_quiz_questions,
            get_curriculum_stats,
            search_accounting,
            validate_module,
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


# Compatibility aliases

service_health_check = accounting_health_check
module_health_check = accounting_health_check


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MODULE_KEY",

    "get_module_id",
    "get_module_title",
    "get_module_description",
    "get_module_info",

    "get_accounting_chapters",
    "get_accounting_chapter",
    "get_chapters",
    "get_chapter",

    "get_accounting_lessons",
    "get_accounting_lesson",
    "get_lessons",
    "get_lesson",

    "get_lesson_content",
    "get_lesson_subtopics",
    "get_lesson_specialized_tips",
    "get_lesson_exam_tips",
    "get_lesson_examples",
    "get_lesson_keywords",

    "get_accounting_quiz",
    "get_accounting_chapter_quiz",
    "get_all_quiz_questions",
    "get_quiz",
    "get_chapter_quiz",
    "get_quiz_questions",

    "get_quiz_question_count",
    "get_chapter_quiz_question_count",
    "get_lesson_quiz_question_count",

    "get_curriculum_stats",
    "get_module_statistics",
    "get_accounting_statistics",

    "search_accounting",
    "search",

    "validate_module",

    "accounting_health_check",
    "service_health_check",
    "module_health_check",
]
