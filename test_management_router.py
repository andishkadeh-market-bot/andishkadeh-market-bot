import inspect

from core.menu import route_menu_callback


def test_router_is_async():
    assert inspect.iscoroutinefunction(
        route_menu_callback
    )


def test_router_exists():
    assert callable(
        route_menu_callback
    )


def test_management_callback_routes():
    expected_callbacks = [
        "menu_management",
        "management_chapter:",
        "management_lesson:",
        "management_quiz:",
        "quiz_answer:",
        "quiz_cancel",
    ]

    source = inspect.getsource(
        route_menu_callback
    )

    for callback in expected_callbacks:
        assert callback in source


print(
    "MANAGEMENT ROUTER TEST PASSED"
)
