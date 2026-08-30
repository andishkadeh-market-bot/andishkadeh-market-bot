from modules.management.handlers import (
    MANAGEMENT_LESSONS,
    get_management_lesson,
)


def test_lesson_03_is_registered():
    assert "management_01_03" in MANAGEMENT_LESSONS

    lesson = MANAGEMENT_LESSONS["management_01_03"]

    assert lesson["id"] == "management_01_03"
    assert lesson["title"]
    assert lesson["lesson"]
    assert lesson["quiz"]


def test_lesson_03_can_be_found_by_handler():
    lesson = get_management_lesson(
        "management_basics",
        2,
    )

    assert lesson is not None
    assert lesson["id"] == "management_01_03"


def test_lesson_03_has_complete_content():
    lesson = get_management_lesson(
        "management_basics",
        2,
    )

    assert lesson is not None

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
        assert field in lesson
        assert lesson[field]


print("LESSON 03 HANDLER TEST PASSED")
