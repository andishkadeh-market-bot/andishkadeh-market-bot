"""
Central content initializer for Andishkadeh Management & Market.

Responsibilities:
- Initialize the SQLite database.
- Discover educational content from module packages.
- Register modules, chapters and lessons in the central Registry.
- Persist discovered content into SQLite through core.registry.
- Keep initialization idempotent.
- Provide health-check information.

This module does NOT:
- Handle Telegram updates.
- Modify bot.py.
- Modify core.database.py.
- Modify core.registry.py.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from dataclasses import dataclass
from typing import Any

from core.database import init_database
from core.registry import (
    registry,
    register_chapter,
    register_lesson,
    register_module,
)


# ==========================================================
# Configuration
# ==========================================================

CONTENT_PACKAGES = (
    "modules.management",
    "modules.banking",
    "modules.international_trade",
    "modules.psychology",
)

CONTENT_MODULE_IDS = {
    "modules.management": "management",
    "modules.banking": "banking",
    "modules.international_trade": "international_trade",
    "modules.psychology": "psychology_socialwork",
}


# ==========================================================
# Internal Data Models
# ==========================================================

@dataclass
class DiscoveredLesson:
    module_id: str
    module_title: str
    chapter_id: str
    chapter_title: str
    lesson_id: str
    lesson_title: str
    data: dict[str, Any]


@dataclass
class DiscoveredChapter:
    module_id: str
    module_title: str
    chapter_id: str
    chapter_title: str
    data: dict[str, Any]


@dataclass
class DiscoveredModule:
    module_id: str
    module_title: str
    description: str
    data: dict[str, Any]


# ==========================================================
# Generic Helpers
# ==========================================================

def _clean_text(value: Any, default: str = "") -> str:
    """Normalize a value into clean text."""
    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def _as_dict(value: Any) -> dict[str, Any] | None:
    """Return value when it is a dictionary."""
    if isinstance(value, dict):
        return value

    return None


def _first_value(
    data: dict[str, Any],
    keys: tuple[str, ...],
    default: Any = None,
) -> Any:
    """Return the first non-empty value from a dictionary."""
    for key in keys:
        if key not in data:
            continue

        value = data.get(key)

        if value is None:
            continue

        if isinstance(value, str) and not value.strip():
            continue

        return value

    return default


def _normalize_identifier(value: Any, fallback: str) -> str:
    """
    Normalize identifiers while preserving meaningful source IDs.
    """
    text = _clean_text(value)

    if text:
        return text

    return fallback


def _looks_like_lesson(data: dict[str, Any]) -> bool:
    """
    Detect whether a dictionary appears to describe a lesson.

    We deliberately require stronger evidence than just `id` + `title`
    because chapter dictionaries and quiz questions may use the same keys.
    """
    lesson_markers = (
        "lesson_id",
        "lesson_title",
        "lesson",
        "content",
        "lesson_content",
        "lesson_text",
        "body",
        "example",
        "specialized_notes",
        "special_points",
        "exam_notes",
        "exam_points",
    )

    if not any(key in data for key in lesson_markers):
        return False

    if "questions" in data and len(data) <= 5:
        return False

    return True


def _looks_like_chapter(data: dict[str, Any]) -> bool:
    """Detect whether a dictionary appears to describe a chapter."""
    chapter_markers = (
        "chapter_id",
        "chapter_title",
        "chapters",
        "lessons",
        "lesson_list",
    )

    if any(key in data for key in chapter_markers):
        return True

    identifier = _first_value(
        data,
        ("id", "code", "slug"),
    )

    title = _first_value(
        data,
        ("title", "name", "chapter_name"),
    )

    if identifier and title:
        return True

    return False


def _extract_module_metadata(
    package_name: str,
    package_data: dict[str, Any] | None,
) -> DiscoveredModule:
    """Extract module metadata from a package or data module."""
    package_data = package_data or {}

    module_id = _first_value(
        package_data,
        (
            "MODULE_ID",
            "module_id",
        ),
        CONTENT_MODULE_IDS.get(package_name, package_name),
    )

    module_title = _first_value(
        package_data,
        (
            "MODULE_TITLE",
            "module_title",
            "TITLE",
        ),
        module_id,
    )

    description = _first_value(
        package_data,
        (
            "MODULE_DESCRIPTION",
            "module_description",
            "DESCRIPTION",
        ),
        "",
    )

    return DiscoveredModule(
        module_id=_normalize_identifier(module_id, package_name),
        module_title=_clean_text(module_title, module_id),
        description=_clean_text(description),
        data=package_data,
    )


# ==========================================================
# Module Discovery
# ==========================================================

def _import_optional(module_name: str) -> Any | None:
    """Import a module without making optional discovery fatal."""
    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def _iter_package_modules(package_name: str):
    """
    Recursively discover Python modules under a package.

    This allows the initializer to work with structures such as:

        modules.management.lessons.lesson_01
        modules.management.lessons.lesson_02

    as well as data.py based modules.
    """
    package = _import_optional(package_name)

    if package is None:
        return

    yield package

    package_path = getattr(package, "__path__", None)

    if not package_path:
        return

    prefix = package.__name__ + "."

    for module_info in pkgutil.walk_packages(
        package_path,
        prefix,
    ):
        module = _import_optional(module_info.name)

        if module is not None:
            yield module


def _find_data_modules(package_name: str) -> list[Any]:
    """Find likely data/content modules inside a module package."""
    candidates: list[Any] = []

    for module in _iter_package_modules(package_name):
        module_name = getattr(module, "__name__", "")

        if module_name.endswith(".data"):
            candidates.append(module)
            continue

        if module_name.endswith(".curriculum"):
            candidates.append(module)
            continue

        if module_name.endswith(".content"):
            candidates.append(module)
            continue

        if module_name.endswith(".psychology_socialwork"):
            candidates.append(module)

    return candidates


# ==========================================================
# Recursive Content Extraction
# ==========================================================

def _iter_dicts(
    value: Any,
    visited: set[int] | None = None,
):
    """
    Recursively yield dictionaries from nested Python structures.

    Cyclic structures are protected against.
    """
    if visited is None:
        visited = set()

    object_id = id(value)

    if object_id in visited:
        return

    visited.add(object_id)

    if isinstance(value, dict):
        yield value

        for child in value.values():
            yield from _iter_dicts(child, visited)

        return

    if isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _iter_dicts(child, visited)


def _collect_public_values(module: Any) -> list[Any]:
    """Collect safe public values from a Python module."""
    values: list[Any] = []

    try:
        attributes = vars(module)
    except Exception:
        return values

    for name, value in attributes.items():
        if name.startswith("_"):
            continue

        if inspect.ismodule(value):
            continue

        if inspect.isfunction(value):
            continue

        if inspect.isclass(value):
            continue

        values.append(value)

    return values


# ==========================================================
# Chapter Extraction
# ==========================================================

def _extract_chapters_from_module(
    module: Any,
    discovered_module: DiscoveredModule,
) -> list[DiscoveredChapter]:
    """Extract chapter records from a content module."""
    chapters: list[DiscoveredChapter] = []
    seen: set[tuple[str, str]] = set()

    values = _collect_public_values(module)

    for value in values:
        for data in _iter_dicts(value):
            chapter_id_raw = _first_value(
                data,
                (
                    "chapter_id",
                    "chapterId",
                ),
            )

            chapter_title_raw = _first_value(
                data,
                (
                    "chapter_title",
                    "chapterTitle",
                    "chapter_name",
                ),
            )

            identifier = _first_value(
                data,
                (
                    "id",
                    "code",
                    "slug",
                ),
            )

            title = _first_value(
                data,
                (
                    "title",
                    "name",
                ),
            )

            chapter_id = chapter_id_raw or identifier
            chapter_title = chapter_title_raw or title

            if not chapter_id or not chapter_title:
                continue

            if _looks_like_lesson(data):
                continue

            if not _looks_like_chapter(data):
                continue

            chapter_id = _normalize_identifier(
                chapter_id,
                "chapter",
            )

            chapter_title = _clean_text(
                chapter_title,
                chapter_id,
            )

            key = (
                discovered_module.module_id,
                chapter_id,
            )

            if key in seen:
                continue

            seen.add(key)

            chapters.append(
                DiscoveredChapter(
                    module_id=discovered_module.module_id,
                    module_title=discovered_module.module_title,
                    chapter_id=chapter_id,
                    chapter_title=chapter_title,
                    data=data,
                )
            )

    return chapters


# ==========================================================
# Lesson Extraction
# ==========================================================

def _extract_lessons_from_module(
    module: Any,
    discovered_module: DiscoveredModule,
) -> list[DiscoveredLesson]:
    """Extract lesson records from a content module."""
    lessons: list[DiscoveredLesson] = []
    seen: set[tuple[str, str, str]] = set()

    values = _collect_public_values(module)

    current_chapter_id = "chapter_01"
    current_chapter_title = "فصل اول"

    for value in values:
        if isinstance(value, dict):
            possible_chapter_id = _first_value(
                value,
                (
                    "chapter_id",
                    "chapterId",
                ),
            )

            possible_chapter_title = _first_value(
                value,
                (
                    "chapter_title",
                    "chapterTitle",
                    "chapter_name",
                ),
            )

            if possible_chapter_id:
                current_chapter_id = _clean_text(
                    possible_chapter_id,
                    current_chapter_id,
                )

            if possible_chapter_title:
                current_chapter_title = _clean_text(
                    possible_chapter_title,
                    current_chapter_title,
                )

        for data in _iter_dicts(value):
            if not _looks_like_lesson(data):
                continue

            lesson_id_raw = _first_value(
                data,
                (
                    "lesson_id",
                    "lessonId",
                ),
            )

            lesson_title_raw = _first_value(
                data,
                (
                    "lesson_title",
                    "lessonTitle",
                ),
            )

            identifier = _first_value(
                data,
                (
                    "id",
                    "code",
                    "slug",
                ),
            )

            title = _first_value(
                data,
                (
                    "title",
                    "name",
                ),
            )

            lesson_id = lesson_id_raw or identifier
            lesson_title = lesson_title_raw or title

            if not lesson_id or not lesson_title:
                continue

            chapter_id = _first_value(
                data,
                (
                    "chapter_id",
                    "chapterId",
                ),
                current_chapter_id,
            )

            chapter_title = _first_value(
                data,
                (
                    "chapter_title",
                    "chapterTitle",
                    "chapter_name",
                ),
                current_chapter_title,
            )

            lesson_id = _normalize_identifier(
                lesson_id,
                "lesson",
            )

            lesson_title = _clean_text(
                lesson_title,
                lesson_id,
            )

            chapter_id = _normalize_identifier(
                chapter_id,
                "chapter_01",
            )

            chapter_title = _clean_text(
                chapter_title,
                chapter_id,
            )

            key = (
                discovered_module.module_id,
                chapter_id,
                lesson_id,
            )

            if key in seen:
                continue

            seen.add(key)

            lessons.append(
                DiscoveredLesson(
                    module_id=discovered_module.module_id,
                    module_title=discovered_module.module_title,
                    chapter_id=chapter_id,
                    chapter_title=chapter_title,
                    lesson_id=lesson_id,
                    lesson_title=lesson_title,
                    data=data,
                )
            )

    return lessons


# ==========================================================
# Special Curriculum Support
# ==========================================================

def _extract_management_curriculum(
    module: Any,
    discovered_module: DiscoveredModule,
) -> tuple[list[DiscoveredChapter], list[DiscoveredLesson]]:
    """
    Support management/curriculum.py explicitly.

    The management curriculum is structured around chapters, while
    detailed lessons may live in separate files.
    """
    chapters: list[DiscoveredChapter] = []
    lessons: list[DiscoveredLesson] = []

    curriculum = getattr(
        module,
        "MANAGEMENT_CURRICULUM",
        None,
    )

    if curriculum is None:
        curriculum = getattr(
            module,
            "CURRICULUM",
            None,
        )

    if not isinstance(curriculum, list):
        return chapters, lessons

    for chapter in curriculum:
        if not isinstance(chapter, dict):
            continue

        chapter_id = _first_value(
            chapter,
            ("id", "chapter_id", "code"),
        )

        chapter_title = _first_value(
            chapter,
            ("title", "name", "chapter_title"),
        )

        if not chapter_id or not chapter_title:
            continue

        chapter_id = _clean_text(chapter_id)
        chapter_title = _clean_text(
            chapter_title,
            chapter_id,
        )

        chapters.append(
            DiscoveredChapter(
                module_id=discovered_module.module_id,
                module_title=discovered_module.module_title,
                chapter_id=chapter_id,
                chapter_title=chapter_title,
                data=chapter,
            )
        )

        chapter_lessons = _first_value(
            chapter,
            (
                "lessons",
                "lesson_list",
                "items",
            ),
            [],
        )

        if not isinstance(chapter_lessons, list):
            continue

        for index, lesson in enumerate(chapter_lessons, start=1):
            if not isinstance(lesson, dict):
                continue

            lesson_id = _first_value(
                lesson,
                (
                    "id",
                    "lesson_id",
                    "code",
                    "slug",
                ),
                f"{chapter_id}_lesson_{index:02d}",
            )

            lesson_title = _first_value(
                lesson,
                (
                    "title",
                    "name",
                    "lesson_title",
                ),
                f"درس {index}",
            )

            lessons.append(
                DiscoveredLesson(
                    module_id=discovered_module.module_id,
                    module_title=discovered_module.module_title,
                    chapter_id=chapter_id,
                    chapter_title=chapter_title,
                    lesson_id=_clean_text(
                        lesson_id,
                        f"{chapter_id}_lesson_{index:02d}",
                    ),
                    lesson_title=_clean_text(
                        lesson_title,
                        f"درس {index}",
                    ),
                    data=lesson,
                )
            )

    return chapters, lessons


# ==========================================================
# Registration
# ==========================================================

def _register_module(
    discovered_module: DiscoveredModule,
) -> None:
    """Register a module in the central Registry."""
    try:
        register_module(
            module_id=discovered_module.module_id,
            title=discovered_module.module_title,
            description=discovered_module.description,
        )
    except TypeError:
        register_module(
            discovered_module.module_id,
            discovered_module.module_title,
        )


def _register_chapter(
    chapter: DiscoveredChapter,
) -> None:
    """Register a chapter in Registry and SQLite."""
    try:
        register_chapter(
            module_id=chapter.module_id,
            chapter_id=chapter.chapter_id,
            title=chapter.chapter_title,
        )
    except TypeError:
        register_chapter(
            chapter.module_id,
            chapter.chapter_id,
            chapter.chapter_title,
        )


def _register_lesson(
    lesson: DiscoveredLesson,
) -> None:
    """Register a lesson in Registry and SQLite."""
    try:
        register_lesson(
            module_id=lesson.module_id,
            chapter_id=lesson.chapter_id,
            lesson_id=lesson.lesson_id,
            title=lesson.lesson_title,
        )
    except TypeError:
        register_lesson(
            lesson.module_id,
            lesson.chapter_id,
            lesson.lesson_id,
            lesson.lesson_title,
        )


# ==========================================================
# Main Initialization
# ==========================================================

def initialize_content() -> dict[str, Any]:
    """
    Discover and register all educational content.

    The operation is designed to be idempotent.
    Running it repeatedly should not create duplicate logical records.
    """
    init_database()

    result: dict[str, Any] = {
        "status": "ok",
        "modules": 0,
        "chapters": 0,
        "lessons": 0,
        "module_details": {},
        "errors": [],
    }

    for package_name in CONTENT_PACKAGES:
        module_result: dict[str, Any] = {
            "status": "ok",
            "chapters": 0,
            "lessons": 0,
            "sources": [],
        }

        try:
            data_modules = _find_data_modules(package_name)

            if not data_modules:
                module_result["status"] = "warning"
                module_result["sources"] = []
                result["module_details"][package_name] = module_result
                continue

            primary_data_module = data_modules[0]

            package_data = {}

            for key in (
                "MODULE_ID",
                "MODULE_TITLE",
                "MODULE_DESCRIPTION",
                "MODULE_VERSION",
            ):
                if hasattr(primary_data_module, key):
                    package_data[key] = getattr(
                        primary_data_module,
                        key,
                    )

            discovered_module = _extract_module_metadata(
                package_name,
                package_data,
            )

            _register_module(discovered_module)

            result["modules"] += 1

            all_chapters: list[DiscoveredChapter] = []
            all_lessons: list[DiscoveredLesson] = []

            for source_module in data_modules:
                module_name = getattr(
                    source_module,
                    "__name__",
                    "unknown",
                )

                module_result["sources"].append(
                    module_name
                )

                if (
                    discovered_module.module_id == "management"
                    and module_name.endswith(".curriculum")
                ):
                    special_chapters, special_lessons = (
                        _extract_management_curriculum(
                            source_module,
                            discovered_module,
                        )
                    )

                    all_chapters.extend(
                        special_chapters
                    )

                    all_lessons.extend(
                        special_lessons
                    )

                generic_chapters = (
                    _extract_chapters_from_module(
                        source_module,
                        discovered_module,
                    )
                )

                generic_lessons = (
                    _extract_lessons_from_module(
                        source_module,
                        discovered_module,
                    )
                )

                all_chapters.extend(generic_chapters)
                all_lessons.extend(generic_lessons)

            unique_chapters: dict[
                tuple[str, str],
                DiscoveredChapter,
            ] = {}

            for chapter in all_chapters:
                unique_chapters[
                    (
                        chapter.module_id,
                        chapter.chapter_id,
                    )
                ] = chapter

            unique_lessons: dict[
                tuple[str, str, str],
                DiscoveredLesson,
            ] = {}

            for lesson in all_lessons:
                unique_lessons[
                    (
                        lesson.module_id,
                        lesson.chapter_id,
                        lesson.lesson_id,
                    )
                ] = lesson

            for chapter in unique_chapters.values():
                _register_chapter(chapter)

            for lesson in unique_lessons.values():
                _register_lesson(lesson)

            module_result["chapters"] = len(
                unique_chapters
            )

            module_result["lessons"] = len(
                unique_lessons
            )

            result["chapters"] += len(
                unique_chapters
            )

            result["lessons"] += len(
                unique_lessons
            )

            result["module_details"][
                package_name
            ] = module_result

        except Exception as exc:
            result["status"] = "warning"

            module_result["status"] = "error"
            module_result["error"] = str(exc)

            result["module_details"][
                package_name
            ] = module_result

            result["errors"].append(
                {
                    "package": package_name,
                    "error": str(exc),
                }
            )

    return result


# ==========================================================
# Aliases
# ==========================================================

def initialize_all_content() -> dict[str, Any]:
    """Compatibility alias for initialize_content()."""
    return initialize_content()


def content_initializer_health_check() -> dict[str, Any]:
    """
    Run a lightweight content initialization health check.
    """
    result: dict[str, Any] = {
        "module": "core.content_initializer",
        "status": "ok",
    }

    try:
        initialization = initialize_content()

        result["initialization"] = initialization

        if initialization.get("errors"):
            result["status"] = "warning"

    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)

    return result


def get_content_statistics() -> dict[str, Any]:
    """
    Return current Registry statistics.

    This is intentionally read-only.
    """
    try:
        statistics = registry.statistics()

        if isinstance(statistics, dict):
            return statistics

        return {
            "status": "ok",
            "registry_statistics": statistics,
        }

    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
        }


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "CONTENT_PACKAGES",
    "initialize_content",
    "initialize_all_content",
    "content_initializer_health_check",
    "get_content_statistics",
]


# ==========================================================
# Local Smoke Test
# ==========================================================

if __name__ == "__main__":
    output = initialize_content()

    print("Content initializer")
    print("===================")
    print(f"Status: {output.get('status')}")
    print(f"Modules: {output.get('modules')}")
    print(f"Chapters: {output.get('chapters')}")
    print(f"Lessons: {output.get('lessons')}")

    if output.get("errors"):
        print()
        print("Errors:")
        for error in output["errors"]:
            print(
                f"- {error.get('package')}: "
                f"{error.get('error')}"
            )
