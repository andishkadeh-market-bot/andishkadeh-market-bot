import pytest

from core import database
from core.registry import (
    Registry,
    LessonRecord,
    ChapterRecord,
    ModuleRecord,
)


# ==========================================================
# Fixtures
# ==========================================================


@pytest.fixture
def registry(tmp_path, monkeypatch):
    """
    Create an isolated Registry backed by a temporary SQLite DB.
    """

    db_path = tmp_path / "test_registry.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    return Registry(
        auto_initialize_database=True
    )


# ==========================================================
# Initialization
# ==========================================================


def test_registry_initialization(
    registry,
):
    assert registry.module_count() == 0
    assert registry.statistics() == {
        "modules": 0,
        "chapters": 0,
        "lessons": 0,
    }


def test_registry_creates_database(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    assert registry is not None
    assert db_path.exists()


# ==========================================================
# Module
# ==========================================================


def test_register_module(
    registry,
):
    module = registry.register_module(
        module_id="management",
        title="آموزش مدیریت",
    )

    assert isinstance(
        module,
        ModuleRecord,
    )

    assert module.module_id == "management"
    assert module.title == "آموزش مدیریت"

    assert registry.module_count() == 1


def test_register_module_updates_title(
    registry,
):
    registry.register_module(
        "management",
        "آموزش مدیریت",
    )

    module = registry.register_module(
        "management",
        "آموزش تخصصی مدیریت",
    )

    assert registry.module_count() == 1
    assert module.title == "آموزش تخصصی مدیریت"

    stored = registry.get_module(
        "management"
    )

    assert stored is not None
    assert stored.title == (
        "آموزش تخصصی مدیریت"
    )


def test_register_module_persists_to_sqlite(
    registry,
):
    registry.register_module(
        "management",
        "آموزش مدیریت",
    )

    with database.get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                module_id,
                title
            FROM modules
            WHERE module_id = ?
            """,
            ("management",),
        ).fetchone()

    assert row is not None
    assert row["module_id"] == "management"
    assert row["title"] == "آموزش مدیریت"


# ==========================================================
# Chapter
# ==========================================================


def test_register_chapter(
    registry,
):
    chapter = registry.register_chapter(
        module_id="management",
        chapter_id="planning",
        title="برنامه‌ریزی",
    )

    assert isinstance(
        chapter,
        ChapterRecord,
    )

    assert chapter.chapter_id == "planning"
    assert chapter.title == "برنامه‌ریزی"
    assert chapter.module_id == "management"

    assert registry.module_count() == 1
    assert registry.chapter_count(
        "management"
    ) == 1


def test_register_chapter_creates_module(
    registry,
):
    registry.register_chapter(
        module_id="management",
        chapter_id="planning",
        title="برنامه‌ریزی",
    )

    assert registry.has_module(
        "management"
    )

    assert registry.has_chapter(
        "management",
        "planning",
    )


def test_register_chapter_updates_title(
    registry,
):
    registry.register_chapter(
        "management",
        "planning",
        "برنامه‌ریزی",
    )

    registry.register_chapter(
        "management",
        "planning",
        "برنامه‌ریزی و تصمیم‌گیری",
    )

    chapter = registry.get_chapter(
        "management",
        "planning",
    )

    assert chapter is not None
    assert chapter.title == (
        "برنامه‌ریزی و تصمیم‌گیری"
    )

    assert registry.chapter_count(
        "management"
    ) == 1


def test_register_chapter_persists_to_sqlite(
    registry,
):
    registry.register_chapter(
        "management",
        "planning",
        "برنامه‌ریزی",
    )

    with database.get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM chapters
            WHERE module_id = ?
              AND chapter_id = ?
            """,
            (
                "management",
                "planning",
            ),
        ).fetchone()

    assert row is not None
    assert row["title"] == "برنامه‌ریزی"


# ==========================================================
# Lesson
# ==========================================================


def test_register_lesson(
    registry,
):
    lesson = registry.register_lesson(
        module_id="management",
        chapter_id="planning",
        lesson_id="lesson_01",
        title="مبانی برنامه‌ریزی",
    )

    assert isinstance(
        lesson,
        LessonRecord,
    )

    assert lesson.lesson_id == "lesson_01"
    assert lesson.title == "مبانی برنامه‌ریزی"
    assert lesson.module_id == "management"
    assert lesson.chapter_id == "planning"

    assert registry.lesson_count(
        "management",
        "planning",
    ) == 1


def test_register_lesson_creates_parents(
    registry,
):
    registry.register_lesson(
        module_id="management",
        chapter_id="planning",
        lesson_id="lesson_01",
        title="مبانی برنامه‌ریزی",
    )

    assert registry.has_module(
        "management"
    )

    assert registry.has_chapter(
        "management",
        "planning",
    )

    assert registry.has_lesson(
        "management",
        "planning",
        "lesson_01",
    )


def test_register_lesson_with_data(
    registry,
):
    lesson = registry.register_lesson(
        module_id="management",
        chapter_id="planning",
        lesson_id="lesson_01",
        title="مبانی برنامه‌ریزی",
        data={
            "level": "basic",
            "duration": 30,
            "tags": [
                "planning",
                "management",
            ],
        },
    )

    assert lesson.data["level"] == "basic"
    assert lesson.data["duration"] == 30
    assert lesson.data["tags"] == [
        "planning",
        "management",
    ]


def test_register_lesson_updates_existing_lesson(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "مبانی برنامه‌ریزی",
    )

    lesson = registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "مبانی پیشرفته برنامه‌ریزی",
        data={
            "level": "advanced"
        },
    )

    assert lesson.title == (
        "مبانی پیشرفته برنامه‌ریزی"
    )

    assert lesson.data == {
        "level": "advanced"
    }

    assert registry.lesson_count(
        "management",
        "planning",
    ) == 1


def test_register_lesson_without_new_data_keeps_old_data(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
        data={
            "level": "basic"
        },
    )

    lesson = registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول جدید",
    )

    assert lesson.title == "درس اول جدید"

    assert lesson.data == {
        "level": "basic"
    }


def test_register_lesson_persists_to_sqlite(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "مبانی برنامه‌ریزی",
    )

    with database.get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM lessons
            WHERE module_id = ?
              AND chapter_id = ?
              AND lesson_id = ?
            """,
            (
                "management",
                "planning",
                "lesson_01",
            ),
        ).fetchone()

    assert row is not None
    assert row["title"] == "مبانی برنامه‌ریزی"


# ==========================================================
# Bulk registration
# ==========================================================


def test_register_many_lessons(
    registry,
):
    lessons = registry.register_many_lessons(
        module_id="management",
        chapter_id="planning",
        lessons=[
            {
                "lesson_id": "lesson_01",
                "title": "درس اول",
            },
            {
                "lesson_id": "lesson_02",
                "title": "درس دوم",
            },
            {
                "lesson_id": "lesson_03",
                "title": "درس سوم",
            },
        ],
    )

    assert len(lessons) == 3

    assert registry.lesson_count(
        "management",
        "planning",
    ) == 3


def test_register_many_lessons_with_data(
    registry,
):
    lessons = registry.register_many_lessons(
        "management",
        "planning",
        [
            {
                "lesson_id": "lesson_01",
                "title": "درس اول",
                "data": {
                    "quiz": True
                },
            },
            {
                "lesson_id": "lesson_02",
                "title": "درس دوم",
                "data": {
                    "quiz": False
                },
            },
        ],
    )

    assert lessons[0].data == {
        "quiz": True
    }

    assert lessons[1].data == {
        "quiz": False
    }


# ==========================================================
# Lookup
# ==========================================================


def test_get_module_returns_module(
    registry,
):
    registry.register_module(
        "management",
        "آموزش مدیریت",
    )

    module = registry.get_module(
        "management"
    )

    assert module is not None
    assert module.module_id == "management"


def test_get_unknown_module_returns_none(
    registry,
):
    assert registry.get_module(
        "unknown"
    ) is None


def test_get_chapter_returns_chapter(
    registry,
):
    registry.register_chapter(
        "management",
        "planning",
        "برنامه‌ریزی",
    )

    chapter = registry.get_chapter(
        "management",
        "planning",
    )

    assert chapter is not None
    assert chapter.chapter_id == "planning"


def test_get_unknown_chapter_returns_none(
    registry,
):
    assert registry.get_chapter(
        "management",
        "unknown",
    ) is None


def test_get_lesson_returns_lesson(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
    )

    lesson = registry.get_lesson(
        "management",
        "planning",
        "lesson_01",
    )

    assert lesson is not None
    assert lesson.lesson_id == "lesson_01"


def test_get_unknown_lesson_returns_none(
    registry,
):
    assert registry.get_lesson(
        "management",
        "planning",
        "unknown",
    ) is None


# ==========================================================
# Existence helpers
# ==========================================================


def test_has_helpers(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
    )

    assert registry.has_module(
        "management"
    ) is True

    assert registry.has_chapter(
        "management",
        "planning",
    ) is True

    assert registry.has_lesson(
        "management",
        "planning",
        "lesson_01",
    ) is True


def test_has_helpers_for_unknown_content(
    registry,
):
    assert registry.has_module(
        "unknown"
    ) is False

    assert registry.has_chapter(
        "unknown",
        "unknown",
    ) is False

    assert registry.has_lesson(
        "unknown",
        "unknown",
        "unknown",
    ) is False


# ==========================================================
# Counts
# ==========================================================


def test_counts(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
    )

    registry.register_lesson(
        "management",
        "planning",
        "lesson_02",
        "درس دوم",
    )

    registry.register_lesson(
        "management",
        "organizing",
        "lesson_03",
        "درس سوم",
    )

    assert registry.module_count() == 1

    assert registry.chapter_count(
        "management"
    ) == 2

    assert registry.lesson_count(
        "management"
    ) == 3

    assert registry.lesson_count(
        "management",
        "planning",
    ) == 2

    assert registry.lesson_count(
        "management",
        "organizing",
    ) == 1


def test_counts_unknown_content(
    registry,
):
    assert registry.chapter_count(
        "unknown"
    ) == 0

    assert registry.lesson_count(
        "unknown"
    ) == 0

    assert registry.lesson_count(
        "management",
        "unknown",
    ) == 0


# ==========================================================
# Listing
# ==========================================================


def test_list_modules(
    registry,
):
    registry.register_module(
        "management",
        "آموزش مدیریت",
    )

    registry.register_module(
        "trade",
        "تجارت بین‌الملل",
    )

    modules = registry.list_modules()

    assert len(modules) == 2

    ids = {
        module.module_id
        for module in modules
    }

    assert ids == {
        "management",
        "trade",
    }


def test_list_chapters(
    registry,
):
    registry.register_chapter(
        "management",
        "planning",
        "برنامه‌ریزی",
    )

    registry.register_chapter(
        "management",
        "organizing",
        "سازماندهی",
    )

    chapters = registry.list_chapters(
        "management"
    )

    assert len(chapters) == 2

    ids = {
        chapter.chapter_id
        for chapter in chapters
    }

    assert ids == {
        "planning",
        "organizing",
    }


def test_list_lessons(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
    )

    registry.register_lesson(
        "management",
        "planning",
        "lesson_02",
        "درس دوم",
    )

    lessons = registry.list_lessons(
        "management",
        "planning",
    )

    assert len(lessons) == 2

    ids = {
        lesson.lesson_id
        for lesson in lessons
    }

    assert ids == {
        "lesson_01",
        "lesson_02",
    }


def test_listing_unknown_content(
    registry,
):
    assert registry.list_chapters(
        "unknown"
    ) == []

    assert registry.list_lessons(
        "management",
        "unknown",
    ) == []


# ==========================================================
# Statistics
# ==========================================================


def test_statistics(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
    )

    registry.register_lesson(
        "management",
        "planning",
        "lesson_02",
        "درس دوم",
    )

    registry.register_lesson(
        "management",
        "organizing",
        "lesson_03",
        "درس سوم",
    )

    registry.register_lesson(
        "trade",
        "international_trade",
        "lesson_04",
        "درس چهارم",
    )

    assert registry.statistics() == {
        "modules": 2,
        "chapters": 3,
        "lessons": 4,
    }


# ==========================================================
# Export
# ==========================================================


def test_export(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "مبانی برنامه‌ریزی",
        data={
            "level": "basic"
        },
    )

    exported = registry.export()

    assert exported["management"]["id"] == (
        "management"
    )

    assert exported["management"]["title"] == (
        "management"
    )

    assert exported["management"]["chapters"][
        "planning"
    ]["lessons"]["lesson_01"]["title"] == (
        "مبانی برنامه‌ریزی"
    )

    assert exported["management"]["chapters"][
        "planning"
    ]["lessons"]["lesson_01"]["data"] == {
        "level": "basic"
    }


def test_export_is_independent(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
        data={
            "level": "basic"
        },
    )

    exported = registry.export()

    exported["management"]["title"] = (
        "تغییر تست"
    )

    exported["management"]["chapters"][
        "planning"
    ]["lessons"]["lesson_01"]["data"][
        "level"
    ] = "changed"

    module = registry.get_module(
        "management"
    )

    lesson = registry.get_lesson(
        "management",
        "planning",
        "lesson_01",
    )

    assert module is not None
    assert module.title == "management"

    assert lesson is not None
    assert lesson.data["level"] == "basic"


# ==========================================================
# Clear memory
# ==========================================================


def test_clear_memory_preserves_sqlite(
    registry,
):
    registry.register_lesson(
        "management",
        "planning",
        "lesson_01",
        "درس اول",
    )

    assert registry.has_lesson(
        "management",
        "planning",
        "lesson_01",
    )

    registry.clear_memory()

    assert registry.module_count() == 0

    assert registry.get_lesson(
        "management",
        "planning",
        "lesson_01",
    ) is None

    with database.get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM lessons
            WHERE module_id = ?
              AND chapter_id = ?
              AND lesson_id = ?
            """,
            (
                "management",
                "planning",
                "lesson_01",
            ),
        ).fetchone()

    assert row is not None
    assert row["lesson_id"] == "lesson_01"


# ==========================================================
# Validation
# ==========================================================


def test_invalid_module_id(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_module(
            "",
            "آموزش مدیریت",
        )


def test_invalid_module_title(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_module(
            "management",
            "",
        )


def test_invalid_chapter_id(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_chapter(
            "management",
            "",
            "برنامه‌ریزی",
        )


def test_invalid_chapter_title(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_chapter(
            "management",
            "planning",
            "",
        )


def test_invalid_lesson_id(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_lesson(
            "management",
            "planning",
            "",
            "درس اول",
        )


def test_invalid_lesson_title(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_lesson(
            "management",
            "planning",
            "lesson_01",
            "",
        )


def test_invalid_lesson_data(
    registry,
):
    with pytest.raises(
        TypeError
    ):
        registry.register_lesson(
            "management",
            "planning",
            "lesson_01",
            "درس اول",
            data="invalid",
        )


def test_invalid_bulk_lessons(
    registry,
):
    with pytest.raises(
        TypeError
    ):
        registry.register_many_lessons(
            "management",
            "planning",
            "invalid",
        )


def test_bulk_lesson_missing_id(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_many_lessons(
            "management",
            "planning",
            [
                {
                    "title": "درس اول"
                }
            ],
        )


def test_bulk_lesson_missing_title(
    registry,
):
    with pytest.raises(
        ValueError
    ):
        registry.register_many_lessons(
            "management",
            "planning",
            [
                {
                    "lesson_id": "lesson_01"
                }
            ],
        )
