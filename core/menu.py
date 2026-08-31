"""
Central menu router for Andishkadeh Management & Market.

Connected modules:
- Main Menu
- Management
- Management Quiz
- International Trade
- Psychology & Social Work
"""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from core.keyboards import main_menu_keyboard

from modules.management.handlers import (
    show_management_menu,
    show_management_chapter,
    show_management_lesson,
    start_management_quiz,
    answer_management_quiz,
    next_management_quiz_question,
    stop_management_quiz,
    cancel_management_quiz,
)

from modules.international_trade.handlers import (
    show_international_trade_menu,
    show_international_trade_chapters,
    show_international_trade_chapter,
    show_international_trade_lesson,
    complete_international_trade_lesson,
    start_international_trade_quiz,
    answer_international_trade_quiz,
    cancel_international_trade_quiz,
)

from modules.psychology.handlers import (
    show_psychology_menu,
    show_psychology_chapter,
    show_psychology_lesson,
    complete_psychology_lesson,
    start_psychology_quiz,
    answer_psychology_quiz,
    cancel_psychology_quiz,
)


logger = logging.getLogger(__name__)


# ==========================================================
# Main Menu
# ==========================================================

MAIN_MENU_TEXT = (
    "🏛️ <b>اندیشکده مدیریت و بازار</b>\n\n"
    "لطفاً بخش موردنظر خود را انتخاب کنید:"
)


async def show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show the main bot menu."""

    if update.message:
        await update.message.reply_text(
            MAIN_MENU_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        return

    if update.callback_query:
        query = update.callback_query

        try:
            await query.answer()
        except Exception:
            logger.exception(
                "Failed to answer main menu callback."
            )

        try:
            await query.edit_message_text(
                MAIN_MENU_TEXT,
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML",
            )
        except Exception:
            logger.exception(
                "Failed to edit main menu message."
            )


# ==========================================================
# Central Callback Router
# ==========================================================

async def route_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route callback queries to the correct module.
    """

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    logger.debug(
        "Central menu callback received: %s",
        data,
    )

    # ======================================================
    # Main Menu
    # ======================================================

    if data == "menu_main":
        await show_main_menu(
            update,
            context,
        )
        return

    # ======================================================
    # Management
    # ======================================================

    if data == "menu_management":
        await show_management_menu(
            update,
            context,
        )
        return

    if data.startswith(
        "management_chapter:"
    ):
        await show_management_chapter(
            update,
            context,
        )
        return

    if data.startswith(
        "management_lesson:"
    ):
        await show_management_lesson(
            update,
            context,
        )
        return

    # ======================================================
    # Management Quiz
    # ======================================================

    if data == "management_quiz_start":
        await start_management_quiz(
            update,
            context,
        )
        return

    if data.startswith(
        "management_quiz_answer:"
    ):
        await answer_management_quiz(
            update,
            context,
        )
        return

    if data == "management_quiz_next":
        await next_management_quiz_question(
            update,
            context,
        )
        return

    if data == "management_quiz_stop":
        await stop_management_quiz(
            update,
            context,
        )
        return

    if data == "management_quiz_cancel":
        await cancel_management_quiz(
            update,
            context,
        )
        return

    # ======================================================
    # International Trade
    # ======================================================

    if data in {
        "menu_international_trade",
        "menu_trade",
    }:
        await show_international_trade_menu(
            update,
            context,
        )
        return

    if data == "trade_chapters":
        await show_international_trade_chapters(
            update,
            context,
        )
        return

    if data.startswith(
        "trade_chapter:"
    ):
        await show_international_trade_chapter(
            update,
            context,
        )
        return

    if data.startswith(
        "trade_lesson:"
    ):
        await show_international_trade_lesson(
            update,
            context,
        )
        return

    if data.startswith(
        "trade_complete:"
    ):
        await complete_international_trade_lesson(
            update,
            context,
        )
        return

    if data.startswith(
        "trade_quiz:"
    ):
        await start_international_trade_quiz(
            update,
            context,
        )
        return

    if data.startswith(
        "trade_quiz_answer:"
    ):
        await answer_international_trade_quiz(
            update,
            context,
        )
        return

    if data.startswith(
        "trade_quiz_cancel:"
    ):
        await cancel_international_trade_quiz(
            update,
            context,
        )
        return

    # ======================================================
    # Psychology & Social Work
    # ======================================================

    if data == "menu_psychology":
        await show_psychology_menu(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_chapter:"
    ):
        await show_psychology_chapter(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_lesson:"
    ):
        await show_psychology_lesson(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_complete:"
    ):
        await complete_psychology_lesson(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_quiz:"
    ):
        await start_psychology_quiz(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_quiz_answer:"
    ):
        await answer_psychology_quiz(
            update,
            context,
        )
        return

    if data == "psychology_quiz_cancel":
        await cancel_psychology_quiz(
            update,
            context,
        )
        return

    # ======================================================
    # Fallback
    # ======================================================

    try:
        await query.answer(
            "این بخش هنوز فعال نشده است.",
            show_alert=False,
        )
    except Exception:
        logger.exception(
            "Failed to answer unknown callback: %s",
            data,
        )


# ==========================================================
# Health Check
# ==========================================================

def menu_health_check() -> bool:
    """Basic central menu health check."""

    try:
        required_functions = (
            main_menu_keyboard,
            show_management_menu,
            show_management_chapter,
            show_management_lesson,
            start_management_quiz,
            answer_management_quiz,
            next_management_quiz_question,
            stop_management_quiz,
            cancel_management_quiz,
            show_international_trade_menu,
            show_international_trade_chapters,
            show_international_trade_chapter,
            show_international_trade_lesson,
            complete_international_trade_lesson,
            start_international_trade_quiz,
            answer_international_trade_quiz,
            cancel_international_trade_quiz,
            show_psychology_menu,
            show_psychology_chapter,
            show_psychology_lesson,
            complete_psychology_lesson,
            start_psychology_quiz,
            answer_psychology_quiz,
            cancel_psychology_quiz,
            route_menu_callback,
        )

        return all(
            callable(function)
            for function in required_functions
        )

    except Exception:
        logger.exception(
            "Central menu health check failed."
        )
        return False


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MAIN_MENU_TEXT",
    "show_main_menu",
    "route_menu_callback",
    "menu_health_check",
]
