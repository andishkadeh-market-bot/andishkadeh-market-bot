from core import database
from core.registry import Registry


def test_registry_initialization(tmp_path, monkeypatch):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    assert registry.module_count() == 0
    assert db_path.exists()


def test_register_module_is_saved_to_sqlite(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    registry.register_module(
        module_id="management",
        title="آموزش مدیریت",
    )

    module = registry.get_module(
        "management"
    )

    assert module is not None
    assert module.module_id == "management"
    assert module.title == "آموزش مدیریت"

    with database.get_connection() as connection:
        row = connection.execute(
            """
            SELECT module_id, title
            FROM modules
            WHERE module_id = ?
            """,
            ("management",),
        ).fetchone()

    assert row is not None
    assert row["module_id"] == "management"
    assert row["title"] == "آموزش مدیریت"


def test_register_chapter_is_saved_to_sqlite(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    registry.register_chapter(
        module_id="management",
        chapter_id="chapter_01",
        title="فصل اول مدیریت",
    )

    chapter = registry.get_chapter(
        "management",
        "chapter_01",
    )

    assert chapter is not None
    assert chapter.chapter_id == "chapter_01"
    assert chapter.title == "فصل اول مدیریت"

    with database.get_connection() as connection:
        row = connection.execute(
            """
            SELECT module_id, chapter_id, title
            FROM chapters
            WHERE module_id = ?
              AND chapter_id = ?
            """,
            (
                "management",
                "chapter_01",
            ),
        ).fetchone()

    assert row is not None
    assert row["module_id"] == "management"
    assert row["chapter_id"] == "chapter_01"
    assert row["title"] == "فصل اول مدیریت"


def test_register_lesson_is_saved_to_sqlite(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    registry.register_lesson(
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
        title="مبانی مدیریت",
        data={
            "test": True,
        },
    )

    lesson = registry.get_lesson(
        "management",
        "chapter_01",
        "lesson_01",
    )

    assert lesson is not None
    assert lesson.lesson_id == "lesson_01"
    assert lesson.title == "مبانی مدیریت"
    assert lesson.data["test"] is True

    with database.get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                module_id,
                chapter_id,
                lesson_id,
                title
            FROM lessons
            WHERE module_id = ?
              AND chapter_id = ?
              AND lesson_id = ?
            """,
            (
                "management",
                "chapter_01",
                "lesson_01",
            ),
        ).fetchone()

    assert row is not None
    assert row["module_id"] == "management"
    assert row["chapter_id"] == "chapter_01"
    assert row["lesson_id"] == "lesson_01"
    assert row["title"] == "مبانی مدیریت"


def test_register_lesson_creates_hierarchy(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    registry.register_lesson(
        module_id="management",
        chapter_id="chapter_02",
        lesson_id="lesson_15",
        title="برنامه‌ریزی",
    )

    assert registry.has_module(
        "management"
    )

    assert registry.has_chapter(
        "management",
        "chapter_02",
    )

    assert registry.has_lesson(
        "management",
        "chapter_02",
        "lesson_15",
    )

    assert registry.module_count() == 1
    assert registry.chapter_count(
        "management"
    ) == 1

    assert registry.lesson_count(
        "management"
    ) == 1


def test_register_many_lessons(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    lessons = registry.register_many_lessons(
        module_id="management",
        chapter_id="chapter_03",
        lessons=[
            {
                "lesson_id": "lesson_20",
                "title": "درس بیستم",
            },
            {
                "lesson_id": "lesson_21",
                "title": "درس بیست و یکم",
            },
            {
                "lesson_id": "lesson_22",
                "title": "درس بیست و دوم",
            },
        ],
    )

    assert len(lessons) == 3

    assert registry.lesson_count(
        "management",
        "chapter_03",
    ) == 3

    assert registry.has_lesson(
        "management",
        "chapter_03",
        "lesson_20",
    )

    assert registry.has_lesson(
        "management",
        "chapter_03",
        "lesson_21",
    )

    assert registry.has_lesson(
        "management",
        "chapter_03",
        "lesson_22",
    )

    with database.get_connection() as connection:
        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM lessons
            WHERE module_id = ?
              AND chapter_id = ?
            """,
            (
                "management",
                "chapter_03",
            ),
        ).fetchone()[0]

    assert count == 3


def test_registry_statistics(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    registry.register_module(
        "management",
        "آموزش مدیریت",
    )

    registry.register_chapter(
        "management",
        "chapter_01",
        "فصل اول",
    )

    registry.register_lesson(
        "management",
        "chapter_01",
        "lesson_01",
        "درس اول",
    )

    registry.register_lesson(
        "management",
        "chapter_01",
        "lesson_02",
        "درس دوم",
    )

    stats = registry.statistics()

    assert stats == {
        "modules": 1,
        "chapters": 1,
        "lessons": 2,
    }


def test_registry_export(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "registry_test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    registry = Registry()

    registry.register_lesson(
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
        title="مبانی مدیریت",
        data={
            "level": "basic",
        },
    )

    exported = registry.export()

    assert "management" in exported

    assert (
        exported["management"]["title"]
        == "management"
    )

    assert (
        "chapter_01"
        in exported["management"]["chapters"]
    )

    lesson = exported[
        "management"
    ]["chapters"][
        "chapter_01"
    ]["lessons"][
        "lesson_01"
    ]

    assert lesson["title"] == "مبانی مدیریت"
    assert lesson["data"]["level"] == "basic"
