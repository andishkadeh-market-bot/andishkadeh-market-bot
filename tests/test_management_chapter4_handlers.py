"""
Management Chapter 4 Handler Test
Tests:
- Lesson 27-36 registration
- Chapter 4 mapping
- Lesson lookup
- Lesson location
- Navigation
- Quiz availability
"""
import pytest
from modules.management.handlers import (
    MANAGEMENT_LESSONS,
    MANAGEMENT_CHAPTER_04_LESSONS,
    MANAGEMENT_CHAPTER_LESSONS,
    get_chapter_lessons,
    get_management_lesson,
    get_lesson_location,
    get_lesson_index,
    lesson_navigation_keyboard,
)
EXPECTED_LESSON_IDS = [
    "lesson_27",
    "lesson_28",
    "lesson_29",
    "lesson_30",
    "lesson_31",
    "lesson_32",
    "lesson_33",
    "lesson_34",
    "lesson_35",
    "lesson_36",
]
def test_chapter_4_contains_ten_lessons():
    """Chapter 4 must contain exactly Lessons 27-36."""
    lessons = MANAGEMENT_CHAPTER_04_LESSONS
    assert len(lessons) == 10
    lesson_ids = [
        lesson["id"]
        for lesson in lessons
    ]
    assert lesson_ids == EXPECTED_LESSON_IDS
def test_chapter_4_is_registered():
    """Leadership chapter must be registered."""
    assert "leadership" in MANAGEMENT_CHAPTER_LESSONS
    assert (
        MANAGEMENT_CHAPTER_LESSONS["leadership"]
        == MANAGEMENT_CHAPTER_04_LESSONS
    )
@pytest.mark.parametrize(
    "lesson_id",
    EXPECTED_LESSON_IDS,
)
def test_chapter_4_lessons_exist_in_management_lessons(
    lesson_id,
):
    """Every Chapter 4 lesson must be globally registered."""
    assert lesson_id in MANAGEMENT_LESSONS
@pytest.mark.parametrize(
    "index, lesson_id",
    list(enumerate(EXPECTED_LESSON_IDS)),
)
def test_get_management_lesson_for_chapter_4(
    index,
    lesson_id,
):
    """Lesson lookup must return the correct lesson."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
    assert lesson["id"] == lesson_id
@pytest.mark.parametrize(
    "lesson_id",
)
def test_lesson_location_for_chapter_4(
    lesson_id,
):
    """Every Chapter 4 lesson must resolve to leadership."""
    location = get_lesson_location(
        lesson_id
    )
    assert location is not None
    chapter_id, index = location
    assert chapter_id == "leadership"
    assert EXPECTED_LESSON_IDS[index] == lesson_id
@pytest.mark.parametrize(
    "index, lesson_id",
    list(enumerate(EXPECTED_LESSON_IDS)),
)
def test_lesson_index_for_chapter_4(
    index,
    lesson_id,
):
    """Every lesson must have the correct index."""
    assert (
        get_lesson_index(lesson_id)
        == index
    )
def test_chapter_4_lessons_are_ordered():
    """Lessons must remain in 27-36 order."""
    lessons = get_chapter_lessons(
        "leadership"
    )
    assert [
        lesson["id"]
        for lesson in lessons
    ] == EXPECTED_LESSON_IDS
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_lesson_has_required_content(
    index,
):
    """Every Chapter 4 lesson must have core educational fields."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
    assert lesson.get("id")
    assert lesson.get("title")
    assert lesson.get("lesson") is not None
    assert isinstance(
        lesson.get("objectives", []),
        list,
    )
    assert isinstance(
        lesson.get("key_concepts", []),
        list,
    )
    assert isinstance(
        lesson.get("specialized_points", []),
        list,
    )
    assert isinstance(
        lesson.get("exam_points", []),
        list,
    )
    assert isinstance(
        lesson.get("review", []),
        list,
    )
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_quiz_field_exists(
    index,
):
    """Every Chapter 4 lesson must expose a quiz field."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
    assert "quiz" in lesson
    assert isinstance(
        lesson["quiz"],
        list,
    )
def test_chapter_4_first_lesson_has_no_previous_navigation():
    """Lesson 27 must not have a previous lesson."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[0]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        0,
        lesson,
    )
    buttons = [
        button
        for row in keyboard.inline_keyboard
        for button in row
    ]
    callback_data = [
        button.callback_data
        for button in buttons
    ]
    assert not any(
        "management_lesson:leadership:-1"
        in callback
        for callback in callback_data
    )
def test_chapter_4_middle_lesson_has_navigation():
    """A middle lesson must provide previous and next navigation."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[4]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        4,
        lesson,
    )
    callbacks = [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
        if button.callback_data
    ]
    assert (
        "management_lesson:leadership:3"
        in callbacks
    )
    assert (
        "management_lesson:leadership:5"
        in callbacks
    )
def test_chapter_4_last_lesson_has_no_next_navigation():
    """Lesson 36 must not have a next lesson."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[-1]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        9,
        lesson,
    )
    callbacks = [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
        if button.callback_data
    ]
    assert not any(
        "management_lesson:leadership:10"
        in callback
        for callback in callbacks
    )
def test_chapter_4_navigation_stays_inside_chapter():
    """Navigation must not jump outside Chapter 4."""
    for index, lesson in enumerate(
        MANAGEMENT_CHAPTER_04_LESSONS
    ):
        keyboard = lesson_navigation_keyboard(
            "leadership",
            index,
            lesson,
        )
        callbacks = [
            button.callback_data
            for row in keyboard.inline_keyboard
            for button in row
            if button.callback_data
        ]
        for callback in callbacks:
            if callback.startswith(
                "management_lesson:"
            ):
                assert callback.startswith(
                    "management_lesson:leadership:"
                )
def test_chapter_4_quiz_callback_uses_lesson_id():
    """Quiz button must point to the current lesson."""
    for index, lesson in enumerate(
        MANAGEMENT_CHAPTER_04_LESSONS
    ):
        keyboard = lesson_navigation_keyboard(
            "leadership",
            index,
            lesson,
        )
        callbacks = [
            button.callback_data
            for row in keyboard.inline_keyboard
            for button in row
            if button.callback_data
        ]
        if lesson.get("quiz"):
            assert (
                f"management_quiz:{lesson['id']}"
                in callbacks
            )
