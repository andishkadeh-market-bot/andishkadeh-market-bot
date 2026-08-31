"""
International Trade Service Layer
Andishkadeh Management & Market
Responsibilities:
- Access International Trade curriculum data
- Retrieve module information
- Retrieve chapters
- Retrieve lessons
- Retrieve lesson content
- Retrieve quiz questions
- Search lessons
- Provide curriculum statistics
- Validate curriculum data
- Provide health check
Important:
This service layer must remain independent from Telegram handlers.
It must NOT import itself.
It must NOT require optional helper functions from data.py.
"""
from __future__ import annotations
from typing import Any, Mapping
# ==========================================================
# Constants
# ==========================================================
MODULE_ID = "international_trade"
MODULE_TITLE = "تجارت بین‌الملل"
MODULE_DESCRIPTION = (
    "آموزش تخصصی تجارت بین‌الملل "
    "به‌صورت فصل‌به‌فصل و درس‌به‌درس"
)
# ==========================================================
# Data import
# ==========================================================
# The data module may expose the curriculum under different
# variable names depending on the current project version.
# We intentionally avoid importing helper functions from data.py
# because that caused the deployment failure.
try:
    from modules.international_trade import data as _data_module
except Exception:
    _data_module = None
# ==========================================================
# Helpers
# ==========================================================
def _normalize_id(value: Any) -> str:
    """Normalize an identifier to a clean string."""
    if value is None:
        return ""
    return str(value).strip()
def _as_dict(value: Any) -> dict[str, Any]:
    """Return a dictionary when possible."""
    if isinstance(value, dict):
        return dict(value)
    return {}
def _find_curriculum_data() -> Any:
    """
    Find the International Trade curriculum data.
    Supported variable names:
    - INTERNATIONAL_TRADE_DATA
    - TRADE_DATA
    - CURRICULUM_DATA
    - INTERNATIONAL_TRADE_CURRICULUM
    - DATA
    """
    if _data_module is None:
        return []
    possible_names = (
        "INTERNATIONAL_TRADE_DATA",
        "TRADE_DATA",
        "CURRICULUM_DATA",
        "INTERNATIONAL_TRADE_CURRICULUM",
        "DATA",
    )
    for name in possible_names:
        if hasattr(_data_module, name):
            value = getattr(
                _data_module,
                name,
            )
            if value is not None:
                return value
    return []
def _get_curriculum() -> Any:
    """Return the current International Trade curriculum."""
    return _find_curriculum_data()
def _get_chapters() -> list[dict[str, Any]]:
    """
    Extract chapters from curriculum data.
    Supports both:
        {"chapters": [...]}
    and:
        [...]
    """
    curriculum = _get_curriculum()
    if isinstance(curriculum, dict):
        chapters = curriculum.get(
            "chapters",
            curriculum.get(
                "sections",
                [],
            ),
        )
        if isinstance(chapters, list):
            return [
                item
                for item in chapters
                if isinstance(item, dict)
            ]
        return []
    if isinstance(curriculum, list):
        return [
            item
            for item in curriculum
            if isinstance(item, dict)
        ]
    return []
def _get_chapter_lessons(
    chapter: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Extract lessons from a chapter."""
    possible_keys = (
        "lessons",
        "topics",
        "items",
    )
    for key in possible_keys:
        lessons = chapter.get(key)
        if isinstance(lessons, list):
            return [
                lesson
                for lesson in lessons
                if isinstance(
                    lesson,
                    dict,
                )
            ]
    return []
def _get_item_id(
    item: Mapping[str, Any],
    primary: str,
    secondary: str,
) -> str:
    """Extract an item identifier."""
    return _normalize_id(
        item.get(primary)
        or item.get(secondary)
    )
def _get_title(
    item: Mapping[str, Any],
    fallback: str = "",
) -> str:
    """Extract a title from a curriculum item."""
    value = (
        item.get("title")
        or item.get("name")
        or item.get("heading")
        or fallback
    )
    return str(value).strip()
# ==========================================================
# Module information
# ==========================================================
def get_module_id() -> str:
    """Return module ID."""
    return MODULE_ID
def get_module_title() -> str:
    """Return module title."""
    curriculum = _get_curriculum()
    if isinstance(curriculum, dict):
        title = (
            curriculum.get("title")
            or curriculum.get("name")
        )
        if title:
            return str(title)
    return MODULE_TITLE
def get_module_description() -> str:
    """Return module description."""
    curriculum = _get_curriculum()
    if isinstance(curriculum, dict):
        description = (
            curriculum.get("description")
            or curriculum.get("intro")
            or curriculum.get("summary")
        )
        if description:
            return str(description)
    return MODULE_DESCRIPTION
def get_module_info() -> dict[str, Any]:
    """
    Return complete module information.
    This function is used by Telegram handlers.
    """
    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "title": get_module_title(),
        "description": get_module_description(),
        "chapters": len(
            _get_chapters()
        ),
    }
# ==========================================================
# Chapters
# ==========================================================
def get_chapters() -> list[dict[str, Any]]:
    """
    Return all International Trade chapters.
    A copy of each chapter is returned.
    """
    result: list[dict[str, Any]] = []
    for chapter in _get_chapters():
        result.append(
            dict(chapter)
        )
    return result
def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return one chapter by ID."""
    normalized_id = _normalize_id(
        chapter_id
    )
    if not normalized_id:
        return None
    for chapter in _get_chapters():
        current_id = _get_item_id(
            chapter,
            "id",
            "chapter_id",
        )
        if current_id == normalized_id:
            return dict(chapter)
    return None
def get_chapter_title(
    chapter_id: str,
) -> str | None:
    """Return chapter title."""
    chapter = get_chapter(
        chapter_id
    )
    if chapter is None:
        return None
    title = _get_title(
        chapter
    )
    return title or None
def get_chapter_ids() -> list[str]:
    """Return all chapter IDs."""
    result: list[str] = []
    for chapter in _get_chapters():
        chapter_id = _get_item_id(
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
def get_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return all lessons for a chapter."""
    chapter = get_chapter(
        chapter_id
    )
    if chapter is None:
        return []
    return [
        dict(lesson)
        for lesson
        in _get_chapter_lessons(
            chapter
        )
    ]
def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return one lesson by chapter and lesson ID."""
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
    chapter = get_chapter(
        normalized_chapter_id
    )
    if chapter is None:
        return None
    for lesson in _get_chapter_lessons(
        chapter
    ):
        current_id = _get_item_id(
            lesson,
            "id",
            "lesson_id",
        )
        if current_id == normalized_lesson_id:
            return dict(lesson)
    return None
def get_lesson_title(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    """Return lesson title."""
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    title = _get_title(
        lesson
    )
    return title or None
def get_lesson_ids(
    chapter_id: str,
) -> list[str]:
    """Return all lesson IDs in a chapter."""
    result: list[str] = []
    for lesson in get_lessons(
        chapter_id
    ):
        lesson_id = _get_item_id(
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
    Return complete lesson data.
    """
    lesson = get_lesson(
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
    Return primary textual lesson content.
    Supports multiple common field names.
    """
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    content_keys = (
        "content",
        "text",
        "lesson",
        "description",
        "lesson_content",
        "body",
        "details",
    )
    for key in content_keys:
        value = lesson.get(key)
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                return cleaned
    return None
# ==========================================================
# Quiz
# ==========================================================
def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Return quiz questions for a lesson.
    Supported lesson fields:
    - quiz
    - questions
    - quiz_questions
    """
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return []
    possible_keys = (
        "quiz",
        "questions",
        "quiz_questions",
    )
    for key in possible_keys:
        questions = lesson.get(key)
        if isinstance(
            questions,
            dict,
        ):
            questions = questions.get(
                "questions",
                [],
            )
        if isinstance(
            questions,
            list,
        ):
            return [
                dict(question)
                for question
                in questions
                if isinstance(
                    question,
                    dict,
                )
            ]
    return []
def get_quiz_question_count(
    chapter_id: str,
    lesson_id: str,
) -> int:
    """Return quiz question count."""
    return len(
        get_quiz_questions(
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
    """
    Search lessons by title or textual content.
    """
    normalized_keyword = (
        _normalize_id(keyword)
        .casefold()
    )
    if not normalized_keyword:
        return []
    results: list[dict[str, Any]] = []
    for chapter in _get_chapters():
        chapter_id = _get_item_id(
            chapter,
            "id",
            "chapter_id",
        )
        lessons = _get_chapter_lessons(
            chapter
        )
        for lesson in lessons:
            lesson_id = _get_item_id(
                lesson,
                "id",
                "lesson_id",
            )
            title = _get_title(
                lesson
            )
            content = (
                get_lesson_text(
                    chapter_id,
                    lesson_id,
                )
                or ""
            )
            searchable_text = (
                f"{title}\n{content}"
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
def get_curriculum_statistics() -> dict[str, int]:
    """
    Return curriculum statistics.
    This function intentionally lives in the service layer.
    Therefore data.py does not need to expose a function with
    the same name.
    """
    chapters = _get_chapters()
    lesson_count = 0
    quiz_question_count = 0
    for chapter in chapters:
        lessons = _get_chapter_lessons(
            chapter
        )
        lesson_count += len(
            lessons
        )
        chapter_id = _get_item_id(
            chapter,
            "id",
            "chapter_id",
        )
        for lesson in lessons:
            lesson_id = _get_item_id(
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
def get_content_statistics() -> dict[str, int]:
    """Alias for curriculum statistics."""
    return get_curriculum_statistics()
# ==========================================================
# Validation
# ==========================================================
def validate_international_trade_data() -> dict[str, Any]:
    """
    Validate International Trade curriculum.
    Returns a report instead of raising exceptions.
    """
    errors: list[str] = []
    warnings: list[str] = []
    chapters = _get_chapters()
    if not chapters:
        warnings.append(
            "No International Trade chapters found."
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
        chapter_id = _get_item_id(
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
        if not _get_title(
            chapter
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
            lesson_id = _get_item_id(
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
            if not _get_title(
                lesson
            ):
                warnings.append(
                    (
                        f"Lesson '{lesson_id or lesson_index}' "
                        f"in chapter '{chapter_id}' "
                        "has no title."
                    )
                )
    statistics = get_curriculum_statistics()
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": statistics,
    }
def validate_management_data() -> dict[str, Any]:
    """
    Compatibility alias.
    Some older project components may expect this name.
    """
    return validate_international_trade_data()
# ==========================================================
# Health check
# ==========================================================
def international_trade_service_health_check() -> bool:
    """Check service availability."""
    try:
        info = get_module_info()
        if not info.get("id"):
            return False
        statistics = get_curriculum_statistics()
        if not isinstance(
            statistics,
            dict,
        ):
            return False
        return True
    except Exception:
        return False
def trade_service_health_check() -> bool:
    """Compatibility alias."""
    return international_trade_service_health_check()
def service_health_check() -> bool:
    """Generic compatibility health check."""
    return international_trade_service_health_check()
# ==========================================================
# Public aliases
# ==========================================================
# These aliases make the service compatible with different
# versions of the handlers without introducing circular imports.
get_trade_chapters = get_chapters
get_trade_chapter = get_chapter
get_trade_lessons = get_lessons
get_trade_lesson = get_lesson
get_trade_module_info = get_module_info
get_trade_quiz_questions = get_quiz_questions
get_trade_statistics = get_curriculum_statistics
# ==========================================================
# Module test
# ==========================================================
if __name__ == "__main__":
    print(
        "International Trade Service"
    )
    print(
        "Module:",
        get_module_info()
    )
    print(
        "Statistics:",
        get_curriculum_statistics()
    )
    print(
        "Health:",
        international_trade_service_health_check()
    )
