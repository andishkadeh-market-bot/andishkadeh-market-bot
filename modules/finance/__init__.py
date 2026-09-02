"""
Finance module for Andishkadeh Management & Market.

This package provides educational content for:
- Financial management
- Financial planning
- Budgeting
- Cash management
- Investment decisions
- Financial analysis
- Risk management
- Working capital
- Capital budgeting
- Financial decision-making
"""

from .data import (
    MODULE_ID,
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    get_module_info,
    get_chapters,
    get_lessons,
    get_curriculum_statistics,
    data_health_check,
)

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "get_module_info",
    "get_chapters",
    "get_lessons",
    "get_curriculum_statistics",
    "data_health_check",
]
