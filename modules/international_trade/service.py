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
- Record quiz attempts when supported
- Provide curriculum statistics
- Provide health checks
- Keep business logic independent from Telegram handlers
Important:
- This file NEVER imports itself.
- Curriculum data comes from modules.international_trade.data.
- Statistics compatibility is handled safely.
"""
from __future__ import annotations
from typing import Any, Mapping
from core.progress import (
    mark_lesson_completed,
    mark_lesson_started,
)
from modules.international_trade.data import (
    MODULE_ID,
    MODULE_TITLE,
    get_chapter,
    get_chapters,
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
        "description": "آموزش تخصصی تجارت بین‌الملل",
    }
# ==========================================================
# Chapters
# ==========================================================
def get_trade_chapters() -> list[dict[str, Any]]:
    """
    Return all International Trade chapters.
    Compatibility API used by handlers.
    """
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
    try:
        chapter = get_chapter(
            normalized_id
        )
    except Exception:
        return None
    if chapter is None:
        return None
    if isinstance(
        chapter,
        Mapping,
    ):
        return dict(chapter)
    return None
# Alias used by some handlers
def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Compatibility alias for chapter lookup."""
    return get_trade_chapter(
        chapter_id
    )
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
    try:
        lessons = get_lessons(
            normalized_id
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
    try:
        lesson = get_lesson(
            normalized_chapter_id,
            normalized_lesson_id,
        )
    except Exception:
        return None
    if lesson is None:
        return None
    if isinstance(
        lesson,
        Mapping,
    ):
        return dict(lesson)
    return None
# Compatibility aliases
def get_lesson_by_id(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Compatibility alias for lesson lookup."""
    return get_trade_lesson(
        chapter_id,
        lesson_id,
    )
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
    try:
        questions = get_quiz_questions(
            chapter_id,
            lesson_id,
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
# Additional compatibility alias
def get_quiz_questions_for_lesson(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Compatibility alias for quiz lookup."""
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
    try:
        mark_lesson_started(
            telegram_id=telegram_id,
            module_id=get_module_id(),
            chapter_id=str(
                chapter_id
            ),
            lesson_id=str(
                lesson_id
            ),
        )
    except Exception:
        return None
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
    try:
        mark_lesson_completed(
            telegram_id=telegram_id,
            module_id=get_module_id(),
            chapter_id=str(
                chapter_id
            ),
            lesson_id=str(
                lesson_id
            ),
        )
    except Exception:
        return False
    return True
# ==========================================================
# Quiz Statistics Compatibility
# ==========================================================
def _load_statistics_function():
    """
    Try to locate an available statistics recording
    function without creating a hard import dependency.
    This prevents International Trade from crashing during
    application startup when the Statistics API changes.
    """
    try:
        import core.statistics as statistics
    except Exception:
        return None
    candidates = (
        "record_quiz_attempt",
        "record_quiz_result",
        "save_quiz_result",
        "record_attempt",
    )
    for function_name in candidates:
        function = getattr(
            statistics,
            function_name,
            None,
        )
        if callable(function):
            return function
    return None
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
    The function attempts to use whichever compatible
    Statistics API is currently available.
    If no compatible Statistics function exists, the quiz
    result is still considered successfully processed and
    zero is returned as a neutral record identifier.
    """
    function = _load_statistics_function()
    if function is None:
        return 0
    payload = {
        "telegram_id": telegram_id,
        "module_id": get_module_id(),
        "chapter_id": str(
            chapter_id
        ),
        "lesson_id": str(
            lesson_id
        ),
        "total_questions": int(
            total_questions
        ),
        "correct_answers": int(
            correct_answers
        ),
        "score": (
            float(score)
            if score is not None
            else None
        ),
    }
    # ------------------------------------------------------
    # Try keyword-based API
    # ------------------------------------------------------
    try:
        result = function(
            **payload
        )
        if result is None:
            return 0
        if isinstance(
            result,
            bool,
        ):
            return int(result)
        if isinstance(
            result,
            int,
        ):
            return result
        try:
            return int(result)
        except Exception:
            return 0
    except TypeError:
        pass
    except Exception:
        return 0
    # ------------------------------------------------------
    # Compatibility fallback
    # ------------------------------------------------------
    try:
        result = function(
            telegram_id,
            get_module_id(),
            str(chapter_id),
            str(lesson_id),
            int(total_questions),
            int(correct_answers),
            (
                float(score)
                if score is not None
                else None
            ),
        )
        if result is None:
            return 0
        try:
            return int(result)
        except Exception:
            return 0
    except Exception:
        return 0
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
# Curriculum Statistics
# ==========================================================
def get_curriculum_stats() -> dict[str, int]:
    """
    Calculate International Trade curriculum statistics
    directly from the curriculum data.
    This function intentionally does NOT import
    get_curriculum_statistics from data.py.
    """
    chapters = get_trade_chapters()
    lesson_count = 0
    quiz_question_count = 0
    for chapter in chapters:
        chapter_id = str(
            chapter.get("id")
            or chapter.get(
                "chapter_id",
                "",
            )
        ).strip()
        if not chapter_id:
            continue
        lessons = get_trade_lessons(
            chapter_id
        )
        lesson_count += len(
            lessons
        )
        for lesson in lessons:
            lesson_id = str(
                lesson.get("id")
                or lesson.get(
                    "lesson_id",
                    "",
                )
            ).strip()
            if not lesson_id:
                continue
            quiz_question_count += len(
                get_trade_quiz(
                    chapter_id,
                    lesson_id,
                )
            )
    return {
        "modules": 1,
        "chapters": len(
            chapters
        ),
        "lessons": lesson_count,
        "quiz_questions": quiz_question_count,
    }
# Compatibility aliases
def get_curriculum_statistics() -> dict[str, int]:
    """
    Compatibility alias for curriculum statistics.
    """
    return get_curriculum_stats()
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
            chapter.get("id")
            or chapter.get(
                "chapter_id",
                "",
            )
        ).strip()
        if not chapter_id:
            continue
        for lesson in get_trade_lessons(
            chapter_id
        ):
            lesson_id = str(
                lesson.get("id")
                or lesson.get(
                    "lesson_id",
                    "",
                )
            ).strip()
            if not lesson_id:
                continue
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
            if (
                normalized_keyword
                in searchable_text
            ):
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
# Module Validation
# ==========================================================
def validate_module() -> dict[str, Any]:
    """
    Validate the International Trade curriculum.
    """
    errors: list[str] = []
    warnings: list[str] = []
    chapters = get_trade_chapters()
    if not chapters:
        warnings.append(
            "No International Trade chapters found."
        )
    chapter_ids: set[str] = set()
    for chapter_index, chapter in enumerate(
        chapters,
        start=1,
    ):
        chapter_id = str(
            chapter.get("id")
            or chapter.get(
                "chapter_id",
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
        lessons = get_trade_lessons(
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
                or lesson.get(
                    "lesson_id",
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
def international_trade_service_health_check() -> bool:
    """
    Check International Trade service integrity.
    """
    try:
        if not get_module_id():
            return False
        if not get_module_title():
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
    "get_chapter_by_id",
    "get_trade_lessons",
    "get_trade_lesson",
    "get_lesson_by_id",
    "get_trade_lesson_content",
    "get_trade_lesson_text",
    "get_trade_quiz",
    "get_trade_quiz_questions",
    "get_quiz_questions_for_lesson",
    "start_lesson",
    "complete_lesson",
    "save_quiz_result",
    "record_trade_quiz_attempt",
    "get_curriculum_stats",
    "get_curriculum_statistics",
    "get_module_statistics",
    "search_lessons",
    "validate_module",
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
