from core.quiz import (
    QuizSession,
    build_questions,
    format_quiz_result,
)

from modules.management.lessons.lesson_02 import (
    LESSON_02,
)


def test_lesson_02_quiz_full_flow():
    questions = build_questions(
        LESSON_02["quiz"]
    )

    assert len(questions) == 5

    session = QuizSession(
        questions
    )

    assert session.current_index == 0
    assert session.current_question is not None
    assert session.total_questions == 5
    assert not session.is_finished

    while not session.is_finished:
        question = session.current_question

        assert question is not None

        selected_answer = question.answer

        result = session.answer(
            selected_answer
        )

        assert result is True

    assert session.is_finished
    assert session.current_question is None

    result = session.result()

    assert result["total"] == 5
    assert result["correct"] == 5
    assert result["wrong"] == 0

    formatted_result = format_quiz_result(
        result
    )

    assert formatted_result
    assert "5" in formatted_result


def test_lesson_02_quiz_wrong_answers():
    questions = build_questions(
        LESSON_02["quiz"]
    )

    session = QuizSession(
        questions
    )

    for _ in range(
        session.total_questions
    ):
        question = session.current_question

        assert question is not None

        wrong_answer = next(
            index
            for index in range(
                len(question.options)
            )
            if index != question.answer
        )

        result = session.answer(
            wrong_answer
        )

        assert result is False

    assert session.is_finished

    result = session.result()

    assert result["total"] == 5
    assert result["correct"] == 0
    assert result["wrong"] == 5


print(
    "MANAGEMENT LESSON 02 QUIZ FLOW TEST PASSED"
)
