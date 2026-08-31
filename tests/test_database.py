import sqlite3

import modules.management
from core import database


def test_database_connection():
    connection = database.get_connection()

    try:
        result = connection.execute(
            "SELECT 1"
        ).fetchone()

        assert result[0] == 1

    finally:
        connection.close()


def test_database_initialization(tmp_path, monkeypatch):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    assert db_path.exists()

    with database.get_connection() as connection:
        tables = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }

    expected_tables = {
        "users",
        "modules",
        "chapters",
        "lessons",
        "lesson_progress",
        "quiz_attempts",
    }

    assert expected_tables.issubset(
        tables
    )


def test_database_health_check():
    assert database.database_health_check() is True


def test_user_upsert(tmp_path, monkeypatch):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    database.upsert_user(
        telegram_id=123456789,
        username="test_user",
        first_name="Ali",
        last_name="Test",
    )

    with database.get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name,
                last_name
            FROM users
            WHERE telegram_id = ?
            """,
            (123456789,),
        ).fetchone()

    assert row is not None
    assert row["telegram_id"] == 123456789
    assert row["username"] == "test_user"
    assert row["first_name"] == "Ali"
    assert row["last_name"] == "Test"


def test_module_chapter_lesson_registration(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    database.upsert_module(
        "management",
        "آموزش مدیریت",
    )

    database.upsert_chapter(
        "management",
        "chapter_01",
        "فصل ۱: مبانی مدیریت",
    )

    database.upsert_lesson(
        "management",
        "chapter_01",
        "lesson_01",
        "درس ۱",
    )

    with database.get_connection() as connection:

        module = connection.execute(
            """
            SELECT *
            FROM modules
            WHERE module_id = ?
            """,
            ("management",),
        ).fetchone()

        chapter = connection.execute(
            """
            SELECT *
            FROM chapters
            WHERE module_id = ?
              AND chapter_id = ?
            """,
            (
                "management",
                "chapter_01",
            ),
        ).fetchone()

        lesson = connection.execute(
            """
            SELECT *
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

    assert module is not None
    assert module["title"] == "آموزش مدیریت"

    assert chapter is not None
    assert chapter["title"] == (
        "فصل ۱: مبانی مدیریت"
    )

    assert lesson is not None
    assert lesson["title"] == "درس ۱"


def test_lesson_progress(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    database.upsert_user(
        telegram_id=987654321,
        username="progress_test",
    )

    database.mark_lesson_started(
        telegram_id=987654321,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    progress = database.get_lesson_progress(
        telegram_id=987654321,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert progress is not None
    assert progress["started"] == 1
    assert progress["completed"] == 0

    database.mark_lesson_completed(
        telegram_id=987654321,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    progress = database.get_lesson_progress(
        telegram_id=987654321,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert progress is not None
    assert progress["started"] == 1
    assert progress["completed"] == 1


def test_user_progress_list(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    database.upsert_user(
        telegram_id=111222333,
    )

    database.mark_lesson_completed(
        telegram_id=111222333,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    database.mark_lesson_completed(
        telegram_id=111222333,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_02",
    )

    progress = database.get_user_progress(
        telegram_id=111222333,
        module_id="management",
    )

    assert len(progress) == 2

    lesson_ids = {
        item["lesson_id"]
        for item in progress
    }

    assert lesson_ids == {
        "lesson_01",
        "lesson_02",
    }


def test_quiz_attempt(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    database.upsert_user(
        telegram_id=444555666,
    )

    attempt_id = database.save_quiz_attempt(
        telegram_id=444555666,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
        total_questions=10,
        correct_answers=8,
        score=80.0,
    )

    assert attempt_id > 0

    attempts = database.get_quiz_attempts(
        telegram_id=444555666,
        module_id="management",
    )

    assert len(attempts) == 1

    attempt = attempts[0]

    assert attempt["total_questions"] == 10
    assert attempt["correct_answers"] == 8
    assert attempt["score"] == 80.0


def test_foreign_keys_are_enabled(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "test_bot.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    with database.get_connection() as connection:
        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

    assert result[0] == 1
