from modules.management.lessons.lesson_02 import LESSON_02


def test_lesson_02_basic_structure():
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


def test_lesson_02_content():
    assert LESSON_02["id"] == "management_01_02"

    assert LESSON_02["title"]

    assert len(LESSON_02["objectives"]) >= 4
    assert len(LESSON_02["key_concepts"]) >= 4
    assert len(LESSON_02["specialized_points"]) >= 4
    assert len(LESSON_02["exam_points"]) >= 4
    assert len(LESSON_02["review"]) >= 4

    assert LESSON_02["lesson"].strip()
    assert LESSON_02["practical_example"].strip()


def test_lesson_02_quiz():
    quiz = LESSON_02["quiz"]

    assert isinstance(quiz, list)
    assert len(quiz) == 5

    for question in quiz:
        assert question["question"]
        assert len(question["options"]) == 4
        assert 0 <= question["answer"] < 4
        assert question["explanation"]


print("LESSON 02 TEST PASSED")
