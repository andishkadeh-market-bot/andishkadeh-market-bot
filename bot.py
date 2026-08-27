import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from support import (
    support_text,
    support_menu,
)


# =========================================================
# تنظیمات ربات
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set in Render Environment Variables."
    )


# =========================================================
# منوی اصلی
# =========================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="education"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون استخدامی",
                callback_data="employment_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🎲 سوالات تصادفی",
                callback_data="random_questions"
            )
        ],

        [
            InlineKeyboardButton(
                "🧠 روانشناسی و مددکاری",
                callback_data="psychology_socialwork"
            )
        ],

        [
            InlineKeyboardButton(
                "🏦 بانکداری تخصصی",
                callback_data="banking"
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 تجارت بین‌الملل",
                callback_data="international_trade"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 بازاریابی و فروش",
                callback_data="marketing"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 اقتصاد و بازار",
                callback_data="economics"
            )
        ],

        [
            InlineKeyboardButton(
                "📂 فایل و منابع آموزشی",
                callback_data="files"
            )
        ],

        [
            InlineKeyboardButton(
                "📱 شبکه‌های اجتماعی",
                callback_data="social"
            )
        ],

        [
            InlineKeyboardButton(
                "🤝 حمایت از اندیشکده",
                callback_data="support"
            )
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# متن خوش‌آمدگویی
# =========================================================

def welcome_text():

    return """
🏛️ اندیشکده مدیریت و بازار

مرکز تخصصی آموزش، آزمون و توسعه مهارت

━━━━━━━━━━━━━━━━━━

🎯 اینجا می‌توانید:

📚 آموزش ببینید
📝 آزمون بدهید
🎲 سوالات تصادفی حل کنید
🧠 روانشناسی و مددکاری را یاد بگیرید
📖 منابع آموزشی دریافت کنید
🚀 برای مسیر حرفه‌ای آماده شوید

━━━━━━━━━━━━━━━━━━

📖 حوزه‌های تخصصی:

📚 مدیریت و مدیریت بازرگانی
🌍 تجارت و بازرگانی بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار
🏦 بانکداری و خدمات مالی
🧠 روانشناسی و مددکاری

━━━━━━━━━━━━━━━━━━

✨ امکانات:

📝 آزمون‌های استخدامی
🎲 سوالات تصادفی
🏆 آزمون‌های جامع
📊 نمایش نتیجه آزمون
📚 درسنامه‌های تخصصی
📂 منابع آموزشی
📱 شبکه‌های اجتماعی
🤝 حمایت از اندیشکده

━━━━━━━━━━━━━━━━━━

👇 از منوی زیر بخش موردنظر خود را انتخاب کنید.
"""


# =========================================================
# دستور /start
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message:

        await update.message.reply_text(
            welcome_text(),
            reply_markup=main_menu()
        )


# =========================================================
# بازگشت به منوی اصلی
# =========================================================

async def home_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        welcome_text(),
        reply_markup=main_menu()
    )


# =========================================================
# بخش حمایت
# =========================================================

async def support_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        support_text(),
        reply_markup=support_menu()
    )


# =========================================================
# بخش‌های موقت
# =========================================================

async def temporary_section(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        """
🚧 این بخش در حال توسعه است.

به‌زودی محتوای کامل این قسمت
در اندیشکده مدیریت و بازار قرار می‌گیرد.

🏛️ اندیشکده مدیریت و بازار
""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 منوی اصلی",
                        callback_data="home"
                    )
                ]
            ]
        )
    )


# =========================================================
# اجرای اصلی ربات
# =========================================================

def main():

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    # -----------------------------------------------------
    # /start
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # -----------------------------------------------------
    # منوی اصلی
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            home_callback,
            pattern=r"^home$"
        )
    )


    # -----------------------------------------------------
    # حمایت
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            support_callback,
            pattern=r"^support$"
        )
    )


    # -----------------------------------------------------
    # بخش‌های در حال توسعه
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(education|employment_exam|"
                r"random_questions|psychology_socialwork|"
                r"banking|international_trade|marketing|"
                r"economics|files|social)$"
            )
        )
    )


    # -----------------------------------------------------
    # اجرای ربات
    # -----------------------------------------------------

    print(
        "🏛️ Andishkadeh Market Bot is running..."
    )

    application.run_polling()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()
