"""
Telegram handlers for the Admin Dashboard.
Andishkadeh Management & Market
--------------------------------
Features:
- Admin authentication using ADMIN_TELEGRAM_ID
- Global dashboard
- User list
- User details
- User progress
- User quiz statistics
- Recent quiz attempts
- Pagination
- Safe navigation
This module is the Telegram UI layer.
Data source:
    core.admin_dashboard
Authentication:
    Environment variable:
        ADMIN_TELEGRAM_ID
The admin ID is NEVER hard-coded in this file.
"""
from __future__ import annotations
import logging
import os
from typing import Any
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes
from core.admin_dashboard import (
    get_dashboard_summary,
    get_module_dashboard,
    get_total_users,
    get_user_dashboard,
    get_user_quiz_attempts,
    get_user_progress_details,
    get_users,
)
# ==========================================================
# Logging
# ==========================================================
logger = logging.getLogger(__name__)
# ==========================================================
# Constants
# ==========================================================
ADMIN_TELEGRAM_ID_ENV = "ADMIN_TELEGRAM_ID"
USERS_PER_PAGE = 8
# ==========================================================
# Admin authentication
# ==========================================================
def get_admin_telegram_id() -> int | None:
    """
    Read the administrator Telegram ID from environment.
    Returns:
        int | None
    """
    raw_value = os.getenv(
        ADMIN_TELEGRAM_ID_ENV
    )
    if not raw_value:
        return None
    try:
        return int(raw_value.strip())
    except (TypeError, ValueError):
        logger.error(
            "%s contains an invalid Telegram ID.",
            ADMIN_TELEGRAM_ID_ENV,
        )
        return None
def is_admin(
    telegram_id: int | None,
) -> bool:
    """
    Return True when the Telegram ID belongs to the admin.
    """
    if telegram_id is None:
        return False
    admin_id = get_admin_telegram_id()
    if admin_id is None:
        return False
    return telegram_id == admin_id
def is_admin_update(
    update: Update,
) -> bool:
    """
    Check whether the current Telegram user is admin.
    """
    user = update.effective_user
    if user is None:
        return False
    return is_admin(
        user.id
    )
# ==========================================================
# Common keyboards
# ==========================================================
def admin_main_keyboard() -> InlineKeyboardMarkup:
    """Build the admin dashboard keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(
                "📊 داشبورد کلی",
                callback_data="admin_dashboard",
            )
        ],
        [
            InlineKeyboardButton(
                "👥 کاربران",
                callback_data="admin_users:0",
            )
        ],
        [
            InlineKeyboardButton(
                "📈 آمار مدیریت",
                callback_data="admin_module:management",
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            )
        ],
    ]
    return InlineKeyboardMarkup(
        keyboard
    )
def admin_back_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for returning to admin dashboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 داشبورد ادمین",
                    callback_data="admin_dashboard",
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="menu_main",
                )
            ],
        ]
    )
# ==========================================================
# Authorization message
# ==========================================================
async def deny_admin_access(
    update: Update,
) -> None:
    """Show an access denied message."""
    query = update.callback_query
    if query is not None:
        await query.answer(
            "⛔ دسترسی غیرمجاز",
            show_alert=True,
        )
        try:
            await query.edit_message_text(
                "⛔ <b>دسترسی غیرمجاز</b>\n\n"
                "این بخش فقط برای مدیر ربات فعال است.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🏠 منوی اصلی",
                                callback_data="menu_main",
                            )
                        ]
                    ]
                ),
            )
        except Exception:
            logger.exception(
                "Failed to edit unauthorized admin message."
            )
        return
    if update.message is not None:
        await update.message.reply_text(
            "⛔ <b>دسترسی غیرمجاز</b>\n\n"
            "این بخش فقط برای مدیر ربات فعال است.",
            parse_mode="HTML",
        )
# ==========================================================
# Admin dashboard
# ==========================================================
async def show_admin_dashboard(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show the main administrative dashboard.
    """
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is not None:
        await query.answer()
    try:
        summary = get_dashboard_summary()
    except Exception:
        logger.exception(
            "Failed to load admin dashboard."
        )
        text = (
            "❌ <b>خطا در بارگذاری داشبورد</b>\n\n"
            "اطلاعات آماری در حال حاضر قابل دریافت نیست."
        )
        if query is not None:
            await query.edit_message_text(
                text,
                parse_mode="HTML",
                reply_markup=admin_back_keyboard(),
            )
        return
    text = f"""
<b>🔐 داشبورد مدیریت اندیشکده</b>
━━━━━━━━━━━━━━━━━━
👥 <b>کاربران</b>
تعداد کاربران: <b>{summary["users"]}</b>
📚 <b>فعالیت آموزشی</b>
شروع درس‌ها: <b>{summary["started_lessons"]}</b>
درس‌های تکمیل‌شده: <b>{summary["completed_lessons"]}</b>
📝 <b>آزمون‌ها</b>
تعداد آزمون‌ها: <b>{summary["quiz_attempts"]}</b>
تعداد سوالات: <b>{summary["total_questions"]}</b>
پاسخ صحیح: <b>{summary["correct_answers"]}</b>
پاسخ غلط: <b>{summary["wrong_answers"]}</b>
📊 <b>عملکرد کلی</b>
دقت پاسخ‌ها: <b>{summary["accuracy"]}%</b>
میانگین نمره: <b>{summary["average_score"]}%</b>
بهترین نمره: <b>{summary["best_score"]}%</b>
━━━━━━━━━━━━━━━━━━
یک بخش را انتخاب کنید:
"""
    if query is not None:
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=admin_main_keyboard(),
        )
# ==========================================================
# Users list
# ==========================================================
def build_users_keyboard(
    page: int,
    users_count: int,
) -> InlineKeyboardMarkup:
    """Build paginated user list keyboard."""
    keyboard: list[list[InlineKeyboardButton]] = []
    if users_count > 0:
        for index in range(users_count):
            absolute_index = (
                page * USERS_PER_PAGE
                + index
            )
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"👤 کاربر {absolute_index + 1}",
                        callback_data=(
                            f"admin_user_index:"
                            f"{absolute_index}"
                        ),
                    )
                ]
            )
    navigation: list[
        InlineKeyboardButton
    ] = []
    if page > 0:
        navigation.append(
            InlineKeyboardButton(
                "⬅️ قبلی",
                callback_data=(
                    f"admin_users:{page - 1}"
                ),
            )
        )
    if users_count == USERS_PER_PAGE:
        navigation.append(
            InlineKeyboardButton(
                "بعدی ➡️",
                callback_data=(
                    f"admin_users:{page + 1}"
                ),
            )
        )
    if navigation:
        keyboard.append(
            navigation
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 داشبورد ادمین",
                callback_data="admin_dashboard",
            )
        ]
    )
    return InlineKeyboardMarkup(
        keyboard
    )
def format_user_label(
    user: dict[str, Any],
) -> str:
    """Create a safe user display label."""
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
    full_name = (
        f"{first_name} {last_name}"
    ).strip()
    if full_name:
        return full_name
    if username:
        return f"@{username}"
    return str(
        user.get(
            "telegram_id",
            "نامشخص",
        )
    )
async def show_admin_users(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show registered users with pagination."""
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, page_raw = data.split(
            ":",
            1,
        )
        page = int(page_raw)
    except (ValueError, IndexError):
        page = 0
    page = max(
        page,
        0,
    )
    offset = (
        page * USERS_PER_PAGE
    )
    try:
        users = get_users(
            limit=USERS_PER_PAGE,
            offset=offset,
        )
        total_users = get_total_users()
    except Exception:
        logger.exception(
            "Failed to load users."
        )
        await query.edit_message_text(
            "❌ خطا در دریافت فهرست کاربران.",
            parse_mode="HTML",
            reply_markup=admin_back_keyboard(),
        )
        return
    if not users:
        if page > 0:
            await query.edit_message_text(
                "این صفحه کاربری ندارد.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⬅️ صفحه قبل",
                                callback_data=(
                                    f"admin_users:"
                                    f"{page - 1}"
                                ),
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "🔙 داشبورد ادمین",
                                callback_data=(
                                    "admin_dashboard"
                                ),
                            )
                        ],
                    ]
                ),
            )
            return
        text = """
<b>👥 کاربران</b>
━━━━━━━━━━━━━━━━━━
هنوز هیچ کاربری در SQLite ثبت نشده است.
"""
    else:
        lines = []
        for index, user in enumerate(
            users,
            start=1,
        ):
            absolute_index = (
                offset + index
            )
            label = format_user_label(
                user
            )
            telegram_id = user.get(
                "telegram_id",
                "-",
            )
            username = user.get(
                "username"
            )
            username_text = (
                f"@{username}"
                if username
                else "بدون username"
            )
            lines.append(
                (
                    f"<b>{absolute_index}.</b> "
                    f"{label}\n"
                    f"   🆔 {telegram_id} | "
                    f"{username_text}"
                )
            )
        text = f"""
<b>👥 کاربران ثبت‌شده</b>
تعداد کل: <b>{total_users}</b>
صفحه: <b>{page + 1}</b>
━━━━━━━━━━━━━━━━━━
{chr(10).join(lines)}
━━━━━━━━━━━━━━━━━━
برای مشاهده جزئیات، کاربر را انتخاب کنید:
"""
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=build_users_keyboard(
            page=page,
            users_count=len(users),
        ),
    )
# ==========================================================
# User by index
# ==========================================================
async def show_admin_user_by_index(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Open a user based on the absolute list index.
    This avoids placing Telegram IDs directly into
    callback data.
    """
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, index_raw = data.split(
            ":",
            1,
        )
        absolute_index = int(
            index_raw
        )
    except (ValueError, IndexError):
        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    if absolute_index < 0:
        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    try:
        users = get_users(
            limit=1,
            offset=absolute_index,
        )
    except Exception:
        logger.exception(
            "Failed to load user at index %s.",
            absolute_index,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت اطلاعات کاربر.",
            reply_markup=admin_back_keyboard(),
        )
        return
    if not users:
        await query.edit_message_text(
            "❌ کاربر موردنظر پیدا نشد.",
            reply_markup=admin_back_keyboard(),
        )
        return
    user = users[0]
    telegram_id = user.get(
        "telegram_id"
    )
    if telegram_id is None:
        await query.edit_message_text(
            "❌ شناسه تلگرام کاربر ثبت نشده است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    await render_admin_user(
        update=update,
        telegram_id=int(
            telegram_id
        ),
    )
# ==========================================================
# User details
# ==========================================================
def format_user_dashboard(
    dashboard: dict[str, Any],
) -> str:
    """Format complete user dashboard."""
    user = dashboard["user"]
    progress = dashboard["progress"]
    statistics = dashboard["statistics"]
    first_name = (
        user.get("first_name")
        or "-"
    )
    last_name = (
        user.get("last_name")
        or "-"
    )
    username = user.get(
        "username"
    )
    username_text = (
        f"@{username}"
        if username
        else "-"
    )
    latest_lesson = dashboard.get(
        "latest_completed_lesson"
    )
    latest_quiz = dashboard.get(
        "latest_quiz_attempt"
    )
    latest_lesson_text = "-"
    if latest_lesson:
        latest_lesson_text = (
            f"{latest_lesson.get('lesson_id', '-')}"
            f" | "
            f"{latest_lesson.get('completed_at', '-')}"
        )
    latest_quiz_text = "-"
    if latest_quiz:
        latest_quiz_text = (
            f"{latest_quiz.get('lesson_id', '-')}"
            f" | نمره "
            f"{latest_quiz.get('score', 0)}%"
        )
    return f"""
<b>👤 جزئیات کاربر</b>
━━━━━━━━━━━━━━━━━━
<b>اطلاعات کاربر</b>
🆔 Telegram ID:
<code>{user.get("telegram_id", "-")}</code>
👤 نام: {first_name}
👤 نام خانوادگی: {last_name}
📱 Username: {username_text}
━━━━━━━━━━━━━━━━━━
<b>📚 پیشرفت آموزشی</b>
شروع درس‌ها: <b>{progress["started_lessons"]}</b>
درس‌های تکمیل‌شده: <b>{progress["completed_lessons"]}</b>
━━━━━━━━━━━━━━━━━━
<b>📝 آمار آزمون</b>
تعداد آزمون: <b>{statistics["attempts"]}</b>
تعداد سوال: <b>{statistics["total_questions"]}</b>
پاسخ صحیح: <b>{statistics["correct_answers"]}</b>
پاسخ غلط: <b>{statistics["wrong_answers"]}</b>
دقت: <b>{statistics["accuracy"]}%</b>
میانگین نمره: <b>{statistics["average_score"]}%</b>
بهترین نمره: <b>{statistics["best_score"]}%</b>
کمترین نمره: <b>{statistics["lowest_score"]}%</b>
━━━━━━━━━━━━━━━━━━
آخرین درس تکمیل‌شده:
<b>{latest_lesson_text}</b>
آخرین آزمون:
<b>{latest_quiz_text}</b>
"""
async def render_admin_user(
    update: Update,
    telegram_id: int,
) -> None:
    """Render one user's complete dashboard."""
    query = update.callback_query
    if query is None:
        return
    try:
        dashboard = get_user_dashboard(
            telegram_id
        )
    except Exception:
        logger.exception(
            "Failed to load dashboard for user %s.",
            telegram_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت اطلاعات کاربر.",
            reply_markup=admin_back_keyboard(),
        )
        return
    if dashboard is None:
        await query.edit_message_text(
            "❌ کاربر موردنظر پیدا نشد.",
            reply_markup=admin_back_keyboard(),
        )
        return
    text = format_user_dashboard(
        dashboard
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📚 جزئیات Progress",
                    callback_data=(
                        f"admin_progress:"
                        f"{telegram_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📝 آزمون‌ها",
                    callback_data=(
                        f"admin_attempts:"
                        f"{telegram_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 کاربران",
                    callback_data="admin_users:0",
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 داشبورد ادمین",
                    callback_data="admin_dashboard",
                )
            ],
        ]
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
# ==========================================================
# User progress
# ==========================================================
async def show_admin_user_progress(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show detailed lesson progress for a user."""
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, telegram_id_raw = data.split(
            ":",
            1,
        )
        telegram_id = int(
            telegram_id_raw
        )
    except (ValueError, IndexError):
        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    try:
        progress = get_user_progress_details(
            telegram_id
        )
    except Exception:
        logger.exception(
            "Failed to load progress for user %s.",
            telegram_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت Progress کاربر.",
            reply_markup=admin_back_keyboard(),
        )
        return
    if not progress:
        text = f"""
<b>📚 Progress کاربر</b>
🆔 <code>{telegram_id}</code>
━━━━━━━━━━━━━━━━━━
هنوز هیچ سابقه‌ای از شروع یا تکمیل درس ثبت نشده است.
"""
    else:
        lines = []
        for item in progress[:30]:
            started = (
                "🟢"
                if item.get("started")
                else "⚪"
            )
            completed = (
                "✅"
                if item.get("completed")
                else "⬜"
            )
            lines.append(
                (
                    f"{started} {completed} "
                    f"<b>{item.get('lesson_id', '-')}</b>\n"
                    f"فصل: {item.get('chapter_id', '-')}\n"
                    f"شروع: {item.get('started_at', '-')}\n"
                    f"تکمیل: {item.get('completed_at', '-')}"
                )
            )
        text = f"""
<b>📚 Progress کاربر</b>
🆔 <code>{telegram_id}</code>
تعداد رکوردها: <b>{len(progress)}</b>
━━━━━━━━━━━━━━━━━━
{chr(10).join(lines)}
"""
        if len(progress) > 30:
            text += (
                "\n\nنمایش فقط ۳۰ رکورد اخیر انجام شده است."
            )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👤 پروفایل کاربر",
                    callback_data=(
                        f"admin_user:"
                        f"{telegram_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 داشبورد ادمین",
                    callback_data="admin_dashboard",
                )
            ],
        ]
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
# ==========================================================
# User quiz attempts
# ==========================================================
async def show_admin_user_attempts(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show recent quiz attempts for a user."""
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, telegram_id_raw = data.split(
            ":",
            1,
        )
        telegram_id = int(
            telegram_id_raw
        )
    except (ValueError, IndexError):
        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    try:
        attempts = get_user_quiz_attempts(
            telegram_id,
            limit=30,
        )
    except Exception:
        logger.exception(
            "Failed to load quiz attempts for user %s.",
            telegram_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت آزمون‌های کاربر.",
            reply_markup=admin_back_keyboard(),
        )
        return
    if not attempts:
        text = f"""
<b>📝 آزمون‌های کاربر</b>
🆔 <code>{telegram_id}</code>
━━━━━━━━━━━━━━━━━━
هنوز هیچ آزمونی برای این کاربر ثبت نشده است.
"""
    else:
        lines = []
        for attempt in attempts:
            score = float(
                attempt.get(
                    "score",
                    0,
                )
            )
            lines.append(
                (
                    f"📝 <b>{attempt.get('lesson_id', '-')}</b>\n"
                    f"فصل: {attempt.get('chapter_id', '-')}\n"
                    f"نتیجه: "
                    f"{attempt.get('correct_answers', 0)} / "
                    f"{attempt.get('total_questions', 0)}\n"
                    f"نمره: <b>{score:.2f}%</b>\n"
                    f"تاریخ: "
                    f"{attempt.get('completed_at') or attempt.get('started_at') or '-'}"
                )
            )
        text = f"""
<b>📝 آزمون‌های کاربر</b>
🆔 <code>{telegram_id}</code>
تعداد آزمون‌ها: <b>{len(attempts)}</b>
━━━━━━━━━━━━━━━━━━
{chr(10).join(lines)}
"""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👤 پروفایل کاربر",
                    callback_data=(
                        f"admin_user:"
                        f"{telegram_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 داشبورد ادمین",
                    callback_data="admin_dashboard",
                )
            ],
        ]
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
# ==========================================================
# Direct user dashboard
# ==========================================================
async def show_admin_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show one user dashboard from callback data."""
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, telegram_id_raw = data.split(
            ":",
            1,
        )
        telegram_id = int(
            telegram_id_raw
        )
    except (ValueError, IndexError):
        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    await render_admin_user(
        update,
        telegram_id,
    )
# ==========================================================
# Module dashboard
# ==========================================================
async def show_admin_module_dashboard(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show global statistics for one module."""
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, module_id = data.split(
            ":",
            1,
        )
    except ValueError:
        await query.edit_message_text(
            "❌ شناسه ماژول نامعتبر است.",
            reply_markup=admin_back_keyboard(),
        )
        return
    try:
        dashboard = get_module_dashboard(
            module_id
        )
    except Exception:
        logger.exception(
            "Failed to load module dashboard: %s",
            module_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت آمار ماژول.",
            reply_markup=admin_back_keyboard(),
        )
        return
    text = f"""
<b>📈 آمار ماژول</b>
ماژول:
<b>{module_id}</b>
━━━━━━━━━━━━━━━━━━
📚 تعداد فصل‌ها:
<b>{dashboard["chapters"]}</b>
📖 تعداد درس‌ها:
<b>{dashboard["lessons"]}</b>
📝 تعداد آزمون‌ها:
<b>{dashboard["quiz_attempts"]}</b>
❓ تعداد سوالات:
<b>{dashboard["total_questions"]}</b>
✅ پاسخ صحیح:
<b>{dashboard["correct_answers"]}</b>
❌ پاسخ غلط:
<b>{dashboard["wrong_answers"]}</b>
🎯 دقت:
<b>{dashboard["accuracy"]}%</b>
📊 میانگین نمره:
<b>{dashboard["average_score"]}%</b>
🏆 بهترین نمره:
<b>{dashboard["best_score"]}%</b>
"""
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_back_keyboard(),
    )
# ==========================================================
# Admin command
# ==========================================================
async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle /admin.
    This command is intended to be registered in bot.py.
    """
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    if update.message is None:
        return
    try:
        summary = get_dashboard_summary()
    except Exception:
        logger.exception(
            "Failed to load dashboard from /admin."
        )
        await update.message.reply_text(
            "❌ خطا در بارگذاری داشبورد ادمین.",
        )
        return
    text = f"""
<b>🔐 پنل مدیریت اندیشکده</b>
👥 کاربران: <b>{summary["users"]}</b>
📝 آزمون‌ها: <b>{summary["quiz_attempts"]}</b>
📚 درس‌های تکمیل‌شده: <b>{summary["completed_lessons"]}</b>
📊 میانگین نمره: <b>{summary["average_score"]}%</b>
از منوی زیر بخش موردنظر را انتخاب کنید:
"""
    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_main_keyboard(),
    )
# ==========================================================
# Callback router
# ==========================================================
async def route_admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route all admin callback queries.
    This handler should be placed before a generic
    catch-all CallbackQueryHandler.
    """
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    if not (
        data == "admin_dashboard"
        or data == "admin_users"
        or data.startswith("admin_users:")
        or data.startswith("admin_user:")
        or data.startswith("admin_user_index:")
        or data.startswith("admin_progress:")
        or data.startswith("admin_attempts:")
        or data.startswith("admin_module:")
    ):
        return
    if not is_admin_update(update):
        await deny_admin_access(update)
        return
    if data == "admin_dashboard":
        await show_admin_dashboard(
            update,
            context,
        )
        return
    if data.startswith("admin_users:"):
        await show_admin_users(
            update,
            context,
        )
        return
    if data == "admin_users":
        await show_admin_users(
            update,
            context,
        )
        return
    if data.startswith("admin_user_index:"):
        await show_admin_user_by_index(
            update,
            context,
        )
        return
    if data.startswith("admin_user:"):
        await show_admin_user(
            update,
            context,
        )
        return
    if data.startswith("admin_progress:"):
        await show_admin_user_progress(
            update,
            context,
        )
        return
    if data.startswith("admin_attempts:"):
        await show_admin_user_attempts(
            update,
            context,
        )
        return
    if data.startswith("admin_module:"):
        await show_admin_module_dashboard(
            update,
            context,
        )
        return
# ==========================================================
# Health check
# ==========================================================
def admin_handlers_health_check() -> bool:
    """
    Basic health check for the admin handler layer.
    Does not contact Telegram.
    """
    try:
        admin_id = get_admin_telegram_id()
        if admin_id is None:
            return False
        return admin_id > 0
    except Exception:
        return False
