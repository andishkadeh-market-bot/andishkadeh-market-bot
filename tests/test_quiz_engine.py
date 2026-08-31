"""
Complete tests for core.quiz_engine.
"""

from core.quiz_engine import (
    QuizEngine,
    QuizQuestion,
    STATUS_ACTIVE,
    STATUS_CANCELLED,
    STATUS_COMPLETED,
)


def build_questions():
    return [
        QuizQuestion(
            id="q1",
            question="2 + 2 = ?",
            options=("3", "4", "5", "6"),
            correct_answer="4",
        ),
        QuizQuestion(
            id="q2",
            question="3 + 3 = ?",
            options=("5", "6", "7", "8"),
            correct_answer="6",
        ),
        QuizQuestion(
            id="q3",
            question="5 + 5 = ?",
            options=("8", "9", "10", "11"),
            correct_answer="10",
        ),
    ]


def test_question_creation():

    question = QuizQuestion(
        id="q1",
        question="Test?",
        options=("A", "B"),
        correct_answer="A",
    )

    assert question.id == "q1"
    assert question.correct_answer == "A"


def test_start_quiz():

    engine = QuizEngine()

    session = engine.start_quiz(
        telegram_id=1001,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    assert session.status == STATUS_ACTIVE
    assert session.total_questions() == 3
    assert session.current_index == 0


def test_current_question():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=1002,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    question = engine.get_current_question(
        1002
    )

    assert question is not None
    assert question.id == "q1"


def test_correct_answer():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=1003,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    result = engine.submit_answer(
        telegram_id=1003,
        answer="4",
    )

    assert result["is_correct"] is True
    assert result["correct_answers"] == 1
    assert result["wrong_answers"] == 0
    assert result["current_index"] == 1


def test_wrong_answer():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=1004,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    result = engine.submit_answer(
        telegram_id=1004,
        answer="3",
    )

    assert result["is_correct"] is False
    assert result["correct_answers"] == 0
    assert result["wrong_answers"] == 1


def test_complete_quiz():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=1005,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    engine.submit_answer(
        telegram_id=1005,
        answer="4",
    )

    engine.submit_answer(
        telegram_id=1005,
        answer="6",
    )

    result = engine.submit_answer(
        telegram_id=1005,
        answer="10",
    )

    assert result["finished"] is True

    final_result = engine.get_result(
        1005
    )

    assert final_result is not None
    assert (
        final_result.status
        == STATUS_COMPLETED
    )
    assert final_result.correct_answers == 3
    assert final_result.wrong_answers == 0
    assert final_result.score == 100.0


def test_partial_score():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=1006,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    engine.submit_answer(
        telegram_id=1006,
        answer="4",
    )

    engine.submit_answer(
        telegram_id=1006,
        answer="5",
    )

    engine.submit_answer(
        telegram_id=1006,
        answer="9",
    )

    result = engine.get_result(
        1006
    )

    assert result is not None
    assert result.correct_answers == 1
    assert result.wrong_answers == 2
    assert result.score == 33.33


def test_cancellation():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=1007,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    result = engine.cancel_quiz(
        1007
    )

    assert (
        result.status
        == STATUS_CANCELLED
    )


def test_multi_user_isolation():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=2001,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    engine.start_quiz(
        telegram_id=2002,
        module_id="exam",
        chapter_id="general",
        lesson_id="exam_1",
        questions=build_questions(),
    )

    engine.submit_answer(
        telegram_id=2001,
        answer="4",
    )

    engine.submit_answer(
        telegram_id=2002,
        answer="3",
    )

    state_1 = engine.get_state(2001)
    state_2 = engine.get_state(2002)

    assert state_1 is not None
    assert state_2 is not None

    assert state_1["correct_answers"] == 1
    assert state_1["wrong_answers"] == 0

    assert state_2["correct_answers"] == 0
    assert state_2["wrong_answers"] == 1

    assert (
        state_1["module_id"]
        == "management"
    )

    assert (
        state_2["module_id"]
        == "exam"
    )


def test_duplicate_active_quiz_is_rejected():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=3001,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    try:

        engine.start_quiz(
            telegram_id=3001,
            module_id="exam",
            chapter_id="chapter_1",
            lesson_id="lesson_1",
            questions=build_questions(),
        )

        assert False

    except RuntimeError:
        assert True


def test_replace_existing_quiz():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=3002,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    engine.start_quiz(
        telegram_id=3002,
        module_id="exam",
        chapter_id="general",
        lesson_id="exam_1",
        questions=build_questions(),
        replace_existing=True,
    )

    state = engine.get_state(
        3002
    )

    assert state is not None
    assert (
        state["module_id"]
        == "exam"
    )


def test_statistics_payload():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=4001,
        module_id="exam",
        chapter_id="general",
        lesson_id="exam_1",
        questions=build_questions(),
    )

    engine.submit_answer(
        telegram_id=4001,
        answer="4",
    )

    engine.submit_answer(
        telegram_id=4001,
        answer="6",
    )

    engine.submit_answer(
        telegram_id=4001,
        answer="10",
    )

    payload = (
        engine.build_statistics_payload(
            4001
        )
    )

    assert payload is not None
    assert (
        payload["telegram_id"]
        == 4001
    )
    assert (
        payload["module_id"]
        == "exam"
    )
    assert (
        payload["correct_answers"]
        == 3
    )
    assert payload["score"] == 100.0


def test_progress_payload():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=4002,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    engine.submit_answer(
        telegram_id=4002,
        answer="4",
    )

    engine.submit_answer(
        telegram_id=4002,
        answer="6",
    )

    engine.submit_answer(
        telegram_id=4002,
        answer="10",
    )

    payload = (
        engine.build_progress_payload(
            4002
        )
    )

    assert payload is not None
    assert (
        payload["telegram_id"]
        == 4002
    )
    assert (
        payload["module_id"]
        == "management"
    )
    assert (
        payload["chapter_id"]
        == "chapter_1"
    )
    assert (
        payload["lesson_id"]
        == "lesson_1"
    )
    assert payload["completed"] is True


def test_state():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=5001,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    state = engine.get_state(
        5001
    )

    assert state is not None
    assert state["status"] == STATUS_ACTIVE
    assert state["current_index"] == 0
    assert state["total_questions"] == 3
    assert (
        state["current_question"]["id"]
        == "q1"
    )


def test_remove_session():

    engine = QuizEngine()

    engine.start_quiz(
        telegram_id=5002,
        module_id="management",
        chapter_id="chapter_1",
        lesson_id="lesson_1",
        questions=build_questions(),
    )

    assert (
        engine.remove_session(
            5002
        )
        is True
    )

    assert (
        engine.get_session(
            5002
        )
        is None
    )


def test_health_check():

    engine = QuizEngine()

    assert (
        engine.health_check()
        is True
    )


def test_global_health_check():

    from core.quiz_engine import (
        quiz_engine_health_check,
    )

    assert (
        quiz_engine_health_check()
        is True
    )


if __name__ == "__main__":

    tests = [
        test_question_creation,
        test_start_quiz,
        test_current_question,
        test_correct_answer,
        test_wrong_answer,
        test_complete_quiz,
        test_partial_score,
        test_cancellation,
        test_multi_user_isolation,
        test_duplicate_active_quiz_is_rejected,
        test_replace_existing_quiz,
        test_statistics_payload,
        test_progress_payload,
        test_state,
        test_remove_session,
        test_health_check,
        test_global_health_check,
    ]

    for test in tests:
        test()
        print(
            f"🟢 {test.__name__}"
        )

    print()
    print(
        "================================"
    )
    print(
        "🟢 ALL QUIZ ENGINE TESTS PASSED"
    )
    print(
        "================================"
    )
