import pytest

from modules.management.handlers import (
    MANAGEMENT_LESSONS,
    MANAGEMENT_CHAPTER_05_LESSONS,
    MANAGEMENT_CHAPTER_LESSONS,
    get_chapter,
    get_chapter_lessons,
    get_management_lesson,
    get_lesson_location,
)


EXPECTED_IDS = [
    "management_05_01",
    "management_05_02",
    "management_05_03",
    "management_05_04",
    "management_05_05",
    "management_05_06",
    "management_05_07",
]


def test_chapter_5_registered():
    assert "controlling" in MANAGEMENT_CHAPTER_LESSONS


def test_chapter_5_curriculum_exists():
    chapter = get_chapter("controlling")

    assert chapter is not None
    assert chapter["id"] == "controlling"
    assert chapter["title"] == "فصل ۵: کنترل مدیریتی"


def test_chapter_5_has_seven_lessons():
    lessons = get_chapter_lessons("controlling")

    assert len(lessons) == 7


def test_chapter_5_lesson_order():
    lessons = get_chapter_lessons("controlling")

    assert [
        lesson["id"]
        for lesson in lessons
    ] == EXPECTED_IDS


@pytest.mark.parametrize(
    "lesson_id",
    EXPECTED_IDS,
)
def test_chapter_5_lesson_registered(
    lesson_id,
):
    assert lesson_id in MANAGEMENT_LESSONS


@pytest.mark.parametrize(
    "index, lesson_id",
    list(enumerate(EXPECTED_IDS)),
)
def test_chapter_5_lesson_lookup(
    index,
    lesson_id,
):
    lesson = get_management_lesson(
        "controlling",
        index,
    )

    assert lesson is not None
    assert lesson["id"] == lesson_id


@pytest.mark.parametrize(
    "lesson_id",
    EXPECTED_IDS,
)
def test_chapter_5_lesson_location(
    lesson_id,
):
    location = get_lesson_location(
        lesson_id
    )

    assert location is not None

    chapter_id, index = location

    assert chapter_id == "controlling"
    assert EXPECTED_IDS[index] == lesson_id


@pytest.mark.parametrize(
    "index",
    range(7),
)
def test_chapter_5_lesson_structure(
    index,
):
    lesson = get_management_lesson(
        "controlling",
        index,
    )

    assert lesson is not None
    assert lesson["id"]
    assert lesson["title"]
    assert lesson["lesson"]

    assert isinstance(
        lesson["objectives"],
        list,
    )

    assert isinstance(
        lesson["key_concepts"],
        list,
    )

    assert isinstance(
        lesson["specialized_points"],
        list,
    )

    assert isinstance(
        lesson["exam_points"],
        list,
    )

    assert isinstance(
        lesson["review"],
        list,
    )

    assert isinstance(
        lesson["quiz"],
        list,
    )

    assert len(
        lesson["quiz"]
    ) >= 5


def test_chapter_5_no_duplicate_lessons():
    lessons = get_chapter_lessons(
        "controlling"
    )

    ids = [
        lesson["id"]
        for lesson in lessons
    ]

    assert len(ids) == len(set(ids))
