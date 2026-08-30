from modules.management.handlers import (
    get_management_lesson,
)

from modules.management.lessons.lesson_01 import (
    LESSON_01,
)

from modules.management.lessons.lesson_02 import (
    LESSON_02,
)


def test_lesson_01_handler_mapping():
    lesson = get_management_lesson(
        "management_basics",
        0,
    )

    assert lesson is LESSON_01
    assert lesson["id"] == "management_01_01"


def test_lesson_02_handler_mapping():
    lesson = get_management_lesson(
        "management_basics",
        1,
    )

    assert lesson is LESSON_02
    assert lesson["id"] == "management_01_02"


def test_invalid_lesson_mapping():
    assert (
        get_management_lesson(
            "management_basics",
            99,
        )
        is None
    )


def test_invalid_chapter_mapping():
    assert (
        get_management_lesson(
            "invalid_chapter",
            0,
        )
        is None
    )


print(
    "LESSON HANDLER TEST PASSED"
)
