"""
Tests for Management Chapter 02 - Lesson 01
Planning
"""

from modules.management.lessons.lesson_08 import LESSON_08


def test_lesson_08_exists():
    """Lesson 08 must exist."""
    assert LESSON_08 is not None


def test_lesson_08_has_correct_id():
    """Lesson 08 must have the correct ID."""
    assert LESSON_08["id"] == "management_02_01"


def test_lesson_08_has_title():
    """Lesson 08 must have a title."""
    assert LESSON_08["title"]
    assert "برنامه‌ریزی" in LESSON_08["title"]


def test_lesson_08_has_objectives():
    """Lesson 08 must contain learning objectives."""
    assert "objectives" in LESSON_08
    assert isinstance(LESSON_08["objectives"], list)
    assert len(LESSON_08["objectives"]) > 0


def test_lesson_08_has_lesson_content():
    """Lesson 08 must contain detailed lesson content."""
    assert "lesson" in LESSON_08
    assert isinstance(LESSON_08["lesson"], str)
    assert len(LESSON_08["lesson"].strip()) > 100


def test_lesson_08_has_key_concepts():
    """Lesson 08 must contain key concepts."""
    assert "key_concepts" in LESSON_08
    assert isinstance(LESSON_08["key_concepts"], list)
    assert len(LESSON_08["key_concepts"]) > 0

    for concept in LESSON_08["key_concepts"]:
        assert "title" in concept
        assert "description" in concept
        assert concept["title"]
        assert concept["description"]


def test_lesson_08_has_specialized_points():
    """Lesson 08 must contain specialized points."""
    assert "specialized_points" in LESSON_08
    assert isinstance(LESSON_08["specialized_points"], list)
    assert len(LESSON_08["specialized_points"]) > 0


def test_lesson_08_has_exam_points():
    """Lesson 08 must contain exam points."""
    assert "exam_points" in LESSON_08
    assert isinstance(LESSON_08["exam_points"], list)
    assert len(LESSON_08["exam_points"]) > 0


def test_lesson_08_has_practical_example():
    """Lesson 08 must contain a practical example."""
    assert "practical_example" in LESSON_08
    assert isinstance(LESSON_08["practical_example"], str)
    assert len(LESSON_08["practical_example"].strip()) > 50


def test_lesson_08_has_review():
    """Lesson 08 must contain review points."""
    assert "review" in LESSON_08
    assert isinstance(LESSON_08["review"], list)
    assert len(LESSON_08["review"]) > 0


def test_lesson_08_has_quiz():
    """Lesson 08 must contain quiz questions."""
    assert "quiz" in LESSON_08
    assert isinstance(LESSON_08["quiz"], list)
    assert len(LESSON_08["quiz"]) >= 5


def test_lesson_08_quiz_structure():
    """Every quiz question must have a valid structure."""

    for question in LESSON_08["quiz"]:
        assert "question" in question
        assert "options" in question
        assert "answer" in question
        assert "explanation" in question

        assert question["question"]
        assert isinstance(question["options"], list)

        assert len(question["options"]) == 4

        assert isinstance(question["answer"], int)
        assert 0 <= question["answer"] < len(
            question["options"]
        )

        assert question["explanation"]


def test_lesson_08_quiz_answers_are_valid():
    """All quiz answers must point to existing options."""

    for question in LESSON_08["quiz"]:
        answer = question["answer"]
        options = question["options"]

        assert 0 <= answer < len(options)
        assert options[answer]


def test_lesson_08_covers_planning_topic():
    """Lesson content must actually cover the planning topic."""

    content = (
        LESSON_08["title"]
        + LESSON_08["lesson"]
        + " ".join(LESSON_08["objectives"])
        + " ".join(LESSON_08["exam_points"])
        + " ".join(LESSON_08["review"])
    )

    assert "برنامه‌ریزی" in content


def test_lesson_08_has_required_sections():
    """Lesson 08 must contain all required educational sections."""

    required_sections = [
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

    for section in required_sections:
        assert section in LESSON_08
