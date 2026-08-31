"""
Management service layer for Andishkadeh Management & Market.

Responsibilities:
- Access Management curriculum data
- Retrieve chapters
- Retrieve lessons
- Retrieve lesson content
- Retrieve quiz questions
- Provide safe lookup helpers
- Keep business logic independent from Telegram handlers
"""

from __future__ import annotations

from typing import Any

from modules.management.data import (
    MANAGEMENT_DATA,
)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = "management"


# ==========================================================
# Internal helpers
# ==========================================================

def _normalize_id(value: Any) -> str:
    """Convert an identifier to a normalized string."""

    if value is None:
        return ""

    return str(value).strip()


def _get_chapters() -> list[dict[str, Any]]:
    """Return the complete Management chapter list."""

    if isinstance(MANAGEMENT_DATA, dict):

        chapters = MANAGEMENT_DATA.get(
            "chapters",
            [],
        )

        if isinstance(chapters, list):
            return chapters

    if isinstance(MANAGEMENT_DATA, list):
        return MANAGEMENT_DATA

    return []


def _get_chapter_lessons(
    chapter: dict[str, Any],
) -> list[dict[str, Any]]:
    """Extract lessons from a chapter."""

    lessons = chapter.get(
        "lessons",
        [],
    )

    if isinstance(lessons, list):
        return lessons

    return []


# ==========================================================
# Module
# ==========================================================

def get_module_id() -> str:
    """Return the Management module ID."""

    return MODULE_ID


def get_module_title() -> str:
    """Return the Management module title."""

    if isinstance(MANAGEMENT_DATA, dict):

        title = MANAGEMENT_DATA.get(
            "title"
        )

        if title:
            return str(title)

    return "آموزش مدیریت"


# ==========================================================
# Chapters
# ==========================================================

def get_chapters() -> list[dict[str, Any]]:
    """
    Return all Management chapters.

    Returns:
        A copy of the chapter list.
    """

    return [
        dict(chapter)
        for chapter in _get_chapters()
    ]


def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """
    Return one chapter by ID.
    """

    normalized_id = _normalize_id(
        chapter_id
    )

    if not normalized_id:
        return None

    for chapter in _get_chapters():

        current_id = _normalize_id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )

        if current_id == normalized_id:
            return dict(chapter)

    return None


def get_chapter_title(
    chapter_id: str,
) -> str | None:
    """Return the title of a chapter."""

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return None

    title = chapter.get("title")

    if title is None:
        return None

    return str(title)


def get_chapter_ids() -> list[str]:
    """Return all chapter IDs."""

    result: list[str] = []

    for chapter in _get_chapters():

        chapter_id = _normalize_id(
            chapter.get("id")
            or chapter.get("chapter_id")
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
    """
    Return all lessons belonging to a chapter.
    """

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return []

    return [
        dict(lesson)
        for lesson in _get_chapter_lessons(
            chapter
        )
    ]


def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Return one lesson by chapter and lesson ID.
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

    chapter = get_chapter(
        normalized_chapter_id
    )

    if chapter is None:
        return None

    for lesson in _get_chapter_lessons(
        chapter
    ):

        current_id = _normalize_id(
            lesson.get("id")
            or lesson.get("lesson_id")
        )

        if current_id == normalized_lesson_id:
            return dict(lesson)

    return None


def get_lesson_title(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    """Return the title of one lesson."""

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    title = lesson.get("title")

    if title is None:
        return None

    return str(title)


def get_lesson_ids(
    chapter_id: str,
) -> list[str]:
    """Return all lesson IDs in a chapter."""

    result: list[str] = []

    for lesson in get_lessons(
        chapter_id
    ):

        lesson_id = _normalize_id(
            lesson.get("id")
            or lesson.get("lesson_id")
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
    Return the complete lesson content.

    The returned dictionary is a copy so callers cannot
    accidentally modify the source curriculum.
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
    Return the primary textual content of a lesson.

    Supports common content field names.
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
        "description",
        "lesson_content",
        "body",
    )

    for key in content_keys:

        value = lesson.get(key)

        if isinstance(value, str):
            cleaned = value.strip()

            if cleaned:
                return cleaned

    return None


# ==========================================================
# Lesson metadata
# ==========================================================

def get_lesson_summary(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Return a compact lesson summary.
    """

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    return {
        "module_id": MODULE_ID,
        "chapter_id": _normalize_id(
            chapter_id
        ),
        "lesson_id": _normalize_id(
            lesson.get("id")
            or lesson.get("lesson_id")
        ),
        "title": lesson.get(
            "title",
            lesson_id,
        ),
    }


# ==========================================================
# Quiz questions
# ==========================================================

def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Return quiz questions for one Management lesson.

    Supports common quiz field names:
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
            list,
        ):

            return [
                dict(question)
                for question in questions
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
    """Return the number of quiz questions."""

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

        chapter_id = _normalize_id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )

        for lesson in _get_chapter_lessons(
            chapter
        ):

            lesson_id = _normalize_id(
                lesson.get("id")
                or lesson.get("lesson_id")
            )

            title = str(
                lesson.get(
                    "title",
                    "",
                )
            )

            content = get_lesson_text(
                chapter_id,
                lesson_id,
            ) or ""

            searchable_text = (
                f"{title}\n{content}"
            ).casefold()

            if (
                normalized_keyword
                in searchable_text
            ):

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
    """
    Return basic Management content statistics.
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

        chapter_id = _normalize_id(
            chapter.get("id")
            or chapter.get("chapter_id")
        )

        for lesson in lessons:

            lesson_id = _normalize_id(
                lesson.get("id")
                or lesson.get("lesson_id")
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
# Validation
# ==========================================================

def validate_management_data() -> dict[str, Any]:
    """
    Validate the Management curriculum structure.

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

        chapter_id = _normalize_id(
            chapter.get("id")
            or chapter.get("chapter_id")
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

        title = chapter.get(
            "title"
        )

        if not title:

            warnings.append(
                f"Chapter '{chapter_id or chapter_index}' has no title."
            )

        lessons = _get_chapter_lessons(
            chapter
        )

        if not lessons:

            warnings.append(
                f"Chapter '{chapter_id or chapter_index}' has no lessons."
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
                        f"lesson #{lesson_index} is not a dictionary."
                    )
                )

                continue

            lesson_id = _normalize_id(
                lesson.get("id")
                or lesson.get("lesson_id")
            )

            if not lesson_id:

                errors.append(
                    (
                        f"Chapter '{chapter_id}' "
                        f"lesson #{lesson_index} has no ID."
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
                        f"in chapter '{chapter_id}' has no title."
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
    Check whether the Management service is usable.
    """

    try:

        report = validate_management_data()

        return bool(
            report["valid"]
        )

    except Exception:
        return False
