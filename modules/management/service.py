"""
Management Service Layer
Andishkadeh Management & Market

Responsibilities:
- Access Management curriculum data
- Retrieve chapters
- Retrieve lessons
- Retrieve lesson content
- Retrieve quiz questions
- Normalize quiz question schemas
- Convert text answers to answer indexes
- Search lessons
- Curriculum statistics
- Data validation
- Health check

This service layer is independent from Telegram handlers.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from modules.management import data as management_data


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = "management"
MODULE_TITLE = "آموزش مدیریت"


# ==========================================================
# Generic Helpers
# ==========================================================

def _normalize_id(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _safe_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return deepcopy(dict(value))

    return {}


def _safe_list(value: Any) -> list[Any]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return [value]


def _get_id(
    item: Mapping[str, Any],
    primary: str = "id",
    secondary: str = "",
) -> str:
    if not isinstance(item, Mapping):
        return ""

    value = item.get(primary)

    if not value and secondary:
        value = item.get(secondary)

    if not value:
        value = item.get("key")

    return _normalize_id(value)


# ==========================================================
# Data Source
# ==========================================================

def _find_data_source() -> Any:
    """
    Detect the curriculum structure used by data.py.

    Supported structures:
    - MANAGEMENT_DATA
    - MANAGEMENT_CURRICULUM
    - CURRICULUM
    - CHAPTERS
    - CHAPTER_1, CHAPTER_2, ...
    """

    for name in (
        "MANAGEMENT_DATA",
        "MANAGEMENT_CURRICULUM",
        "CURRICULUM",
        "CHAPTERS",
    ):
        value = getattr(
            management_data,
            name,
            None,
        )

        if value is not None:
            return value

    chapters: list[dict[str, Any]] = []

    index = 1

    while True:
        name = f"CHAPTER_{index}"

        value = getattr(
            management_data,
            name,
            None,
        )

        if value is None:
            break

        if isinstance(value, Mapping):
            chapters.append(
                deepcopy(dict(value))
            )

        index += 1

    return chapters


def _raw_chapters() -> list[dict[str, Any]]:
    source = _find_data_source()

    if isinstance(source, list):
        return [
            deepcopy(dict(item))
            for item in source
            if isinstance(item, Mapping)
        ]

    if isinstance(source, Mapping):

        if isinstance(
            source.get("chapters"),
            list,
        ):
            return [
                deepcopy(dict(item))
                for item in source["chapters"]
                if isinstance(item, Mapping)
            ]

        if isinstance(
            source.get("data"),
            list,
        ):
            return [
                deepcopy(dict(item))
                for item in source["data"]
                if isinstance(item, Mapping)
            ]

        if (
            source.get("id")
            and source.get("lessons") is not None
        ):
            return [
                deepcopy(dict(source))
            ]

    return []


# ==========================================================
# Chapter Normalization
# ==========================================================

def _normalize_chapter(
    chapter: Any,
) -> dict[str, Any]:

    if not isinstance(chapter, Mapping):
        return {}

    result = deepcopy(dict(chapter))

    chapter_id = (
        result.get("id")
        or result.get("chapter_id")
        or result.get("key")
        or ""
    )

    result["id"] = _normalize_id(
        chapter_id
    )

    result["chapter_id"] = result["id"]

    result["title"] = _normalize_text(
        result.get("title")
        or result.get("name")
        or result["id"]
    )

    result["description"] = _normalize_text(
        result.get("description")
        or result.get("summary")
        or ""
    )

    lessons = result.get(
        "lessons",
        [],
    )

    result["lessons"] = [
        deepcopy(dict(lesson))
        for lesson in _safe_list(lessons)
        if isinstance(lesson, Mapping)
    ]

    return result


def _normalize_lesson(
    lesson: Any,
) -> dict[str, Any]:

    if not isinstance(lesson, Mapping):
        return {}

    result = deepcopy(dict(lesson))

    lesson_id = (
        result.get("id")
        or result.get("lesson_id")
        or result.get("key")
        or ""
    )

    result["id"] = _normalize_id(
        lesson_id
    )

    result["lesson_id"] = result["id"]

    result["title"] = _normalize_text(
        result.get("title")
        or result.get("name")
        or result["id"]
    )

    content = (
        result.get("content")
        or result.get("text")
        or result.get("lesson_content")
        or result.get("body")
        or result.get("details")
        or result.get("description")
        or ""
    )

    result["content"] = _normalize_text(
        content
    )

    result["subtopics"] = _safe_list(
        result.get(
            "subtopics",
            result.get(
                "topics",
                result.get(
                    "sub_topics",
                    [],
                ),
            ),
        )
    )

    result["special_points"] = _safe_list(
        result.get(
            "special_points",
            result.get(
                "specialized_tips",
                result.get(
                    "professional_tips",
                    [],
                ),
            ),
        )
    )

    result["exam_points"] = _safe_list(
        result.get(
            "exam_points",
            result.get(
                "exam_tips",
                result.get(
                    "test_tips",
                    [],
                ),
            ),
        )
    )

    result["examples"] = _safe_list(
        result.get(
            "examples",
            result.get(
                "practical_examples",
                [],
            ),
        )
    )

    result["keywords"] = _safe_list(
        result.get(
            "keywords",
            result.get(
                "key_terms",
                [],
            ),
        )
    )

    return result


# ==========================================================
# Module Information
# ==========================================================

def get_module_id() -> str:
    return MODULE_ID


def get_module_title() -> str:

    title = getattr(
        management_data,
        "MODULE_TITLE",
        None,
    )

    if title:
        return _normalize_text(title)

    return MODULE_TITLE


def get_module_description() -> str:

    description = getattr(
        management_data,
        "MODULE_DESCRIPTION",
        "",
    )

    return _normalize_text(
        description
    )


def get_module_info() -> dict[str, Any]:

    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "key": MODULE_ID,
        "title": get_module_title(),
        "description": get_module_description(),
    }


# ==========================================================
# Chapters
# ==========================================================

def get_management_chapters() -> list[dict[str, Any]]:

    return [
        _normalize_chapter(chapter)
        for chapter in _raw_chapters()
        if _normalize_chapter(chapter).get("id")
    ]


def get_chapters() -> list[dict[str, Any]]:
    return get_management_chapters()


def get_management_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:

    target = _normalize_id(
        chapter_id
    )

    if not target:
        return None

    for chapter in get_management_chapters():

        if chapter["id"] == target:
            return deepcopy(chapter)

    return None


def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:

    return get_management_chapter(
        chapter_id
    )


def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:

    return get_management_chapter(
        chapter_id
    )


def get_chapter_title(
    chapter_id: str,
) -> str | None:

    chapter = get_management_chapter(
        chapter_id
    )

    if chapter is None:
        return None

    return _normalize_text(
        chapter.get("title")
    )


def get_chapter_ids() -> list[str]:

    return [
        chapter["id"]
        for chapter in get_management_chapters()
        if chapter.get("id")
    ]


# ==========================================================
# Lessons
# ==========================================================

def get_management_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:

    chapter = get_management_chapter(
        chapter_id
    )

    if chapter is None:
        return []

    return [
        _normalize_lesson(lesson)
        for lesson in chapter.get(
            "lessons",
            [],
        )
        if _normalize_lesson(lesson).get("id")
    ]


def get_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:

    return get_management_lessons(
        chapter_id
    )


def get_management_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    target_chapter = _normalize_id(
        chapter_id
    )

    target_lesson = _normalize_id(
        lesson_id
    )

    if (
        not target_chapter
        or not target_lesson
    ):
        return None

    lessons = get_management_lessons(
        target_chapter
    )

    for lesson in lessons:

        if lesson["id"] == target_lesson:
            return deepcopy(lesson)

    return None


def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    return get_management_lesson(
        chapter_id,
        lesson_id,
    )


def get_lesson_by_id(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    return get_management_lesson(
        chapter_id,
        lesson_id,
    )


def get_lesson_title(
    chapter_id: str,
    lesson_id: str,
) -> str | None:

    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    return _normalize_text(
        lesson.get("title")
    )


def get_lesson_ids(
    chapter_id: str,
) -> list[str]:

    return [
        lesson["id"]
        for lesson in get_management_lessons(
            chapter_id
        )
        if lesson.get("id")
    ]


# ==========================================================
# Lesson Content
# ==========================================================

def get_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    return get_management_lesson(
        chapter_id,
        lesson_id,
    )


def get_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:

    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return None

    content = _normalize_text(
        lesson.get("content")
    )

    if content:
        return content

    for key in (
        "text",
        "description",
        "lesson_content",
        "body",
        "details",
        "summary",
    ):

        value = lesson.get(key)

        if isinstance(value, str):

            value = value.strip()

            if value:
                return value

    return None


def get_management_lesson_content(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    return get_lesson_content(
        chapter_id,
        lesson_id,
    )


def get_management_lesson_text(
    chapter_id: str,
    lesson_id: str,
) -> str | None:

    return get_lesson_text(
        chapter_id,
        lesson_id,
    )


def get_lesson_summary(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:

    lesson = get_management_lesson(
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
            lesson_id
        ),
        "title": lesson.get(
            "title",
            "",
        ),
        "summary": lesson.get(
            "summary",
            "",
        ),
    }


# ==========================================================
# Quiz Helpers
# ==========================================================

def _answer_to_index(
    value: Any,
    options: list[str],
) -> int:

    if value is None:
        return 0

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, int):
        return value

    text = _normalize_text(value)

    if not text:
        return 0

    # A / B / C / D
    letters = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    upper = text.upper()

    if upper in letters:
        return letters[upper]

    # Persian option letters
    persian_letters = {
        "الف": 0,
        "ب": 1,
        "ج": 2,
        "د": 3,
    }

    if text in persian_letters:
        return persian_letters[text]

    # Numeric index
    try:
        numeric = int(text)

        if 0 <= numeric < len(options):
            return numeric

        # Support 1-based numbering
        if 1 <= numeric <= len(options):
            return numeric - 1

    except (TypeError, ValueError):
        pass

    # Full answer text
    normalized_value = text.casefold()

    for index, option in enumerate(options):

        if (
            _normalize_text(option).casefold()
            == normalized_value
        ):
            return index

    return 0


def _normalize_question(
    question: Any,
    question_index: int = 0,
) -> dict[str, Any]:

    if not isinstance(question, Mapping):

        return {
            "id": f"management_q_{question_index + 1}",
            "question": _normalize_text(
                question
            ),
            "options": [],
            "correct_index": 0,
            "explanation": "",
        }

    result = deepcopy(dict(question))

    question_id = (
        result.get("id")
        or result.get("question_id")
        or f"management_q_{question_index + 1}"
    )

    result["id"] = _normalize_id(
        question_id
    )

    result["question"] = _normalize_text(
        result.get("question")
        or result.get("text")
        or result.get("question_text")
        or ""
    )

    raw_options = (
        result.get("options")
        or result.get("choices")
        or result.get("answers")
        or []
    )

    options: list[str] = []

    for option in _safe_list(
        raw_options
    ):

        if isinstance(option, Mapping):

            option_text = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or option.get("value")
                or ""
            )

        else:

            option_text = option

        options.append(
            _normalize_text(option_text)
        )

    result["options"] = options

    raw_correct = None

    if result.get("correct_index") is not None:
        raw_correct = result.get(
            "correct_index"
        )

    elif result.get("answer_index") is not None:
        raw_correct = result.get(
            "answer_index"
        )

    elif result.get("correct_answer") is not None:
        raw_correct = result.get(
            "correct_answer"
        )

    elif result.get("answer") is not None:
        raw_correct = result.get(
            "answer"
        )

    elif result.get("correct") is not None:
        raw_correct = result.get(
            "correct"
        )

    result["correct_index"] = _answer_to_index(
        raw_correct,
        options,
    )

    if options:

        if (
            result["correct_index"] < 0
            or result["correct_index"] >= len(options)
        ):
            result["correct_index"] = 0

    result["explanation"] = _normalize_text(
        result.get("explanation")
        or result.get("answer_explanation")
        or result.get("solution")
        or result.get("reason")
        or ""
    )

    return result


# ==========================================================
# Quiz Bank Access
# ==========================================================

def _get_management_quiz_bank() -> Any:

    for name in (
        "MANAGEMENT_QUIZ_QUESTIONS",
        "QUIZ_QUESTIONS",
        "MANAGEMENT_QUIZ",
        "QUIZ_BANK",
    ):

        value = getattr(
            management_data,
            name,
            None,
        )

        if value is not None:
            return value

    return None


def _quiz_from_bank(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    bank = _get_management_quiz_bank()

    if bank is None:
        return []

    target_chapter = _normalize_id(
        chapter_id
    )

    target_lesson = _normalize_id(
        lesson_id
    )

    raw_questions: Any = None

    # ------------------------------------------------------
    # Main structure:
    # {
    #     (chapter_id, lesson_id): [...]
    # }
    # ------------------------------------------------------

    if isinstance(bank, Mapping):

        tuple_key = (
            target_chapter,
            target_lesson,
        )

        if tuple_key in bank:
            raw_questions = bank[
                tuple_key
            ]

        if raw_questions is None:

            string_keys = (
                f"{target_chapter}:{target_lesson}",
                f"{target_chapter}/{target_lesson}",
                f"{target_chapter}_{target_lesson}",
            )

            for key in string_keys:

                if key in bank:

                    raw_questions = bank[key]

                    break

        if raw_questions is None:

            chapter_entry = bank.get(
                target_chapter
            )

            if isinstance(
                chapter_entry,
                Mapping,
            ):

                raw_questions = (
                    chapter_entry.get(
                        target_lesson
                    )
                )

    if raw_questions is None:
        return []

    result: list[dict[str, Any]] = []

    for index, question in enumerate(
        _safe_list(raw_questions)
    ):

        normalized = _normalize_question(
            question,
            index,
        )

        normalized["module_id"] = MODULE_ID
        normalized["chapter_id"] = target_chapter
        normalized["lesson_id"] = target_lesson

        result.append(
            normalized
        )

    return result


# ==========================================================
# Public Quiz API
# ==========================================================

def get_management_lesson_quiz(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )

    # ------------------------------------------------------
    # First: Quiz embedded inside lesson
    # ------------------------------------------------------

    if lesson is not None:

        for key in (
            "quiz",
            "questions",
            "quiz_questions",
            "test",
        ):

            raw_questions = lesson.get(
                key
            )

            if isinstance(
                raw_questions,
                list,
            ) and raw_questions:

                return [
                    _normalize_question(
                        question,
                        index,
                    )
                    for index, question
                    in enumerate(
                        raw_questions
                    )
                    if isinstance(
                        question,
                        Mapping,
                    )
                ]

    # ------------------------------------------------------
    # Second: Central Management Quiz Bank
    # ------------------------------------------------------

    return _quiz_from_bank(
        chapter_id,
        lesson_id,
    )


def get_management_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    return get_management_lesson_quiz(
        chapter_id,
        lesson_id,
    )


def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    return get_management_lesson_quiz(
        chapter_id,
        lesson_id,
    )


def get_quiz_questions_for_lesson(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:

    return get_management_lesson_quiz(
        chapter_id,
        lesson_id,
    )


# ==========================================================
# All Lessons
# ==========================================================

def get_all_lessons() -> list[dict[str, Any]]:

    result: list[dict[str, Any]] = []

    for chapter in get_management_chapters():

        chapter_id = chapter["id"]

        for lesson in get_management_lessons(
            chapter_id
        ):

            item = deepcopy(lesson)

            item["module_id"] = MODULE_ID
            item["chapter_id"] = chapter_id

            result.append(item)

    return result


def get_management_all_lessons() -> list[dict[str, Any]]:
    return get_all_lessons()


# ==========================================================
# All Quiz Questions
# ==========================================================

def get_all_questions() -> list[dict[str, Any]]:

    result: list[dict[str, Any]] = []

    for chapter in get_management_chapters():

        chapter_id = chapter["id"]

        for lesson in get_management_lessons(
            chapter_id
        ):

            lesson_id = lesson["id"]

            questions = get_management_lesson_quiz(
                chapter_id,
                lesson_id,
            )

            result.extend(
                questions
            )

    return result


def get_management_all_questions() -> list[dict[str, Any]]:
    return get_all_questions()


def get_management_quiz_bank() -> list[dict[str, Any]]:
    return get_all_questions()


# ==========================================================
# Search
# ==========================================================

def search_lessons(
    keyword: str,
) -> list[dict[str, Any]]:

    normalized_keyword = _normalize_text(
        keyword
    ).casefold()

    if not normalized_keyword:
        return []

    results: list[dict[str, Any]] = []

    for chapter in get_management_chapters():

        chapter_id = chapter["id"]

        chapter_title = _normalize_text(
            chapter.get("title")
        )

        for lesson in get_management_lessons(
            chapter_id
        ):

            lesson_id = lesson["id"]

            title = _normalize_text(
                lesson.get("title")
            )

            content = get_lesson_text(
                chapter_id,
                lesson_id,
            ) or ""

            keywords = " ".join(
                _normalize_text(item)
                for item in _safe_list(
                    lesson.get("keywords")
                )
            )

            searchable = (
                f"{chapter_title}\n"
                f"{title}\n"
                f"{content}\n"
                f"{keywords}"
            ).casefold()

            if normalized_keyword in searchable:

                results.append(
                    {
                        "module_id": MODULE_ID,
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "chapter_title": chapter_title,
                        "title": title,
                    }
                )

    return results


# ==========================================================
# Statistics
# ==========================================================

def get_curriculum_statistics() -> dict[str, int]:

    chapters = get_management_chapters()

    lesson_count = 0
    question_count = 0

    for chapter in chapters:

        chapter_id = chapter["id"]

        lessons = get_management_lessons(
            chapter_id
        )

        lesson_count += len(
            lessons
        )

        for lesson in lessons:

            question_count += len(
                get_management_lesson_quiz(
                    chapter_id,
                    lesson["id"],
                )
            )

    return {
        "modules": 1,
        "chapters": len(chapters),
        "lessons": lesson_count,
        "quiz_questions": question_count,
    }


def get_curriculum_stats() -> dict[str, int]:
    return get_curriculum_statistics()


def get_management_statistics() -> dict[str, int]:
    return get_curriculum_statistics()


def get_module_statistics() -> dict[str, Any]:

    statistics = get_curriculum_statistics()

    return {
        "module_id": MODULE_ID,
        "title": get_module_title(),
        "description": get_module_description(),
        **statistics,
    }


# ==========================================================
# Validation
# ==========================================================

def validate_module() -> dict[str, Any]:

    errors: list[str] = []
    warnings: list[str] = []

    chapters = get_management_chapters()

    if not chapters:

        errors.append(
            "No Management chapters found."
        )

    chapter_ids: set[str] = set()

    for chapter_index, chapter in enumerate(
        chapters,
        start=1,
    ):

        chapter_id = _normalize_id(
            chapter.get("id")
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

        chapter_ids.add(
            chapter_id
        )

        if not chapter.get("title"):

            warnings.append(
                f"Chapter '{chapter_id}' has no title."
            )

        lessons = get_management_lessons(
            chapter_id
        )

        if not lessons:

            warnings.append(
                f"Chapter '{chapter_id}' has no lessons."
            )

            continue

        lesson_ids: set[str] = set()

        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):

            lesson_id = _normalize_id(
                lesson.get("id")
            )

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
                    f"has no title."
                )

            if not get_lesson_text(
                chapter_id,
                lesson_id,
            ):

                warnings.append(
                    f"Lesson '{lesson_id}' "
                    f"in chapter '{chapter_id}' "
                    "has no textual content."
                )

            questions = get_management_lesson_quiz(
                chapter_id,
                lesson_id,
            )

            if not questions:

                warnings.append(
                    f"Lesson '{lesson_id}' "
                    f"in chapter '{chapter_id}' "
                    "has no quiz questions."
                )

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": get_curriculum_statistics(),
    }


def validate_curriculum() -> dict[str, Any]:
    return validate_module()


# ==========================================================
# Health Check
# ==========================================================

def management_service_health_check() -> bool:

    try:

        if not get_module_id():
            return False

        if not get_module_title():
            return False

        chapters = get_management_chapters()

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

            chapter_id = chapter.get(
                "id"
            )

            if not chapter_id:
                return False

            lessons = get_management_lessons(
                chapter_id
            )

            if not isinstance(
                lessons,
                list,
            ):
                return False

            for lesson in lessons:

                if not isinstance(
                    lesson,
                    dict,
                ):
                    return False

                if not lesson.get("id"):
                    return False

        return True

    except Exception:

        return False


def service_health_check() -> bool:
    return management_service_health_check()


def management_data_health_check() -> bool:

    function = getattr(
        management_data,
        "data_health_check",
        None,
    )

    if callable(function):

        try:
            result = function()

            if isinstance(
                result,
                bool,
            ):
                return result

            if isinstance(
                result,
                Mapping,
            ):
                return bool(
                    result.get(
                        "valid",
                        result.get(
                            "healthy",
                            True,
                        ),
                    )
                )

        except Exception:
            pass

    return management_service_health_check()


# ==========================================================
# Compatibility API
# ==========================================================

get_management_module_info = get_module_info

get_management_lesson_by_id = get_management_lesson

get_management_lesson_quiz_questions = (
    get_management_lesson_quiz
)


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    # Module
    "get_module_id",
    "get_module_title",
    "get_module_description",
    "get_module_info",
    "get_management_module_info",

    # Chapters
    "get_management_chapters",
    "get_chapters",
    "get_management_chapter",
    "get_chapter",
    "get_chapter_by_id",
    "get_chapter_title",
    "get_chapter_ids",

    # Lessons
    "get_management_lessons",
    "get_lessons",
    "get_management_lesson",
    "get_lesson",
    "get_lesson_by_id",
    "get_management_lesson_by_id",
    "get_lesson_title",
    "get_lesson_ids",

    # Content
    "get_lesson_content",
    "get_lesson_text",
    "get_lesson_summary",
    "get_management_lesson_content",
    "get_management_lesson_text",

    # Quiz
    "get_management_lesson_quiz",
    "get_management_quiz_questions",
    "get_management_lesson_quiz_questions",
    "get_quiz_questions",
    "get_quiz_questions_for_lesson",
    "get_management_quiz_bank",

    # Collections
    "get_all_lessons",
    "get_management_all_lessons",
    "get_all_questions",
    "get_management_all_questions",

    # Search
    "search_lessons",

    # Statistics
    "get_curriculum_statistics",
    "get_curriculum_stats",
    "get_management_statistics",
    "get_module_statistics",

    # Validation
    "validate_module",
    "validate_curriculum",

    # Health
    "management_service_health_check",
    "service_health_check",
    "management_data_health_check",
]
