from core.quiz import (
    build_questions,
)

from modules.management.lessons.lesson_02 import (
    LESSON_02,
)


def test_lesson_02_quiz_exists():
    quiz = LESSON_02["quiz"]

    assert isinstance(quiz, list)
    assert len(quiz) == 5


def test_lesson_02_quiz_builds():
    questions = build_questions(
        LESSON_02["quiz"]
    )

    assert len(questions) == 5


def test_lesson_02_quiz_questions():
    questions = build_questions(
        LESSON_02["quiz"]
    )

    for question in questions:
        assert question.question
        assert len(question.options) == 4
        assert 0 <= question.answer < 4
        assert question.explanation


def test_lesson_02_quiz_answers():
    questions = build_questions(
        LESSON_02["quiz"]
    )

    for question in questions:
        assert isinstance(
            question.answer,
            int,
        )

        assert (
            question.options[
                question.answer
            ]
        )


print(
    "MANAGEMENT LESSON 02 QUIZ TEST PASSED"
)
