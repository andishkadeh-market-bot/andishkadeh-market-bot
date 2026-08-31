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
- General Exam module
- International Trade module
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
    MANAGEMENT_CHAPTER_LESSONS,
)
from modules.admin.handlers import (
    admin_command,
    route_admin_callback,
)
from modules.exam.handlers import (
    route_exam_callback,
    exam_handlers_health_check,
)
from modules.exam.data import (
    data_health_check,
)
from modules.exam.service import (
    exam_service_health_check,
)
from modules.international_trade.handlers import (
    route_international_trade_callback,
    international_trade_handlers_health_check,
)
from modules.international_trade.service import (
    get_module_info,
    get_chapters,
    get_lessons,
    get_lesson,
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
GENERAL_EXAM_MODULE_ID = "general_exam"
GENERAL_EXAM_MODULE_TITLE = "آزمون عمومی"
GENERAL_EXAM_CHAPTER_ID = "general"
GENERAL_EXAM_CHAPTER_TITLE = "آزمون عمومی"
GENERAL_EXAM_LESSON_ID = "general_quiz"
GENERAL_EXAM_LESSON_TITLE = "آزمون عمومی"
INTERNATIONAL_TRADE_MODULE_ID = "international_trade"
INTERNATIONAL_TRADE_MODULE_TITLE = "تجارت بین‌الملل"
# ==========================================================
# Management Auto Registry
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
            "Management Auto Registry complete: "
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
# General Exam Auto Registry
# ==========================================================
def register_general_exam_content() -> dict[str, int]:
    """
    Register the General Exam module.
    Structure:
        general_exam
            └── general
                    └── general_quiz
    """
    logger.info(
        "Starting General Exam Auto Registry..."
    )
    registry.register_module(
        module_id=GENERAL_EXAM_MODULE_ID,
        title=GENERAL_EXAM_MODULE_TITLE,
    )
    registry.register_chapter(
        module_id=GENERAL_EXAM_MODULE_ID,
        chapter_id=GENERAL_EXAM_CHAPTER_ID,
        title=GENERAL_EXAM_CHAPTER_TITLE,
    )
    registry.register_lesson(
        module_id=GENERAL_EXAM_MODULE_ID,
        chapter_id=GENERAL_EXAM_CHAPTER_ID,
        lesson_id=GENERAL_EXAM_LESSON_ID,
        title=GENERAL_EXAM_LESSON_TITLE,
        data={
            "type": "general_exam",
            "module_id": GENERAL_EXAM_MODULE_ID,
            "chapter_id": GENERAL_EXAM_CHAPTER_ID,
            "lesson_id": GENERAL_EXAM_LESSON_ID,
        },
    )
    statistics = registry.statistics()
    logger.info(
        (
            "General Exam Auto Registry complete: "
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
# International Trade Auto Registry
# ==========================================================
def register_international_trade_content() -> dict[str, int]:
    """
    Register the complete International Trade module.
    Content is loaded from:
        modules.international_trade.service
    Structure:
        international_trade
            ├── chapters
            │     └── lessons
            │
            └── lesson data
    """
    logger.info(
        "Starting International Trade Auto Registry..."
    )
    module_id = INTERNATIONAL_TRADE_MODULE_ID
    module_title = INTERNATIONAL_TRADE_MODULE_TITLE
    try:
        module_info = get_module_info()
        if isinstance(module_info, dict):
            module_id = str(
                module_info.get(
                    "id",
                    module_info.get(
                        "module_id",
                        module_id,
                    ),
                )
            )
            module_title = str(
                module_info.get(
                    "title",
                    module_title,
                )
            )
    except Exception:
        logger.exception(
            "Failed to load International Trade module info."
        )
    registry.register_module(
        module_id=module_id,
        title=module_title,
    )
    try:
        chapters = get_chapters()
    except Exception:
        logger.exception(
            "Failed to load International Trade chapters."
        )
        chapters = []
    registered_chapters = 0
    registered_lessons = 0
    for chapter in chapters:
        if not isinstance(
            chapter,
            dict,
        ):
            continue
        chapter_id = (
            chapter.get("id")
            or chapter.get("chapter_id")
        )
        if not chapter_id:
            continue
        chapter_id = str(
            chapter_id
        )
        chapter_title = (
            chapter.get("title")
            or chapter.get("name")
            or chapter_id
        )
        registry.register_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
            title=str(chapter_title),
        )
        registered_chapters += 1
        try:
            lessons = get_lessons(
                chapter_id
            )
        except Exception:
            logger.exception(
                (
                    "Failed to load lessons "
                    "for International Trade chapter %s."
                ),
                chapter_id,
            )
            lessons = []
        for lesson in lessons:
            if not isinstance(
                lesson,
                dict,
            ):
                continue
            lesson_id = (
                lesson.get("id")
                or lesson.get("lesson_id")
            )
            if not lesson_id:
                continue
            lesson_id = str(
                lesson_id
            )
            lesson_title = (
                lesson.get("title")
                or lesson.get("name")
                or lesson_id
            )
            registry.register_lesson(
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=str(lesson_title),
                data=lesson,
            )
            registered_lessons += 1
    statistics = registry.statistics()
    logger.info(
        (
            "International Trade Auto Registry complete: "
            "module=%s chapters=%s lessons=%s"
        ),
        module_id,
        registered_chapters,
        registered_lessons,
    )
    logger.info(
        (
            "Global Registry after International Trade: "
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
# Complete Auto Registry
# ==========================================================
def register_all_content() -> dict[str, int]:
    """
    Register all currently available modules.
    Modules:
    - Management
    - General Exam
    - International Trade
    """
    logger.info(
        "========================================"
    )
    logger.info(
        "Starting complete Auto Registry..."
    )
    register_management_content()
    register_general_exam_content()
    register_international_trade_content()
    statistics = registry.statistics()
    result = {
        "modules": statistics["modules"],
        "chapters": statistics["chapters"],
        "lessons": statistics["lessons"],
    }
    logger.info(
        (
            "Complete Auto Registry finished: "
            "modules=%s chapters=%s lessons=%s"
        ),
        result["modules"],
        result["chapters"],
        result["lessons"],
    )
    logger.info(
        "========================================"
    )
    return result
# ==========================================================
# Core Health Checks
# ==========================================================
def run_core_health_checks() -> bool:
    """
    Run local health checks for core systems.
    No Telegram API request is performed.
    """
    logger.info(
        "Running core health checks..."
    )
    try:
        registry_stats = (
            registry.statistics()
        )
        if not isinstance(
            registry_stats,
            dict,
        ):
            logger.error(
                "Registry health check failed."
            )
            return False
        if (
            registry_stats.get(
                "modules",
                0,
            )
            < 1
        ):
            logger.error(
                "Registry contains no modules."
            )
            return False
        logger.info(
            "Registry health check: OK"
        )
    except Exception:
        logger.exception(
            "Registry health check failed."
        )
        return False
    return True
# ==========================================================
# General Exam Health Checks
# ==========================================================
def run_exam_health_checks() -> bool:
    """
    Run all local health checks for General Exam.
    Checks:
    - Question bank
    - Exam service
    - Exam handlers
    """
    logger.info(
        "Running General Exam health checks..."
    )
    try:
        if not data_health_check():
            logger.error(
                "General Exam data health check failed."
            )
            return False
        logger.info(
            "General Exam data: OK"
        )
        if not exam_service_health_check():
            logger.error(
                "General Exam service health check failed."
            )
            return False
        logger.info(
            "General Exam service: OK"
        )
        if not exam_handlers_health_check():
            logger.error(
                "General Exam handlers health check failed."
            )
            return False
        logger.info(
            "General Exam handlers: OK"
        )
        return True
    except Exception:
        logger.exception(
            "General Exam health checks failed."
        )
        return False
# ==========================================================
# International Trade Health Checks
# ==========================================================
def run_international_trade_health_checks() -> bool:
    """
    Run local health checks for International Trade.
    """
    logger.info(
        "Running International Trade health checks..."
    )
    try:
        if not international_trade_handlers_health_check():
            logger.error(
                "International Trade handlers health check failed."
            )
            return False
        logger.info(
            "International Trade handlers: OK"
        )
        try:
            module_info = get_module_info()
            if not isinstance(
                module_info,
                dict,
            ):
                logger.error(
                    "International Trade module info is invalid."
                )
                return False
        except Exception:
            logger.exception(
                "International Trade module info health check failed."
            )
            return False
        try:
            chapters = get_chapters()
            if not isinstance(
                chapters,
                list,
            ):
                logger.error(
                    "International Trade chapters data is invalid."
                )
                return False
        except Exception:
            logger.exception(
                "International Trade chapters health check failed."
            )
            return False
        logger.info(
            "International Trade data: OK"
        )
        return True
    except Exception:
        logger.exception(
            "International Trade health checks failed."
        )
        return False
# ==========================================================
# Core Initialization
# ==========================================================
def initialize_core() -> None:
    """
    Initialize all core systems.
    Order:
    1. SQLite
    2. Auto Registry
    3. Progress
    4. Statistics
    5. Core health checks
    6. General Exam health checks
    7. International Trade health checks
    """
    logger.info(
        "========================================"
    )
    logger.info(
        "Initializing SQLite database..."
    )
    init_database()
    logger.info(
        "SQLite database initialized successfully."
    )
    # ------------------------------------------------------
    # Auto Registry
    # ------------------------------------------------------
    logger.info(
        "Initializing complete Auto Registry..."
    )
    registry_result = (
        register_all_content()
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
    # ------------------------------------------------------
    # Progress
    # ------------------------------------------------------
    logger.info(
        "Initializing Progress system..."
    )
    initialize_progress_system()
    logger.info(
        "Progress system initialized successfully."
    )
    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------
    logger.info(
        "Initializing Statistics system..."
    )
    initialize_statistics_system()
    logger.info(
        "Statistics system initialized successfully."
    )
    # ------------------------------------------------------
    # Health Checks
    # ------------------------------------------------------
    if not run_core_health_checks():
        raise RuntimeError(
            "Core health checks failed."
        )
    if not run_exam_health_checks():
        raise RuntimeError(
            "General Exam health checks failed."
        )
    if not run_international_trade_health_checks():
        raise RuntimeError(
            "International Trade health checks failed."
        )
    logger.info(
        "All core systems initialized successfully."
    )
    logger.info(
        "========================================"
    )
# ==========================================================
# Auto User Registry
# ==========================================================
async def register_telegram_user(
    update: Update,
) -> bool:
    """
    Register or update current Telegram user.
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
    Automatically register users interacting
    with callback buttons.
    This handler is intentionally non-blocking.
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
# Error Handler
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
    Create and configure Telegram application.
    Callback order:
    1. Auto User Registry
    2. Admin callbacks
    3. General Exam callbacks
    4. International Trade callbacks
    5. Generic menu callbacks
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
    # General Exam callbacks
    #
    # Must be registered before generic menu router.
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_exam_callback,
            pattern=(
                r"^("
                r"exam_general_start"
                r"|exam_general_cancel"
                r"|exam_general_answer:\d+"
                r")$"
            ),
        )
    )
    # ======================================================
    # International Trade callbacks
    #
    # IMPORTANT:
    # Must be registered before generic menu router.
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_international_trade_callback,
            pattern=(
                r"^("
                r"menu_international_trade"
                r"|trade_chapters"
                r"|trade_chapter:.+"
                r"|trade_lesson:.+:.+"
                r"|trade_complete:.+:.+"
                r"|trade_quiz:.+:.+"
                r"|trade_quiz_answer:.+:.+:\d+:\d+"
                r"|trade_quiz_cancel:.+:.+"
                r")$"
            ),
        )
    )
    # ======================================================
    # Generic Menu callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_menu_callback
        )
    )
    # ======================================================
    # Error Handler
    # ======================================================
    application.add_error_handler(
        error_handler
    )
    logger.info(
        "Telegram application configured successfully."
    )
    return application
# ==========================================================
# Integration Health Check
# ==========================================================
def integration_health_check() -> bool:
    """
    Run local integration health checks.
    Verifies:
    - Registry
    - General Exam
    - International Trade
    """
    try:
        if not run_core_health_checks():
            return False
        if not run_exam_health_checks():
            return False
        if not run_international_trade_health_checks():
            return False
        logger.info(
            "========================================"
        )
        logger.info(
            "Integration health check: ALL TESTS PASSED"
        )
        logger.info(
            "========================================"
        )
        return True
    except Exception:
        logger.exception(
            "Integration health check failed."
        )
        return False
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
# Entry Point
# ==========================================================
if __name__ == "__main__":
    main()
