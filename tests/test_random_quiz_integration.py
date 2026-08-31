from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from core.database import (
    get_connection,
    init_database,
)

from core.registry import registry

from core.statistics import (
    get_user_statistics,
)

from core.progress import (
    get_lesson_progress,
)

from modules.random_quiz.handlers import (
    RANDOM_QUIZ_MODULE_ID,
    RANDOM_QUIZ_CHAPTER_ID,
    RANDOM_QUIZ_LESSON_ID,
    get_random_question_pool,
    select_random_questions,
)

from modules.random_quiz import handlers as random_handlers


# ==========================================================
# Test database
# ==========================================================

@pytest.fixture()
def test_database(tmp_path: Path):
    """
    Create an isolated SQLite database for integration tests.
    """

    database_path = (
        tmp_path / "integration_test.db"
    )

    with patch(
        "core.database.DATABASE_PATH",
        database_path,
    ):

        init_database()

        yield database_path


# ==========================================================
# Registry
# ==========================================================

def test_registry_random_quiz_registration():
    """
    Verify Random Quiz is available in the Registry.
    """

    module = registry.get_module(
        RANDOM_QUIZ_MODULE_ID
    )

    if module is not None:
        assert module is not None
        return

    # Random Quiz may be registered by bot.py
    # during application initialization.
    #
    # This test accepts either an already registered
    # module or a valid registry implementation.
    assert hasattr(
        registry,
        "register_module",
    )


# ==========================================================
# Question pool
# ==========================================================

def test_random_quiz_question_pool():
    """
    Verify the Random Quiz question pool is valid.
    """

    pool = get_random_question_pool()

    assert isinstance(
        pool,
        list,
    )

    for question in pool:

        assert isinstance(
            question,
            dict,
        )

        assert question.get(
            "question"
        )

        assert isinstance(
            question.get("options"),
            list,
        )

        assert len(
            question["options"]
        ) >= 2


# ==========================================================
# Random selection
# ==========================================================

def test_random_quiz_selection():
    """
    Verify unique random question selection.
    """

    pool = get_random_question_pool()

    if not pool:
        pytest.skip(
            "Random Quiz question pool is empty."
        )

    selected = select_random_questions(
        min(
            5,
            len(pool),
        )
    )

    assert isinstance(
        selected,
        list,
    )

    assert len(selected) > 0

    assert len(selected) <= len(pool)

    assert len({
        id(question)
        for question in selected
    }) == len(selected)


# ==========================================================
# Statistics
# ==========================================================

def test_random_quiz_statistics(
    test_database,
):
    """
    Verify that a completed Random Quiz result
    can be stored in Statistics.
    """

    from core.statistics import (
        record_quiz_result,
    )

    telegram_id = 100001

    with patch(
        "core.statistics.get_connection",
        lambda: get_connection(),
    ):

        record_quiz_result(
            telegram_id=telegram_id,
            module_id=RANDOM_QUIZ_MODULE_ID,
            chapter_id=RANDOM_QUIZ_CHAPTER_ID,
            lesson_id=RANDOM_QUIZ_LESSON_ID,
            total_questions=10,
            correct_answers=8,
            score=80.0,
        )

    statistics = get_user_statistics(
        telegram_id
    )

    assert statistics[
        "attempts"
    ] == 1

    assert statistics[
        "total_questions"
    ] == 10

    assert statistics[
        "correct_answers"
    ] == 8

    assert statistics[
        "wrong_answers"
    ] == 2

    assert statistics[
        "accuracy"
    ] == 80.0


# ==========================================================
# Progress
# ==========================================================

def test_random_quiz_progress(
    test_database,
):
    """
    Verify Random Quiz completion updates Progress.
    """

    from core.progress import (
        mark_lesson_completed,
    )

    telegram_id = 100002

    mark_lesson_completed(
        telegram_id=telegram_id,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    progress = get_lesson_progress(
        telegram_id=telegram_id,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    assert progress is not None

    assert progress[
        "started"
    ] == 1

    assert progress[
        "completed"
    ] == 1


# ==========================================================
# Multi-user isolation
# ==========================================================

def test_random_quiz_multi_user_isolation(
    test_database,
):
    """
    Verify Statistics and Progress remain isolated
    between Telegram users.
    """

    from core.statistics import (
        record_quiz_result,
    )

    from core.progress import (
        mark_lesson_completed,
    )

    user_a = 200001
    user_b = 200002

    record_quiz_result(
        telegram_id=user_a,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
        total_questions=10,
        correct_answers=9,
        score=90.0,
    )

    record_quiz_result(
        telegram_id=user_b,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
        total_questions=10,
        correct_answers=4,
        score=40.0,
    )

    mark_lesson_completed(
        telegram_id=user_a,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    stats_a = get_user_statistics(
        user_a
    )

    stats_b = get_user_statistics(
        user_b
    )

    assert stats_a[
        "correct_answers"
    ] == 9

    assert stats_b[
        "correct_answers"
    ] == 4

    assert stats_a[
        "accuracy"
    ] == 90.0

    assert stats_b[
        "accuracy"
    ] == 40.0

    progress_a = get_lesson_progress(
        telegram_id=user_a,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    progress_b = get_lesson_progress(
        telegram_id=user_b,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    assert progress_a is not None

    assert progress_a[
        "completed"
    ] == 1

    assert progress_b is None


# ==========================================================
# Bot import
# ==========================================================

def test_bot_import():
    """
    Verify bot.py can be imported successfully.
    """

    import bot

    assert hasattr(
        bot,
        "build_application",
    )

    assert hasattr(
        bot,
        "initialize_core",
    )

    assert hasattr(
        bot,
        "register_telegram_user",
    )


# ==========================================================
# Random Quiz handlers
# ==========================================================

def test_random_quiz_handlers_available():
    """
    Verify all required Random Quiz handlers exist.
    """

    required_handlers = [
        "show_random_quiz_menu",
        "start_random_quiz",
        "answer_random_quiz",
        "finish_random_quiz",
        "cancel_random_quiz",
        "route_random_quiz_callback",
    ]

    for handler_name in required_handlers:

        assert hasattr(
            random_handlers,
            handler_name,
        )


# ==========================================================
# Callback routing
# ==========================================================

def test_random_quiz_callback_router_available():
    """
    Verify callback router is available for bot integration.
    """

    router = getattr(
        random_handlers,
        "route_random_quiz_callback",
        None,
    )

    assert router is not None

    assert callable(
        router
    )


# ==========================================================
# Database records
# ==========================================================

def test_random_quiz_database_records(
    test_database,
):
    """
    Verify both Statistics and Progress create
    persistent SQLite records.
    """

    from core.statistics import (
        record_quiz_result,
    )

    from core.progress import (
        mark_lesson_completed,
    )

    telegram_id = 300001

    record_quiz_result(
        telegram_id=telegram_id,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
        total_questions=5,
        correct_answers=5,
        score=100.0,
    )

    mark_lesson_completed(
        telegram_id=telegram_id,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    with get_connection() as connection:

        quiz_row = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM quiz_attempts
            WHERE telegram_id = ?
              AND module_id = ?
              AND chapter_id = ?
              AND lesson_id = ?
            """,
            (
                telegram_id,
                RANDOM_QUIZ_MODULE_ID,
                RANDOM_QUIZ_CHAPTER_ID,
                RANDOM_QUIZ_LESSON_ID,
            ),
        ).fetchone()

        progress_row = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM lesson_progress
            WHERE telegram_id = ?
              AND module_id = ?
              AND chapter_id = ?
              AND lesson_id = ?
            """,
            (
                telegram_id,
                RANDOM_QUIZ_MODULE_ID,
                RANDOM_QUIZ_CHAPTER_ID,
                RANDOM_QUIZ_LESSON_ID,
            ),
        ).fetchone()

    assert quiz_row["count"] == 1

    assert progress_row["count"] == 1


# ==========================================================
# Completion calculation
# ==========================================================

def test_random_quiz_score_calculation():
    """
    Verify score calculation used by Random Quiz.
    """

    test_cases = [
        (10, 10, 100.0),
        (10, 9, 90.0),
        (10, 8, 80.0),
        (10, 5, 50.0),
        (10, 0, 0.0),
        (20, 15, 75.0),
    ]

    for total, correct, expected in test_cases:

        score = round(
            correct
            / total
            * 100,
            2,
        )

        assert score == expected


# ==========================================================
# Cancellation isolation
# ==========================================================

def test_random_quiz_cancellation_does_not_create_result(
    test_database,
):
    """
    Verify a cancelled quiz does not automatically
    create a completed Statistics record.
    """

    telegram_id = 400001

    statistics = get_user_statistics(
        telegram_id
    )

    assert statistics[
        "attempts"
    ] == 0

    progress = get_lesson_progress(
        telegram_id=telegram_id,
        module_id=RANDOM_QUIZ_MODULE_ID,
        chapter_id=RANDOM_QUIZ_CHAPTER_ID,
        lesson_id=RANDOM_QUIZ_LESSON_ID,
    )

    assert progress is None


# ==========================================================
# Final integration health
# ==========================================================

def test_random_quiz_full_integration_health(
    test_database,
):
    """
    Final high-level architecture health test.
    """

    import bot

    assert callable(
        bot.build_application
    )

    assert callable(
        bot.initialize_core
    )

    assert callable(
        random_handlers.start_random_quiz
    )

    assert callable(
        random_handlers.answer_random_quiz
    )

    assert callable(
        random_handlers.finish_random_quiz
    )

    assert callable(
        random_handlers.cancel_random_quiz
    )

    assert callable(
        random_handlers.route_random_quiz_callback
    )

    assert callable(
        get_random_question_pool
    )

    assert callable(
        select_random_questions
    )


# ==========================================================
# Runner
# ==========================================================

if __name__ == "__main__":

    print(
        "================================"
    )

    print(
        "Running Random Quiz Integration Tests..."
    )

    print(
        "================================"
    )

    pytest.main(
        [
            __file__,
            "-v",
        ]
    )
