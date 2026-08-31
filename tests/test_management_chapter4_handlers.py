"""
Management Chapter 4 Handler Test
Tests:
- Chapter 4 registration
- Lessons 27-36 registration
- Lesson lookup
- Lesson location
- Lesson ordering
- Required lesson content
- Quiz field
- Previous/next navigation
- Quiz callback
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
# ==========================================================
# Expected Chapter 4 Lessons
# ==========================================================
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
# ==========================================================
# Chapter 4 Registration
# ==========================================================
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
def test_chapter_4_lessons_are_ordered():
    """Lessons must remain in 27-36 order."""
    lessons = get_chapter_lessons(
        "leadership"
    )
    assert [
        lesson["id"]
        for lesson in lessons
    ] == EXPECTED_LESSON_IDS
# ==========================================================
# Global Lesson Registration
# ==========================================================
@pytest.mark.parametrize(
    "lesson_id",
    EXPECTED_LESSON_IDS,
)
def test_chapter_4_lessons_exist_in_management_lessons(
    lesson_id,
):
    """Every Chapter 4 lesson must be globally registered."""
    assert lesson_id in MANAGEMENT_LESSONS
# ==========================================================
# Lesson Lookup
# ==========================================================
@pytest.mark.parametrize(
    "index, lesson_id",
    list(
        enumerate(
            EXPECTED_LESSON_IDS
        )
    ),
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
# ==========================================================
# Lesson Location
# ==========================================================
@pytest.mark.parametrize(
    "lesson_id",
    EXPECTED_LESSON_IDS,
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
# ==========================================================
# Lesson Index
# ==========================================================
@pytest.mark.parametrize(
    "index, lesson_id",
    list(
        enumerate(
            EXPECTED_LESSON_IDS
        )
    ),
)
def test_lesson_index_for_chapter_4(
    index,
    lesson_id,
):
    """Every lesson must have the correct index."""
    assert (
        get_lesson_index(
            lesson_id
        )
        == index
    )
# ==========================================================
# Lesson Content
# ==========================================================
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_lesson_has_required_content(
    index,
):
    """Every Chapter 4 lesson must have core fields."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
    assert lesson.get("id")
    assert lesson.get("title")
    assert (
        lesson.get("lesson")
        is not None
    )
    assert isinstance(
        lesson.get(
            "objectives",
            [],
        ),
        list,
    )
    assert isinstance(
        lesson.get(
            "key_concepts",
            [],
        ),
        list,
    )
    assert isinstance(
        lesson.get(
            "specialized_points",
            [],
        ),
        list,
    )
    assert isinstance(
        lesson.get(
            "exam_points",
            [],
        ),
        list,
    )
    assert isinstance(
        lesson.get(
            "review",
            [],
        ),
        list,
    )
# ==========================================================
# Quiz Field
# ==========================================================
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
# ==========================================================
# Navigation Helpers
# ==========================================================
def get_callbacks(
    keyboard,
):
    """Return all callback data from an inline keyboard."""
    return [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
        if button.callback_data
    ]
def test_chapter_4_first_lesson_has_no_previous_navigation():
    """Lesson 27 must not have a previous lesson."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[0]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        0,
        lesson,
    )
    callbacks = get_callbacks(
        keyboard
    )
    assert (
        "management_lesson:leadership:-1"
        not in callbacks
    )
def test_chapter_4_middle_lesson_has_navigation():
    """A middle lesson must provide previous and next navigation."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[4]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        4,
        lesson,
    )
    callbacks = get_callbacks(
        keyboard
    )
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
    callbacks = get_callbacks(
        keyboard
    )
    assert (
        "management_lesson:leadership:10"
        not in callbacks
    )
# ==========================================================
# Navigation Boundary Test
# ==========================================================
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_navigation_stays_inside_chapter(
    index,
):
    """Navigation must never jump outside Chapter 4."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[
        index
    ]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        index,
        lesson,
    )
    callbacks = get_callbacks(
        keyboard
    )
    for callback in callbacks:
        if callback.startswith(
            "management_lesson:"
        ):
            assert callback.startswith(
                "management_lesson:leadership:"
            )
# ==========================================================
# Quiz Callback
# ==========================================================
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_quiz_callback_uses_lesson_id(
    index,
):
    """Quiz button must point to the current lesson."""
    lesson = MANAGEMENT_CHAPTER_04_LESSONS[
        index
    ]
    keyboard = lesson_navigation_keyboard(
        "leadership",
        index,
        lesson,
    )
    callbacks = get_callbacks(
        keyboard
    )
    if lesson.get("quiz"):
        assert (
            f"management_quiz:{lesson['id']}"
            in callbacks
        )
# ==========================================================
# Individual Lesson ID Sequence
# ==========================================================
def test_chapter_4_starts_with_lesson_27():
    """Chapter 4 must start with Lesson 27."""
    assert (
        MANAGEMENT_CHAPTER_04_LESSONS[0]["id"]
        == "lesson_27"
    )
def test_chapter_4_ends_with_lesson_36():
    """Chapter 4 must end with Lesson 36."""
    assert (
        MANAGEMENT_CHAPTER_04_LESSONS[-1]["id"]
        == "lesson_36"
    )
def test_chapter_4_contains_no_duplicate_lessons():
    """Chapter 4 must not contain duplicate lesson IDs."""
    lesson_ids = [
        lesson["id"]
        for lesson in MANAGEMENT_CHAPTER_04_LESSONS
    ]
    assert len(lesson_ids) == len(
        set(lesson_ids)
    )
# ==========================================================
# Complete Chapter 4 Integrity
# ==========================================================
def test_chapter_4_integrity():
    """
    Final integrity test.
    Chapter 4 must contain exactly ten unique lessons,
    ordered from Lesson 27 through Lesson 36.
    """
    lessons = get_chapter_lessons(
        "leadership"
    )
    assert len(lessons) == 10
    lesson_ids = [
        lesson["id"]
        for lesson in lessons
    ]
    assert len(
        lesson_ids
    ) == len(
        set(lesson_ids)
    )
    assert lesson_ids == [
        f"lesson_{number}"
        for number in range(
            27,
            37,
        )
    ]
    for lesson_id in lesson_ids:
        assert lesson_id in MANAGEMENT_LESSONS
