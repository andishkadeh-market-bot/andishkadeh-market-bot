"""
Central menu routing for Andishkadeh Management & Market.
Responsibilities:
- Show the main menu
- Route module menu callbacks
- Keep module-specific handlers from being processed twice
- Provide menu health checks
"""
from __future__ import annotations
import logging
from importlib import import_module
from typing import Any, Awaitable, Callable
from telegram import Update
from telegram.ext import ContextTypes
logger = logging.getLogger(__name__)
# ============================================================
# Safe module loader
# ============================================================
def _load_module(module_path: str) -> Any | None:
    """Safely import a module."""
    try:
        return import_module(module_path)
    except Exception:
        logger.exception(
            "Failed to load module: %s",
            module_path,
        )
        return None
def _get_function(
    module: Any | None,
    function_name: str,
) -> Callable[..., Any] | None:
    """Safely get a callable from a module."""
    if module is None:
        return None
    function = getattr(module, function_name, None)
    if callable(function):
        return function
    return None
async def _call_handler(
    handler: Callable[..., Any] | None,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> Any:
    """Call sync or async handler safely."""
    if handler is None:
        return None
    try:
        result = handler(update, context)
        if isinstance(result, Awaitable):
            return await result
        return result
    except Exception:
        logger.exception("Menu handler failed")
        return None
async def _answer_callback(update: Update) -> None:
    """Safely answer a callback query."""
    query = update.callback_query
    if query is None:
        return
    try:
        await query.answer()
    except Exception:
        logger.exception(
            "Failed to answer callback query"
        )
# ============================================================
# Main Menu
# ============================================================
async def show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show the main menu.
    Uses the actual keyboard function defined in
    core.keyboards:
        main_menu_keyboard()
    """
    await _answer_callback(update)
    keyboards = _load_module("core.keyboards")
    if keyboards is None:
        logger.error(
            "core.keyboards could not be loaded"
        )
        return
    # --------------------------------------------------------
    # IMPORTANT:
    # The actual function in core/keyboards.py is:
    # main_menu_keyboard()
    # --------------------------------------------------------
    builder = _get_function(
        keyboards,
        "main_menu_keyboard",
    )
    if builder is None:
        logger.error(
            "main_menu_keyboard() was not found in core.keyboards"
        )
        return
    try:
        keyboard = builder()
        message = update.effective_message
        if message is None:
            logger.warning(
                "No effective message available for main menu"
            )
            return
        await message.reply_text(
            "منوی اصلی اندیشکده مدیریت و بازار:",
            reply_markup=keyboard,
        )
    except Exception:
        logger.exception(
            "Failed to show main menu"
        )
# ============================================================
# Management
# ============================================================
async def _route_management(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Management callbacks."""
    module = _load_module(
        "modules.management.handlers"
    )
    if module is None:
        return False
    if data == "menu_management":
        handler = _get_function(
            module,
            "show_management_menu",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("management_chapter:"):
        handler = _get_function(
            module,
            "show_management_chapter",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("management_lesson:"):
        handler = _get_function(
            module,
            "show_management_lesson",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("management_quiz_start"):
        handler = _get_function(
            module,
            "start_management_quiz",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("management_quiz_answer:"):
        handler = _get_function(
            module,
            "answer_management_quiz",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("management_quiz:"):
        handler = _get_function(
            module,
            "handle_management_quiz",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data in {
        "management_quiz_next",
        "management_quiz_stop",
        "management_quiz_cancel",
    }:
        handler = _get_function(
            module,
            "handle_management_quiz",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# International Trade
# ============================================================
async def _route_international_trade(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route International Trade callbacks."""
    module = _load_module(
        "modules.international_trade.handlers"
    )
    if module is None:
        return False
    if data == "menu_international_trade":
        handler = _get_function(
            module,
            "show_trade_menu",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("trade_chapter:"):
        handler = _get_function(
            module,
            "show_trade_chapter",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("trade_lesson:"):
        handler = _get_function(
            module,
            "show_trade_lesson",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("trade_quiz"):
        handler = _get_function(
            module,
            "handle_trade_quiz",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Marketing
# ============================================================
async def _route_marketing(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Marketing callbacks."""
    module = _load_module(
        "modules.marketing.handlers"
    )
    if module is None:
        return False
    if data == "menu_marketing":
        handler = _get_function(
            module,
            "show_marketing_menu",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("marketing_"):
        handler = _get_function(
            module,
            "handle_marketing_callback",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Economy
# ============================================================
async def _route_economy(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Economy callbacks."""
    module = _load_module(
        "modules.economy.handlers"
    )
    if module is None:
        return False
    # Actual callback from core.keyboards.py:
    # menu_economics
    if data == "menu_economics":
        handler = _get_function(
            module,
            "show_economy_menu",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("economy_"):
        handler = _get_function(
            module,
            "handle_economy_callback",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Accounting
# ============================================================
async def _route_accounting(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Accounting callbacks."""
    module = _load_module(
        "modules.accounting.handlers"
    )
    if module is None:
        return False
    if data == "menu_accounting":
        handler = _get_function(
            module,
            "show_accounting_menu",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("accounting_"):
        handler = _get_function(
            module,
            "handle_accounting_callback",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Psychology & Social Work
# ============================================================
async def _route_psychology(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Psychology & Social Work callbacks."""
    module = _load_module(
        "modules.psychology.handlers"
    )
    if module is None:
        return False
    if data == "menu_psychology":
        handler = _get_function(
            module,
            "show_psychology_menu",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    if data.startswith("psychology_"):
        handler = _get_function(
            module,
            "handle_psychology_callback",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Finance
# ============================================================
async def _route_finance(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Finance callbacks."""
    module = _load_module(
        "modules.finance.handlers"
    )
    if module is None:
        return False
    if (
        data == "menu_finance"
        or data == "finance_menu"
        or data == "finance_back"
        or data.startswith("finance_chapter:")
        or data.startswith("finance_lesson:")
    ):
        handler = _get_function(
            module,
            "route_finance_callback",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Random Quiz
# ============================================================
async def _route_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: str,
) -> bool:
    """Route Random Quiz callbacks."""
    module = _load_module(
        "modules.random_quiz.handlers"
    )
    if module is None:
        return False
    if data == "menu_random" or data.startswith("random_quiz"):
        handler = _get_function(
            module,
            "handle_random_quiz_callback",
        )
        if handler is not None:
            await _call_handler(
                handler,
                update,
                context,
            )
            return True
    return False
# ============================================================
# Central callback router
# ============================================================
async def route_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Central router for menu callbacks.
    Dedicated module callbacks are skipped here when bot.py
    already has a dedicated handler for them.
    """
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    logger.debug(
        "Central menu router received callback: %s",
        data,
    )
    await _answer_callback(update)
    # --------------------------------------------------------
    # Main Menu
    # --------------------------------------------------------
    if data == "menu_main":
        await show_main_menu(
            update,
            context,
        )
        return
    # --------------------------------------------------------
    # Finance
    # --------------------------------------------------------
    if (
        data == "menu_finance"
        or data == "finance_menu"
        or data == "finance_back"
        or data.startswith("finance_chapter:")
        or data.startswith("finance_lesson:")
    ):
        logger.debug(
            "Skipping central Finance routing: %s",
            data,
        )
        return
    # --------------------------------------------------------
    # Management
    # --------------------------------------------------------
    if (
        data == "menu_management"
        or data.startswith("management_chapter:")
        or data.startswith("management_lesson:")
        or data.startswith("management_quiz_start")
        or data.startswith("management_quiz:")
        or data.startswith("management_quiz_answer:")
        or data in {
            "management_quiz_next",
            "management_quiz_stop",
            "management_quiz_cancel",
        }
    ):
        logger.debug(
            "Skipping central Management routing: %s",
            data,
        )
        return
    # --------------------------------------------------------
    # International Trade
    # --------------------------------------------------------
    if (
        data == "menu_international_trade"
        or data.startswith("trade_chapter:")
        or data.startswith("trade_lesson:")
        or data.startswith("trade_quiz")
    ):
        logger.debug(
            "Skipping central International Trade routing: %s",
            data,
        )
        return
    # --------------------------------------------------------
    # Psychology
    # --------------------------------------------------------
    if (
        data == "menu_psychology"
        or data.startswith("psychology_")
    ):
        logger.debug(
            "Skipping central Psychology routing: %s",
            data,
        )
        return
    # --------------------------------------------------------
    # Banking
    # --------------------------------------------------------
    if (
        data == "menu_banking"
        or data.startswith("banking_")
    ):
        logger.debug(
            "Skipping central Banking routing: %s",
            data,
        )
        return
    # --------------------------------------------------------
    # General Exam
    # --------------------------------------------------------
    if (
        data == "menu_exam"
        or data.startswith("exam_")
    ):
        logger.debug(
            "Skipping central Exam routing: %s",
            data,
        )
        return
    # --------------------------------------------------------
    # Random Quiz
    # --------------------------------------------------------
    handled = await _route_random_quiz(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # Management compatibility route
    # --------------------------------------------------------
    handled = await _route_management(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # International Trade compatibility route
    # --------------------------------------------------------
    handled = await _route_international_trade(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # Marketing
    # --------------------------------------------------------
    handled = await _route_marketing(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # Economy
    # --------------------------------------------------------
    handled = await _route_economy(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # Accounting
    # --------------------------------------------------------
    handled = await _route_accounting(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # Psychology compatibility route
    # --------------------------------------------------------
    handled = await _route_psychology(
        update,
        context,
        data,
    )
    if handled:
        return
    # --------------------------------------------------------
    # Finance compatibility route
    # --------------------------------------------------------
    handled = await _route_finance(
        update,
        context,
        data,
    )
    if handled:
        return
    logger.debug(
        "No central menu route matched callback: %s",
        data,
    )
# ============================================================
# Health Check
# ============================================================
def menu_health_check() -> dict[str, Any]:
    """
    Check central menu configuration and module handlers.
    """
    result: dict[str, Any] = {
        "module": "core.menu",
        "status": "ok",
        "checks": {},
    }
    # --------------------------------------------------------
    # Keyboard check
    # --------------------------------------------------------
    keyboards = _load_module(
        "core.keyboards"
    )
    keyboard_available = False
    if keyboards is not None:
        keyboard_builder = _get_function(
            keyboards,
            "main_menu_keyboard",
        )
        if keyboard_builder is not None:
            try:
                keyboard = keyboard_builder()
                keyboard_available = (
                    keyboard is not None
                    and bool(
                        keyboard.inline_keyboard
                    )
                )
            except Exception:
                logger.exception(
                    "Main keyboard health check failed"
                )
    result["checks"]["main_keyboard"] = {
        "available": keyboard_available,
    }
    if not keyboard_available:
        result["status"] = "warning"
    # --------------------------------------------------------
    # Module handler checks
    # --------------------------------------------------------
    required_modules = {
        "management": (
            "modules.management.handlers"
        ),
        "banking": (
            "modules.banking.handlers"
        ),
        "international_trade": (
            "modules.international_trade.handlers"
        ),
        "marketing": (
            "modules.marketing.handlers"
        ),
        "economy": (
            "modules.economy.handlers"
        ),
        "accounting": (
            "modules.accounting.handlers"
        ),
        "psychology": (
            "modules.psychology.handlers"
        ),
        "finance": (
            "modules.finance.handlers"
        ),
        "random_quiz": (
            "modules.random_quiz.handlers"
        ),
    }
    failed = []
    for name, module_path in required_modules.items():
        module = _load_module(
            module_path
        )
        available = module is not None
        result["checks"][name] = {
            "module": module_path,
            "available": available,
        }
        if not available:
            failed.append(name)
    if failed:
        result["status"] = "warning"
        result["failed_modules"] = failed
    return result
# ============================================================
# Backward-compatible aliases
# ============================================================
show_menu = show_main_menu
handle_menu_callback = route_menu_callback
__all__ = [
    "show_main_menu",
    "route_menu_callback",
    "handle_menu_callback",
    "show_menu",
    "menu_health_check",
]
