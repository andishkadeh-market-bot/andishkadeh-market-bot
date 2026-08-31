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
- HTTP Health Server for Render/UptimeRobot
Modules:
- Management
- General Exam
- International Trade
- Psychology & Social Work
- Banking
"""
from __future__ import annotations
import asyncio
import logging
import os
from contextlib import suppress
from aiohttp import web
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
# ==========================================================
# Management
# ==========================================================
from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)
from modules.management.handlers import (
    MANAGEMENT_CHAPTER_LESSONS,
)
# ==========================================================
# Admin
# ==========================================================
from modules.admin.handlers import (
    admin_command,
    route_admin_callback,
)
# ==========================================================
# General Exam
# ==========================================================
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
# ==========================================================
# International Trade
# ==========================================================
from modules.international_trade.handlers import (
    route_international_trade_callback,
    international_trade_handlers_health_check,
)
from modules.international_trade.service import (
    get_module_info,
    get_chapters,
    get_lessons,
)
# ==========================================================
# Psychology & Social Work
# ==========================================================
from modules.psychology.handlers import (
    show_psychology_menu,
    show_psychology_chapter,
    show_psychology_lesson,
    complete_psychology_lesson,
    start_psychology_quiz,
    answer_psychology_quiz,
    cancel_psychology_quiz,
)
from modules.psychology.service import (
    register_psychology_module,
)
from modules.psychology.data import (
    MODULE_ID as PSYCHOLOGY_MODULE_ID,
    MODULE_TITLE as PSYCHOLOGY_MODULE_TITLE,
    get_chapters as get_psychology_chapters,
    get_curriculum_statistics as get_psychology_curriculum_statistics,
)
# ==========================================================
# Banking
# ==========================================================
try:
    from modules.banking.data import (
        MODULE_ID as BANKING_MODULE_ID,
        MODULE_TITLE as BANKING_MODULE_TITLE,
        MODULE_DESCRIPTION as BANKING_MODULE_DESCRIPTION,
        get_chapters as get_banking_chapters,
        data_health_check as banking_data_health_check,
    )
    BANKING_AVAILABLE = True
except ImportError:
    BANKING_MODULE_ID = "banking"
    BANKING_MODULE_TITLE = "🏦 بانکداری تخصصی"
    BANKING_MODULE_DESCRIPTION = (
        "ماژول بانکداری تخصصی"
    )
    BANKING_AVAILABLE = False
    def get_banking_chapters():
        return []
    def banking_data_health_check() -> bool:
        return False
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
# HTTP Health Server
# ==========================================================
async def health_handler(
    request: web.Request,
) -> web.Response:
    """
    Health endpoint for Render and UptimeRobot.
    Returns HTTP 200 when the application process
    is alive and the health endpoint is reachable.
    """
    return web.json_response(
        {
            "status": "ok",
            "service": "andishkadeh-market-bot",
            "app": APP_NAME,
            "version": APP_VERSION,
        },
        status=200,
    )
async def root_handler(
    request: web.Request,
) -> web.Response:
    """Simple root endpoint."""
    return web.Response(
        text=(
            "Andishkadeh Market Bot is running.\n"
            "Health: /health"
        ),
        status=200,
        content_type="text/plain",
    )
async def start_health_server() -> web.AppRunner:
    """
    Start the HTTP health server.
    Render provides the PORT environment variable.
    """
    port_value = os.environ.get(
        "PORT",
        "10000",
    )
    try:
        port = int(port_value)
    except ValueError:
        logger.warning(
            "Invalid PORT value '%s'. Using 10000.",
            port_value,
        )
        port = 10000
    app = web.Application()
    app.router.add_get(
        "/",
        root_handler,
    )
    app.router.add_get(
        "/health",
        health_handler,
    )
    runner = web.AppRunner(
        app,
        access_log=logger,
    )
    await runner.setup()
    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=port,
    )
    await site.start()
    logger.info(
        "HTTP Health Server started on 0.0.0.0:%s",
        port,
    )
    logger.info(
        "Health endpoint available at /health"
    )
    return runner
# ==========================================================
# Management Auto Registry
# ==========================================================
def register_management_content() -> dict[str, int]:
    """Register the complete Management module."""
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
    """Register the General Exam module."""
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
    """Register the complete International Trade module."""
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
    return {
        "modules": statistics["modules"],
        "chapters": statistics["chapters"],
        "lessons": statistics["lessons"],
    }
# ==========================================================
# Psychology Auto Registry
# ==========================================================
def register_psychology_content() -> dict[str, int]:
    """Register the Psychology & Social Work module."""
    logger.info(
        "Starting Psychology & Social Work Auto Registry..."
    )
    try:
        result = register_psychology_module()
        logger.info(
            (
                "Psychology Auto Registry complete: "
                "modules=%s chapters=%s lessons=%s"
            ),
            result.get("modules", 0),
            result.get("chapters", 0),
            result.get("lessons", 0),
        )
        return {
            "modules": int(
                result.get("modules", 0)
            ),
            "chapters": int(
                result.get("chapters", 0)
            ),
            "lessons": int(
                result.get("lessons", 0)
            ),
        }
    except Exception:
        logger.exception(
            "Psychology Auto Registry failed."
        )
        raise
# ==========================================================
# Banking Auto Registry
# ==========================================================
def register_banking_content() -> dict[str, int]:
    """
    Register Banking module when the module exists.
    At this stage only data.py exists, so chapters are
    registered. Lessons will be added when curriculum.py
    and handlers.py are created.
    """
    logger.info(
        "Starting Banking Auto Registry..."
    )
    if not BANKING_AVAILABLE:
        logger.warning(
            "Banking module is not available yet."
        )
        return {
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
        }
    registry.register_module(
        module_id=BANKING_MODULE_ID,
        title=BANKING_MODULE_TITLE,
    )
    registered_chapters = 0
    try:
        chapters = get_banking_chapters()
    except Exception:
        logger.exception(
            "Failed to load Banking chapters."
        )
        chapters = []
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
        chapter_title = (
            chapter.get("title")
            or chapter.get("name")
            or chapter_id
        )
        registry.register_chapter(
            module_id=BANKING_MODULE_ID,
            chapter_id=str(chapter_id),
            title=str(chapter_title),
        )
        registered_chapters += 1
    statistics = registry.statistics()
    logger.info(
        (
            "Banking Auto Registry complete: "
            "chapters=%s"
        ),
        registered_chapters,
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
    register_psychology_content()
    register_banking_content()
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
    """Run local health checks for core systems."""
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
    """Run all General Exam health checks."""
    logger.info(
        "Running General Exam health checks..."
    )
    try:
        if not data_health_check():
            logger.error(
                "General Exam data health check failed."
            )
            return False
        if not exam_service_health_check():
            logger.error(
                "General Exam service health check failed."
            )
            return False
        if not exam_handlers_health_check():
            logger.error(
                "General Exam handlers health check failed."
            )
            return False
        logger.info(
            "General Exam health checks: OK"
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
    """Run local health checks for International Trade."""
    logger.info(
        "Running International Trade health checks..."
    )
    try:
        if not international_trade_handlers_health_check():
            logger.error(
                "International Trade handlers health check failed."
            )
            return False
        module_info = get_module_info()
        if not isinstance(
            module_info,
            dict,
        ):
            logger.error(
                "International Trade module info is invalid."
            )
            return False
        chapters = get_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            logger.error(
                "International Trade chapters data is invalid."
            )
            return False
        logger.info(
            "International Trade health checks: OK"
        )
        return True
    except Exception:
        logger.exception(
            "International Trade health checks failed."
        )
        return False
# ==========================================================
# Psychology Health Checks
# ==========================================================
def run_psychology_health_checks() -> bool:
    """Run local health checks for Psychology."""
    logger.info(
        "Running Psychology & Social Work health checks..."
    )
    try:
        if not PSYCHOLOGY_MODULE_ID:
            return False
        if not PSYCHOLOGY_MODULE_TITLE:
            return False
        chapters = get_psychology_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            return False
        statistics = (
            get_psychology_curriculum_statistics()
        )
        if not isinstance(
            statistics,
            dict,
        ):
            return False
        chapters_count = int(
            statistics.get(
                "chapters",
                0,
            )
        )
        lessons_count = int(
            statistics.get(
                "lessons",
                0,
            )
        )
        questions_count = int(
            statistics.get(
                "questions",
                0,
            )
        )
        if chapters_count < 1:
            return False
        if lessons_count < 1:
            return False
        if questions_count < 1:
            return False
        logger.info(
            (
                "Psychology health checks: OK "
                "chapters=%s lessons=%s questions=%s"
            ),
            chapters_count,
            lessons_count,
            questions_count,
        )
        return True
    except Exception:
        logger.exception(
            "Psychology health checks failed."
        )
        return False
# ==========================================================
# Banking Health Checks
# ==========================================================
def run_banking_health_checks() -> bool:
    """
    Run Banking health checks.
    Banking is allowed to be in development stage.
    """
    logger.info(
        "Running Banking health checks..."
    )
    if not BANKING_AVAILABLE:
        logger.warning(
            "Banking module is not available yet."
        )
        return True
    try:
        if not BANKING_MODULE_ID:
            return False
        if not BANKING_MODULE_TITLE:
            return False
        if not banking_data_health_check():
            logger.error(
                "Banking data health check failed."
            )
            return False
        chapters = get_banking_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            return False
        logger.info(
            "Banking data: OK chapters=%s",
            len(chapters),
        )
        return True
    except Exception:
        logger.exception(
            "Banking health checks failed."
        )
        return False
# ==========================================================
# Core Initialization
# ==========================================================
def initialize_core() -> None:
    """Initialize all core systems."""
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
    logger.info(
        "Initializing Progress system..."
    )
    initialize_progress_system()
    logger.info(
        "Progress system initialized successfully."
    )
    logger.info(
        "Initializing Statistics system..."
    )
    initialize_statistics_system()
    logger.info(
        "Statistics system initialized successfully."
    )
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
    if not run_psychology_health_checks():
        raise RuntimeError(
            "Psychology & Social Work health checks failed."
        )
    if not run_banking_health_checks():
        raise RuntimeError(
            "Banking health checks failed."
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
    """Register or update current Telegram user."""
    user = update.effective_user
    if user is None:
        logger.warning(
            "Unable to register user: effective_user is None."
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
    """Handle /start."""
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
    """Handle /menu."""
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
    """Automatically register callback users."""
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
    """Global Telegram error handler."""
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
    IMPORTANT:
    The callback registry handler is NOT registered as a
    catch-all before the module handlers.
    Telegram handlers are ordered so actual module handlers
    receive callbacks before any generic fallback.
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
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_international_trade_callback,
            pattern=(
                r"^("
                r"menu_international_trade"
                r"|menu_trade"
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
    # Psychology callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            show_psychology_menu,
            pattern=r"^menu_psychology$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            show_psychology_chapter,
            pattern=r"^psychology_chapter:.+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            show_psychology_lesson,
            pattern=r"^psychology_lesson:.+:.+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            complete_psychology_lesson,
            pattern=r"^psychology_complete:.+:.+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            start_psychology_quiz,
            pattern=r"^psychology_quiz:.+:.+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            answer_psychology_quiz,
            pattern=r"^psychology_quiz_answer:\d+:\d+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            cancel_psychology_quiz,
            pattern=r"^psychology_quiz_cancel$",
        )
    )
    # ======================================================
    # Management callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            show_management_menu,
            pattern=r"^menu_management$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            show_management_chapter,
            pattern=r"^management_chapter:.+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            show_management_lesson,
            pattern=r"^management_lesson:.+:.+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            start_management_quiz,
            pattern=r"^management_quiz_start$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            answer_management_quiz,
            pattern=r"^management_quiz_answer:\d+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            cancel_management_quiz,
            pattern=r"^management_quiz_stop$",
        )
    )
    # ======================================================
    # Generic central menu router
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_menu_callback
        )
    )
    # ======================================================
    # Callback User Registry
    #
    # IMPORTANT:
    # This is registered AFTER all real callback handlers.
    # It is intentionally non-blocking.
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            callback_user_registry,
            pattern=r".+",
            block=False,
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
    """Run local integration health checks."""
    try:
        if not run_core_health_checks():
            return False
        if not run_exam_health_checks():
            return False
        if not run_international_trade_health_checks():
            return False
        if not run_psychology_health_checks():
            return False
        if not run_banking_health_checks():
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
# Main Async Runner
# ==========================================================
async def run_bot() -> None:
    """
    Run Telegram polling and HTTP health server together.
    """
    application = build_application()
    health_runner = await start_health_server()
    try:
        logger.info(
            "Initializing Telegram application..."
        )
        await application.initialize()
        logger.info(
            "Telegram application initialized successfully."
        )
        await application.start()
        logger.info(
            "Starting Telegram polling..."
        )
        await application.updater.start_polling(
            drop_pending_updates=True
        )
        logger.info(
            "Telegram polling started successfully."
        )
        logger.info(
            "Andishkadeh Management & Market is running."
        )
        # Keep both services alive.
        await asyncio.Event().wait()
    finally:
        logger.info(
            "Stopping Telegram application..."
        )
        if application.updater is not None:
            with suppress(Exception):
                await application.updater.stop()
        with suppress(Exception):
            await application.stop()
        with suppress(Exception):
            await application.shutdown()
        logger.info(
            "Stopping HTTP Health Server..."
        )
        with suppress(Exception):
            await health_runner.cleanup()
        logger.info(
            "Application shutdown complete."
        )
# ==========================================================
# Main
# ==========================================================
def main() -> None:
    """Start the application."""
    logger.info(
        "========================================"
    )
    logger.info(
        "%s v%s is starting...",
        APP_NAME,
        APP_VERSION,
    )
    logger.info(
        "Starting Telegram Bot + HTTP Health Server..."
    )
    try:
        asyncio.run(
            run_bot()
        )
    except KeyboardInterrupt:
        logger.info(
            "Application stopped by user."
        )
    except Exception:
        logger.exception(
            "Fatal application error."
        )
        raise
# ==========================================================
# Entry Point
# ==========================================================
if __name__ == "__main__":
    main()
