from core.quiz import QuizSession, build_questions
from modules.management.lessons.lesson_03 import LESSON_03


def test_lesson_03_quiz_flow():
    questions = build_questions(
        LESSON_03["quiz"]
    )

    assert questions
    assert len(questions) == 5

    session = QuizSession(questions)

    assert session.current_index == 0
    assert session.current_question is not None
    assert session.total_questions == 5
    assert session.is_finished is False

    for question in questions:
        current_question = session.current_question

        assert current_question is not None
        assert current_question.question == question.question

        selected_option = current_question.answer

        result = session.answer(
            selected_option
        )

        assert result is True

    assert session.is_finished is True

    result = session.result()

    assert result is not None
    assert result["total"] == 5
    assert result["correct"] == 5
    assert result["wrong"] == 0


def test_lesson_03_quiz_wrong_answer_flow():
    questions = build_questions(
        LESSON_03["quiz"]
    )

    session = QuizSession(questions)

    for _ in range(len(questions)):
        current_question = session.current_question

        assert current_question is not None

        wrong_option = next(
            index
            for index in range(
                len(current_question.options)
            )
            if index != current_question.answer
        )

        result = session.answer(
            wrong_option
        )

        assert result is False

    assert session.is_finished is True

    result = session.result()

    assert result["total"] == 5
    assert result["correct"] == 0
    assert result["wrong"] == 5


print("LESSON 03 QUIZ FLOW TEST PASSED")
