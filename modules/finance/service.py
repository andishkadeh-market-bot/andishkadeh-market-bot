"""
Finance Service Layer
Andishkadeh Management & Market

لایه سرویس حرفه‌ای مدیریت مالی

مسئولیت‌ها:
- اتصال امن Handler به Data و Content
- مدیریت فصل‌ها و درس‌ها
- دریافت محتوای کامل آموزشی
- دریافت نکات تخصصی و آزمونی
- دریافت مثال‌های کاربردی
- مدیریت آزمون‌ها
- جست‌وجوی محتوای مدیریت مالی
- محاسبه آمار دوره
- اعتبارسنجی ساختار آموزشی
- Health Check
- سازگاری با نسخه‌های مختلف data.py و content.py
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import data
from . import content


# ============================================================
# Constants
# ============================================================

MODULE_ID = "finance"
DEFAULT_MODULE_TITLE = "💰 مدیریت مالی"


# ============================================================
# Generic Helpers
# ============================================================

def _safe_call(
    function_name: str,
    *args: Any,
    default: Any = None,
    **kwargs: Any,
) -> Any:
    """
    اجرای امن تابع از ماژول‌های data/content.
    """
    function = getattr(data, function_name, None)

    if function is None:
        return default

    try:
        return function(*args, **kwargs)
    except Exception:
        return default


def _safe_content_call(
    function_name: str,
    *args: Any,
    default: Any = None,
    **kwargs: Any,
) -> Any:
    """
    اجرای امن تابع از content.py.
    """
    function = getattr(content, function_name, None)

    if function is None:
        return default

    try:
        return function(*args, **kwargs)
    except Exception:
        return default


def _normalize_text(value: Any, default: str = "") -> str:
    """
    نرمال‌سازی متن.
    """
    if value is None:
        return default

    return str(value).strip()


def _normalize_list(value: Any) -> List[Any]:
    """
    نرمال‌سازی لیست.
    """
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, set):
        return list(value)

    return [value]


def _get_id(item: Any) -> str:
    """
    دریافت شناسه از dict/object.
    """
    if isinstance(item, dict):
        return _normalize_text(
            item.get("id")
            or item.get("chapter_id")
            or item.get("lesson_id")
            or item.get("key")
        )

    return _normalize_text(
        getattr(item, "id", None)
        or getattr(item, "chapter_id", None)
        or getattr(item, "lesson_id", None)
    )


def _get_title(item: Any) -> str:
    """
    دریافت عنوان.
    """
    if isinstance(item, dict):
        return _normalize_text(
            item.get("title")
            or item.get("name")
            or item.get("chapter_title")
            or item.get("lesson_title")
        )

    return _normalize_text(
        getattr(item, "title", None)
        or getattr(item, "name", None)
    )


# ============================================================
# Module Information
# ============================================================

def get_module_title() -> str:
    """
    عنوان ماژول مدیریت مالی.
    """
    title = getattr(data, "MODULE_TITLE", None)

    return _normalize_text(title, DEFAULT_MODULE_TITLE)


def get_module_description() -> str:
    """
    توضیحات ماژول.
    """
    description = getattr(data, "MODULE_DESCRIPTION", None)

    if description:
        return _normalize_text(description)

    return (
        "دوره تخصصی مدیریت مالی شامل مبانی مالی، تحلیل صورت‌های مالی، "
        "تصمیم‌گیری مالی، بودجه‌بندی، سرمایه‌گذاری، تأمین مالی، "
        "مدیریت سرمایه در گردش و مدیریت ریسک."
    )


def get_module_info() -> Dict[str, Any]:
    """
    اطلاعات کامل ماژول.
    """
    info = {}

    raw_info = getattr(data, "get_module_info", None)

    if callable(raw_info):
        try:
            result = raw_info()

            if isinstance(result, dict):
                info.update(result)
        except Exception:
            pass

    info.setdefault("module_id", MODULE_ID)
    info.setdefault("title", get_module_title())
    info.setdefault("description", get_module_description())

    chapters = get_finance_chapters()

    info.setdefault("chapter_count", len(chapters))
    info.setdefault("lesson_count", get_total_lesson_count())
    info.setdefault("quiz_count", len(get_all_quiz_questions()))

    return info


# ============================================================
# Chapters
# ============================================================

def get_finance_chapters() -> List[Dict[str, Any]]:
    """
    دریافت تمام فصل‌های مدیریت مالی.
    """
    chapters = _safe_call(
        "get_chapters",
        default=None,
    )

    if chapters is None:
        chapters = getattr(data, "FINANCE_CHAPTERS", None)

    if chapters is None:
        chapters = getattr(data, "CHAPTERS", None)

    chapters = _normalize_list(chapters)

    normalized = []

    for chapter in chapters:
        if isinstance(chapter, dict):
            item = dict(chapter)
        else:
            item = {
                "id": _get_id(chapter),
                "title": _get_title(chapter),
            }

        item["id"] = _normalize_text(item.get("id"))
        item["title"] = _normalize_text(item.get("title"))

        if item["id"]:
            normalized.append(item)

    return normalized


def get_finance_chapter(chapter_id: str) -> Optional[Dict[str, Any]]:
    """
    دریافت یک فصل مشخص.
    """
    chapter_id = _normalize_text(chapter_id)

    if not chapter_id:
        return None

    chapter = _safe_call(
        "get_chapter",
        chapter_id,
        default=None,
    )

    if chapter is None:
        for item in get_finance_chapters():
            if item.get("id") == chapter_id:
                chapter = item
                break

    if chapter is None:
        return None

    if isinstance(chapter, dict):
        result = dict(chapter)
    else:
        result = {
            "id": _get_id(chapter),
            "title": _get_title(chapter),
        }

    result["id"] = _normalize_text(result.get("id"), chapter_id)
    result["title"] = _normalize_text(result.get("title"))

    return result


# ============================================================
# Lessons
# ============================================================

def get_finance_lessons(chapter_id: str) -> List[Dict[str, Any]]:
    """
    دریافت درس‌های یک فصل.
    """
    chapter_id = _normalize_text(chapter_id)

    if not chapter_id:
        return []

    lessons = _safe_call(
        "get_lessons",
        chapter_id,
        default=None,
    )

    if lessons is None:
        lessons_map = getattr(data, "FINANCE_LESSONS", None)

        if isinstance(lessons_map, dict):
            lessons = lessons_map.get(chapter_id, [])

    lessons = _normalize_list(lessons)

    normalized = []

    for lesson in lessons:
        if isinstance(lesson, dict):
            item = dict(lesson)
        else:
            item = {
                "id": _get_id(lesson),
                "title": _get_title(lesson),
            }

        item["id"] = _normalize_text(item.get("id"))
        item["title"] = _normalize_text(item.get("title"))
        item["chapter_id"] = chapter_id

        if item["id"]:
            normalized.append(item)

    return normalized


def get_finance_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Optional[Dict[str, Any]]:
    """
    دریافت یک درس مشخص.
    """
    chapter_id = _normalize_text(chapter_id)
    lesson_id = _normalize_text(lesson_id)

    if not chapter_id or not lesson_id:
        return None

    lesson = _safe_call(
        "get_lesson",
        chapter_id,
        lesson_id,
        default=None,
    )

    if lesson is None:
        for item in get_finance_lessons(chapter_id):
            if item.get("id") == lesson_id:
                lesson = item
                break

    if lesson is None:
        return None

    if isinstance(lesson, dict):
        result = dict(lesson)
    else:
        result = {
            "id": _get_id(lesson),
            "title": _get_title(lesson),
        }

    result["id"] = _normalize_text(result.get("id"), lesson_id)
    result["title"] = _normalize_text(result.get("title"))
    result["chapter_id"] = chapter_id

    return result


# ============================================================
# Educational Content
# ============================================================

def get_lesson_content(lesson_id: str) -> Optional[Dict[str, Any]]:
    """
    دریافت محتوای کامل یک درس از content.py.
    """
    lesson_id = _normalize_text(lesson_id)

    if not lesson_id:
        return None

    result = _safe_content_call(
        "get_lesson_content",
        lesson_id,
        default=None,
    )

    if result is None:
        return None

    if not isinstance(result, dict):
        return {
            "lesson_id": lesson_id,
            "lesson_text": _normalize_text(result),
        }

    content_data = dict(result)

    content_data.setdefault("lesson_id", lesson_id)

    content_data.setdefault(
        "lesson_text",
        content_data.get("content", ""),
    )

    content_data.setdefault("subtopics", [])
    content_data.setdefault("detailed_content", "")
    content_data.setdefault("specialized_points", [])
    content_data.setdefault("exam_points", [])
    content_data.setdefault("practical_example", "")
    content_data.setdefault("review", [])

    return content_data


def get_complete_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Dict[str, Any]:
    """
    ترکیب اطلاعات Data و Content برای ساخت یک درس کامل.
    """
    lesson = get_finance_lesson(chapter_id, lesson_id)

    if lesson is None:
        return {}

    lesson_content = get_lesson_content(lesson_id)

    result = dict(lesson)

    if lesson_content:
        result.update(lesson_content)

    result["chapter_id"] = chapter_id
    result["lesson_id"] = lesson_id

    return result


def get_specialized_tips(lesson_id: str) -> List[str]:
    """
    دریافت نکات تخصصی.
    """
    lesson_content = get_lesson_content(lesson_id)

    if not lesson_content:
        return []

    return [
        _normalize_text(item)
        for item in _normalize_list(
            lesson_content.get("specialized_points")
        )
        if _normalize_text(item)
    ]


def get_exam_tips(lesson_id: str) -> List[str]:
    """
    دریافت نکات آزمونی.
    """
    lesson_content = get_lesson_content(lesson_id)

    if not lesson_content:
        return []

    return [
        _normalize_text(item)
        for item in _normalize_list(
            lesson_content.get("exam_points")
        )
        if _normalize_text(item)
    ]


def get_examples(lesson_id: str) -> List[str]:
    """
    دریافت مثال کاربردی.
    """
    lesson_content = get_lesson_content(lesson_id)

    if not lesson_content:
        return []

    examples = lesson_content.get("practical_example")

    if isinstance(examples, list):
        return [
            _normalize_text(item)
            for item in examples
            if _normalize_text(item)
        ]

    if examples:
        return [_normalize_text(examples)]

    return []


def get_keywords(lesson_id: str) -> List[str]:
    """
    دریافت کلیدواژه‌های درس.
    """
    lesson_content = get_lesson_content(lesson_id)

    if not lesson_content:
        return []

    keywords = lesson_content.get("keywords", [])

    return [
        _normalize_text(item)
        for item in _normalize_list(keywords)
        if _normalize_text(item)
    ]


# ============================================================
# Quiz
# ============================================================

def get_finance_quiz(
    chapter_id: str,
    lesson_id: str,
) -> List[Dict[str, Any]]:
    """
    دریافت آزمون یک درس.
    """
    chapter_id = _normalize_text(chapter_id)
    lesson_id = _normalize_text(lesson_id)

    if not chapter_id or not lesson_id:
        return []

    questions = _safe_call(
        "get_quiz",
        chapter_id,
        lesson_id,
        default=None,
    )

    if questions is None:
        quiz_map = getattr(data, "FINANCE_QUIZ_QUESTIONS", None)

        if isinstance(quiz_map, dict):
            questions = quiz_map.get(
                (chapter_id, lesson_id),
                [],
            )

    if questions is None:
        lesson_content = get_lesson_content(lesson_id)

        if lesson_content:
            questions = lesson_content.get("quiz", [])

    questions = _normalize_list(questions)

    normalized = []

    for question in questions:
        if not isinstance(question, dict):
            continue

        item = dict(question)

        item.setdefault("question", "")
        item.setdefault("options", [])
        item.setdefault("correct_index", 0)

        item["question"] = _normalize_text(item["question"])
        item["options"] = [
            _normalize_text(option)
            for option in _normalize_list(item["options"])
        ]

        try:
            item["correct_index"] = int(item["correct_index"])
        except (TypeError, ValueError):
            item["correct_index"] = 0

        if item["question"] and item["options"]:
            normalized.append(item)

    return normalized


def get_all_quiz_questions() -> List[Dict[str, Any]]:
    """
    دریافت تمام سوالات آزمون مدیریت مالی.
    """
    questions = _safe_call(
        "get_all_quiz_questions",
        default=None,
    )

    if questions is None:
        quiz_map = getattr(
            data,
            "FINANCE_QUIZ_QUESTIONS",
            {},
        )

        questions = []

        if isinstance(quiz_map, dict):
            for key, values in quiz_map.items():
                chapter_id = ""
                lesson_id = ""

                if isinstance(key, tuple) and len(key) >= 2:
                    chapter_id = _normalize_text(key[0])
                    lesson_id = _normalize_text(key[1])

                for question in _normalize_list(values):
                    if not isinstance(question, dict):
                        continue

                    item = dict(question)
                    item.setdefault(
                        "chapter_id",
                        chapter_id,
                    )
                    item.setdefault(
                        "lesson_id",
                        lesson_id,
                    )

                    questions.append(item)

    normalized = []

    for question in _normalize_list(questions):
        if not isinstance(question, dict):
            continue

        item = dict(question)

        item.setdefault("question", "")
        item.setdefault("options", [])
        item.setdefault("correct_index", 0)

        if _normalize_text(item.get("question")):
            normalized.append(item)

    return normalized


def get_finance_chapter_quiz(
    chapter_id: str,
) -> List[Dict[str, Any]]:
    """
    دریافت تمام سوالات یک فصل.
    """
    chapter_id = _normalize_text(chapter_id)

    if not chapter_id:
        return []

    questions = []

    for lesson in get_finance_lessons(chapter_id):
        lesson_id = lesson.get("id")

        if not lesson_id:
            continue

        for question in get_finance_quiz(
            chapter_id,
            lesson_id,
        ):
            item = dict(question)
            item.setdefault("chapter_id", chapter_id)
            item.setdefault("lesson_id", lesson_id)
            questions.append(item)

    return questions


# ============================================================
# Statistics
# ============================================================

def get_total_lesson_count() -> int:
    """
    تعداد کل درس‌ها.
    """
    total = 0

    for chapter in get_finance_chapters():
        chapter_id = chapter.get("id")

        if chapter_id:
            total += len(
                get_finance_lessons(chapter_id)
            )

    return total


def get_total_quiz_count() -> int:
    """
    تعداد کل سوالات آزمون.
    """
    return len(get_all_quiz_questions())


def get_curriculum_stats() -> Dict[str, Any]:
    """
    آمار کامل دوره مدیریت مالی.
    """
    chapters = get_finance_chapters()

    lesson_count = 0

    for chapter in chapters:
        chapter_id = chapter.get("id")

        if chapter_id:
            lesson_count += len(
                get_finance_lessons(chapter_id)
            )

    quiz_count = get_total_quiz_count()

    return {
        "module_id": MODULE_ID,
        "title": get_module_title(),
        "chapter_count": len(chapters),
        "lesson_count": lesson_count,
        "quiz_count": quiz_count,
        "average_lessons_per_chapter": (
            round(lesson_count / len(chapters), 2)
            if chapters
            else 0
        ),
    }


def get_finance_statistics() -> Dict[str, Any]:
    """
    Alias آماری برای سازگاری.
    """
    return get_curriculum_stats()


# ============================================================
# Search
# ============================================================

def search_content(
    query: str,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """
    جست‌وجوی محتوای مدیریت مالی.

    جست‌وجو در:
    - عنوان فصل
    - عنوان درس
    - متن درس
    - زیرموضوع‌ها
    - نکات تخصصی
    - نکات آزمونی
    - مثال کاربردی
    - کلیدواژه‌ها
    """
    query = _normalize_text(query).lower()

    if not query:
        return []

    try:
        limit = max(1, int(limit))
    except (TypeError, ValueError):
        limit = 20

    results = []

    for chapter in get_finance_chapters():
        chapter_id = chapter.get("id", "")
        chapter_title = chapter.get("title", "")

        for lesson in get_finance_lessons(chapter_id):
            lesson_id = lesson.get("id", "")
            lesson_title = lesson.get("title", "")

            complete = get_complete_lesson(
                chapter_id,
                lesson_id,
            )

            searchable_parts = [
                chapter_title,
                lesson_title,
                complete.get("lesson_text", ""),
                complete.get("detailed_content", ""),
                complete.get("practical_example", ""),
            ]

            searchable_parts.extend(
                _normalize_list(
                    complete.get("subtopics", [])
                )
            )

            searchable_parts.extend(
                _normalize_list(
                    complete.get("specialized_points", [])
                )
            )

            searchable_parts.extend(
                _normalize_list(
                    complete.get("exam_points", [])
                )
            )

            searchable_parts.extend(
                _normalize_list(
                    complete.get("keywords", [])
                )
            )

            searchable_text = " ".join(
                _normalize_text(part)
                for part in searchable_parts
                if _normalize_text(part)
            ).lower()

            if query in searchable_text:
                results.append(
                    {
                        "chapter_id": chapter_id,
                        "chapter_title": chapter_title,
                        "lesson_id": lesson_id,
                        "lesson_title": lesson_title,
                        "content": complete,
                    }
                )

                if len(results) >= limit:
                    return results

    return results


# ============================================================
# Validation
# ============================================================

def validate_curriculum() -> Dict[str, Any]:
    """
    اعتبارسنجی ساختار آموزشی مدیریت مالی.
    """
    chapters = get_finance_chapters()

    errors = []
    warnings = []

    if not chapters:
        errors.append(
            "هیچ فصلی برای ماژول مدیریت مالی یافت نشد."
        )

    chapter_ids = set()

    for chapter in chapters:
        chapter_id = _normalize_text(
            chapter.get("id")
        )

        chapter_title = _normalize_text(
            chapter.get("title")
        )

        if not chapter_id:
            errors.append(
                "یک فصل فاقد شناسه است."
            )
            continue

        if chapter_id in chapter_ids:
            errors.append(
                f"شناسه فصل تکراری است: {chapter_id}"
            )

        chapter_ids.add(chapter_id)

        if not chapter_title:
            warnings.append(
                f"فصل {chapter_id} فاقد عنوان است."
            )

        lessons = get_finance_lessons(chapter_id)

        if not lessons:
            warnings.append(
                f"فصل {chapter_id} فاقد درس است."
            )

        lesson_ids = set()

        for lesson in lessons:
            lesson_id = _normalize_text(
                lesson.get("id")
            )

            lesson_title = _normalize_text(
                lesson.get("title")
            )

            if not lesson_id:
                errors.append(
                    f"فصل {chapter_id} دارای درس بدون شناسه است."
                )
                continue

            if lesson_id in lesson_ids:
                errors.append(
                    f"درس تکراری در فصل {chapter_id}: "
                    f"{lesson_id}"
                )

            lesson_ids.add(lesson_id)

            if not lesson_title:
                warnings.append(
                    f"درس {lesson_id} فاقد عنوان است."
                )

            lesson_content = get_lesson_content(
                lesson_id
            )

            if not lesson_content:
                warnings.append(
                    f"برای درس {lesson_id} محتوای آموزشی یافت نشد."
                )

            quiz = get_finance_quiz(
                chapter_id,
                lesson_id,
            )

            if not quiz:
                warnings.append(
                    f"برای درس {lesson_id} آزمون یافت نشد."
                )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "chapter_count": len(chapters),
        "lesson_count": get_total_lesson_count(),
        "quiz_count": get_total_quiz_count(),
    }


# ============================================================
# Health Check
# ============================================================

def finance_health_check() -> Dict[str, Any]:
    """
    بررسی سلامت ماژول مدیریت مالی.
    """
    try:
        validation = validate_curriculum()

        return {
            "module_id": MODULE_ID,
            "status": (
                "healthy"
                if validation["valid"]
                else "warning"
            ),
            "valid": validation["valid"],
            "chapters": validation["chapter_count"],
            "lessons": validation["lesson_count"],
            "quizzes": validation["quiz_count"],
            "errors": validation["errors"],
            "warnings": validation["warnings"],
        }

    except Exception as exc:
        return {
            "module_id": MODULE_ID,
            "status": "error",
            "valid": False,
            "chapters": 0,
            "lessons": 0,
            "quizzes": 0,
            "errors": [
                f"Finance service error: {exc}"
            ],
            "warnings": [],
        }


# ============================================================
# Compatibility Aliases
# ============================================================

get_chapters = get_finance_chapters
get_chapter = get_finance_chapter
get_lessons = get_finance_lessons
get_lesson = get_finance_lesson
get_quiz = get_finance_quiz
get_all_questions = get_all_quiz_questions
get_chapter_quiz = get_finance_chapter_quiz
get_statistics = get_curriculum_stats
health_check = finance_health_check


# ============================================================
# Public API
# ============================================================

__all__ = [
    "get_module_title",
    "get_module_description",
    "get_module_info",

    "get_finance_chapters",
    "get_finance_chapter",

    "get_finance_lessons",
    "get_finance_lesson",
    "get_complete_lesson",
    "get_lesson_content",

    "get_specialized_tips",
    "get_exam_tips",
    "get_examples",
    "get_keywords",

    "get_finance_quiz",
    "get_finance_chapter_quiz",
    "get_all_quiz_questions",

    "get_total_lesson_count",
    "get_total_quiz_count",
    "get_curriculum_stats",
    "get_finance_statistics",

    "search_content",

    "validate_curriculum",
    "finance_health_check",

    "get_chapters",
    "get_chapter",
    "get_lessons",
    "get_lesson",
    "get_quiz",
    "get_all_questions",
    "get_chapter_quiz",
    "get_statistics",
    "health_check",
]
