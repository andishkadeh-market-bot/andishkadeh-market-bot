"""
Tests for Management Chapter 4 lessons.

Lessons:
27-36
"""

import importlib


LESSON_MODULES = [
    "modules.management.lessons.lesson_27",
    "modules.management.lessons.lesson_28",
    "modules.management.lessons.lesson_29",
    "modules.management.lessons.lesson_30",
    "modules.management.lessons.lesson_31",
    "modules.management.lessons.lesson_32",
    "modules.management.lessons.lesson_33",
    "modules.management.lessons.lesson_34",
    "modules.management.lessons.lesson_35",
    "modules.management.lessons.lesson_36",
]


LESSON_VARIABLES = [
    "LESSON_27",
    "LESSON_28",
    "LESSON_29",
    "LESSON_30",
    "LESSON_31",
    "LESSON_32",
    "LESSON_33",
    "LESSON_34",
    "LESSON_35",
    "LESSON_36",
]


REQUIRED_FIELDS = [
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


EXPECTED_IDS = [
    "management_04_01",
    "management_04_02",
    "management_04_03",
    "management_04_04",
    "management_04_05",
    "management_04_06",
    "management_04_07",
    "management_04_08",
    "management_04_09",
    "management_04_10",
]


def load_lessons():
    """Import Lessons 27-36."""

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


def test_all_chapter_4_lessons_import():
    """All Chapter 4 lessons must import."""

    lessons = load_lessons()

    assert len(lessons) == 10


def test_chapter_4_lesson_ids():
    """Lesson IDs must follow the expected sequence."""

    lessons = load_lessons()

    actual_ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert actual_ids == EXPECTED_IDS


def test_lesson_ids_are_unique():
    """All lesson IDs must be unique."""

    lessons = load_lessons()

    ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert len(ids) == len(set(ids))


def test_required_fields_exist():
    """Every lesson must contain all required fields."""

    lessons = load_lessons()

    for lesson in lessons:
        for field in REQUIRED_FIELDS:
            assert field in lesson, (
                f"Missing '{field}' in "
                f"{lesson['id']}"
            )


def test_basic_text_fields_are_not_empty():
    """Basic text fields must not be empty."""

    lessons = load_lessons()

    fields = [
        "id",
        "title",
        "lesson",
        "practical_example",
    ]

    for lesson in lessons:
        for field in fields:
            assert isinstance(
                lesson[field],
                str,
            )

            assert lesson[field].strip()


def test_learning_sections_are_lists():
    """Educational sections must be lists."""

    lessons = load_lessons()

    fields = [
        "objectives",
        "key_concepts",
        "specialized_points",
        "exam_points",
        "review",
        "quiz",
    ]

    for lesson in lessons:
        for field in fields:
            assert isinstance(
                lesson[field],
                list,
            )

            assert len(
                lesson[field]
            ) > 0


def test_key_concepts_structure():
    """Key concepts must have title and description."""

    lessons = load_lessons()

    for lesson in lessons:
        for concept in lesson[
            "key_concepts"
        ]:
            assert isinstance(
                concept,
                dict,
            )

            assert "title" in concept
            assert "description" in concept

            assert concept[
                "title"
            ].strip()

            assert concept[
                "description"
            ].strip()


def test_quiz_structure():
    """Every quiz must contain valid questions."""

    lessons = load_lessons()

    for lesson in lessons:

        assert len(
            lesson["quiz"]
        ) >= 5

        for question in lesson["quiz"]:

            assert isinstance(
                question,
                dict,
            )

            assert "question" in question
            assert "options" in question
            assert "answer" in question
            assert "explanation" in question

            assert question[
                "question"
            ].strip()

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

            assert question[
                "explanation"
            ].strip()


def test_quiz_options_are_not_empty():
    """Quiz options must contain text."""

    lessons = load_lessons()

    for lesson in lessons:
        for question in lesson[
            "quiz"
        ]:
            for option in question[
                "options"
            ]:
                assert isinstance(
                    option,
                    str,
                )

                assert option.strip()


def test_quiz_answers_are_valid():
    """Every quiz answer must point to an existing option."""

    lessons = load_lessons()

    for lesson in lessons:
        for question in lesson[
            "quiz"
        ]:
            answer = question[
                "answer"
            ]

            options = question[
                "options"
            ]

            assert 0 <= answer < len(
                options
            )


def test_chapter_4_content_completeness():
    """Every lesson must contain sufficient educational content."""

    lessons = load_lessons()

    for lesson in lessons:

        assert len(
            lesson["objectives"]
        ) >= 3

        assert len(
            lesson["key_concepts"]
        ) >= 3

        assert len(
            lesson["specialized_points"]
        ) >= 3

        assert len(
            lesson["exam_points"]
        ) >= 3

        assert len(
            lesson["review"]
        ) >= 3

        assert len(
            lesson["quiz"]
        ) >= 5
