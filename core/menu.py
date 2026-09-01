"""
Central Menu Router
Andishkadeh Management & Market
Connected modules:
- Main Menu
- Management
- International Trade
- Marketing & Sales
- Economy & Market
- Accounting
- Psychology & Social Work
Architecture:
    bot.py
        ↓
    core.menu
        ↓
    modules.<module>.handlers
Design goals:
- Safe module loading
- Central callback routing
- Back navigation
- Compatibility aliases
- Optional module protection
- No module-specific business logic here
- Preserve Render / existing bot architecture
"""
from __future__ import annotations
import importlib
import logging
from typing import Any, Callable
from telegram import Update
from telegram.ext import ContextTypes
from core.keyboards import main_menu_keyboard
logger = logging.getLogger(__name__)
# ==========================================================
# Main Menu
# ==========================================================
MAIN_MENU_TEXT = (
    "🏛️ <b>اندیشکده مدیریت و بازار</b>\n\n"
    "مرکز آموزش تخصصی مدیریت، اقتصاد، تجارت، "
    "بازاریابی، حسابداری و توسعه حرفه‌ای.\n\n"
    "📚 لطفاً بخش موردنظر خود را انتخاب کنید:"
)
# ==========================================================
# Safe Module Loader
# ==========================================================
def _load_module(module_path: str) -> Any | None:
    """
    Safely import an optional module.
    If a module has a problem, the whole bot should not crash.
    """
    try:
        return importlib.import_module(module_path)
    except Exception:
        logger.exception(
            "Unable to load module: %s",
            module_path,
        )
        return None
def _get_function(
    module: Any | None,
    *names: str,
) -> Callable[..., Any] | None:
    """
    Return the first callable function found.
    """
    if module is None:
        return None
    for name in names:
        function = getattr(
            module,
            name,
            None,
        )
        if callable(function):
            return function
    return None
async def _call_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    module_path: str,
    function_names: tuple[str, ...],
) -> bool:
    """
    Safely execute a module handler.
    """
    module = _load_module(
        module_path
    )
    function = _get_function(
        module,
        *function_names,
    )
    if function is None:
        logger.warning(
            "No compatible handler found in %s: %s",
            module_path,
            function_names,
        )
        return False
    try:
        await function(
            update,
            context,
        )
        return True
    except TypeError:
        logger.exception(
            "Handler signature mismatch: %s.%s",
            module_path,
            getattr(
                function,
                "__name__",
                "unknown",
            ),
        )
        return False
    except Exception:
        logger.exception(
            "Handler execution failed: %s.%s",
            module_path,
            getattr(
                function,
                "__name__",
                "unknown",
            ),
        )
        return False
# ==========================================================
# Callback Answer
# ==========================================================
async def _answer_callback(
    update: Update,
) -> None:
    """
    Safely close Telegram callback loading state.
    """
    query = update.callback_query
    if query is None:
        return
    try:
        await query.answer()
    except Exception:
        logger.exception(
            "Failed to answer callback query."
        )
# ==========================================================
# Main Menu
# ==========================================================
async def show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Display central main menu.
    """
    query = update.callback_query
    if query is not None:
        await _answer_callback(
            update
        )
        try:
            await query.edit_message_text(
                text=MAIN_MENU_TEXT,
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML",
            )
            return
        except Exception:
            logger.exception(
                "Unable to edit main menu message."
            )
    message = update.effective_message
    if message is not None:
        try:
            await message.reply_text(
                text=MAIN_MENU_TEXT,
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML",
            )
        except Exception:
            logger.exception(
                "Unable to send main menu."
            )
# ==========================================================
# Management
# ==========================================================
async def _route_management(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    module_path = (
        "modules.management.handlers"
    )
    if data == "menu_management":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_management_menu",
                "show_management",
            ),
        )
    if data.startswith(
        "management_chapter:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_management_chapter",
                "show_management_chapter_menu",
            ),
        )
    if data.startswith(
        "management_lesson:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_management_lesson",
                "show_management_lesson_content",
            ),
        )
    if data in {
        "management_quiz_start",
        "management_quiz_all",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_management_quiz",
                "start_management_quiz_all",
            ),
        )
    if data.startswith(
        "management_quiz_answer:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "answer_management_quiz",
                "handle_management_quiz_answer",
            ),
        )
    if data == "management_quiz_next":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "next_management_quiz_question",
                "_show_next_quiz_question",
            ),
        )
    if data == "management_quiz_stop":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "stop_management_quiz",
                "finish_management_quiz",
                "cancel_management_quiz",
            ),
        )
    if data == "management_quiz_cancel":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "cancel_management_quiz",
                "stop_management_quiz",
            ),
        )
    return False
# ==========================================================
# International Trade
# ==========================================================
async def _route_international_trade(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    module_path = (
        "modules.international_trade.handlers"
    )
    if data in {
        "menu_international_trade",
        "menu_trade",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_international_trade_menu",
                "show_trade_menu",
                "show_international_trade",
            ),
        )
    if data == "trade_chapters":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_international_trade_chapters",
                "show_trade_chapters",
            ),
        )
    if data.startswith(
        "trade_chapter:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_international_trade_chapter",
                "show_trade_chapter",
            ),
        )
    if data.startswith(
        "trade_lesson:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_international_trade_lesson",
                "show_trade_lesson",
            ),
        )
    if data.startswith(
        "trade_complete:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "complete_international_trade_lesson",
                "complete_trade_lesson",
            ),
        )
    if data.startswith(
        "trade_quiz:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_international_trade_quiz",
                "start_trade_quiz",
            ),
        )
    if data.startswith(
        "trade_quiz_answer:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "answer_international_trade_quiz",
                "answer_trade_quiz",
            ),
        )
    if data.startswith(
        "trade_quiz_cancel:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "cancel_international_trade_quiz",
                "cancel_trade_quiz",
            ),
        )
    return False
# ==========================================================
# Marketing & Sales
# ==========================================================
async def _route_marketing(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    module_path = (
        "modules.marketing.handlers"
    )
    # Main menu
    if data == "menu_marketing":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_marketing_menu",
                "show_marketing",
            ),
        )
    # Chapter
    if data.startswith(
        "marketing_chapter:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_marketing_chapter",
                "show_marketing_chapter_menu",
                "show_marketing_chapter_lessons",
            ),
        )
    # Lesson
    if data.startswith(
        "marketing_lesson:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_marketing_lesson",
                "show_marketing_lesson_content",
            ),
        )
    # Lesson quiz
    if data.startswith(
        "marketing_quiz_lesson:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_marketing_quiz",
                "start_marketing_quiz_lesson",
            ),
        )
    # Chapter quiz
    if data.startswith(
        "marketing_quiz_chapter:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_marketing_chapter_quiz",
            ),
        )
    # Comprehensive quiz
    if data == "marketing_quiz_all":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_marketing_quiz_all",
                "start_marketing_quiz",
            ),
        )
    # Quiz answer
    if data.startswith(
        "marketing_quiz_answer:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "answer_marketing_quiz",
                "handle_marketing_quiz_answer",
            ),
        )
    # Statistics
    if data == "marketing_statistics":
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_marketing_statistics",
            ),
        )
    return False
# ==========================================================
# Economy & Market
# ==========================================================
async def _route_economy(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    module_path = (
        "modules.economy.handlers"
    )
    # ------------------------------------------------------
    # Main economy menu
    # ------------------------------------------------------
    if data in {
        "menu_economics",
        "menu_economy",
        "menu_market",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_economy_menu",
                "show_economy",
                "show_market_menu",
            ),
        )
    # ------------------------------------------------------
    # Chapters
    # ------------------------------------------------------
    if data in {
        "economy_chapters",
        "market_chapters",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_economy_chapters",
                "show_market_chapters",
            ),
        )
    # ------------------------------------------------------
    # Chapter
    # ------------------------------------------------------
    if (
        data.startswith(
            "economy_chapter:"
        )
        or data.startswith(
            "market_chapter:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_economy_chapter",
                "show_market_chapter",
                "show_economy_chapter_menu",
            ),
        )
    # ------------------------------------------------------
    # Lesson
    # ------------------------------------------------------
    if (
        data.startswith(
            "economy_lesson:"
        )
        or data.startswith(
            "market_lesson:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_economy_lesson",
                "show_market_lesson",
                "show_economy_lesson_content",
            ),
        )
    # ------------------------------------------------------
    # Complete lesson
    # ------------------------------------------------------
    if (
        data.startswith(
            "economy_complete:"
        )
        or data.startswith(
            "market_complete:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "complete_economy_lesson",
                "complete_market_lesson",
            ),
        )
    # ------------------------------------------------------
    # Lesson quiz
    # ------------------------------------------------------
    if (
        data.startswith(
            "economy_quiz_lesson:"
        )
        or data.startswith(
            "market_quiz_lesson:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_economy_quiz",
                "start_economy_quiz_lesson",
                "start_market_quiz",
            ),
        )
    # ------------------------------------------------------
    # Chapter quiz
    # ------------------------------------------------------
    if (
        data.startswith(
            "economy_quiz_chapter:"
        )
        or data.startswith(
            "market_quiz_chapter:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_economy_chapter_quiz",
                "start_market_chapter_quiz",
            ),
        )
    # ------------------------------------------------------
    # Comprehensive quiz
    # ------------------------------------------------------
    if data in {
        "economy_quiz_all",
        "market_quiz_all",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_economy_quiz_all",
                "start_economy_quiz",
                "start_market_quiz",
            ),
        )
    # ------------------------------------------------------
    # Quiz answer
    # ------------------------------------------------------
    if (
        data.startswith(
            "economy_quiz_answer:"
        )
        or data.startswith(
            "market_quiz_answer:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "answer_economy_quiz",
                "answer_market_quiz",
                "handle_economy_quiz_answer",
            ),
        )
    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------
    if data in {
        "economy_statistics",
        "market_statistics",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_economy_statistics",
                "show_market_statistics",
            ),
        )
    return False
# ==========================================================
# Accounting
# ==========================================================
async def _route_accounting(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """
    Central routing for Accounting module.
    Expected module:
        modules/accounting/handlers.py
    The router supports both the primary callback naming
    convention and compatibility aliases.
    """
    module_path = (
        "modules.accounting.handlers"
    )
    # ------------------------------------------------------
    # Main accounting menu
    # ------------------------------------------------------
    if data in {
        "menu_accounting",
        "menu_account",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_accounting_menu",
                "show_accounting",
                "show_accounting_main_menu",
            ),
        )
    # ------------------------------------------------------
    # Accounting chapters
    # ------------------------------------------------------
    if data in {
        "accounting_chapters",
        "account_chapters",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_accounting_chapters",
                "show_account_chapters",
            ),
        )
    # ------------------------------------------------------
    # Accounting chapter
    # ------------------------------------------------------
    if (
        data.startswith(
            "accounting_chapter:"
        )
        or data.startswith(
            "account_chapter:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_accounting_chapter",
                "show_account_chapter",
                "show_accounting_chapter_menu",
            ),
        )
    # ------------------------------------------------------
    # Accounting lesson
    # ------------------------------------------------------
    if (
        data.startswith(
            "accounting_lesson:"
        )
        or data.startswith(
            "account_lesson:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_accounting_lesson",
                "show_account_lesson",
                "show_accounting_lesson_content",
            ),
        )
    # ------------------------------------------------------
    # Complete accounting lesson
    # ------------------------------------------------------
    if (
        data.startswith(
            "accounting_complete:"
        )
        or data.startswith(
            "account_complete:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "complete_accounting_lesson",
                "complete_account_lesson",
                "complete_accounting",
            ),
        )
    # ------------------------------------------------------
    # Accounting lesson quiz
    # ------------------------------------------------------
    if (
        data.startswith(
            "accounting_quiz_lesson:"
        )
        or data.startswith(
            "account_quiz_lesson:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_accounting_quiz",
                "start_accounting_quiz_lesson",
                "start_account_quiz",
            ),
        )
    # ------------------------------------------------------
    # Accounting chapter quiz
    # ------------------------------------------------------
    if (
        data.startswith(
            "accounting_quiz_chapter:"
        )
        or data.startswith(
            "account_quiz_chapter:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_accounting_chapter_quiz",
                "start_account_chapter_quiz",
            ),
        )
    # ------------------------------------------------------
    # Comprehensive accounting quiz
    # ------------------------------------------------------
    if data in {
        "accounting_quiz_all",
        "account_quiz_all",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_accounting_quiz_all",
                "start_accounting_quiz",
                "start_account_quiz",
            ),
        )
    # ------------------------------------------------------
    # Accounting quiz answer
    # ------------------------------------------------------
    if (
        data.startswith(
            "accounting_quiz_answer:"
        )
        or data.startswith(
            "account_quiz_answer:"
        )
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "answer_accounting_quiz",
                "answer_account_quiz",
                "handle_accounting_quiz_answer",
            ),
        )
    # ------------------------------------------------------
    # Accounting quiz next
    # ------------------------------------------------------
    if data in {
        "accounting_quiz_next",
        "account_quiz_next",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "next_accounting_quiz_question",
                "_show_next_quiz_question",
                "show_next_accounting_quiz_question",
            ),
        )
    # ------------------------------------------------------
    # Accounting quiz stop
    # ------------------------------------------------------
    if data in {
        "accounting_quiz_stop",
        "account_quiz_stop",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "stop_accounting_quiz",
                "finish_accounting_quiz",
                "cancel_accounting_quiz",
            ),
        )
    # ------------------------------------------------------
    # Accounting quiz cancel
    # ------------------------------------------------------
    if data in {
        "accounting_quiz_cancel",
        "account_quiz_cancel",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "cancel_accounting_quiz",
                "stop_accounting_quiz",
            ),
        )
    # ------------------------------------------------------
    # Accounting statistics
    # ------------------------------------------------------
    if data in {
        "accounting_statistics",
        "account_statistics",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_accounting_statistics",
                "show_account_statistics",
            ),
        )
    return False
# ==========================================================
# Psychology & Social Work
# ==========================================================
async def _route_psychology(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    module_path = (
        "modules.psychology.handlers"
    )
    # ------------------------------------------------------
    # Main menu
    # ------------------------------------------------------
    if data in {
        "menu_psychology",
        "menu_social_work",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_psychology_menu",
                "show_psychology",
            ),
        )
    # ------------------------------------------------------
    # Chapter
    # ------------------------------------------------------
    if data.startswith(
        "psychology_chapter:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_psychology_chapter",
                "show_psychology_chapter_menu",
            ),
        )
    # ------------------------------------------------------
    # Lesson
    # ------------------------------------------------------
    if data.startswith(
        "psychology_lesson:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "show_psychology_lesson",
                "show_psychology_lesson_content",
            ),
        )
    # ------------------------------------------------------
    # Complete lesson
    # ------------------------------------------------------
    if data.startswith(
        "psychology_complete:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "complete_psychology_lesson",
                "complete_psychology",
            ),
        )
    # ------------------------------------------------------
    # Quiz
    # ------------------------------------------------------
    if data.startswith(
        "psychology_quiz:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "start_psychology_quiz",
            ),
        )
    # ------------------------------------------------------
    # Quiz answer
    # ------------------------------------------------------
    if data.startswith(
        "psychology_quiz_answer:"
    ):
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "answer_psychology_quiz",
                "handle_psychology_quiz_answer",
            ),
        )
    # ------------------------------------------------------
    # Quiz cancel
    # ------------------------------------------------------
    if data in {
        "psychology_quiz_cancel",
        "psychology_quiz_stop",
    }:
        return await _call_handler(
            update,
            context,
            module_path,
            (
                "cancel_psychology_quiz",
                "stop_psychology_quiz",
                "finish_psychology_quiz",
            ),
        )
    return False
# ==========================================================
# Central Callback Router
# ==========================================================
async def route_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Central callback router.
    The router only decides which module receives the
    callback. All module logic remains inside handlers.py.
    """
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    logger.info(
        "Central callback received: %s",
        data,
    )
    # ------------------------------------------------------
    # Main menu
    # ------------------------------------------------------
    if data == "menu_main":
        await show_main_menu(
            update,
            context,
        )
        return
    # ------------------------------------------------------
    # Management
    # ------------------------------------------------------
    handled = await _route_management(
        update,
        context,
        data,
    )
    if handled:
        return
    # ------------------------------------------------------
    # International Trade
    # ------------------------------------------------------
    handled = await _route_international_trade(
        update,
        context,
        data,
    )
    if handled:
        return
    # ------------------------------------------------------
    # Marketing
    # ------------------------------------------------------
    handled = await _route_marketing(
        update,
        context,
        data,
    )
    if handled:
        return
    # ------------------------------------------------------
    # Economy
    # ------------------------------------------------------
    handled = await _route_economy(
        update,
        context,
        data,
    )
    if handled:
        return
    # ------------------------------------------------------
    # Accounting
    # ------------------------------------------------------
    handled = await _route_accounting(
        update,
        context,
        data,
    )
    if handled:
        return
    # ------------------------------------------------------
    # Psychology
    # ------------------------------------------------------
    handled = await _route_psychology(
        update,
        context,
        data,
    )
    if handled:
        return
    # ------------------------------------------------------
    # Unknown callback
    # ------------------------------------------------------
    logger.warning(
        "Unknown callback received: %s",
        data,
    )
    try:
        await query.answer(
            "این بخش هنوز فعال نشده است.",
            show_alert=False,
        )
    except Exception:
        logger.exception(
            "Unable to answer unknown callback."
        )
# ==========================================================
# Menu Health Check
# ==========================================================
def menu_health_check() -> bool:
    """
    Basic health check for the central menu.
    Optional modules are deliberately not imported here.
    Therefore a problem in Accounting, Marketing, Economy,
    etc. cannot prevent the central router from loading.
    """
    try:
        required_functions = (
            main_menu_keyboard,
            show_main_menu,
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
