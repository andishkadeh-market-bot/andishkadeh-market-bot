"""
Integration tests for Management Chapter 3.

Covers the complete Chapter 3 flow:

Curriculum
    ↓
Lesson 20-26
    ↓
Management lesson registry
    ↓
Lesson lookup
    ↓
Lesson navigation
    ↓
Quiz availability
    ↓
Quiz question generation
"""

import importlib

import pytest


CURRICULUM_MODULE = (
    "modules.management.curriculum"
)

HANDLERS_MODULE = (
    "modules.management.handlers"
)

CHAPTER_ID = "organizing"

EXPECTED_LESSON_IDS = [
    "management_03_01",
    "management_03_02",
    "management_03_03",
    "management_03_04",
    "management_03_05",
    "management_03_06",
    "management_03_07",
]


LESSON_MODULES = [
    "modules.management.lessons.lesson_20",
    "modules.management.lessons.lesson_21",
    "modules.management.lessons.lesson_22",
    "modules.management.lessons.lesson_23",
    "modules.management.lessons.lesson_24",
    "modules.management.lessons.lesson_25",
    "modules.management.lessons.lesson_26",
]


LESSON_VARIABLES = [
    "LESSON_20",
    "LESSON_21",
    "LESSON_22",
    "LESSON_23",
    "LESSON_24",
    "LESSON_25",
    "LESSON_26",
]


# ==========================================================
# Helpers
# ==========================================================

def load_curriculum():
    """Load management curriculum."""

    return importlib.import_module(
        CURRICULUM_MODULE
    )


def load_handlers():
    """Load management handlers."""

    return importlib.import_module(
        HANDLERS_MODULE
    )


def load_chapter_3_lessons():
    """Load Lessons 20-26."""

    lessons = []

    for module_name, variable_name in zip(
        LESSON_MODULES,
        LESSON_VARIABLES,
    ):
        module = importlib.import_module(
            module_name
        )

        assert hasattr(
            module,
            variable_name,
        ), (
            f"{module_name} must contain "
            f"{variable_name}"
        )

        lesson = getattr(
            module,
            variable_name,
        )

        assert isinstance(
            lesson,
            dict,
        )

        lessons.append(
            lesson
        )

    return lessons


# ==========================================================
# Curriculum integration
# ==========================================================

def test_chapter_3_exists_in_curriculum():
    """Chapter 3 must exist in the curriculum."""

    curriculum = load_curriculum()

    assert hasattr(
        curriculum,
        "MANAGEMENT_CURRICULUM",
    )

    chapter = next(
        (
            item
            for item in curriculum.MANAGEMENT_CURRICULUM
            if item["id"] == CHAPTER_ID
        ),
        None,
    )

    assert chapter is not None


def test_chapter_3_curriculum_has_seven_lessons():
    """Chapter 3 curriculum must contain seven lessons."""

    curriculum = load_curriculum()

    chapter = next(
        (
            item
            for item in curriculum.MANAGEMENT_CURRICULUM
            if item["id"] == CHAPTER_ID
        ),
        None,
    )

    assert chapter is not None

    assert len(
        chapter["lessons"]
    ) == 7


# ==========================================================
# Lesson integration
# ==========================================================

def test_chapter_3_lesson_count():
    """Lessons 20-26 must contain exactly seven lessons."""

    lessons = load_chapter_3_lessons()

    assert len(lessons) == 7


def test_chapter_3_lesson_ids():
    """Lesson IDs must match the expected Chapter 3 sequence."""

    lessons = load_chapter_3_lessons()

    actual_ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert actual_ids == (
        EXPECTED_LESSON_IDS
    )


def test_chapter_3_lessons_have_unique_ids():
    """All Chapter 3 lesson IDs must be unique."""

    lessons = load_chapter_3_lessons()

    ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert len(ids) == len(
        set(ids)
    )


# ==========================================================
# Handler registry integration
# ==========================================================

def test_chapter_3_is_registered_in_handlers():
    """Chapter 3 must be registered in handler mappings."""

    handlers = load_handlers()

    assert CHAPTER_ID in (
        handlers.MANAGEMENT_CHAPTER_LESSONS
    )


def test_all_chapter_3_lessons_are_registered():
    """Every Chapter 3 lesson must exist in MANAGEMENT_LESSONS."""

    handlers = load_handlers()

    lessons = load_chapter_3_lessons()

    for lesson in lessons:
        lesson_id = lesson["id"]

        assert lesson_id in (
            handlers.MANAGEMENT_LESSONS
        )


def test_handler_registry_points_to_correct_lessons():
    """Registry entries must reference the correct lesson objects."""

    handlers = load_handlers()

    lessons = load_chapter_3_lessons()

    for lesson in lessons:
        lesson_id = lesson["id"]

        assert (
            handlers.MANAGEMENT_LESSONS[
                lesson_id
            ]
            is lesson
        )


# ==========================================================
# Chapter mapping integration
# ==========================================================

def test_chapter_3_handler_mapping_has_seven_lessons():
    """Handler chapter mapping must contain seven lessons."""

    handlers = load_handlers()

    lessons = handlers.MANAGEMENT_CHAPTER_LESSONS[
        CHAPTER_ID
    ]

    assert len(lessons) == 7


def test_handler_mapping_order_matches_lessons():
    """Handler mapping order must match Lessons 20-26."""

    handlers = load_handlers()

    mapped_lessons = (
        handlers.MANAGEMENT_CHAPTER_LESSONS[
            CHAPTER_ID
        ]
    )

    actual_ids = [
        lesson["id"]
        for lesson in mapped_lessons
    ]

    assert actual_ids == (
        EXPECTED_LESSON_IDS
    )


# ==========================================================
# Lesson lookup integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index, expected_id",
    [
        (0, "management_03_01"),
        (1, "management_03_02"),
        (2, "management_03_03"),
        (3, "management_03_04"),
        (4, "management_03_05"),
        (5, "management_03_06"),
        (6, "management_03_07"),
    ],
)
def test_lesson_lookup_integration(
    lesson_index,
    expected_id,
):
    """Each lesson index must resolve to the correct lesson."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    assert lesson is not None

    assert lesson["id"] == expected_id


# ==========================================================
# Lesson location integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_lesson_location_integration(
    lesson_index,
):
    """Every Chapter 3 lesson must resolve to its chapter and index."""

    handlers = load_handlers()

    lessons = load_chapter_3_lessons()

    lesson_id = lessons[
        lesson_index
    ]["id"]

    location = (
        handlers.get_lesson_location(
            lesson_id
        )
    )

    assert location == (
        CHAPTER_ID,
        lesson_index,
    )


# ==========================================================
# Lesson index integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_lesson_index_integration(
    lesson_index,
):
    """Every Chapter 3 lesson must return its correct index."""

    handlers = load_handlers()

    lessons = load_chapter_3_lessons()

    lesson_id = lessons[
        lesson_index
    ]["id"]

    result = handlers.get_lesson_index(
        lesson_id
    )

    assert result == lesson_index


# ==========================================================
# Lesson formatting integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_lesson_formatting_integration(
    lesson_index,
):
    """Every Chapter 3 lesson must be formatable."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    assert lesson is not None

    text = handlers.format_lesson_text(
        lesson
    )

    assert isinstance(
        text,
        str,
    )

    assert text.strip()

    assert lesson["title"] in text

    assert "اهداف یادگیری" in text

    assert "درسنامه" in text

    assert "مفاهیم کلیدی" in text

    assert "نکات تخصصی" in text

    assert "نکات آزمونی" in text

    assert "مثال کاربردی" in text

    assert "مرور و جمع‌بندی" in text


# ==========================================================
# Navigation integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_lesson_navigation_integration(
    lesson_index,
):
    """Every Chapter 3 lesson must produce a navigation keyboard."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    assert lesson is not None

    keyboard = (
        handlers.lesson_navigation_keyboard(
            CHAPTER_ID,
            lesson_index,
            lesson,
        )
    )

    assert keyboard is not None

    assert hasattr(
        keyboard,
        "inline_keyboard",
    )

    assert len(
        keyboard.inline_keyboard
    ) > 0


# ==========================================================
# Navigation callbacks
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_lesson_navigation_has_chapter_callback(
    lesson_index,
):
    """Every lesson must link back to Chapter 3."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    keyboard = (
        handlers.lesson_navigation_keyboard(
            CHAPTER_ID,
            lesson_index,
            lesson,
        )
    )

    callbacks = [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
        if button.callback_data
    ]

    assert (
        f"management_chapter:{CHAPTER_ID}"
        in callbacks
    )


# ==========================================================
# Quiz integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_lesson_quiz_exists(
    lesson_index,
):
    """Every Chapter 3 lesson must have quiz data."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    assert lesson is not None

    assert "quiz" in lesson

    assert isinstance(
        lesson["quiz"],
        list,
    )

    assert len(
        lesson["quiz"]
    ) > 0


@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_quiz_questions_can_be_built(
    lesson_index,
):
    """Quiz questions for every lesson must be buildable."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    assert lesson is not None

    from core.quiz import build_questions

    questions = build_questions(
        lesson["quiz"]
    )

    assert isinstance(
        questions,
        list,
    )

    assert len(
        questions
    ) > 0


# ==========================================================
# Quiz button integration
# ==========================================================

@pytest.mark.parametrize(
    "lesson_index",
    range(7),
)
def test_quiz_button_exists_for_every_lesson(
    lesson_index,
):
    """Every Chapter 3 lesson must expose a quiz button."""

    handlers = load_handlers()

    lesson = handlers.get_management_lesson(
        CHAPTER_ID,
        lesson_index,
    )

    keyboard = (
        handlers.lesson_navigation_keyboard(
            CHAPTER_ID,
            lesson_index,
            lesson,
        )
    )

    callbacks = [
        button.callback_data
        for row in keyboard.inline_keyboard
        for button in row
        if button.callback_data
    ]

    expected = (
        f"management_quiz:"
        f"{lesson['id']}"
    )

    assert expected in callbacks


# ==========================================================
# Complete Chapter 3 flow
# ==========================================================

def test_complete_chapter_3_flow():
    """
    Validate the complete Chapter 3 chain:

    curriculum
        ->
    lessons
        ->
    registry
        ->
    lookup
        ->
    location
        ->
    formatting
        ->
    navigation
        ->
    quiz
    """

    curriculum = load_curriculum()
    handlers = load_handlers()

    chapter = next(
        (
            item
            for item in curriculum.MANAGEMENT_CURRICULUM
            if item["id"] == CHAPTER_ID
        ),
        None,
    )

    assert chapter is not None

    lessons = handlers.MANAGEMENT_CHAPTER_LESSONS[
        CHAPTER_ID
    ]

    assert len(lessons) == 7

    for index, lesson in enumerate(
        lessons
    ):
        # Registry
        assert lesson["id"] in (
            handlers.MANAGEMENT_LESSONS
        )

        # Lookup
        loaded = handlers.get_management_lesson(
            CHAPTER_ID,
            index,
        )

        assert loaded is lesson

        # Location
        location = (
            handlers.get_lesson_location(
                lesson["id"]
            )
        )

        assert location == (
            CHAPTER_ID,
            index,
        )

        # Formatting
        text = handlers.format_lesson_text(
            lesson
        )

        assert text.strip()

        # Navigation
        keyboard = (
            handlers.lesson_navigation_keyboard(
                CHAPTER_ID,
                index,
                lesson,
            )
        )

        assert keyboard is not None

        # Quiz
        assert lesson["quiz"]

    assert [
        lesson["id"]
        for lesson in lessons
    ] == EXPECTED_LESSON_IDS
