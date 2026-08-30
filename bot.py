"""
Andishkadeh Management & Market
New lightweight bot core
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, APP_NAME, APP_VERSION
from database import Database


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
# Start
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Handle /start."""

    user = update.effective_user

    if user is None:
        return

    db.create_or_update_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    await update.message.reply_text(
        f"سلام {user.first_name} 🌱\n\n"
        f"به {APP_NAME} خوش آمدید.\n\n"
        f"نسخه: {APP_VERSION}\n\n"
        "هسته جدید ربات با موفقیت فعال شد."
    )


# ==========================================================
# Application
# ==========================================================

def build_application() -> Application:
    """Create and configure Telegram application."""

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    return application


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """Start the bot."""

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
