"""
Educational content for the Psychology & Social Work module.

Andishkadeh Management & Market
"""

from __future__ import annotations

from typing import Any


MODULE_ID = "psychology"
MODULE_TITLE = "روانشناسی و مددکاری"


PSYCHOLOGY_CURRICULUM: list[dict[str, Any]] = [
    {
        "id": "chapter_1",
        "title": "مبانی روانشناسی",
        "lessons": [
            {
                "id": "lesson_1",
                "title": "تعریف و مفهوم روانشناسی",
                "content": (
                    "روانشناسی علم مطالعه علمی رفتار و فرایندهای ذهنی "
                    "انسان است. این علم تلاش می‌کند رفتار، شناخت، "
                    "هیجان و فرایندهای ذهنی را توصیف و تبیین کند."
                ),
                "special_points": [
                    "روانشناسی بر مطالعه علمی رفتار و فرایندهای ذهنی تمرکز دارد.",
                    "رفتار می‌تواند قابل مشاهده یا قابل اندازه‌گیری باشد.",
                    "فرایندهای شناختی شامل توجه، حافظه، یادگیری و تفکر هستند.",
                ],
                "exam_points": [
                    "تعریف روانشناسی را با مطالعه رفتار و فرایندهای ذهنی به خاطر بسپارید.",
                    "بین رفتار قابل مشاهده و فرایند ذهنی تفاوت قائل شوید.",
                ],
                "example": (
                    "بررسی علت کاهش تمرکز یک دانشجو هنگام مطالعه، "
                    "نمونه‌ای از بررسی یک فرایند روانشناختی است."
                ),
                "questions": [
                    {
                        "id": "q1",
                        "question": "روانشناسی به طور کلی چه چیزی را مطالعه می‌کند؟",
                        "options": [
                            "رفتار و فرایندهای ذهنی",
                            "فقط ساختار بدن",
                            "فقط بیماری‌های جسمی",
                            "فقط روابط اقتصادی",
                        ],
                        "correct_answer": "رفتار و فرایندهای ذهنی",
                        "explanation": (
                            "روانشناسی به مطالعه علمی رفتار و فرایندهای ذهنی می‌پردازد."
                        ),
                    },
                    {
                        "id": "q2",
                        "question": "کدام مورد نمونه‌ای از فرایند شناختی است؟",
                        "options": [
                            "حافظه",
                            "رشد استخوان",
                            "ضربان قلب",
                            "فشار خون",
                        ],
                        "correct_answer": "حافظه",
                        "explanation": (
                            "حافظه یکی از فرایندهای شناختی انسان است."
                        ),
                    },
                ],
            },
            {
                "id": "lesson_2",
                "title": "رفتار و فرایندهای ذهنی",
                "content": (
                    "رفتار شامل فعالیت‌ها و واکنش‌هایی است که می‌توان "
                    "آن‌ها را به شکل مستقیم یا غیرمستقیم بررسی کرد. "
                    "فرایندهای ذهنی مانند ادراک، حافظه، تفکر و تصمیم‌گیری "
                    "نیز بخش مهمی از مطالعه روانشناسی هستند."
                ),
                "special_points": [
                    "رفتار نتیجه تعامل عوامل زیستی، روانی و محیطی است.",
                    "فرایندهای ذهنی همیشه به صورت مستقیم قابل مشاهده نیستند.",
                    "برای مطالعه فرایندهای ذهنی از روش‌های علمی استفاده می‌شود.",
                ],
                "exam_points": [
                    "رفتار با فرایند ذهنی یکسان نیست.",
                    "عوامل محیطی می‌توانند بر رفتار اثر بگذارند.",
                ],
                "example": (
                    "اضطراب قبل از یک آزمون ممکن است باعث تغییر در "
                    "رفتار، تمرکز و تصمیم‌گیری فرد شود."
                ),
                "questions": [
                    {
                        "id": "q1",
                        "question": "کدام مورد یک فرایند ذهنی محسوب می‌شود؟",
                        "options": [
                            "تفکر",
                            "راه رفتن",
                            "نوشتن",
                            "دویدن",
                        ],
                        "correct_answer": "تفکر",
                        "explanation": (
                            "تفکر یک فرایند ذهنی و شناختی است."
                        ),
                    },
                    {
                        "id": "q2",
                        "question": "رفتار انسان معمولاً تحت تأثیر چه عواملی قرار دارد؟",
                        "options": [
                            "عوامل زیستی، روانی و محیطی",
                            "فقط عوامل اقتصادی",
                            "فقط عوامل ژنتیکی",
                            "فقط عوامل محیطی",
                        ],
                        "correct_answer": "عوامل زیستی، روانی و محیطی",
                        "explanation": (
                            "رفتار انسان حاصل تعامل عوامل مختلف زیستی، "
                            "روانی و محیطی است."
                        ),
                    },
                ],
            },
        ],
    },
    {
        "id": "chapter_2",
        "title": "روانشناسی رشد",
        "lessons": [
            {
                "id": "lesson_1",
                "title": "مفهوم رشد و تحول",
                "content": (
                    "روانشناسی رشد تغییرات جسمانی، شناختی، هیجانی و "
                    "اجتماعی انسان را در طول زندگی بررسی می‌کند."
                ),
                "special_points": [
                    "رشد فقط به تغییرات جسمانی محدود نمی‌شود.",
                    "تحول شناختی و اجتماعی نیز بخشی از رشد انسان است.",
                    "رشد در دوره‌های مختلف زندگی ویژگی‌های متفاوتی دارد.",
                ],
                "exam_points": [
                    "رشد را یک فرایند چندبعدی در نظر بگیرید.",
                    "ابعاد جسمانی، شناختی، هیجانی و اجتماعی را تفکیک کنید.",
                ],
                "example": (
                    "افزایش توانایی حل مسئله در دوران کودکی نمونه‌ای "
                    "از تحول شناختی است."
                ),
                "questions": [
                    {
                        "id": "q1",
                        "question": "کدام مورد یکی از ابعاد رشد انسان است؟",
                        "options": [
                            "رشد شناختی",
                            "فقط رشد مالی",
                            "فقط رشد شغلی",
                            "فقط رشد اقتصادی",
                        ],
                        "correct_answer": "رشد شناختی",
                        "explanation": (
                            "رشد شناختی یکی از ابعاد اصلی تحول انسان است."
                        ),
                    },
                    {
                        "id": "q2",
                        "question": "روانشناسی رشد چه چیزی را بررسی می‌کند؟",
                        "options": [
                            "تغییرات انسان در طول زندگی",
                            "فقط تغییرات مالی",
                            "فقط بیماری‌های جسمی",
                            "فقط عملکرد سازمان‌ها",
                        ],
                        "correct_answer": "تغییرات انسان در طول زندگی",
                        "explanation": (
                            "روانشناسی رشد تغییرات انسان را در ابعاد مختلف "
                            "و در طول زندگی بررسی می‌کند."
                        ),
                    },
                ],
            },
        ],
    },
    {
        "id": "chapter_3",
        "title": "مددکاری اجتماعی",
        "lessons": [
            {
                "id": "lesson_1",
                "title": "مفهوم مددکاری اجتماعی",
                "content": (
                    "مددکاری اجتماعی حرفه‌ای است که با هدف کمک به افراد، "
                    "گروه‌ها و جوامع برای بهبود عملکرد اجتماعی، حل مسائل "
                    "و افزایش دسترسی به منابع و حمایت‌های اجتماعی فعالیت می‌کند."
                ),
                "special_points": [
                    "مددکاری اجتماعی بر فرد و محیط اجتماعی او توجه دارد.",
                    "توانمندسازی یکی از مفاهیم مهم در مددکاری اجتماعی است.",
                    "مددکار باید اصول حرفه‌ای و اخلاقی را رعایت کند.",
                ],
                "exam_points": [
                    "مددکاری اجتماعی را صرفاً کمک مالی در نظر نگیرید.",
                    "توانمندسازی و حل مسئله از مفاهیم مهم این حوزه هستند.",
                ],
                "example": (
                    "کمک به یک خانواده برای شناسایی منابع حمایتی و "
                    "دسترسی به خدمات اجتماعی نمونه‌ای از مداخله مددکاری است."
                ),
                "questions": [
                    {
                        "id": "q1",
                        "question": "یکی از اهداف مهم مددکاری اجتماعی چیست؟",
                        "options": [
                            "توانمندسازی و بهبود عملکرد اجتماعی",
                            "جایگزینی کامل خانواده",
                            "تشخیص همه بیماری‌های جسمی",
                            "حذف کامل مشکلات اقتصادی جامعه",
                        ],
                        "correct_answer": "توانمندسازی و بهبود عملکرد اجتماعی",
                        "explanation": (
                            "توانمندسازی و بهبود عملکرد اجتماعی از اهداف مهم "
                            "مددکاری اجتماعی است."
                        ),
                    },
                    {
                        "id": "q2",
                        "question": "مددکاری اجتماعی بیشتر بر چه رویکردی تأکید دارد؟",
                        "options": [
                            "فرد و محیط اجتماعی",
                            "فقط درآمد فرد",
                            "فقط درمان بیماری جسمی",
                            "فقط مسائل سازمانی",
                        ],
                        "correct_answer": "فرد و محیط اجتماعی",
                        "explanation": (
                            "مددکاری اجتماعی رابطه فرد با محیط اجتماعی و "
                            "شرایط زندگی او را مورد توجه قرار می‌دهد."
                        ),
                    },
                ],
            },
        ],
    },
]


def get_chapters() -> list[dict[str, Any]]:
    """Return all Psychology chapters."""
    return list(PSYCHOLOGY_CURRICULUM)


def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return one chapter by ID."""

    for chapter in PSYCHOLOGY_CURRICULUM:
        if str(chapter.get("id")) == str(chapter_id):
            return chapter

    return None


def get_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return lessons for one chapter."""

    chapter = get_chapter(chapter_id)

    if chapter is None:
        return []

    lessons = chapter.get("lessons", [])

    if not isinstance(lessons, list):
        return []

    return lessons


def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return one lesson."""

    for lesson in get_lessons(chapter_id):
        if str(lesson.get("id")) == str(lesson_id):
            return lesson

    return None


def get_all_lessons() -> list[dict[str, Any]]:
    """Return all lessons with chapter metadata."""

    result: list[dict[str, Any]] = []

    for chapter in PSYCHOLOGY_CURRICULUM:
        chapter_id = chapter.get("id")
        chapter_title = chapter.get("title", "")

        lessons = chapter.get("lessons", [])

        if not isinstance(lessons, list):
            continue

        for lesson in lessons:
            if not isinstance(lesson, dict):
                continue

            item = dict(lesson)
            item["chapter_id"] = chapter_id
            item["chapter_title"] = chapter_title

            result.append(item)

    return result


def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return quiz questions for one lesson."""

    lesson = get_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:
        return []

    questions = lesson.get("questions", [])

    if not isinstance(questions, list):
        return []

    return [
        question
        for question in questions
        if isinstance(question, dict)
    ]


def get_curriculum_statistics() -> dict[str, int]:
    """Return basic curriculum statistics."""

    chapters = len(PSYCHOLOGY_CURRICULUM)
    lessons = 0
    questions = 0

    for chapter in PSYCHOLOGY_CURRICULUM:
        chapter_lessons = chapter.get("lessons", [])

        if not isinstance(chapter_lessons, list):
            continue

        lessons += len(chapter_lessons)

        for lesson in chapter_lessons:
            if not isinstance(lesson, dict):
                continue

            lesson_questions = lesson.get(
                "questions",
                [],
            )

            if isinstance(lesson_questions, list):
                questions += len(lesson_questions)

    return {
        "chapters": chapters,
        "lessons": lessons,
        "questions": questions,
    }


def data_health_check() -> bool:
    """Validate the Psychology curriculum structure."""

    try:
        if not MODULE_ID:
            return False

        if not MODULE_TITLE:
            return False

        if not isinstance(
            PSYCHOLOGY_CURRICULUM,
            list,
        ):
            return False

        for chapter in PSYCHOLOGY_CURRICULUM:
            if not isinstance(chapter, dict):
                return False

            if not chapter.get("id"):
                return False

            if not chapter.get("title"):
                return False

            lessons = chapter.get("lessons", [])

            if not isinstance(lessons, list):
                return False

            for lesson in lessons:
                if not isinstance(lesson, dict):
                    return False

                if not lesson.get("id"):
                    return False

                if not lesson.get("title"):
                    return False

                questions = lesson.get(
                    "questions",
                    [],
                )

                if not isinstance(questions, list):
                    return False

                for question in questions:
                    if not isinstance(question, dict):
                        return False

                    if not question.get("id"):
                        return False

                    if not question.get("question"):
                        return False

                    options = question.get(
                        "options",
                        [],
                    )

                    if not isinstance(options, list):
                        return False

                    if len(options) < 2:
                        return False

                    correct_answer = question.get(
                        "correct_answer"
                    )

                    if correct_answer not in options:
                        return False

        return True

    except Exception:
        return False
