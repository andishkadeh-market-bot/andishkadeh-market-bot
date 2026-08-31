"""
Management Chapter 4 Integration Test
Integration coverage:
- Chapter 4 registration
- Lessons 27-36
- Curriculum -> Handler mapping
- Lesson lookup
- Lesson navigation
- Quiz availability
- Quiz callback mapping
- Chapter boundaries
- Full Chapter 4 integrity
"""
import pytest
from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)
from modules.management.handlers import (
    MANAGEMENT_LESSONS,
    MANAGEMENT_CHAPTER_04_LESSONS,
    MANAGEMENT_CHAPTER_LESSONS,
    get_chapter,
    get_chapter_lessons,
    get_management_lesson,
    get_lesson_location,
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
# ==========================================================
# Curriculum
# ==========================================================
def test_chapter_4_exists_in_curriculum():
    """Chapter 4 must exist in the management curriculum."""
    chapter = next(
        (
            chapter
            for chapter in MANAGEMENT_CURRICULUM
            if chapter["id"] == "leadership"
        ),
        None,
    )
    assert chapter is not None
def test_chapter_4_handler_mapping_exists():
    """Chapter 4 must be connected to its handler lesson list."""
    assert "leadership" in MANAGEMENT_CHAPTER_LESSONS
    assert (
        MANAGEMENT_CHAPTER_LESSONS["leadership"]
        == MANAGEMENT_CHAPTER_04_LESSONS
    )
# ==========================================================
# Curriculum -> Handler Lesson Count
# ==========================================================
def test_chapter_4_curriculum_has_expected_lessons():
    """
    Curriculum and detailed lesson content must both
    represent the complete Chapter 4 sequence.
    """
    chapter = get_chapter(
        "leadership"
    )
    assert chapter is not None
    curriculum_lessons = chapter.get(
        "lessons",
        [],
    )
    handler_lessons = get_chapter_lessons(
        "leadership"
    )
    assert len(handler_lessons) == 10
    assert len(curriculum_lessons) >= 10
# ==========================================================
# Lesson Sequence
# ==========================================================
def test_chapter_4_complete_sequence():
    """Chapter 4 must contain Lessons 27-36 in order."""
    lessons = get_chapter_lessons(
        "leadership"
    )
    lesson_ids = [
        lesson["id"]
        for lesson in lessons
    ]
    assert lesson_ids == EXPECTED_LESSON_IDS
def test_chapter_4_has_no_duplicate_lessons():
    """No Chapter 4 lesson may appear more than once."""
    lessons = get_chapter_lessons(
        "leadership"
    )
    lesson_ids = [
        lesson["id"]
        for lesson in lessons
    ]
    assert len(lesson_ids) == len(
        set(lesson_ids)
    )
# ==========================================================
# Global Lesson Registry
# ==========================================================
@pytest.mark.parametrize(
    "lesson_id",
    EXPECTED_LESSON_IDS,
)
def test_every_chapter_4_lesson_is_registered(
    lesson_id,
):
    """Every Chapter 4 lesson must exist globally."""
    assert lesson_id in MANAGEMENT_LESSONS
# ==========================================================
# Lesson Lookup Integration
# ==========================================================
@pytest.mark.parametrize(
    "index, lesson_id",
    list(
        enumerate(
            EXPECTED_LESSON_IDS
        )
    ),
)
def test_lesson_lookup_returns_correct_lesson(
    index,
    lesson_id,
):
    """Handler lookup must return the expected lesson."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
    assert lesson["id"] == lesson_id
    assert (
        MANAGEMENT_LESSONS[lesson_id]
        is lesson
    )
# ==========================================================
# Lesson Location Integration
# ==========================================================
@pytest.mark.parametrize(
    "index, lesson_id",
    list(
        enumerate(
            EXPECTED_LESSON_IDS
        )
    ),
)
def test_lesson_location_matches_chapter_and_index(
    index,
    lesson_id,
):
    """Every lesson must resolve to Chapter 4 correctly."""
    location = get_lesson_location(
        lesson_id
    )
    assert location is not None
    chapter_id, lesson_index = location
    assert chapter_id == "leadership"
    assert lesson_index == index
# ==========================================================
# Lesson Content Integration
# ==========================================================
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_lesson_has_complete_structure(
    index,
):
    """Every Chapter 4 lesson must expose the expected fields."""
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
    assert isinstance(
        lesson.get(
            "quiz",
            [],
        ),
        list,
    )
# ==========================================================
# Quiz Integration
# ==========================================================
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_quiz_data_is_available(
    index,
):
    """Every Chapter 4 lesson must expose quiz data."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
    quiz = lesson.get(
        "quiz",
        [],
    )
    assert isinstance(
        quiz,
        list,
    )
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_quiz_callback_matches_lesson(
    index,
):
    """Quiz navigation must point to the current lesson."""
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
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
# ==========================================================
# Navigation Integration
# ==========================================================
def get_callbacks(
    keyboard,
):
    """Extract callback data from an inline keyboard."""
    return [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
        if button.callback_data
    ]
def test_lesson_27_is_first_lesson():
    """Lesson 27 must be the first Chapter 4 lesson."""
    lesson = get_management_lesson(
        "leadership",
        0,
    )
    assert lesson is not None
    assert lesson["id"] == "lesson_27"
def test_lesson_36_is_last_lesson():
    """Lesson 36 must be the last Chapter 4 lesson."""
    lesson = get_management_lesson(
        "leadership",
        9,
    )
    assert lesson is not None
    assert lesson["id"] == "lesson_36"
def test_lesson_27_has_no_previous_lesson():
    """Lesson 27 cannot navigate to Lesson 26 through Chapter 4 navigation."""
    lesson = get_management_lesson(
        "leadership",
        0,
    )
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
def test_lesson_27_navigates_to_lesson_28():
    """Lesson 27 must navigate forward to Lesson 28."""
    lesson = get_management_lesson(
        "leadership",
        0,
    )
    keyboard = lesson_navigation_keyboard(
        "leadership",
        0,
        lesson,
    )
    callbacks = get_callbacks(
        keyboard
    )
    assert (
        "management_lesson:leadership:1"
        in callbacks
    )
def test_lesson_28_navigates_back_to_lesson_27():
    """Lesson 28 must navigate backward to Lesson 27."""
    lesson = get_management_lesson(
        "leadership",
        1,
    )
    keyboard = lesson_navigation_keyboard(
        "leadership",
        1,
        lesson,
    )
    callbacks = get_callbacks(
        keyboard
    )
    assert (
        "management_lesson:leadership:0"
        in callbacks
    )
def test_lesson_36_has_no_next_lesson():
    """Lesson 36 cannot navigate forward beyond Chapter 4."""
    lesson = get_management_lesson(
        "leadership",
        9,
    )
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
# Cross-Chapter Boundary
# ==========================================================
@pytest.mark.parametrize(
    "index",
    range(10),
)
def test_chapter_4_navigation_stays_inside_chapter(
    index,
):
    """
    All previous/next lesson callbacks generated
    inside Chapter 4 must remain inside Chapter 4.
    """
    lesson = get_management_lesson(
        "leadership",
        index,
    )
    assert lesson is not None
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
# Complete Integration Integrity
# ==========================================================
def test_management_chapter_4_full_integration():
    """
    Final integration check for Chapter 4.
    Curriculum
        ↓
    Handler mapping
        ↓
    Lessons 27-36
        ↓
    Global lesson registry
        ↓
    Lesson lookup
        ↓
    Lesson location
        ↓
    Navigation
        ↓
    Quiz callback
    """
    chapter = get_chapter(
        "leadership"
    )
    assert chapter is not None
    lessons = get_chapter_lessons(
        "leadership"
    )
    assert len(lessons) == 10
    for index, expected_id in enumerate(
        EXPECTED_LESSON_IDS
    ):
        lesson = get_management_lesson(
            "leadership",
            index,
        )
        assert lesson is not None
        assert lesson["id"] == expected_id
        assert expected_id in MANAGEMENT_LESSONS
        location = get_lesson_location(
            expected_id
        )
        assert location == (
            "leadership",
            index,
        )
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
                f"management_quiz:{expected_id}"
                in callbacks
            )
