"""
Unified data layer for Psychology & Social Work.
Andishkadeh Management & Market
این فایل منبع محتوای آموزشی را از
psychology_socialwork.py
دریافت و برای handlers/service استاندارد می‌کند.
نکته:
محتوای تخصصی اصلی حذف یا کپی نمی‌شود.
psychology_socialwork.py منبع اصلی Curriculum است.
"""
from __future__ import annotations
from typing import Any
from modules.psychology import psychology_socialwork as content
# ==========================================================
# Module Identity
# ==========================================================
MODULE_ID = getattr(
    content,
    "MODULE_ID",
    "psychology_socialwork",
)
MODULE_TITLE = getattr(
    content,
    "MODULE_TITLE",
    "🧠 روانشناسی و مددکاری",
)
MODULE_DESCRIPTION = getattr(
    content,
    "MODULE_DESCRIPTION",
    "دوره جامع روانشناسی و مددکاری اجتماعی.",
)
MODULE_VERSION = getattr(
    content,
    "MODULE_VERSION",
    "1.0.0",
)
CONTENT_NOTE = getattr(
    content,
    "CONTENT_NOTE",
    (
        "این محتوا آموزشی است و جایگزین تشخیص، درمان، "
        "مشاوره تخصصی یا نظر متخصص واجد صلاحیت نیست."
    ),
)
# ==========================================================
# Internal Helpers
# ==========================================================
def _as_dict(value: Any) -> dict[str, Any] | None:
    """Return value as dictionary when possible."""
    if not isinstance(value, dict):
        return None
    return value
def _text(value: Any, default: str = "") -> str:
    """Normalize text."""
    if value is None:
        return default
    result = str(value).strip()
    return result if result else default
def _normalize_points(
    lesson: dict[str, Any],
    primary_key: str,
    fallback_key: str,
) -> list[str]:
    """
    Normalize lesson point lists.
    Supports both:
    - special_points / exam_points
    - specialized_notes / exam_notes
    """
    value = lesson.get(primary_key)
    if not isinstance(value, list):
        value = lesson.get(fallback_key, [])
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            result.append(text)
    return result
def _normalize_options(
    raw_options: Any,
) -> list[str]:
    """
    Normalize quiz options.
    Supported formats:
    1. ["A", "B", "C", "D"]
    2. [
        {"id": "A", "text": "..."},
        {"id": "B", "text": "..."},
    ]
    """
    if not isinstance(raw_options, list):
        return []
    result: list[str] = []
    for option in raw_options:
        if isinstance(option, dict):
            value = (
                option.get("text")
                or option.get("label")
                or option.get("value")
            )
        else:
            value = option
        if value is None:
            continue
        text = str(value).strip()
        if text:
            result.append(text)
    return result
def _normalize_answer(
    raw_answer: Any,
    raw_options: Any,
) -> str:
    """
    Normalize correct answer.
    The source module may store the answer as:
    - option letter: A / B / C / D
    - option text
    """
    answer = _text(raw_answer)
    if not answer:
        return ""
    options = (
        raw_options
        if isinstance(raw_options, list)
        else []
    )
    normalized_options = _normalize_options(
        options
    )
    # If answer is an option index/letter,
    # resolve it to the actual option text.
    answer_upper = answer.upper()
    letter_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }
    if answer_upper in letter_map:
        index = letter_map[answer_upper]
        if index < len(normalized_options):
            return normalized_options[index]
    # Persian option labels
    persian_map = {
        "الف": 0,
        "ب": 1,
        "ج": 2,
        "د": 3,
    }
    if answer in persian_map:
        index = persian_map[answer]
        if index < len(normalized_options):
            return normalized_options[index]
    return answer
def _normalize_question(
    raw_question: Any,
    fallback_id: str,
) -> dict[str, Any] | None:
    """Normalize one quiz question."""
    if not isinstance(raw_question, dict):
        return None
    question_text = (
        raw_question.get("question")
        or raw_question.get("text")
    )
    question_text = _text(
        question_text
    )
    if not question_text:
        return None
    question_id = _text(
        raw_question.get("id"),
        fallback_id,
    )
    raw_options = raw_question.get(
        "options",
        [],
    )
    normalized_options = _normalize_options(
        raw_options
    )
    if not normalized_options:
        return None
    raw_answer = (
        raw_question.get("correct_answer")
        or raw_question.get("answer")
        or raw_question.get("correct")
    )
    correct_answer = _normalize_answer(
        raw_answer,
        raw_options,
    )
    explanation = _text(
        raw_question.get("explanation")
        or raw_question.get("feedback"),
        "پاسخ بر اساس محتوای آموزشی این درس تعیین شده است.",
    )
    return {
        "id": question_id,
        "question": question_text,
        "options": normalized_options,
        "correct_answer": correct_answer,
        "answer": correct_answer,
        "explanation": explanation,
    }
def _normalize_lesson(
    raw_lesson: Any,
    chapter_id: str,
    index: int,
) -> dict[str, Any] | None:
    """Normalize one lesson."""
    if not isinstance(raw_lesson, dict):
        return None
    lesson_id = _text(
        raw_lesson.get("id"),
        f"{chapter_id}_lesson_{index}",
    )
    title = _text(
        raw_lesson.get("title"),
        lesson_id,
    )
    content_text = _text(
        raw_lesson.get("content"),
        "محتوای این درس هنوز ثبت نشده است.",
    )
    example = _text(
        raw_lesson.get("example")
        or raw_lesson.get("practical_example"),
        "-",
    )
    special_points = _normalize_points(
        raw_lesson,
        "special_points",
        "specialized_notes",
    )
    exam_points = _normalize_points(
        raw_lesson,
        "exam_points",
        "exam_notes",
    )
    raw_questions = raw_lesson.get(
        "questions",
        [],
    )
    questions: list[dict[str, Any]] = []
    if isinstance(raw_questions, list):
        for q_index, raw_question in enumerate(
            raw_questions,
            start=1,
        ):
            normalized = _normalize_question(
                raw_question,
                f"{lesson_id}_q{q_index}",
            )
            if normalized is not None:
                questions.append(
                    normalized
                )
    return {
        "id": lesson_id,
        "title": title,
        "content": content_text,
        "example": example,
        "special_points": special_points,
        "exam_points": exam_points,
        "questions": questions,
        # Preserve the original fields too.
        "specialized_notes": special_points,
        "exam_notes": exam_points,
    }
def _normalize_chapter(
    raw_chapter: Any,
    index: int,
) -> dict[str, Any] | None:
    """Normalize one chapter."""
    if not isinstance(raw_chapter, dict):
        return None
    chapter_id = _text(
        raw_chapter.get("id"),
        f"chapter_{index}",
    )
    title = _text(
        raw_chapter.get("title"),
        chapter_id,
    )
    description = _text(
        raw_chapter.get("description"),
        "",
    )
    raw_lessons = raw_chapter.get(
        "lessons",
        [],
    )
    lessons: list[dict[str, Any]] = []
    if isinstance(raw_lessons, list):
        for lesson_index, raw_lesson in enumerate(
            raw_lessons,
            start=1,
        ):
            normalized = _normalize_lesson(
                raw_lesson,
                chapter_id,
                lesson_index,
            )
            if normalized is not None:
                lessons.append(
                    normalized
                )
    return {
        "id": chapter_id,
        "title": title,
        "description": description,
        "lessons": lessons,
    }
# ==========================================================
# Source Curriculum Discovery
# ==========================================================
def _load_source_chapters() -> list[dict[str, Any]]:
    """
    Load chapters from psychology_socialwork.py.
    Preferred source:
        CHAPTER_1 ... CHAPTER_12
    If a future version exposes:
        PSYCHOLOGY_CURRICULUM
    that structure is also supported.
    """
    raw_chapters: list[Any] = []
    # ------------------------------------------------------
    # Preferred structure: CHAPTER_1 ... CHAPTER_12
    # ------------------------------------------------------
    for index in range(1, 13):
        chapter = getattr(
            content,
            f"CHAPTER_{index}",
            None,
        )
        if chapter is not None:
            raw_chapters.append(
                chapter
            )
    # ------------------------------------------------------
    # Fallback structure
    # ------------------------------------------------------
    if not raw_chapters:
        curriculum = getattr(
            content,
            "PSYCHOLOGY_CURRICULUM",
            None,
        )
        if isinstance(
            curriculum,
            list,
        ):
            raw_chapters = list(
                curriculum
            )
    normalized: list[dict[str, Any]] = []
    for index, raw_chapter in enumerate(
        raw_chapters,
        start=1,
    ):
        chapter = _normalize_chapter(
            raw_chapter,
            index,
        )
        if chapter is not None:
            normalized.append(
                chapter
            )
    return normalized
# Load once.
PSYCHOLOGY_CURRICULUM: list[
    dict[str, Any]
] = _load_source_chapters()
# ==========================================================
# Public API
# ==========================================================
def get_chapters() -> list[dict[str, Any]]:
    """Return all Psychology chapters."""
    return list(
        PSYCHOLOGY_CURRICULUM
    )
def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return one chapter by ID."""
    chapter_id = str(
        chapter_id
    ).strip()
    for chapter in PSYCHOLOGY_CURRICULUM:
        if str(
            chapter.get("id", "")
        ) == chapter_id:
            return chapter
    return None
def get_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return all lessons of a chapter."""
    chapter = get_chapter(
        chapter_id
    )
    if chapter is None:
        return []
    lessons = chapter.get(
        "lessons",
        [],
    )
    if not isinstance(
        lessons,
        list,
    ):
        return []
    return list(lessons)
def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return one lesson."""
    lesson_id = str(
        lesson_id
    ).strip()
    for lesson in get_lessons(
        chapter_id
    ):
        if str(
            lesson.get("id", "")
        ) == lesson_id:
            return lesson
    return None
def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return normalized quiz questions."""
    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        return []
    questions = lesson.get(
        "questions",
        [],
    )
    if not isinstance(
        questions,
        list,
    ):
        return []
    return list(questions)
def get_curriculum_statistics() -> dict[str, int]:
    """Return curriculum statistics."""
    chapters = get_chapters()
    lessons_count = 0
    questions_count = 0
    for chapter in chapters:
        lessons = chapter.get(
            "lessons",
            [],
        )
        if not isinstance(
            lessons,
            list,
        ):
            continue
        lessons_count += len(
            lessons
        )
        for lesson in lessons:
            questions = lesson.get(
                "questions",
                [],
            )
            if isinstance(
                questions,
                list,
            ):
                questions_count += len(
                    questions
                )
    return {
        "chapters": len(chapters),
        "lessons": lessons_count,
        "questions": questions_count,
    }
def psychology_data_health_check() -> bool:
    """
    Validate that the unified content layer
    contains the expected 12 chapters.
    """
    try:
        statistics = (
            get_curriculum_statistics()
        )
        return (
            statistics["chapters"] == 12
            and statistics["lessons"] > 0
            and statistics["questions"] > 0
        )
    except Exception:
        return False
