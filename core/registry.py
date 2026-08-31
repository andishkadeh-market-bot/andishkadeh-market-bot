"""
Automatic registry for Andishkadeh Management & Market.

This module provides a lightweight registry for:
- Modules
- Chapters
- Lessons
- Quizzes

The registry is intentionally independent from Telegram handlers
and database storage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    lessons: dict[str, LessonRecord] = field(
        default_factory=dict
    )


@dataclass
class ModuleRecord:
    """Registered module."""

    module_id: str
    title: str
    chapters: dict[str, ChapterRecord] = field(
        default_factory=dict
    )


# ==========================================================
# Registry
# ==========================================================


class Registry:
    """
    Central registry for educational content.

    The registry keeps content metadata in memory.
    Persistent storage will be handled later by SQLite.
    """

    def __init__(self) -> None:
        self.modules: dict[
            str,
            ModuleRecord,
        ] = {}

    # ======================================================
    # Module
    # ======================================================

    def register_module(
        self,
        module_id: str,
        title: str,
    ) -> ModuleRecord:
        """Register or update a module."""

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

            self.modules[module_id] = module

        else:
            module.title = title

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
        """Register or update a chapter."""

        if module_id not in self.modules:
            self.register_module(
                module_id,
                module_id,
            )

        if not chapter_id:
            raise ValueError(
                "chapter_id cannot be empty."
            )

        if not title:
            raise ValueError(
                "chapter title cannot be empty."
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
        """Register or update a lesson."""

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

        return lesson

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
            module_id,
            chapter_id,
        )

        if chapter is None:
            return None

        return chapter.lessons.get(
            lesson_id
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
        """Return number of chapters."""

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
        """Return number of registered lessons."""

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
            for chapter in module.chapters.values()
        )

    # ======================================================
    # Export
    # ======================================================

    def export(self) -> dict[str, Any]:
        """Export registry contents as dictionaries."""

        result: dict[str, Any] = {}

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
                result[module_id][
                    "chapters"
                ][chapter_id] = {
                    "id": chapter.chapter_id,
                    "title": chapter.title,
                    "lessons": {},
                }

                for lesson_id, lesson in (
                    chapter.lessons.items()
                ):
                    result[module_id][
                        "chapters"
                    ][chapter_id][
                        "lessons"
                    ][lesson_id] = {
                        "id": lesson.lesson_id,
                        "title": lesson.title,
                        "data": lesson.data,
                    }

        return result


# ==========================================================
# Global Registry
# ==========================================================


registry = Registry()
