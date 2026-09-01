"""
Management education module.
Andishkadeh Management & Market

Compatibility layer for the Management module.

This file ensures that legacy imports used by handlers
remain compatible with the current data architecture.
"""

from __future__ import annotations

# Load the actual curriculum data first.
from . import data as _data


# ==========================================================
# Compatibility Constants
# ==========================================================

# Current data.py uses CHAPTERS as the canonical curriculum.
# Older handlers may import MANAGEMENT_CHAPTERS.
#
# Keep both names pointing to the same curriculum source.
MANAGEMENT_CHAPTERS = getattr(
    _data,
    "CHAPTERS",
    [],
)


# ==========================================================
# Public Module Metadata
# ==========================================================

MODULE_KEY = getattr(
    _data,
    "MODULE_KEY",
    "management",
)

MODULE_TITLE = getattr(
    _data,
    "MODULE_TITLE",
    "📚 آموزش مدیریت",
)

MODULE_DESCRIPTION = getattr(
    _data,
    "MODULE_DESCRIPTION",
    "",
)


# ==========================================================
# Compatibility Accessors
# ==========================================================

get_management_chapters = getattr(
    _data,
    "get_management_chapters",
    lambda: MANAGEMENT_CHAPTERS,
)

get_management_chapter = getattr(
    _data,
    "get_management_chapter",
    lambda chapter_id: None,
)

get_management_lessons = getattr(
    _data,
    "get_management_lessons",
    lambda chapter_id: [],
)

get_management_lesson = getattr(
    _data,
    "get_management_lesson",
    lambda chapter_id, lesson_id: None,
)

get_management_quiz = getattr(
    _data,
    "get_management_quiz",
    lambda chapter_id, lesson_id: [],
)

get_all_quiz_questions = getattr(
    _data,
    "get_all_quiz_questions",
    lambda: [],
)


# ==========================================================
# Health Check
# ==========================================================

def management_module_health_check() -> bool:
    """
    Validate that the Management module curriculum
    can be loaded successfully.
    """

    try:
        return isinstance(
            MANAGEMENT_CHAPTERS,
            list,
        )

    except Exception:
        return False


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MODULE_KEY",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "MANAGEMENT_CHAPTERS",
    "get_management_chapters",
    "get_management_chapter",
    "get_management_lessons",
    "get_management_lesson",
    "get_management_quiz",
    "get_all_quiz_questions",
    "management_module_health_check",
]
