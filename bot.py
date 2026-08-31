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
)
from core.registry import (
    registry,
)
from core.progress import (
    initialize_progress_system,
    register_user,
)
from core.statistics import (
    initialize_statistics_system,
)
from core.menu import (
    route_menu_callback,
    show_main_menu,
)
from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)
from modules.management.handlers import (
    MANAGEMENT_LESSONS,
    MANAGEMENT_CHAPTER_LESSONS,
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
# Auto Registry
# ==========================================================
def register_management_content() -> None:
    """
    Register all currently available Management content.
    The in-memory Registry and SQLite database are both updated.
    Only lessons that actually exist in the detailed content
    layer are registered. This prevents placeholder curriculum
    entries from being counted as completed educational content.
    """
    module_id = "management"
    module_title = "آموزش مدیریت"
    logger.info(
        "Registering management module..."
    )
    registry.register_module(
        module_id=module_id,
        title=module_title,
    )
    registered_chapters = 0
    registered_lessons = 0
    for chapter in MANAGEMENT_CURRICULUM:
        chapter_id = chapter["id"]
        chapter_title = chapter["title"]
        detailed_lessons = (
            MANAGEMENT_CHAPTER_LESSONS.get(
                chapter_id,
                [],
            )
        )
        # --------------------------------------------------
        # Register chapter only when detailed content exists
        # --------------------------------------------------
        if not detailed_lessons:
            logger.info(
                "Skipping chapter without detailed lessons: %s",
                chapter_id,
            )
            continue
        registry.register_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
            title=chapter_title,
        )
        registered_chapters += 1
        # --------------------------------------------------
        # Register lessons
        # --------------------------------------------------
        for lesson in detailed_lessons:
            lesson_id = lesson.get(
                "id"
            )
            lesson_title = lesson.get(
                "title",
                lesson_id,
            )
            if not lesson_id:
                logger.warning(
                    "Skipping lesson without id "
                    "in chapter %s",
                    chapter_id,
                )
                continue
            registry.register_lesson(
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=lesson_title,
                data=lesson,
            )
            registered_lessons += 1
    statistics = registry.statistics()
    logger.info(
        "Management Registry initialized: "
        "chapters=%s lessons=%s",
        statistics["chapters"],
        statistics["lessons"],
    )
    logger.info(
        "Management content registration complete: "
        "chapters=%s lessons=%s",
        registered_chapters,
        registered_lessons,
    )
# ==========================================================
# Core initialization
# ==========================================================
def initialize_core() -> None:
    """
    Initialize all persistent core systems.
    Initialization order:
        1. SQLite
        2. Auto Registry
        3. Progress
        4. Statistics
    """
    logger.info(
        "========================================"
    )
    logger.info(
        "Initializing core systems..."
    )
    # ------------------------------------------------------
    # SQLite
    # ------------------------------------------------------
    logger.info(
        "Initializing SQLite database..."
    )
    init_database()
    logger.info(
        "SQLite database initialized."
    )
    # ------------------------------------------------------
    # Auto Registry
    # ------------------------------------------------------
    logger.info(
        "Initializing Auto Registry..."
    )
    register_management_content()
    logger.info(
        "Auto Registry initialized."
    )
    # ------------------------------------------------------
    # Progress
    # ------------------------------------------------------
    logger.info(
        "Initializing Progress system..."
    )
    initialize_progress_system()
    logger.info(
        "Progress system initialized."
    )
    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------
    logger.info(
        "Initializing Statistics system..."
    )
    initialize_statistics_system()
    logger.info(
        "Statistics system initialized."
    )
    logger.info(
        "All core systems initialized successfully."
    )
    logger.info(
        "========================================"
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
    Every Telegram user is automatically registered
    or updated in SQLite through the Progress application layer.
    """
    user = update.effective_user
    if user is None:
        return
    if update.message is None:
        return
    try:
        # --------------------------------------------------
        # Auto user registry
        # --------------------------------------------------
        register_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        logger.info(
            "User registered/updated: "
            "telegram_id=%s username=%s",
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
