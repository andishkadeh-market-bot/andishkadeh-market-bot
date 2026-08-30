"""
Shared utility functions for Andishkadeh Management & Market.
"""

from typing import Optional

from telegram import Update


def get_user_id(update: Update) -> Optional[int]:
    """Return the Telegram user ID from an update."""

    user = update.effective_user

    if user is None:
        return None

    return user.id


def get_user_name(update: Update) -> str:
    """Return the user's first name or a safe fallback."""

    user = update.effective_user

    if user is None:
        return "کاربر"

    return user.first_name or "کاربر"


def get_username(update: Update) -> Optional[str]:
    """Return the Telegram username."""

    user = update.effective_user

    if user is None:
        return None

    return user.username


def safe_text(
    value: Optional[str],
    default: str = "",
) -> str:
    """Return text safely, using a default when empty."""

    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


def build_section_text(
    title: str,
    description: str,
) -> str:
    """Build a consistent section header."""

    return (
        f"<b>{title}</b>\n\n"
        f"{description}"
    )
