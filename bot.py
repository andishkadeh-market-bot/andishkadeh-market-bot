"""
Andishkadeh Management & Market
Lightweight bot core.
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, APP_NAME, APP_VERSION
from database import Database

from core.menu import (
    route_menu_callback,
    show_main_menu,
)


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Database
# ==========================================================

db = Database()


# ==========================================================
# /start
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Handle /start command."""

    user = update.effective_user

    if user is None or update.message is None:
        return

    db.create_or_update_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    await show_main_menu(
        update,
        context,
    )


# ==========================================================
# Application Factory
# ==========================================================

def build_application() -> Application:
    """Create and configure the Telegram application."""

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            route_menu_callback
        )
    )

    return application


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """Start the Telegram bot."""

    application = build_application()

    logger.info(
        "%s v%s is starting...",
        APP_NAME,
        APP_VERSION,
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
