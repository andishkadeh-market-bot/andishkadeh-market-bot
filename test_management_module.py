from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)

from modules.management.lessons.lesson_01 import (
    LESSON_01,
)

from modules.management.lessons.lesson_02 import (
    LESSON_02,
)


def test_management_curriculum_exists():
    assert isinstance(
        MANAGEMENT_CURRICULUM,
        list,
    )

    assert len(
        MANAGEMENT_CURRICULUM
    ) >= 1


def test_management_chapter_structure():
    chapter = MANAGEMENT_CURRICULUM[0]

    assert chapter["id"] == "management_basics"

    assert chapter["title"] == (
        "فصل ۱: مبانی و مفاهیم مدیریت"
    )

    assert "lessons" in chapter

    assert isinstance(
        chapter["lessons"],
        list,
    )

    assert len(
        chapter["lessons"]
    ) >= 2


def test_first_two_lessons_exist():
    chapter = MANAGEMENT_CURRICULUM[0]

    assert chapter["lessons"][0] == (
        LESSON_01["title"].replace(
            "📖 ",
            "",
        )
    )

    assert chapter["lessons"][1] == (
        LESSON_02["title"].replace(
            "📖 ",
            "",
        )
    )


def test_lesson_01_structure():
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

    for field in required_fields:
        assert field in LESSON_01


def test_lesson_02_structure():
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

    for field in required_fields:
        assert field in LESSON_02


def test_lesson_01_and_02_have_quiz():
    assert len(
        LESSON_01["quiz"]
    ) >= 1

    assert len(
        LESSON_02["quiz"]
    ) >= 1

    for lesson in (
        LESSON_01,
        LESSON_02,
    ):
        for question in lesson["quiz"]:
            assert "question" in question
            assert "options" in question
            assert "answer" in question
            assert "explanation" in question

            assert len(
                question["options"]
            ) == 4

            assert (
                0
                <= question["answer"]
                < 4
            )


print(
    "MANAGEMENT MODULE TEST PASSED"
)
