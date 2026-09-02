"""
User educational dashboard for Andishkadeh Management & Market.
Responsibilities:
- Build user dashboard data
- Calculate overall educational progress
- Show module progress
- Show quiz statistics
- Show latest educational activity
- Format a compact, professional Telegram dashboard
"""
from html import escape
from typing import Any, Dict, List, Optional
from core.database import get_user_progress, get_quiz_attempts
from core.registry import registry
# ============================================================
# Helpers
# ============================================================
def _safe_text(value: Any, default: str = "-") -> str:
    """Return safe Telegram-readable text."""
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default
def _progress_bar(percentage: float, length: int = 10) -> str:
    """Build a compact text progress bar."""
    try:
        percentage = max(0.0, min(100.0, float(percentage)))
    except (TypeError, ValueError):
        percentage = 0.0
    filled = round((percentage / 100) * length)
    filled = max(0, min(length, filled))
    return "█" * filled + "░" * (length - filled)
def _module_icon(module_id: str) -> str:
    """Return a consistent icon for each module."""
    icons = {
        "management": "📚",
        "banking": "🏦",
        "international_trade": "🌍",
        "psychology_socialwork": "🧠",
        "finance": "💳",
        "exam": "📝",
        "general_exam": "📝",
        "random_quiz": "🎲",
        "marketing": "📈",
        "economy": "💰",
        "files": "📂",
        "social": "📱",
    }
    return icons.get(module_id, "📘")
def _clean_module_title(title: Any) -> str:
    """
    Remove a leading icon from module titles.
    Some module titles already contain an emoji. Since the dashboard
    supplies its own consistent icon, duplicated icons are removed.
    """
    text = _safe_text(title)
    known_icons = (
        "📚 ",
        "🏦 ",
        "🌍 ",
        "🧠 ",
        "💳 ",
        "📝 ",
        "🎲 ",
        "📈 ",
        "💰 ",
        "📂 ",
        "📱 ",
        "📘 ",
    )
    for icon in known_icons:
        if text.startswith(icon):
            return text[len(icon):].strip()
    return text
def _module_short_title(module_id: str, title: Any) -> str:
    """Return a compact dashboard-friendly module title."""
    clean_title = _clean_module_title(title)
    short_titles = {
        "management": "مدیریت",
        "banking": "بانکداری",
        "international_trade": "تجارت",
        "psychology_socialwork": "روانشناسی",
        "finance": "مدیریت مالی",
        "general_exam": "آزمون عمومی",
        "exam": "آزمون عمومی",
    }
    return short_titles.get(module_id, clean_title)
def _format_percentage(value: Any) -> str:
    """Format percentage safely."""
    try:
        return f"{float(value):.0f}٪"
    except (TypeError, ValueError):
        return "۰٪"
def _format_number(value: Any) -> str:
    """Format numeric values as simple integers."""
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "۰"
def _get_user_id(user: Any) -> Optional[int]:
    """Extract Telegram user ID from a user object or integer."""
    if user is None:
        return None
    if isinstance(user, int):
        return user
    for attr in ("id", "user_id"):
        value = getattr(user, attr, None)
        if value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
    if isinstance(user, dict):
        for key in ("id", "user_id"):
            if key in user:
                try:
                    return int(user[key])
                except (TypeError, ValueError):
                    return None
    return None
# ============================================================
# User
# ============================================================
def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user information from the database."""
    try:
        from core.database import get_connection
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            try:
                return dict(row)
            except (TypeError, ValueError):
                return {
                    "user_id": row[0],
                }
        finally:
            connection.close()
    except Exception:
        return None
# ============================================================
# Registered modules
# ============================================================
def get_registered_modules() -> List[Dict[str, Any]]:
    """
    Return registered modules from the central registry.
    Falls back to registry statistics if direct listing is unavailable.
    """
    try:
        modules = registry.list_modules()
        if modules:
            result = []
            for module in modules:
                if hasattr(module, "__dict__"):
                    result.append(dict(module.__dict__))
                elif isinstance(module, dict):
                    result.append(dict(module))
            return result
    except Exception:
        pass
    return []
def get_module_title(module_id: str) -> str:
    """Return module title."""
    try:
        module = registry.get_module(module_id)
        if module is not None:
            if hasattr(module, "title"):
                return _safe_text(module.title)
            if isinstance(module, dict):
                return _safe_text(module.get("title"))
    except Exception:
        pass
    fallback_titles = {
        "management": "مدیریت",
        "banking": "بانکداری",
        "international_trade": "تجارت بین‌الملل",
        "psychology_socialwork": "روانشناسی و مددکاری",
        "finance": "مدیریت مالی",
        "exam": "آزمون عمومی",
        "general_exam": "آزمون عمومی",
    }
    return fallback_titles.get(module_id, module_id)
# ============================================================
# Module dashboard
# ============================================================
def get_module_dashboard(
    user_id: int,
    module_id: str,
) -> Dict[str, Any]:
    """Return progress information for one module."""
    try:
        progress = registry.get_module_progress(user_id, module_id)
        if isinstance(progress, dict):
            total = int(progress.get("total_lessons", 0) or 0)
            started = int(progress.get("started_lessons", 0) or 0)
            completed = int(progress.get("completed_lessons", 0) or 0)
            percentage = (
                (completed / total) * 100
                if total > 0
                else 0
            )
            return {
                "module_id": module_id,
                "title": get_module_title(module_id),
                "total_lessons": total,
                "started_lessons": started,
                "completed_lessons": completed,
                "remaining_lessons": max(0, total - completed),
                "progress_percentage": percentage,
            }
    except Exception:
        pass
    # Database fallback
    try:
        progress = get_user_progress(user_id)
        if isinstance(progress, dict):
            module_data = progress.get(module_id)
            if isinstance(module_data, dict):
                total = int(
                    module_data.get("total_lessons", 0) or 0
                )
                started = int(
                    module_data.get("started_lessons", 0) or 0
                )
                completed = int(
                    module_data.get("completed_lessons", 0) or 0
                )
                percentage = (
                    (completed / total) * 100
                    if total > 0
                    else 0
                )
                return {
                    "module_id": module_id,
                    "title": get_module_title(module_id),
                    "total_lessons": total,
                    "started_lessons": started,
                    "completed_lessons": completed,
                    "remaining_lessons": max(
                        0,
                        total - completed,
                    ),
                    "progress_percentage": percentage,
                }
    except Exception:
        pass
    return {
        "module_id": module_id,
        "title": get_module_title(module_id),
        "total_lessons": 0,
        "started_lessons": 0,
        "completed_lessons": 0,
        "remaining_lessons": 0,
        "progress_percentage": 0,
    }
# ============================================================
# User dashboard data
# ============================================================
def get_user_dashboard(user_id: int) -> Dict[str, Any]:
    """Build complete dashboard data for a user."""
    user = get_user(user_id)
    modules = []
    module_ids = [
        "management",
        "banking",
        "international_trade",
        "psychology_socialwork",
        "finance",
        "general_exam",
    ]
    for module_id in module_ids:
        modules.append(
            get_module_dashboard(
                user_id,
                module_id,
            )
        )
    total_lessons = sum(
        item["total_lessons"]
        for item in modules
    )
    started_lessons = sum(
        item["started_lessons"]
        for item in modules
    )
    completed_lessons = sum(
        item["completed_lessons"]
        for item in modules
    )
    remaining_lessons = max(
        0,
        total_lessons - completed_lessons,
    )
    overall_percentage = (
        (completed_lessons / total_lessons) * 100
        if total_lessons > 0
        else 0
    )
    attempts = []
    try:
        attempts = get_quiz_attempts(user_id) or []
    except Exception:
        attempts = []
    quiz_count = len(attempts)
    total_questions = 0
    correct_answers = 0
    wrong_answers = 0
    scores = []
    for attempt in attempts:
        if not isinstance(attempt, dict):
            continue
        total_questions += int(
            attempt.get("total_questions", 0) or 0
        )
        correct_answers += int(
            attempt.get("correct_answers", 0) or 0
        )
        wrong_answers += int(
            attempt.get("wrong_answers", 0) or 0
        )
        score = attempt.get("score")
        if score is not None:
            try:
                scores.append(float(score))
            except (TypeError, ValueError):
                pass
    if total_questions == 0:
        total_questions = correct_answers + wrong_answers
    accuracy = (
        (correct_answers / total_questions) * 100
        if total_questions > 0
        else 0
    )
    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )
    best_score = max(scores) if scores else 0
    latest_activity = None
    try:
        completed = [
            item
            for item in attempts
            if isinstance(item, dict)
        ]
        if completed:
            latest_activity = completed[-1]
    except Exception:
        latest_activity = None
    return {
        "user": user,
        "modules": modules,
        "total_lessons": total_lessons,
        "started_lessons": started_lessons,
        "completed_lessons": completed_lessons,
        "remaining_lessons": remaining_lessons,
        "progress_percentage": overall_percentage,
        "quiz_count": quiz_count,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "accuracy": accuracy,
        "average_score": average_score,
        "best_score": best_score,
        "latest_activity": latest_activity,
    }
# ============================================================
# Dashboard summary
# ============================================================
def get_dashboard_summary(user_id: int) -> Dict[str, Any]:
    """Return compact dashboard summary."""
    dashboard = get_user_dashboard(user_id)
    return {
        "total_lessons": dashboard["total_lessons"],
        "started_lessons": dashboard["started_lessons"],
        "completed_lessons": dashboard["completed_lessons"],
        "remaining_lessons": dashboard["remaining_lessons"],
        "progress_percentage": dashboard["progress_percentage"],
        "quiz_count": dashboard["quiz_count"],
        "total_questions": dashboard["total_questions"],
        "correct_answers": dashboard["correct_answers"],
        "wrong_answers": dashboard["wrong_answers"],
        "accuracy": dashboard["accuracy"],
        "average_score": dashboard["average_score"],
        "best_score": dashboard["best_score"],
    }
# ============================================================
# Dashboard formatter
# ============================================================
def format_dashboard(
    user_id: int,
    username: Optional[str] = None,
) -> str:
    """
    Format a professional, compact Telegram dashboard.
    Design:
    - Overall statistics in two columns
    - Modules vertically for better mobile readability
    - Quiz statistics two-by-two
    - Extra spacing between quiz columns
    - Clear visual sections
    """
    dashboard = get_user_dashboard(user_id)
    user = dashboard.get("user") or {}
    if username is None:
        username = (
            user.get("username")
            if isinstance(user, dict)
            else None
        )
    display_name = _safe_text(
        username or user.get("first_name") if isinstance(user, dict) else username,
        "دوست عزیز",
    )
    display_name = escape(display_name)
    total_lessons = _format_number(
        dashboard["total_lessons"]
    )
    started_lessons = _format_number(
        dashboard["started_lessons"]
    )
    completed_lessons = _format_number(
        dashboard["completed_lessons"]
    )
    remaining_lessons = _format_number(
        dashboard["remaining_lessons"]
    )
    progress_percentage = _format_percentage(
        dashboard["progress_percentage"]
    )
    progress_bar = _progress_bar(
        dashboard["progress_percentage"]
    )
    lines = []
    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------
    lines.append("👤 <b>داشبورد آموزشی</b>")
    lines.append("")
    lines.append(f"سلام {display_name} 👋")
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📊 <b>وضعیت کلی</b>")
    lines.append("")
    lines.append(
        f"📚 {total_lessons} درس"
        f"　　▶️ {started_lessons} شروع‌شده"
    )
    lines.append(
        f"✅ {completed_lessons} تکمیل‌شده"
        f"　　⏳ {remaining_lessons} باقی‌مانده"
    )
    lines.append("")
    lines.append(
        f"{progress_bar}  {progress_percentage}"
    )
    # --------------------------------------------------------
    # Modules
    # --------------------------------------------------------
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📚 <b>ماژول‌های آموزشی</b>")
    lines.append("")
    for module in dashboard["modules"]:
        module_id = _safe_text(
            module.get("module_id"),
            "",
        )
        title = _module_short_title(
            module_id,
            module.get("title"),
        )
        icon = _module_icon(module_id)
        percentage = _format_percentage(
            module.get("progress_percentage", 0)
        )
        completed = _format_number(
            module.get("completed_lessons", 0)
        )
        total = _format_number(
            module.get("total_lessons", 0)
        )
        lines.append(
            f"{icon} {escape(title)}"
            f" — {percentage} ({completed}/{total})"
        )
    # --------------------------------------------------------
    # Quiz performance
    # --------------------------------------------------------
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📝 <b>عملکرد آزمون‌ها</b>")
    lines.append("")
    quiz_count = _format_number(
        dashboard["quiz_count"]
    )
    total_questions = _format_number(
        dashboard["total_questions"]
    )
    correct_answers = _format_number(
        dashboard["correct_answers"]
    )
    wrong_answers = _format_number(
        dashboard["wrong_answers"]
    )
    accuracy = _format_percentage(
        dashboard["accuracy"]
    )
    average_score = _format_percentage(
        dashboard["average_score"]
    )
    best_score = _format_percentage(
        dashboard["best_score"]
    )
    # Two-by-two layout with wider spacing
    lines.append(
        f"🎯 آزمون‌ها: {quiz_count}"
        f"　　　　 📖 سؤالات: {total_questions}"
    )
    lines.append("")
    
    lines.append(
        f"✅ صحیح: {correct_answers}"
        f"　　　　　 ❌ غلط: {wrong_answers}"
    )
    lines.append("")
    lines.append(
        f"📈 دقت: {accuracy}"
        f"　　　　　📊 میانگین: {average_score}"
    )
    lines.append("")
    lines.append(
        f"🏆 بهترین نمره: {best_score}"
    )
    # --------------------------------------------------------
    # Latest activity
    # --------------------------------------------------------
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📌 <b>آخرین فعالیت آموزشی</b>")
    lines.append("")
    latest_activity = dashboard.get(
        "latest_activity"
    )
    if isinstance(latest_activity, dict):
        lesson_title = latest_activity.get(
            "lesson_title"
        ) or latest_activity.get(
            "title"
        )
        if lesson_title:
            lines.append(
                f"📘 {escape(_safe_text(lesson_title))}"
            )
        score = latest_activity.get("score")
        if score is not None:
            lines.append(
                f"📊 نمره: {_format_percentage(score)}"
            )
    else:
        lines.append(
            "هنوز فعالیت آموزشی تکمیل‌شده‌ای ثبت نشده است."
        )
    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("اندیشکده مدیریت و بازار")
    return "\n".join(lines)
# ============================================================
# Health check
# ============================================================
def dashboard_health_check() -> bool:
    """Basic dashboard health check."""
    try:
        required_functions = (
            get_user,
            get_registered_modules,
            get_module_title,
            get_module_dashboard,
            get_user_dashboard,
            get_dashboard_summary,
            format_dashboard,
        )
        return all(
            callable(function)
            for function in required_functions
        )
    except Exception:
        return False
__all__ = [
    "get_user",
    "get_registered_modules",
    "get_module_title",
    "get_module_dashboard",
    "get_user_dashboard",
    "get_dashboard_summary",
    "format_dashboard",
    "dashboard_health_check",
]
