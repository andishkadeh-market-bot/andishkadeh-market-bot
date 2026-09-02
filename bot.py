"""
Andishkadeh Management & Market
Main Telegram bot entry point.
Core:
- SQLite database
- Auto Registry
- Content Initializer
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
- Finance
- Random Quiz
- Profile
"""
from __future__ import annotations
import asyncio
import logging
import os
from contextlib import suppress
from aiohttp import web
from telegram import MenuButtonCommands, Update
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
from core.content_initializer import initialize_all_content
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
from modules.membership.handlers import (
    is_member,
    show_membership_required,
    membership_handlers,
)
# ==========================================================
# Profile
# ==========================================================
from modules.profile.handlers import (
    route_profile_callback,
    profile_handlers_health_check,
)
# ==========================================================
# Management
# ==========================================================
from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)
from modules.management.handlers import (
    MANAGEMENT_CHAPTER_LESSONS,
    show_management_menu,
    show_management_chapter,
    show_management_lesson,
    start_management_quiz,
    answer_management_quiz,
    cancel_management_quiz,
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
    route_psychology_callback,
    psychology_handlers_health_check,
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
    from modules.banking.handlers import (
        route_banking_callback,
        banking_handlers_health_check,
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
    async def route_banking_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        return
    def banking_handlers_health_check() -> bool:
        return False
# ==========================================================
# Finance
# ==========================================================
try:
    from modules.finance.data import (
        MODULE_ID as FINANCE_MODULE_ID,
        MODULE_TITLE as FINANCE_MODULE_TITLE,
        MODULE_DESCRIPTION as FINANCE_MODULE_DESCRIPTION,
        get_chapters as get_finance_chapters,
        get_lessons as get_finance_lessons,
        data_health_check as finance_data_health_check,
    )
    from modules.finance.handlers import (
        route_finance_callback,
        finance_handlers_health_check,
    )
    FINANCE_AVAILABLE = True
except ImportError:
    FINANCE_MODULE_ID = "finance"
    FINANCE_MODULE_TITLE = "💰 مدیریت مالی"
    FINANCE_MODULE_DESCRIPTION = (
        "ماژول مدیریت مالی"
    )
    FINANCE_AVAILABLE = False
    def get_finance_chapters():
        return []
    def get_finance_lessons():
        return []
    def finance_data_health_check() -> bool:
        return False
    async def route_finance_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        return
    def finance_handlers_health_check() -> bool:
        return False
# ==========================================================
# Random Quiz
# ==========================================================
from modules.random_quiz.handlers import (
    route_random_quiz_callback,
    random_quiz_handlers_health_check,
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
# HTTP Health Server
# ==========================================================
async def health_handler(
    request: web.Request,
) -> web.Response:
    """
    Health endpoint for Render and UptimeRobot.
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
    """
    Simple root endpoint.
    """
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
    Start HTTP health server.
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
    """
    Register complete Management module.
    Kept for compatibility with the existing bot architecture.
    Primary content initialization is now handled by
    core.content_initializer.
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
    Register General Exam module.
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
    Register complete International Trade module.
    Kept for compatibility with the existing bot architecture.
    Primary content initialization is now handled by
    core.content_initializer.
    """
    logger.info(
        "Starting International Trade Auto Registry..."
    )
    module_id = INTERNATIONAL_TRADE_MODULE_ID
    module_title = INTERNATIONAL_TRADE_MODULE_TITLE
    try:
        module_info = get_module_info()
        if isinstance(
            module_info,
            dict,
        ):
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
    """
    Register complete Psychology & Social Work module.
    Kept for compatibility with the existing bot architecture.
    Primary content initialization is now handled by
    core.content_initializer.
    """
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
    Register complete Banking module.
    Kept for compatibility with the existing bot architecture.
    Primary content initialization is now handled by
    core.content_initializer.
    """
    logger.info(
        "Starting Banking Auto Registry..."
    )
    if not BANKING_AVAILABLE:
        logger.warning(
            "Banking module is not available."
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
    registered_lessons = 0
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
        chapter_id = str(
            chapter_id
        )
        chapter_title = (
            chapter.get("title")
            or chapter.get("name")
            or chapter_id
        )
        registry.register_chapter(
            module_id=BANKING_MODULE_ID,
            chapter_id=chapter_id,
            title=str(chapter_title),
        )
        registered_chapters += 1
        lessons = (
            chapter.get("lessons")
            or []
        )
        if isinstance(
            lessons,
            list,
        ):
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
                    module_id=BANKING_MODULE_ID,
                    chapter_id=chapter_id,
                    lesson_id=lesson_id,
                    title=str(lesson_title),
                    data=lesson,
                )
                registered_lessons += 1
    statistics = registry.statistics()
    logger.info(
        (
            "Banking Auto Registry complete: "
            "module=%s chapters=%s lessons=%s"
        ),
        BANKING_MODULE_ID,
        registered_chapters,
        registered_lessons,
    )
    return {
        "modules": statistics["modules"],
        "chapters": statistics["chapters"],
        "lessons": statistics["lessons"],
    }
# ==========================================================
# Finance Auto Registry
# ==========================================================
def register_finance_content() -> dict[str, int]:
    """
    Register complete Finance module.
    Kept for compatibility with the existing bot architecture.
    Primary content initialization is handled by
    core.content_initializer.
    """
    logger.info(
        "Starting Finance Auto Registry..."
    )
    if not FINANCE_AVAILABLE:
        logger.warning(
            "Finance module is not available."
        )
        return {
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
        }
    registry.register_module(
        module_id=FINANCE_MODULE_ID,
        title=FINANCE_MODULE_TITLE,
    )
    registered_chapters = 0
    registered_lessons = 0
    try:
        chapters = get_finance_chapters()
    except Exception:
        logger.exception(
            "Failed to load Finance chapters."
        )
        chapters = []
    lessons = []
    try:
        lessons = get_finance_lessons()
    except Exception:
        logger.exception(
            "Failed to load Finance lessons."
        )
    lessons_by_chapter: dict[str, list[dict]] = {}
    for lesson in lessons:
        if not isinstance(
            lesson,
            dict,
        ):
            continue
        chapter_id = lesson.get(
            "chapter_id"
        )
        lesson_id = lesson.get(
            "id"
        ) or lesson.get(
            "lesson_id"
        )
        if not chapter_id or not lesson_id:
            continue
        chapter_id = str(
            chapter_id
        )
        lessons_by_chapter.setdefault(
            chapter_id,
            [],
        ).append(
            lesson
        )
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
            module_id=FINANCE_MODULE_ID,
            chapter_id=chapter_id,
            title=str(chapter_title),
        )
        registered_chapters += 1
        for lesson in lessons_by_chapter.get(
            chapter_id,
            [],
        ):
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
                module_id=FINANCE_MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=str(lesson_title),
                data=lesson,
            )
            registered_lessons += 1
    statistics = registry.statistics()
    logger.info(
        (
            "Finance Auto Registry complete: "
            "module=%s chapters=%s lessons=%s"
        ),
        FINANCE_MODULE_ID,
        registered_chapters,
        registered_lessons,
    )
    return {
        "modules": statistics["modules"],
        "chapters": statistics["chapters"],
        "lessons": statistics["lessons"],
    }
# ==========================================================
# Complete Content Initialization
# ==========================================================
def register_all_content() -> dict[str, int]:
    """
    Initialize all educational content.
    The new architecture uses core.content_initializer as
    the primary source of truth for module content.
    General Exam remains registered separately because it is
    not part of the current CONTENT_PACKAGES handled by the
    content initializer.
    """
    logger.info(
        "========================================"
    )
    logger.info(
        "Starting complete Content Initialization..."
    )
    try:
        initializer_result = (
            initialize_all_content()
        )
        if not isinstance(
            initializer_result,
            dict,
        ):
            logger.warning(
                (
                    "Content Initializer returned "
                    "an unexpected result: %r"
                ),
                initializer_result,
            )
            initializer_result = {}
        if initializer_result.get(
            "status"
        ) == "error":
            raise RuntimeError(
                "Content Initializer returned an error."
            )
        logger.info(
            (
                "Content Initializer finished: "
                "modules=%s chapters=%s lessons=%s"
            ),
            initializer_result.get(
                "modules",
                0,
            ),
            initializer_result.get(
                "chapters",
                0,
            ),
            initializer_result.get(
                "lessons",
                0,
            ),
        )
    except Exception:
        logger.exception(
            "Content Initializer failed."
        )
        raise
    try:
        register_general_exam_content()
    except Exception:
        logger.exception(
            "General Exam content registration failed."
        )
        raise
    statistics = registry.statistics()
    result = {
        "modules": int(
            statistics.get(
                "modules",
                0,
            )
        ),
        "chapters": int(
            statistics.get(
                "chapters",
                0,
            )
        ),
        "lessons": int(
            statistics.get(
                "lessons",
                0,
            )
        ),
    }
    logger.info(
        (
            "Complete Content Initialization finished: "
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
    Run core health checks.
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
        if (
            registry_stats.get(
                "lessons",
                0,
            )
            < 1
        ):
            logger.error(
                "Registry contains no lessons."
            )
            return False
        logger.info(
            (
                "Registry health check: OK "
                "modules=%s chapters=%s lessons=%s"
            ),
            registry_stats.get(
                "modules",
                0,
            ),
            registry_stats.get(
                "chapters",
                0,
            ),
            registry_stats.get(
                "lessons",
                0,
            ),
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
    Run General Exam health checks.
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
    """
    Run International Trade health checks.
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
# Psychology Handlers Health Check
# ==========================================================
def run_psychology_handlers_health_check() -> bool:
    """
    Check Psychology callback handlers.
    """
    logger.info(
        "Running Psychology handlers health check..."
    )
    try:
        result = psychology_handlers_health_check()
        if not result:
            logger.error(
                "Psychology handlers health check failed."
            )
            return False
        logger.info(
            "Psychology handlers health check: OK"
        )
        return True
    except Exception:
        logger.exception(
            "Psychology handlers health check failed."
        )
        return False
# ==========================================================
# Psychology Health Checks
# ==========================================================
def run_psychology_health_checks() -> bool:
    """
    Run complete Psychology & Social Work health checks.
    """
    logger.info(
        "Running Psychology & Social Work health checks..."
    )
    try:
        if not PSYCHOLOGY_MODULE_ID:
            logger.error(
                "Psychology module ID is empty."
            )
            return False
        if not PSYCHOLOGY_MODULE_TITLE:
            logger.error(
                "Psychology module title is empty."
            )
            return False
        chapters = get_psychology_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            logger.error(
                "Psychology chapters data is invalid."
            )
            return False
        statistics = (
            get_psychology_curriculum_statistics()
        )
        if not isinstance(
            statistics,
            dict,
        ):
            logger.error(
                "Psychology curriculum statistics are invalid."
            )
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
        if chapters_count < 12:
            logger.error(
                (
                    "Psychology curriculum incomplete: "
                    "expected at least 12 chapters, got %s"
                ),
                chapters_count,
            )
            return False
        if lessons_count < 1:
            logger.error(
                "Psychology contains no lessons."
            )
            return False
        if questions_count < 1:
            logger.error(
                "Psychology contains no quiz questions."
            )
            return False
        if not run_psychology_handlers_health_check():
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
    """
    logger.info(
        "Running Banking health checks..."
    )
    if not BANKING_AVAILABLE:
        logger.error(
            "Banking module is not available."
        )
        return False
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
        if not banking_handlers_health_check():
            logger.error(
                "Banking handlers health check failed."
            )
            return False
        chapters = get_banking_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            logger.error(
                "Banking chapters data is invalid."
            )
            return False
        logger.info(
            (
                "Banking health checks: OK "
                "chapters=%s"
            ),
            len(chapters),
        )
        return True
    except Exception:
        logger.exception(
            "Banking health checks failed."
        )
        return False
# ==========================================================
# Finance Health Checks
# ==========================================================
def run_finance_health_checks() -> bool:
    """
    Run Finance health checks.
    """
    logger.info(
        "Running Finance health checks..."
    )
    if not FINANCE_AVAILABLE:
        logger.error(
            "Finance module is not available."
        )
        return False
    try:
        if not FINANCE_MODULE_ID:
            logger.error(
                "Finance module ID is empty."
            )
            return False
        if not FINANCE_MODULE_TITLE:
            logger.error(
                "Finance module title is empty."
            )
            return False
        if not finance_data_health_check():
            logger.error(
                "Finance data health check failed."
            )
            return False
        if not finance_handlers_health_check():
            logger.error(
                "Finance handlers health check failed."
            )
            return False
        chapters = get_finance_chapters()
        if not isinstance(
            chapters,
            list,
        ):
            logger.error(
                "Finance chapters data is invalid."
            )
            return False
        lessons = get_finance_lessons()
        if not isinstance(
            lessons,
            list,
        ):
            logger.error(
                "Finance lessons data is invalid."
            )
            return False
        logger.info(
            (
                "Finance health checks: OK "
                "chapters=%s lessons=%s"
            ),
            len(chapters),
            len(lessons),
        )
        return True
    except Exception:
        logger.exception(
            "Finance health checks failed."
        )
        return False
# ==========================================================
# Profile Health Check
# ==========================================================
def run_profile_health_check() -> bool:
    """
    Run Profile handlers health check.
    """
    logger.info(
        "Running Profile handlers health check..."
    )
    try:
        result = profile_handlers_health_check()
        if not isinstance(
            result,
            dict,
        ):
            logger.error(
                "Profile handlers health check returned invalid result."
            )
            return False
        status = result.get(
            "status",
            "error",
        )
        if status not in (
            "ok",
            "healthy",
        ):
            logger.error(
                "Profile handlers health check failed: %s",
                result,
            )
            return False
        logger.info(
            "Profile handlers health check: OK"
        )
        return True
    except Exception:
        logger.exception(
            "Profile handlers health check failed."
        )
        return False
# ==========================================================
# Content Initializer Health Check
# ==========================================================
def run_content_initializer_health_check() -> bool:
    """
    Verify that the content initializer is available and
    the registry contains educational content.
    """
    logger.info(
        "Running Content Initializer health check..."
    )
    try:
        registry_stats = registry.statistics()
        if not isinstance(
            registry_stats,
            dict,
        ):
            logger.error(
                "Content Initializer registry result is invalid."
            )
            return False
        modules = int(
            registry_stats.get(
                "modules",
                0,
            )
        )
        chapters = int(
            registry_stats.get(
                "chapters",
                0,
            )
        )
        lessons = int(
            registry_stats.get(
                "lessons",
                0,
            )
        )
        if modules < 1:
            logger.error(
                "Content Initializer registered no modules."
            )
            return False
        if lessons < 1:
            logger.error(
                "Content Initializer registered no lessons."
            )
            return False
        logger.info(
            (
                "Content Initializer health check: OK "
                "modules=%s chapters=%s lessons=%s"
            ),
            modules,
            chapters,
            lessons,
        )
        return True
    except Exception:
        logger.exception(
            "Content Initializer health check failed."
        )
        return False
# ==========================================================
# Core Initialization
# ==========================================================
def initialize_core() -> None:
    """
    Initialize all core systems.
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
    logger.info(
        "Initializing complete educational content..."
    )
    registry_result = (
        register_all_content()
    )
    logger.info(
        (
            "Educational content initialized: "
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
    if not run_content_initializer_health_check():
        raise RuntimeError(
            "Content Initializer health check failed."
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
    if not run_finance_health_checks():
        raise RuntimeError(
            "Finance health checks failed."
        )
    if not run_profile_health_check():
        raise RuntimeError(
            "Profile handlers health check failed."
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
    """
    Handle /start with mandatory channel membership check.
    """
    if update.message is None:
        return
    if not await is_member(
        update,
        context,
    ):
        await show_membership_required(
            update,
            context,
        )
        return
    registered = await register_telegram_user(
        update
    )
    if not registered:
        await update.message.reply_text(
            "❌ در ثبت اطلاعات شما مشکلی پیش آمد.\n\n"
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
    Handle /menu with mandatory channel membership check.
    """
    if update.message is None:
        return
    if not await is_member(
        update,
        context,
    ):
        await show_membership_required(
            update,
            context,
        )
        return
    registered = await register_telegram_user(
        update
    )
    if not registered:
        await update.message.reply_text(
            "❌ در ثبت اطلاعات شما مشکلی پیش آمد."
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
    Register users interacting with callback buttons.
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
# Membership Guard for Callback Menus
# ==========================================================
async def guarded_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Check mandatory channel membership before allowing
    access to the main menu callback router.
    """
    if not await is_member(
        update,
        context,
    ):
        await show_membership_required(
            update,
            context,
        )
        return
    await route_menu_callback(
        update,
        context,
    )
# ==========================================================
# Membership Guard for Profile
# ==========================================================
async def guarded_profile_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Check mandatory channel membership before allowing
    access to the user profile/dashboard.
    """
    if not await is_member(
        update,
        context,
    ):
        await show_membership_required(
            update,
            context,
        )
        return
    await route_profile_callback(
        update,
        context,
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
    Handler groups:
    Group -1:
        Auto User Registry.
    Group 0:
        Commands and module-specific callback routers.
    Group 1:
        Generic central menu router.
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
    # Callback Auto User Registry
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            callback_user_registry,
            pattern=r"^(?!check_membership$).*",
        ),
        group=-1,
    )
    # ======================================================
    # Commands
    # ======================================================
    application.add_handler(
        CommandHandler(
            "start",
            start,
        ),
        group=0,
    )
    application.add_handler(
        CommandHandler(
            "menu",
            menu_command,
        ),
        group=0,
    )
    application.add_handler(
        CommandHandler(
            "admin",
            admin_command,
        ),
        group=0,
    )
    # ======================================================
    # Membership callbacks
    # ======================================================
    application.add_handlers(
        membership_handlers,
        group=0,
    )
    # ======================================================
    # Profile callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            guarded_profile_callback,
            pattern=r"^menu_profile$",
        ),
        group=0,
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
        ),
        group=0,
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
        ),
        group=0,
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
        ),
        group=0,
    )
    # ======================================================
    # Psychology & Social Work callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_psychology_callback,
            pattern=(
                r"^("
                r"menu_psychology"
                r"|psychology_chapter:.+"
                r"|psychology_lesson:.+:.+"
                r"|psychology_complete:.+:.+"
                r"|psychology_quiz:.+:.+"
                r"|psychology_quiz_answer:.+"
                r"|psychology_quiz_cancel"
                r")$"
            ),
        ),
        group=0,
    )
    # ======================================================
    # Management callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            show_management_menu,
            pattern=r"^menu_management$",
        ),
        group=0,
    )
    application.add_handler(
        CallbackQueryHandler(
            show_management_chapter,
            pattern=r"^management_chapter:.+$",
        ),
        group=0,
    )
    application.add_handler(
        CallbackQueryHandler(
            show_management_lesson,
            pattern=r"^management_lesson:.+:.+$",
        ),
        group=0,
    )
    # ======================================================
    # Management Quiz Start
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            start_management_quiz,
            pattern=(
                r"^("
                r"management_quiz_start"
                r"|management_quiz:.+"
                r")$"
            ),
        ),
        group=0,
    )
    # ======================================================
    # Management Quiz Answers
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            answer_management_quiz,
            pattern=(
                r"^("
                r"management_quiz_answer:\d+"
                r"|quiz_answer:\d+"
                r")$"
            ),
        ),
        group=0,
    )
    # ======================================================
    # Management Quiz Cancellation
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            cancel_management_quiz,
            pattern=(
                r"^("
                r"management_quiz_stop"
                r"|quiz_cancel"
                r")$"
            ),
        ),
        group=0,
    )
    # ======================================================
    # Banking callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_banking_callback,
            pattern=(
                r"^("
                r"menu_banking"
                r"|banking_chapters"
                r"|banking_chapter:.+"
                r"|banking_lesson:.+:.+"
                r"|banking_complete:.+:.+"
                r"|banking_quiz:.+:.+"
                r"|banking_quiz_answer:.+:.+:\d+:\d+"
                r"|banking_quiz_cancel"
                r")$"
            ),
        ),
        group=0,
    )
    # ======================================================
    # Finance callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_finance_callback,
            pattern=(
                r"^("
                r"finance_menu"
                r"|finance_back"
                r"|finance_chapter:.+"
                r"|finance_lesson:.+"
                r")$"
            ),
        ),
        group=0,
    )
    # ======================================================
    # Random Quiz callbacks
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            route_random_quiz_callback,
            pattern=r"^random_quiz",
        ),
        group=0,
    )
    # ======================================================
    # Generic Central Menu Router
    # ======================================================
    application.add_handler(
        CallbackQueryHandler(
            guarded_menu_callback,
            pattern=r"^(?!check_membership$).*",
        ),
        group=1,
    )
    # ======================================================
    # Global Error Handler
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
    Run all local integration health checks.
    """
    try:
        if not run_core_health_checks():
            return False
        if not run_content_initializer_health_check():
            return False
        if not run_exam_health_checks():
            return False
        if not run_international_trade_health_checks():
            return False
        if not run_psychology_health_checks():
            return False
        if not run_banking_health_checks():
            return False
        if not run_finance_health_checks():
            return False
        if not run_profile_health_check():
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
        # ==================================================
        # Telegram Menu Button
        # ==================================================
        await application.bot.set_chat_menu_button(
            menu_button=MenuButtonCommands()
        )
        logger.info(
            "Telegram Menu Button configured successfully."
        )
        await application.start()
        logger.info(
            "Starting Telegram polling..."
        )
        if application.updater is None:
            raise RuntimeError(
                "Telegram updater is not available."
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
    """
    Start application.
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
