"""
Automatic content registry for Andishkadeh Management & Market.

Responsibilities:
- Register modules
- Register chapters
- Register lessons
- Keep an in-memory registry
- Persist registered content into SQLite
- Provide lookup helpers
- Provide existence helpers
- Provide count helpers
- Provide listing helpers
- Export registry data
- Provide registry statistics

The Registry is intentionally independent from Telegram handlers.

SQLite is used as the persistent storage layer through core.database.
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

    description: str = ""

    lessons: dict[str, LessonRecord] = field(
        default_factory=dict
    )


@dataclass
class ModuleRecord:
    """Registered module."""

    module_id: str
    title: str

    description: str = ""

    chapters: dict[str, ChapterRecord] = field(
        default_factory=dict
    )


# ==========================================================
# Registry
# ==========================================================

class Registry:
    """
    Central registry for educational content.

    Content exists in two layers:

    1. In-memory registry
    2. SQLite persistent storage

    Telegram handlers can use the registry without knowing
    anything about SQLite.
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
    # Internal helpers
    # ======================================================

    @staticmethod
    def _validate_identifier(
        value: str,
        field_name: str,
    ) -> None:

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_title(
        title: str,
        field_name: str,
    ) -> None:

        if not isinstance(title, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not title.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _normalize_description(
        description: Any,
    ) -> str:

        if description is None:
            return ""

        if not isinstance(description, str):
            return str(description)

        return description.strip()

    @staticmethod
    def _normalize_lesson_data(
        data: Any,
    ) -> dict[str, Any]:

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise TypeError(
                "lesson data must be a dictionary."
            )

        return dict(data)

    def _ensure_database(self) -> None:

        if self.auto_initialize_database:
            init_database()

    # ======================================================
    # Module registration
    # ======================================================

    def register_module(
        self,
        module_id: str,
        title: str,
        description: str = "",
    ) -> ModuleRecord:

        self._validate_identifier(
            module_id,
            "module_id",
        )

        self._validate_title(
            title,
            "module title",
        )

        description = self._normalize_description(
            description
        )

        module = self.modules.get(
            module_id
        )

        if module is None:

            module = ModuleRecord(
                module_id=module_id,
                title=title,
                description=description,
            )

            self.modules[
                module_id
            ] = module

        else:

            module.title = title

            if description:
                module.description = description

        self._ensure_database()

        try:

            upsert_module(
                module_id=module_id,
                title=title,
                description=description,
            )

        except TypeError:

            upsert_module(
                module_id=module_id,
                title=title,
            )

        return module

    # ======================================================
    # Chapter registration
    # ======================================================

    def register_chapter(
        self,
        module_id: str,
        chapter_id: str,
        title: str,
        description: str = "",
    ) -> ChapterRecord:

        self._validate_identifier(
            module_id,
            "module_id",
        )

        self._validate_identifier(
            chapter_id,
            "chapter_id",
        )

        self._validate_title(
            title,
            "chapter title",
        )

        description = self._normalize_description(
            description
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
                description=description,
            )

            module.chapters[
                chapter_id
            ] = chapter

        else:

            chapter.title = title

            if description:
                chapter.description = description

        self._ensure_database()

        upsert_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
            title=title,
        )

        return chapter

    # ======================================================
    # Lesson registration
    # ======================================================

    def register_lesson(
        self,
        module_id: str,
        chapter_id: str,
        lesson_id: str,
        title: str,
        data: dict[str, Any] | None = None,
    ) -> LessonRecord:

        self._validate_identifier(
            module_id,
            "module_id",
        )

        self._validate_identifier(
            chapter_id,
            "chapter_id",
        )

        self._validate_identifier(
            lesson_id,
            "lesson_id",
        )

        self._validate_title(
            title,
            "lesson title",
        )

        normalized_data = (
            self._normalize_lesson_data(data)
        )

        # --------------------------------------------------
        # Preserve existing chapter information.
        # --------------------------------------------------

        chapter = self.get_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
        )

        if chapter is None:

            chapter = self.register_chapter(
                module_id=module_id,
                chapter_id=chapter_id,
                title=chapter_id,
            )

        # --------------------------------------------------
        # Register or update lesson.
        # --------------------------------------------------

        lesson = chapter.lessons.get(
            lesson_id
        )

        if lesson is None:

            lesson = LessonRecord(
                lesson_id=lesson_id,
                title=title,
                module_id=module_id,
                chapter_id=chapter_id,
                data=normalized_data,
            )

            chapter.lessons[
                lesson_id
            ] = lesson

        else:

            lesson.title = title

            # IMPORTANT:
            # Never erase existing lesson data when
            # a caller does not provide new data.
            if data is not None:
                lesson.data = normalized_data

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
        lessons: list[dict[str, Any]],
    ) -> list[LessonRecord]:

        if not isinstance(
            lessons,
            list,
        ):
            raise TypeError(
                "lessons must be a list."
            )

        registered: list[
            LessonRecord
        ] = []

        for lesson_data in lessons:

            if not isinstance(
                lesson_data,
                dict,
            ):
                raise TypeError(
                    "Each lesson must be a dictionary."
                )

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

        return self.modules.get(
            module_id
        )

    def get_chapter(
        self,
        module_id: str,
        chapter_id: str,
    ) -> ChapterRecord | None:

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
    # Existence
    # ======================================================

    def has_module(
        self,
        module_id: str,
    ) -> bool:

        return module_id in self.modules

    def has_chapter(
        self,
        module_id: str,
        chapter_id: str,
    ) -> bool:

        return (
            self.get_chapter(
                module_id=module_id,
                chapter_id=chapter_id,
            )
            is not None
        )

    def has_lesson(
        self,
        module_id: str,
        chapter_id: str,
        lesson_id: str,
    ) -> bool:

        return (
            self.get_lesson(
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
            )
            is not None
        )

    # ======================================================
    # Counts
    # ======================================================

    def module_count(self) -> int:

        return len(
            self.modules
        )

    def chapter_count(
        self,
        module_id: str,
    ) -> int:

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

        return list(
            self.modules.values()
        )

    def list_chapters(
        self,
        module_id: str,
    ) -> list[ChapterRecord]:

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

        chapter = self.get_chapter(
            module_id=module_id,
            chapter_id=chapter_id,
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
                "description": module.description,
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
                    "description": chapter.description,
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
                        "data": dict(
                            lesson.data
                        ),
                    }

        return result

    # ======================================================
    # Clear memory
    # ======================================================

    def clear_memory(
        self,
    ) -> None:

        self.modules.clear()


# ==========================================================
# Global Registry
# ==========================================================

registry = Registry()
