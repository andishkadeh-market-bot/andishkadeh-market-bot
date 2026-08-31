"""
Andishkadeh Management & Market
Main Telegram bot entry point.

Architecture:
    Telegram
        ↓
    bot.py
        ↓
    Core initialization
        ├── SQLite Database
        ├── Auto Registry
        ├── User Progress
        └── Statistics
        ↓
    Menu Router
        ↓
    Modules
"""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from config import (
    APP_NAME,
    APP_VERSION,
    BOT_TOKEN,
)

from core.database import (
    init_database,
    upsert_user,
)

from core.menu import (
    route_menu_callback,
    show_main_menu,
)

from core.progress import (
    initialize_progress_system,
)

from core.statistics import (
    initialize_statistics_system,
)


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Core initialization
# ==========================================================

def initialize_core() -> None:
    """
    Initialize all persistent core systems.

    The database is initialized once.
    Registry, Progress and Statistics use
    the same SQLite database.
    """

    logger.info(
        "Initializing SQLite database..."
    )

    init_database()

    logger.info(
        "Initializing Progress system..."
    )

    initialize_progress_system()

    logger.info(
        "Initializing Statistics system..."
    )

    initialize_statistics_system()

    logger.info(
        "Core systems initialized successfully."
    )


# ==========================================================
# /start
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle /start command.

    Every Telegram user is automatically
    registered or updated in SQLite.
    """

    user = update.effective_user

    if user is None:
        return

    if update.message is None:
        return

    try:

        upsert_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        logger.info(
            "User registered: telegram_id=%s username=%s",
            user.id,
            user.username,
        )

    except Exception:
        logger.exception(
            "Failed to register user: telegram_id=%s",
            user.id,
        )

        await update.message.reply_text(
            "خطایی در ثبت اطلاعات شما رخ داد. "
            "لطفاً دوباره /start را ارسال کنید."
        )

        return

    await show_main_menu(
        update,
        context,
    )


# ==========================================================
# Error handler
# ==========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Global Telegram error handler.
    """

    logger.error(
        "Unhandled Telegram error: %s",
        context.error,
        exc_info=context.error,
    )


# ==========================================================
# Application Factory
# ==========================================================

def build_application() -> Application:
    """
    Create and configure the Telegram application.
    """

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not configured."
        )

    # ------------------------------------------------------
    # Initialize persistent core
    # ------------------------------------------------------

    initialize_core()

    # ------------------------------------------------------
    # Build Telegram application
    # ------------------------------------------------------

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # ------------------------------------------------------
    # Commands
    # ------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    # ------------------------------------------------------
    # Callback router
    # ------------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            route_menu_callback
        )
    )

    # ------------------------------------------------------
    # Global error handler
    # ------------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    return application


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Start the Telegram bot.
    """

    logger.info(
        "========================================"
    )

    logger.info(
        "%s v%s is starting...",
        APP_NAME,
        APP_VERSION,
    )

    logger.info(
        "Initializing application..."
    )

    application = build_application()

    logger.info(
        "Application initialized successfully."
    )

    logger.info(
        "Starting polling..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# ==========================================================
# Entry point
# ==========================================================

if __name__ == "__main__":
    main()
