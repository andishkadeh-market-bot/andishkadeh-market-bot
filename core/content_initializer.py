"""
Andishkadeh Management & Market
Content Initializer

مسئول:
- کشف محتوای ماژول‌ها
- ثبت Module / Chapter / Lesson در Registry
- همگام‌سازی محتوا با SQLite
- پشتیبانی از ساختارهای قدیمی و جدید ماژول‌ها
- Health Check
- Statistics

نکته:
این فایل فقط مسئول Initialization و Registration محتواست.
منطق Telegram و UI در handlers.py قرار دارد.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any

from core.database import (
    init_database,
    upsert_module,
    upsert_chapter,
    upsert_lesson,
)

from core.registry import registry


# ==========================================================
# Module Configuration
# ==========================================================

CONTENT_PACKAGES: dict[str, str] = {
    "management": "modules.management.data",
    "banking": "modules.banking.data",
    "international_trade": "modules.international_trade.data",
    "psychology_socialwork": "modules.psychology.data",
    "finance": "modules.finance.data",
}


CONTENT_MODULE_IDS: tuple[str, ...] = (
    "management",
    "banking",
    "international_trade",
    "psychology_socialwork",
    "finance",
)


# ==========================================================
# Data Models
# ==========================================================

@dataclass
class DiscoveredLesson:
    lesson_id: str
    title: str
    module_id: str
    chapter_id: str
    content: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiscoveredChapter:
    chapter_id: str
    title: str
    module_id: str
    description: str = ""
    lessons: list[DiscoveredLesson] = field(
        default_factory=list
    )


@dataclass
class DiscoveredModule:
    module_id: str
    title: str
    description: str = ""
    chapters: list[DiscoveredChapter] = field(
        default_factory=list
    )


# ==========================================================
# Generic Helpers
# ==========================================================

def _safe_str(value: Any) -> str:
    if value is None:
        return ""

    try:
        return str(value).strip()
    except Exception:
        return ""


def _first_non_empty(
    data: dict[str, Any],
    keys: tuple[str, ...],
    default: str = "",
) -> str:
    for key in keys:
        value = data.get(key)

        if value is not None:
            text = _safe_str(value)

            if text:
                return text

    return default


def _normalize_id(
    value: Any,
) -> str:
    return _safe_str(value)


def _get_module_id(
    data_module: Any,
    fallback: str = "",
) -> str:
    value = getattr(
        data_module,
        "MODULE_ID",
        None,
    )

    if value:
        return _safe_str(value)

    return fallback


def _get_module_title(
    data_module: Any,
    fallback: str = "",
) -> str:
    value = getattr(
        data_module,
        "MODULE_TITLE",
        None,
    )

    if value:
        return _safe_str(value)

    return fallback


def _get_module_description(
    data_module: Any,
) -> str:
    value = getattr(
        data_module,
        "MODULE_DESCRIPTION",
        "",
    )

    return _safe_str(value)


# ==========================================================
# International Trade Extraction
# ==========================================================

def _extract_international_trade_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:
    """
    Extract International Trade content.

    Supported structure:

    INTERNATIONAL_TRADE_CURRICULUM
    INTERNATIONAL_TRADE_LESSONS
    INTERNATIONAL_TRADE_QUIZ_QUESTIONS

    This function intentionally handles the exact structure
    currently used by modules.international_trade.data.
    """

    module_id = _get_module_id(
        data_module,
        "international_trade",
    )

    module_title = _get_module_title(
        data_module,
        "🌍 تجارت بین‌الملل",
    )

    module_description = _get_module_description(
        data_module,
    )

    curriculum = getattr(
        data_module,
        "INTERNATIONAL_TRADE_CURRICULUM",
        None,
    )

    lessons_map = getattr(
        data_module,
        "INTERNATIONAL_TRADE_LESSONS",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        return None

    if not isinstance(
        lessons_map,
        dict,
    ):
        lessons_map = {}

    chapters: list[DiscoveredChapter] = []

    for chapter_item in curriculum:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = lessons_map.get(
            chapter_id,
            [],
        )

        if not isinstance(
            raw_lessons,
            list,
        ):
            raw_lessons = []

        lessons: list[DiscoveredLesson] = []

        for lesson_item in raw_lessons:

            if not isinstance(
                lesson_item,
                dict,
            ):
                continue

            lesson_id = _first_non_empty(
                lesson_item,
                (
                    "id",
                    "lesson_id",
                ),
            )

            if not lesson_id:
                continue

            lesson_title = _first_non_empty(
                lesson_item,
                (
                    "title",
                    "name",
                ),
                f"درس {lesson_id}",
            )

            lesson_content = _first_non_empty(
                lesson_item,
                (
                    "content",
                    "lesson_text",
                    "text",
                ),
            )

            lessons.append(
                DiscoveredLesson(
                    lesson_id=lesson_id,
                    title=lesson_title,
                    module_id=module_id,
                    chapter_id=chapter_id,
                    content=lesson_content,
                    metadata=dict(
                        lesson_item
                    ),
                )
            )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Finance Extraction
# ==========================================================

def _extract_finance_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:
    """
    Extract Finance content.

    Supported structure:

    CHAPTERS
    LESSONS

    Finance uses a separate chapter and lesson registry.
    """

    module_id = _get_module_id(
        data_module,
        "finance",
    )

    module_title = _get_module_title(
        data_module,
        "💳 مدیریت مالی",
    )

    module_description = _get_module_description(
        data_module,
    )

    chapters_data = getattr(
        data_module,
        "CHAPTERS",
        None,
    )

    lessons_data = getattr(
        data_module,
        "LESSONS",
        None,
    )

    if not isinstance(
        chapters_data,
        list,
    ):
        return None

    if not isinstance(
        lessons_data,
        list,
    ):
        lessons_data = []

    lessons_by_chapter: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    for lesson in lessons_data:

        if not isinstance(
            lesson,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            lesson,
            (
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        lessons_by_chapter.setdefault(
            chapter_id,
            [],
        ).append(
            lesson
        )

    chapters: list[DiscoveredChapter] = []

    for chapter_item in chapters_data:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = lessons_by_chapter.get(
            chapter_id,
            [],
        )

        lessons: list[DiscoveredLesson] = []

        for lesson_item in raw_lessons:

            lesson_id = _first_non_empty(
                lesson_item,
                (
                    "id",
                    "lesson_id",
                ),
            )

            if not lesson_id:
                continue

            lesson_title = _first_non_empty(
                lesson_item,
                (
                    "title",
                    "name",
                ),
                f"درس {lesson_id}",
            )

            lesson_content = _first_non_empty(
                lesson_item,
                (
                    "content",
                    "lesson_text",
                    "text",
                ),
            )

            lessons.append(
                DiscoveredLesson(
                    lesson_id=lesson_id,
                    title=lesson_title,
                    module_id=module_id,
                    chapter_id=chapter_id,
                    content=lesson_content,
                    metadata=dict(
                        lesson_item
                    ),
                )
            )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Management Extraction
# ==========================================================

def _extract_management_curriculum(
    data_module: Any,
) -> DiscoveredModule | None:
    """
    Extract Management curriculum.

    Supported structure:

    MANAGEMENT_CURRICULUM
    MANAGEMENT_CHAPTERS
    MANAGEMENT_LESSONS
    """

    module_id = _get_module_id(
        data_module,
        "management",
    )

    module_title = _get_module_title(
        data_module,
        "📚 آموزش مدیریت",
    )

    module_description = _get_module_description(
        data_module,
    )

    curriculum = getattr(
        data_module,
        "MANAGEMENT_CURRICULUM",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        curriculum = getattr(
            data_module,
            "MANAGEMENT_CHAPTERS",
            None,
        )

    lessons_map = getattr(
        data_module,
        "MANAGEMENT_LESSONS",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        return None

    if not isinstance(
        lessons_map,
        dict,
    ):
        lessons_map = {}

    chapters: list[DiscoveredChapter] = []

    for chapter_item in curriculum:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
                "original_chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        chapter_description = _first_non_empty(
            chapter_item,
            (
                "description",
                "desc",
            ),
        )

        raw_lessons = lessons_map.get(
            chapter_id,
            [],
        )

        if not isinstance(
            raw_lessons,
            list,
        ):
            raw_lessons = []

        lessons: list[DiscoveredLesson] = []

        for lesson_item in raw_lessons:

            if not isinstance(
                lesson_item,
                dict,
            ):
                continue

            lesson_id = _first_non_empty(
                lesson_item,
                (
                    "id",
                    "lesson_id",
                ),
            )

            if not lesson_id:
                continue

            lesson_title = _first_non_empty(
                lesson_item,
                (
                    "title",
                    "name",
                ),
                f"درس {lesson_id}",
            )

            lesson_content = _first_non_empty(
                lesson_item,
                (
                    "content",
                    "lesson_text",
                    "text",
                ),
            )

            lessons.append(
                DiscoveredLesson(
                    lesson_id=lesson_id,
                    title=lesson_title,
                    module_id=module_id,
                    chapter_id=chapter_id,
                    content=lesson_content,
                    metadata=dict(
                        lesson_item
                    ),
                )
            )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=chapter_description,
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Generic Extraction
# ==========================================================

def _extract_generic_curriculum(
    data_module: Any,
    fallback_module_id: str,
) -> DiscoveredModule | None:
    """
    Generic extractor for modules whose data structure follows
    a standard curriculum/chapter/lesson pattern.
    """

    module_id = _get_module_id(
        data_module,
        fallback_module_id,
    )

    module_title = _get_module_title(
        data_module,
        module_id,
    )

    module_description = _get_module_description(
        data_module,
    )

    curriculum = getattr(
        data_module,
        "CURRICULUM",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        curriculum = getattr(
            data_module,
            "CHAPTERS",
            None,
        )

    lessons_map = getattr(
        data_module,
        "LESSONS",
        None,
    )

    if not isinstance(
        curriculum,
        list,
    ):
        return None

    if not isinstance(
        lessons_map,
        dict,
    ):
        lessons_map = {}

    chapters: list[DiscoveredChapter] = []

    for chapter_item in curriculum:

        if not isinstance(
            chapter_item,
            dict,
        ):
            continue

        chapter_id = _first_non_empty(
            chapter_item,
            (
                "id",
                "chapter_id",
            ),
        )

        if not chapter_id:
            continue

        chapter_title = _first_non_empty(
            chapter_item,
            (
                "title",
                "name",
            ),
            f"فصل {chapter_id}",
        )

        raw_lessons = lessons_map.get(
            chapter_id,
            [],
        )

        if not isinstance(
            raw_lessons,
            list,
        ):
            raw_lessons = []

        lessons: list[DiscoveredLesson] = []

        for lesson_item in raw_lessons:

            if not isinstance(
                lesson_item,
                dict,
            ):
                continue

            lesson_id = _first_non_empty(
                lesson_item,
                (
                    "id",
                    "lesson_id",
                ),
            )

            if not lesson_id:
                continue

            lesson_title = _first_non_empty(
                lesson_item,
                (
                    "title",
                    "name",
                ),
                f"درس {lesson_id}",
            )

            lesson_content = _first_non_empty(
                lesson_item,
                (
                    "content",
                    "lesson_text",
                    "text",
                ),
            )

            lessons.append(
                DiscoveredLesson(
                    lesson_id=lesson_id,
                    title=lesson_title,
                    module_id=module_id,
                    chapter_id=chapter_id,
                    content=lesson_content,
                    metadata=dict(
                        lesson_item
                    ),
                )
            )

        chapters.append(
            DiscoveredChapter(
                chapter_id=chapter_id,
                title=chapter_title,
                module_id=module_id,
                description=_first_non_empty(
                    chapter_item,
                    (
                        "description",
                        "desc",
                    ),
                ),
                lessons=lessons,
            )
        )

    if not chapters:
        return None

    return DiscoveredModule(
        module_id=module_id,
        title=module_title,
        description=module_description,
        chapters=chapters,
    )


# ==========================================================
# Module Discovery
# ==========================================================

def discover_module(
    module_id: str,
    package_path: str,
) -> DiscoveredModule | None:
    """
    Import and discover one module.
    """

    try:
        data_module = import_module(
            package_path
        )
    except Exception:
        return None

    normalized_module_id = _safe_str(
        module_id
    )

    # ------------------------------------------------------
    # International Trade
    # ------------------------------------------------------

    if normalized_module_id == "international_trade":
        return _extract_international_trade_curriculum(
            data_module
        )

    # ------------------------------------------------------
    # Finance
    # ------------------------------------------------------

    if normalized_module_id == "finance":
        return _extract_finance_curriculum(
            data_module
        )

    # ------------------------------------------------------
    # Management
    # ------------------------------------------------------

    if normalized_module_id == "management":
        return _extract_management_curriculum(
            data_module
        )

    # ------------------------------------------------------
    # Generic modules
    # ------------------------------------------------------

    return _extract_generic_curriculum(
        data_module,
        normalized_module_id,
    )


# ==========================================================
# Database Synchronization
# ==========================================================

def _sync_module_to_database(
    module: DiscoveredModule,
) -> bool:
    try:

        upsert_module(
            module.module_id,
            module.title,
            module.description,
        )

        return True

    except TypeError:

        try:
            upsert_module(
                module_id=module.module_id,
                title=module.title,
                description=module.description,
            )

            return True

        except Exception:
            return False

    except Exception:
        return False


def _sync_chapter_to_database(
    chapter: DiscoveredChapter,
) -> bool:
    try:

        upsert_chapter(
            chapter.module_id,
            chapter.chapter_id,
            chapter.title,
        )

        return True

    except TypeError:

        try:
            upsert_chapter(
                module_id=chapter.module_id,
                chapter_id=chapter.chapter_id,
                title=chapter.title,
            )

            return True

        except Exception:
            return False

    except Exception:
        return False


def _sync_lesson_to_database(
    lesson: DiscoveredLesson,
) -> bool:
    try:

        upsert_lesson(
            lesson.module_id,
            lesson.chapter_id,
            lesson.lesson_id,
            lesson.title,
        )

        return True

    except TypeError:

        try:
            upsert_lesson(
                module_id=lesson.module_id,
                chapter_id=lesson.chapter_id,
                lesson_id=lesson.lesson_id,
                title=lesson.title,
            )

            return True

        except Exception:
            return False

    except Exception:
        return False


# ==========================================================
# Registry Registration
# ==========================================================

def _register_module(
    module: DiscoveredModule,
) -> int:
    """
    Register a complete module in Registry.

    Returns number of registered lessons.
    """

    try:

        registry.register_module(
            module_id=module.module_id,
            title=module.title,
            description=module.description,
        )

    except TypeError:

        registry.register_module(
            module.module_id,
            module.title,
            module.description,
        )

    lesson_count = 0

    for chapter in module.chapters:

        try:

            registry.register_chapter(
                module_id=chapter.module_id,
                chapter_id=chapter.chapter_id,
                title=chapter.title,
                description=chapter.description,
            )

        except TypeError:

            registry.register_chapter(
                chapter.module_id,
                chapter.chapter_id,
                chapter.title,
                chapter.description,
            )

        for lesson in chapter.lessons:

            try:

                registry.register_lesson(
                    module_id=lesson.module_id,
                    chapter_id=lesson.chapter_id,
                    lesson_id=lesson.lesson_id,
                    title=lesson.title,
                )

            except TypeError:

                registry.register_lesson(
                    lesson.module_id,
                    lesson.chapter_id,
                    lesson.lesson_id,
                    lesson.title,
                )

            lesson_count += 1

    return lesson_count


# ==========================================================
# Initialize One Module
# ==========================================================

def initialize_content(
    module_id: str,
    package_path: str,
) -> dict[str, Any]:
    """
    Initialize one content module.

    Returns:
        {
            "module_id": ...,
            "success": bool,
            "chapters": int,
            "lessons": int,
        }
    """

    result: dict[str, Any] = {
        "module_id": module_id,
        "success": False,
        "chapters": 0,
        "lessons": 0,
    }

    discovered = discover_module(
        module_id,
        package_path,
    )

    if discovered is None:
        return result

    try:

        lesson_count = _register_module(
            discovered
        )

        result["chapters"] = len(
            discovered.chapters
        )

        result["lessons"] = lesson_count

        # --------------------------------------------------
        # Database Synchronization
        # --------------------------------------------------

        _sync_module_to_database(
            discovered
        )

        for chapter in discovered.chapters:

            _sync_chapter_to_database(
                chapter
            )

            for lesson in chapter.lessons:

                _sync_lesson_to_database(
                    lesson
                )

        result["success"] = True

        return result

    except Exception:
        return result


# ==========================================================
# Initialize All Modules
# ==========================================================

def initialize_all_content() -> dict[str, Any]:
    """
    Initialize all configured content modules.

    This function is intentionally tolerant:
    failure in one module does not prevent other modules
    from being initialized.
    """

    init_database()

    results: dict[str, Any] = {
        "success": True,
        "modules": 0,
        "chapters": 0,
        "lessons": 0,
        "errors": 0,
        "details": {},
    }

    for module_id in CONTENT_MODULE_IDS:

        package_path = CONTENT_PACKAGES.get(
            module_id
        )

        if not package_path:
            results["errors"] += 1

            results["details"][module_id] = {
                "success": False,
                "chapters": 0,
                "lessons": 0,
                "error": "Package path not configured.",
            }

            continue

        module_result = initialize_content(
            module_id,
            package_path,
        )

        results["details"][module_id] = (
            module_result
        )

        if module_result.get(
            "success"
        ):
            results["modules"] += 1

            results["chapters"] += int(
                module_result.get(
                    "chapters",
                    0,
                )
            )

            results["lessons"] += int(
                module_result.get(
                    "lessons",
                    0,
                )
            )

        else:
            results["errors"] += 1

    if results["modules"] == 0:
        results["success"] = False

    return results


# ==========================================================
# Registry Statistics
# ==========================================================

def get_registry_statistics() -> dict[str, int]:
    """
    Return current Registry statistics.
    """

    try:

        statistics = registry.statistics()

        return {
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

    except Exception:

        return {
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
        }


# ==========================================================
# Content Health Check
# ==========================================================

def content_health_check() -> bool:
    """
    Check whether content has been initialized correctly.
    """

    try:

        statistics = get_registry_statistics()

        if statistics["modules"] < 1:
            return False

        if statistics["chapters"] < 1:
            return False

        if statistics["lessons"] < 1:
            return False

        return True

    except Exception:
        return False


def run_content_initializer_health_check() -> bool:
    """
    Compatibility alias used by bot.py.
    """

    return content_health_check()


# ==========================================================
# Detailed Health Report
# ==========================================================

def get_content_health_report() -> dict[str, Any]:
    """
    Return detailed initialization report.
    """

    statistics = get_registry_statistics()

    module_details: dict[str, Any] = {}

    for module_id in CONTENT_MODULE_IDS:

        try:

            module = registry.get_module(
                module_id
            )

            if module is None:

                module_details[module_id] = {
                    "registered": False,
                    "chapters": 0,
                    "lessons": 0,
                }

                continue

            chapter_count = registry.chapter_count(
                module_id
            )

            lesson_count = registry.lesson_count(
                module_id
            )

            module_details[module_id] = {
                "registered": True,
                "chapters": int(
                    chapter_count
                ),
                "lessons": int(
                    lesson_count
                ),
            }

        except Exception:

            module_details[module_id] = {
                "registered": False,
                "chapters": 0,
                "lessons": 0,
            }

    return {
        "healthy": content_health_check(),
        "statistics": statistics,
        "modules": module_details,
    }


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "CONTENT_PACKAGES",
    "CONTENT_MODULE_IDS",

    "DiscoveredLesson",
    "DiscoveredChapter",
    "DiscoveredModule",

    "discover_module",

    "initialize_content",
    "initialize_all_content",

    "get_registry_statistics",

    "content_health_check",
    "run_content_initializer_health_check",

    "get_content_health_report",
]


# ==========================================================
# Local Test
# ==========================================================

if __name__ == "__main__":

    result = initialize_all_content()

    print(
        "======================================"
    )

    print(
        "Content Initializer"
    )

    print(
        "======================================"
    )

    print(
        f"Success: {result.get('success')}"
    )

    print(
        f"Modules: {result.get('modules')}"
    )

    print(
        f"Chapters: {result.get('chapters')}"
    )

    print(
        f"Lessons: {result.get('lessons')}"
    )

    print(
        f"Errors: {result.get('errors')}"
    )

    print(
        "--------------------------------------"
    )

    for module_id, details in (
        result.get(
            "details",
            {},
        ).items()
    ):

        print(
            f"{module_id}: "
            f"success={details.get('success')} "
            f"chapters={details.get('chapters')} "
            f"lessons={details.get('lessons')}"
        )

    print(
        "--------------------------------------"
    )

    print(
        "Registry:"
    )

    print(
        get_registry_statistics()
    )

    print(
        "Health:"
    )

    print(
        content_health_check()
    )

    print(
        "======================================"
    )
