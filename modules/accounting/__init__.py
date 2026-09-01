"""
Accounting Module
Andishkadeh Management & Market

حسابداری تخصصی و حرفه‌ای
"""

from .service import (
    get_module_title,
    get_module_info,
    get_accounting_chapters,
    get_accounting_chapter,
    get_accounting_lessons,
    get_accounting_lesson,
    get_accounting_quiz,
    get_all_quiz_questions,
    get_curriculum_stats,
)

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
]
