"""
Andishkadeh Management & Market
Banking Specialized Module - Service Layer
File:
    modules/banking/service.py
Purpose:
    Business/service layer for the Banking Specialized module.
Responsibilities:
    - Module information
    - Chapter retrieval
    - Lesson retrieval
    - Lesson details
    - Quiz retrieval
    - Question retrieval
    - Search
    - Curriculum statistics
    - Safe data access
    - Compatibility helpers for handlers.py
Design:
    handlers.py
        ↓
    service.py
        ↓
    data.py
The service layer intentionally contains no Telegram code.
"""
from __future__ import annotations
import logging
from copy import deepcopy
from typing import Any
from . import data
logger = logging.getLogger(__name__)
# ==========================================================
# Constants
# ==========================================================
MODULE_ID = getattr(
    data,
    "MODULE_ID",
    "banking",
)
MODULE_TITLE = getattr(
    data,
    "MODULE_TITLE",
    "🏦 بانکداری تخصصی",
)
MODULE_DESCRIPTION = getattr(
    data,
    "MODULE_DESCRIPTION",
    "آموزش تخصصی و کاربردی بانکداری، قوانین بانکی، عملیات بانکی، "
    "بانکداری اسلامی، مبارزه با پولشویی، اعتبارسنجی و مدیریت بانک.",
)
# ==========================================================
# Internal Helpers
# ==========================================================
def _copy(value: Any) -> Any:
    """
    Return a deep copy so handlers cannot accidentally mutate
    the original curriculum stored in data.py.
    """
    try:
        return deepcopy(value)
    except Exception:
        logger.exception(
            "Failed to deepcopy banking data."
        )
        return value
def _as_dict(value: Any) -> dict[str, Any]:
    """Convert a value to a safe dictionary."""
    if isinstance(value, dict):
        return _copy(value)
    return {}
def _as_list(value: Any) -> list[Any]:
    """Convert a value to a safe list."""
    if isinstance(value, list):
        return _copy(value)
    if isinstance(value, tuple):
        return _copy(list(value))
    return []
def _get_raw_curriculum() -> list[dict[str, Any]]:
    """
    Load the curriculum from data.py.
    Supports several possible data.py structures so the service
    remains compatible while the banking module evolves.
    """
    possible_names = (
        "BANKING_CURRICULUM",
        "CURRICULUM",
        "CHAPTERS",
        "BANKING_CHAPTERS",
    )
    for name in possible_names:
        value = getattr(data, name, None)
        if isinstance(value, list):
            return _as_list(value)
    # Optional function-based data provider.
    provider = getattr(
        data,
        "get_curriculum",
        None,
    )
    if callable(provider):
        try:
            result = provider()
            if isinstance(result, list):
                return _as_list(result)
        except Exception:
            logger.exception(
                "Banking curriculum provider failed."
            )
    # Fallback to get_chapters().
    provider = getattr(
        data,
        "get_chapters",
        None,
    )
    if callable(provider):
        try:
            result = provider()
            if isinstance(result, list):
                return _as_list(result)
        except Exception:
            logger.exception(
                "Banking get_chapters provider failed."
            )
    return []
def _chapter_id(chapter: dict[str, Any]) -> str:
    """Return normalized chapter ID."""
    value = (
        chapter.get("id")
        or chapter.get("chapter_id")
    )
    return str(value) if value is not None else ""
def _chapter_title(chapter: dict[str, Any]) -> str:
    """Return normalized chapter title."""
    value = (
        chapter.get("title")
        or chapter.get("name")
        or _chapter_id(chapter)
    )
    return str(value)
def _lesson_id(lesson: dict[str, Any]) -> str:
    """Return normalized lesson ID."""
    value = (
        lesson.get("id")
        or lesson.get("lesson_id")
    )
    return str(value) if value is not None else ""
def _lesson_title(lesson: dict[str, Any]) -> str:
    """Return normalized lesson title."""
    value = (
        lesson.get("title")
        or lesson.get("name")
        or _lesson_id(lesson)
    )
    return str(value)
def _get_chapter_lessons(
    chapter: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Extract lessons from a chapter.
    Supported keys:
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
    return str(MODULE_ID)
def get_module_title() -> str:
    """Return Banking module title."""
    return str(MODULE_TITLE)
def get_module_description() -> str:
    """Return Banking module description."""
    return str(MODULE_DESCRIPTION)
# ==========================================================
# Chapters
# ==========================================================
def get_chapters() -> list[dict[str, Any]]:
    """
    Return all Banking chapters.
    Each chapter is normalized to:
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
        if not isinstance(chapter, dict):
            continue
        chapter_id = _chapter_id(chapter)
        if not chapter_id:
            continue
        normalized = _copy(chapter)
        normalized["id"] = chapter_id
        normalized["chapter_id"] = chapter_id
        normalized["title"] = _chapter_title(chapter)
        lessons = _get_chapter_lessons(chapter)
        normalized["lessons"] = lessons
        result.append(normalized)
    return result
def get_chapter(
    chapter_id: str | int,
) -> dict[str, Any] | None:
    """
    Return one Banking chapter by ID.
    """
    target = str(chapter_id)
    for chapter in get_chapters():
        current_id = str(
            chapter.get("id", "")
        )
        current_chapter_id = str(
            chapter.get("chapter_id", "")
        )
        if target in {
            current_id,
            current_chapter_id,
        }:
            return _copy(chapter)
    return None
def chapter_exists(
    chapter_id: str | int,
) -> bool:
    """Check whether a chapter exists."""
    return get_chapter(chapter_id) is not None
# ==========================================================
# Lessons
# ==========================================================
def get_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return all lessons belonging to a chapter.
    """
    chapter = get_chapter(chapter_id)
    if chapter is None:
        return []
    lessons = _get_chapter_lessons(chapter)
    result: list[dict[str, Any]] = []
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        lesson_id = _lesson_id(lesson)
        if not lesson_id:
            continue
        normalized = _copy(lesson)
        normalized["id"] = lesson_id
        normalized["lesson_id"] = lesson_id
        normalized["title"] = _lesson_title(lesson)
        normalized["chapter_id"] = str(chapter_id)
        result.append(normalized)
    return result
def get_lesson(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """
    Return one lesson from a specific chapter.
    """
    target_chapter = str(chapter_id)
    target_lesson = str(lesson_id)
    for lesson in get_lessons(
        target_chapter
    ):
        current_id = str(
            lesson.get("id", "")
        )
        current_lesson_id = str(
            lesson.get("lesson_id", "")
        )
        if target_lesson in {
            current_id,
            current_lesson_id,
        }:
            return _copy(lesson)
    return None
def lesson_exists(
    chapter_id: str | int,
    lesson_id: str | int,
) -> bool:
    """Check whether a lesson exists."""
    return (
        get_lesson(
            chapter_id,
            lesson_id,
        )
        is not None
    )
# ==========================================================
# Lesson Content
# ==========================================================
def get_lesson_content(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """
    Return the complete lesson content.
    This intentionally returns the full lesson dictionary
    instead of only the text, because the Banking module is
    designed to support:
        - lesson text
        - detailed explanations
        - technical notes
        - exam notes
        - examples
        - questions
        - references
        - summary
        - review
    """
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    return _copy(lesson)
def get_lesson_text(
    chapter_id: str | int,
    lesson_id: str | int,
) -> str:
    """
    Extract the primary educational text from a lesson.
    Supports common field names used by curriculum files.
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
        value = lesson.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""
# ==========================================================
# Educational Sections
# ==========================================================
def get_lesson_section(
    chapter_id: str | int,
    lesson_id: str | int,
    section: str,
) -> Any:
    """
    Return a named educational section.
    Examples:
        get_lesson_section(..., "summary")
        get_lesson_section(..., "exam_notes")
        get_lesson_section(..., "examples")
        get_lesson_section(..., "references")
    """
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    value = lesson.get(section)
    return _copy(value)
def get_summary(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return lesson summary."""
    return get_lesson_section(
        chapter_id,
        lesson_id,
        "summary",
    )
def get_exam_notes(
    chapter_id: str | int,
    lesson_id: str | int,
) -> Any:
    """Return lesson exam notes."""
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
        if isinstance(value, list):
            return _as_list(value)
    return []
def get_references(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[Any]:
    """Return lesson references."""
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
        if isinstance(value, list):
            return _as_list(value)
    return []
# ==========================================================
# Quiz System
# ==========================================================
def get_quiz_questions(
    chapter_id: str | int,
    lesson_id: str | int,
) -> list[dict[str, Any]]:
    """
    Return quiz questions for a lesson.
    Supported keys:
        questions
        quiz
        quiz_questions
    """
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return []
    for key in (
        "questions",
        "quiz_questions",
        "quiz",
    ):
        value = lesson.get(key)
        if isinstance(value, list):
            return _as_list(value)
    return []
def get_quiz_question(
    chapter_id: str | int,
    lesson_id: str | int,
    question_index: int,
) -> dict[str, Any] | None:
    """
    Return a single quiz question by zero-based index.
    """
    questions = get_quiz_questions(
        chapter_id,
        lesson_id,
    )
    if question_index < 0:
        return None
    if question_index >= len(questions):
        return None
    question = questions[question_index]
    if not isinstance(question, dict):
        return None
    return _copy(question)
def get_question_count(
    chapter_id: str | int,
    lesson_id: str | int,
) -> int:
    """Return number of quiz questions."""
    return len(
        get_quiz_questions(
            chapter_id,
            lesson_id,
        )
    )
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
        - technical notes
        - exam notes
    """
    normalized_query = (
        str(query or "")
        .strip()
        .casefold()
    )
    if not normalized_query:
        return []
    results: list[dict[str, Any]] = []
    for chapter in get_chapters():
        chapter_id = str(
            chapter.get("id", "")
        )
        chapter_title = str(
            chapter.get("title", "")
        )
        chapter_text = " ".join(
            str(
                chapter.get(
                    key,
                    "",
                )
            )
            for key in (
                "description",
                "keywords",
            )
        )
        for lesson in get_lessons(
            chapter_id
        ):
            lesson_id = str(
                lesson.get("id", "")
            )
            lesson_title = str(
                lesson.get("title", "")
            )
            searchable_parts = [
                chapter_title,
                chapter_text,
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
                        "exam_notes",
                        "",
                    )
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
                    }
                )
    return results
# ==========================================================
# Statistics
# ==========================================================
def get_curriculum_statistics() -> dict[str, int]:
    """
    Calculate Banking curriculum statistics.
    Returns:
        {
            "chapters": ...,
            "lessons": ...,
            "questions": ...
        }
    """
    chapters = get_chapters()
    lessons_count = 0
    questions_count = 0
    for chapter in chapters:
        chapter_id = str(
            chapter.get("id", "")
        )
        lessons = get_lessons(
            chapter_id
        )
        lessons_count += len(
            lessons
        )
        for lesson in lessons:
            questions_count += len(
                get_quiz_questions(
                    chapter_id,
                    lesson.get(
                        "id",
                        "",
                    ),
                )
            )
    return {
        "chapters": len(chapters),
        "lessons": lessons_count,
        "questions": questions_count,
    }
def statistics() -> dict[str, int]:
    """Compatibility alias."""
    return get_curriculum_statistics()
# ==========================================================
# Health Check
# ==========================================================
def data_health_check() -> bool:
    """
    Validate the Banking data structure.
    This function is intentionally conservative.
    A Banking module may initially contain chapters without
    quizzes while development is still underway.
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
            logger.error(
                "Banking chapters are not a list."
            )
            return False
        seen_chapters: set[str] = set()
        for chapter in chapters:
            if not isinstance(
                chapter,
                dict,
            ):
                logger.error(
                    "Banking chapter is not a dictionary."
                )
                return False
            chapter_id = _chapter_id(
                chapter
            )
            if not chapter_id:
                logger.error(
                    "Banking chapter has no ID."
                )
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
            lessons = get_lessons(
                chapter_id
            )
            seen_lessons: set[str] = set()
            for lesson in lessons:
                lesson_id = _lesson_id(
                    lesson
                )
                if not lesson_id:
                    logger.error(
                        (
                            "Banking lesson without ID "
                            "in chapter %s."
                        ),
                        chapter_id,
                    )
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
        stats = (
            get_curriculum_statistics()
        )
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
    Validate the service layer itself.
    """
    try:
        info = get_module_info()
        if not isinstance(
            info,
            dict,
        ):
            return False
        chapters = get_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            return False
        stats = (
            get_curriculum_statistics()
        )
        if not isinstance(
            stats,
            dict,
        ):
            return False
        return True
    except Exception:
        logger.exception(
            "Banking service health check failed."
        )
        return False
# ==========================================================
# Compatibility Aliases
# ==========================================================
def get_all_chapters() -> list[dict[str, Any]]:
    """Compatibility alias for get_chapters()."""
    return get_chapters()
def get_all_lessons(
    chapter_id: str | int,
) -> list[dict[str, Any]]:
    """Compatibility alias for get_lessons()."""
    return get_lessons(
        chapter_id
    )
def get_lesson_details(
    chapter_id: str | int,
    lesson_id: str | int,
) -> dict[str, Any] | None:
    """Compatibility alias for get_lesson_content()."""
    return get_lesson_content(
        chapter_id,
        lesson_id,
    )
# ==========================================================
# Public API
# ==========================================================
__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "get_module_info",
    "get_module_id",
    "get_module_title",
    "get_module_description",
    "get_chapters",
    "get_all_chapters",
    "get_chapter",
    "chapter_exists",
    "get_lessons",
    "get_all_lessons",
    "get_lesson",
    "lesson_exists",
    "get_lesson_content",
    "get_lesson_details",
    "get_lesson_text",
    "get_lesson_section",
    "get_summary",
    "get_exam_notes",
    "get_specialized_notes",
    "get_examples",
    "get_references",
    "get_quiz_questions",
    "get_quiz_question",
    "get_question_count",
    "search",
    "get_curriculum_statistics",
    "statistics",
    "data_health_check",
    "service_health_check",
]
