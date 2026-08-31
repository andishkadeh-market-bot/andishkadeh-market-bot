"""
International Trade service layer.
Andishkadeh Management & Market
Responsibilities:
- Load International Trade curriculum
- Retrieve module information
- Retrieve chapters
- Retrieve lessons
- Retrieve lesson content
- Retrieve quiz questions
- Record quiz attempts
- Provide health checks
- Keep business logic independent from Telegram handlers
Important:
This file must NEVER import itself.
All curriculum data must come from modules.international_trade.data.
"""
from __future__ import annotations
from typing import Any, Mapping
from core.progress import (
    mark_lesson_completed,
    mark_lesson_started,
)
from core.statistics import (
    record_quiz_attempt,
)
from modules.international_trade.data import (
    MODULE_ID,
    MODULE_TITLE,
    get_chapter,
    get_chapters,
    get_curriculum_statistics,
    get_lesson,
    get_lessons,
    get_quiz_questions,
)
# ==========================================================
# Module Information
# ==========================================================
def get_module_id() -> str:
    """Return the International Trade module ID."""
    return str(MODULE_ID)
def get_module_title() -> str:
    """Return the International Trade module title."""
    return str(MODULE_TITLE)
def get_module_info() -> dict[str, str]:
    """Return basic module information."""
    return {
        "id": get_module_id(),
        "module_id": get_module_id(),
        "title": get_module_title(),
    }
# ==========================================================
# Chapters
# ==========================================================
def get_trade_chapters() -> list[dict[str, Any]]:
    """
    Return all International Trade chapters.
    Compatibility API used by handlers.
    """
    chapters = get_chapters()
    if not isinstance(chapters, list):
        return []
    return [
        dict(chapter)
        for chapter in chapters
        if isinstance(chapter, Mapping)
    ]
def get_trade_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """
    Return one International Trade chapter.
    """
    if chapter_id is None:
        return None
    normalized_id = str(
        chapter_id
    ).strip()
    if not normalized_id:
        return None
    chapter = get_chapter(
        normalized_id
    )
    if chapter is None:
        return None
    if isinstance(chapter, Mapping):
        return dict(chapter)
    return None
# ==========================================================
# Lessons
# ==========================================================
def get_trade_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """
    Return all lessons of a chapter.
    Compatibility API used by handlers.
    """
    if chapter_id is None:
        return []
    normalized_id = str(
        chapter_id
    ).strip()
    if not normalized_id:
        return []
    lessons = get_lessons(
        normalized_id
    )
    if not isinstance(lessons, list):
        return []
    return [
        dict(lesson)
        for lesson in lessons
        if isinstance(lesson, Mapping)
    ]
def get_trade_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Return one International Trade lesson.
    """
    if (
        chapter_id is None
        or lesson_id is None
    ):
        return None
    normalized_chapter_id = str(
        chapter_id
    ).strip()
    normalized_lesson_id = str(
        lesson_id
    ).strip()
    if (
        not normalized_chapter_id
        or not normalized_lesson_id
    ):
        return None
    lesson = get_lesson(
        normalized_chapter_id,
        normalized_lesson_id,
    )
    if lesson is None:
        return None
    if isinstance(lesson, Mapping):
        return dict(lesson)
    return None
# ==========================================================
# Lesson Content
# ==========================================================
def get_trade_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Return complete lesson content.
    """
    lesson = get_trade_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    return dict(lesson)
def get_trade_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:
    """
    Return the primary text content of a lesson.
    """
    lesson = get_trade_lesson(
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
        if isinstance(
            value,
            str,
        ):
            cleaned = value.strip()
            if cleaned:
                return cleaned
    return None
# ==========================================================
# Quiz
# ==========================================================
def get_trade_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Return quiz questions for a lesson.
    Compatibility API used by handlers.
    """
    if (
        chapter_id is None
        or lesson_id is None
    ):
        return []
    questions = get_quiz_questions(
        chapter_id,
        lesson_id,
    )
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
def get_trade_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Explicit quiz-question API.
    """
    return get_trade_quiz(
        chapter_id,
        lesson_id,
    )
# ==========================================================
# Lesson Start
# ==========================================================
def start_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Register lesson start and return lesson data.
    """
    if telegram_id <= 0:
        return None
    lesson = get_trade_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return None
    mark_lesson_started(
        telegram_id=telegram_id,
        module_id=get_module_id(),
        chapter_id=str(chapter_id),
        lesson_id=str(lesson_id),
    )
    return lesson
# ==========================================================
# Lesson Completion
# ==========================================================
def complete_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """
    Mark an International Trade lesson as completed.
    """
    if telegram_id <= 0:
        return False
    lesson = get_trade_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return False
    mark_lesson_completed(
        telegram_id=telegram_id,
        module_id=get_module_id(),
        chapter_id=str(chapter_id),
        lesson_id=str(lesson_id),
    )
    return True
# ==========================================================
# Quiz Result
# ==========================================================
def save_quiz_result(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """
    Save an International Trade quiz result.
    """
    return record_quiz_attempt(
        telegram_id=telegram_id,
        module_id=get_module_id(),
        chapter_id=str(chapter_id),
        lesson_id=str(lesson_id),
        total_questions=int(
            total_questions
        ),
        correct_answers=int(
            correct_answers
        ),
        score=(
            float(score)
            if score is not None
            else None
        ),
    )
def record_trade_quiz_attempt(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """
    Compatibility wrapper for trade handlers.
    """
    return save_quiz_result(
        telegram_id=telegram_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
    )
# ==========================================================
# Statistics
# ==========================================================
def get_curriculum_stats() -> dict[str, int]:
    """
    Return curriculum statistics.
    """
    statistics = get_curriculum_statistics()
    if not isinstance(
        statistics,
        Mapping,
    ):
        return {
            "modules": 1,
            "chapters": 0,
            "lessons": 0,
            "quiz_questions": 0,
        }
    return {
        "modules": int(
            statistics.get(
                "modules",
                1,
            )
        ),
        "chapters": int(
            statistics.get(
                "chapters",
                0,
            )
        ),
        "lessons": int(
            statistics.get(
                "lessons",
                0,
            )
        ),
        "quiz_questions": int(
            statistics.get(
                "quiz_questions",
                statistics.get(
                    "questions",
                    0,
                ),
            )
        ),
    }
def get_module_statistics() -> dict[str, Any]:
    """
    Return complete module statistics.
    """
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
    """
    Search International Trade lessons by title/content.
    """
    if keyword is None:
        return []
    normalized_keyword = str(
        keyword
    ).strip().casefold()
    if not normalized_keyword:
        return []
    results: list[
        dict[str, Any]
    ] = []
    for chapter in get_trade_chapters():
        chapter_id = str(
            chapter.get(
                "id",
                chapter.get(
                    "chapter_id",
                    "",
                ),
            )
        ).strip()
        if not chapter_id:
            continue
        for lesson in get_trade_lessons(
            chapter_id
        ):
            lesson_id = str(
                lesson.get(
                    "id",
                    lesson.get(
                        "lesson_id",
                        "",
                    ),
                )
            ).strip()
            title = str(
                lesson.get(
                    "title",
                    "",
                )
            )
            content = (
                get_trade_lesson_text(
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
                        "module_id": get_module_id(),
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "title": title,
                    }
                )
    return results
# ==========================================================
# Health Check
# ==========================================================
def international_trade_service_health_check() -> bool:
    """
    Check International Trade service integrity.
    """
    try:
        module_info = get_module_info()
        if not isinstance(
            module_info,
            dict,
        ):
            return False
        if not module_info.get(
            "id"
        ):
            return False
        if not module_info.get(
            "title"
        ):
            return False
        chapters = get_trade_chapters()
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
                or chapter.get(
                    "chapter_id"
                )
            )
            if not chapter_id:
                return False
            lessons = get_trade_lessons(
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
    """
    Generic service health-check alias.
    """
    return international_trade_service_health_check()
# ==========================================================
# Public Exports
# ==========================================================
__all__ = [
    "get_module_id",
    "get_module_title",
    "get_module_info",
    "get_trade_chapters",
    "get_trade_chapter",
    "get_trade_lessons",
    "get_trade_lesson",
    "get_trade_lesson_content",
    "get_trade_lesson_text",
    "get_trade_quiz",
    "get_trade_quiz_questions",
    "start_lesson",
    "complete_lesson",
    "save_quiz_result",
    "record_trade_quiz_attempt",
    "get_curriculum_stats",
    "get_module_statistics",
    "search_lessons",
    "international_trade_service_health_check",
    "service_health_check",
]
# ==========================================================
# Local Test
# ==========================================================
if __name__ == "__main__":
    print(
        "International Trade Service Health:",
        international_trade_service_health_check(),
    )
    print(
        "Module:",
        get_module_info(),
    )
    print(
        "Statistics:",
        get_curriculum_stats(),
    )
