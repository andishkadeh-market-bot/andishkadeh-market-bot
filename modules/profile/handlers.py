"""
Profile handlers for Andishkadeh Management & Market.

This module is responsible for:
- Showing the user's personal learning dashboard
- Reading dashboard data from core.dashboard
- Formatting the dashboard for Telegram
- Providing a safe callback handler for menu_profile

This module does NOT modify bot.py or core.dashboard.py.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.dashboard import (
    dashboard_health_check,
    format_dashboard,
    get_user_dashboard,
)


PROFILE_CALLBACK = "menu_profile"
PROFILE_BACK_CALLBACK = "menu_main"


def _profile_keyboard() -> InlineKeyboardMarkup:
    """
    Build the keyboard shown below the user's profile/dashboard.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data=PROFILE_BACK_CALLBACK,
                )
            ]
        ]
    )


async def show_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Display the current user's learning dashboard.
    """
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    user = update.effective_user

    if user is None:
        await query.edit_message_text(
            "❌ اطلاعات کاربر در دسترس نیست."
        )
        return

    telegram_id = user.id

    try:
        dashboard = get_user_dashboard(telegram_id)

        if not dashboard:
            await query.edit_message_text(
                "👤 <b>پروفایل من</b>\n\n"
                "اطلاعاتی برای نمایش پروفایل شما پیدا نشد.",
                parse_mode=ParseMode.HTML,
                reply_markup=_profile_keyboard(),
            )
            return

        text = format_dashboard(dashboard)

        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=_profile_keyboard(),
        )

    except Exception:
        await query.edit_message_text(
            "❌ در نمایش پروفایل مشکلی پیش آمد.\n"
            "لطفاً دوباره تلاش کنید.",
            reply_markup=_profile_keyboard(),
        )


async def route_profile_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route profile-related callbacks.
    """
    query = update.callback_query

    if query is None:
        return

    callback_data = query.data or ""

    if callback_data == PROFILE_CALLBACK:
        await show_profile(update, context)


def profile_handlers_health_check() -> dict:
    """
    Health check for the profile handlers module.
    """
    result = {
        "module": "profile.handlers",
        "status": "ok",
        "dependencies": {},
    }

    try:
        dashboard_result = dashboard_health_check()
        result["dependencies"]["core.dashboard"] = dashboard_result

        if isinstance(dashboard_result, dict):
            dashboard_status = dashboard_result.get("status")

            if dashboard_status not in (None, "ok", "healthy"):
                result["status"] = "warning"

    except Exception as exc:
        result["status"] = "error"
        result["dependencies"]["core.dashboard"] = {
            "status": "error",
            "error": str(exc),
        }

    return result


__all__ = [
    "PROFILE_CALLBACK",
    "PROFILE_BACK_CALLBACK",
    "show_profile",
    "route_profile_callback",
    "profile_handlers_health_check",
]
