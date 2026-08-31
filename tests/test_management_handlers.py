import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from modules.management import handlers


# ==========================================================
# Helpers
# ==========================================================

def make_update(
    user_id: int = 1001,
    username: str = "test_user",
):
    update = MagicMock()

    update.effective_user.id = user_id
    update.effective_user.username = username
    update.effective_user.first_name = "Test"
    update.effective_user.last_name = "User"

    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()

    return update


# ==========================================================
# Structure tests
# ==========================================================

def test_management_has_50_lessons():

    assert len(
        handlers.MANAGEMENT_LESSONS
    ) == 50


def test_management_chapters_are_defined():

    assert len(
        handlers.MANAGEMENT_CHAPTER_LESSONS
    ) == 6


def test_chapter_01_has_12_lessons():

    assert len(
        handlers.MANAGEMENT_CHAPTER_01_LESSONS
    ) == 12


def test_chapter_02_has_7_lessons():

    assert len(
        handlers.MANAGEMENT_CHAPTER_02_LESSONS
    ) == 7


def test_chapter_03_has_7_lessons():

    assert len(
        handlers.MANAGEMENT_CHAPTER_03_LESSONS
    ) == 7


def test_chapter_04_has_10_lessons():

    assert len(
        handlers.MANAGEMENT_CHAPTER_04_LESSONS
    ) == 10


def test_chapter_05_has_7_lessons():

    assert len(
        handlers.MANAGEMENT_CHAPTER_05_LESSONS
    ) == 7


def test_chapter_06_has_7_lessons():

    assert len(
        handlers.MANAGEMENT_CHAPTER_06_LESSONS
    ) == 7


# ==========================================================
# Helper tests
# ==========================================================

def test_get_chapter():

    chapter = handlers.get_chapter(
        "management_basics"
    )

    assert chapter is not None
    assert chapter["id"] == "management_basics"


def test_get_invalid_chapter():

    chapter = handlers.get_chapter(
        "invalid_chapter"
    )

    assert chapter is None


def test_get_chapter_lessons():

    lessons = handlers.get_chapter_lessons(
        "planning"
    )

    assert len(lessons) == 7


def test_get_management_lesson():

    lesson = handlers.get_management_lesson(
        "planning",
        0,
    )

    assert lesson is not None
    assert lesson["id"]


def test_get_invalid_lesson():

    lesson = handlers.get_management_lesson(
        "planning",
        999,
    )

    assert lesson is None


def test_get_lesson_location():

    location = handlers.get_lesson_location(
        handlers.LESSON_20["id"]
    )

    assert location is not None
    assert location[0] == "organizing"


def test_get_lesson_index():

    index = handlers.get_lesson_index(
        handlers.LESSON_20["id"]
    )

    assert index == 0


# ==========================================================
# Keyboard tests
# ==========================================================

def test_management_menu_keyboard():

    keyboard = (
        handlers.management_menu_keyboard()
    )

    assert keyboard.inline_keyboard
    assert len(
        keyboard.inline_keyboard
    ) >= 7


def test_chapter_keyboard():

    keyboard = (
        handlers.management_chapter_keyboard(
            "planning"
        )
    )

    assert keyboard.inline_keyboard


def test_lesson_navigation_keyboard():

    lesson = handlers.LESSON_13

    keyboard = (
        handlers.lesson_navigation_keyboard(
            "planning",
            0,
            lesson,
        )
    )

    assert keyboard.inline_keyboard


# ==========================================================
# Lesson formatting
# ==========================================================

def test_format_lesson_text():

    lesson = handlers.LESSON_01

    text = handlers.format_lesson_text(
        lesson
    )

    assert lesson["title"] in text
    assert "اهداف یادگیری" in text
    assert "درسنامه" in text
    assert "مفاهیم کلیدی" in text


# ==========================================================
# Progress registration
# ==========================================================

def test_register_lesson_started():

    with patch(
        "modules.management.handlers.start_lesson"
    ) as mocked_start:

        handlers.register_lesson_started(
            telegram_id=1001,
            chapter_id="planning",
            lesson_id=handlers.LESSON_13["id"],
        )

    mocked_start.assert_called_once_with(
        telegram_id=1001,
        module_id="management",
        chapter_id="planning",
        lesson_id=handlers.LESSON_13["id"],
    )


def test_register_lesson_completed():

    with patch(
        "modules.management.handlers.complete_lesson"
    ) as mocked_complete:

        handlers.register_lesson_completed(
            telegram_id=1001,
            chapter_id="planning",
            lesson_id=handlers.LESSON_13["id"],
        )

    mocked_complete.assert_called_once_with(
        telegram_id=1001,
        module_id="management",
        chapter_id="planning",
        lesson_id=handlers.LESSON_13["id"],
    )


def test_register_progress_error_does_not_break():

    with patch(
        "modules.management.handlers.start_lesson",
        side_effect=RuntimeError(
            "database error"
        ),
    ):

        handlers.register_lesson_started(
            telegram_id=1001,
            chapter_id="planning",
            lesson_id=handlers.LESSON_13["id"],
        )


# ==========================================================
# Statistics registration
# ==========================================================

def test_register_quiz_result():

    with patch(
        "modules.management.handlers.record_quiz_result"
    ) as mocked_record:

        handlers.register_quiz_result(
            telegram_id=1001,
            chapter_id="planning",
            lesson_id=handlers.LESSON_13["id"],
            total_questions=10,
            correct_answers=8,
            score=80.0,
        )

    mocked_record.assert_called_once_with(
        telegram_id=1001,
        module_id="management",
        chapter_id="planning",
        lesson_id=handlers.LESSON_13["id"],
        total_questions=10,
        correct_answers=8,
        score=80.0,
    )


def test_register_statistics_error_does_not_break():

    with patch(
        "modules.management.handlers.record_quiz_result",
        side_effect=RuntimeError(
            "statistics error"
        ),
    ):

        handlers.register_quiz_result(
            telegram_id=1001,
            chapter_id="planning",
            lesson_id=handlers.LESSON_13["id"],
            total_questions=10,
            correct_answers=8,
            score=80.0,
        )


# ==========================================================
# Lesson integration
# ==========================================================

def test_show_management_lesson_registers_progress():

    update = make_update()

    update.callback_query.data = (
        "management_lesson:"
        "planning:0"
    )

    context = MagicMock()

    with patch(
        "modules.management.handlers.register_lesson_started"
    ) as mocked_start:

        with patch(
            "modules.management.handlers.send_long_text",
            new=AsyncMock(),
        ):

            asyncio.run(
                handlers.show_management_lesson(
                    update,
                    context,
                )
            )

    mocked_start.assert_called_once()

    call = mocked_start.call_args

    assert (
        call.kwargs["telegram_id"]
        == 1001
    )

    assert (
        call.kwargs["chapter_id"]
        == "planning"
    )

    assert (
        call.kwargs["lesson_id"]
        == handlers.LESSON_13["id"]
    )


# ==========================================================
# Quiz start
# ==========================================================

def test_start_management_quiz():

    update = make_update(
        user_id=2001
    )

    update.callback_query.data = (
        "management_quiz:"
        f"{handlers.LESSON_13['id']}"
    )

    context = MagicMock()

    handlers.QUIZ_SESSIONS.clear()
    handlers.QUIZ_LESSON_CONTEXT.clear()

    with patch(
        "modules.management.handlers.register_lesson_started"
    ) as mocked_start:

        asyncio.run(
            handlers.start_management_quiz(
                update,
                context,
            )
        )

    assert 2001 in (
        handlers.QUIZ_SESSIONS
    )

    assert 2001 in (
        handlers.QUIZ_LESSON_CONTEXT
    )

    mocked_start.assert_called_once()


# ==========================================================
# Quiz result integration
# ==========================================================

def test_finished_quiz_records_statistics_and_completion():

    user_id = 3001

    update = make_update(
        user_id=user_id
    )

    update.callback_query.data = (
        "quiz_answer:0"
    )

    context = MagicMock()

    question = MagicMock()
    question.question = "Test question"
    question.options = [
        "Correct",
        "Wrong",
    ]
    question.answer = 0
    question.explanation = "Explanation"

    session = MagicMock()

    session.current_question = question
    session.is_finished = True
    session.total_questions = 1

    result = MagicMock()
    result.total = 1
    result.correct = 1
    result.wrong = 0
    result.percentage = 100.0

    session.answer.return_value = True
    session.result.return_value = result

    handlers.QUIZ_SESSIONS[user_id] = session

    handlers.QUIZ_LESSON_CONTEXT[user_id] = {
        "lesson_id": handlers.LESSON_13["id"],
        "chapter_id": "planning",
        "lesson_index": 0,
    }

    with patch(
        "modules.management.handlers.register_quiz_result"
    ) as mocked_result:

        with patch(
            "modules.management.handlers.register_lesson_completed"
        ) as mocked_completed:

            asyncio.run(
                handlers.answer_management_quiz(
                    update,
                    context,
                )
            )

    mocked_result.assert_called_once()

    mocked_completed.assert_called_once()

    assert (
        user_id
        not in handlers.QUIZ_SESSIONS
    )

    assert (
        user_id
        not in handlers.QUIZ_LESSON_CONTEXT
    )


# ==========================================================
# Cancel quiz
# ==========================================================

def test_cancel_management_quiz():

    user_id = 4001

    update = make_update(
        user_id=user_id
    )

    update.callback_query.data = (
        "quiz_cancel"
    )

    context = MagicMock()

    handlers.QUIZ_SESSIONS[user_id] = MagicMock()

    handlers.QUIZ_LESSON_CONTEXT[user_id] = {
        "lesson_id": handlers.LESSON_13["id"],
        "chapter_id": "planning",
        "lesson_index": 0,
    }

    asyncio.run(
        handlers.cancel_management_quiz(
            update,
            context,
        )
    )

    assert (
        user_id
        not in handlers.QUIZ_SESSIONS
    )

    assert (
        user_id
        not in handlers.QUIZ_LESSON_CONTEXT
    )
