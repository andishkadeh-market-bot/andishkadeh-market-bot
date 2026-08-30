from modules.management.lessons.lesson_03 import (
    LESSON_03,
)


def test_lesson_03_structure():
    assert LESSON_03["id"] == "management_01_03"
    assert LESSON_03["title"]
    assert LESSON_03["objectives"]
    assert LESSON_03["lesson"]
    assert LESSON_03["key_concepts"]
    assert LESSON_03["specialized_points"]
    assert LESSON_03["exam_points"]
    assert LESSON_03["practical_example"]
    assert LESSON_03["review"]
    assert LESSON_03["quiz"]


def test_lesson_03_objectives():
    assert len(LESSON_03["objectives"]) >= 4

    for objective in LESSON_03["objectives"]:
        assert isinstance(objective, str)
        assert objective.strip()


def test_lesson_03_key_concepts():
    assert len(LESSON_03["key_concepts"]) >= 4

    for concept in LESSON_03["key_concepts"]:
        assert concept["title"]
        assert concept["description"]


def test_lesson_03_specialized_points():
    assert len(LESSON_03["specialized_points"]) >= 5

    for point in LESSON_03["specialized_points"]:
        assert isinstance(point, str)
        assert point.strip()


def test_lesson_03_exam_points():
    assert len(LESSON_03["exam_points"]) >= 5

    for point in LESSON_03["exam_points"]:
        assert isinstance(point, str)
        assert point.strip()


def test_lesson_03_review():
    assert len(LESSON_03["review"]) >= 4

    for item in LESSON_03["review"]:
        assert isinstance(item, str)
        assert item.strip()


def test_lesson_03_quiz():
    assert len(LESSON_03["quiz"]) == 5

    for question in LESSON_03["quiz"]:
        assert question["question"]
        assert len(question["options"]) == 4
        assert isinstance(question["answer"], int)
        assert 0 <= question["answer"] < 4
        assert question["explanation"]


print("LESSON 03 TEST PASSED")
