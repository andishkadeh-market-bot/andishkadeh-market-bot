"""
Shared utility functions for Andishkadeh Management & Market.
"""

from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes


TELEGRAM_MESSAGE_LIMIT = 4096


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


def split_long_text(
    text: str,
    limit: int = TELEGRAM_MESSAGE_LIMIT,
) -> list[str]:
    """
    Split long text into Telegram-safe chunks.

    The function tries to split at paragraph or newline
    boundaries before falling back to a hard split.
    """

    if not text:
        return []

    if limit <= 0:
        raise ValueError(
            "Message limit must be greater than zero."
        )

    if len(text) <= limit:
        return [text]

    chunks = []
    remaining = text

    while len(remaining) > limit:
        split_at = remaining.rfind(
            "\n\n",
            0,
            limit,
        )

        if split_at <= 0:
            split_at = remaining.rfind(
                "\n",
                0,
                limit,
            )

        if split_at <= 0:
            split_at = remaining.rfind(
                " ",
                0,
                limit,
            )

        if split_at <= 0:
            split_at = limit

        chunk = remaining[:split_at].strip()

        if chunk:
            chunks.append(chunk)

        remaining = remaining[split_at:].strip()

    if remaining:
        chunks.append(remaining)

    return chunks


async def send_long_text(
    update: Update,
    text: str,
    reply_markup=None,
    parse_mode: Optional[str] = None,
) -> None:
    """
    Send a long text safely within Telegram's message limit.

    Reply markup is attached only to the final message.
    """

    chunks = split_long_text(text)

    if not chunks:
        return

    if update.message:
        for index, chunk in enumerate(chunks):
            markup = (
                reply_markup
                if index == len(chunks) - 1
                else None
            )

            await update.message.reply_text(
                chunk,
                reply_markup=markup,
                parse_mode=parse_mode,
            )

        return

    if update.callback_query:
        query = update.callback_query

        for index, chunk in enumerate(chunks):
            markup = (
                reply_markup
                if index == len(chunks) - 1
                else None
            )

            if index == 0:
                await query.edit_message_text(
                    chunk,
                    reply_markup=markup,
                    parse_mode=parse_mode,
                )
            else:
                await query.message.reply_text(
                    chunk,
                    reply_markup=markup,
                    parse_mode=parse_mode,
                )
