from modules.management.lessons.lesson_04 import LESSON_04


def test_lesson_04_exists():
    assert LESSON_04 is not None
    assert LESSON_04["id"] == "management_01_04"
    assert LESSON_04["title"]


def test_lesson_04_has_required_sections():
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
        assert field in LESSON_04
        assert LESSON_04[field]


def test_lesson_04_content_is_not_empty():
    assert len(LESSON_04["objectives"]) >= 5
    assert len(LESSON_04["key_concepts"]) >= 3
    assert len(LESSON_04["specialized_points"]) >= 5
    assert len(LESSON_04["exam_points"]) >= 5
    assert len(LESSON_04["review"]) >= 4


def test_lesson_04_quiz():
    quiz = LESSON_04["quiz"]

    assert len(quiz) == 5

    for question in quiz:
        assert question["question"]
        assert len(question["options"]) == 4
        assert isinstance(question["answer"], int)
        assert 0 <= question["answer"] < 4
        assert question["options"][question["answer"]]
        assert question["explanation"]


print("LESSON 04 TEST PASSED")
