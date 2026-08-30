from core.quiz import build_questions
from modules.management.lessons.lesson_03 import LESSON_03


def test_lesson_03_quiz_exists():
    assert "quiz" in LESSON_03
    assert LESSON_03["quiz"]
    assert len(LESSON_03["quiz"]) == 5


def test_lesson_03_quiz_questions():
    questions = build_questions(
        LESSON_03["quiz"]
    )

    assert len(questions) == 5

    for question in questions:
        assert question.question
        assert len(question.options) == 4
        assert isinstance(question.answer, int)
        assert 0 <= question.answer < 4
        assert question.explanation


def test_lesson_03_quiz_answers():
    questions = build_questions(
        LESSON_03["quiz"]
    )

    for question in questions:
        correct_answer = question.answer

        assert question.options[correct_answer]
        assert question.explanation


print("LESSON 03 QUIZ TEST PASSED")
