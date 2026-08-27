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
    banking_back_menu,
    banking_intro_text,
    banking_chapter_text,
    chapter_exam_menu,
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
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
# 🏠 منوی اصلی
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
# 👋 متن خوش‌آمدگویی
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
# 🏠 بازگشت به منوی اصلی
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
# 🤝 حمایت
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
# 🏦 منوی بانکداری
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text, keyboard = banking_intro_text()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# 📚 نمایش فصل بانکداری
# =========================================================

async def banking_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "banking_chapter_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=banking_back_menu()
        )

        return


    if chapter not in CHAPTER_NAMES:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    try:

        text, keyboard = banking_chapter_text(chapter)

    except Exception as error:

        print(
            f"Error loading chapter {chapter}: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری درسنامه.

لطفاً بعداً دوباره تلاش کنید.
""",
            reply_markup=banking_back_menu()
        )

        return


    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# 📝 منوی آزمون فصل
# =========================================================

async def banking_exam_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "banking_exam_menu_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=banking_back_menu()
        )

        return


    if chapter not in CHAPTER_NAMES:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )


    if not questions:

        await query.edit_message_text(
            """
❌ برای این فصل هنوز سؤال آزمون ثبت نشده است.
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📖 مشاهده درسنامه",
                            callback_data=(
                                f"banking_chapter_{chapter}"
                            )
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🏦 بانکداری",
                            callback_data="banking"
                        )
                    ],
                ]
            )
        )

        return


    text, keyboard = chapter_exam_menu(chapter)

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# 📝 نمایش سؤال آزمون
# =========================================================

async def banking_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        # banking_exam_1_0_0

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (IndexError, ValueError):

        await query.edit_message_text(
            """
⚠️ خطا در اطلاعات آزمون.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=banking_back_menu()
        )

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )


    if not questions:

        await query.edit_message_text(
            "❌ سوالی برای این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    if index >= len(questions):

        await show_exam_result(
            query,
            chapter,
            score
        )

        return


    question = questions[index]

    name = CHAPTER_NAMES.get(
        chapter,
        "بانکداری"
    )


    text = f"""
📝 آزمون بانکداری

📘 فصل {chapter} | {name}

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
                        f"banking_answer_"
                        f"{chapter}_"
                        f"{index}_"
                        f"{option_index}_"
                        f"{score}"
                    )
                )
            ]
        )


    keyboard.append(
        [
            InlineKeyboardButton(
                "🏦 خروج از آزمون",
                callback_data="banking"
            )
        ]
    )


    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 پردازش پاسخ
# =========================================================

async def banking_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        # banking_answer_1_0_0_0

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (IndexError, ValueError):

        await query.edit_message_text(
            """
⚠️ خطایی در پردازش پاسخ رخ داد.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=banking_back_menu()
        )

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )


    if not questions:

        await query.edit_message_text(
            "❌ سوالی برای این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    if index >= len(questions):

        await show_exam_result(
            query,
            chapter,
            score
        )

        return


    question = questions[index]

    correct = question["correct"]


    if selected == correct:

        score += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

آفرین 👏
"""


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


    if next_index < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"banking_exam_"
                        f"{chapter}_"
                        f"{next_index}_"
                        f"{score}"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    "📖 مشاهده درسنامه",
                    callback_data=(
                        f"banking_chapter_{chapter}"
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


    else:

        await show_exam_result(
            query,
            chapter,
            score
        )


# =========================================================
# 🏁 نتیجه آزمون
# =========================================================

async def show_exam_result(
    query,
    chapter,
    score
):

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    total = len(questions)


    if total == 0:

        await query.edit_message_text(
            "❌ آزمونی برای این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    wrong = total - score

    percentage = round(
        (score / total) * 100
    )


    if percentage >= 90:

        evaluation = "🏆 فوق‌العاده"

        message = (
            "تسلط شما بر این فصل بسیار عالی است."
        )

    elif percentage >= 80:

        evaluation = "🥇 عالی"

        message = (
            "تسلط بسیار خوبی روی مباحث فصل دارید."
        )

    elif percentage >= 70:

        evaluation = "🥈 خوب"

        message = (
            "تسلط مناسبی دارید، اما مرور فصل "
            "باعث تسلط بیشتر شما می‌شود."
        )

    elif percentage >= 50:

        evaluation = "🟡 متوسط"

        message = (
            "بعضی مفاهیم نیاز به مرور و تمرین "
            "بیشتری دارند."
        )

    else:

        evaluation = "📚 نیازمند مطالعه"

        message = (
            "پیشنهاد می‌شود درسنامه فصل را دوباره "
            "مطالعه کنید و آزمون را تکرار کنید."
        )


    name = CHAPTER_NAMES.get(
        chapter,
        "بانکداری"
    )


    text = f"""
🏁 آزمون فصل {chapter} به پایان رسید.

🏦 {name}

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی: {evaluation}

━━━━━━━━━━━━━━━━━━

💡 {message}

━━━━━━━━━━━━━━━━━━

🎯 هدف اندیشکده:

یادگیری مفهومی
+
تست‌زنی
+
مرور هدفمند
+
آمادگی آزمون استخدامی
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
                callback_data=(
                    f"banking_exam_{chapter}_0_0"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "📖 مرور فصل",
                callback_data=(
                    f"banking_chapter_{chapter}"
                )
            )
        ],
    ]


    if chapter < 12:

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 ورود به فصل {chapter + 1}",
                    callback_data=(
                        f"banking_chapter_{chapter + 1}"
                    )
                )
            ]
        )


    keyboard.extend(
        [

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
    )


    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 🏆 آزمون جامع
# =========================================================

async def banking_full_exam_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        """
🏆 آزمون جامع بانکداری

━━━━━━━━━━━━━━━━━━

🚧 آزمون جامع در حال توسعه است.

در نسخه بعدی، سؤالات تمام فصل‌های
بانکداری در یک آزمون ترکیبی قرار می‌گیرند.

━━━━━━━━━━━━━━━━━━

📚 فصل‌های موجود:

۱. مبانی بانکداری
۲. سپرده‌ها و حساب‌ها
۳. تسهیلات و اعتبارات
۴. عقود بانکی
۵. قوانین و مقررات
۶. چک و اسناد بانکی
۷. مبارزه با پولشویی
۸. اعتبارسنجی
۹. بانکداری الکترونیک
۱۰. مدیریت ریسک
۱۱. بانک مرکزی و سیاست پولی
۱۲. بانکداری اسلامی
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏦 بازگشت به بانکداری",
                        callback_data="banking"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 منوی اصلی",
                        callback_data="home"
                    )
                ]
            ]
        )
    )


# =========================================================
# 🚧 بخش‌های موقت
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

━━━━━━━━━━━━━━━━━━

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
# ⚠️ Callback ناشناخته
# =========================================================

async def unknown_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer(
        "این گزینه در حال حاضر فعال نیست."
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


    # /start

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # HOME

    application.add_handler(
        CallbackQueryHandler(
            home_callback,
            pattern=r"^home$"
        )
    )


    # SUPPORT

    application.add_handler(
        CallbackQueryHandler(
            support_callback,
            pattern=r"^support$"
        )
    )


    # BANKING

    application.add_handler(
        CallbackQueryHandler(
            banking_callback,
            pattern=r"^banking$"
        )
    )


    # BANKING CHAPTER

    application.add_handler(
        CallbackQueryHandler(
            banking_chapter_callback,
            pattern=r"^banking_chapter_[0-9]+$"
        )
    )


    # BANKING EXAM MENU

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_menu_callback,
            pattern=r"^banking_exam_menu_[0-9]+$"
        )
    )


    # BANKING EXAM QUESTIONS

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_question_callback,
            pattern=r"^banking_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )


    # BANKING ANSWERS

    application.add_handler(
        CallbackQueryHandler(
            banking_answer_callback,
            pattern=r"^banking_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
        )
    )


    # FULL EXAM

    application.add_handler(
        CallbackQueryHandler(
            banking_full_exam_callback,
            pattern=r"^banking_full_exam$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            banking_full_exam_callback,
            pattern=r"^banking_full_exam_start$"
        )
    )


    # TEMPORARY SECTIONS

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


    # UNKNOWN

    application.add_handler(
        CallbackQueryHandler(
            unknown_callback
        )
    )


    print(
        "🏛️ Andishkadeh Market Bot is running..."
    )


    application.run_polling()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
