"""
Central menu router for Andishkadeh Management & Market.
Connected modules:
- Main Menu
- Management
- Management Quiz
- International Trade
"""
from __future__ import annotations
import logging
from telegram import Update
from telegram.ext import ContextTypes
from core.keyboards import (
    main_menu_keyboard,
)
from modules.management.handlers import (
    show_management_menu,
    show_management_chapter,
    show_management_lesson,
    start_management_quiz,
    answer_management_quiz,
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
# ==========================================================
# Logging
# ==========================================================
logger = logging.getLogger(__name__)
# ==========================================================
# Main Menu Text
# ==========================================================
MAIN_MENU_TEXT = (
    "🏛️ <b>اندیشکده مدیریت و بازار</b>\n\n"
    "لطفاً بخش موردنظر خود را انتخاب کنید:"
)
# ==========================================================
# Main Menu
# ==========================================================
async def show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show the main bot menu.
    Supports:
    - Telegram messages
    - Callback queries
    """
    # ------------------------------------------------------
    # Message
    # ------------------------------------------------------
    if update.message:
        await update.message.reply_text(
            MAIN_MENU_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        return
    # ------------------------------------------------------
    # Callback Query
    # ------------------------------------------------------
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
                "Failed to edit message for main menu."
            )
# ==========================================================
# Central Menu Router
# ==========================================================
async def route_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route callback queries to the correct module.
    Callback priority:
    1. Main Menu
    2. Management
    3. Management Quiz
    4. International Trade
    5. Fallback
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
    if data.startswith(
        "management_quiz:"
    ):
        await start_management_quiz(
            update,
            context,
        )
        return
    if data.startswith(
        "quiz_answer:"
    ):
        await answer_management_quiz(
            update,
            context,
        )
        return
    if data == "quiz_cancel":
        await cancel_management_quiz(
            update,
            context,
        )
        return
    # ======================================================
    # International Trade
    # ======================================================
    if data == "menu_international_trade":
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
    # ======================================================
    # International Trade Quiz
    # ======================================================
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
    # Unknown Callback
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
    """
    Basic health check for the central menu system.
    Returns:
        True when the menu system is correctly configured.
    """
    try:
        if not MAIN_MENU_TEXT:
            return False
        if main_menu_keyboard is None:
            return False
        if show_management_menu is None:
            return False
        if show_international_trade_menu is None:
            return False
        if route_menu_callback is None:
            return False
        return True
    except Exception:
        logger.exception(
            "Central menu health check failed."
        )
        return False
