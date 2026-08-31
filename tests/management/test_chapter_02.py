“””
Integration tests for Management Chapter 2.

Chapter 2:
برنامه‌ریزی
“””

from modules.management.lessons.lesson_13 import LESSON_13
from modules.management.lessons.lesson_14 import LESSON_14
from modules.management.lessons.lesson_15 import LESSON_15
from modules.management.lessons.lesson_16 import LESSON_16
from modules.management.lessons.lesson_17 import LESSON_17
from modules.management.lessons.lesson_18 import LESSON_18
from modules.management.lessons.lesson_19 import LESSON_19

CHAPTER_02_LESSONS = [
LESSON_13,
LESSON_14,
LESSON_15,
LESSON_16,
LESSON_17,
LESSON_18,
LESSON_19,
]

def test_chapter_02_has_seven_lessons():
“”“Chapter 2 must contain seven lessons.”””
assert len(CHAPTER_02_LESSONS) == 7

def test_chapter_02_lesson_ids_are_correct():
“”“All Chapter 2 lesson IDs must be correct.”””
expected_ids = [
“management_02_01”,
“management_02_02”,
“management_02_03”,
“management_02_04”,
“management_02_05”,
“management_02_06”,
“management_02_07”,
]

actual_ids = [
    lesson["id"]
    for lesson in CHAPTER_02_LESSONS
]
assert actual_ids == expected_ids

def test_chapter_02_lessons_have_required_sections():
“”“Every lesson must contain all required sections.”””

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
for lesson in CHAPTER_02_LESSONS:
    for section in required_sections:
        assert section in lesson
        assert lesson[section]

def test_chapter_02_lessons_have_quizzes():
“”“Every lesson must have quiz questions.”””

for lesson in CHAPTER_02_LESSONS:
    assert isinstance(
        lesson["quiz"],
        list,
    )
    assert len(
        lesson["quiz"]
    ) >= 5

def test_chapter_02_quiz_structure_is_valid():
“”“Every quiz question must have valid structure.”””

for lesson in CHAPTER_02_LESSONS:
    for question in lesson["quiz"]:
        assert "question" in question
        assert "options" in question
        assert "answer" in question
        assert "explanation" in question
        assert question["question"]
        assert isinstance(
            question["options"],
            list,
        )
        assert len(
            question["options"]
        ) == 4
        assert isinstance(
            question["answer"],
            int,
        )
        assert (
            0
            <= question["answer"]
            < len(question["options"])
        )
        assert question["explanation"]

def test_chapter_02_lesson_titles_are_not_empty():
“”“All lesson titles must exist.”””

for lesson in CHAPTER_02_LESSONS:
    assert isinstance(
        lesson["title"],
        str,
    )
    assert lesson["title"].strip()

def test_chapter_02_is_management_chapter():
“”“All lessons must belong to Management Chapter 2.”””

for lesson in CHAPTER_02_LESSONS:
    assert lesson["id"].startswith(
        "management_02_"
    )

def test_chapter_02_has_meaningful_content():
“”“Lessons must contain sufficiently detailed content.”””

for lesson in CHAPTER_02_LESSONS:
    assert len(
        lesson["lesson"].strip()
    ) > 300
    assert len(
        lesson["objectives"]
    ) >= 5
    assert len(
        lesson["key_concepts"]
    ) >= 4
    assert len(
        lesson["specialized_points"]
    ) >= 5
    assert len(
        lesson["exam_points"]
    ) >= 5
    assert len(
        lesson["review"]
    ) >= 5

def test_chapter_02_quiz_answers_are_valid():
“”“All quiz answer indexes must be valid.”””

for lesson in CHAPTER_02_LESSONS:
    for question in lesson["quiz"]:
        answer = question["answer"]
        options = question["options"]
        assert 0 <= answer < len(options)
        assert options[answer]
