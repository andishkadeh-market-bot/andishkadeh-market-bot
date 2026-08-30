"""
Integration tests for the Management education module.
"""

from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)

from modules.management.lessons.lesson_01 import (
    LESSON_01,
)

from modules.management.lessons.lesson_02 import (
    LESSON_02,
)

from modules.management.lessons.lesson_03 import (
    LESSON_03,
)

from modules.management.lessons.lesson_04 import (
    LESSON_04,
)

from modules.management.handlers import (
    MANAGEMENT_LESSONS,
    management_menu_keyboard,
    management_chapter_keyboard,
    get_management_lesson,
)


# ==========================================================
# Curriculum
# ==========================================================

def test_management_curriculum_exists():
    assert MANAGEMENT_CURRICULUM
    assert isinstance(
        MANAGEMENT_CURRICULUM,
        list,
    )


def test_management_basics_chapter_exists():
    chapter = next(
        (
            item
            for item in MANAGEMENT_CURRICULUM
            if item["id"] == "management_basics"
        ),
        None,
    )

    assert chapter is not None
    assert len(chapter["lessons"]) >= 4


# ==========================================================
# Lesson registration
# ==========================================================

def test_first_four_lessons_are_registered():
    assert LESSON_01["id"] in MANAGEMENT_LESSONS
    assert LESSON_02["id"] in MANAGEMENT_LESSONS
    assert LESSON_03["id"] in MANAGEMENT_LESSONS
    assert LESSON_04["id"] in MANAGEMENT_LESSONS


def test_lessons_have_required_structure():
    lessons = [
        LESSON_01,
        LESSON_02,
        LESSON_03,
        LESSON_04,
    ]

    required_fields = [
        "id",
        "title",
        "objectives",
        "lesson",
        "key_concepts",
        "specialized_points",
        "exam_points",
        "practical_example",
        "review",
        "quiz",
    ]

    for lesson in lessons:
        for field in required_fields:
            assert field in lesson

        assert lesson["id"]
        assert lesson["title"]
        assert lesson["lesson"]
        assert lesson["quiz"]


# ==========================================================
# Quiz availability
# ==========================================================

def test_first_four_lessons_have_quiz():
    lessons = [
        LESSON_01,
        LESSON_02,
        LESSON_03,
        LESSON_04,
    ]

    for lesson in lessons:
        assert isinstance(
            lesson["quiz"],
            list,
        )

        assert len(
            lesson["quiz"]
        ) > 0


# ==========================================================
# Lesson lookup
# ==========================================================

def test_lesson_01_lookup():
    lesson = get_management_lesson(
        "management_basics",
        0,
    )

    assert lesson is not None
    assert lesson["id"] == LESSON_01["id"]


def test_lesson_02_lookup():
    lesson = get_management_lesson(
        "management_basics",
        1,
    )

    assert lesson is not None
    assert lesson["id"] == LESSON_02["id"]


def test_lesson_03_lookup():
    lesson = get_management_lesson(
        "management_basics",
        2,
    )

    assert lesson is not None
    assert lesson["id"] == LESSON_03["id"]


def test_lesson_04_lookup():
    lesson = get_management_lesson(
        "management_basics",
        3,
    )

    assert lesson is not None
    assert lesson["id"] == LESSON_04["id"]


# ==========================================================
# Invalid lesson lookup
# ==========================================================

def test_invalid_lesson_index_returns_none():
    lesson = get_management_lesson(
        "management_basics",
        999,
    )

    assert lesson is None


def test_invalid_chapter_returns_none():
    lesson = get_management_lesson(
        "invalid_chapter",
        0,
    )

    assert lesson is None


# ==========================================================
# Menu generation
# ==========================================================

def test_management_menu_keyboard():
    keyboard = management_menu_keyboard()

    assert keyboard is not None
    assert keyboard.inline_keyboard

    assert len(
        keyboard.inline_keyboard
    ) >= len(
        MANAGEMENT_CURRICULUM
    )


def test_management_chapter_keyboard():
    keyboard = management_chapter_keyboard(
        "management_basics"
    )

    assert keyboard is not None
    assert keyboard.inline_keyboard

    # فصل اول حداقل چهار درس دارد
    assert len(
        keyboard.inline_keyboard
    ) >= 5


# ==========================================================
# Lesson order
# ==========================================================

def test_first_four_lessons_are_in_correct_order():
    lesson_ids = [
        LESSON_01["id"],
        LESSON_02["id"],
        LESSON_03["id"],
        LESSON_04["id"],
    ]

    expected = [
        get_management_lesson(
            "management_basics",
            index,
        )["id"]
        for index in range(4)
    ]

    assert expected == lesson_ids


# ==========================================================
# Quiz structure
# ==========================================================

def test_quiz_questions_have_required_fields():
    lessons = [
        LESSON_01,
        LESSON_02,
        LESSON_03,
        LESSON_04,
    ]

    required_fields = [
        "question",
        "options",
        "answer",
        "explanation",
    ]

    for lesson in lessons:
        for question in lesson["quiz"]:
            for field in required_fields:
                assert field in question

            assert question["question"]
            assert isinstance(
                question["options"],
                list,
            )

            assert len(
                question["options"]
            ) >= 2

            assert isinstance(
                question["answer"],
                int,
            )

            assert (
                0
                <= question["answer"]
                < len(question["options"])
            )

            assert question["explanation"]


# ==========================================================
# Complete Management integration
# ==========================================================

def test_management_module_integration():
    """
    Verify that the first four lessons are connected
    from curriculum to content and quiz.
    """

    for index, lesson in enumerate(
        [
            LESSON_01,
            LESSON_02,
            LESSON_03,
            LESSON_04,
        ]
    ):
        curriculum_lesson = (
            MANAGEMENT_CURRICULUM[0]["lessons"][index]
        )

        registered_lesson = (
            MANAGEMENT_LESSONS.get(
                lesson["id"]
            )
        )

        loaded_lesson = get_management_lesson(
            "management_basics",
            index,
        )

        assert curriculum_lesson
        assert registered_lesson is lesson
        assert loaded_lesson is lesson
        assert lesson["quiz"]


# ==========================================================
# Final sanity check
# ==========================================================

def test_management_module_ready_for_next_lesson():
    """
    The module is considered ready to continue
    when Lessons 01-04 are fully integrated.
    """

    lessons = [
        LESSON_01,
        LESSON_02,
        LESSON_03,
        LESSON_04,
    ]

    assert len(lessons) == 4

    for lesson in lessons:
        assert lesson["id"] in MANAGEMENT_LESSONS
        assert lesson["quiz"]
