"""
International Trade Service Layer
Andishkadeh Management & Market
Responsibilities:
- Load International Trade curriculum
- Retrieve module information
- Retrieve chapters
- Retrieve lessons
- Retrieve lesson content
- Normalize quiz questions
- Normalize correct answers
- Record lesson progress
- Record quiz attempts through compatible Statistics APIs
- Provide curriculum statistics
- Search lessons
- Validate curriculum
- Provide health checks
Design:
- Business logic stays independent from Telegram handlers.
- Curriculum data is loaded from modules.international_trade.data.
- The public API keeps compatibility with existing handlers.
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
# Constants
# ==========================================================
MODULE_DESCRIPTION = (
    "آموزش تخصصی و کاربردی تجارت بین‌الملل از مبانی "
    "تجارت و نظریه‌های اقتصادی تا قراردادها، اینکوترمز، "
    "پرداخت‌های بین‌المللی، گمرک، لجستیک، بیمه، WTO "
    "و تجارت دیجیتال."
)
SUPPORTED_OPTION_IDS = ("A", "B", "C", "D")
PERSIAN_OPTION_IDS = {
    "الف": 0,
    "ب": 1,
    "ج": 2,
    "د": 3,
}
ARABIC_OPTION_IDS = {
    "ا": 0,
    "ب": 1,
    "ج": 2,
    "د": 3,
}
ENGLISH_OPTION_IDS = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}
# ==========================================================
# Generic Helpers
# ==========================================================
def _safe_text(
    value: Any,
    default: str = "",
) -> str:
    """Safely convert a value to stripped text."""
    if value is None:
        return default
    try:
        text = str(value).strip()
    except Exception:
        return default
    return text if text else default
def _safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """Safely convert a value to int."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
def _safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
def _mapping_copy(
    value: Any,
) -> dict[str, Any] | None:
    """Return a dictionary copy when value is mapping-like."""
    if isinstance(value, Mapping):
        return dict(value)
    return None
def _first_value(
    mapping: Mapping[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    """Return the first meaningful value from a mapping."""
    for key in keys:
        value = mapping.get(key)
        if value is None:
            continue
        if isinstance(value, str):
            if value.strip():
                return value
            continue
        return value
    return default
# ==========================================================
# Module Information
# ==========================================================
def get_module_id() -> str:
    """Return the International Trade module ID."""
    return str(MODULE_ID)
def get_module_title() -> str:
    """Return the International Trade module title."""
    return str(MODULE_TITLE)
def get_module_info() -> dict[str, Any]:
    """Return complete module information."""
    return {
        "id": get_module_id(),
        "module_id": get_module_id(),
        "title": get_module_title(),
        "description": MODULE_DESCRIPTION,
        "language": "fa",
        "level": "تخصصی",
    }
# ==========================================================
# Chapter APIs
# ==========================================================
def get_trade_chapters() -> list[dict[str, Any]]:
    """Return all International Trade chapters."""
    try:
        chapters = get_chapters()
    except Exception:
        return []
    if not isinstance(chapters, list):
        return []
    result: list[dict[str, Any]] = []
    for chapter in chapters:
        normalized = _mapping_copy(chapter)
        if normalized is not None:
            result.append(normalized)
    return result
def get_trade_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return one International Trade chapter."""
    chapter_id = _safe_text(chapter_id)
    if not chapter_id:
        return None
    try:
        chapter = get_chapter(chapter_id)
    except Exception:
        return None
    return _mapping_copy(chapter)
def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Compatibility alias for chapter lookup."""
    return get_trade_chapter(chapter_id)
# ==========================================================
# Lesson APIs
# ==========================================================
def get_trade_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return all lessons belonging to a chapter."""
    chapter_id = _safe_text(chapter_id)
    if not chapter_id:
        return []
    try:
        lessons = get_lessons(chapter_id)
    except Exception:
        return []
    if not isinstance(lessons, list):
        return []
    result: list[dict[str, Any]] = []
    for lesson in lessons:
        normalized = _mapping_copy(lesson)
        if normalized is not None:
            result.append(normalized)
    return result
def get_trade_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return one International Trade lesson."""
    chapter_id = _safe_text(chapter_id)
    lesson_id = _safe_text(lesson_id)
    if not chapter_id or not lesson_id:
        return None
    try:
        lesson = get_lesson(
            chapter_id,
            lesson_id,
        )
    except Exception:
        return None
    return _mapping_copy(lesson)
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
    """Return complete lesson content."""
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
    Return the primary textual content of a lesson.
    The data layer may use different keys depending on
    the lesson schema, so several compatible keys are checked.
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
        "article",
        "explanation",
    )
    for key in content_keys:
        value = lesson.get(key)
        if isinstance(value, str):
            text = value.strip()
            if text:
                return text
    return None
# ==========================================================
# Quiz Answer Normalization
# ==========================================================
def _normalize_option_index(
    value: Any,
    options: list[Any] | None = None,
) -> int | None:
    """
    Convert different answer formats to a zero-based index.
    Supported:
    - 0, 1, 2, 3
    - 1, 2, 3, 4
    - A, B, C, D
    - a, b, c, d
    - الف، ب، ج، د
    - option text
    - option dictionaries containing id/key/text/value
    """
    if value is None:
        return None
    # ------------------------------------------------------
    # Boolean is not a valid option index.
    # ------------------------------------------------------
    if isinstance(value, bool):
        return None
    # ------------------------------------------------------
    # Direct integer.
    #
    # The canonical internal representation is zero-based.
    # However, 1-4 is also accepted for compatibility.
    # ------------------------------------------------------
    if isinstance(value, int):
        if 0 <= value <= 3:
            return value
        if 1 <= value <= 4:
            return value - 1
        return None
    text = _safe_text(value)
    if not text:
        return None
    # ------------------------------------------------------
    # Remove common punctuation around option labels.
    # ------------------------------------------------------
    normalized = (
        text
        .strip()
        .upper()
        .replace(")", "")
        .replace("(", "")
        .replace(".", "")
        .replace(":", "")
        .replace("،", "")
        .strip()
    )
    # ------------------------------------------------------
    # Persian option labels.
    # ------------------------------------------------------
    if text in PERSIAN_OPTION_IDS:
        return PERSIAN_OPTION_IDS[text]
    if normalized in PERSIAN_OPTION_IDS:
        return PERSIAN_OPTION_IDS[normalized]
    # ------------------------------------------------------
    # Arabic option labels.
    # ------------------------------------------------------
    if text in ARABIC_OPTION_IDS:
        return ARABIC_OPTION_IDS[text]
    # ------------------------------------------------------
    # English A-D.
    # ------------------------------------------------------
    if normalized in ENGLISH_OPTION_IDS:
        return ENGLISH_OPTION_IDS[normalized]
    # ------------------------------------------------------
    # Numeric text.
    # ------------------------------------------------------
    try:
        numeric = int(normalized)
        if 0 <= numeric <= 3:
            return numeric
        if 1 <= numeric <= 4:
            return numeric - 1
    except ValueError:
        pass
    # ------------------------------------------------------
    # Match complete option text.
    # ------------------------------------------------------
    if options:
        normalized_value = text.casefold()
        for index, option in enumerate(options):
            if isinstance(option, Mapping):
                candidates = (
                    option.get("text"),
                    option.get("title"),
                    option.get("value"),
                    option.get("label"),
                )
            else:
                candidates = (option,)
            for candidate in candidates:
                candidate_text = _safe_text(candidate)
                if not candidate_text:
                    continue
                if candidate_text.casefold() == normalized_value:
                    return index
    return None
def _extract_correct_answer(
    question: Mapping[str, Any],
) -> Any:
    """Extract the most likely correct-answer field."""
    return _first_value(
        question,
        "correct_index",
        "answer_index",
        "correct_answer_index",
        "correct_option_index",
        "correct_option",
        "correct_answer",
        "answer",
        "solution",
        default=None,
    )
def _normalize_options(
    options: Any,
) -> list[dict[str, str]]:
    """
    Normalize quiz options to:
    [
        {"id": "A", "text": "..."},
        {"id": "B", "text": "..."},
        ...
    ]
    """
    normalized: list[dict[str, str]] = []
    if isinstance(options, Mapping):
        items = list(options.items())
        for index, (key, value) in enumerate(items):
            option_id = _safe_text(
                key,
                chr(65 + index),
            ).upper()
            option_text = _safe_text(value)
            normalized.append(
                {
                    "id": option_id,
                    "text": option_text,
                }
            )
        return normalized
    if not isinstance(options, list):
        return normalized
    for index, option in enumerate(options):
        default_id = chr(65 + index)
        if isinstance(option, Mapping):
            option_id = _first_value(
                option,
                "id",
                "key",
                "label",
                default=default_id,
            )
            option_text = _first_value(
                option,
                "text",
                "title",
                "value",
                "answer",
                default="",
            )
            normalized.append(
                {
                    "id": _safe_text(
                        option_id,
                        default_id,
                    ).upper(),
                    "text": _safe_text(
                        option_text
                    ),
                }
            )
        else:
            normalized.append(
                {
                    "id": default_id,
                    "text": _safe_text(option),
                }
            )
    return normalized
def normalize_question(
    question: Mapping[str, Any],
    index: int = 0,
) -> dict[str, Any]:
    """
    Normalize a raw quiz question into a stable schema.
    Returned structure includes:
    - id
    - question
    - options
    - correct_index
    - correct_answer
    - explanation
    """
    source = dict(question)
    question_id = _safe_text(
        _first_value(
            source,
            "id",
            "question_id",
            default=f"it_question_{index + 1:02d}",
        )
    )
    question_text = _safe_text(
        _first_value(
            source,
            "question",
            "text",
            "title",
            "prompt",
            default="",
        )
    )
    options = _normalize_options(
        source.get("options", [])
    )
    raw_correct_answer = _extract_correct_answer(
        source
    )
    option_values: list[Any] = [
        option.get("text", "")
        for option in options
    ]
    correct_index = _normalize_option_index(
        raw_correct_answer,
        option_values,
    )
    # ------------------------------------------------------
    # If correct answer is stored as a full option object,
    # try its internal fields too.
    # ------------------------------------------------------
    if correct_index is None and isinstance(
        raw_correct_answer,
        Mapping,
    ):
        correct_index = _normalize_option_index(
            _first_value(
                raw_correct_answer,
                "id",
                "key",
                "index",
                "text",
                "value",
                default=None,
            ),
            option_values,
        )
    # ------------------------------------------------------
    # Normalize correct answer text.
    # ------------------------------------------------------
    correct_answer_text = ""
    if correct_index is not None:
        if 0 <= correct_index < len(options):
            correct_answer_text = _safe_text(
                options[correct_index].get("text")
            )
    if not correct_answer_text:
        if isinstance(raw_correct_answer, str):
            correct_answer_text = raw_correct_answer.strip()
    explanation = _safe_text(
        _first_value(
            source,
            "explanation",
            "solution_explanation",
            "reason",
            "answer_explanation",
            default="",
        )
    )
    normalized = dict(source)
    normalized.update(
        {
            "id": question_id,
            "question": question_text,
            "options": options,
            "correct_index": correct_index,
            "correct_answer": correct_answer_text,
            "explanation": explanation,
        }
    )
    return normalized
# ==========================================================
# Quiz APIs
# ==========================================================
def get_trade_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return normalized quiz questions for a lesson."""
    chapter_id = _safe_text(chapter_id)
    lesson_id = _safe_text(lesson_id)
    if not chapter_id or not lesson_id:
        return []
    try:
        questions = get_quiz_questions(
            chapter_id,
            lesson_id,
        )
    except Exception:
        return []
    if not isinstance(questions, list):
        return []
    result: list[dict[str, Any]] = []
    for index, question in enumerate(
        questions
    ):
        if not isinstance(question, Mapping):
            continue
        result.append(
            normalize_question(
                question,
                index=index,
            )
        )
    return result
def get_trade_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Explicit quiz-question API."""
    return get_trade_quiz(
        chapter_id,
        lesson_id,
    )
def get_quiz_questions_for_lesson(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Compatibility alias for quiz lookup."""
    return get_trade_quiz(
        chapter_id,
        lesson_id,
    )
def get_quiz_question(
    chapter_id: str,
    lesson_id: str,
    question_index: int = 0,
) -> dict[str, Any] | None:
    """Return one normalized quiz question."""
    questions = get_trade_quiz(
        chapter_id,
        lesson_id,
    )
    if not questions:
        return None
    try:
        index = int(question_index)
    except (TypeError, ValueError):
        return None
    if index < 0 or index >= len(questions):
        return None
    return questions[index]
def get_all_quiz_questions() -> list[dict[str, Any]]:
    """
    Return every quiz question across the whole module.
    This is useful for:
    - global quiz systems
    - random quiz
    - search
    - validation
    """
    result: list[dict[str, Any]] = []
    for chapter in get_trade_chapters():
        chapter_id = _safe_text(
            _first_value(
                chapter,
                "id",
                "chapter_id",
                default="",
            )
        )
        if not chapter_id:
            continue
        for lesson in get_trade_lessons(
            chapter_id
        ):
            lesson_id = _safe_text(
                _first_value(
                    lesson,
                    "id",
                    "lesson_id",
                    default="",
                )
            )
            if not lesson_id:
                continue
            questions = get_trade_quiz(
                chapter_id,
                lesson_id,
            )
            for question in questions:
                item = dict(question)
                item["module_id"] = get_module_id()
                item["chapter_id"] = chapter_id
                item["lesson_id"] = lesson_id
                result.append(item)
    return result
# ==========================================================
# Answer Validation
# ==========================================================
def check_answer(
    question: Mapping[str, Any],
    selected_answer: Any,
) -> bool:
    """
    Check a selected answer against a normalized question.
    Returns False when the correct answer cannot be resolved.
    """
    normalized = normalize_question(question)
    options = normalized.get(
        "options",
        [],
    )
    option_texts = [
        option.get("text", "")
        for option in options
        if isinstance(option, Mapping)
    ]
    selected_index = _normalize_option_index(
        selected_answer,
        option_texts,
    )
    correct_index = normalized.get(
        "correct_index"
    )
    if selected_index is None:
        return False
    if correct_index is None:
        return False
    return selected_index == correct_index
def is_correct_answer(
    question: Mapping[str, Any],
    selected_answer: Any,
) -> bool:
    """Compatibility alias for answer validation."""
    return check_answer(
        question,
        selected_answer,
    )
def get_correct_answer_index(
    question: Mapping[str, Any],
) -> int | None:
    """Return normalized zero-based correct answer index."""
    normalized = normalize_question(question)
    value = normalized.get(
        "correct_index"
    )
    if isinstance(value, int):
        return value
    return None
# ==========================================================
# Lesson Progress
# ==========================================================
def start_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Mark lesson as started and return lesson data.
    """
    telegram_id = _safe_int(
        telegram_id
    )
    chapter_id = _safe_text(chapter_id)
    lesson_id = _safe_text(lesson_id)
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
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )
    except TypeError:
        try:
            mark_lesson_started(
                telegram_id,
                get_module_id(),
                chapter_id,
                lesson_id,
            )
        except Exception:
            return None
    except Exception:
        return None
    return lesson
def complete_lesson(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """Mark an International Trade lesson as completed."""
    telegram_id = _safe_int(
        telegram_id
    )
    chapter_id = _safe_text(chapter_id)
    lesson_id = _safe_text(lesson_id)
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
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )
        return True
    except TypeError:
        try:
            mark_lesson_completed(
                telegram_id,
                get_module_id(),
                chapter_id,
                lesson_id,
            )
            return True
        except Exception:
            return False
    except Exception:
        return False
# ==========================================================
# Statistics Compatibility
# ==========================================================
def _load_statistics_function():
    """
    Locate a compatible statistics function dynamically.
    The dynamic lookup keeps this service independent from
    future changes in core.statistics.
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
        "save_attempt",
        "add_quiz_attempt",
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
    Save quiz result using the available Statistics API.
    Returns:
        Record ID when available.
        0 when no compatible persistence function exists.
    """
    telegram_id = _safe_int(
        telegram_id
    )
    chapter_id = _safe_text(chapter_id)
    lesson_id = _safe_text(lesson_id)
    total_questions = max(
        0,
        _safe_int(total_questions),
    )
    correct_answers = max(
        0,
        _safe_int(correct_answers),
    )
    if score is None:
        if total_questions > 0:
            score = (
                correct_answers
                / total_questions
                * 100
            )
        else:
            score = 0.0
    else:
        score = _safe_float(score)
    if telegram_id <= 0:
        return 0
    function = _load_statistics_function()
    if function is None:
        return 0
    payload = {
        "telegram_id": telegram_id,
        "user_id": telegram_id,
        "module_id": get_module_id(),
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score": float(score),
    }
    # ------------------------------------------------------
    # First attempt: keyword arguments.
    # ------------------------------------------------------
    try:
        result = function(
            **payload
        )
        if result is None:
            return 0
        if isinstance(result, bool):
            return int(result)
        try:
            return int(result)
        except (TypeError, ValueError):
            return 0
    except TypeError:
        pass
    except Exception:
        return 0
    # ------------------------------------------------------
    # Compatibility positional signatures.
    # ------------------------------------------------------
    positional_variants = (
        (
            telegram_id,
            get_module_id(),
            chapter_id,
            lesson_id,
            total_questions,
            correct_answers,
            float(score),
        ),
        (
            telegram_id,
            get_module_id(),
            chapter_id,
            lesson_id,
            correct_answers,
            total_questions,
        ),
        (
            telegram_id,
            get_module_id(),
            total_questions,
            correct_answers,
            float(score),
        ),
    )
    for args in positional_variants:
        try:
            result = function(*args)
            if result is None:
                return 0
            if isinstance(result, bool):
                return int(result)
            try:
                return int(result)
            except (TypeError, ValueError):
                return 0
        except TypeError:
            continue
        except Exception:
            return 0
    return 0
def record_trade_quiz_attempt(
    telegram_id: int,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> int:
    """Compatibility wrapper for Trade handlers."""
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
    """Calculate complete curriculum statistics."""
    chapters = get_trade_chapters()
    lesson_count = 0
    quiz_question_count = 0
    for chapter in chapters:
        chapter_id = _safe_text(
            _first_value(
                chapter,
                "id",
                "chapter_id",
                default="",
            )
        )
        if not chapter_id:
            continue
        lessons = get_trade_lessons(
            chapter_id
        )
        lesson_count += len(lessons)
        for lesson in lessons:
            lesson_id = _safe_text(
                _first_value(
                    lesson,
                    "id",
                    "lesson_id",
                    default="",
                )
            )
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
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": quiz_question_count,
    }
def get_curriculum_statistics() -> dict[str, int]:
    """Compatibility alias."""
    return get_curriculum_stats()
def get_module_statistics() -> dict[str, Any]:
    """Return module-level statistics."""
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
    Search lessons by title and textual content.
    """
    keyword = _safe_text(keyword)
    if not keyword:
        return []
    normalized_keyword = keyword.casefold()
    results: list[dict[str, Any]] = []
    for chapter in get_trade_chapters():
        chapter_id = _safe_text(
            _first_value(
                chapter,
                "id",
                "chapter_id",
                default="",
            )
        )
        chapter_title = _safe_text(
            _first_value(
                chapter,
                "title",
                "name",
                default="",
            )
        )
        if not chapter_id:
            continue
        for lesson in get_trade_lessons(
            chapter_id
        ):
            lesson_id = _safe_text(
                _first_value(
                    lesson,
                    "id",
                    "lesson_id",
                    default="",
                )
            )
            lesson_title = _safe_text(
                _first_value(
                    lesson,
                    "title",
                    "name",
                    default="",
                )
            )
            if not lesson_id:
                continue
            lesson_text = (
                get_trade_lesson_text(
                    chapter_id,
                    lesson_id,
                )
                or ""
            )
            searchable_text = (
                f"{chapter_title}\n"
                f"{lesson_title}\n"
                f"{lesson_text}"
            ).casefold()
            if normalized_keyword in searchable_text:
                results.append(
                    {
                        "module_id": get_module_id(),
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "chapter_title": chapter_title,
                        "title": lesson_title,
                    }
                )
    return results
# ==========================================================
# Validation
# ==========================================================
def validate_module() -> dict[str, Any]:
    """
    Validate the International Trade curriculum.
    Checks:
    - chapters exist
    - chapter IDs are unique
    - lessons exist
    - lesson IDs are unique within chapters
    - quiz questions have text
    - questions have options
    - questions have resolvable correct answers
    """
    errors: list[str] = []
    warnings: list[str] = []
    chapters = get_trade_chapters()
    if not chapters:
        errors.append(
            "No International Trade chapters found."
        )
    chapter_ids: set[str] = set()
    total_lessons = 0
    total_questions = 0
    for chapter_index, chapter in enumerate(
        chapters,
        start=1,
    ):
        chapter_id = _safe_text(
            _first_value(
                chapter,
                "id",
                "chapter_id",
                default="",
            )
        )
        if not chapter_id:
            errors.append(
                f"Chapter #{chapter_index} has no ID."
            )
            continue
        if chapter_id in chapter_ids:
            errors.append(
                f"Duplicate chapter ID: {chapter_id}"
            )
        else:
            chapter_ids.add(chapter_id)
        lessons = get_trade_lessons(
            chapter_id
        )
        if not lessons:
            warnings.append(
                f"Chapter {chapter_id} has no lessons."
            )
            continue
        lesson_ids: set[str] = set()
        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):
            total_lessons += 1
            lesson_id = _safe_text(
                _first_value(
                    lesson,
                    "id",
                    "lesson_id",
                    default="",
                )
            )
            if not lesson_id:
                errors.append(
                    (
                        f"Chapter {chapter_id}: "
                        f"lesson #{lesson_index} has no ID."
                    )
                )
                continue
            if lesson_id in lesson_ids:
                errors.append(
                    (
                        f"Chapter {chapter_id}: "
                        f"duplicate lesson ID {lesson_id}"
                    )
                )
            else:
                lesson_ids.add(lesson_id)
            questions = get_trade_quiz(
                chapter_id,
                lesson_id,
            )
            total_questions += len(questions)
            if not questions:
                warnings.append(
                    (
                        f"Lesson {chapter_id}/{lesson_id} "
                        "has no quiz questions."
                    )
                )
                continue
            for question_index, question in enumerate(
                questions,
                start=1,
            ):
                question_text = _safe_text(
                    question.get("question")
                )
                if not question_text:
                    errors.append(
                        (
                            f"Question #{question_index} "
                            f"in {chapter_id}/{lesson_id} "
                            "has no text."
                        )
                    )
                options = question.get(
                    "options",
                    [],
                )
                if not isinstance(options, list):
                    errors.append(
                        (
                            f"Question #{question_index} "
                            f"in {chapter_id}/{lesson_id} "
                            "has invalid options."
                        )
                    )
                    continue
                if len(options) < 2:
                    errors.append(
                        (
                            f"Question #{question_index} "
                            f"in {chapter_id}/{lesson_id} "
                            "has fewer than two options."
                        )
                    )
                correct_index = question.get(
                    "correct_index"
                )
                if correct_index is None:
                    errors.append(
                        (
                            f"Question #{question_index} "
                            f"in {chapter_id}/{lesson_id} "
                            "has no resolvable correct answer."
                        )
                    )
                elif not (
                    isinstance(correct_index, int)
                    and 0 <= correct_index < len(options)
                ):
                    errors.append(
                        (
                            f"Question #{question_index} "
                            f"in {chapter_id}/{lesson_id} "
                            "has an invalid correct answer index."
                        )
                    )
    return {
        "valid": len(errors) == 0,
        "module_id": get_module_id(),
        "module_title": get_module_title(),
        "chapters": len(chapters),
        "lessons": total_lessons,
        "quiz_questions": total_questions,
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
# ==========================================================
# Health Check
# ==========================================================
def international_trade_service_health_check() -> dict[str, Any]:
    """
    Perform a lightweight service health check.
    """
    try:
        stats = get_curriculum_stats()
        return {
            "ok": True,
            "healthy": True,
            "module_id": get_module_id(),
            "module_title": get_module_title(),
            "chapters": stats["chapters"],
            "lessons": stats["lessons"],
            "quiz_questions": stats["quiz_questions"],
        }
    except Exception as exc:
        return {
            "ok": False,
            "healthy": False,
            "module_id": get_module_id(),
            "module_title": get_module_title(),
            "error": str(exc),
        }
def service_health_check() -> dict[str, Any]:
    """Compatibility alias for health check."""
    return international_trade_service_health_check()
# ==========================================================
# Public Compatibility Aliases
# ==========================================================
get_chapters_for_module = get_trade_chapters
get_chapter_for_module = get_trade_chapter
get_lessons_for_chapter = get_trade_lessons
get_lesson_for_chapter = get_trade_lesson
get_quiz_for_lesson = get_trade_quiz
# ==========================================================
# Exported API
# ==========================================================
__all__ = [
    # Module
    "get_module_id",
    "get_module_title",
    "get_module_info",
    # Chapters
    "get_trade_chapters",
    "get_trade_chapter",
    "get_chapter_by_id",
    # Lessons
    "get_trade_lessons",
    "get_trade_lesson",
    "get_lesson_by_id",
    "get_trade_lesson_content",
    "get_trade_lesson_text",
    # Quiz
    "normalize_question",
    "get_trade_quiz",
    "get_trade_quiz_questions",
    "get_quiz_questions_for_lesson",
    "get_quiz_question",
    "get_all_quiz_questions",
    # Answers
    "check_answer",
    "is_correct_answer",
    "get_correct_answer_index",
    # Progress
    "start_lesson",
    "complete_lesson",
    # Statistics
    "save_quiz_result",
    "record_trade_quiz_attempt",
    # Statistics / Search / Validation
    "get_curriculum_stats",
    "get_curriculum_statistics",
    "get_module_statistics",
    "search_lessons",
    "validate_module",
    # Health
    "international_trade_service_health_check",
    "service_health_check",
]
