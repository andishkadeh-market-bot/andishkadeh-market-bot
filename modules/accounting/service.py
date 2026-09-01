"""
Accounting Service Layer
Andishkadeh Management & Market
"""

from __future__ import annotations

from typing import Any

from .data import (
    MODULE_INFO,
    ACCOUNTING_CHAPTERS,
    get_all_quiz_questions as _get_all_quiz_questions,
)


def get_module_title() -> str:
    return str(MODULE_INFO.get("title", "🧾 حسابداری تخصصی"))


def get_module_info() -> dict[str, Any]:
    return dict(MODULE_INFO)


def get_accounting_chapters() -> list[dict[str, Any]]:
    return ACCOUNTING_CHAPTERS


def get_accounting_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:

    for chapter in ACCOUNTING_CHAPTERS:
        if str(chapter.get("id")) == str(chapter_id):
            return chapter

    return None


def get_accounting_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:

    chapter = get_accounting_chapter(chapter_id)

    if chapter is None:
        return []

    lessons = chapter.get("lessons", [])

    if not isinstance(lessons, list):
        return []

    return lessons


def get_accounting_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    for lesson in get_accounting_lessons(chapter_id):
        if str(lesson.get("id")) == str(lesson_id):
            return lesson

    return None


def get_accounting_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    quiz = lesson.get("quiz", [])

    if not isinstance(quiz, list):
        return []

    return quiz


def get_all_quiz_questions() -> list[dict[str, Any]]:
    return _get_all_quiz_questions()


def get_curriculum_stats() -> dict[str, int]:

    chapters = len(ACCOUNTING_CHAPTERS)

    lessons = 0
    quiz_questions = 0

    for chapter in ACCOUNTING_CHAPTERS:
        chapter_lessons = chapter.get("lessons", [])

        if not isinstance(chapter_lessons, list):
            continue

        lessons += len(chapter_lessons)

        for lesson in chapter_lessons:
            quiz = lesson.get("quiz", [])

            if isinstance(quiz, list):
                quiz_questions += len(quiz)

    return {
        "chapters": chapters,
        "lessons": lessons,
        "quiz_questions": quiz_questions,
    }


def search_accounting_content(
    keyword: str,
) -> list[dict[str, Any]]:

    query = str(keyword or "").strip().lower()

    if not query:
        return []

    results: list[dict[str, Any]] = []

    for chapter in ACCOUNTING_CHAPTERS:

        chapter_text = " ".join(
            [
                str(chapter.get("title", "")),
                str(chapter.get("description", "")),
            ]
        ).lower()

        for lesson in chapter.get("lessons", []):

            lesson_text = " ".join(
                [
                    str(lesson.get("title", "")),
                    str(lesson.get("content", "")),
                    " ".join(
                        map(
                            str,
                            lesson.get("keywords", []),
                        )
                    ),
                ]
            ).lower()

            if query in chapter_text or query in lesson_text:

                results.append(
                    {
                        "chapter_id": chapter.get("id"),
                        "chapter_title": chapter.get("title"),
                        "lesson_id": lesson.get("id"),
                        "lesson_title": lesson.get("title"),
                    }
                )

    return results


__all__ = [
    "get_module_title",
    "get_module_info",
    "get_accounting_chapters",
    "get_accounting_chapter",
    "get_accounting_lessons",
    "get_accounting_lesson",
    "get_accounting_quiz",
    "get_all_quiz_questions",
    "get_curriculum_stats",
    "search_accounting_content",
]
