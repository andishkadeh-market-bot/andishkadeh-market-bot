from modules.management.lessons.lesson_08 import LESSON_08


def test_lesson_08_exists():
    assert LESSON_08 is not None


def test_lesson_08_has_required_fields():
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
        assert field in LESSON_08


def test_lesson_08_id():
    assert LESSON_08["id"] == "management_02_01"


def test_lesson_08_has_content():
    assert LESSON_08["objectives"]
    assert LESSON_08["lesson"]
    assert LESSON_08["key_concepts"]
    assert LESSON_08["specialized_points"]
    assert LESSON_08["exam_points"]
    assert LESSON_08["practical_example"]
    assert LESSON_08["review"]


def test_lesson_08_quiz_exists():
    assert LESSON_08["quiz"]
    assert len(LESSON_08["quiz"]) >= 5


def test_lesson_08_quiz_structure():
    for question in LESSON_08["quiz"]:
        assert "question" in question
        assert "options" in question
        assert "answer" in question
        assert "explanation" in question

        assert question["question"]
        assert len(question["options"]) >= 2

        assert isinstance(
            question["answer"],
            int,
        )

        assert 0 <= question["answer"] < len(
            question["options"]
        )

        assert question["explanation"]


def test_lesson_08_quiz_answers_are_valid():
    for question in LESSON_08["quiz"]:
        answer = question["answer"]
        options = question["options"]

        assert 0 <= answer < len(options)
