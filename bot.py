import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set in Render Environment Variables."
    )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        """
🏛️ اندیشکده مدیریت و بازار

به مرکز آموزشی اندیشکده خوش آمدید.

📚 آموزش تخصصی
📝 آزمون و تست
🎲 سوالات تصادفی
🧠 روانشناسی و مددکاری
🏦 بانکداری
🌍 تجارت
📈 بازاریابی
💰 اقتصاد

━━━━━━━━━━━━━━━━━━

🚧 ربات در حال توسعه است.
به‌زودی بخش‌های آموزشی و آزمون‌ها فعال می‌شوند.
"""
    )


def main():

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    print(
        "🏛️ Andishkadeh Market Bot is running..."
    )

    application.run_polling()


if __name__ == "__main__":
    main()
