"""
Integration tests for Management Chapter 3 lessons.

Lessons covered:
20, 21, 22, 23, 24, 25, 26
"""

import importlib


LESSON_MODULES = [
    "modules.management.lessons.lesson_20",
    "modules.management.lessons.lesson_21",
    "modules.management.lessons.lesson_22",
    "modules.management.lessons.lesson_23",
    "modules.management.lessons.lesson_24",
    "modules.management.lessons.lesson_25",
    "modules.management.lessons.lesson_26",
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


def load_lessons():
    """Import all Chapter 3 lesson modules."""

    lessons = []

    for module_name in LESSON_MODULES:
        module = importlib.import_module(module_name)

        lesson_number = module_name.split("_")[-1]

        lesson_variable = f"LESSON_{lesson_number}"

        assert hasattr(
            module,
            lesson_variable,
        ), (
            f"{module_name} must contain "
            f"{lesson_variable}"
        )

        lesson = getattr(
            module,
            lesson_variable,
        )

        assert isinstance(
            lesson,
            dict,
        ), (
            f"{lesson_variable} must be a dictionary"
        )

        lessons.append(lesson)

    return lessons


def test_all_chapter_3_lessons_import():
    """All Chapter 3 lesson modules must import successfully."""

    lessons = load_lessons()

    assert len(lessons) == 7


def test_lesson_ids_are_unique():
    """Every lesson must have a unique ID."""

    lessons = load_lessons()

    lesson_ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert len(lesson_ids) == len(
        set(lesson_ids)
    )


def test_required_fields_exist():
    """Every lesson must contain all required fields."""

    lessons = load_lessons()

    for lesson in lessons:
        for field in REQUIRED_FIELDS:
            assert field in lesson, (
                f"Missing field '{field}' "
                f"in {lesson.get('id')}"
            )


def test_basic_lesson_fields_are_not_empty():
    """Important text fields must not be empty."""

    lessons = load_lessons()

    text_fields = [
        "id",
        "title",
        "lesson",
        "practical_example",
    ]

    for lesson in lessons:
        for field in text_fields:
            value = lesson[field]

            assert isinstance(
                value,
                str,
            ), (
                f"{lesson['id']} field "
                f"'{field}' must be a string"
            )

            assert value.strip(), (
                f"{lesson['id']} field "
                f"'{field}' must not be empty"
            )


def test_learning_sections_are_lists():
    """Learning sections must be lists."""

    lessons = load_lessons()

    list_fields = [
        "objectives",
        "key_concepts",
        "specialized_points",
        "exam_points",
        "review",
        "quiz",
    ]

    for lesson in lessons:
        for field in list_fields:
            assert isinstance(
                lesson[field],
                list,
            ), (
                f"{lesson['id']} field "
                f"'{field}' must be a list"
            )

            assert len(
                lesson[field]
            ) > 0, (
                f"{lesson['id']} field "
                f"'{field}' must not be empty"
            )


def test_key_concepts_structure():
    """Every key concept must have title and description."""

    lessons = load_lessons()

    for lesson in lessons:
        for concept in lesson["key_concepts"]:
            assert isinstance(
                concept,
                dict,
            ), (
                f"{lesson['id']} key concept "
                f"must be a dictionary"
            )

            assert "title" in concept
            assert "description" in concept

            assert concept["title"].strip()
            assert concept["description"].strip()


def test_quiz_structure():
    """Every quiz question must have valid structure."""

    lessons = load_lessons()

    for lesson in lessons:
        quiz = lesson["quiz"]

        assert len(quiz) >= 5, (
            f"{lesson['id']} must have "
            f"at least 5 quiz questions"
        )

        for question in quiz:

            assert isinstance(
                question,
                dict,
            )

            assert "question" in question
            assert "options" in question
            assert "answer" in question
            assert "explanation" in question

            assert isinstance(
                question["question"],
                str,
            )

            assert question["question"].strip()

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
            ), (
                f"Invalid answer index in "
                f"{lesson['id']}"
            )

            assert isinstance(
                question["explanation"],
                str,
            )

            assert question[
                "explanation"
            ].strip()


def test_quiz_questions_are_not_empty():
    """Quiz questions and options must contain text."""

    lessons = load_lessons()

    for lesson in lessons:
        for question in lesson["quiz"]:

            assert (
                question["question"].strip()
            )

            for option in question[
                "options"
            ]:
                assert isinstance(
                    option,
                    str,
                )

                assert option.strip()


def test_chapter_3_lesson_ids():
    """Chapter 3 lesson IDs must follow the expected sequence."""

    lessons = load_lessons()

    expected_ids = [
        "management_03_01",
        "management_03_02",
        "management_03_03",
        "management_03_04",
        "management_03_05",
        "management_03_06",
        "management_03_07",
    ]

    actual_ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert actual_ids == expected_ids


def test_chapter_3_lesson_titles_exist():
    """All Chapter 3 lessons must have meaningful titles."""

    lessons = load_lessons()

    for lesson in lessons:
        assert len(
            lesson["title"].strip()
        ) >= 5


def test_chapter_3_content_completeness():
    """Every lesson must contain enough educational content."""

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
