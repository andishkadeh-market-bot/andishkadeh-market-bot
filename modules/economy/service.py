"""
Economy & Market service layer.
Andishkadeh Management & Market

Responsibilities:
- Module information
- Chapter retrieval
- Lesson retrieval
- Quiz retrieval
- Curriculum statistics
- Search
- Validation
- Health check

This layer contains business logic only.
It does not import Telegram handlers.
"""

from __future__ import annotations

from typing import Any, Mapping

from modules.economy.data import (
    MODULE_ID,
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    get_chapters,
    get_chapter,
    get_lessons,
    get_lesson,
    get_quiz_questions,
    get_all_quiz_questions,
    get_curriculum_statistics,
)


# ==========================================================
# Module Information
# ==========================================================

def get_module_id() -> str:
    return str(MODULE_ID)


def get_module_title() -> str:
    return str(MODULE_TITLE)


def get_module_info() -> dict[str, str]:
    return {
        "id": get_module_id(),
        "module_id": get_module_id(),
        "title": get_module_title(),
        "description": str(
            MODULE_DESCRIPTION
        ),
    }


# ==========================================================
# Chapters
# ==========================================================

def get_economy_chapters() -> list[dict[str, Any]]:
    try:
        chapters = get_chapters()
    except Exception:
        return []

    if not isinstance(
        chapters,
        list,
    ):
        return []

    return [
        dict(chapter)
        for chapter in chapters
        if isinstance(
            chapter,
            Mapping,
        )
    ]


def get_economy_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:

    normalized = str(
        chapter_id or ""
    ).strip()

    if not normalized:
        return None

    try:
        chapter = get_chapter(
            normalized
        )
    except Exception:
        return None

    if isinstance(
        chapter,
        Mapping,
    ):
        return dict(chapter)

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

    normalized = str(
        chapter_id or ""
    ).strip()

    if not normalized:
        return []

    try:
        lessons = get_lessons(
            normalized
        )
    except Exception:
        return []

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
            Mapping,
        )
    ]


def get_economy_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    chapter = str(
        chapter_id or ""
    ).strip()

    lesson = str(
        lesson_id or ""
    ).strip()

    if not chapter or not lesson:
        return None

    try:
        result = get_lesson(
            chapter,
            lesson,
        )
    except Exception:
        return None

    if isinstance(
        result,
        Mapping,
    ):
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


# ==========================================================
# Lesson Content
# ==========================================================

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
        value = lesson.get(
            key
        )

        if isinstance(
            value,
            str,
        ):
            value = value.strip()

            if value:
                return value

    return None


# ==========================================================
# Quiz
# ==========================================================

def get_economy_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    chapter = str(
        chapter_id or ""
    ).strip()

    lesson = str(
        lesson_id or ""
    ).strip()

    if not chapter or not lesson:
        return []

    try:
        questions = get_quiz_questions(
            chapter,
            lesson,
        )
    except Exception:
        return []

    if not isinstance(
        questions,
        list,
    ):
        return []

    return [
        dict(question)
        for question in questions
        if isinstance(
            question,
            Mapping,
        )
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

    try:
        questions = get_all_quiz_questions_from_data()
    except Exception:
        return []

    return [
        dict(question)
        for question in questions
        if isinstance(
            question,
            Mapping,
        )
    ]


def get_all_quiz_questions_from_data() -> list[dict[str, Any]]:
    return get_all_quiz_questions.__wrapped__()  # type: ignore[attr-defined]


# Replace recursive wrapper safely after function creation.
get_all_quiz_questions_from_data = (
    lambda: __import__(
        "modules.economy.data",
        fromlist=["get_all_quiz_questions"],
    ).get_all_quiz_questions()
)


# ==========================================================
# Curriculum Statistics
# ==========================================================

def get_curriculum_stats() -> dict[str, int]:

    try:
        stats = get_curriculum_statistics()
    except Exception:
        stats = {}

    if not isinstance(
        stats,
        Mapping,
    ):
        stats = {}

    return {
        "modules": int(
            stats.get(
                "modules",
                1,
            )
        ),
        "chapters": int(
            stats.get(
                "chapters",
                0,
            )
        ),
        "lessons": int(
            stats.get(
                "lessons",
                0,
            )
        ),
        "quiz_questions": int(
            stats.get(
                "quiz_questions",
                0,
            )
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

    results: list[
        dict[str, Any]
    ] = []

    for chapter in get_economy_chapters():

        chapter_id = str(
            chapter.get(
                "id",
                "",
            )
        ).strip()

        chapter_title = str(
            chapter.get(
                "title",
                "",
            )
        )

        chapter_description = str(
            chapter.get(
                "description",
                "",
            )
        )

        for lesson in get_economy_lessons(
            chapter_id
        ):

            lesson_id = str(
                lesson.get(
                    "id",
                    "",
                )
            ).strip()

            title = str(
                lesson.get(
                    "title",
                    "",
                )
            )

            content = str(
                lesson.get(
                    "content",
                    "",
                )
            )

            searchable = (
                f"{chapter_title}\n"
                f"{chapter_description}\n"
                f"{title}\n"
                f"{content}"
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
# Validation
# ==========================================================

def validate_module() -> dict[str, Any]:

    errors: list[str] = []
    warnings: list[str] = []

    chapters = get_economy_chapters()

    if not chapters:
        errors.append(
            "Economy curriculum has no chapters."
        )

    chapter_ids: set[str] = set()

    for chapter_index, chapter in enumerate(
        chapters,
        start=1,
    ):

        chapter_id = str(
            chapter.get(
                "id",
                "",
            )
        ).strip()

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

        if not chapter.get(
            "title"
        ):
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

        lesson_ids: set[str] = set()

        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):

            lesson_id = str(
                lesson.get(
                    "id",
                    "",
                )
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

            if not lesson.get(
                "title"
            ):
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
# Health Check
# ==========================================================

def service_health_check() -> bool:

    try:
        if not get_module_id():
            return False

        if not get_module_title():
            return False

        if not get_economy_chapters():
            return False

        validation = validate_module()

        return bool(
            validation.get(
                "valid",
                False,
            )
        )

    except Exception:
        return False


def economy_service_health_check() -> bool:
    return service_health_check()


# ==========================================================
# Public Exports
# ==========================================================

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


if __name__ == "__main__":
    print(
        "Economy Service Health:",
        service_health_check(),
    )

    print(
        "Module:",
        get_module_info(),
    )

    print(
        "Statistics:",
        get_curriculum_stats(),
    )
