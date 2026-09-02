"""
User dashboard service for Andishkadeh Management & Market.

This module combines:
- Registry
- Progress
- Statistics
- SQLite

Responsibilities:
- Build user dashboard
- Show module progress
- Show quiz statistics
- Show latest completed lesson
- Show latest quiz attempt
- Show best quiz attempt
- Show chapter progress
- Format dashboard data
- Provide health check

The dashboard does not write progress or statistics.
Those events are handled by the Progress and Statistics layers.
"""

from __future__ import annotations

from html import escape
from typing import Any

from core.database import (
    get_connection,
    init_database,
)

from core.progress import (
    get_last_completed_lesson,
    get_module_progress,
)

from core.statistics import (
    get_best_attempt,
    get_latest_attempt,
    get_user_statistics,
)

from core.registry import registry


# ==========================================================
# Constants
# ==========================================================

MANAGEMENT_MODULE_ID = "management"


# ==========================================================
# Initialization
# ==========================================================

def initialize_dashboard_system() -> None:
    """Initialize the SQLite database required by dashboard."""

    init_database()


# ==========================================================
# User
# ==========================================================

def get_user(
    telegram_id: int,
) -> dict[str, Any] | None:
    """Return a registered user."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name,
                last_name,
                created_at,
                updated_at
            FROM users
            WHERE telegram_id = ?
            LIMIT 1
            """,
            (
                telegram_id,
            ),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


# ==========================================================
# Module metadata
# ==========================================================

def get_registered_modules() -> list[dict[str, Any]]:
    """Return modules registered in the Registry."""

    modules = []

    for module in registry.list_modules():

        modules.append(
            {
                "module_id": module.module_id,
                "title": module.title,
                "chapters": len(
                    module.chapters
                ),
                "lessons": sum(
                    len(chapter.lessons)
                    for chapter in module.chapters.values()
                ),
            }
        )

    return modules


def get_module_title(
    module_id: str,
) -> str:
    """Return a friendly module title."""

    module = registry.get_module(
        module_id
    )

    if module is not None:
        return module.title

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT title
            FROM modules
            WHERE module_id = ?
            LIMIT 1
            """,
            (
                module_id,
            ),
        ).fetchone()

    if row is not None:
        return str(
            row["title"]
        )

    return module_id


# ==========================================================
# Module dashboard
# ==========================================================

def get_module_dashboard(
    telegram_id: int,
    module_id: str,
) -> dict[str, Any]:
    """Return complete dashboard information for one module."""

    progress = get_module_progress(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    statistics = get_user_statistics(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    latest_attempt = get_latest_attempt(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    best_attempt = get_best_attempt(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    return {
        "module_id": module_id,
        "module_title": get_module_title(
            module_id
        ),
        "progress": progress,
        "statistics": statistics,
        "latest_attempt": latest_attempt,
        "best_attempt": best_attempt,
    }


# ==========================================================
# Complete user dashboard
# ==========================================================

def get_user_dashboard(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any]:
    """
    Build the complete dashboard.

    If module_id is provided, dashboard is limited
    to that module.

    Otherwise all registered SQLite modules are included.
    """

    initialize_dashboard_system()

    user = get_user(
        telegram_id
    )

    if module_id is not None:

        module_ids = [
            module_id
        ]

    else:

        with get_connection() as connection:

            rows = connection.execute(
                """
                SELECT module_id
                FROM modules
                ORDER BY id
                """
            ).fetchall()

        module_ids = [
            str(row["module_id"])
            for row in rows
        ]

        for module in registry.list_modules():

            if module.module_id not in module_ids:

                module_ids.append(
                    module.module_id
                )

    modules = [
        get_module_dashboard(
            telegram_id=telegram_id,
            module_id=current_module_id,
        )
        for current_module_id in module_ids
    ]

    if module_id is not None:

        progress = get_module_progress(
            telegram_id=telegram_id,
            module_id=module_id,
        )

        statistics = get_user_statistics(
            telegram_id=telegram_id,
            module_id=module_id,
        )

        last_completed = (
            get_last_completed_lesson(
                telegram_id=telegram_id,
                module_id=module_id,
            )
        )

        latest_attempt = get_latest_attempt(
            telegram_id=telegram_id,
            module_id=module_id,
        )

        best_attempt = get_best_attempt(
            telegram_id=telegram_id,
            module_id=module_id,
        )

    else:

        total_lessons = sum(
            int(
                item["progress"]["total_lessons"]
            )
            for item in modules
        )

        started_lessons = sum(
            int(
                item["progress"]["started_lessons"]
            )
            for item in modules
        )

        completed_lessons = sum(
            int(
                item["progress"]["completed_lessons"]
            )
            for item in modules
        )

        remaining_lessons = max(
            total_lessons
            - completed_lessons,
            0,
        )

        percentage = (
            round(
                completed_lessons
                / total_lessons
                * 100,
                2,
            )
            if total_lessons > 0
            else 0.0
        )

        progress = {
            "module_id": None,
            "total_lessons": total_lessons,
            "started_lessons": started_lessons,
            "completed_lessons": completed_lessons,
            "remaining_lessons": remaining_lessons,
            "percentage": percentage,
            "completed": (
                total_lessons > 0
                and completed_lessons >= total_lessons
            ),
            "chapters": [],
        }

        statistics = get_user_statistics(
            telegram_id=telegram_id
        )

        last_completed = (
            get_last_completed_lesson(
                telegram_id=telegram_id
            )
        )

        latest_attempt = get_latest_attempt(
            telegram_id=telegram_id
        )

        best_attempt = get_best_attempt(
            telegram_id=telegram_id
        )

    return {
        "telegram_id": telegram_id,
        "user": user,
        "module_id": module_id,
        "module_title": (
            get_module_title(module_id)
            if module_id is not None
            else "همه ماژول‌ها"
        ),
        "progress": progress,
        "statistics": statistics,
        "latest_attempt": latest_attempt,
        "best_attempt": best_attempt,
        "last_completed_lesson": last_completed,
        "modules": modules,
    }


# ==========================================================
# Compact summary
# ==========================================================

def get_dashboard_summary(
    telegram_id: int,
    module_id: str | None = None,
) -> dict[str, Any]:
    """Return the most important dashboard metrics."""

    dashboard = get_user_dashboard(
        telegram_id=telegram_id,
        module_id=module_id,
    )

    progress = dashboard["progress"]
    statistics = dashboard["statistics"]

    return {
        "telegram_id": telegram_id,
        "module_id": module_id,
        "progress_percentage": float(
            progress["percentage"]
        ),
        "total_lessons": int(
            progress["total_lessons"]
        ),
        "started_lessons": int(
            progress["started_lessons"]
        ),
        "completed_lessons": int(
            progress["completed_lessons"]
        ),
        "remaining_lessons": int(
            progress["remaining_lessons"]
        ),
        "quiz_attempts": int(
            statistics["attempts"]
        ),
        "average_score": float(
            statistics["average_score"]
        ),
        "best_score": float(
            statistics["best_score"]
        ),
        "accuracy": float(
            statistics["accuracy"]
        ),
    }


# ==========================================================
# Formatting helpers
# ==========================================================

def _format_percentage(
    value: float | int | None,
) -> str:
    """Format percentage for Telegram."""

    if value is None:
        return "0٪"

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "0٪"

    if numeric.is_integer():
        return f"{int(numeric)}٪"

    return f"{numeric:.2f}٪"


def _format_user_name(
    user: dict[str, Any] | None,
) -> str:
    """Return the best available user display name."""

    if not user:
        return "کاربر"

    first_name = (
        user.get("first_name")
        or ""
    ).strip()

    last_name = (
        user.get("last_name")
        or ""
    ).strip()

    username = (
        user.get("username")
        or ""
    ).strip()

    full_name = " ".join(
        part
        for part in (
            first_name,
            last_name,
        )
        if part
    )

    if full_name:
        return full_name

    if username:
        return (
            "@"
            + username.lstrip("@")
        )

    return "کاربر"


def _progress_bar(
    percentage: float | int | None,
    width: int = 10,
) -> str:
    """Create a compact text progress bar."""

    try:
        numeric = max(
            0.0,
            min(
                100.0,
                float(percentage or 0),
            ),
        )
    except (TypeError, ValueError):
        numeric = 0.0

    filled = round(
        numeric / 100 * width
    )

    empty = width - filled

    return (
        "█" * filled
        + "░" * empty
    )


def _safe_text(
    value: Any,
    default: str = "-",
) -> str:
    """Escape dynamic text for Telegram HTML."""

    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return escape(
        text,
        quote=False,
    )


def _module_short_title(
    title: str,
) -> str:
    """
    Return a compact module title suitable for
    two-column Telegram dashboard rows.
    """

    replacements = {
        "آموزش مدیریت": "مدیریت",
        "بانکداری تخصصی": "بانکداری",
        "تجارت بین‌الملل": "تجارت",
        "روانشناسی و مددکاری": "روانشناسی",
        "مدیریت مالی": "مدیریت مالی",
        "آزمون عمومی": "آزمون عمومی",
    }

    return replacements.get(
        title,
        title,
    )


def _module_icon(
    module_id: str,
) -> str:
    """Return a consistent icon for each module."""

    icons = {
        "management": "📚",
        "banking": "🏦",
        "international_trade": "🌍",
        "psychology_socialwork": "🧠",
        "finance": "💳",
        "exam": "📝",
        "general_exam": "📝",
    }

    return icons.get(
        module_id,
        "📘",
    )


# ==========================================================
# Dashboard formatter
# ==========================================================

def format_dashboard(
    dashboard: dict[str, Any],
) -> str:
    """
    Convert dashboard data into a modern,
    compact and Telegram-compatible HTML layout.
    """

    user_name = _safe_text(
        _format_user_name(
            dashboard.get("user")
        ),
        "کاربر",
    )

    progress = dashboard.get(
        "progress",
        {},
    )

    statistics = dashboard.get(
        "statistics",
        {},
    )

    last_completed = dashboard.get(
        "last_completed_lesson"
    )

    modules = dashboard.get(
        "modules",
        [],
    )

    total_lessons = int(
        progress.get(
            "total_lessons",
            0,
        )
        or 0
    )

    started_lessons = int(
        progress.get(
            "started_lessons",
            0,
        )
        or 0
    )

    completed_lessons = int(
        progress.get(
            "completed_lessons",
            0,
        )
        or 0
    )

    remaining_lessons = int(
        progress.get(
            "remaining_lessons",
            0,
        )
        or 0
    )

    percentage = float(
        progress.get(
            "percentage",
            0,
        )
        or 0
    )

    attempts = int(
        statistics.get(
            "attempts",
            0,
        )
        or 0
    )

    total_questions = int(
        statistics.get(
            "total_questions",
            0,
        )
        or 0
    )

    correct_answers = int(
        statistics.get(
            "correct_answers",
            0,
        )
        or 0
    )

    wrong_answers = int(
        statistics.get(
            "wrong_answers",
            0,
        )
        or 0
    )

    accuracy = statistics.get(
        "accuracy",
        0,
    )

    average_score = statistics.get(
        "average_score",
        0,
    )

    best_score = statistics.get(
        "best_score",
        0,
    )

    lines = [
        "<b>👤 داشبورد آموزشی</b>",
        f"سلام <b>{user_name}</b> 👋",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "<b>📊 وضعیت کلی</b>",
        "",
        (
            f"📚 <b>{total_lessons}</b> درس"
            f"    ▶️ <b>{started_lessons}</b> شروع‌شده"
        ),
        (
            f"✅ <b>{completed_lessons}</b> تکمیل‌شده"
            f"    ⏳ <b>{remaining_lessons}</b> باقی‌مانده"
        ),
        "",
        (
            f"{_progress_bar(percentage)}  "
            f"<b>{_format_percentage(percentage)}</b>"
        ),
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "<b>📚 ماژول‌های آموزشی</b>",
        "",
    ]

    # ------------------------------------------------------
    # Modules: two columns
    # ------------------------------------------------------

    module_rows: list[str] = []

    for item in modules:

        item_progress = item.get(
            "progress",
            {},
        )

        module_id = str(
            item.get(
                "module_id",
                "",
            )
        )

        raw_title = str(
            item.get(
                "module_title",
                module_id or "-",
            )
        )

        title = _safe_text(
            _module_short_title(
                raw_title
            )
        )

        module_percentage = item_progress.get(
            "percentage",
            0,
        )

        completed = int(
            item_progress.get(
                "completed_lessons",
                0,
            )
            or 0
        )

        total = int(
            item_progress.get(
                "total_lessons",
                0,
            )
            or 0
        )

        icon = _module_icon(
            module_id
        )

        module_rows.append(
            (
                f"{icon} <b>{title}</b> "
                f"{_format_percentage(module_percentage)} "
                f"({completed}/{total})"
            )
        )

    for index in range(
        0,
        len(module_rows),
        2,
    ):

        first = module_rows[index]

        second = (
            module_rows[index + 1]
            if index + 1 < len(module_rows)
            else ""
        )

        if second:

            lines.append(
                f"{first}    {second}"
            )

        else:

            lines.append(
                first
            )

    # ------------------------------------------------------
    # Quiz statistics
    # ------------------------------------------------------

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━━━━━━━",
            "<b>📝 عملکرد آزمون‌ها</b>",
            "",
            (
                f"🎯 آزمون‌ها: <b>{attempts}</b>"
                f"    📖 سوالات: <b>{total_questions}</b>"
            ),
            (
                f"✅ صحیح: <b>{correct_answers}</b>"
                f"    ❌ غلط: <b>{wrong_answers}</b>"
            ),
            (
                f"📈 دقت: <b>{_format_percentage(accuracy)}</b>"
                f"    📊 میانگین: <b>{_format_percentage(average_score)}</b>"
            ),
            (
                f"🏆 بهترین نمره: "
                f"<b>{_format_percentage(best_score)}</b>"
            ),
        ]
    )

    # ------------------------------------------------------
    # Latest completed lesson
    # ------------------------------------------------------

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━━━━━━━",
            "<b>📌 آخرین فعالیت آموزشی</b>",
            "",
        ]
    )

    if last_completed:

        module_id = last_completed.get(
            "module_id"
        )

        chapter_id = last_completed.get(
            "chapter_id"
        )

        lesson_id = last_completed.get(
            "lesson_id"
        )

        module_title = (
            get_module_title(
                str(module_id)
            )
            if module_id
            else "-"
        )

        lines.extend(
            [
                (
                    f"📚 ماژول: "
                    f"<b>{_safe_text(module_title)}</b>"
                ),
                (
                    f"📑 فصل: "
                    f"<b>{_safe_text(chapter_id)}</b>"
                ),
                (
                    f"📘 درس: "
                    f"<b>{_safe_text(lesson_id)}</b>"
                ),
            ]
        )

    else:

        lines.append(
            "هنوز فعالیت آموزشی تکمیل‌شده‌ای ثبت نشده است."
        )

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━━━━━━━",
            "<i>اندیشکده مدیریت و بازار</i>",
        ]
    )

    return "\n".join(
        lines
    )


# ==========================================================
# Health check
# ==========================================================

def dashboard_health_check() -> bool:
    """Check whether dashboard dependencies are accessible."""

    try:

        initialize_dashboard_system()

        with get_connection() as connection:

            connection.execute(
                "SELECT 1"
            ).fetchone()

            connection.execute(
                "SELECT COUNT(*) FROM users"
            ).fetchone()

            connection.execute(
                "SELECT COUNT(*) FROM lesson_progress"
            ).fetchone()

            connection.execute(
                "SELECT COUNT(*) FROM quiz_attempts"
            ).fetchone()

            connection.execute(
                "SELECT COUNT(*) FROM modules"
            ).fetchone()

        return True

    except Exception:
        return False


# ==========================================================
# Manual smoke test
# ==========================================================

if __name__ == "__main__":

    initialize_dashboard_system()

    print(
        "Dashboard system initialized successfully."
    )
