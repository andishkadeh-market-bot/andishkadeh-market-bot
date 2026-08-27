import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from support import support_text, support_menu

from banking import (
    banking_menu,
    banking_chapter_1_text,
    chapter_1_exam_menu,
    chapter_1_exam_text,
    BANKING_CHAPTER_1_QUESTIONS,
)


# =========================================================
# TOKEN
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

🎯 یادگیری مفهومی
+
📝 تمرین و آزمون
+
📊 ارزیابی عملکرد

━━━━━━━━━━━━━━━━━━

👇 بخش موردنظر خود را انتخاب کنید.
"""


# =========================================================
# /start
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
# منوی اصلی
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
# حمایت از اندیشکده
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
# منوی بانکداری
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🏦 بانکداری تخصصی

مرکز آموزش تخصصی بانکداری و آمادگی
آزمون‌های استخدامی بانک‌ها

━━━━━━━━━━━━━━━━━━

📚 ساختار آموزشی:

هر فصل شامل:

📖 درسنامه تخصصی
🧠 نکات مهم
💡 مثال‌های کاربردی
⭐ نکات آزمونی
📝 آزمون پایان فصل

━━━━━━━━━━━━━━━━━━

🎯 مسیر پیشنهادی:

فصل ۱
⬇️
مطالعه درسنامه
⬇️
آزمون فصل
⬇️
ارزیابی نتیجه
⬇️
فصل بعد

━━━━━━━━━━━━━━━━━━

🏆 در پایان:
آزمون جامع بانکداری

👇 فصل موردنظر را انتخاب کنید.
"""

    await query.edit_message_text(
        text,
        reply_markup=banking_menu()
    )


# =========================================================
# فصل اول بانکداری
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
# معرفی آزمون فصل اول
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
# شروع واقعی آزمون فصل اول
# =========================================================

async def banking_ch1_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await show_banking_ch1_question(
        query,
        index=0,
        score=0
    )


# =========================================================
# نمایش سؤال
# =========================================================

async def show_banking_ch1_question(
    query,
    index,
    score
):

    questions = BANKING_CHAPTER_1_QUESTIONS

    # جلوگیری از خطای شماره سؤال
    if index >= len(questions):

        await show_banking_ch1_result(
            query,
            score
        )

        return


    question = questions[index]

    text = f"""
📝 آزمون پایان فصل ۱

🏦 مبانی بانکداری

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

{question["question"]}

━━━━━━━━━━━━━━━━━━

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
                        f"banking_ch1_answer:"
                        f"{index}:"
                        f"{option_index}:"
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
# پاسخ سؤال
# =========================================================

async def banking_ch1_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split(":")

        index = int(data[1])
        selected = int(data[2])
        score = int(data[3])

    except (IndexError, ValueError):

        await query.edit_message_text(
            """
⚠️ خطایی در پردازش پاسخ رخ داد.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 شروع دوباره آزمون",
                            callback_data="banking_ch1_start"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔙 بانکداری",
                            callback_data="banking"
                        )
                    ],
                ]
            )
        )

        return


    question = BANKING_CHAPTER_1_QUESTIONS[index]

    correct = question["correct"]


    # =====================================================
    # پاسخ صحیح
    # =====================================================

    if selected == correct:

        score += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

آفرین، به سؤال بعدی بروید.
"""

    # =====================================================
    # پاسخ غلط
    # =====================================================

    else:

        correct_option = question["options"][correct]

        result_text = f"""
❌ پاسخ صحیح نیست.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{correct_option}

━━━━━━━━━━━━━━━━━━

⭐ امتیاز فعلی: {score}
"""


    next_index = index + 1


    # =====================================================
    # سؤال بعدی
    # =====================================================

    if next_index < len(
        BANKING_CHAPTER_1_QUESTIONS
    ):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"banking_ch1_next:"
                        f"{next_index}:"
                        f"{score}"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    "🏦 خروج از آزمون",
                    callback_data="banking"
                )
            ],

        ]

        await query.edit_message_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =====================================================
    # پایان آزمون
    # =====================================================

    else:

        await show_banking_ch1_result(
            query,
            score
        )


# =========================================================
# سؤال بعدی
# =========================================================

async def banking_ch1_next_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split(":")

        index = int(data[1])
        score = int(data[2])

    except (IndexError, ValueError):

        await query.edit_message_text(
            "⚠️ خطا در ادامه آزمون."
        )

        return


    await show_banking_ch1_question(
        query,
        index,
        score
    )


# =========================================================
# نتیجه آزمون
# =========================================================

async def show_banking_ch1_result(
    query,
    score
):

    total = len(
        BANKING_CHAPTER_1_QUESTIONS
    )

    percentage = round(
        (score / total) * 100
    )


    if percentage >= 80:

        level = "🏆 عالی"

        message = (
            "تسلط بسیار خوبی روی مباحث فصل دارید."
        )

    elif percentage >= 60:

        level = "🥈 خوب"

        message = (
            "مفاهیم اصلی را یاد گرفته‌اید، "
            "اما مرور بیشتر باعث تسلط شما می‌شود."
        )

    elif percentage >= 40:

        level = "🟡 نیاز به مرور"

        message = (
            "پیشنهاد می‌شود درسنامه فصل را دوباره "
            "مطالعه کنید و سپس آزمون را تکرار کنید."
        )

    else:

        level = "🔴 نیاز به مطالعه مجدد"

        message = (
            "پیشنهاد می‌شود ابتدا درسنامه فصل را "
            "به‌طور کامل مرور کنید."
        )


    text = f"""
🏁 آزمون فصل اول به پایان رسید.

🏦 مبانی بانکداری

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {total - score}

📈 درصد: {percentage}٪

🎯 ارزیابی: {level}

━━━━━━━━━━━━━━━━━━

💡 {message}

━━━━━━━━━━━━━━━━━━

📚 بعد از تسلط بر این فصل،
می‌توانید وارد فصل بعدی شوید.
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
                callback_data="banking_ch1_start"
            )
        ],

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
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
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

محتوای تخصصی این قسمت به‌زودی
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
    # /start
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
    # CHAPTER 1
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
    # CHAPTER 1 EXAM START
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_ch1_start_callback,
            pattern=r"^banking_ch1_start$"
        )
    )


    # -----------------------------------------------------
    # CHAPTER 1 ANSWERS
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_ch1_answer_callback,
            pattern=r"^banking_ch1_answer:"
        )
    )


    # -----------------------------------------------------
    # CHAPTER 1 NEXT
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            banking_ch1_next_callback,
            pattern=r"^banking_ch1_next:"
        )
    )


    # -----------------------------------------------------
    # TEMPORARY SECTIONS
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(education|"
                r"employment_exam|"
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
# START
# =========================================================

if __name__ == "__main__":

    main()
