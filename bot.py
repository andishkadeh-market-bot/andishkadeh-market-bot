"""
Andishkadeh Management & Market
Main Telegram bot entry point.

Core:
- SQLite database
- Auto Registry
- Auto User Registry
- Progress
- Statistics
- Admin Dashboard
- Management module
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

from config import APP_NAME, APP_VERSION, BOT_TOKEN

from core.database import init_database
from core.registry import registry
from core.progress import (
    initialize_progress_system,
    register_user,
)
from core.statistics import initialize_statistics_system

from core.menu import (
    route_menu_callback,
    show_main_menu,
)

from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)

from modules.management.handlers import (
    MANAGEMENT_CHAPTER_LESSONS,
)

from modules.admin.handlers import (
    admin_command,
    route_admin_callback,
)


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

MANAGEMENT_MODULE_ID = "management"

MANAGEMENT_MODULE_TITLE = "آموزش مدیریت"


# ==========================================================
# Auto Registry
# ==========================================================

def register_management_content() -> dict[str, int]:
    """
    Register the complete Management module.

    Registers:
    - Module
    - Chapters
    - Lessons
    - Lesson data
    """

    logger.info(
        "Starting Management Auto Registry..."
    )

    registry.register_module(
        module_id=MANAGEMENT_MODULE_ID,
        title=MANAGEMENT_MODULE_TITLE,
    )

    for chapter in MANAGEMENT_CURRICULUM:

        chapter_id = chapter.get("id")

        if not chapter_id:
            continue

        detailed_lessons = (
            MANAGEMENT_CHAPTER_LESSONS.get(
                chapter_id,
                [],
            )
        )

        if not detailed_lessons:
            logger.warning(
                "Chapter '%s' has no registered lessons.",
                chapter_id,
            )
            continue

        registry.register_chapter(
            module_id=MANAGEMENT_MODULE_ID,
            chapter_id=chapter_id,
            title=chapter.get(
                "title",
                chapter_id,
            ),
        )

        for lesson in detailed_lessons:

            lesson_id = lesson.get("id")

            if not lesson_id:
                continue

            registry.register_lesson(
                module_id=MANAGEMENT_MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=lesson.get(
                    "title",
                    lesson_id,
                ),
                data=lesson,
            )

    statistics = registry.statistics()

    logger.info(
        (
            "Auto Registry complete: "
            "modules=%s chapters=%s lessons=%s"
        ),
        statistics["modules"],
        statistics["chapters"],
        statistics["lessons"],
    )

    return {
        "modules": statistics["modules"],
        "chapters": statistics["chapters"],
        "lessons": statistics["lessons"],
    }


# ==========================================================
# Core initialization
# ==========================================================

def initialize_core() -> None:
    """
    Initialize all core systems.

    Order:
    1. SQLite
    2. Auto Registry
    3. Progress
    4. Statistics
    """

    logger.info(
        "Initializing SQLite database..."
    )

    init_database()

    logger.info(
        "Initializing Auto Registry..."
    )

    registry_result = (
        register_management_content()
    )

    logger.info(
        (
            "Registry initialized: "
            "modules=%s chapters=%s lessons=%s"
        ),
        registry_result["modules"],
        registry_result["chapters"],
        registry_result["lessons"],
    )

    logger.info(
        "Initializing Progress system..."
    )

    initialize_progress_system()

    logger.info(
        "Initializing Statistics system..."
    )

    initialize_statistics_system()

    logger.info(
        "All core systems initialized successfully."
    )


# ==========================================================
# Auto User Registry
# ==========================================================

async def register_telegram_user(
    update: Update,
) -> bool:
    """
    Register or update the current Telegram user.

    Returns:
        True if the user was successfully registered.
        False otherwise.
    """

    user = update.effective_user

    if user is None:
        logger.warning(
            "Unable to register user: "
            "effective_user is None."
        )
        return False

    try:

        register_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        logger.info(
            (
                "Auto User Registry: "
                "telegram_id=%s username=%s"
            ),
            user.id,
            user.username,
        )

        return True

    except Exception:

        logger.exception(
            (
                "Auto User Registry failed: "
                "telegram_id=%s"
            ),
            user.id,
        )

        return False


# ==========================================================
# /start
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle /start.

    The user is automatically registered before
    the main menu is displayed.
    """

    if update.message is None:
        return

    registered = (
        await register_telegram_user(
            update
        )
    )

    if not registered:

        await update.message.reply_text(
            "❌ خطایی در ثبت اطلاعات شما رخ داد.\n\n"
            "لطفاً چند لحظه بعد دوباره /start را ارسال کنید."
        )

        return

    await show_main_menu(
        update,
        context,
    )


# ==========================================================
# /menu
# ==========================================================

async def menu_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle /menu.

    Re-registers the user and displays the main menu.
    """

    if update.message is None:
        return

    registered = (
        await register_telegram_user(
            update
        )
    )

    if not registered:

        await update.message.reply_text(
            "❌ خطایی در ثبت اطلاعات شما رخ داد."
        )

        return

    await show_main_menu(
        update,
        context,
    )


# ==========================================================
# Callback User Auto Registry
# ==========================================================

async def callback_user_registry(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Automatically register users interacting with
    callback buttons.

    This handler is intentionally placed before
    the menu routers.
    """

    user = update.effective_user

    if user is None:
        return

    try:

        register_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    except Exception:

        logger.exception(
            (
                "Callback Auto User Registry failed: "
                "telegram_id=%s"
            ),
            user.id,
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
# Application factory
# ==========================================================

def build_application() -> Application:
    """
    Create and configure the Telegram application.
    """

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN is not configured."
        )

    initialize_core()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # ======================================================
    # Commands
    # ======================================================

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CommandHandler(
            "menu",
            menu_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin_command,
        )
    )

    # ======================================================
    # Callback Auto User Registry
    # ======================================================

    application.add_handler(
        CallbackQueryHandler(
            callback_user_registry,
            pattern=r".+",
            block=False,
        )
    )

    # ======================================================
    # Admin callbacks
    #
    # IMPORTANT:
    # Admin callbacks must be registered BEFORE
    # the generic menu callback router.
    # ======================================================

    application.add_handler(
        CallbackQueryHandler(
            route_admin_callback,
            pattern=(
                r"^("
                r"admin_dashboard"
                r"|admin_users(?::\d+)?"
                r"|admin_user(?:_index)?:-?\d+"
                r"|admin_progress:-?\d+"
                r"|admin_attempts:-?\d+"
                r"|admin_module:.+"
                r")$"
            ),
        )
    )

    # ======================================================
    # Generic menu callbacks
    # ======================================================

    application.add_handler(
        CallbackQueryHandler(
            route_menu_callback
        )
    )

    # ======================================================
    # Error handler
    # ======================================================

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Telegram application configured successfully."
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
