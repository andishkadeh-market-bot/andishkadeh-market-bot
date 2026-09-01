"""
Economy & Market service layer.
Andishkadeh Management & Market
"""

from __future__ import annotations

from typing import Any, Mapping

from modules.economy import data


# ==========================================================
# Module Information
# ==========================================================

def get_module_id() -> str:
    return str(data.MODULE_ID)


def get_module_title() -> str:
    return str(data.MODULE_TITLE)


def get_module_info() -> dict[str, str]:
    return {
        "id": get_module_id(),
        "module_id": get_module_id(),
        "title": get_module_title(),
        "description": str(
            data.MODULE_DESCRIPTION
        ),
    }


# ==========================================================
# Chapters
# ==========================================================

def get_economy_chapters() -> list[dict[str, Any]]:
    chapters = data.get_chapters()

    if not isinstance(chapters, list):
        return []

    return [
        dict(item)
        for item in chapters
        if isinstance(item, Mapping)
    ]


def get_economy_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:

    result = data.get_chapter(
        str(chapter_id or "").strip()
    )

    if isinstance(result, Mapping):
        return dict(result)

    return None


def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:
    return get_economy_chapter(
        chapter_id
    )


# ==========================================================
# Lessons
# ==========================================================

def get_economy_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:

    lessons = data.get_lessons(
        str(chapter_id or "").strip()
    )

    if not isinstance(lessons, list):
        return []

    return [
        dict(item)
        for item in lessons
        if isinstance(item, Mapping)
    ]


def get_economy_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    result = data.get_lesson(
        str(chapter_id or "").strip(),
        str(lesson_id or "").strip(),
    )

    if isinstance(result, Mapping):
        return dict(result)

    return None


def get_lesson_by_id(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    return get_economy_lesson(
        chapter_id,
        lesson_id,
    )


def get_economy_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    return get_economy_lesson(
        chapter_id,
        lesson_id,
    )


def get_economy_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:

    lesson = get_economy_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    for key in (
        "content",
        "text",
        "description",
        "lesson_content",
        "body",
        "details",
    ):
        value = lesson.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return None


# ==========================================================
# Quiz
# ==========================================================

def get_economy_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    questions = data.get_quiz_questions(
        str(chapter_id or "").strip(),
        str(lesson_id or "").strip(),
    )

    if not isinstance(questions, list):
        return []

    return [
        dict(item)
        for item in questions
        if isinstance(item, Mapping)
    ]


def get_economy_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    return get_economy_quiz(
        chapter_id,
        lesson_id,
    )


def get_all_quiz_questions() -> list[dict[str, Any]]:

    questions = data.get_all_quiz_questions()

    if not isinstance(questions, list):
        return []

    return [
        dict(item)
        for item in questions
        if isinstance(item, Mapping)
    ]


# ==========================================================
# Statistics
# ==========================================================

def get_curriculum_stats() -> dict[str, int]:
    stats = data.get_curriculum_statistics()

    return {
        "modules": int(stats.get("modules", 1)),
        "chapters": int(stats.get("chapters", 0)),
        "lessons": int(stats.get("lessons", 0)),
        "quiz_questions": int(
            stats.get("quiz_questions", 0)
        ),
    }


def get_curriculum_statistics() -> dict[str, int]:
    return get_curriculum_stats()


def get_module_statistics() -> dict[str, Any]:
    return {
        "module_id": get_module_id(),
        "title": get_module_title(),
        **get_curriculum_stats(),
    }


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

    results = []

    for chapter in get_economy_chapters():

        chapter_id = str(
            chapter.get("id", "")
        )

        chapter_text = (
            str(chapter.get("title", ""))
            + "\n"
            + str(chapter.get("description", ""))
        ).casefold()

        for lesson in get_economy_lessons(
            chapter_id
        ):

            lesson_id = str(
                lesson.get("id", "")
            )

            lesson_text = (
                str(lesson.get("title", ""))
                + "\n"
                + str(lesson.get("content", ""))
            ).casefold()

            searchable = (
                chapter_text
                + "\n"
                + lesson_text
            )

            if normalized in searchable:
                results.append(
                    {
                        "module_id": get_module_id(),
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "title": str(
                            lesson.get(
                                "title",
                                lesson_id,
                            )
                        ),
                    }
                )

    return results


# ==========================================================
# Validation
# ==========================================================

def validate_module() -> dict[str, Any]:

    errors = []
    warnings = []

    chapters = get_economy_chapters()

    if not chapters:
        errors.append(
            "Economy curriculum has no chapters."
        )

    chapter_ids = set()

    for index, chapter in enumerate(
        chapters,
        start=1,
    ):

        chapter_id = str(
            chapter.get("id", "")
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

        chapter_ids.add(chapter_id)

        if not chapter.get("title"):
            warnings.append(
                f"Chapter '{chapter_id}' has no title."
            )

        lessons = get_economy_lessons(
            chapter_id
        )

        if not lessons:
            warnings.append(
                f"Chapter '{chapter_id}' has no lessons."
            )

        lesson_ids = set()

        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):

            lesson_id = str(
                lesson.get("id", "")
            ).strip()

            if not lesson_id:
                errors.append(
                    (
                        f"Chapter '{chapter_id}' "
                        f"lesson #{lesson_index} has no ID."
                    )
                )
                continue

            if lesson_id in lesson_ids:
                errors.append(
                    (
                        f"Duplicate lesson ID "
                        f"'{lesson_id}' in chapter "
                        f"'{chapter_id}'."
                    )
                )

            lesson_ids.add(
                lesson_id
            )

            if not lesson.get("title"):
                warnings.append(
                    (
                        f"Lesson '{lesson_id}' "
                        f"in chapter '{chapter_id}' "
                        "has no title."
                    )
                )

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": get_curriculum_stats(),
    }


# ==========================================================
# Health
# ==========================================================

def service_health_check() -> bool:

    try:
        validation = validate_module()

        return (
            bool(get_module_id())
            and bool(get_module_title())
            and bool(get_economy_chapters())
            and bool(validation["valid"])
        )

    except Exception:
        return False


def economy_service_health_check() -> bool:
    return service_health_check()


__all__ = [
    "get_module_id",
    "get_module_title",
    "get_module_info",

    "get_economy_chapters",
    "get_economy_chapter",
    "get_chapter_by_id",

    "get_economy_lessons",
    "get_economy_lesson",
    "get_lesson_by_id",

    "get_economy_lesson_content",
    "get_economy_lesson_text",

    "get_economy_quiz",
    "get_economy_quiz_questions",
    "get_all_quiz_questions",

    "get_curriculum_stats",
    "get_curriculum_statistics",
    "get_module_statistics",

    "search_lessons",
    "validate_module",

    "service_health_check",
    "economy_service_health_check",
]
