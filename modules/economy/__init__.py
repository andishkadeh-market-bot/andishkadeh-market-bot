"""
Economy & Market Module
Andishkadeh Management & Market

Professional economics education module.

Layers:
- data.py     -> curriculum and educational data
- service.py  -> business logic and data access
- handlers.py -> Telegram presentation and quiz interaction
"""

from .data import (
    MODULE_ID,
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    get_chapters,
    get_chapter,
    get_lessons,
    get_lesson,
    get_quiz_questions,
)

from .service import (
    get_module_id,
    get_module_title,
    get_module_info,
    get_economy_chapters,
    get_economy_chapter,
    get_economy_lessons,
    get_economy_lesson,
    get_economy_quiz,
    get_all_quiz_questions,
    get_curriculum_stats,
    validate_module,
    service_health_check,
)

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "get_chapters",
    "get_chapter",
    "get_lessons",
    "get_lesson",
    "get_quiz_questions",
    "get_module_id",
    "get_module_title",
    "get_module_info",
    "get_economy_chapters",
    "get_economy_chapter",
    "get_economy_lessons",
    "get_economy_lesson",
    "get_economy_quiz",
    "get_all_quiz_questions",
    "get_curriculum_stats",
    "validate_module",
    "service_health_check",
]
