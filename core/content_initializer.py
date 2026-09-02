"""
Content Initializer for Andishkadeh Management & Market.
This module:
- discovers educational content from project modules
- registers modules/chapters/lessons in the central registry
- stores discovered content in the database
- provides health/statistics helpers
It does NOT handle Telegram UI.
"""
from __future__ import annotations
import importlib
import inspect
import logging
import pkgutil
from dataclasses import dataclass, field
from typing import Any, Iterable
from core.database import (
    init_database,
    upsert_module,
    upsert_chapter,
    upsert_lesson,
)
from core.registry import registry
logger = logging.getLogger(__name__)
# ============================================================================
# Configuration
# ============================================================================
CONTENT_PACKAGES = (
    "modules.management",
    "modules.banking",
    "modules.international_trade",
    "modules.psychology",
    "modules.finance",
)
CONTENT_MODULE_IDS = {
    "modules.management": "management",
    "modules.banking": "banking",
    "modules.international_trade": "international_trade",
    "modules.psychology": "psychology_socialwork",
    "modules.finance": "finance",
}
# ============================================================================
# Data models
# ============================================================================
@dataclass
class DiscoveredLesson:
    module_id: str
    chapter_id: str
    lesson_id: str
    title: str
    description: str = ""
    data: dict[str, Any] = field(default_factory=dict)
@dataclass
class DiscoveredChapter:
    module_id: str
    chapter_id: str
    title: str
    lessons: list[DiscoveredLesson] = field(
        default_factory=list
    )
    data: dict[str, Any] = field(default_factory=dict)
@dataclass
class DiscoveredModule:
    module_id: str
    title: str
    chapters: list[DiscoveredChapter] = field(
        default_factory=list
    )
    data: dict[str, Any] = field(default_factory=dict)
# ============================================================================
# Generic helpers
# ============================================================================
def _clean_text(
    value: Any,
    default: str = "",
) -> str:
    if value is None:
        return default
    if isinstance(value, str):
        text = value.strip()
        return text if text else default
    text = str(value).strip()
    return text if text else default
def _as_dict(
    value: Any,
) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if hasattr(value, "__dict__"):
        try:
            return dict(vars(value))
        except Exception:
            return {}
    return {}
def _first_value(
    data: dict[str, Any],
    keys: Iterable[str],
    default: Any = None,
) -> Any:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return default
def _normalize_identifier(
    value: Any,
    fallback: str,
) -> str:
    text = _clean_text(
        value,
        fallback,
    )
    replacements = {
        " ": "_",
        "-": "_",
        "/": "_",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip("_") or fallback
# ============================================================================
# Import helpers
# ============================================================================
def _import_optional(
    name: str,
) -> Any | None:
    try:
        return importlib.import_module(name)
    except Exception as exc:
        logger.warning(
            "Could not import %s: %s",
            name,
            exc,
        )
        return None
def _iter_package_modules(
    package_name: str,
) -> list[Any]:
    package = _import_optional(
        package_name
    )
    if package is None:
        return []
    modules: list[Any] = [package]
    package_path = getattr(
        package,
        "__path__",
        None,
    )
    if not package_path:
        return modules
    try:
        for item in pkgutil.walk_packages(
            package_path,
            package.__name__ + ".",
        ):
            imported = _import_optional(
                item.name
            )
            if imported is not None:
                modules.append(imported)
    except Exception as exc:
        logger.warning(
            "Could not scan package %s: %s",
            package_name,
            exc,
        )
    return modules
def _find_data_modules(
    package_name: str,
) -> list[Any]:
    modules = _iter_package_modules(
        package_name
    )
    result: list[Any] = []
    for module in modules:
        module_name = getattr(
            module,
            "__name__",
            "",
        )
        if (
            module_name.endswith(".data")
            or module_name.endswith(".content")
            or module_name.endswith(".lessons")
            or module_name.endswith(".curriculum")
            or module_name == package_name
        ):
            result.append(module)
    return result or modules
# ============================================================================
# Module metadata
# ============================================================================
def _extract_module_metadata(
    module: Any,
    module_id: str,
) -> tuple[str, dict[str, Any]]:
    data = _as_dict(module)
    title = _first_value(
        data,
        (
            "MODULE_TITLE",
            "module_title",
            "MODULE_NAME",
            "module_name",
            "TITLE",
            "title",
            "NAME",
            "name",
        ),
        module_id,
    )
    return (
        _clean_text(
            title,
            module_id,
        ),
        data,
    )
# ============================================================================
# Management curriculum
# ============================================================================
def _extract_management_curriculum(
    module_id: str = "management",
) -> list[DiscoveredChapter]:
    """
    Extract Management curriculum from:
        MANAGEMENT_CURRICULUM
        MANAGEMENT_LESSONS
    MANAGEMENT_CURRICULUM:
        [
            {
                "id": "chapter_01",
                "title": "...",
            },
            ...
        ]
    MANAGEMENT_LESSONS:
        {
            "chapter_01": [
                {
                    "id": "lesson_01_01",
                    "title": "...",
                    ...
                },
                ...
            ]
        }
    """
    package_name = "modules.management"
    chapters: list[DiscoveredChapter] = []
    data_modules = _find_data_modules(
        package_name
    )
    for module in data_modules:
        raw_curriculum = getattr(
            module,
            "MANAGEMENT_CURRICULUM",
            None,
        )
        raw_lessons = getattr(
            module,
            "MANAGEMENT_LESSONS",
            None,
        )
        if not isinstance(
            raw_curriculum,
            (list, tuple),
        ):
            continue
        if not isinstance(
            raw_lessons,
            dict,
        ):
            raw_lessons = {}
        for chapter_index, chapter_value in enumerate(
            raw_curriculum,
            start=1,
        ):
            chapter_data = _as_dict(
                chapter_value
            )
            if not chapter_data:
                continue
            chapter_id_value = _first_value(
                chapter_data,
                (
                    "chapter_id",
                    "id",
                    "chapter_number",
                    "chapter_no",
                    "number",
                ),
                f"chapter_{chapter_index:02d}",
            )
            original_chapter_id = _clean_text(
                chapter_id_value,
                f"chapter_{chapter_index:02d}",
            )
            chapter_id = _normalize_identifier(
                original_chapter_id,
                f"chapter_{chapter_index:02d}",
            )
            chapter_title = _clean_text(
                _first_value(
                    chapter_data,
                    (
                        "chapter_title",
                        "title",
                        "name",
                        "subject",
                    ),
                    f"فصل {chapter_index}",
                ),
                f"فصل {chapter_index}",
            )
            lesson_values = raw_lessons.get(
                original_chapter_id
            )
            if lesson_values is None:
                lesson_values = raw_lessons.get(
                    chapter_id,
                    [],
                )
            if not isinstance(
                lesson_values,
                (list, tuple, set),
            ):
                lesson_values = []
            lessons: list[
                DiscoveredLesson
            ] = []
            for lesson_index, lesson_value in enumerate(
                lesson_values,
                start=1,
            ):
                lesson_data = _as_dict(
                    lesson_value
                )
                if not lesson_data:
                    continue
                lesson_id_value = _first_value(
                    lesson_data,
                    (
                        "lesson_id",
                        "id",
                        "lesson_number",
                        "lesson_no",
                        "number",
                    ),
                    f"lesson_{chapter_index:02d}_{lesson_index:02d}",
                )
                lesson_id = _normalize_identifier(
                    lesson_id_value,
                    f"lesson_{chapter_index:02d}_{lesson_index:02d}",
                )
                lesson_title = _clean_text(
                    _first_value(
                        lesson_data,
                        (
                            "lesson_title",
                            "title",
                            "name",
                            "subject",
                        ),
                        f"درس {lesson_index}",
                    ),
                    f"درس {lesson_index}",
                )
                description = _clean_text(
                    _first_value(
                        lesson_data,
                        (
                            "description",
                            "summary",
                            "intro",
                        ),
                        "",
                    ),
                )
                lessons.append(
                    DiscoveredLesson(
                        module_id=module_id,
                        chapter_id=chapter_id,
                        lesson_id=lesson_id,
                        title=lesson_title,
                        description=description,
                        data=lesson_data,
                    )
                )
            chapters.append(
                DiscoveredChapter(
                    module_id=module_id,
                    chapter_id=chapter_id,
                    title=chapter_title,
                    lessons=lessons,
                    data=chapter_data,
                )
            )
    return chapters
# ============================================================================
# Finance curriculum
# ============================================================================
def _extract_finance_curriculum(
    module_id: str = "finance",
) -> list[DiscoveredChapter]:
    """
    Extract Finance curriculum from:
        CHAPTERS
        LESSONS
    CHAPTERS is a list.
    LESSONS is a list where each lesson contains
    a chapter_id field.
    """
    package_name = "modules.finance"
    chapters: list[DiscoveredChapter] = []
    data_modules = _find_data_modules(
        package_name
    )
    for module in data_modules:
        raw_chapters = getattr(
            module,
            "CHAPTERS",
            None,
        )
        raw_lessons = getattr(
            module,
            "LESSONS",
            None,
        )
        if not isinstance(
            raw_chapters,
            (list, tuple),
        ):
            continue
        if not isinstance(
            raw_lessons,
            (list, tuple),
        ):
            raw_lessons = []
        lessons_by_chapter: dict[
            str,
            list[DiscoveredLesson],
        ] = {}
        for lesson_index, lesson_value in enumerate(
            raw_lessons,
            start=1,
        ):
            lesson_data = _as_dict(
                lesson_value
            )
            if not lesson_data:
                continue
            chapter_id_value = _first_value(
                lesson_data,
                (
                    "chapter_id",
                    "chapter",
                    "chapter_number",
                    "chapter_no",
                ),
            )
            if chapter_id_value is None:
                continue
            chapter_id = _normalize_identifier(
                chapter_id_value,
                f"chapter_{lesson_index:02d}",
            )
            lesson_id_value = _first_value(
                lesson_data,
                (
                    "lesson_id",
                    "id",
                    "lesson_number",
                    "lesson_no",
                    "number",
                ),
                f"lesson_{lesson_index:02d}",
            )
            lesson_id = _normalize_identifier(
                lesson_id_value,
                f"lesson_{lesson_index:02d}",
            )
            lesson_title = _clean_text(
                _first_value(
                    lesson_data,
                    (
                        "lesson_title",
                        "title",
                        "name",
                        "subject",
                    ),
                    f"درس {lesson_index}",
                ),
                f"درس {lesson_index}",
            )
            description = _clean_text(
                _first_value(
                    lesson_data,
                    (
                        "description",
                        "summary",
                        "intro",
                    ),
                    "",
                ),
            )
            lessons_by_chapter.setdefault(
                chapter_id,
                [],
            ).append(
                DiscoveredLesson(
                    module_id=module_id,
                    chapter_id=chapter_id,
                    lesson_id=lesson_id,
                    title=lesson_title,
                    description=description,
                    data=lesson_data,
                )
            )
        for chapter_index, chapter_value in enumerate(
            raw_chapters,
            start=1,
        ):
            chapter_data = _as_dict(
                chapter_value
            )
            if not chapter_data:
                continue
            chapter_id_value = _first_value(
                chapter_data,
                (
                    "chapter_id",
                    "id",
                    "chapter_number",
                    "chapter_no",
                    "number",
                ),
                f"chapter_{chapter_index:02d}",
            )
            chapter_id = _normalize_identifier(
                chapter_id_value,
                f"chapter_{chapter_index:02d}",
            )
            chapter_title = _clean_text(
                _first_value(
                    chapter_data,
                    (
                        "chapter_title",
                        "title",
                        "name",
                        "subject",
                    ),
                    f"فصل {chapter_index}",
                ),
                f"فصل {chapter_index}",
            )
            lessons = lessons_by_chapter.get(
                chapter_id,
                [],
            )
            chapters.append(
                DiscoveredChapter(
                    module_id=module_id,
                    chapter_id=chapter_id,
                    title=chapter_title,
                    lessons=lessons,
                    data=chapter_data,
                )
            )
    return chapters
# ============================================================================
# Generic curriculum extraction
# ============================================================================
def _extract_chapters_from_module(
    module: Any,
    module_id: str,
) -> list[DiscoveredChapter]:
    """
    Generic extractor for modules that expose
    chapters directly as dictionaries/lists.
    """
    chapters: list[
        DiscoveredChapter
    ] = []
    public_names: list[str] = []
    try:
        public_names = [
            name
            for name in dir(module)
            if not name.startswith("_")
        ]
    except Exception:
        return chapters
    for name in public_names:
        try:
            value = getattr(
                module,
                name,
            )
        except Exception:
            continue
        if (
            inspect.ismodule(value)
            or inspect.isfunction(value)
            or inspect.isclass(value)
        ):
            continue
        if isinstance(value, dict):
            candidates = list(
                value.values()
            )
        elif isinstance(
            value,
            (list, tuple, set),
        ):
            candidates = list(value)
        else:
            continue
        for chapter_index, candidate in enumerate(
            candidates,
            start=1,
        ):
            chapter_data = _as_dict(
                candidate
            )
            if not chapter_data:
                continue
            if not any(
                key in chapter_data
                for key in (
                    "chapter_id",
                    "chapter",
                    "chapter_number",
                    "chapter_no",
                    "chapter_title",
                    "chapters",
                    "lessons",
                )
            ):
                continue
            chapter_id_value = _first_value(
                chapter_data,
                (
                    "chapter_id",
                    "id",
                    "chapter_number",
                    "chapter_no",
                    "number",
                ),
                f"chapter_{chapter_index:02d}",
            )
            chapter_id = _normalize_identifier(
                chapter_id_value,
                f"chapter_{chapter_index:02d}",
            )
            chapter_title = _clean_text(
                _first_value(
                    chapter_data,
                    (
                        "chapter_title",
                        "title",
                        "name",
                        "subject",
                    ),
                    f"فصل {chapter_index}",
                ),
                f"فصل {chapter_index}",
            )
            lessons_data = _first_value(
                chapter_data,
                (
                    "lessons",
                    "lesson_list",
                    "items",
                    "contents",
                ),
                [],
            )
            if isinstance(
                lessons_data,
                dict,
            ):
                lesson_candidates = list(
                    lessons_data.values()
                )
            elif isinstance(
                lessons_data,
                (list, tuple, set),
            ):
                lesson_candidates = list(
                    lessons_data
                )
            else:
                lesson_candidates = []
            lessons: list[
                DiscoveredLesson
            ] = []
            for lesson_index, lesson_value in enumerate(
                lesson_candidates,
                start=1,
            ):
                lesson_data = _as_dict(
                    lesson_value
                )
                if not lesson_data:
                    continue
                lesson_id_value = _first_value(
                    lesson_data,
                    (
                        "lesson_id",
                        "id",
                        "lesson_number",
                        "lesson_no",
                        "number",
                    ),
                    f"lesson_{chapter_index:02d}_{lesson_index:02d}",
                )
                lesson_id = _normalize_identifier(
                    lesson_id_value,
                    f"lesson_{chapter_index:02d}_{lesson_index:02d}",
                )
                lesson_title = _clean_text(
                    _first_value(
                        lesson_data,
                        (
                            "lesson_title",
                            "title",
                            "name",
                            "subject",
                        ),
                        f"درس {lesson_index}",
                    ),
                    f"درس {lesson_index}",
                )
                lessons.append(
                    DiscoveredLesson(
                        module_id=module_id,
                        chapter_id=chapter_id,
                        lesson_id=lesson_id,
                        title=lesson_title,
                        description=_clean_text(
                            _first_value(
                                lesson_data,
                                (
                                    "description",
                                    "summary",
                                    "intro",
                                ),
                                "",
                            )
                        ),
                        data=lesson_data,
                    )
                )
            chapters.append(
                DiscoveredChapter(
                    module_id=module_id,
                    chapter_id=chapter_id,
                    title=chapter_title,
                    lessons=lessons,
                    data=chapter_data,
                )
            )
    # Remove duplicate chapters while preserving order.
    unique: list[
        DiscoveredChapter
    ] = []
    seen: set[
        tuple[str, str]
    ] = set()
    for chapter in chapters:
        key = (
            chapter.module_id,
            chapter.chapter_id,
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(chapter)
    return unique
# ============================================================================
# Database synchronization
# ============================================================================
def _sync_module_to_database(
    module_id: str,
    title: str,
) -> None:
    try:
        upsert_module(
            module_id,
            title,
        )
    except TypeError:
        try:
            upsert_module(
                module_id=module_id,
                title=title,
            )
        except Exception:
            logger.exception(
                "Could not sync module to database: %s",
                module_id,
            )
def _sync_chapter_to_database(
    module_id: str,
    chapter_id: str,
    title: str,
) -> None:
    try:
        upsert_chapter(
            module_id,
            chapter_id,
            title,
        )
    except TypeError:
        try:
            upsert_chapter(
                module_id=module_id,
                chapter_id=chapter_id,
                title=title,
            )
        except Exception:
            logger.exception(
                "Could not sync chapter to database: %s/%s",
                module_id,
                chapter_id,
            )
def _sync_lesson_to_database(
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    title: str,
) -> None:
    try:
        upsert_lesson(
            module_id,
            chapter_id,
            lesson_id,
            title,
        )
    except TypeError:
        try:
            upsert_lesson(
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=title,
            )
        except Exception:
            logger.exception(
                "Could not sync lesson to database: %s/%s/%s",
                module_id,
                chapter_id,
                lesson_id,
            )
# ============================================================================
# Registry registration
# ============================================================================
def _register_module(
    module_id: str,
    title: str,
) -> None:
    try:
        registry.register_module(
            module_id=module_id,
            title=title,
        )
    except TypeError:
        registry.register_module(
            module_id,
            title,
        )
def _register_chapter(
    module_id: str,
    chapter_id: str,
    title: str,
) -> None:
    try:
        registry.register_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
            title=title,
        )
    except TypeError:
        registry.register_chapter(
            module_id,
            chapter_id,
            title,
        )
def _register_lesson(
    module_id: str,
    chapter_id: str,
    lesson_id: str,
    title: str,
) -> None:
    try:
        registry.register_lesson(
            module_id=module_id,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            title=title,
        )
    except TypeError:
        registry.register_lesson(
            module_id,
            chapter_id,
            lesson_id,
            title,
        )
# ============================================================================
# Main initialization
# ============================================================================
def initialize_content() -> dict[str, Any]:
    """
    Discover and register all supported educational content.
    """
    init_database()
    discovered_modules: list[
        DiscoveredModule
    ] = []
    for package_name in CONTENT_PACKAGES:
        module_id = CONTENT_MODULE_IDS.get(
            package_name,
            package_name.split(".")[-1],
        )
        data_modules = _find_data_modules(
            package_name
        )
        module_title = module_id
        module_data: dict[
            str,
            Any,
        ] = {}
        for data_module in data_modules:
            title, metadata = (
                _extract_module_metadata(
                    data_module,
                    module_id,
                )
            )
            if (
                title
                and title != module_id
            ):
                module_title = title
            module_data.update(
                metadata
            )
        # ------------------------------------------------------------
        # Dedicated curriculum extraction
        # ------------------------------------------------------------
        if module_id == "management":
            chapters = (
                _extract_management_curriculum(
                    module_id
                )
            )
        elif module_id == "finance":
            chapters = (
                _extract_finance_curriculum(
                    module_id
                )
            )
        else:
            chapters = []
            for data_module in data_modules:
                extracted = (
                    _extract_chapters_from_module(
                        data_module,
                        module_id,
                    )
                )
                for chapter in extracted:
                    if not any(
                        existing.chapter_id
                        == chapter.chapter_id
                        for existing in chapters
                    ):
                        chapters.append(
                            chapter
                        )
        discovered_modules.append(
            DiscoveredModule(
                module_id=module_id,
                title=module_title,
                chapters=chapters,
                data=module_data,
            )
        )
    # ------------------------------------------------------------
    # Register everything
    # ------------------------------------------------------------
    total_modules = 0
    total_chapters = 0
    total_lessons = 0
    for module in discovered_modules:
        _register_module(
            module.module_id,
            module.title,
        )
        _sync_module_to_database(
            module.module_id,
            module.title,
        )
        total_modules += 1
        for chapter in module.chapters:
            _register_chapter(
                module.module_id,
                chapter.chapter_id,
                chapter.title,
            )
            _sync_chapter_to_database(
                module.module_id,
                chapter.chapter_id,
                chapter.title,
            )
            total_chapters += 1
            for lesson in chapter.lessons:
                _register_lesson(
                    module.module_id,
                    chapter.chapter_id,
                    lesson.lesson_id,
                    lesson.title,
                )
                _sync_lesson_to_database(
                    module.module_id,
                    chapter.chapter_id,
                    lesson.lesson_id,
                    lesson.title,
                )
                total_lessons += 1
    result = {
        "status": "ok",
        "modules": total_modules,
        "chapters": total_chapters,
        "lessons": total_lessons,
    }
    logger.info(
        "Content initialization completed: %s",
        result,
    )
    return result
def initialize_all_content() -> dict[str, Any]:
    """
    Public entry point used by bot.py.
    """
    try:
        return initialize_content()
    except Exception as exc:
        logger.exception(
            "Content initialization failed."
        )
        return {
            "status": "error",
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
            "error": str(exc),
        }
# ============================================================================
# Health check
# ============================================================================
def content_initializer_health_check() -> dict[str, Any]:
    """
    Verify that the content initializer can access
    the registry and database.
    """
    result: dict[str, Any] = {
        "module": "core.content_initializer",
        "status": "ok",
        "details": {},
    }
    try:
        init_database()
        statistics = registry.statistics()
        result["details"][
            "registry"
        ] = statistics
        if not isinstance(
            statistics,
            dict,
        ):
            result["status"] = "error"
            result["details"][
                "error"
            ] = "Registry statistics are invalid."
    except Exception as exc:
        result["status"] = "error"
        result["details"][
            "error"
        ] = str(exc)
    return result
def get_content_statistics() -> dict[str, Any]:
    """
    Return current registry statistics.
    """
    try:
        statistics = registry.statistics()
        if isinstance(
            statistics,
            dict,
        ):
            return statistics
        return {
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
        }
    except Exception as exc:
        logger.exception(
            "Could not read content statistics."
        )
        return {
            "status": "error",
            "modules": 0,
            "chapters": 0,
            "lessons": 0,
            "error": str(exc),
        }
# ============================================================================
# Exported API
# ============================================================================
__all__ = [
    "CONTENT_PACKAGES",
    "CONTENT_MODULE_IDS",
    "DiscoveredLesson",
    "DiscoveredChapter",
    "DiscoveredModule",
    "initialize_content",
    "initialize_all_content",
    "content_initializer_health_check",
    "get_content_statistics",
]
# ============================================================================
# Smoke test
# ============================================================================
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )
    print(
        "Starting content initializer..."
    )
    result = initialize_all_content()
    print(
        "Initialization result:"
    )
    print(result)
    print(
        "\nCurrent content statistics:"
    )
    print(
        get_content_statistics()
    )
    print(
        "\nHealth check:"
    )
    print(
        content_initializer_health_check()
    )
