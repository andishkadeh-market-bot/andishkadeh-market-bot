"""
Andishkadeh Management & Market
Lightweight bot core.
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

from config import BOT_TOKEN, APP_NAME, APP_VERSION
from database import Database

from core.menu import (
    show_main_menu,
    show_section_placeholder,
    SECTION_TITLES,
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
# Callback Router
# ==========================================================

async def callback_router(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route callback queries to the correct menu handler."""

    query = update.callback_query

    if query is None:
        return

    if query.data == "menu_main":
        await show_main_menu(
            update,
            context,
        )
        return

    if query.data in SECTION_TITLES:
        await show_section_placeholder(
            update,
            context,
        )
        return

    await query.answer(
        "این گزینه هنوز فعال نشده است."
    )


# ==========================================================
# Application
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
            callback_router
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
