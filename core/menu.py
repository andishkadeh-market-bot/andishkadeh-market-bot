"""
Central menu routing for Andishkadeh Management & Market.
"""

from telegram import Update
from telegram.ext import ContextTypes

from core.keyboards import main_menu_keyboard, back_button

from modules.management.handlers import (
    show_management_menu,
    show_management_chapter,
    show_management_lesson,
)


MENU_TEXT = """
🏛️ <b>اندیشکده مدیریت و بازار</b>

مرکز آموزش و توسعه تخصصی مدیریت، تجارت و بازار

از منوی زیر حوزه موردنظر خود را انتخاب کنید:
"""


SECTION_TITLES = {
    "menu_education": "📚 آموزش تخصصی",
    "menu_exam": "📝 آزمون استخدامی",
    "menu_banking": "🏦 بانکداری تخصصی",
    "menu_accounting": "🧾 حسابداری",
    "menu_finance": "💳 مدیریت مالی",
    "menu_trade": "🌍 تجارت بین‌الملل",
    "menu_marketing": "📈 بازاریابی و فروش",
    "menu_economics": "💰 اقتصاد و بازار",
    "menu_psychology": "🧠 روانشناسی و مددکاری",
    "menu_random": "🎲 سوالات تصادفی",
    "menu_resources": "📂 فایل و منابع آموزشی",
    "menu_social": "📱 شبکه‌های اجتماعی",
    "menu_profile": "👤 پروفایل من",
    "menu_about": "ℹ️ درباره اندیشکده",
}


async def show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Display the main menu."""

    if update.message:
        await update.message.reply_text(
            MENU_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )

    elif update.callback_query:
        query = update.callback_query

        await query.answer()

        await query.edit_message_text(
            MENU_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )


async def show_section_placeholder(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Display a temporary placeholder for unfinished modules."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    section = SECTION_TITLES.get(
        query.data,
        "بخش انتخاب‌شده",
    )

    text = f"""
<b>{section}</b>

این بخش در معماری جدید ربات تعریف شده است.

📚 محتوای تخصصی این بخش به‌صورت ماژول مستقل اضافه خواهد شد.

🔹 درسنامه
🔹 زیرموضوع‌ها
🔹 آموزش مفصل
🔹 نکات تخصصی
🔹 نکات آزمونی
🔹 مثال کاربردی
🔹 آزمون
🔹 نتیجه
🔹 مرور
"""

    await query.edit_message_text(
        text,
        reply_markup=back_button(),
        parse_mode="HTML",
    )


async def route_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route menu callbacks to their corresponding module."""

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if data == "menu_management":
        await show_management_menu(
            update,
            context,
        )
        return

    if data.startswith("management_chapter:"):
        await show_management_chapter(
            update,
            context,
        )
        return

    if data.startswith("management_lesson:"):
        await show_management_lesson(
            update,
            context,
        )
        return

    if data == "menu_main":
        await show_main_menu(
            update,
            context,
        )
        return

    if data in SECTION_TITLES:
        await show_section_placeholder(
            update,
            context,
        )
        return

    await query.answer(
        "این گزینه هنوز فعال نشده است."
    )
