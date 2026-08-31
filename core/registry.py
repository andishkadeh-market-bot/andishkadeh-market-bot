"""
Automatic content registry for Andishkadeh Management & Market.

Responsibilities:
- Register modules
- Register chapters
- Register lessons
- Keep an in-memory registry
- Persist registered content into SQLite
- Export registered content
- Provide lookup and count helpers

The Registry keeps the existing public API simple so existing
handlers and curriculum code can continue using it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.database import (
    init_database,
    upsert_module,
    upsert_chapter,
    upsert_lesson,
)


# ==========================================================
# Data Models
# ==========================================================


@dataclass
class LessonRecord:
    """Registered lesson."""

    lesson_id: str
    title: str
    module_id: str
    chapter_id: str

    data: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ChapterRecord:
    """Registered chapter."""

    chapter_id: str
    title: str
    module_id: str

    lessons: dict[
        str,
        LessonRecord,
    ] = field(
        default_factory=dict
    )


@dataclass
class ModuleRecord:
    """Registered module."""

    module_id: str
    title: str

    chapters: dict[
        str,
        ChapterRecord,
    ] = field(
        default_factory=dict
    )


# ==========================================================
# Registry
# ==========================================================


class Registry:
    """
    Central registry for educational content.

    Content is maintained in memory and persisted to SQLite.

    SQLite is used only as the persistent storage layer.
    Telegram handlers do not need to know how the data is stored.
    """

    def __init__(
        self,
        auto_initialize_database: bool = True,
    ) -> None:

        self.modules: dict[
            str,
            ModuleRecord,
        ] = {}

        self.auto_initialize_database = (
            auto_initialize_database
        )

        if self.auto_initialize_database:
            init_database()

    # ======================================================
    # Internal database helpers
    # ======================================================

    def _ensure_database(self) -> None:
        """Ensure the SQLite database exists."""

        if self.auto_initialize_database:
            init_database()

    # ======================================================
    # Module
    # ======================================================

    def register_module(
        self,
        module_id: str,
        title: str,
    ) -> ModuleRecord:
        """
        Register or update a module.

        The module is stored both in memory and SQLite.
        """

        if not module_id:
            raise ValueError(
                "module_id cannot be empty."
            )

        if not title:
            raise ValueError(
                "module title cannot be empty."
            )

        module = self.modules.get(
            module_id
        )

        if module is None:

            module = ModuleRecord(
                module_id=module_id,
                title=title,
            )

            self.modules[
                module_id
            ] = module

        else:

            module.title = title

        self._ensure_database()

        upsert_module(
            module_id=module_id,
            title=title,
        )

        return module

    # ======================================================
    # Chapter
    # ======================================================

    def register_chapter(
        self,
        module_id: str,
        chapter_id: str,
        title: str,
    ) -> ChapterRecord:
        """
        Register or update a chapter.

        If the module does not exist yet, it is created
        automatically.
        """

        if not module_id:
            raise ValueError(
                "module_id cannot be empty."
            )

        if not chapter_id:
            raise ValueError(
                "chapter_id cannot be empty."
            )

        if not title:
            raise ValueError(
                "chapter title cannot be empty."
            )

        if module_id not in self.modules:

            self.register_module(
                module_id=module_id,
                title=module_id,
            )

        module = self.modules[
            module_id
        ]

        chapter = module.chapters.get(
            chapter_id
        )

        if chapter is None:

            chapter = ChapterRecord(
                chapter_id=chapter_id,
                title=title,
                module_id=module_id,
            )

            module.chapters[
                chapter_id
            ] = chapter

        else:

            chapter.title = title

        self._ensure_database()

        upsert_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
            title=title,
        )

        return chapter

    # ======================================================
    # Lesson
    # ======================================================

    def register_lesson(
        self,
        module_id: str,
        chapter_id: str,
        lesson_id: str,
        title: str,
        data: dict[str, Any] | None = None,
    ) -> LessonRecord:
        """
        Register or update a lesson.

        The lesson is automatically persisted to SQLite.
        """

        if not module_id:
            raise ValueError(
                "module_id cannot be empty."
            )

        if not chapter_id:
            raise ValueError(
                "chapter_id cannot be empty."
            )

        if not lesson_id:
            raise ValueError(
                "lesson_id cannot be empty."
            )

        if not title:
            raise ValueError(
                "lesson title cannot be empty."
            )

        chapter = self.register_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
            title=chapter_id,
        )

        lesson = chapter.lessons.get(
            lesson_id
        )

        if lesson is None:

            lesson = LessonRecord(
                lesson_id=lesson_id,
                title=title,
                module_id=module_id,
                chapter_id=chapter_id,
                data=data or {},
            )

            chapter.lessons[
                lesson_id
            ] = lesson

        else:

            lesson.title = title

            if data is not None:
                lesson.data = data

        self._ensure_database()

        upsert_lesson(
            module_id=module_id,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            title=title,
        )

        return lesson

    # ======================================================
    # Bulk registration
    # ======================================================

    def register_many_lessons(
        self,
        module_id: str,
        chapter_id: str,
        lessons: list[
            dict[str, Any]
        ],
    ) -> list[LessonRecord]:
        """
        Register multiple lessons.

        Each lesson dictionary must contain:
            lesson_id
            title

        Optional:
            data
        """

        registered: list[
            LessonRecord
        ] = []

        for lesson_data in lessons:

            lesson_id = lesson_data.get(
                "lesson_id"
            )

            title = lesson_data.get(
                "title"
            )

            data = lesson_data.get(
                "data"
            )

            if lesson_id is None:
                raise ValueError(
                    "Each lesson must contain "
                    "'lesson_id'."
                )

            if title is None:
                raise ValueError(
                    "Each lesson must contain "
                    "'title'."
                )

            lesson = self.register_lesson(
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                title=title,
                data=data,
            )

            registered.append(
                lesson
            )

        return registered

    # ======================================================
    # Lookup
    # ======================================================

    def get_module(
        self,
        module_id: str,
    ) -> ModuleRecord | None:
        """Return a registered module."""

        return self.modules.get(
            module_id
        )

    def get_chapter(
        self,
        module_id: str,
        chapter_id: str,
    ) -> ChapterRecord | None:
        """Return a registered chapter."""

        module = self.get_module(
            module_id
        )

        if module is None:
            return None

        return module.chapters.get(
            chapter_id
        )

    def get_lesson(
        self,
        module_id: str,
        chapter_id: str,
        lesson_id: str,
    ) -> LessonRecord | None:
        """Return a registered lesson."""

        chapter = self.get_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
        )

        if chapter is None:
            return None

        return chapter.lessons.get(
            lesson_id
        )

    # ======================================================
    # Existence helpers
    # ======================================================

    def has_module(
        self,
        module_id: str,
    ) -> bool:
        """Check whether a module exists."""

        return (
            module_id in self.modules
        )

    def has_chapter(
        self,
        module_id: str,
        chapter_id: str,
    ) -> bool:
        """Check whether a chapter exists."""

        return (
            self.get_chapter(
                module_id,
                chapter_id,
            )
            is not None
        )

    def has_lesson(
        self,
        module_id: str,
        chapter_id: str,
        lesson_id: str,
    ) -> bool:
        """Check whether a lesson exists."""

        return (
            self.get_lesson(
                module_id,
                chapter_id,
                lesson_id,
            )
            is not None
        )

    # ======================================================
    # Counts
    # ======================================================

    def module_count(self) -> int:
        """Return number of registered modules."""

        return len(
            self.modules
        )

    def chapter_count(
        self,
        module_id: str,
    ) -> int:
        """Return number of chapters in a module."""

        module = self.get_module(
            module_id
        )

        if module is None:
            return 0

        return len(
            module.chapters
        )

    def lesson_count(
        self,
        module_id: str,
        chapter_id: str | None = None,
    ) -> int:
        """
        Return number of registered lessons.

        If chapter_id is supplied, only that chapter is counted.
        """

        module = self.get_module(
            module_id
        )

        if module is None:
            return 0

        if chapter_id is not None:

            chapter = module.chapters.get(
                chapter_id
            )

            if chapter is None:
                return 0

            return len(
                chapter.lessons
            )

        return sum(
            len(chapter.lessons)
            for chapter
            in module.chapters.values()
        )

    # ======================================================
    # Listing
    # ======================================================

    def list_modules(
        self,
    ) -> list[ModuleRecord]:
        """Return all registered modules."""

        return list(
            self.modules.values()
        )

    def list_chapters(
        self,
        module_id: str,
    ) -> list[ChapterRecord]:
        """Return all chapters of a module."""

        module = self.get_module(
            module_id
        )

        if module is None:
            return []

        return list(
            module.chapters.values()
        )

    def list_lessons(
        self,
        module_id: str,
        chapter_id: str,
    ) -> list[LessonRecord]:
        """Return all lessons of a chapter."""

        chapter = self.get_chapter(
            module_id,
            chapter_id,
        )

        if chapter is None:
            return []

        return list(
            chapter.lessons.values()
        )

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return basic registry statistics.
        """

        modules = self.module_count()

        chapters = sum(
            len(module.chapters)
            for module
            in self.modules.values()
        )

        lessons = sum(
            len(chapter.lessons)
            for module
            in self.modules.values()
            for chapter
            in module.chapters.values()
        )

        return {
            "modules": modules,
            "chapters": chapters,
            "lessons": lessons,
        }

    # ======================================================
    # Export
    # ======================================================

    def export(
        self,
    ) -> dict[str, Any]:
        """
        Export the complete registry as dictionaries.
        """

        result: dict[
            str,
            Any,
        ] = {}

        for module_id, module in (
            self.modules.items()
        ):

            result[module_id] = {
                "id": module.module_id,
                "title": module.title,
                "chapters": {},
            }

            for chapter_id, chapter in (
                module.chapters.items()
            ):

                result[
                    module_id
                ][
                    "chapters"
                ][chapter_id] = {
                    "id": chapter.chapter_id,
                    "title": chapter.title,
                    "lessons": {},
                }

                for lesson_id, lesson in (
                    chapter.lessons.items()
                ):

                    result[
                        module_id
                    ][
                        "chapters"
                    ][chapter_id][
                        "lessons"
                    ][lesson_id] = {
                        "id": lesson.lesson_id,
                        "title": lesson.title,
                        "data": lesson.data,
                    }

        return result

    # ======================================================
    # Clear
    # ======================================================

    def clear_memory(
        self,
    ) -> None:
        """
        Clear only the in-memory registry.

        SQLite data is intentionally preserved.
        """

        self.modules.clear()


# ==========================================================
# Global Registry
# ==========================================================

registry = Registry()
