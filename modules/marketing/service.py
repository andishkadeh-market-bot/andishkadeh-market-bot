"""
Professional Marketing Service Layer
Andishkadeh Management & Market
Responsibilities:
- Module information
- Chapter management
- Lesson management
- Lesson content
- Quiz questions
- Quiz normalization
- Search
- Curriculum statistics
- Curriculum validation
- Health check
Data source:
    modules.marketing.data
This service layer is independent from Telegram handlers.
"""
from __future__ import annotations
from copy import deepcopy
from typing import Any, Mapping
from modules.marketing.data import (
    MODULE_ID,
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    get_chapters,
    get_chapter,
    get_lessons,
    get_lesson,
    get_quiz_questions,
)
# ==========================================================
# Generic Helpers
# ==========================================================
def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
def _id(value: Any) -> str:
    return _text(value)
def _list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if value is None:
        return []
    return [value]
# ==========================================================
# Module Information
# ==========================================================
def get_module_id() -> str:
    return str(MODULE_ID)
def get_module_title() -> str:
    return str(MODULE_TITLE)
def get_module_info() -> dict[str, Any]:
    return {
        "id": get_module_id(),
        "module_id": get_module_id(),
        "title": get_module_title(),
        "description": str(MODULE_DESCRIPTION),
    }
# ==========================================================
# Chapters
# ==========================================================
def get_marketing_chapters() -> list[dict[str, Any]]:
    try:
        chapters = get_chapters()
    except Exception:
        return []
    if not isinstance(chapters, list):
        return []
    result: list[dict[str, Any]] = []
    for chapter in chapters:
        if not isinstance(chapter, Mapping):
            continue
        item = deepcopy(dict(chapter))
        chapter_id = (
            item.get("id")
            or item.get("chapter_id")
            or item.get("key")
            or ""
        )
        item["id"] = _id(chapter_id)
        item["chapter_id"] = item["id"]
        if not item["id"]:
            continue
        item["title"] = _text(
            item.get("title")
            or item.get("name")
            or item["id"]
        )
        result.append(item)
    return result
def get_marketing_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    target = _id(chapter_id)
    if not target:
        return None
    try:
        chapter = get_chapter(target)
    except Exception:
        chapter = None
    if isinstance(chapter, Mapping):
        result = deepcopy(dict(chapter))
        result["id"] = _id(
            result.get("id")
            or result.get("chapter_id")
            or target
        )
        result["chapter_id"] = result["id"]
        return result
    # Fallback to normalized chapter collection.
    for chapter in get_marketing_chapters():
        if chapter.get("id") == target:
            return deepcopy(chapter)
    return None
def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:
    return get_marketing_chapter(chapter_id)
def get_marketing_chapter_ids() -> list[str]:
    return [
        chapter["id"]
        for chapter in get_marketing_chapters()
        if chapter.get("id")
    ]
# ==========================================================
# Lessons
# ==========================================================
def get_marketing_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    target = _id(chapter_id)
    if not target:
        return []
    try:
        lessons = get_lessons(target)
    except Exception:
        return []
    if not isinstance(lessons, list):
        return []
    result: list[dict[str, Any]] = []
    for lesson in lessons:
        if not isinstance(lesson, Mapping):
            continue
        item = deepcopy(dict(lesson))
        lesson_id = (
            item.get("id")
            or item.get("lesson_id")
            or item.get("key")
            or ""
        )
        item["id"] = _id(lesson_id)
        item["lesson_id"] = item["id"]
        item["chapter_id"] = target
        if not item["id"]:
            continue
        item["title"] = _text(
            item.get("title")
            or item.get("name")
            or item["id"]
        )
        result.append(item)
    return result
def get_marketing_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    chapter = _id(chapter_id)
    lesson = _id(lesson_id)
    if not chapter or not lesson:
        return None
    try:
        result = get_lesson(
            chapter,
            lesson,
        )
    except Exception:
        result = None
    if isinstance(result, Mapping):
        item = deepcopy(dict(result))
        item["id"] = _id(
            item.get("id")
            or item.get("lesson_id")
            or lesson
        )
        item["lesson_id"] = item["id"]
        item["chapter_id"] = chapter
        return item
    # Fallback.
    for item in get_marketing_lessons(chapter):
        if item.get("id") == lesson:
            return deepcopy(item)
    return None
def get_lesson_by_id(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    return get_marketing_lesson(
        chapter_id,
        lesson_id,
    )
def get_marketing_lesson_ids(
    chapter_id: str,
) -> list[str]:
    return [
        lesson["id"]
        for lesson in get_marketing_lessons(
            chapter_id
        )
        if lesson.get("id")
    ]
# ==========================================================
# Lesson Content
# ==========================================================
def get_marketing_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    lesson = get_marketing_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    return deepcopy(lesson)
def get_marketing_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    lesson = get_marketing_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    content_keys = (
        "content",
        "text",
        "description",
        "lesson_content",
        "body",
        "details",
        "summary",
    )
    for key in content_keys:
        value = lesson.get(key)
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                return cleaned
    return None
def get_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    return get_marketing_lesson_content(
        chapter_id,
        lesson_id,
    )
def get_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    return get_marketing_lesson_text(
        chapter_id,
        lesson_id,
    )
# ==========================================================
# Quiz Normalization
# ==========================================================
def _answer_index(
    value: Any,
    options: list[str],
) -> int:
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        if 0 <= value < len(options):
            return value
        if 1 <= value <= len(options):
            return value - 1
        return 0
    text = _text(value)
    if not text:
        return 0
    # English option letters.
    letter_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }
    if text.upper() in letter_map:
        return letter_map[text.upper()]
    # Persian option letters.
    persian_map = {
        "الف": 0,
        "ب": 1,
        "ج": 2,
        "د": 3,
    }
    if text in persian_map:
        return persian_map[text]
    # Numeric string.
    try:
        number = int(text)
        if 0 <= number < len(options):
            return number
        if 1 <= number <= len(options):
            return number - 1
    except (TypeError, ValueError):
        pass
    # Exact option text.
    normalized_answer = text.casefold()
    for index, option in enumerate(options):
        if (
            _text(option).casefold()
            == normalized_answer
        ):
            return index
    return 0
def normalize_question(
    question: Any,
    index: int = 0,
) -> dict[str, Any]:
    if not isinstance(question, Mapping):
        return {
            "id": f"marketing_q_{index + 1}",
            "question": _text(question),
            "options": [],
            "correct_index": 0,
            "answer_index": 0,
            "explanation": "",
        }
    result = deepcopy(dict(question))
    question_id = (
        result.get("id")
        or result.get("question_id")
        or f"marketing_q_{index + 1}"
    )
    result["id"] = _id(question_id)
    result["question"] = _text(
        result.get("question")
        or result.get("text")
        or result.get("question_text")
        or ""
    )
    raw_options = (
        result.get("options")
        or result.get("choices")
        or result.get("answers")
        or []
    )
    options: list[str] = []
    for option in _list(raw_options):
        if isinstance(option, Mapping):
            value = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or option.get("value")
                or ""
            )
        else:
            value = option
        options.append(
            _text(value)
        )
    result["options"] = options
    # ------------------------------------------------------
    # Detect correct answer from all supported schemas.
    # ------------------------------------------------------
    correct_value = None
    if result.get("correct_index") is not None:
        correct_value = result.get(
            "correct_index"
        )
    elif result.get("answer_index") is not None:
        correct_value = result.get(
            "answer_index"
        )
    elif result.get("correct_answer") is not None:
        correct_value = result.get(
            "correct_answer"
        )
    elif result.get("answer") is not None:
        correct_value = result.get(
            "answer"
        )
    elif result.get("correct") is not None:
        correct_value = result.get(
            "correct"
        )
    correct_index = _answer_index(
        correct_value,
        options,
    )
    if options:
        if (
            correct_index < 0
            or correct_index >= len(options)
        ):
            correct_index = 0
    else:
        correct_index = 0
    result["correct_index"] = correct_index
    result["answer_index"] = correct_index
    # Preserve the original answer value.
    if (
        result.get("correct_answer") is not None
    ):
        result["correct_answer"] = result[
            "correct_answer"
        ]
    result["explanation"] = _text(
        result.get("explanation")
        or result.get("solution")
        or result.get("answer_explanation")
        or result.get("reason")
        or ""
    )
    return result
# ==========================================================
# Quiz
# ==========================================================
def get_marketing_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    chapter = _id(chapter_id)
    lesson = _id(lesson_id)
    if not chapter or not lesson:
        return []
    try:
        questions = get_quiz_questions(
            chapter,
            lesson,
        )
    except Exception:
        return []
    if not isinstance(questions, list):
        return []
    result: list[dict[str, Any]] = []
    for index, question in enumerate(
        questions
    ):
        if not isinstance(
            question,
            Mapping,
        ):
            continue
        item = normalize_question(
            question,
            index,
        )
        item["module_id"] = get_module_id()
        item["chapter_id"] = chapter
        item["lesson_id"] = lesson
        result.append(item)
    return result
def get_marketing_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    return get_marketing_quiz(
        chapter_id,
        lesson_id,
    )
def get_quiz_questions_for_lesson(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    return get_marketing_quiz(
        chapter_id,
        lesson_id,
    )
def get_all_quiz_questions() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for chapter in get_marketing_chapters():
        chapter_id = _id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )
        if not chapter_id:
            continue
        for lesson in get_marketing_lessons(
            chapter_id
        ):
            lesson_id = _id(
                lesson.get("id")
                or lesson.get("lesson_id")
            )
            if not lesson_id:
                continue
            questions = get_marketing_quiz(
                chapter_id,
                lesson_id,
            )
            results.extend(
                questions
            )
    return results
# ==========================================================
# Search
# ==========================================================
def search_lessons(
    keyword: str,
) -> list[dict[str, Any]]:
    normalized = _text(
        keyword
    ).casefold()
    if not normalized:
        return []
    results: list[dict[str, Any]] = []
    for chapter in get_marketing_chapters():
        chapter_id = _id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )
        chapter_title = _text(
            chapter.get("title")
            or chapter.get("name")
            or ""
        )
        if not chapter_id:
            continue
        for lesson in get_marketing_lessons(
            chapter_id
        ):
            lesson_id = _id(
                lesson.get("id")
                or lesson.get("lesson_id")
            )
            title = _text(
                lesson.get("title")
                or lesson.get("name")
                or ""
            )
            content = (
                get_marketing_lesson_text(
                    chapter_id,
                    lesson_id,
                )
                or ""
            )
            raw_keywords = lesson.get(
                "keywords",
                [],
            )
            keywords = " ".join(
                _text(item)
                for item in _list(
                    raw_keywords
                )
            )
            searchable = (
                f"{chapter_title}\n"
                f"{title}\n"
                f"{content}\n"
                f"{keywords}"
            ).casefold()
            if normalized in searchable:
                results.append(
                    {
                        "module_id": get_module_id(),
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "chapter_title": chapter_title,
                        "title": title,
                    }
                )
    return results
# ==========================================================
# Statistics
# ==========================================================
def get_curriculum_stats() -> dict[str, int]:
    chapters = get_marketing_chapters()
    lesson_count = 0
    quiz_count = 0
    for chapter in chapters:
        chapter_id = _id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )
        if not chapter_id:
            continue
        lessons = get_marketing_lessons(
            chapter_id
        )
        lesson_count += len(
            lessons
        )
        for lesson in lessons:
            lesson_id = _id(
                lesson.get("id")
                or lesson.get("lesson_id")
            )
            if not lesson_id:
                continue
            quiz_count += len(
                get_marketing_quiz(
                    chapter_id,
                    lesson_id,
                )
            )
    return {
        "modules": 1,
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": quiz_count,
    }
def get_curriculum_statistics() -> dict[str, int]:
    return get_curriculum_stats()
def get_module_statistics() -> dict[str, Any]:
    return {
        "module_id": get_module_id(),
        "title": get_module_title(),
        "description": str(
            MODULE_DESCRIPTION
        ),
        **get_curriculum_stats(),
    }
# ==========================================================
# Validation
# ==========================================================
def validate_curriculum() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    chapters = get_marketing_chapters()
    if not chapters:
        errors.append(
            "No marketing chapters found."
        )
    chapter_ids: set[str] = set()
    for chapter_index, chapter in enumerate(
        chapters,
        start=1,
    ):
        chapter_id = _id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )
        if not chapter_id:
            errors.append(
                f"Chapter #{chapter_index} has no ID."
            )
            continue
        if chapter_id in chapter_ids:
            errors.append(
                f"Duplicate chapter ID: {chapter_id}"
            )
        chapter_ids.add(
            chapter_id
        )
        if not chapter.get("title"):
            warnings.append(
                f"Chapter '{chapter_id}' has no title."
            )
        lessons = get_marketing_lessons(
            chapter_id
        )
        if not lessons:
            warnings.append(
                f"Chapter '{chapter_id}' has no lessons."
            )
            continue
        lesson_ids: set[str] = set()
        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):
            lesson_id = _id(
                lesson.get("id")
                or lesson.get("lesson_id")
            )
            if not lesson_id:
                errors.append(
                    f"Chapter '{chapter_id}' "
                    f"lesson #{lesson_index} has no ID."
                )
                continue
            if lesson_id in lesson_ids:
                errors.append(
                    f"Duplicate lesson ID "
                    f"'{lesson_id}' in chapter "
                    f"'{chapter_id}'."
                )
            lesson_ids.add(
                lesson_id
            )
            if not lesson.get("title"):
                warnings.append(
                    f"Lesson '{lesson_id}' "
                    f"in chapter '{chapter_id}' "
                    "has no title."
                )
            if not get_marketing_lesson_text(
                chapter_id,
                lesson_id,
            ):
                warnings.append(
                    f"Lesson '{lesson_id}' "
                    f"in chapter '{chapter_id}' "
                    "has no content."
                )
            questions = get_marketing_quiz(
                chapter_id,
                lesson_id,
            )
            if not questions:
                warnings.append(
                    f"Lesson '{lesson_id}' "
                    f"in chapter '{chapter_id}' "
                    "has no quiz questions."
                )
            for question_index, question in enumerate(
                questions,
                start=1,
            ):
                options = question.get(
                    "options",
                    [],
                )
                if len(options) < 2:
                    errors.append(
                        f"Question #{question_index} "
                        f"in '{chapter_id}/{lesson_id}' "
                        "has fewer than 2 options."
                    )
                correct_index = question.get(
                    "correct_index"
                )
                if not isinstance(
                    correct_index,
                    int,
                ):
                    errors.append(
                        f"Question #{question_index} "
                        f"in '{chapter_id}/{lesson_id}' "
                        "has invalid correct_index."
                    )
                elif options and not (
                    0 <= correct_index < len(options)
                ):
                    errors.append(
                        f"Question #{question_index} "
                        f"in '{chapter_id}/{lesson_id}' "
                        "has out-of-range correct_index."
                    )
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": get_curriculum_stats(),
    }
def validate_module() -> dict[str, Any]:
    return validate_curriculum()
# ==========================================================
# Health Check
# ==========================================================
def marketing_service_health_check() -> bool:
    try:
        if not get_module_id():
            return False
        if not get_module_title():
            return False
        chapters = get_marketing_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            return False
        for chapter in chapters:
            if not isinstance(
                chapter,
                dict,
            ):
                return False
            chapter_id = (
                chapter.get("id")
                or chapter.get("chapter_id")
            )
            if not chapter_id:
                return False
            lessons = get_marketing_lessons(
                str(chapter_id)
            )
            if not isinstance(
                lessons,
                list,
            ):
                return False
        return True
    except Exception:
        return False
def service_health_check() -> bool:
    return marketing_service_health_check()
# ==========================================================
# Compatibility Aliases
# ==========================================================
get_marketing_module_info = get_module_info
get_marketing_lesson_quiz = get_marketing_quiz
get_marketing_all_quiz_questions = (
    get_all_quiz_questions
)
# ==========================================================
# Public API
# ==========================================================
__all__ = [
    # Module
    "get_module_id",
    "get_module_title",
    "get_module_info",
    "get_marketing_module_info",
    # Chapters
    "get_marketing_chapters",
    "get_marketing_chapter",
    "get_chapter_by_id",
    "get_marketing_chapter_ids",
    # Lessons
    "get_marketing_lessons",
    "get_marketing_lesson",
    "get_lesson_by_id",
    "get_marketing_lesson_ids",
    # Content
    "get_marketing_lesson_content",
    "get_marketing_lesson_text",
    "get_lesson_content",
    "get_lesson_text",
    # Quiz
    "normalize_question",
    "get_marketing_quiz",
    "get_marketing_lesson_quiz",
    "get_marketing_quiz_questions",
    "get_quiz_questions_for_lesson",
    "get_all_quiz_questions",
    "get_marketing_all_quiz_questions",
    # Search
    "search_lessons",
    # Statistics
    "get_curriculum_stats",
    "get_curriculum_statistics",
    "get_module_statistics",
    # Validation
    "validate_curriculum",
    "validate_module",
    # Health
    "marketing_service_health_check",
    "service_health_check",
]
