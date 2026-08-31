"""
Admin handlers for Andishkadeh Management & Market.

This module provides a safe administrative handler layer.
It is intentionally lightweight so the main bot can start
even when no advanced admin features are configured yet.
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
    """Return the basic Admin keyboard."""

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
# Admin Menu
# ==========================================================

async def show_admin_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show the basic Admin menu."""

    query = update.callback_query

    if query is not None:
        await query.answer()

    text = (
        "⚙️ <b>مدیریت ربات</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "بخش مدیریت ربات فعال است.\n\n"
        "امکانات مدیریتی پیشرفته می‌توانند "
        "در نسخه‌های بعدی به این بخش اضافه شوند."
    )

    if query is not None:
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=admin_menu_keyboard(),
        )
        return

    if update.message is not None:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=admin_menu_keyboard(),
        )


# ==========================================================
# Callback Router
# ==========================================================

async def route_admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route Admin callbacks safely."""

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


# ==========================================================
# Health Check
# ==========================================================

def admin_handlers_health_check() -> bool:
    """Return Admin handler health status."""

    try:
        return bool(
            MODULE_ID
            and MODULE_TITLE
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
    "show_admin_menu",
    "show_admin",
    "admin_menu",
    "route_admin_callback",
    "admin_handlers_health_check",
]
