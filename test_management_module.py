from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)

from modules.management.lessons.lesson_01 import (
    LESSON_01,
)

from modules.management.handlers import (
    management_menu_keyboard,
    management_chapter_keyboard,
    format_lesson_text,
)


def test_management_curriculum_exists():
    assert isinstance(
        MANAGEMENT_CURRICULUM,
        list,
    )

    assert len(
        MANAGEMENT_CURRICULUM
    ) >= 1


def test_management_chapter_structure():
    chapter = MANAGEMENT_CURRICULUM[0]

    assert "id" in chapter
    assert "title" in chapter
    assert "lessons" in chapter

    assert isinstance(
        chapter["lessons"],
        list,
    )

    assert len(
        chapter["lessons"]
    ) >= 1


def test_first_lesson_matches_curriculum():
    chapter = MANAGEMENT_CURRICULUM[0]

    assert chapter["id"] == (
        "management_chapter_01"
    )

    assert chapter["lessons"][0] == (
        LESSON_01["title"]
    )


def test_lesson_structure():
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
        assert field in LESSON_01


def test_lesson_content_is_not_empty():
    assert LESSON_01["lesson"].strip()
    assert LESSON_01["practical_example"].strip()

    assert len(
        LESSON_01["objectives"]
    ) > 0

    assert len(
        LESSON_01["key_concepts"]
    ) > 0

    assert len(
        LESSON_01["specialized_points"]
    ) > 0

    assert len(
        LESSON_01["exam_points"]
    ) > 0

    assert len(
        LESSON_01["review"]
    ) > 0


def test_lesson_quiz_exists():
    quiz = LESSON_01["quiz"]

    assert isinstance(
        quiz,
        list,
    )

    assert len(quiz) >= 1

    for question in quiz:
        assert len(
            question["options"]
        ) == 4

        assert (
            0
            <= question["answer"]
            < 4
        )


def test_management_menu_keyboard():
    keyboard = management_menu_keyboard()

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) >= 2


def test_management_chapter_keyboard():
    keyboard = management_chapter_keyboard(
        "management_chapter_01"
    )

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) >= 2


def test_management_chapter_invalid():
    keyboard = management_chapter_keyboard(
        "invalid_chapter"
    )

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) == 1


def test_lesson_formatting():
    text = format_lesson_text(
        LESSON_01
    )

    assert text
    assert "اهداف یادگیری" in text
    assert "درسنامه" in text
    assert "مفاهیم کلیدی" in text
    assert "نکات تخصصی" in text
    assert "نکات آزمونی" in text
    assert "مثال کاربردی" in text
    assert "مرور و جمع‌بندی" in text


print(
    "MANAGEMENT MODULE TEST PASSED"
)
