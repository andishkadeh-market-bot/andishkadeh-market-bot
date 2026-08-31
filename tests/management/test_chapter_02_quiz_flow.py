"""
Quiz flow tests for Management Chapter 2.
"""

from core.quiz import (
    QuizSession,
    build_questions,
    format_quiz_result,
)

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


def test_chapter_02_quizzes_build():
    for lesson in CHAPTER_02_LESSONS:
        questions = build_questions(
            lesson["quiz"]
        )

        assert questions
        assert len(questions) >= 5


def test_chapter_02_quiz_can_start():
    for lesson in CHAPTER_02_LESSONS:
        questions = build_questions(
            lesson["quiz"]
        )

        session = QuizSession(
            questions
        )

        assert session.current_question is not None
        assert session.current_index == 0


def test_chapter_02_quiz_accepts_answers():
    for lesson in CHAPTER_02_LESSONS:
        questions = build_questions(
            lesson["quiz"]
        )

        session = QuizSession(
            questions
        )

        question = session.current_question

        assert question is not None

        selected_answer = question.answer

        result = session.answer(
            selected_answer
        )

        assert result is True


def test_chapter_02_quiz_rejects_wrong_answers():
    for lesson in CHAPTER_02_LESSONS:
        questions = build_questions(
            lesson["quiz"]
        )

        session = QuizSession(
            questions
        )

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


def test_chapter_02_quiz_flow_to_completion():
    for lesson in CHAPTER_02_LESSONS:
        questions = build_questions(
            lesson["quiz"]
        )

        session = QuizSession(
            questions
        )

        while not session.is_finished:
            question = session.current_question

            assert question is not None

            session.answer(
                question.answer
            )

        result = session.result()

        assert result is not None

        result_text = format_quiz_result(
            result
        )

        assert result_text
        assert isinstance(
            result_text,
            str,
        )
