"""
Tests for Management Lesson 11.

Chapter 2:
Planning
"""

from modules.management.lessons.lesson_11 import (
    LESSON_11,
)


def test_lesson_11_exists():
    assert LESSON_11 is not None


def test_lesson_11_has_correct_id():
    assert LESSON_11["id"] == "management_02_01"


def test_lesson_11_has_title():
    assert LESSON_11["title"]
    assert "برنامه‌ریزی" in LESSON_11["title"]


def test_lesson_11_has_objectives():
    assert isinstance(
        LESSON_11["objectives"],
        list,
    )
    assert len(LESSON_11["objectives"]) > 0


def test_lesson_11_has_lesson_content():
    assert isinstance(
        LESSON_11["lesson"],
        str,
    )
    assert len(
        LESSON_11["lesson"].strip()
    ) > 100


def test_lesson_11_has_key_concepts():
    assert isinstance(
        LESSON_11["key_concepts"],
        list,
    )
    assert len(
        LESSON_11["key_concepts"]
    ) > 0

    for concept in LESSON_11["key_concepts"]:
        assert "title" in concept
        assert "description" in concept
        assert concept["title"]
        assert concept["description"]


def test_lesson_11_has_specialized_points():
    assert isinstance(
        LESSON_11["specialized_points"],
        list,
    )
    assert len(
        LESSON_11["specialized_points"]
    ) > 0


def test_lesson_11_has_exam_points():
    assert isinstance(
        LESSON_11["exam_points"],
        list,
    )
    assert len(
        LESSON_11["exam_points"]
    ) > 0


def test_lesson_11_has_practical_example():
    assert isinstance(
        LESSON_11["practical_example"],
        str,
    )
    assert len(
        LESSON_11["practical_example"].strip()
    ) > 50


def test_lesson_11_has_review():
    assert isinstance(
        LESSON_11["review"],
        list,
    )
    assert len(
        LESSON_11["review"]
    ) > 0


def test_lesson_11_has_quiz():
    assert isinstance(
        LESSON_11["quiz"],
        list,
    )
    assert len(
        LESSON_11["quiz"]
    ) >= 10


def test_lesson_11_quiz_structure():
    for question in LESSON_11["quiz"]:
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
        )

        assert isinstance(
            question["explanation"],
            str,
        )

        assert question[
            "explanation"
        ].strip()


def test_lesson_11_has_all_required_fields():
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
        assert field in LESSON_11
