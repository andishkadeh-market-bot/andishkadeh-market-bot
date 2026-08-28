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

# =========================================================
# IMPORT MODULES
# =========================================================

from support import support_text, support_menu

from banking import (
    banking_menu,
    banking_intro_text,
    banking_chapter_text,
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
)

# ---------------------------------------------------------
# در نسخه بعدی این بخش‌ها به فایل‌های تخصصی جداگانه متصل
# می‌شوند:
#
# psychology.py
# management.py
# international_trade.py
# marketing.py
# economics.py
# employment_exam.py
# files.py
# social.py
# ---------------------------------------------------------


# =========================================================
# TOKEN
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
                "📚 آموزش تخصصی مدیریت",
                callback_data="management"
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
                "🏦 بانکداری تخصصی",
                callback_data="banking"
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
# WELCOME TEXT
# =========================================================

def welcome_text():

    return """
🏛️ اندیشکده مدیریت و بازار

مرکز تخصصی آموزش، آزمون و توسعه مهارت

━━━━━━━━━━━━━━━━━━

🎓 آموزش تخصصی
📝 آزمون و ارزیابی
📊 تحلیل عملکرد
📚 منابع آموزشی
🎯 آمادگی آزمون‌های استخدامی

━━━━━━━━━━━━━━━━━━

📚 حوزه‌های تخصصی:

🏢 مدیریت و مدیریت بازرگانی
🌍 تجارت بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار
🏦 بانکداری و خدمات مالی
🧠 روانشناسی و مددکاری

━━━━━━━━━━━━━━━━━━

🎯 سیستم آموزشی اندیشکده:

یادگیری مفهومی
⬇️
مطالعه تخصصی
⬇️
تمرین
⬇️
آزمون
⬇️
تحلیل عملکرد
⬇️
مرور نقاط ضعف

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

    text, keyboard = banking_intro_text()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# BANKING CHAPTER
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
            reply_markup=banking_menu()
        )

        return


    if chapter not in CHAPTER_NAMES:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=banking_menu()
        )

        return


    try:

        text = banking_chapter_text(chapter)

    except Exception as error:

        print(
            f"Banking chapter error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری درسنامه.

لطفاً دوباره تلاش کنید.
""",
            reply_markup=banking_menu()
        )

        return


    keyboard = []


    # -----------------------------------------------------
    # EXAM
    # -----------------------------------------------------

    if BANKING_CHAPTER_QUESTIONS.get(chapter):

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📝 آزمون فصل {chapter}",
                    callback_data=(
                        f"banking_exam_intro_{chapter}"
                    )
                )
            ]
        )


    # -----------------------------------------------------
    # PREVIOUS / NEXT
    # -----------------------------------------------------

    navigation = []


    if chapter > 1:

        navigation.append(
            InlineKeyboardButton(
                "⬅️ فصل قبل",
                callback_data=(
                    f"banking_chapter_{chapter - 1}"
                )
            )
        )


    if chapter < len(CHAPTER_NAMES):

        navigation.append(
            InlineKeyboardButton(
                "فصل بعد ➡️",
                callback_data=(
                    f"banking_chapter_{chapter + 1}"
                )
            )
        )


    if navigation:

        keyboard.append(navigation)


    # -----------------------------------------------------
    # BACK
    # -----------------------------------------------------

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
# BANKING EXAM INTRO
# =========================================================

async def banking_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "banking_exam_intro_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=banking_menu()
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
                            "📖 درسنامه",
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


    name = CHAPTER_NAMES.get(
        chapter,
        "بانکداری"
    )


    text = f"""
📝 آزمون پایان فصل {chapter}

🏦 {name}

━━━━━━━━━━━━━━━━━━

🎯 آزمون تخصصی و مفهومی

📝 تعداد سؤالات:
{len(questions)}

━━━━━━━━━━━━━━━━━━

📌 قوانین آزمون

• هر سؤال چهار گزینه دارد.
• فقط یک گزینه صحیح است.
• پاسخ‌ها بررسی می‌شوند.
• امتیاز شما محاسبه می‌شود.
• نتیجه در پایان نمایش داده می‌شود.

━━━━━━━━━━━━━━━━━━

💡 پیشنهاد:

ابتدا درسنامه را مطالعه کنید،
سپس آزمون را انجام دهید.

━━━━━━━━━━━━━━━━━━

👇 شروع آزمون
"""


    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 شروع آزمون",
                callback_data=(
                    f"banking_exam_{chapter}_0_0"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "📖 بازگشت به درسنامه",
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


    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# BANKING EXAM QUESTION
# =========================================================

async def banking_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (IndexError, ValueError):

        await query.edit_message_text(
            """
⚠️ اطلاعات آزمون نامعتبر است.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=banking_menu()
        )

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )


    if not questions:

        await query.edit_message_text(
            "❌ سوالی برای این فصل وجود ندارد.",
            reply_markup=banking_menu()
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

📘 فصل {chapter}
🏦 {name}

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

{question["question"]}

━━━━━━━━━━━━━━━━━━

👇 گزینه موردنظر را انتخاب کنید:
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
# BANKING ANSWER
# =========================================================

async def banking_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (IndexError, ValueError):

        await query.edit_message_text(
            """
⚠️ خطا در پردازش پاسخ.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=banking_menu()
        )

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )


    if index >= len(questions):

        await show_exam_result(
            query,
            chapter,
            score
        )

        return


    question = questions[index]

    correct = question["correct"]


    # -----------------------------------------------------
    # CORRECT
    # -----------------------------------------------------

    if selected == correct:

        score += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

آفرین 👏
"""


    # -----------------------------------------------------
    # WRONG
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # NEXT
    # -----------------------------------------------------

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
                    "📖 درسنامه فصل",
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
# EXAM RESULT
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
            reply_markup=banking_menu()
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
            "تسلط مناسبی دارید، اما مرور فصل پیشنهاد می‌شود."
        )

    elif percentage >= 50:

        evaluation = "🟡 متوسط"
        message = (
            "بعضی مفاهیم نیاز به مرور و تمرین بیشتری دارند."
        )

    else:

        evaluation = "📚 نیازمند مطالعه"
        message = (
            "پیشنهاد می‌شود درسنامه فصل را دوباره مطالعه کنید."
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

🎯 ارزیابی:
{evaluation}

━━━━━━━━━━━━━━━━━━

💡 {message}

━━━━━━━━━━━━━━━━━━

🎯 مسیر پیشنهادی:

مرور اشتباهات
⬇️
مطالعه دوباره
⬇️
آزمون مجدد
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


    if chapter < len(CHAPTER_NAMES):

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 فصل {chapter + 1}",
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
# TEMPORARY SECTIONS
# =========================================================

async def temporary_section(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    section_names = {

        "management":
            "📚 مدیریت و مدیریت بازرگانی",

        "international_trade":
            "🌍 تجارت بین‌الملل",

        "marketing":
            "📈 بازاریابی و فروش",

        "economics":
            "💰 اقتصاد و بازار",

        "employment_exam":
            "📝 آزمون استخدامی",

        "random_questions":
            "🎲 سوالات تصادفی",

        "psychology_socialwork":
            "🧠 روانشناسی و مددکاری",

        "files":
            "📂 فایل و منابع آموزشی",

        "social":
            "📱 شبکه‌های اجتماعی",
    }


    section = section_names.get(
        query.data,
        "بخش آموزشی"
    )


    await query.edit_message_text(
        f"""
🚧 {section}

این بخش در حال توسعه است.

ساختار این قسمت به صورت تخصصی
و مستقل طراحی خواهد شد.

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
""",
        reply_markup=InlineKeyboardMarkup(
            [
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
# BANKING FULL EXAM PLACEHOLDER
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

این قسمت برای آزمون جامع
۱۲ فصل بانکداری در نظر گرفته شده است.

🚧 موتور آزمون جامع در مرحله بعد
به سیستم آزمون متصل می‌شود.

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=InlineKeyboardMarkup(
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
    )


# =========================================================
# UNKNOWN CALLBACK
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


    # =====================================================
    # START
    # =====================================================

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # =====================================================
    # HOME
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            home_callback,
            pattern=r"^home$"
        )
    )


    # =====================================================
    # SUPPORT
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            support_callback,
            pattern=r"^support$"
        )
    )


    # =====================================================
    # BANKING
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_callback,
            pattern=r"^banking$"
        )
    )


    # =====================================================
    # BANKING FULL EXAM
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_full_exam_callback,
            pattern=r"^banking_full_exam$"
        )
    )


    # =====================================================
    # BANKING CHAPTER
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_chapter_callback,
            pattern=r"^banking_chapter_[0-9]+$"
        )
    )


    # =====================================================
    # BANKING EXAM INTRO
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_intro_callback,
            pattern=r"^banking_exam_intro_[0-9]+$"
        )
    )


    # =====================================================
    # BANKING EXAM QUESTION
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_question_callback,
            pattern=r"^banking_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )


    # =====================================================
    # BANKING ANSWER
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_answer_callback,
            pattern=r"^banking_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
        )
    )


    # =====================================================
    # OTHER SECTIONS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(management|"
                r"international_trade|"
                r"marketing|"
                r"economics|"
                r"employment_exam|"
                r"random_questions|"
                r"psychology_socialwork|"
                r"files|"
                r"social)$"
            )
        )
    )


    # =====================================================
    # UNKNOWN
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            unknown_callback
        )
    )


    # =====================================================
    # RUN
    # =====================================================

    print(
        "🏛️ Andishkadeh Market Bot is running..."
    )

    application.run_polling()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    main()
