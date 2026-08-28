# =========================================================
# bot.py
# 🏛️ اندیشکده مدیریت و بازار
# نسخه جدید و یکپارچه
# =========================================================

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
# IMPORTS
# =========================================================

from support import (
    support_text,
    support_menu,
)

from banking import (
    banking_menu,
    banking_back_menu,
    banking_intro_text,
    banking_chapter_text,
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
)

from psychology import (
    psychology_menu,
    psychology_intro_text,
    psychology_topic_text,
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
# 📝 متن خوش‌آمدگویی
# =========================================================

def welcome_text():

    return """
🏛️ اندیشکده مدیریت و بازار

مرکز تخصصی آموزش، آزمون و توسعه مهارت‌های حرفه‌ای

━━━━━━━━━━━━━━━━━━

📚 آموزش تخصصی
📝 آزمون‌های استخدامی
🎲 سوالات تصادفی
🧠 روانشناسی و مددکاری
🏦 بانکداری تخصصی
🌍 تجارت بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار
📂 فایل و منابع آموزشی

━━━━━━━━━━━━━━━━━━

🎯 سیستم آموزشی اندیشکده

آموزش مفهومی
⬇️
مطالعه تخصصی
⬇️
تمرین
⬇️
آزمون
⬇️
ارزیابی
⬇️
مرور اشتباهات

━━━━━━━━━━━━━━━━━━

📌 هدف:

کمک به یادگیری واقعی،
آمادگی آزمون‌های استخدامی،
افزایش مهارت‌های مدیریتی،
مالی و تجاری.

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

    if not update.message:
        return

    await update.message.reply_text(
        welcome_text(),
        reply_markup=main_menu()
    )


# =========================================================
# 🏠 بازگشت به خانه
# =========================================================

async def home_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

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

    try:
        await query.answer()
    except Exception:
        pass

    await query.edit_message_text(
        support_text(),
        reply_markup=support_menu()
    )


# =========================================================
# 🏦 بانکداری
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        text, keyboard = banking_intro_text()

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except Exception as error:

        print(
            f"Banking loading error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری بخش بانکداری.

لطفاً فایل banking.py را بررسی کنید.
""",
            reply_markup=main_menu()
        )


# =========================================================
# 📘 فصل بانکداری
# =========================================================

async def banking_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        chapter = int(
            query.data.replace(
                "banking_chapter_",
                ""
            )
        )

    except (ValueError, TypeError):

        await query.edit_message_text(
            "❌ شماره فصل معتبر نیست.",
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

        result = banking_chapter_text(chapter)

        # تابع banking_chapter_text ممکن است
        # متن و کیبورد را برگرداند.

        if isinstance(result, tuple):

            text, keyboard = result

        else:

            text = result

            keyboard = InlineKeyboardMarkup(
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
                    ]
                ]
            )

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except Exception as error:

        print(
            f"Banking chapter {chapter} error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری درسنامه.

لطفاً دوباره تلاش کنید.
""",
            reply_markup=banking_back_menu()
        )


# =========================================================
# 📝 معرفی آزمون فصل
# =========================================================

async def banking_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        chapter = int(
            query.data.replace(
                "banking_exam_intro_",
                ""
            )
        )

    except (ValueError, TypeError):

        await query.edit_message_text(
            "❌ شماره فصل معتبر نیست.",
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
                    ]
                ]
            )
        )

        return

    name = CHAPTER_NAMES.get(
        chapter,
        "بانکداری"
    )

    text = f"""
📝 آزمون فصل {chapter}

🏦 {name}

━━━━━━━━━━━━━━━━━━

🎯 آزمون تخصصی

تعداد سؤالات:
{len(questions)}

━━━━━━━━━━━━━━━━━━

📌 قوانین

• هر سؤال چهار گزینه دارد.
• فقط یک پاسخ صحیح است.
• پاسخ صحیح امتیاز دارد.
• نتیجه در پایان نمایش داده می‌شود.

━━━━━━━━━━━━━━━━━━

🎯 پیشنهاد:

ابتدا درسنامه را مطالعه کنید،
سپس آزمون را شروع کنید.

━━━━━━━━━━━━━━━━━━
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
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 سؤال آزمون
# =========================================================

async def banking_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (IndexError, ValueError, TypeError):

        await query.edit_message_text(
            """
⚠️ اطلاعات آزمون معتبر نیست.

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
            "❌ سؤال‌های این فصل پیدا نشد.",
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

📘 فصل {chapter}
🏦 {name}

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز: {score}

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
# 📝 پاسخ آزمون
# =========================================================

async def banking_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (IndexError, ValueError, TypeError):

        await query.edit_message_text(
            """
⚠️ خطا در پردازش پاسخ.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=banking_back_menu()
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

        correct_option = (
            question["options"][correct]
        )

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
                    "📖 درسنامه",
                    callback_data=(
                        f"banking_chapter_{chapter}"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    "🏦 خروج",
                    callback_data="banking"
                )
            ]
        ]

        await query.edit_message_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
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
            "پیشنهاد می‌شود."
        )

    elif percentage >= 50:

        evaluation = "🟡 متوسط"

        message = (
            "برخی مفاهیم نیاز به مرور و تمرین "
            "بیشتری دارند."
        )

    else:

        evaluation = "📚 نیازمند مطالعه"

        message = (
            "پیشنهاد می‌شود درسنامه را دوباره "
            "مطالعه کرده و آزمون را تکرار کنید."
        )

    name = CHAPTER_NAMES.get(
        chapter,
        "بانکداری"
    )

    text = f"""
🏁 آزمون فصل {chapter} تمام شد.

🏦 {name}

━━━━━━━━━━━━━━━━━━

📊 نتیجه

📝 تعداد سؤالات: {total}

✅ صحیح: {score}

❌ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی:
{evaluation}

━━━━━━━━━━━━━━━━━━

💡 {message}

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
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
        ]
    ]

    if chapter < 12:

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
            ]
        ]
    )

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# 🧠 روانشناسی و مددکاری
# =========================================================

async def psychology_socialwork_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        text = psychology_intro_text()

        await query.edit_message_text(
            text,
            reply_markup=psychology_menu()
        )

    except Exception as error:

        print(
            f"Psychology loading error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری بخش روانشناسی و مددکاری.

لطفاً فایل psychology.py را بررسی کنید.
""",
            reply_markup=main_menu()
        )


# =========================================================
# 🧠 موضوعات روانشناسی و مددکاری
# =========================================================

async def psychology_topic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    try:

        topic_id = int(
            query.data.replace(
                "psychology_topic_",
                ""
            )
        )

    except (ValueError, TypeError):

        await query.edit_message_text(
            "❌ موضوع انتخاب‌شده معتبر نیست.",
            reply_markup=psychology_menu()
        )

        return

    try:

        result = psychology_topic_text(
            topic_id
        )

        if isinstance(result, tuple):

            text, keyboard = result

        else:

            text = result

            keyboard = psychology_menu()

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except Exception as error:

        print(
            f"Psychology topic {topic_id} error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری محتوای این موضوع.

لطفاً دوباره تلاش کنید.
""",
            reply_markup=psychology_menu()
        )


# =========================================================
# 🚧 بخش‌های در حال توسعه
# =========================================================

async def temporary_section(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    await query.edit_message_text(
        """
🚧 این بخش در حال توسعه است.

محتوای تخصصی این قسمت در نسخه‌های
بعدی اندیشکده اضافه خواهد شد.

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

آموزش تخصصی
+
آزمون
+
منابع
+
مهارت حرفه‌ای
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
# ⚠️ Callback ناشناخته
# =========================================================

async def unknown_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    try:
        await query.answer(
            "این گزینه در حال حاضر فعال نیست."
        )
    except Exception:
        pass


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
    # /start
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
    # PSYCHOLOGY
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_socialwork_callback,
            pattern=r"^psychology_socialwork$"
        )
    )

    # =====================================================
    # PSYCHOLOGY TOPICS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_topic_callback,
            pattern=r"^psychology_topic_[0-9]+$"
        )
    )

    # =====================================================
    # OTHER SECTIONS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(education|"
                r"employment_exam|"
                r"random_questions|"
                r"international_trade|"
                r"marketing|"
                r"economics|"
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

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
