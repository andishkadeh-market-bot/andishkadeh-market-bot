from core import database

from core.statistics import (
    calculate_score,
    get_attempts,
    get_best_attempt,
    get_latest_attempt,
    get_lesson_statistics,
    get_module_statistics,
    get_user_statistics,
    record_quiz_result,
    statistics_health_check,
)


def setup_statistics_database(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "statistics_test.db"

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

    return db_path


def test_calculate_score():
    assert calculate_score(
        8,
        10,
    ) == 80.0

    assert calculate_score(
        7,
        10,
    ) == 70.0

    assert calculate_score(
        3,
        4,
    ) == 75.0


def test_calculate_score_validation():

    try:
        calculate_score(
            1,
            0,
        )
        assert False

    except ValueError:
        assert True

    try:
        calculate_score(
            -1,
            10,
        )
        assert False

    except ValueError:
        assert True

    try:
        calculate_score(
            11,
            10,
        )
        assert False

    except ValueError:
        assert True


def test_record_quiz_result(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    attempt_id = record_quiz_result(
        telegram_id=2001,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
        total_questions=10,
        correct_answers=8,
    )

    assert attempt_id > 0

    attempts = get_attempts(
        telegram_id=2001,
    )

    assert len(attempts) == 1

    attempt = attempts[0]

    assert attempt["total_questions"] == 10
    assert attempt["correct_answers"] == 8
    assert attempt["score"] == 80.0


def test_record_quiz_result_custom_score(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        telegram_id=2002,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
        total_questions=10,
        correct_answers=8,
        score=82.5,
    )

    attempts = get_attempts(
        telegram_id=2002,
    )

    assert len(attempts) == 1
    assert attempts[0]["score"] == 82.5


def test_user_statistics(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        2003,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        8,
    )

    record_quiz_result(
        2003,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        6,
    )

    statistics = get_user_statistics(
        telegram_id=2003,
    )

    assert statistics["attempts"] == 2
    assert statistics["total_questions"] == 20
    assert statistics["correct_answers"] == 14
    assert statistics["wrong_answers"] == 6
    assert statistics["accuracy"] == 70.0
    assert statistics["average_score"] == 70.0
    assert statistics["best_score"] == 80.0
    assert statistics["lowest_score"] == 60.0


def test_module_statistics(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        2004,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        9,
    )

    record_quiz_result(
        2004,
        "management",
        "chapter_01",
        "lesson_02",
        10,
        7,
    )

    statistics = get_module_statistics(
        telegram_id=2004,
        module_id="management",
    )

    assert statistics["attempts"] == 2
    assert statistics["total_questions"] == 20
    assert statistics["correct_answers"] == 16
    assert statistics["accuracy"] == 80.0
    assert statistics["best_score"] == 90.0

    assert len(
        statistics["lessons"]
    ) == 2


def test_lesson_statistics(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        2005,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        9,
    )

    record_quiz_result(
        2005,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        7,
    )

    statistics = get_lesson_statistics(
        telegram_id=2005,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert statistics["attempts"] == 2
    assert statistics["total_questions"] == 20
    assert statistics["correct_answers"] == 16
    assert statistics["wrong_answers"] == 4
    assert statistics["accuracy"] == 80.0
    assert statistics["average_score"] == 80.0
    assert statistics["best_score"] == 90.0


def test_get_attempts_filters(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        2006,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        8,
    )

    record_quiz_result(
        2006,
        "management",
        "chapter_01",
        "lesson_02",
        10,
        6,
    )

    all_attempts = get_attempts(
        telegram_id=2006,
    )

    assert len(all_attempts) == 2

    lesson_attempts = get_attempts(
        telegram_id=2006,
        module_id="management",
        chapter_id="chapter_01",
        lesson_id="lesson_01",
    )

    assert len(lesson_attempts) == 1
    assert (
        lesson_attempts[0]["lesson_id"]
        == "lesson_01"
    )


def test_latest_attempt(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        2007,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        5,
    )

    record_quiz_result(
        2007,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        9,
    )

    latest = get_latest_attempt(
        telegram_id=2007,
        module_id="management",
    )

    assert latest is not None
    assert latest["correct_answers"] == 9


def test_best_attempt(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    record_quiz_result(
        2008,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        5,
    )

    record_quiz_result(
        2008,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        9,
    )

    record_quiz_result(
        2008,
        "management",
        "chapter_01",
        "lesson_01",
        10,
        7,
    )

    best = get_best_attempt(
        telegram_id=2008,
        module_id="management",
    )

    assert best is not None
    assert best["correct_answers"] == 9
    assert best["score"] == 90.0


def test_empty_user_statistics(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    statistics = get_user_statistics(
        telegram_id=999999,
    )

    assert statistics["attempts"] == 0
    assert statistics["total_questions"] == 0
    assert statistics["correct_answers"] == 0
    assert statistics["wrong_answers"] == 0
    assert statistics["accuracy"] == 0.0
    assert statistics["average_score"] == 0.0
    assert statistics["best_score"] == 0.0


def test_statistics_health_check(
    tmp_path,
    monkeypatch,
):
    setup_statistics_database(
        tmp_path,
        monkeypatch,
    )

    assert statistics_health_check() is True
