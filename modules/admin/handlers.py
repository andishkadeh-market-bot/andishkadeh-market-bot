"""
Admin handlers for Andishkadeh Management & Market.

Provides:
- /admin command
- Admin menu
- Callback routing
- Compatibility aliases
- Safe health check
"""

from __future__ import annotations

import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = "admin"
MODULE_TITLE = "مدیریت ربات"


# ==========================================================
# Keyboard
# ==========================================================

def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Return the Admin menu keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="menu_main",
                )
            ]
        ]
    )


# ==========================================================
# Admin Command
# ==========================================================

async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle the /admin command.

    This is intentionally safe and lightweight.
    Advanced admin features can be added later.
    """

    user = update.effective_user

    logger.info(
        "Admin command requested by user: %s",
        user.id if user else "unknown",
    )

    text = (
        "⚙️ <b>مدیریت ربات</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "پنل مدیریت ربات فعال است.\n\n"
        "امکانات مدیریتی پیشرفته در نسخه‌های "
        "بعدی قابل توسعه هستند."
    )

    if update.message is not None:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=admin_menu_keyboard(),
        )
        return

    query = update.callback_query

    if query is not None:
        await query.answer()

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=admin_menu_keyboard(),
        )


# ==========================================================
# Admin Menu
# ==========================================================

async def show_admin_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show Admin menu."""

    query = update.callback_query

    if query is not None:
        await query.answer()

        text = (
            "⚙️ <b>مدیریت ربات</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "پنل مدیریت ربات فعال است."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=admin_menu_keyboard(),
        )

        return

    if update.message is not None:
        await admin_command(
            update,
            context,
        )


# ==========================================================
# Callback Router
# ==========================================================

async def route_admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route Admin callbacks."""

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if data == "menu_admin":
        await show_admin_menu(
            update,
            context,
        )
        return

    if data == "admin_menu":
        await show_admin_menu(
            update,
            context,
        )
        return


# ==========================================================
# Health Check
# ==========================================================

def admin_handlers_health_check() -> bool:
    """Return Admin handler health status."""

    try:
        return bool(
            MODULE_ID
            and MODULE_TITLE
            and callable(admin_command)
            and callable(show_admin_menu)
        )
    except Exception:
        return False


# ==========================================================
# Compatibility Aliases
# ==========================================================

show_admin = show_admin_menu

admin_menu = show_admin_menu


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "admin_menu_keyboard",
    "admin_command",
    "show_admin_menu",
    "show_admin",
    "admin_menu",
    "route_admin_callback",
    "admin_handlers_health_check",
]
