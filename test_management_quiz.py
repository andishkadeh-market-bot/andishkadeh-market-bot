from core.quiz import QuizSession, build_questions
from modules.management.lessons.lesson_01 import LESSON_01


def test_management_lesson_quiz_structure():
    raw_questions = LESSON_01["quiz"]

    assert len(raw_questions) == 3

    for question in raw_questions:
        assert "question" in question
        assert "options" in question
        assert "answer" in question
        assert "explanation" in question

        assert len(question["options"]) == 4
        assert 0 <= question["answer"] < 4


def test_management_lesson_quiz_engine():
    questions = build_questions(
        LESSON_01["quiz"]
    )

    quiz = QuizSession(questions)

    assert quiz.total_questions == 3

    assert quiz.answer(2) is True
    assert quiz.answer(0) is True
    assert quiz.answer(1) is True

    result = quiz.result()

    assert result.total == 3
    assert result.correct == 3
    assert result.wrong == 0
    assert result.percentage == 100.0


print("MANAGEMENT QUIZ INTEGRATION TEST PASSED")
