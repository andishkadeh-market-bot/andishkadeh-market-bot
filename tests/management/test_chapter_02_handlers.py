"""
Handler tests for Management Chapter 2.
"""

from modules.management.handlers import (
    MANAGEMENT_CHAPTER_02_LESSONS,
    MANAGEMENT_LESSONS,
    get_chapter_lessons,
    get_lesson_location,
    get_management_lesson,
    format_lesson_text,
    lesson_navigation_keyboard,
    quiz_keyboard,
)

from modules.management.lessons.lesson_13 import LESSON_13
from modules.management.lessons.lesson_14 import LESSON_14
from modules.management.lessons.lesson_15 import LESSON_15
from modules.management.lessons.lesson_16 import LESSON_16
from modules.management.lessons.lesson_17 import LESSON_17
from modules.management.lessons.lesson_18 import LESSON_18
from modules.management.lessons.lesson_19 import LESSON_19


def test_chapter_02_has_seven_handler_lessons():
    assert len(
        MANAGEMENT_CHAPTER_02_LESSONS
    ) == 7


def test_chapter_02_lessons_are_correct():
    expected = [
        LESSON_13,
        LESSON_14,
        LESSON_15,
        LESSON_16,
        LESSON_17,
        LESSON_18,
        LESSON_19,
    ]

    assert (
        MANAGEMENT_CHAPTER_02_LESSONS
        == expected
    )


def test_chapter_02_lessons_are_registered():
    for lesson in MANAGEMENT_CHAPTER_02_LESSONS:
        assert lesson["id"] in MANAGEMENT_LESSONS
        assert (
            MANAGEMENT_LESSONS[lesson["id"]]
            == lesson
        )


def test_planning_chapter_has_seven_lessons():
    lessons = get_chapter_lessons(
        "planning"
    )

    assert len(lessons) == 7


def test_planning_lessons_are_retrievable():
    for index in range(7):
        lesson = get_management_lesson(
            "planning",
            index,
        )

        assert lesson is not None
        assert lesson["id"].startswith(
            "management_02_"
        )


def test_chapter_02_lesson_locations_are_correct():
    expected_ids = [
        "management_02_01",
        "management_02_02",
        "management_02_03",
        "management_02_04",
        "management_02_05",
        "management_02_06",
        "management_02_07",
    ]

    for index, lesson_id in enumerate(
        expected_ids
    ):
        location = get_lesson_location(
            lesson_id
        )

        assert location == (
            "planning",
            index,
        )


def test_lesson_13_handler_content():
    lesson = get_management_lesson(
        "planning",
        0,
    )

    assert lesson["id"] == "management_02_01"
    assert "برنامه‌ریزی" in lesson["title"]


def test_lesson_19_handler_content():
    lesson = get_management_lesson(
        "planning",
        6,
    )

    assert lesson["id"] == "management_02_07"
    assert "تحلیل محیط" in lesson["title"]


def test_lesson_formatter_supports_chapter_02():
    for lesson in MANAGEMENT_CHAPTER_02_LESSONS:
        text = format_lesson_text(
            lesson
        )

        assert lesson["title"] in text
        assert "اهداف یادگیری" in text
        assert "درسنامه" in text
        assert "مفاهیم کلیدی" in text
        assert "نکات تخصصی" in text
        assert "نکات آزمونی" in text
        assert "مثال کاربردی" in text
        assert "مرور و جمع‌بندی" in text


def test_chapter_02_lessons_have_quizzes():
    for lesson in MANAGEMENT_CHAPTER_02_LESSONS:
        assert lesson["quiz"]
        assert len(
            lesson["quiz"]
        ) >= 5


def test_chapter_02_quiz_buttons_can_be_created():
    from core.quiz import (
        QuizSession,
        build_questions,
    )

    for lesson in MANAGEMENT_CHAPTER_02_LESSONS:
        questions = build_questions(
            lesson["quiz"]
        )

        session = QuizSession(
            questions
        )

        keyboard = quiz_keyboard(
            session
        )

        assert keyboard is not None
        assert keyboard.inline_keyboard


def test_chapter_02_navigation_keyboard():
    for index, lesson in enumerate(
        MANAGEMENT_CHAPTER_02_LESSONS
    ):
        keyboard = lesson_navigation_keyboard(
            chapter_id="planning",
            lesson_index=index,
            lesson=lesson,
        )

        assert keyboard is not None
        assert keyboard.inline_keyboard


def test_chapter_02_navigation_boundaries():
    first_keyboard = (
        lesson_navigation_keyboard(
            chapter_id="planning",
            lesson_index=0,
            lesson=LESSON_13,
        )
    )

    last_keyboard = (
        lesson_navigation_keyboard(
            chapter_id="planning",
            lesson_index=6,
            lesson=LESSON_19,
        )
    )

    assert first_keyboard.inline_keyboard
    assert last_keyboard.inline_keyboard
