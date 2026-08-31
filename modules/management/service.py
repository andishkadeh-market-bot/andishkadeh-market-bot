"""
Management service layer for Andishkadeh Management & Market.
Responsibilities:
- Access Management curriculum data
- Retrieve chapters
- Retrieve lessons
- Retrieve lesson content
- Retrieve quiz questions
- Provide compatibility helpers for Telegram handlers
- Validate Management data
- Provide content statistics
This service layer is independent from Telegram.
"""
from __future__ import annotations
from typing import Any, Iterable, Mapping
from modules.management import data as management_data
# ==========================================================
# Constants
# ==========================================================
MODULE_ID = "management"
MODULE_TITLE = "آموزش مدیریت"
# ==========================================================
# Internal helpers
# ==========================================================
def _normalize_id(value: Any) -> str:
    """Normalize identifiers to strings."""
    if value is None:
        return ""
    return str(value).strip()
def _copy_dict(value: Any) -> dict[str, Any]:
    """Return a safe dictionary copy."""
    if isinstance(value, dict):
        return dict(value)
    return {}
def _find_data_source() -> Any:
    """
    Find the Management curriculum source.
    The current data.py uses CHAPTER_1, CHAPTER_2, ...
    rather than MANAGEMENT_DATA.
    This function supports both structures so the service
    remains compatible with future refactors.
    """
    # ------------------------------------------------------
    # Preferred explicit curriculum objects
    # ------------------------------------------------------
    for name in (
        "MANAGEMENT_DATA",
        "MANAGEMENT_CURRICULUM",
        "CURRICULUM",
        "CHAPTERS",
    ):
        value = getattr(
            management_data,
            name,
            None,
        )
        if value is not None:
            return value
    # ------------------------------------------------------
    # Current architecture:
    # CHAPTER_1, CHAPTER_2, ...
    # ------------------------------------------------------
    chapters: list[dict[str, Any]] = []
    index = 1
    while True:
        name = f"CHAPTER_{index}"
        value = getattr(
            management_data,
            name,
            None,
        )
        if value is None:
            break
        if isinstance(value, dict):
            chapters.append(
                dict(value)
            )
        index += 1
    return chapters
def _get_chapters() -> list[dict[str, Any]]:
    """Return normalized Management chapters."""
    source = _find_data_source()
    # ------------------------------------------------------
    # Dictionary-based curriculum
    # ------------------------------------------------------
    if isinstance(source, dict):
        chapters = source.get(
            "chapters",
            source.get(
                "data",
                [],
            ),
        )
        if isinstance(chapters, list):
            return [
                dict(chapter)
                for chapter in chapters
                if isinstance(
                    chapter,
                    dict,
                )
            ]
        # A single chapter dictionary
        if (
            source.get("id")
            and source.get("lessons") is not None
        ):
            return [
                dict(source)
            ]
    # ------------------------------------------------------
    # List-based curriculum
    # ------------------------------------------------------
    if isinstance(source, list):
        return [
            dict(chapter)
            for chapter in source
            if isinstance(
                chapter,
                dict,
            )
        ]
    return []
def _get_chapter_lessons(
    chapter: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Return lessons belonging to a chapter."""
    lessons = chapter.get(
        "lessons",
        [],
    )
    if not isinstance(
        lessons,
        list,
    ):
        return []
    return [
        dict(lesson)
        for lesson in lessons
        if isinstance(
            lesson,
            dict,
        )
    ]
def _get_id(
    item: Mapping[str, Any],
    primary: str,
    secondary: str,
) -> str:
    """Read an ID using compatible field names."""
    return _normalize_id(
        item.get(primary)
        or item.get(secondary)
    )
# ==========================================================
# Module information
# ==========================================================
def get_module_id() -> str:
    """Return Management module ID."""
    return MODULE_ID
def get_module_title() -> str:
    """Return Management module title."""
    title = getattr(
        management_data,
        "MODULE_TITLE",
        None,
    )
    if title:
        return str(title)
    source = _find_data_source()
    if isinstance(source, dict):
        title = source.get(
            "title"
        )
        if title:
            return str(title)
    return MODULE_TITLE
def get_module_info() -> dict[str, Any]:
    """Return Management module information."""
    description = getattr(
        management_data,
        "MODULE_DESCRIPTION",
        "",
    )
    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "title": get_module_title(),
        "description": str(
            description or ""
        ),
    }
# ==========================================================
# Chapters
# ==========================================================
def get_management_chapters() -> list[dict[str, Any]]:
    """
    Return all Management chapters.
    Compatibility name used by Management handlers.
    """
    return [
        dict(chapter)
        for chapter in _get_chapters()
    ]
def get_chapters() -> list[dict[str, Any]]:
    """Alias for get_management_chapters()."""
    return get_management_chapters()
def get_management_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """
    Return one Management chapter by ID.
    Compatibility name used by Management handlers.
    """
    normalized_id = _normalize_id(
        chapter_id
    )
    if not normalized_id:
        return None
    for chapter in _get_chapters():
        current_id = _get_id(
            chapter,
            "id",
            "chapter_id",
        )
        if current_id == normalized_id:
            return dict(chapter)
    return None
def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Alias for get_management_chapter()."""
    return get_management_chapter(
        chapter_id
    )
def get_chapter_title(
    chapter_id: str,
) -> str | None:
    """Return chapter title."""
    chapter = get_management_chapter(
        chapter_id
    )
    if chapter is None:
        return None
    title = chapter.get(
        "title"
    )
    if title is None:
        return None
    return str(title)
def get_chapter_ids() -> list[str]:
    """Return all Management chapter IDs."""
    result: list[str] = []
    for chapter in _get_chapters():
        chapter_id = _get_id(
            chapter,
            "id",
            "chapter_id",
        )
        if chapter_id:
            result.append(
                chapter_id
            )
    return result
# ==========================================================
# Lessons
# ==========================================================
def get_management_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """
    Return all lessons of a Management chapter.
    Compatibility name used by Management handlers.
    """
    chapter = get_management_chapter(
        chapter_id
    )
    if chapter is None:
        return []
    return _get_chapter_lessons(
        chapter
    )
def get_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Alias for get_management_lessons()."""
    return get_management_lessons(
        chapter_id
    )
def get_management_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Return one Management lesson.
    Compatibility name used by Management handlers.
    """
    normalized_chapter_id = _normalize_id(
        chapter_id
    )
    normalized_lesson_id = _normalize_id(
        lesson_id
    )
    if (
        not normalized_chapter_id
        or not normalized_lesson_id
    ):
        return None
    chapter = get_management_chapter(
        normalized_chapter_id
    )
    if chapter is None:
        return None
    for lesson in _get_chapter_lessons(
        chapter
    ):
        current_id = _get_id(
            lesson,
            "id",
            "lesson_id",
        )
        if current_id == normalized_lesson_id:
            return dict(lesson)
    return None
def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Alias for get_management_lesson()."""
    return get_management_lesson(
        chapter_id,
        lesson_id,
    )
def get_lesson_title(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    """Return Management lesson title."""
    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    title = lesson.get(
        "title"
    )
    if title is None:
        return None
    return str(title)
def get_lesson_ids(
    chapter_id: str,
) -> list[str]:
    """Return lesson IDs in a chapter."""
    result: list[str] = []
    for lesson in get_management_lessons(
        chapter_id
    ):
        lesson_id = _get_id(
            lesson,
            "id",
            "lesson_id",
        )
        if lesson_id:
            result.append(
                lesson_id
            )
    return result
# ==========================================================
# Lesson content
# ==========================================================
def get_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Return complete lesson dictionary.
    """
    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    return dict(lesson)
def get_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    """
    Return primary text content of a lesson.
    """
    lesson = get_management_lesson(
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
        "summary",
    )
    for key in content_keys:
        value = lesson.get(
            key
        )
        if isinstance(
            value,
            str,
        ):
            cleaned = value.strip()
            if cleaned:
                return cleaned
    return None
def get_lesson_summary(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return compact lesson summary."""
    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    normalized_lesson_id = _get_id(
        lesson,
        "id",
        "lesson_id",
    )
    return {
        "module_id": MODULE_ID,
        "chapter_id": _normalize_id(
            chapter_id
        ),
        "lesson_id": normalized_lesson_id,
        "title": lesson.get(
            "title",
            normalized_lesson_id,
        ),
        "summary": lesson.get(
            "summary",
            "",
        ),
    }
# ==========================================================
# Quiz
# ==========================================================
def get_management_lesson_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Return quiz questions for a Management lesson.
    Compatibility name used by Management handlers.
    """
    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return []
    possible_keys = (
        "quiz",
        "questions",
        "quiz_questions",
        "test",
    )
    for key in possible_keys:
        questions = lesson.get(
            key
        )
        if not isinstance(
            questions,
            list,
        ):
            continue
        result: list[dict[str, Any]] = []
        for question in questions:
            if isinstance(
                question,
                dict,
            ):
                result.append(
                    dict(question)
                )
        return result
    return []
def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Alias for get_management_lesson_quiz()."""
    return get_management_lesson_quiz(
        chapter_id,
        lesson_id,
    )
def get_quiz_question_count(
    chapter_id: str,
    lesson_id: str,
) -> int:
    """Return number of quiz questions."""
    return len(
        get_management_lesson_quiz(
            chapter_id,
            lesson_id,
        )
    )
# ==========================================================
# Search
# ==========================================================
def search_lessons(
    keyword: str,
) -> list[dict[str, Any]]:
    """Search Management lessons."""
    normalized_keyword = (
        _normalize_id(
            keyword
        ).casefold()
    )
    if not normalized_keyword:
        return []
    results: list[dict[str, Any]] = []
    for chapter in _get_chapters():
        chapter_id = _get_id(
            chapter,
            "id",
            "chapter_id",
        )
        for lesson in _get_chapter_lessons(
            chapter
        ):
            lesson_id = _get_id(
                lesson,
                "id",
                "lesson_id",
            )
            title = str(
                lesson.get(
                    "title",
                    "",
                )
            )
            content = (
                get_lesson_text(
                    chapter_id,
                    lesson_id,
                )
                or ""
            )
            summary = str(
                lesson.get(
                    "summary",
                    "",
                )
            )
            searchable_text = (
                f"{title}\n"
                f"{summary}\n"
                f"{content}"
            ).casefold()
            if normalized_keyword in searchable_text:
                results.append(
                    {
                        "module_id": MODULE_ID,
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "title": title,
                    }
                )
    return results
# ==========================================================
# Statistics
# ==========================================================
def get_content_statistics() -> dict[str, int]:
    """Return Management content statistics."""
    chapters = _get_chapters()
    lesson_count = 0
    quiz_question_count = 0
    for chapter in chapters:
        chapter_id = _get_id(
            chapter,
            "id",
            "chapter_id",
        )
        lessons = _get_chapter_lessons(
            chapter
        )
        lesson_count += len(
            lessons
        )
        for lesson in lessons:
            lesson_id = _get_id(
                lesson,
                "id",
                "lesson_id",
            )
            quiz_question_count += (
                get_quiz_question_count(
                    chapter_id,
                    lesson_id,
                )
            )
    return {
        "modules": 1,
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": quiz_question_count,
    }
# ==========================================================
# Compatibility statistics
# ==========================================================
def get_curriculum_statistics() -> dict[str, int]:
    """
    Return curriculum statistics.
    Kept as a compatibility helper for the module
    architecture.
    """
    return get_content_statistics()
# ==========================================================
# Validation
# ==========================================================
def validate_management_data() -> dict[str, Any]:
    """
    Validate Management curriculum structure.
    Returns a report instead of raising exceptions.
    """
    errors: list[str] = []
    warnings: list[str] = []
    chapters = _get_chapters()
    if not chapters:
        errors.append(
            "No Management chapters found."
        )
    chapter_ids: set[str] = set()
    for chapter_index, chapter in enumerate(
        chapters,
        start=1,
    ):
        if not isinstance(
            chapter,
            dict,
        ):
            errors.append(
                f"Chapter #{chapter_index} is not a dictionary."
            )
            continue
        chapter_id = _get_id(
            chapter,
            "id",
            "chapter_id",
        )
        if not chapter_id:
            errors.append(
                f"Chapter #{chapter_index} has no ID."
            )
        elif chapter_id in chapter_ids:
            errors.append(
                f"Duplicate chapter ID: {chapter_id}"
            )
        else:
            chapter_ids.add(
                chapter_id
            )
        if not chapter.get(
            "title"
        ):
            warnings.append(
                (
                    f"Chapter '{chapter_id or chapter_index}' "
                    "has no title."
                )
            )
        lessons = _get_chapter_lessons(
            chapter
        )
        if not lessons:
            warnings.append(
                (
                    f"Chapter '{chapter_id or chapter_index}' "
                    "has no lessons."
                )
            )
        lesson_ids: set[str] = set()
        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):
            if not isinstance(
                lesson,
                dict,
            ):
                errors.append(
                    (
                        f"Chapter '{chapter_id}' "
                        f"lesson #{lesson_index} "
                        "is not a dictionary."
                    )
                )
                continue
            lesson_id = _get_id(
                lesson,
                "id",
                "lesson_id",
            )
            if not lesson_id:
                errors.append(
                    (
                        f"Chapter '{chapter_id}' "
                        f"lesson #{lesson_index} "
                        "has no ID."
                    )
                )
            elif lesson_id in lesson_ids:
                errors.append(
                    (
                        f"Duplicate lesson ID "
                        f"'{lesson_id}' in chapter "
                        f"'{chapter_id}'."
                    )
                )
            else:
                lesson_ids.add(
                    lesson_id
                )
            if not lesson.get(
                "title"
            ):
                warnings.append(
                    (
                        f"Lesson '{lesson_id or lesson_index}' "
                        f"in chapter '{chapter_id}' "
                        "has no title."
                    )
                )
    statistics = get_content_statistics()
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": statistics,
    }
# ==========================================================
# Health check
# ==========================================================
def management_service_health_check() -> bool:
    """
    Check whether Management service is usable.
    """
    try:
        report = validate_management_data()
        return bool(
            report.get(
                "valid",
                False,
            )
        )
    except Exception:
        return False
# ==========================================================
# Public exports
# ==========================================================
__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "get_module_id",
    "get_module_title",
    "get_module_info",
    "get_management_chapters",
    "get_chapters",
    "get_management_chapter",
    "get_chapter",
    "get_chapter_title",
    "get_chapter_ids",
    "get_management_lessons",
    "get_lessons",
    "get_management_lesson",
    "get_lesson",
    "get_lesson_title",
    "get_lesson_ids",
    "get_lesson_content",
    "get_lesson_text",
    "get_lesson_summary",
    "get_management_lesson_quiz",
    "get_quiz_questions",
    "get_quiz_question_count",
    "search_lessons",
    "get_content_statistics",
    "get_curriculum_statistics",
    "validate_management_data",
    "management_service_health_check",
]
