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
- محاسبه نتیجه آزمون
- ثبت Attempt آزمون
- بازیابی سوابق آزمون
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
# Database
# ============================================================

try:
    from core.database import (
        save_quiz_attempt as db_save_quiz_attempt,
        get_quiz_attempts as db_get_quiz_attempts,
    )
except Exception:
    db_save_quiz_attempt = None
    db_get_quiz_attempts = None


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
    اجرای امن تابع از data.py.
    """
    function = getattr(
        data,
        function_name,
        None,
    )

    if not callable(function):
        return default

    try:
        return function(
            *args,
            **kwargs,
        )

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
    function = getattr(
        content,
        function_name,
        None,
    )

    if not callable(function):
        return default

    try:
        return function(
            *args,
            **kwargs,
        )

    except Exception:
        return default


def _normalize_text(
    value: Any,
    default: str = "",
) -> str:
    """
    نرمال‌سازی متن.
    """
    if value is None:
        return default

    return str(value).strip()


def _normalize_list(
    value: Any,
) -> List[Any]:
    """
    تبدیل خروجی‌های مختلف به لیست.
    """
    if value is None:
        return []

    if isinstance(
        value,
        list,
    ):
        return value

    if isinstance(
        value,
        tuple,
    ):
        return list(value)

    if isinstance(
        value,
        set,
    ):
        return list(value)

    return [value]


def _get_id(
    item: Any,
) -> str:
    """
    دریافت شناسه از dict/object.
    """
    if isinstance(
        item,
        dict,
    ):

        return _normalize_text(
            item.get("id")
            or item.get("chapter_id")
            or item.get("lesson_id")
            or item.get("key")
        )

    return _normalize_text(
        getattr(
            item,
            "id",
            None,
        )
        or getattr(
            item,
            "chapter_id",
            None,
        )
        or getattr(
            item,
            "lesson_id",
            None,
        )
    )


def _get_title(
    item: Any,
) -> str:
    """
    دریافت عنوان از dict/object.
    """
    if isinstance(
        item,
        dict,
    ):

        return _normalize_text(
            item.get("title")
            or item.get("name")
            or item.get("chapter_title")
            or item.get("lesson_title")
        )

    return _normalize_text(
        getattr(
            item,
            "title",
            None,
        )
        or getattr(
            item,
            "name",
            None,
        )
    )


def _get_quiz_correct_index(
    question: Dict[str, Any],
) -> Optional[int]:
    """
    دریافت index پاسخ صحیح سؤال.

    پشتیبانی از:
    - correct_index
    - answer_index
    - correct_answer
    - answer
    """
    if not isinstance(
        question,
        dict,
    ):
        return None

    raw_value = None

    for key in (
        "correct_index",
        "answer_index",
        "correct_answer",
        "answer",
    ):

        if key in question:

            value = question.get(
                key
            )

            if value is not None:

                raw_value = value
                break

    if raw_value is None:
        return None

    try:

        return int(
            raw_value
        )

    except (
        TypeError,
        ValueError,
    ):

        return None


# ============================================================
# Module Information
# ============================================================

def get_module_title() -> str:
    """
    عنوان ماژول مدیریت مالی.
    """
    title = getattr(
        data,
        "MODULE_TITLE",
        None,
    )

    return _normalize_text(
        title,
        DEFAULT_MODULE_TITLE,
    )


def get_module_description() -> str:
    """
    توضیحات ماژول.
    """
    description = getattr(
        data,
        "MODULE_DESCRIPTION",
        None,
    )

    if description:

        return _normalize_text(
            description
        )

    return (
        "دوره تخصصی مدیریت مالی شامل مبانی مالی، "
        "تحلیل صورت‌های مالی، تصمیم‌گیری مالی، "
        "بودجه‌بندی، سرمایه‌گذاری، تأمین مالی، "
        "مدیریت سرمایه در گردش و مدیریت ریسک."
    )


def get_module_info() -> Dict[str, Any]:
    """
    اطلاعات کامل ماژول.
    """
    info: Dict[str, Any] = {}

    raw_info = getattr(
        data,
        "get_module_info",
        None,
    )

    if callable(
        raw_info
    ):

        try:

            result = raw_info()

            if isinstance(
                result,
                dict,
            ):

                info.update(
                    result
                )

        except Exception:
            pass

    info.setdefault(
        "module_id",
        MODULE_ID,
    )

    info.setdefault(
        "id",
        MODULE_ID,
    )

    info.setdefault(
        "title",
        get_module_title(),
    )

    info.setdefault(
        "description",
        get_module_description(),
    )

    chapters = get_finance_chapters()

    info.setdefault(
        "chapter_count",
        len(chapters),
    )

    info.setdefault(
        "chapters",
        len(chapters),
    )

    info.setdefault(
        "lesson_count",
        get_total_lesson_count(),
    )

    info.setdefault(
        "lessons",
        get_total_lesson_count(),
    )

    info.setdefault(
        "quiz_count",
        len(
            get_all_quiz_questions()
        ),
    )

    return info


# ============================================================
# Chapters
# ============================================================

def get_finance_chapters() -> List[Dict[str, Any]]:
    """
    دریافت تمام فصل‌های مدیریت مالی.
    """
    chapters = None

    raw_get_chapters = getattr(
        data,
        "get_chapters",
        None,
    )

    if callable(
        raw_get_chapters
    ):

        try:

            chapters = raw_get_chapters()

        except (
            TypeError,
            Exception,
        ):

            chapters = None

    if chapters is None:

        chapters = getattr(
            data,
            "CHAPTERS",
            None,
        )

    if chapters is None:

        chapters = getattr(
            data,
            "FINANCE_CHAPTERS",
            None,
        )

    chapters = _normalize_list(
        chapters
    )

    normalized: List[Dict[str, Any]] = []

    for chapter in chapters:

        if isinstance(
            chapter,
            dict,
        ):

            item = dict(
                chapter
            )

        else:

            item = {
                "id": _get_id(
                    chapter
                ),
                "title": _get_title(
                    chapter
                ),
            }

        item["id"] = _normalize_text(
            item.get("id")
        )

        item["title"] = _normalize_text(
            item.get("title")
        )

        if item["id"]:

            normalized.append(
                item
            )

    return normalized


def get_finance_chapter(
    chapter_id: str,
) -> Optional[Dict[str, Any]]:
    """
    دریافت یک فصل مشخص.
    """
    chapter_id = _normalize_text(
        chapter_id
    )

    if not chapter_id:
        return None

    raw_get_chapter = getattr(
        data,
        "get_chapter",
        None,
    )

    if callable(
        raw_get_chapter
    ):

        try:

            chapter = raw_get_chapter(
                chapter_id
            )

            if chapter is not None:

                if isinstance(
                    chapter,
                    dict,
                ):

                    result = dict(
                        chapter
                    )

                else:

                    result = {
                        "id": _get_id(
                            chapter
                        ),
                        "title": _get_title(
                            chapter
                        ),
                    }

                result["id"] = _normalize_text(
                    result.get("id"),
                    chapter_id,
                )

                result["title"] = _normalize_text(
                    result.get("title")
                )

                return result

        except Exception:
            pass

    for chapter in get_finance_chapters():

        if chapter.get(
            "id"
        ) == chapter_id:

            return dict(
                chapter
            )

    return None


# ============================================================
# Lessons
# ============================================================

def _get_all_finance_lessons_from_data() -> List[Dict[str, Any]]:
    """
    دریافت تمام درس‌ها از data.py.
    """
    lessons = None

    raw_get_lessons = getattr(
        data,
        "get_lessons",
        None,
    )

    if callable(
        raw_get_lessons
    ):

        try:

            lessons = raw_get_lessons()

        except (
            TypeError,
            Exception,
        ):

            lessons = None

    if lessons is None:

        lessons = getattr(
            data,
            "LESSONS",
            None,
        )

    if lessons is None:

        lessons = getattr(
            data,
            "FINANCE_LESSONS",
            None,
        )

    if isinstance(
        lessons,
        dict,
    ):

        flattened: List[Any] = []

        for key, value in lessons.items():

            values = _normalize_list(
                value
            )

            for lesson in values:

                if isinstance(
                    lesson,
                    dict,
                ):

                    item = dict(
                        lesson
                    )

                    if not item.get(
                        "chapter_id"
                    ):

                        item["chapter_id"] = key

                    flattened.append(
                        item
                    )

                else:

                    flattened.append(
                        lesson
                    )

        lessons = flattened

    lessons = _normalize_list(
        lessons
    )

    normalized: List[Dict[str, Any]] = []

    for lesson in lessons:

        if isinstance(
            lesson,
            dict,
        ):

            item = dict(
                lesson
            )

        else:

            item = {
                "id": _get_id(
                    lesson
                ),
                "title": _get_title(
                    lesson
                ),
            }

        item["id"] = _normalize_text(
            item.get("id")
        )

        item["title"] = _normalize_text(
            item.get("title")
        )

        item["chapter_id"] = _normalize_text(
            item.get("chapter_id")
        )

        if item["id"]:

            normalized.append(
                item
            )

    return normalized


def get_finance_lessons(
    chapter_id: str,
) -> List[Dict[str, Any]]:
    """
    دریافت درس‌های یک فصل.
    """
    chapter_id = _normalize_text(
        chapter_id
    )

    if not chapter_id:
        return []

    all_lessons = (
        _get_all_finance_lessons_from_data()
    )

    normalized: List[Dict[str, Any]] = []

    for lesson in all_lessons:

        lesson_chapter_id = _normalize_text(
            lesson.get(
                "chapter_id"
            )
        )

        if lesson_chapter_id != chapter_id:
            continue

        item = dict(
            lesson
        )

        item["chapter_id"] = chapter_id

        normalized.append(
            item
        )

    return normalized


def get_finance_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Optional[Dict[str, Any]]:
    """
    دریافت یک درس مشخص.
    """
    chapter_id = _normalize_text(
        chapter_id
    )

    lesson_id = _normalize_text(
        lesson_id
    )

    if not chapter_id or not lesson_id:
        return None

    raw_get_lesson = getattr(
        data,
        "get_lesson",
        None,
    )

    if callable(
        raw_get_lesson
    ):

        try:

            lesson = raw_get_lesson(
                chapter_id,
                lesson_id,
            )

            if lesson is not None:

                if isinstance(
                    lesson,
                    dict,
                ):

                    result = dict(
                        lesson
                    )

                else:

                    result = {
                        "id": _get_id(
                            lesson
                        ),
                        "title": _get_title(
                            lesson
                        ),
                    }

                result["id"] = _normalize_text(
                    result.get("id"),
                    lesson_id,
                )

                result["title"] = _normalize_text(
                    result.get("title")
                )

                result["chapter_id"] = chapter_id

                return result

        except (
            TypeError,
            Exception,
        ):

            pass

    for lesson in get_finance_lessons(
        chapter_id
    ):

        if lesson.get(
            "id"
        ) == lesson_id:

            return dict(
                lesson
            )

    return None


# ============================================================
# Educational Content
# ============================================================

def get_lesson_content(
    lesson_id: str,
) -> Optional[Dict[str, Any]]:
    """
    دریافت محتوای کامل یک درس از content.py.
    """
    lesson_id = _normalize_text(
        lesson_id
    )

    if not lesson_id:
        return None

    result = _safe_content_call(
        "get_lesson_content",
        lesson_id,
        default=None,
    )

    if result is None:
        return None

    if not isinstance(
        result,
        dict,
    ):

        return {
            "lesson_id": lesson_id,
            "lesson_text": _normalize_text(
                result
            ),
        }

    content_data = dict(
        result
    )

    content_data.setdefault(
        "lesson_id",
        lesson_id,
    )

    content_data.setdefault(
        "lesson_text",
        content_data.get(
            "content",
            "",
        ),
    )

    content_data.setdefault(
        "subtopics",
        [],
    )

    content_data.setdefault(
        "detailed_content",
        "",
    )

    content_data.setdefault(
        "specialized_points",
        [],
    )

    content_data.setdefault(
        "exam_points",
        [],
    )

    content_data.setdefault(
        "practical_example",
        "",
    )

    content_data.setdefault(
        "review",
        [],
    )

    return content_data


def get_complete_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Dict[str, Any]:
    """
    ترکیب اطلاعات Data و Content.
    """
    lesson = get_finance_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return {}

    lesson_content = get_lesson_content(
        lesson_id
    )

    result = dict(
        lesson
    )

    if lesson_content:

        result.update(
            lesson_content
        )

    result["chapter_id"] = chapter_id
    result["lesson_id"] = lesson_id

    return result


def get_specialized_tips(
    lesson_id: str,
) -> List[str]:
    """
    دریافت نکات تخصصی.
    """
    lesson_content = get_lesson_content(
        lesson_id
    )

    if not lesson_content:
        return []

    return [
        _normalize_text(item)
        for item in _normalize_list(
            lesson_content.get(
                "specialized_points"
            )
        )
        if _normalize_text(item)
    ]


def get_exam_tips(
    lesson_id: str,
) -> List[str]:
    """
    دریافت نکات آزمونی.
    """
    lesson_content = get_lesson_content(
        lesson_id
    )

    if not lesson_content:
        return []

    return [
        _normalize_text(item)
        for item in _normalize_list(
            lesson_content.get(
                "exam_points"
            )
        )
        if _normalize_text(item)
    ]


def get_examples(
    lesson_id: str,
) -> List[str]:
    """
    دریافت مثال‌های کاربردی.
    """
    lesson_content = get_lesson_content(
        lesson_id
    )

    if not lesson_content:
        return []

    examples = lesson_content.get(
        "practical_example"
    )

    if isinstance(
        examples,
        list,
    ):

        return [
            _normalize_text(item)
            for item in examples
            if _normalize_text(item)
        ]

    if examples:

        return [
            _normalize_text(
                examples
            )
        ]

    return []


def get_keywords(
    lesson_id: str,
) -> List[str]:
    """
    دریافت کلیدواژه‌های درس.
    """
    lesson_content = get_lesson_content(
        lesson_id
    )

    if not lesson_content:
        return []

    keywords = lesson_content.get(
        "keywords",
        [],
    )

    return [
        _normalize_text(item)
        for item in _normalize_list(
            keywords
        )
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
    chapter_id = _normalize_text(
        chapter_id
    )

    lesson_id = _normalize_text(
        lesson_id
    )

    if not chapter_id or not lesson_id:
        return []

    questions = _safe_call(
        "get_quiz",
        chapter_id,
        lesson_id,
        default=None,
    )

    if questions is None:

        quiz_map = getattr(
            data,
            "FINANCE_QUIZ_QUESTIONS",
            None,
        )

        if isinstance(
            quiz_map,
            dict,
        ):

            questions = quiz_map.get(
                (
                    chapter_id,
                    lesson_id,
                ),
                [],
            )

    if questions is None:

        lesson_content = get_lesson_content(
            lesson_id
        )

        if lesson_content:

            questions = lesson_content.get(
                "quiz",
                [],
            )

    questions = _normalize_list(
        questions
    )

    normalized: List[Dict[str, Any]] = []

    for question in questions:

        if not isinstance(
            question,
            dict,
        ):
            continue

        item = dict(
            question
        )

        item.setdefault(
            "question",
            "",
        )

        item.setdefault(
            "options",
            [],
        )

        item.setdefault(
            "correct_index",
            0,
        )

        item["question"] = _normalize_text(
            item["question"]
        )

        item["options"] = [
            _normalize_text(option)
            for option in _normalize_list(
                item["options"]
            )
        ]

        try:

            item["correct_index"] = int(
                item["correct_index"]
            )

        except (
            TypeError,
            ValueError,
        ):

            item["correct_index"] = 0

        if (
            item["question"]
            and item["options"]
        ):

            item["chapter_id"] = chapter_id
            item["lesson_id"] = lesson_id

            normalized.append(
                item
            )

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

        if isinstance(
            quiz_map,
            dict,
        ):

            for key, values in quiz_map.items():

                chapter_id = ""
                lesson_id = ""

                if (
                    isinstance(key, tuple)
                    and len(key) >= 2
                ):

                    chapter_id = _normalize_text(
                        key[0]
                    )

                    lesson_id = _normalize_text(
                        key[1]
                    )

                for question in _normalize_list(
                    values
                ):

                    if not isinstance(
                        question,
                        dict,
                    ):
                        continue

                    item = dict(
                        question
                    )

                    item.setdefault(
                        "chapter_id",
                        chapter_id,
                    )

                    item.setdefault(
                        "lesson_id",
                        lesson_id,
                    )

                    questions.append(
                        item
                    )

    normalized: List[Dict[str, Any]] = []

    for question in _normalize_list(
        questions
    ):

        if not isinstance(
            question,
            dict,
        ):
            continue

        item = dict(
            question
        )

        item.setdefault(
            "question",
            "",
        )

        item.setdefault(
            "options",
            [],
        )

        item.setdefault(
            "correct_index",
            0,
        )

        item["question"] = _normalize_text(
            item.get("question")
        )

        item["options"] = [
            _normalize_text(option)
            for option in _normalize_list(
                item.get(
                    "options",
                    [],
                )
            )
        ]

        try:

            item["correct_index"] = int(
                item.get(
                    "correct_index",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            item["correct_index"] = 0

        if item["question"]:

            normalized.append(
                item
            )

    return normalized


def get_finance_chapter_quiz(
    chapter_id: str,
) -> List[Dict[str, Any]]:
    """
    دریافت تمام سوالات یک فصل.
    """
    chapter_id = _normalize_text(
        chapter_id
    )

    if not chapter_id:
        return []

    questions: List[Dict[str, Any]] = []

    for lesson in get_finance_lessons(
        chapter_id
    ):

        lesson_id = lesson.get(
            "id"
        )

        if not lesson_id:
            continue

        for question in get_finance_quiz(
            chapter_id,
            lesson_id,
        ):

            item = dict(
                question
            )

            item.setdefault(
                "chapter_id",
                chapter_id,
            )

            item.setdefault(
                "lesson_id",
                lesson_id,
            )

            questions.append(
                item
            )

    return questions


# ============================================================
# Quiz Result
# ============================================================

def calculate_quiz_score(
    total_questions: int,
    correct_answers: int,
) -> float:
    """
    محاسبه درصد آزمون.
    """
    try:

        total_questions = int(
            total_questions
        )

        correct_answers = int(
            correct_answers
        )

    except (
        TypeError,
        ValueError,
    ):

        return 0.0

    if total_questions <= 0:
        return 0.0

    correct_answers = max(
        0,
        min(
            correct_answers,
            total_questions,
        ),
    )

    return round(
        (
            correct_answers
            / total_questions
        )
        * 100,
        2,
    )


def calculate_quiz_result(
    quiz: List[Dict[str, Any]],
    answers: List[int],
) -> Dict[str, Any]:
    """
    محاسبه نتیجه کامل آزمون.
    """
    questions = _normalize_list(
        quiz
    )

    submitted_answers = _normalize_list(
        answers
    )

    total_questions = len(
        questions
    )

    correct_answers = 0
    answered_questions = 0

    results: List[Dict[str, Any]] = []

    for index, question in enumerate(
        questions
    ):

        selected_index = None

        if index < len(
            submitted_answers
        ):

            raw_answer = submitted_answers[
                index
            ]

            if raw_answer is not None:

                try:

                    selected_index = int(
                        raw_answer
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    selected_index = None

        correct_index = _get_quiz_correct_index(
            question
        )

        options = _normalize_list(
            question.get(
                "options",
                [],
            )
        )

        if (
            correct_index is not None
            and (
                correct_index < 0
                or correct_index >= len(options)
            )
        ):

            correct_index = None

        is_answered = (
            selected_index is not None
        )

        if is_answered:

            answered_questions += 1

        is_correct = (
            is_answered
            and correct_index is not None
            and selected_index == correct_index
        )

        if is_correct:

            correct_answers += 1

        results.append(
            {
                "question_index": index,
                "selected_index": selected_index,
                "correct_index": correct_index,
                "answered": is_answered,
                "correct": is_correct,
            }
        )

    wrong_answers = (
        answered_questions
        - correct_answers
    )

    unanswered_questions = (
        total_questions
        - answered_questions
    )

    score = calculate_quiz_score(
        total_questions,
        correct_answers,
    )

    return {
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "unanswered_questions": unanswered_questions,
        "score": score,
        "results": results,
    }


# ============================================================
# Quiz Attempts
# ============================================================

def start_quiz_attempt(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
) -> Dict[str, Any]:
    """
    ایجاد وضعیت اولیه Attempt آزمون.
    """
    try:

        telegram_id = int(
            telegram_id
        )

    except (
        TypeError,
        ValueError,
    ):

        telegram_id = 0

    try:

        total_questions = int(
            total_questions
        )

    except (
        TypeError,
        ValueError,
    ):

        total_questions = 0

    return {
        "telegram_id": telegram_id,
        "module_id": _normalize_text(
            module_id,
            MODULE_ID,
        ),
        "chapter_id": _normalize_text(
            chapter_id
        ),
        "lesson_id": _normalize_text(
            lesson_id
        ),
        "total_questions": max(
            0,
            total_questions,
        ),
        "current_question": 0,
        "answers": [],
        "correct_answers": 0,
        "completed": False,
    }


def save_quiz_attempt(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    total_questions: int,
    correct_answers: int,
    score: float | None = None,
) -> Optional[int]:
    """
    ثبت Attempt تکمیل‌شده در دیتابیس.
    """
    if db_save_quiz_attempt is None:
        return None

    try:

        telegram_id = int(
            telegram_id
        )

        total_questions = int(
            total_questions
        )

        correct_answers = int(
            correct_answers
        )

    except (
        TypeError,
        ValueError,
    ):

        return None

    total_questions = max(
        0,
        total_questions,
    )

    correct_answers = max(
        0,
        min(
            correct_answers,
            total_questions,
        ),
    )

    if score is None:

        score = calculate_quiz_score(
            total_questions,
            correct_answers,
        )

    try:

        score = float(
            score
        )

    except (
        TypeError,
        ValueError,
    ):

        score = calculate_quiz_score(
            total_questions,
            correct_answers,
        )

    score = max(
        0.0,
        min(
            score,
            100.0,
        ),
    )

    try:

        return db_save_quiz_attempt(
            telegram_id=telegram_id,
            module_id=_normalize_text(
                module_id,
                MODULE_ID,
            ),
            chapter_id=_normalize_text(
                chapter_id
            ),
            lesson_id=_normalize_text(
                lesson_id
            ),
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
        )

    except Exception:

        return None


def get_finance_quiz_attempts(
    telegram_id: int,
) -> List[Dict[str, Any]]:
    """
    دریافت تمام سوابق آزمون‌های مدیریت مالی
    برای یک کاربر.

    خروجی شامل رکوردهای ذخیره‌شده در:
        quiz_attempts

    است.
    """
    if db_get_quiz_attempts is None:
        return []

    try:

        telegram_id = int(
            telegram_id
        )

    except (
        TypeError,
        ValueError,
    ):

        return []

    if telegram_id <= 0:
        return []

    try:

        attempts = db_get_quiz_attempts(
            telegram_id=telegram_id,
            module_id=MODULE_ID,
        )

    except TypeError:

        try:

            attempts = db_get_quiz_attempts(
                telegram_id,
                MODULE_ID,
            )

        except Exception:

            return []

    except Exception:

        return []

    attempts = _normalize_list(
        attempts
    )

    normalized: List[Dict[str, Any]] = []

    for attempt in attempts:

        if isinstance(
            attempt,
            dict,
        ):

            item = dict(
                attempt
            )

        else:

            item = {
                "id": getattr(
                    attempt,
                    "id",
                    None,
                ),
            }

        item.setdefault(
            "module_id",
            MODULE_ID,
        )

        normalized.append(
            item
        )

    return normalized


def get_finance_quiz_attempt(
    telegram_id: int,
    attempt_id: int,
) -> Optional[Dict[str, Any]]:
    """
    دریافت یک سابقه آزمون مشخص.
    """
    try:

        attempt_id = int(
            attempt_id
        )

    except (
        TypeError,
        ValueError,
    ):

        return None

    if attempt_id <= 0:
        return None

    attempts = get_finance_quiz_attempts(
        telegram_id
    )

    for attempt in attempts:

        try:

            current_id = int(
                attempt.get(
                    "id",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            continue

        if current_id == attempt_id:

            return dict(
                attempt
            )

    return None


def get_finance_attempt_statistics(
    telegram_id: int,
) -> Dict[str, Any]:
    """
    محاسبه آمار سوابق آزمون‌های مدیریت مالی.
    """
    attempts = get_finance_quiz_attempts(
        telegram_id
    )

    total_attempts = len(
        attempts
    )

    total_questions = 0
    total_correct = 0
    total_score = 0.0

    best_score = 0.0

    for attempt in attempts:

        try:

            questions = int(
                attempt.get(
                    "total_questions",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            questions = 0

        try:

            correct = int(
                attempt.get(
                    "correct_answers",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            correct = 0

        try:

            score = float(
                attempt.get(
                    "score",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            score = 0.0

        total_questions += max(
            0,
            questions,
        )

        total_correct += max(
            0,
            correct,
        )

        total_score += score

        best_score = max(
            best_score,
            score,
        )

    average_score = (
        round(
            total_score
            / total_attempts,
            2,
        )
        if total_attempts
        else 0.0
    )

    overall_score = (
        round(
            (
                total_correct
                / total_questions
            )
            * 100,
            2,
        )
        if total_questions
        else 0.0
    )

    return {
        "module_id": MODULE_ID,
        "total_attempts": total_attempts,
        "total_questions": total_questions,
        "total_correct_answers": total_correct,
        "average_score": average_score,
        "best_score": best_score,
        "overall_score": overall_score,
    }


def complete_quiz_attempt(
    telegram_id: int,
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    quiz: List[Dict[str, Any]],
    answers: List[int],
) -> Dict[str, Any]:
    """
    محاسبه نتیجه و ثبت Attempt آزمون.
    """
    result = calculate_quiz_result(
        quiz,
        answers,
    )

    attempt_id = save_quiz_attempt(
        telegram_id=telegram_id,
        module_id=module_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=result[
            "total_questions"
        ],
        correct_answers=result[
            "correct_answers"
        ],
        score=result[
            "score"
        ],
    )

    result["attempt_id"] = attempt_id

    result["saved"] = (
        attempt_id is not None
    )

    return result


# ============================================================
# Quiz Question
# ============================================================

def get_quiz_question(
    quiz: List[Dict[str, Any]],
    question_index: int,
) -> Optional[Dict[str, Any]]:
    """
    دریافت یک سؤال بر اساس index.
    """
    try:

        question_index = int(
            question_index
        )

    except (
        TypeError,
        ValueError,
    ):

        return None

    if question_index < 0:
        return None

    questions = _normalize_list(
        quiz
    )

    if question_index >= len(
        questions
    ):

        return None

    question = questions[
        question_index
    ]

    if not isinstance(
        question,
        dict,
    ):

        return None

    return dict(
        question
    )


def validate_quiz_answer(
    question: Dict[str, Any],
    selected_index: int,
) -> Dict[str, Any]:
    """
    بررسی یک پاسخ آزمون بدون ثبت دیتابیس.
    """
    if not isinstance(
        question,
        dict,
    ):

        return {
            "valid": False,
            "answered": False,
            "correct": False,
            "selected_index": None,
            "correct_index": None,
        }

    try:

        selected_index = int(
            selected_index
        )

    except (
        TypeError,
        ValueError,
    ):

        return {
            "valid": False,
            "answered": False,
            "correct": False,
            "selected_index": None,
            "correct_index": None,
        }

    options = _normalize_list(
        question.get(
            "options",
            [],
        )
    )

    correct_index = _get_quiz_correct_index(
        question
    )

    if (
        correct_index is not None
        and (
            correct_index < 0
            or correct_index >= len(options)
        )
    ):

        correct_index = None

    if not options:

        return {
            "valid": False,
            "answered": False,
            "correct": False,
            "selected_index": selected_index,
            "correct_index": correct_index,
        }

    if (
        selected_index < 0
        or selected_index >= len(options)
    ):

        return {
            "valid": False,
            "answered": False,
            "correct": False,
            "selected_index": selected_index,
            "correct_index": correct_index,
        }

    is_correct = (
        correct_index is not None
        and selected_index == correct_index
    )

    return {
        "valid": True,
        "answered": True,
        "correct": is_correct,
        "selected_index": selected_index,
        "correct_index": correct_index,
    }


# ============================================================
# Statistics
# ============================================================

def get_total_lesson_count() -> int:
    """
    تعداد کل درس‌ها.
    """
    return len(
        _get_all_finance_lessons_from_data()
    )


def get_total_quiz_count() -> int:
    """
    تعداد کل سوالات آزمون.
    """
    return len(
        get_all_quiz_questions()
    )


def get_curriculum_stats() -> Dict[str, Any]:
    """
    آمار کامل دوره مدیریت مالی.
    """
    chapters = get_finance_chapters()

    lesson_count = get_total_lesson_count()
    quiz_count = get_total_quiz_count()

    return {
        "module_id": MODULE_ID,
        "title": get_module_title(),
        "chapter_count": len(
            chapters
        ),
        "lesson_count": lesson_count,
        "quiz_count": quiz_count,
        "average_lessons_per_chapter": (
            round(
                lesson_count
                / len(chapters),
                2,
            )
            if chapters
            else 0
        ),
    }


def get_finance_statistics() -> Dict[str, Any]:
    """
    Alias آماری.
    """
    return get_curriculum_stats()


def get_curriculum_statistics() -> Dict[str, Any]:
    """
    سازگاری با data.py.
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
    """
    query = _normalize_text(
        query
    ).lower()

    if not query:
        return []

    try:

        limit = max(
            1,
            int(limit),
        )

    except (
        TypeError,
        ValueError,
    ):

        limit = 20

    results: List[Dict[str, Any]] = []

    for chapter in get_finance_chapters():

        chapter_id = chapter.get(
            "id",
            "",
        )

        chapter_title = chapter.get(
            "title",
            "",
        )

        for lesson in get_finance_lessons(
            chapter_id
        ):

            lesson_id = lesson.get(
                "id",
                "",
            )

            lesson_title = lesson.get(
                "title",
                "",
            )

            complete = get_complete_lesson(
                chapter_id,
                lesson_id,
            )

            searchable_parts: List[Any] = [
                chapter_title,
                lesson_title,
                complete.get(
                    "lesson_text",
                    "",
                ),
                complete.get(
                    "detailed_content",
                    "",
                ),
                complete.get(
                    "practical_example",
                    "",
                ),
            ]

            searchable_parts.extend(
                _normalize_list(
                    complete.get(
                        "subtopics",
                        [],
                    )
                )
            )

            searchable_parts.extend(
                _normalize_list(
                    complete.get(
                        "specialized_points",
                        [],
                    )
                )
            )

            searchable_parts.extend(
                _normalize_list(
                    complete.get(
                        "exam_points",
                        [],
                    )
                )
            )

            searchable_parts.extend(
                _normalize_list(
                    complete.get(
                        "keywords",
                        [],
                    )
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

    errors: List[str] = []
    warnings: List[str] = []

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

        chapter_ids.add(
            chapter_id
        )

        if not chapter_title:

            warnings.append(
                f"فصل {chapter_id} فاقد عنوان است."
            )

        lessons = get_finance_lessons(
            chapter_id
        )

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

            lesson_ids.add(
                lesson_id
            )

            if not lesson_title:

                warnings.append(
                    f"درس {lesson_id} فاقد عنوان است."
                )

            lesson_content = get_lesson_content(
                lesson_id
            )

            if not lesson_content:

                warnings.append(
                    f"برای درس {lesson_id} "
                    f"محتوای آموزشی یافت نشد."
                )

            quiz = get_finance_quiz(
                chapter_id,
                lesson_id,
            )

            if not quiz:

                warnings.append(
                    f"برای درس {lesson_id} "
                    f"آزمون یافت نشد."
                )

            for question in quiz:

                options = _normalize_list(
                    question.get(
                        "options",
                        [],
                    )
                )

                correct_index = _get_quiz_correct_index(
                    question
                )

                if len(options) != 4:

                    warnings.append(
                        f"سؤال آزمون درس {lesson_id} "
                        f"دقیقاً ۴ گزینه ندارد."
                    )

                if correct_index is None:

                    warnings.append(
                        f"سؤال آزمون درس {lesson_id} "
                        f"دارای correct_index نامعتبر است."
                    )

                    continue

                if (
                    correct_index < 0
                    or correct_index >= len(options)
                ):

                    warnings.append(
                        f"سؤال آزمون درس {lesson_id} "
                        f"دارای پاسخ صحیح خارج از محدوده گزینه‌هاست."
                    )

    if len(chapters) != 12:

        warnings.append(
            f"تعداد فصل‌ها ۱۲ نیست: {len(chapters)}"
        )

    total_lessons = get_total_lesson_count()

    if total_lessons != 48:

        warnings.append(
            f"تعداد درس‌ها ۴۸ نیست: {total_lessons}"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "chapter_count": len(chapters),
        "lesson_count": total_lessons,
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
            "chapters": validation[
                "chapter_count"
            ],
            "lessons": validation[
                "lesson_count"
            ],
            "quizzes": validation[
                "quiz_count"
            ],
            "errors": validation[
                "errors"
            ],
            "warnings": validation[
                "warnings"
            ],
            "quiz_answer_service": (
                db_save_quiz_attempt
                is not None
            ),
            "quiz_history_service": (
                db_get_quiz_attempts
                is not None
            ),
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
            "quiz_answer_service": False,
            "quiz_history_service": False,
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

get_quiz_attempts = get_finance_quiz_attempts
get_quiz_attempt = get_finance_quiz_attempt
get_attempt_statistics = get_finance_attempt_statistics


# ============================================================
# Public API
# ============================================================

__all__ = [
    # Module
    "get_module_title",
    "get_module_description",
    "get_module_info",

    # Chapters
    "get_finance_chapters",
    "get_finance_chapter",

    # Lessons
    "get_finance_lessons",
    "get_finance_lesson",

    # Content
    "get_complete_lesson",
    "get_lesson_content",
    "get_specialized_tips",
    "get_exam_tips",
    "get_examples",
    "get_keywords",

    # Quiz
    "get_finance_quiz",
    "get_finance_chapter_quiz",
    "get_all_quiz_questions",
    "get_quiz_question",

    # Quiz result
    "calculate_quiz_score",
    "calculate_quiz_result",
    "validate_quiz_answer",

    # Quiz attempt
    "start_quiz_attempt",
    "save_quiz_attempt",
    "get_finance_quiz_attempts",
    "get_finance_quiz_attempt",
    "get_finance_attempt_statistics",
    "complete_quiz_attempt",

    # Statistics
    "get_total_lesson_count",
    "get_total_quiz_count",
    "get_curriculum_stats",
    "get_finance_statistics",
    "get_curriculum_statistics",

    # Search
    "search_content",

    # Validation
    "validate_curriculum",

    # Health
    "finance_health_check",

    # Compatibility
    "get_chapters",
    "get_chapter",
    "get_lessons",
    "get_lesson",
    "get_quiz",
    "get_all_questions",
    "get_chapter_quiz",
    "get_statistics",
    "health_check",

    # History compatibility
    "get_quiz_attempts",
    "get_quiz_attempt",
    "get_attempt_statistics",
]
