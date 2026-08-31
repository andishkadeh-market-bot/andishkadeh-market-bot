"""
Service layer for Psychology & Social Work.

Andishkadeh Management & Market
"""

from __future__ import annotations

from typing import Any

from core.database import (
    upsert_chapter,
    upsert_lesson,
)
from core.progress import (
    mark_lesson_completed,
    mark_lesson_started,
)
from core.registry import registry
from core.statistics import record_quiz_result

from modules.psychology.data import (
    MODULE_ID,
    MODULE_TITLE,
    get_chapter,
    get_chapters,
    get_curriculum_statistics,
    get_lesson,
    get_lessons,
    get_quiz_questions,
)


def register_psychology_module() -> dict[str, int]:
    """
    Register the complete Psychology module.

    Registers:
    - Module
    - Chapters
    - Lessons
    - Lesson data
    - Database records
    """

    registry.register_module(
        module_id=MODULE_ID,
        title=MODULE_TITLE,
    )

    registered_chapters = 0
    registered_lessons = 0

    for chapter in get_chapters():
        chapter_id = chapter.get("id")

        if not chapter_id:
            continue

        chapter_id = str(chapter_id)

        chapter_title = str(
            chapter.get(
                "title",
                chapter_id,
            )
        )

        registry.register_chapter(
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            title=chapter_title,
        )

        upsert_chapter(
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            title=chapter_title,
        )

        registered_chapters += 1

        lessons = chapter.get(
            "lessons",
            [],
        )

        if not isinstance(lessons, list):
            continue

        for lesson in lessons:
            if not isinstance(lesson, dict):
                continue

            lesson_id = lesson.get("id")

            if not lesson_id:
                continue

            lesson_id = str(lesson_id)

            lesson_title = str(
                lesson.get(
                    "title",
                    lesson_id,
                )
            )

            registry.register_lesson(
                module_id=MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=lesson_title,
                data=lesson,
            )

            upsert_lesson(
                module_id=MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=lesson_title,
            )

            registered_lessons += 1

    return {
        "modules": 1,
        "chapters": registered_chapters,
        "lessons": registered_lessons,
    }


def start_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Register lesson start and return lesson data."""

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    mark_lesson_started(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    return lesson


def complete_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Mark a Psychology lesson as completed."""

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return False

    mark_lesson_completed(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    return True


def save_quiz_result(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
) -> int:
    """Save Psychology quiz result to Statistics."""

    return record_quiz_result(
        telegram_id=telegram_id,
        module_id=MODULE_ID,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
    )


def get_lesson_data(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return lesson data."""

    return get_lesson(
        chapter_id,
        lesson_id,
    )


def get_chapter_data(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return chapter data."""

    return get_chapter(
        chapter_id,
    )


def get_chapter_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return lessons of a chapter."""

    return get_lessons(
        chapter_id,
    )


def get_lesson_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return quiz questions for a lesson."""

    return get_quiz_questions(
        chapter_id,
        lesson_id,
    )


def get_psychology_statistics() -> dict[str, int]:
    """Return Psychology curriculum statistics."""

    return get_curriculum_statistics()


def psychology_service_health_check() -> bool:
    """Basic service-layer health check."""

    try:
        statistics = get_curriculum_statistics()

        return (
            isinstance(statistics, dict)
            and statistics.get("chapters", 0) > 0
            and statistics.get("lessons", 0) > 0
            and statistics.get("questions", 0) > 0
        )

    except Exception:
        return False
