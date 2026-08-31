"""
Data definitions for Random Quiz module.
"""

from __future__ import annotations

from typing import Any


RANDOM_QUIZ_CONFIG: dict[str, Any] = {
    "module_id": "random_quiz",
    "title": "🎲 سوالات تصادفی",
    "description": (
        "آزمون تصادفی از میان سوالات ثبت‌شده اندیشکده"
    ),
    "default_question_count": 10,
    "minimum_question_count": 1,
    "maximum_question_count": 20,
}


def get_random_quiz_config() -> dict[str, Any]:
    """Return a copy of the Random Quiz configuration."""

    return dict(RANDOM_QUIZ_CONFIG)
