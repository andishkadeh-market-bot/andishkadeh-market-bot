"""
Finance Module
Andishkadeh Management & Market

ماژول مدیریت مالی

معماری:

Telegram Handler
        ↓
Service Layer
        ↓
Data / Content
        ↓
Database

مسئولیت این فایل:
- تعریف API عمومی ماژول Finance
- ارائه Service Layer به سایر بخش‌های پروژه
- حفظ Compatibility با نسخه‌های قبلی
- جلوگیری از وابستگی مستقیم سایر بخش‌ها به data.py
"""

from .service import (
    # --------------------------------------------------------
    # Module
    # --------------------------------------------------------
    get_module_title,
    get_module_description,
    get_module_info,

    # --------------------------------------------------------
    # Chapters
    # --------------------------------------------------------
    get_finance_chapters,
    get_finance_chapter,

    # --------------------------------------------------------
    # Lessons
    # --------------------------------------------------------
    get_finance_lessons,
    get_finance_lesson,

    # --------------------------------------------------------
    # Educational Content
    # --------------------------------------------------------
    get_complete_lesson,
    get_lesson_content,
    get_specialized_tips,
    get_exam_tips,
    get_examples,
    get_keywords,

    # --------------------------------------------------------
    # Quiz
    # --------------------------------------------------------
    get_finance_quiz,
    get_finance_chapter_quiz,
    get_all_quiz_questions,
    get_quiz_question,

    # --------------------------------------------------------
    # Quiz Result
    # --------------------------------------------------------
    calculate_quiz_score,
    calculate_quiz_result,
    validate_quiz_answer,

    # --------------------------------------------------------
    # Quiz Attempt
    # --------------------------------------------------------
    start_quiz_attempt,
    save_quiz_attempt,
    complete_quiz_attempt,

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------
    get_total_lesson_count,
    get_total_quiz_count,
    get_curriculum_stats,
    get_finance_statistics,
    get_curriculum_statistics,

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------
    search_content,

    # --------------------------------------------------------
    # Validation / Health
    # --------------------------------------------------------
    validate_curriculum,
    finance_health_check,
)


# ============================================================
# Module Constants
# ============================================================

MODULE_ID = "finance"

MODULE_TITLE = get_module_title()

MODULE_DESCRIPTION = get_module_description()


# ============================================================
# Compatibility API
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
    # --------------------------------------------------------
    # Constants
    # --------------------------------------------------------
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",

    # --------------------------------------------------------
    # Module
    # --------------------------------------------------------
    "get_module_title",
    "get_module_description",
    "get_module_info",

    # --------------------------------------------------------
    # Chapters
    # --------------------------------------------------------
    "get_finance_chapters",
    "get_finance_chapter",

    # Compatibility
    "get_chapters",
    "get_chapter",

    # --------------------------------------------------------
    # Lessons
    # --------------------------------------------------------
    "get_finance_lessons",
    "get_finance_lesson",

    # Compatibility
    "get_lessons",
    "get_lesson",

    # --------------------------------------------------------
    # Educational Content
    # --------------------------------------------------------
    "get_complete_lesson",
    "get_lesson_content",
    "get_specialized_tips",
    "get_exam_tips",
    "get_examples",
    "get_keywords",

    # --------------------------------------------------------
    # Quiz
    # --------------------------------------------------------
    "get_finance_quiz",
    "get_finance_chapter_quiz",
    "get_all_quiz_questions",
    "get_quiz_question",

    # Compatibility
    "get_quiz",
    "get_all_questions",
    "get_chapter_quiz",

    # --------------------------------------------------------
    # Quiz Result
    # --------------------------------------------------------
    "calculate_quiz_score",
    "calculate_quiz_result",
    "validate_quiz_answer",

    # --------------------------------------------------------
    # Quiz Attempt
    # --------------------------------------------------------
    "start_quiz_attempt",
    "save_quiz_attempt",
    "complete_quiz_attempt",

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------
    "get_total_lesson_count",
    "get_total_quiz_count",
    "get_curriculum_stats",
    "get_finance_statistics",
    "get_curriculum_statistics",

    # Compatibility
    "get_statistics",

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------
    "search_content",

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------
    "validate_curriculum",

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------
    "finance_health_check",

    # Compatibility
    "health_check",
]
