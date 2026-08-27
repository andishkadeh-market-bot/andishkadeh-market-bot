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

from banking import (
    banking_menu,
    banking_back_menu,
    banking_chapter_1_text,
    chapter_1_exam_menu,
    chapter_1_exam_text,
    BANKING_CHAPTER_1_QUESTIONS,
)


# =========================================================
# BOT TOKEN
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set in Render Environment Variables."
    )


# =========================================================
# MAIN MENU
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
# WELCOME
# =========================================================

def welcome_text():

    return """
🏛️ اندیشکده مدیریت و بازار

مرکز تخصصی آموزش، آزمون و توسعه مهارت

━━━━━━━━━━━━━━━━━━

📚 آموزش تخصصی
📝 آزمون‌های استخدامی
🎲 سوالات تصادفی
🧠 روانشناسی و مددکاری
📖 منابع آموزشی
🚀 توسعه مهارت‌های حرفه‌ای

━━━━━━━━━━━━━━━━━━

📖 حوزه‌های آموزشی:

📚 مدیریت و مدیریت بازرگانی
🌍 تجارت و بازرگانی بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار
🏦 بانکداری و خدمات مالی
🧠 روانشناسی و مددکاری

━━━━━━━━━━━━━━━━━━

👇 بخش موردنظر خود را انتخاب کنید.
"""


# =========================================================
# START
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
# HOME
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
# SUPPORT
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
# BANKING MAIN MENU
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🏦 بانکداری تخصصی

مرکز آموزش تخصصی بانکداری و آمادگی آزمون‌های استخدامی بانک‌ها

━━━━━━━━━━━━━━━━━━

📚 مسیر یادگیری را از فصل اول شروع کنید.

هر فصل شامل:

📖 درسنامه تخصصی
🧠 نکات مهم
💡 مثال و توضیح مفهومی
📝 آزمون پایان فصل

━━━━━━━━━━━━━━━━━━

🎯 پس از تکمیل فصل‌ها:
🏆 آزمون جامع بانکداری

👇 فصل موردنظر را انتخاب کنید.
"""

    await query.edit_message_text(
        text,
        reply_markup=banking_menu()
    )


# =========================================================
# BANKING CHAPTER 1
# =========================================================

async def banking_chapter_1_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = banking_chapter_1_text()

    keyboard = [
        [
            InlineKeyboardButton(
                "📝 آزمون پایان فصل ۱",
                callback_data="banking_ch1_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بانکداری",
                callback_data="banking"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# CHAPTER 1 EXAM INTRO
# =========================================================

async def banking_ch1_exam_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        chapter_1_exam_text(),
        reply_markup=chapter_1_exam_menu()
    )


# =========================================================
# CHAPTER 1 QUESTION
# =========================================================

async def banking_ch1_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    index: int = 0,
    score: int = 0
):

    query = update.callback_query

    question = BANKING_CHAPTER_1_QUESTIONS[index]

    text = f"""
📝 آزمون پایان فصل ۱

🏦 مبانی بانکداری

━━━━━━━━━━━━━━━━━━

سؤال {index + 1} از {len(BANKING_CHAPTER_1_QUESTIONS)}

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

{question["question"]}

👇 گزینه صحیح را انتخاب کنید:
"""

    keyboard = []

    for option_index, option in enumerate(
        question["options"]
    ):

        keyboard.append(
            [
                InlineKeyboardButton(
                    option,
                    callback_data=(
                        f"banking_ch1_answer_"
                        f"{index}_"
                        f"{option_index}_"
                        f"{score}"
                    )
                )
            ]
        )

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# CHAPTER 1 ANSWER
# =========================================================

async def banking_ch1_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data.split("_")

    index = int(data[3])
    selected = int(data[4])
    score = int(data[5])

    question = BANKING_CHAPTER_1_QUESTIONS[index]

    correct = question["correct"]

    if selected == correct:

        score += 1

        result_text = """
✅ پاسخ صحیح بود.

🎯 یک امتیاز دریافت کردید.
"""

    else:

        correct_option = question["options"][correct]

        result_text = f"""
❌ پاسخ صحیح نیست.

✅ پاسخ صحیح:

{correct_option}
"""


    next_index = index + 1

    if next_index < len(BANKING_CHAPTER_1_QUESTIONS):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"banking_ch1_next_"
                        f"{next_index}_"
                        f"{score}"
                    )
                )
            ],

        ]

        await query.edit_message_text(

            result_text,

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    else:

        total = len(
            BANKING_CHAPTER_1_QUESTIONS
        )

        percentage = round(
            (score / total) * 100
        )

        if percentage >= 80:

            level = "🏆 عالی"

        elif percentage >= 60:

            level = "🥈 خوب"

        elif percentage >= 40:

            level = "🟡 نیاز به مرور"

        else:

            level = "🔴 نیاز به مطالعه مجدد فصل"


        final_text = f"""
🏁 آزمون فصل اول به پایان رسید.

🏦 مبانی بانکداری

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون:

تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {total - score}

📈 درصد: {percentage}٪

🎯 ارزیابی: {level}

━━━━━━━━━━━━━━━━━━

📚 پیشنهاد:

برای تسلط بیشتر، نکات فصل را دوباره
مرور کنید و سپس به فصل بعد بروید.
"""

        keyboard = [

            [
                InlineKeyboardButton(
                    "📖 مرور فصل",
                    callback_data="banking_chapter_1"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏦 بانکداری",
                    callback_data="banking"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="home"
                )
            ],

        ]

        await query.edit_message_text(

            final_text,

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )


# =========================================================
# NEXT QUESTION
# =========================================================

async def banking_ch1_next_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    data = query.data.split("_")

    index = int(data[3])
    score = int(data[4])

    await query.answer()

    await banking_ch1_question(
        update,
        context,
        index,
        score
    )


# =========================================================
# TEMPORARY SECTIONS
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
# MAIN
# =========================================================

def main():

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    # -----------------------------------------------------
    # START
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # -----------------------------------------------------
    # HOME
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            home_callback,
            pattern=r"^home$"
        )
    )


    # -----------------------------------------------------
    # SUPPORT
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            support_callback,
            pattern=r"^support$"
        )
    )


    # -----------------------------------------------------
    # BANKING
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_callback,
            pattern=r"^banking$"
        )
    )


    # -----------------------------------------------------
    # BANKING CHAPTER 1
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_chapter_1_callback,
            pattern=r"^banking_chapter_1$"
        )
    )


    # -----------------------------------------------------
    # CHAPTER 1 EXAM INTRO
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_ch1_exam_callback,
            pattern=r"^banking_ch1_exam$"
        )
    )


    # -----------------------------------------------------
    # CHAPTER 1 ANSWER
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_ch1_answer_callback,
            pattern=r"^banking_ch1_answer_"
        )
    )


    # -----------------------------------------------------
    # CHAPTER 1 NEXT
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_ch1_next_callback,
            pattern=r"^banking_ch1_next_"
        )
    )


    # -----------------------------------------------------
    # TEMPORARY SECTIONS
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(education|employment_exam|"
                r"random_questions|"
                r"psychology_socialwork|"
                r"international_trade|"
                r"marketing|"
                r"economics|"
                r"files|"
                r"social)$"
            )
        )
    )


    # -----------------------------------------------------
    # RUN
    # -----------------------------------------------------

    print(
        "🏛️ Andishkadeh Market Bot is running..."
    )

    application.run_polling()


# =========================================================
# START BOT
# =========================================================

if __name__ == "__main__":

    main()
