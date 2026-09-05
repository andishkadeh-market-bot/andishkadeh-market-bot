"""
Finance Service Layer
Andishkadeh Management & Market

لایه سرویس مدیریت مالی

Responsibilities:
- Module information
- Chapters
- Lessons
- Lesson content
- Quiz questions
- Quiz normalization
- Quiz scoring
- Quiz attempts
- Search
- Statistics
- Validation
- Health check
- Compatibility APIs for handlers
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any, Dict, List, Optional

from . import data

try:
    from . import content
except Exception:
    content = None


logger = logging.getLogger(__name__)


# ============================================================
# Constants
# ============================================================

MODULE_ID = "finance"
DEFAULT_MODULE_TITLE = "💰 مدیریت مالی"

DEFAULT_MODULE_DESCRIPTION = (
    "دوره تخصصی مدیریت مالی شامل مبانی مالی، "
    "تحلیل صورت‌های مالی، تصمیم‌گیری مالی، "
    "بودجه‌بندی، سرمایه‌گذاری، تأمین مالی، "
    "مدیریت سرمایه در گردش و مدیریت ریسک."
)


# ============================================================
# Database
# ============================================================

try:
    from core.database import (
        save_quiz_attempt as db_save_quiz_attempt,
        get_quiz_attempts as db_get_quiz_attempts,
    )
except Exception:
    db_save_quiz_attempt = None
    db_get_quiz_attempts = None


# ============================================================
# Generic Helpers
# ============================================================

def _normalize_text(
    value: Any,
    default: str = "",
) -> str:
    if value is None:
        return default

    return str(value).strip()


def _normalize_list(
    value: Any,
) -> List[Any]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, set):
        return list(value)

    return [value]


def _safe_call(
    function_name: str,
    *args: Any,
    default: Any = None,
    **kwargs: Any,
) -> Any:
    function = getattr(
        data,
        function_name,
        None,
    )

    if not callable(function):
        return default

    try:
        return function(
            *args,
            **kwargs,
        )
    except Exception:
        logger.exception(
            "Finance data function failed: %s",
            function_name,
        )
        return default


def _safe_content_call(
    function_name: str,
    *args: Any,
    default: Any = None,
    **kwargs: Any,
) -> Any:
    if content is None:
        return default

    function = getattr(
        content,
        function_name,
        None,
    )

    if not callable(function):
        return default

    try:
        return function(
            *args,
            **kwargs,
        )
    except Exception:
        logger.exception(
            "Finance content function failed: %s",
            function_name,
        )
        return default


def _get_id(
    item: Any,
) -> str:
    if isinstance(item, dict):
        return _normalize_text(
            item.get("id")
            or item.get("chapter_id")
            or item.get("lesson_id")
            or item.get("key")
        )

    return _normalize_text(
        getattr(item, "id", None)
        or getattr(item, "chapter_id", None)
        or getattr(item, "lesson_id", None)
    )


def _get_title(
    item: Any,
) -> str:
    if isinstance(item, dict):
        return _normalize_text(
            item.get("title")
            or item.get("name")
            or item.get("chapter_title")
            or item.get("lesson_title")
        )

    return _normalize_text(
        getattr(item, "title", None)
        or getattr(item, "name", None)
    )


# ============================================================
# Quiz Normalization
# ============================================================

def _answer_to_index(
    value: Any,
    options: List[str],
) -> int:
    """
    Convert supported answer formats into zero-based index.

    Supported:
    - 0 / 1 / 2 / 3
    - "0" / "1" / "2" / "3"
    - A / B / C / D
    - a / b / c / d
    - الف / ب / ج / د
    - complete option text
    """

    if value is None:
        return 0

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        try:
            return int(value)
        except Exception:
            return 0

    text = _normalize_text(
        value
    )

    if not text:
        return 0

    english = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    if text.upper() in english:
        return english[text.upper()]

    persian = {
        "الف": 0,
        "ب": 1,
        "ج": 2,
        "د": 3,
    }

    if text in persian:
        return persian[text]

    try:
        return int(text)
    except Exception:
        pass

    normalized_text = text.casefold()

    for index, option in enumerate(options):
        if (
            _normalize_text(option).casefold()
            == normalized_text
        ):
            return index

    return 0


def _normalize_question(
    question: Any,
) -> Dict[str, Any]:
    """
    Normalize one Finance quiz question.
    """

    if not isinstance(
        question,
        dict,
    ):
        return {
            "id": "",
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

    result["id"] = _normalize_text(
        result.get("id")
        or result.get("question_id")
        or result.get("key")
    )

    result["question"] = _normalize_text(
        result.get("question")
        or result.get("text")
        or result.get("question_text")
        or result.get("title")
    )

    raw_options = (
        result.get("options")
        or result.get("choices")
        or result.get("answers")
        or result.get("variants")
        or []
    )

    options: List[str] = []

    for option in _normalize_list(
        raw_options
    ):
        if isinstance(
            option,
            dict,
        ):
            option = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or option.get("title")
                or ""
            )

        options.append(
            _normalize_text(
                option
            )
        )

    result["options"] = options

    raw_correct = None

    for key in (
        "correct_index",
        "answer_index",
        "correct_option",
        "correct_answer_index",
        "correct_answer",
        "answer",
    ):
        if key in result:
            value = result.get(key)

            if value is not None:
                raw_correct = value
                break

    result["correct_index"] = _answer_to_index(
        raw_correct,
        options,
    )

    result["explanation"] = _normalize_text(
        result.get("explanation")
        or result.get("answer_explanation")
        or result.get("solution")
        or result.get("solution_text")
        or result.get("reason")
    )

    return result


def _validate_questions(
    questions: Any,
) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []

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

        if not item.get("question"):
            continue

        if len(options) < 2:
            continue

        if not (
            0 <= correct_index < len(options)
        ):
            continue

        result.append(
            item
        )

    return result


# ============================================================
# Module Information
# ============================================================

def get_module_id() -> str:
    return MODULE_ID


def get_module_title() -> str:
    title = getattr(
        data,
        "MODULE_TITLE",
        None,
    )

    return _normalize_text(
        title,
        DEFAULT_MODULE_TITLE,
    )


def get_module_description() -> str:
    description = getattr(
        data,
        "MODULE_DESCRIPTION",
        None,
    )

    return _normalize_text(
        description,
        DEFAULT_MODULE_DESCRIPTION,
    )


def get_module_info() -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    raw_info = getattr(
        data,
        "get_module_info",
        None,
    )

    if callable(raw_info):
        try:
            value = raw_info()

            if isinstance(
                value,
                dict,
            ):
                result.update(
                    value
                )
        except Exception:
            logger.exception(
                "Unable to load Finance module info."
            )

    stats = get_curriculum_stats()

    result.setdefault(
        "module_id",
        MODULE_ID,
    )

    result.setdefault(
        "id",
        MODULE_ID,
    )

    result.setdefault(
        "title",
        get_module_title(),
    )

    result.setdefault(
        "description",
        get_module_description(),
    )

    result.setdefault(
        "chapter_count",
        stats["chapters"],
    )

    result.setdefault(
        "lesson_count",
        stats["lessons"],
    )

    result.setdefault(
        "quiz_count",
        stats["quiz_questions"],
    )

    return result


# ============================================================
# Chapters
# ============================================================

def get_finance_chapters() -> List[Dict[str, Any]]:
    chapters = _safe_call(
        "get_chapters",
        default=None,
    )

    if chapters is None:
        chapters = getattr(
            data,
            "CHAPTERS",
            None,
        )

    if chapters is None:
        chapters = getattr(
            data,
            "FINANCE_CHAPTERS",
            [],
        )

    result: List[Dict[str, Any]] = []

    for chapter in _normalize_list(
        chapters
    ):
        if isinstance(
            chapter,
            dict,
        ):
            item = dict(
                chapter
            )
        else:
            item = {
                "id": _get_id(chapter),
                "title": _get_title(chapter),
            }

        item["id"] = _normalize_text(
            item.get("id")
        )

        item["title"] = _normalize_text(
            item.get("title"),
            item["id"],
        )

        if item["id"]:
            result.append(
                item
            )

    return result


def get_finance_chapter(
    chapter_id: str,
) -> Optional[Dict[str, Any]]:
    chapter_id = _normalize_text(
        chapter_id
    )

    if not chapter_id:
        return None

    chapter = _safe_call(
        "get_chapter",
        chapter_id,
        default=None,
    )

    if chapter is not None:
        if isinstance(
            chapter,
            dict,
        ):
            result = dict(
                chapter
            )
        else:
            result = {
                "id": _get_id(chapter),
                "title": _get_title(chapter),
            }

        result["id"] = _normalize_text(
            result.get("id"),
            chapter_id,
        )

        result["title"] = _normalize_text(
            result.get("title"),
            result["id"],
        )

        return result

    for item in get_finance_chapters():
        if item.get("id") == chapter_id:
            return item

    return None


# ============================================================
# Lessons
# ============================================================

def get_finance_lessons(
    chapter_id: str,
) -> List[Dict[str, Any]]:
    chapter_id = _normalize_text(
        chapter_id
    )

    if not chapter_id:
        return []

    lessons = _safe_call(
        "get_lessons",
        chapter_id,
        default=None,
    )

    if lessons is None:
        lessons = _safe_call(
            "get_lessons",
            default=None,
        )

    if lessons is None:
        lessons = getattr(
            data,
            "LESSONS",
            None,
        )

    if lessons is None:
        lessons = getattr(
            data,
            "FINANCE_LESSONS",
            [],
        )

    result: List[Dict[str, Any]] = []

    if isinstance(
        lessons,
        dict,
    ):
        iterable = []

        for key, values in lessons.items():
            for lesson in _normalize_list(
                values
            ):
                if isinstance(
                    lesson,
                    dict,
                ):
                    item = dict(
                        lesson
                    )

                    item.setdefault(
                        "chapter_id",
                        key,
                    )

                    iterable.append(
                        item
                    )
                else:
                    iterable.append(
                        lesson
                    )
    else:
        iterable = _normalize_list(
            lessons
        )

    for lesson in iterable:
        if not isinstance(
            lesson,
            dict,
        ):
            continue

        item = dict(
            lesson
        )

        item["id"] = _normalize_text(
            item.get("id")
            or item.get("lesson_id")
        )

        item["title"] = _normalize_text(
            item.get("title")
            or item.get("name"),
            item["id"],
        )

        item["chapter_id"] = _normalize_text(
            item.get("chapter_id")
            or item.get("chapter")
            or item.get("parent_id")
        )

        if (
            item["chapter_id"]
            and item["chapter_id"] != chapter_id
        ):
            continue

        item["chapter_id"] = chapter_id

        if item["id"]:
            result.append(
                item
            )

    return result


def get_finance_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Optional[Dict[str, Any]]:
    chapter_id = _normalize_text(
        chapter_id
    )

    lesson_id = _normalize_text(
        lesson_id
    )

    if not chapter_id or not lesson_id:
        return None

    lesson = _safe_call(
        "get_lesson",
        chapter_id,
        lesson_id,
        default=None,
    )

    if lesson is not None:
        if isinstance(
            lesson,
            dict,
        ):
            result = dict(
                lesson
            )
        else:
            result = {
                "id": _get_id(lesson),
                "title": _get_title(lesson),
            }

        result["id"] = _normalize_text(
            result.get("id"),
            lesson_id,
        )

        result["chapter_id"] = _normalize_text(
            result.get("chapter_id"),
            chapter_id,
        )

        result["title"] = _normalize_text(
            result.get("title"),
            lesson_id,
        )

        return result

    for item in get_finance_lessons(
        chapter_id
    ):
        if item.get("id") == lesson_id:
            return item

    return None


# ============================================================
# Complete Lesson
# ============================================================

def get_complete_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Return a complete normalized lesson.

    Supports both data.py and content.py.
    """

    lesson = get_finance_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    result = dict(
        lesson
    )

    content_result = _safe_content_call(
        "get_lesson_content",
        chapter_id,
        lesson_id,
        default=None,
    )

    if content_result is None:
        content_result = _safe_content_call(
            "get_complete_lesson",
            chapter_id,
            lesson_id,
            default=None,
        )

    if isinstance(
        content_result,
        dict,
    ):
        result.update(
            content_result
        )

    elif content_result:
        result["lesson_text"] = _normalize_text(
            content_result
        )

    result.setdefault(
        "lesson_text",
        _normalize_text(
            result.get("content")
            or result.get("text")
            or result.get("body")
            or result.get("description")
        ),
    )

    result.setdefault(
        "detailed_content",
        _normalize_text(
            result.get("detailed_content")
            or result.get("content")
        ),
    )

    result.setdefault(
        "subtopics",
        _normalize_list(
            result.get("subtopics")
        ),
    )

    result.setdefault(
        "specialized_points",
        _normalize_list(
            result.get("specialized_points")
        ),
    )

    result.setdefault(
        "exam_points",
        _normalize_list(
            result.get("exam_points")
        ),
    )

    result.setdefault(
        "practical_example",
        result.get(
            "practical_example",
            [],
        ),
    )

    return result


# ============================================================
# Quiz
# ============================================================

def get_finance_quiz(
    chapter_id: str,
    lesson_id: str,
) -> List[Dict[str, Any]]:
    chapter_id = _normalize_text(
        chapter_id
    )

    lesson_id = _normalize_text(
        lesson_id
    )

    if not chapter_id or not lesson_id:
        return []

    questions = _safe_call(
        "get_quiz",
        chapter_id,
        lesson_id,
        default=None,
    )

    if questions is None:
        questions = _safe_call(
            "get_quiz_questions",
            chapter_id,
            lesson_id,
            default=None,
        )

    if questions is None:
        questions = _safe_content_call(
            "get_quiz",
            chapter_id,
            lesson_id,
            default=None,
        )

    if questions is None:
        lesson = get_finance_lesson(
            chapter_id,
            lesson_id,
        )

        if lesson:
            questions = (
                lesson.get("quiz")
                or lesson.get("questions")
                or lesson.get("quiz_questions")
                or []
            )

    return _validate_questions(
        questions
    )


def get_quiz_question(
    chapter_id: str,
    lesson_id: str,
    question_index: int,
) -> Optional[Dict[str, Any]]:
    questions = get_finance_quiz(
        chapter_id,
        lesson_id,
    )

    try:
        index = int(
            question_index
        )
    except Exception:
        return None

    if index < 0 or index >= len(questions):
        return None

    return questions[index]


def get_all_quiz_questions() -> List[Dict[str, Any]]:
    """
    Return every Finance quiz question.
    """

    direct = _safe_call(
        "get_all_quiz_questions",
        default=None,
    )

    if direct is not None:
        return _validate_questions(
            direct
        )

    result: List[
        Dict[str, Any]
    ] = []

    for chapter in get_finance_chapters():

        chapter_id = chapter.get(
            "id",
            "",
        )

        for lesson in get_finance_lessons(
            chapter_id
        ):

            lesson_id = lesson.get(
                "id",
                "",
            )

            result.extend(
                get_finance_quiz(
                    chapter_id,
                    lesson_id,
                )
            )

    return result


# Compatibility aliases

get_quiz = get_finance_quiz
get_finance_quiz_questions = get_finance_quiz


# ============================================================
# Quiz Scoring
# ============================================================

def calculate_quiz_result(
    questions: List[Dict[str, Any]],
    answers: List[Any],
) -> Dict[str, Any]:
    """
    Calculate quiz result.

    answers:
        zero-based indexes or supported answer formats.
    """

    normalized_questions = _validate_questions(
        questions
    )

    total = len(
        normalized_questions
    )

    if total == 0:
        return {
            "score": 0,
            "correct": 0,
            "wrong": 0,
            "total": 0,
            "percentage": 0,
        }

    correct = 0

    normalized_answers = _normalize_list(
        answers
    )

    for index, question in enumerate(
        normalized_questions
    ):

        if index >= len(
            normalized_answers
        ):
            continue

        selected_index = _answer_to_index(
            normalized_answers[index],
            question.get(
                "options",
                [],
            ),
        )

        if selected_index == question.get(
            "correct_index"
        ):
            correct += 1

    wrong = total - correct

    percentage = round(
        (correct / total) * 100,
        2,
    )

    return {
        "score": correct,
        "correct": correct,
        "wrong": wrong,
        "total": total,
        "percentage": percentage,
    }


# ============================================================
# Quiz Attempt Persistence
# ============================================================

def _save_attempt_to_database(
    user_id: Any,
    chapter_id: str,
    lesson_id: str,
    score: int,
    total: int,
    percentage: float,
) -> Any:
    if db_save_quiz_attempt is None:
        return None

    try:
        return db_save_quiz_attempt(
            user_id=user_id,
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            score=score,
            total=total,
            percentage=percentage,
        )
    except TypeError:
        try:
            return db_save_quiz_attempt(
                user_id,
                MODULE_ID,
                chapter_id,
                lesson_id,
                score,
                total,
                percentage,
            )
        except Exception:
            logger.exception(
                "Unable to save Finance quiz attempt."
            )
            return None

    except Exception:
        logger.exception(
            "Unable to save Finance quiz attempt."
        )
        return None


def complete_quiz_attempt(
    user_id: Any,
    chapter_id: str,
    lesson_id: str,
    answers: List[Any],
    questions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Calculate and persist a completed quiz attempt.
    """

    if questions is None:
        questions = get_finance_quiz(
            chapter_id,
            lesson_id,
        )

    result = calculate_quiz_result(
        questions,
        answers,
    )

    _save_attempt_to_database(
        user_id=user_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        score=result["score"],
        total=result["total"],
        percentage=result["percentage"],
    )

    result.update(
        {
            "module_id": MODULE_ID,
            "chapter_id": chapter_id,
            "lesson_id": lesson_id,
        }
    )

    return result


def get_finance_quiz_attempts(
    user_id: Any,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """
    Return previous Finance quiz attempts.
    """

    if db_get_quiz_attempts is None:
        return []

    try:
        attempts = db_get_quiz_attempts(
            user_id=user_id,
            module_id=MODULE_ID,
            limit=limit,
        )

    except TypeError:

        try:
            attempts = db_get_quiz_attempts(
                user_id,
                MODULE_ID,
                limit,
            )

        except Exception:
            logger.exception(
                "Unable to read Finance quiz attempts."
            )
            return []

    except Exception:
        logger.exception(
            "Unable to read Finance quiz attempts."
        )
        return []

    return _normalize_list(
        attempts
    )


# Compatibility alias

get_quiz_attempts = get_finance_quiz_attempts


# ============================================================
# Curriculum Statistics
# ============================================================

def get_total_lesson_count() -> int:
    total = 0

    for chapter in get_finance_chapters():
        total += len(
            get_finance_lessons(
                chapter.get("id", "")
            )
        )

    return total


def get_curriculum_stats() -> Dict[str, int]:
    chapters = get_finance_chapters()

    lesson_count = 0

    for chapter in chapters:
        lesson_count += len(
            get_finance_lessons(
                chapter.get("id", "")
            )
        )

    return {
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": len(
            get_all_quiz_questions()
        ),
    }


def get_finance_statistics() -> Dict[str, int]:
    return get_curriculum_stats()


def get_module_statistics() -> Dict[str, int]:
    return get_curriculum_stats()


# ============================================================
# Search
# ============================================================

def _search_text(
    value: Any,
) -> str:

    if value is None:
        return ""

    if isinstance(
        value,
        dict,
    ):
        return " ".join(
            _search_text(item)
            for item in value.values()
        )

    if isinstance(
        value,
        (list, tuple, set),
    ):
        return " ".join(
            _search_text(item)
            for item in value
        )

    return _normalize_text(
        value
    )


def search_finance(
    query: str,
) -> List[Dict[str, Any]]:
    term = _normalize_text(
        query
    ).casefold()

    if not term:
        return []

    results: List[
        Dict[str, Any]
    ] = []

    for chapter in get_finance_chapters():

        chapter_id = chapter.get(
            "id",
            "",
        )

        chapter_title = _normalize_text(
            chapter.get(
                "title"
            )
        )

        chapter_description = _normalize_text(
            chapter.get(
                "description"
            )
        )

        if (
            term in chapter_title.casefold()
            or term in chapter_description.casefold()
        ):
            results.append(
                {
                    "type": "chapter",
                    "chapter_id": chapter_id,
                    "title": chapter_title,
                    "description": chapter_description,
                }
            )

        for lesson in get_finance_lessons(
            chapter_id
        ):

            searchable = _search_text(
                lesson
            )

            if term not in searchable.casefold():
                continue

            results.append(
                {
                    "type": "lesson",
                    "chapter_id": chapter_id,
                    "lesson_id": lesson.get(
                        "id",
                        "",
                    ),
                    "title": lesson.get(
                        "title",
                        "",
                    ),
                    "content": lesson.get(
                        "content",
                        lesson.get(
                            "lesson_text",
                            "",
                        ),
                    ),
                }
            )

    return results


search = search_finance


# ============================================================
# Validation
# ============================================================

def validate_module() -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    try:
        chapters = get_finance_chapters()

        if not chapters:
            warnings.append(
                "No Finance chapters found."
            )

        chapter_ids = set()

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

            lessons = get_finance_lessons(
                chapter_id
            )

            if not lessons:
                warnings.append(
                    f"No lessons in chapter: {chapter_id}"
                )

            lesson_ids = set()

            for lesson in lessons:

                lesson_id = lesson.get(
                    "id",
                    "",
                )

                if not lesson_id:
                    errors.append(
                        f"Lesson without id: {chapter_id}"
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

                quiz = get_finance_quiz(
                    chapter_id,
                    lesson_id,
                )

                if not quiz:
                    warnings.append(
                        f"No quiz: "
                        f"{chapter_id}/{lesson_id}"
                    )

        return {
            "valid": not errors,
            "module": MODULE_ID,
            "errors": errors,
            "warnings": warnings,
            "statistics": get_curriculum_stats(),
        }

    except Exception as exc:

        logger.exception(
            "Finance validation failed."
        )

        return {
            "valid": False,
            "module": MODULE_ID,
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


# ============================================================
# Health Check
# ============================================================

def finance_health_check() -> bool:
    try:

        required = (
            get_module_id,
            get_module_title,
            get_module_description,
            get_module_info,
            get_finance_chapters,
            get_finance_chapter,
            get_finance_lessons,
            get_finance_lesson,
            get_complete_lesson,
            get_finance_quiz,
            get_quiz_question,
            calculate_quiz_result,
            complete_quiz_attempt,
            get_finance_quiz_attempts,
            get_curriculum_stats,
            search_finance,
            validate_module,
        )

        return all(
            callable(function)
            for function in required
        )

    except Exception:
        logger.exception(
            "Finance health check failed."
        )
        return False


service_health_check = finance_health_check
module_health_check = finance_health_check


# ============================================================
# Public API
# ============================================================

__all__ = [
    "MODULE_ID",

    "get_module_id",
    "get_module_title",
    "get_module_description",
    "get_module_info",

    "get_finance_chapters",
    "get_finance_chapter",

    "get_finance_lessons",
    "get_finance_lesson",
    "get_complete_lesson",

    "get_finance_quiz",
    "get_finance_quiz_questions",
    "get_quiz",
    "get_all_quiz_questions",
    "get_quiz_question",

    "calculate_quiz_result",
    "complete_quiz_attempt",

    "get_finance_quiz_attempts",
    "get_quiz_attempts",

    "get_total_lesson_count",
    "get_curriculum_stats",
    "get_finance_statistics",
    "get_module_statistics",

    "search_finance",
    "search",

    "validate_module",

    "finance_health_check",
    "service_health_check",
    "module_health_check",
]
