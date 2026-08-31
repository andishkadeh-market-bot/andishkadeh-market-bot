"""
Tests for Management Lesson 10.

موضوع:
مدیریت در سازمان‌های امروزی
"""

from modules.management.lessons.lesson_10 import LESSON_10


def test_lesson_10_exists():
    """Lesson 10 should exist."""
    assert LESSON_10 is not None


def test_lesson_10_has_correct_id():
    """Lesson 10 should have the expected ID."""
    assert LESSON_10["id"] == "management_01_10"


def test_lesson_10_has_title():
    """Lesson 10 should have a title."""
    assert LESSON_10["title"]
    assert "مدیریت در سازمان‌های امروزی" in LESSON_10["title"]


def test_lesson_10_has_objectives():
    """Lesson 10 should contain learning objectives."""
    assert "objectives" in LESSON_10
    assert isinstance(LESSON_10["objectives"], list)
    assert len(LESSON_10["objectives"]) > 0


def test_lesson_10_has_lesson_content():
    """Lesson 10 should contain the main lesson."""
    assert "lesson" in LESSON_10
    assert isinstance(LESSON_10["lesson"], str)
    assert len(LESSON_10["lesson"].strip()) > 100


def test_lesson_10_has_key_concepts():
    """Lesson 10 should contain key concepts."""
    assert "key_concepts" in LESSON_10
    assert isinstance(LESSON_10["key_concepts"], list)
    assert len(LESSON_10["key_concepts"]) > 0

    for concept in LESSON_10["key_concepts"]:
        assert "title" in concept
        assert "description" in concept
        assert concept["title"]
        assert concept["description"]


def test_lesson_10_has_specialized_points():
    """Lesson 10 should contain specialized points."""
    assert "specialized_points" in LESSON_10
    assert isinstance(LESSON_10["specialized_points"], list)
    assert len(LESSON_10["specialized_points"]) > 0


def test_lesson_10_has_exam_points():
    """Lesson 10 should contain exam points."""
    assert "exam_points" in LESSON_10
    assert isinstance(LESSON_10["exam_points"], list)
    assert len(LESSON_10["exam_points"]) > 0


def test_lesson_10_has_practical_example():
    """Lesson 10 should contain a practical example."""
    assert "practical_example" in LESSON_10
    assert isinstance(LESSON_10["practical_example"], str)
    assert len(LESSON_10["practical_example"].strip()) > 50


def test_lesson_10_has_review():
    """Lesson 10 should contain review points."""
    assert "review" in LESSON_10
    assert isinstance(LESSON_10["review"], list)
    assert len(LESSON_10["review"]) > 0


def test_lesson_10_has_quiz():
    """Lesson 10 should contain quiz questions."""
    assert "quiz" in LESSON_10
    assert isinstance(LESSON_10["quiz"], list)
    assert len(LESSON_10["quiz"]) > 0


def test_lesson_10_quiz_structure():
    """Every Lesson 10 quiz question should have a valid structure."""

    for question in LESSON_10["quiz"]:
        assert "question" in question
        assert "options" in question
        assert "answer" in question
        assert "explanation" in question

        assert isinstance(question["question"], str)
        assert question["question"].strip()

        assert isinstance(question["options"], list)
        assert len(question["options"]) >= 2

        assert isinstance(question["answer"], int)

        assert 0 <= question["answer"] < len(
            question["options"]
        )

        assert isinstance(question["explanation"], str)
        assert question["explanation"].strip()


def test_lesson_10_quiz_has_enough_questions():
    """Lesson 10 should have a meaningful quiz."""
    assert len(LESSON_10["quiz"]) >= 10


def test_lesson_10_quiz_answers_are_valid():
    """All quiz answers should point to existing options."""

    for question in LESSON_10["quiz"]:
        answer = question["answer"]
        options = question["options"]

        assert 0 <= answer < len(options)


def test_lesson_10_is_complete():
    """Lesson 10 should contain all required content sections."""

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
        assert field in LESSON_10


def test_lesson_10_quiz_questions_are_not_empty():
    """Quiz questions and options should not be empty."""

    for question in LESSON_10["quiz"]:
        assert question["question"].strip()

        for option in question["options"]:
            assert isinstance(option, str)
            assert option.strip()
