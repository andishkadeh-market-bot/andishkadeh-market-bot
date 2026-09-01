"""
Professional Marketing Service Layer
Andishkadeh Management & Market
Responsibilities:
- Module information
- Chapter management
- Lesson management
- Lesson content
- Quiz questions
- Search
- Curriculum statistics
- Curriculum validation
- Health check
Data source:
    modules.marketing.data
"""
from __future__ import annotations
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
    return [
        dict(chapter)
        for chapter in chapters
        if isinstance(chapter, Mapping)
    ]
def get_marketing_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    if not chapter_id:
        return None
    try:
        chapter = get_chapter(
            str(chapter_id).strip()
        )
    except Exception:
        return None
    if isinstance(chapter, Mapping):
        return dict(chapter)
    return None
def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:
    return get_marketing_chapter(chapter_id)
# ==========================================================
# Lessons
# ==========================================================
def get_marketing_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    if not chapter_id:
        return []
    try:
        lessons = get_lessons(
            str(chapter_id).strip()
        )
    except Exception:
        return []
    if not isinstance(lessons, list):
        return []
    return [
        dict(lesson)
        for lesson in lessons
        if isinstance(lesson, Mapping)
    ]
def get_marketing_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    if not chapter_id or not lesson_id:
        return None
    try:
        lesson = get_lesson(
            str(chapter_id).strip(),
            str(lesson_id).strip(),
        )
    except Exception:
        return None
    if isinstance(lesson, Mapping):
        return dict(lesson)
    return None
def get_lesson_by_id(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    return get_marketing_lesson(
        chapter_id,
        lesson_id,
    )
# ==========================================================
# Lesson Content
# ==========================================================
def get_marketing_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    return get_marketing_lesson(
        chapter_id,
        lesson_id,
    )
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
def get_marketing_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    if not chapter_id or not lesson_id:
        return []
    try:
        questions = get_quiz_questions(
            str(chapter_id).strip(),
            str(lesson_id).strip(),
        )
    except Exception:
        return []
    if not isinstance(questions, list):
        return []
    return [
        dict(question)
        for question in questions
        if isinstance(question, Mapping)
    ]
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
        chapter_id = str(
            chapter.get("id")
            or chapter.get("chapter_id")
            or ""
        ).strip()
        if not chapter_id:
            continue
        for lesson in get_marketing_lessons(
            chapter_id
        ):
            lesson_id = str(
                lesson.get("id")
                or lesson.get("lesson_id")
                or ""
            ).strip()
            if not lesson_id:
                continue
            for question in get_marketing_quiz(
                chapter_id,
                lesson_id,
            ):
                item = dict(question)
                item.setdefault(
                    "chapter_id",
                    chapter_id,
                )
                item.setdefault(
                    "lesson_id",
                    lesson_id,
                )
                results.append(item)
    return results
# ==========================================================
# Search
# ==========================================================
def search_lessons(
    keyword: str,
) -> list[dict[str, Any]]:
    normalized = str(
        keyword or ""
    ).strip().casefold()
    if not normalized:
        return []
    results: list[dict[str, Any]] = []
    for chapter in get_marketing_chapters():
        chapter_id = str(
            chapter.get("id")
            or chapter.get("chapter_id")
            or ""
        ).strip()
        if not chapter_id:
            continue
        for lesson in get_marketing_lessons(
            chapter_id
        ):
            lesson_id = str(
                lesson.get("id")
                or lesson.get("lesson_id")
                or ""
            ).strip()
            title = str(
                lesson.get("title") or ""
            )
            content = (
                get_marketing_lesson_text(
                    chapter_id,
                    lesson_id,
                )
                or ""
            )
            keywords = " ".join(
                str(item)
                for item in lesson.get(
                    "keywords",
                    [],
                )
            )
            searchable = (
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
        chapter_id = str(
            chapter.get("id")
            or chapter.get("chapter_id")
            or ""
        ).strip()
        if not chapter_id:
            continue
        lessons = get_marketing_lessons(
            chapter_id
        )
        lesson_count += len(lessons)
        for lesson in lessons:
            lesson_id = str(
                lesson.get("id")
                or lesson.get("lesson_id")
                or ""
            ).strip()
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
        warnings.append(
            "No marketing chapters found."
        )
    chapter_ids: set[str] = set()
    for index, chapter in enumerate(
        chapters,
        start=1,
    ):
        chapter_id = str(
            chapter.get("id")
            or chapter.get("chapter_id")
            or ""
        ).strip()
        if not chapter_id:
            errors.append(
                f"Chapter #{index} has no ID."
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
        lesson_ids: set[str] = set()
        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):
            lesson_id = str(
                lesson.get("id")
                or lesson.get("lesson_id")
                or ""
            ).strip()
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
# Public API
# ==========================================================
__all__ = [
    "get_module_id",
    "get_module_title",
    "get_module_info",
    "get_marketing_chapters",
    "get_marketing_chapter",
    "get_chapter_by_id",
    "get_marketing_lessons",
    "get_marketing_lesson",
    "get_lesson_by_id",
    "get_marketing_lesson_content",
    "get_marketing_lesson_text",
    "get_marketing_quiz",
    "get_marketing_quiz_questions",
    "get_quiz_questions_for_lesson",
    "get_all_quiz_questions",
    "search_lessons",
    "get_curriculum_stats",
    "get_curriculum_statistics",
    "get_module_statistics",
    "validate_curriculum",
    "validate_module",
    "marketing_service_health_check",
    "service_health_check",
]
