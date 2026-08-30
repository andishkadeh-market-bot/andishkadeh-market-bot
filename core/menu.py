"""
Central menu router for Andishkadeh Management & Market.
"""

from telegram import Update
from telegram.ext import ContextTypes

from core.keyboards import main_menu_keyboard

from modules.management.handlers import (
    show_management_menu,
    show_management_chapter,
    show_management_lesson,
    start_management_quiz,
    answer_management_quiz,
    cancel_management_quiz,
)


async def show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show the main bot menu."""

    if update.message:
        await update.message.reply_text(
            "🏛️ <b>اندیشکده مدیریت و بازار</b>\n\n"
            "لطفاً بخش موردنظر خود را انتخاب کنید:",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )

        return

    if update.callback_query:
        query = update.callback_query

        await query.answer()

        await query.edit_message_text(
            "🏛️ <b>اندیشکده مدیریت و بازار</b>\n\n"
            "لطفاً بخش موردنظر خود را انتخاب کنید:",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )


async def route_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route callback queries to the correct module."""

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    # ------------------------------------------------------
    # Main menu
    # ------------------------------------------------------

    if data == "menu_main":
        await show_main_menu(
            update,
            context,
        )
        return

    # ------------------------------------------------------
    # Management
    # ------------------------------------------------------

    if data == "menu_management":
        await show_management_menu(
            update,
            context,
        )
        return

    if data.startswith(
        "management_chapter:"
    ):
        await show_management_chapter(
            update,
            context,
        )
        return

    if data.startswith(
        "management_lesson:"
    ):
        await show_management_lesson(
            update,
            context,
        )
        return

    # ------------------------------------------------------
    # Management Quiz
    # ------------------------------------------------------

    if data.startswith(
        "management_quiz:"
    ):
        await start_management_quiz(
            update,
            context,
        )
        return

    if data.startswith(
        "quiz_answer:"
    ):
        await answer_management_quiz(
            update,
            context,
        )
        return

    if data == "quiz_cancel":
        await cancel_management_quiz(
            update,
            context,
        )
        return

    # ------------------------------------------------------
    # Temporary fallback
    # ------------------------------------------------------

    await query.answer(
        "این بخش هنوز فعال نشده است.",
        show_alert=False,
    )
