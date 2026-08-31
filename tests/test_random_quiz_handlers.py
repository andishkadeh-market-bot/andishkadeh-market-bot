from __future__ import annotations

import asyncio

from modules.random_quiz.handlers import (
    get_random_question_pool,
    select_random_questions,
    random_quiz_handlers_health_check,
)


def test_health_check():
    assert random_quiz_handlers_health_check() is True


def test_question_pool():
    pool = get_random_question_pool()

    assert isinstance(pool, list)

    for question in pool:
        assert isinstance(question, dict)
        assert question.get("question")
        assert isinstance(
            question.get("options"),
            list,
        )
        assert len(question["options"]) >= 2


def test_random_question_selection():
    pool = get_random_question_pool()

    if not pool:
        return

    selected = select_random_questions(5)

    assert isinstance(selected, list)
    assert len(selected) <= 5
    assert len(selected) <= len(pool)

    selected_ids = {
        id(question)
        for question in selected
    }

    assert len(selected_ids) == len(selected)


def test_question_selection_limit():
    pool = get_random_question_pool()

    if not pool:
        return

    selected = select_random_questions(100)

    assert len(selected) <= 20
    assert len(selected) <= len(pool)


def test_question_selection_minimum():
    pool = get_random_question_pool()

    if not pool:
        return

    selected = select_random_questions(0)

    assert len(selected) >= 1


def test_handler_imports():
    from modules.random_quiz import handlers

    assert hasattr(
        handlers,
        "start_random_quiz",
    )

    assert hasattr(
        handlers,
        "answer_random_quiz",
    )

    assert hasattr(
        handlers,
        "finish_random_quiz",
    )

    assert hasattr(
        handlers,
        "cancel_random_quiz",
    )

    assert hasattr(
        handlers,
        "route_random_quiz_callback",
    )

    assert hasattr(
        handlers,
        "show_random_quiz_menu",
    )


def test_async_handlers_are_callable():
    from modules.random_quiz.handlers import (
        start_random_quiz,
        answer_random_quiz,
        finish_random_quiz,
        cancel_random_quiz,
        route_random_quiz_callback,
        show_random_quiz_menu,
    )

    assert asyncio.iscoroutinefunction(
        start_random_quiz
    )

    assert asyncio.iscoroutinefunction(
        answer_random_quiz
    )

    assert asyncio.iscoroutinefunction(
        finish_random_quiz
    )

    assert asyncio.iscoroutinefunction(
        cancel_random_quiz
    )

    assert asyncio.iscoroutinefunction(
        route_random_quiz_callback
    )

    assert asyncio.iscoroutinefunction(
        show_random_quiz_menu
    )


if __name__ == "__main__":
    tests = [
        test_health_check,
        test_question_pool,
        test_random_question_selection,
        test_question_selection_limit,
        test_question_selection_minimum,
        test_handler_imports,
        test_async_handlers_are_callable,
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
        "🟢 ALL RANDOM QUIZ HANDLER TESTS PASSED"
    )
    print(
        "================================"
    )
