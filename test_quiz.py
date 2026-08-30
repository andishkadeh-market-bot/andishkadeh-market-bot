from core.quiz import (
    QuizQuestion,
    QuizSession,
    build_questions,
    format_quiz_result,
)


def test_question_creation():
    question = QuizQuestion(
        question="مدیریت چیست؟",
        options=[
            "گزینه اول",
            "گزینه دوم",
            "گزینه سوم",
            "گزینه چهارم",
        ],
        answer=2,
        explanation="مدیریت فرایند دستیابی به اهداف از طریق منابع است.",
    )

    assert question.question == "مدیریت چیست؟"
    assert len(question.options) == 4
    assert question.answer == 2


def test_quiz_session_correct_answer():
    questions = [
        QuizQuestion(
            question="۲ + ۲ چند است؟",
            options=[
                "۳",
                "۴",
                "۵",
                "۶",
            ],
            answer=1,
        )
    ]

    quiz = QuizSession(questions)

    assert quiz.total_questions == 1
    assert quiz.current_index == 0
    assert quiz.correct_answers == 0

    result = quiz.answer(1)

    assert result is True
    assert quiz.correct_answers == 1
    assert quiz.wrong_answers == 0
    assert quiz.is_finished is True


def test_quiz_session_wrong_answer():
    questions = [
        QuizQuestion(
            question="۲ + ۲ چند است؟",
            options=[
                "۳",
                "۴",
                "۵",
                "۶",
            ],
            answer=1,
        )
    ]

    quiz = QuizSession(questions)

    result = quiz.answer(0)

    assert result is False
    assert quiz.correct_answers == 0
    assert quiz.wrong_answers == 1
    assert quiz.is_finished is True


def test_quiz_multiple_questions():
    questions = [
        QuizQuestion(
            question="سوال اول",
            options=["الف", "ب", "ج", "د"],
            answer=0,
        ),
        QuizQuestion(
            question="سوال دوم",
            options=["الف", "ب", "ج", "د"],
            answer=2,
        ),
        QuizQuestion(
            question="سوال سوم",
            options=["الف", "ب", "ج", "د"],
            answer=3,
        ),
    ]

    quiz = QuizSession(questions)

    assert quiz.answer(0) is True
    assert quiz.answer(1) is False
    assert quiz.answer(3) is True

    assert quiz.correct_answers == 2
    assert quiz.wrong_answers == 1
    assert quiz.is_finished is True


def test_quiz_percentage():
    questions = [
        QuizQuestion(
            question="سوال اول",
            options=["الف", "ب"],
            answer=0,
        ),
        QuizQuestion(
            question="سوال دوم",
            options=["الف", "ب"],
            answer=1,
        ),
    ]

    quiz = QuizSession(questions)

    quiz.answer(0)
    quiz.answer(0)

    result = quiz.result()

    assert result.total == 2
    assert result.correct == 1
    assert result.wrong == 1
    assert result.percentage == 50.0


def test_build_questions():
    raw_questions = [
        {
            "question": "مدیریت چیست؟",
            "options": [
                "گزینه اول",
                "گزینه دوم",
                "گزینه سوم",
                "گزینه چهارم",
            ],
            "answer": 1,
            "explanation": "پاسخ صحیح گزینه دوم است.",
        }
    ]

    questions = build_questions(
        raw_questions
    )

    assert len(questions) == 1
    assert isinstance(
        questions[0],
        QuizQuestion,
    )
    assert questions[0].answer == 1


def test_result_format():
    questions = [
        QuizQuestion(
            question="سوال اول",
            options=["الف", "ب"],
            answer=0,
        ),
        QuizQuestion(
            question="سوال دوم",
            options=["الف", "ب"],
            answer=1,
        ),
    ]

    quiz = QuizSession(questions)

    quiz.answer(0)
    quiz.answer(1)

    result = quiz.result()

    text = format_quiz_result(result)

    assert "نتیجه آزمون" in text
    assert "پاسخ صحیح" in text
    assert "100.0٪" in text


def test_invalid_option():
    questions = [
        QuizQuestion(
            question="سوال",
            options=["الف", "ب"],
            answer=0,
        )
    ]

    quiz = QuizSession(questions)

    try:
        quiz.answer(5)
        assert False
    except ValueError:
        assert True


def test_answer_after_quiz_finished():
    questions = [
        QuizQuestion(
            question="سوال",
            options=["الف", "ب"],
            answer=0,
        )
    ]

    quiz = QuizSession(questions)

    quiz.answer(0)

    try:
        quiz.answer(0)
        assert False
    except ValueError:
        assert True


print("QUIZ TEST PASSED")
