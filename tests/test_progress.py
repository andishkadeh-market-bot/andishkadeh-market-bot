from core import database
from core.progress import (
    complete_lesson,
    get_chapter_progress,
    get_last_completed_lesson,
    get_lesson_status,
    get_module_progress,
    get_progress_percentage,
    get_user_progress,
    is_lesson_completed,
    is_lesson_started,
    is_module_completed,
    progress_health_check,
    register_user,
    start_lesson,
)


def setup_test_database(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "progress_test.db"

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
        "فصل اول",
    )

    database.upsert_lesson(
        "management",
        "chapter_01",
        "lesson_01",
        "درس اول",
    )

    database.upsert_lesson(
        "management",
        "chapter_01",
        "lesson_02",
        "درس دوم",
    )

    database.upsert_lesson(
        "management",
        "chapter_01",
        "lesson_03",
        "درس سوم",
    )

    database.upsert_chapter(
        "management",
        "chapter_02",
        "فصل دوم",
    )

    database.upsert_lesson(
        "management",
        "chapter_02",
        "lesson_04",
        "درس چهارم",
    )

    return db_path


def test_register_user(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    register_user(
        telegram_id=1001,
        username="ali",
        first_name="Ali",
        last_name="Test",
    )

    with database.get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (1001,),
        ).fetchone()

    assert row is not None
    assert row["username"] == "ali"
    assert row["first_name"] == "Ali"


def test_start_lesson(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    start_lesson(
        telegram_id=1002,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    status = get_lesson_status(
        telegram_id=1002,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert status["started"] is True
    assert status["completed"] is False


def test_complete_lesson(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    complete_lesson(
        telegram_id=1003,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    status = get_lesson_status(
        telegram_id=1003,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert status["started"] is True
    assert status["completed"] is True


def test_lesson_status_helpers(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    assert is_lesson_started(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    ) is False

    assert is_lesson_completed(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    ) is False

    start_lesson(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert is_lesson_started(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    ) is True

    complete_lesson(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert is_lesson_completed(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    ) is True


def test_chapter_progress(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    complete_lesson(
        telegram_id=1005,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    progress = get_chapter_progress(
        telegram_id=1005,
        module_id="management",
        chapter_id="chapter_01",
    )

    assert progress["total_lessons"] == 3
    assert progress["started_lessons"] == 1
    assert progress["completed_lessons"] == 1
    assert progress["remaining_lessons"] == 2
    assert progress["percentage"] == 33.33
    assert progress["completed"] is False


def test_module_progress(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    complete_lesson(
        telegram_id=1006,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    complete_lesson(
        telegram_id=1006,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_02",
    )

    progress = get_module_progress(
        telegram_id=1006,
        module_id="management",
    )

    assert progress["total_lessons"] == 4
    assert progress["completed_lessons"] == 2
    assert progress["remaining_lessons"] == 2
    assert progress["percentage"] == 50.0
    assert progress["completed"] is False
    assert len(progress["chapters"]) == 2


def test_user_progress(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    complete_lesson(
        telegram_id=1007,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    complete_lesson(
        telegram_id=1007,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_02",
    )

    progress = get_user_progress(
        telegram_id=1007,
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


def test_last_completed_lesson(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    complete_lesson(
        telegram_id=1008,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    last_lesson = get_last_completed_lesson(
        telegram_id=1008,
        module_id="management",
    )

    assert last_lesson is not None
    assert last_lesson["lesson_id"] == "lesson_01"


def test_progress_percentage(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    complete_lesson(
        telegram_id=1009,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    percentage = get_progress_percentage(
        telegram_id=1009,
        module_id="management",
    )

    assert percentage == 25.0


def test_module_completion(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    assert is_module_completed(
        telegram_id=1010,
        module_id="management",
    ) is False

    complete_lesson(
        1010,
        "management",
        "chapter_01",
        "lesson_01",
    )

    complete_lesson(
        1010,
        "management",
        "chapter_01",
        "lesson_02",
    )

    complete_lesson(
        1010,
        "management",
        "chapter_01",
        "lesson_03",
    )

    complete_lesson(
        1010,
        "management",
        "chapter_02",
        "lesson_04",
    )

    assert is_module_completed(
        telegram_id=1010,
        module_id="management",
    ) is True


def test_progress_health_check(
    tmp_path,
    monkeypatch,
):
    setup_test_database(
        tmp_path,
        monkeypatch,
    )

    assert progress_health_check() is True
