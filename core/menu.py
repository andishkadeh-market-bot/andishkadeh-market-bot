"""
Central menu routing for Andishkadeh Management & Market.
"""

from telegram import Update
from telegram.ext import ContextTypes

from core.keyboards import main_menu_keyboard, back_button


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
    """
    Temporary section handler.

    Real educational modules will replace this handler later.
    """

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
