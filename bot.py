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
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
    banking_chapter_1_text,
    banking_chapter_2_text,
    banking_chapter_3_text,
    banking_chapter_4_text,
    banking_chapter_5_text,
    banking_chapter_6_text,
    banking_chapter_7_text,
    banking_chapter_8_text,
    banking_chapter_9_text,
    banking_chapter_10_text,
    banking_chapter_11_text,
    banking_chapter_12_text,
    banking_exam_result,
    banking_full_exam_text,
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
🏦 بانکداری تخصصی
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
# BANKING MENU
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        banking_intro_text(),
        reply_markup=banking_menu()
    )


# =========================================================
# متن فصل‌ها
# =========================================================

CHAPTER_TEXT_FUNCTIONS = {

    1: banking_chapter_1_text,
    2: banking_chapter_2_text,
    3: banking_chapter_3_text,
    4: banking_chapter_4_text,
    5: banking_chapter_5_text,
    6: banking_chapter_6_text,
    7: banking_chapter_7_text,
    8: banking_chapter_8_text,
    9: banking_chapter_9_text,
    10: banking_chapter_10_text,
    11: banking_chapter_11_text,
    12: banking_chapter_12_text,

}


# =========================================================
# نمایش فصل
# =========================================================

async def banking_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.split("_")[-1]
        )

    except (ValueError, IndexError):

        await query.edit_message_text(
            "⚠️ خطا در شناسایی فصل.",
            reply_markup=banking_back_menu()
        )

        return


    if chapter not in CHAPTER_TEXT_FUNCTIONS:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    text = CHAPTER_TEXT_FUNCTIONS[chapter]()


    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون پایان فصل {chapter}",
                callback_data=f"banking_exam_intro_{chapter}"
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
# معرفی آزمون فصل
# =========================================================

async def banking_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.split("_")[-1]
        )

    except (ValueError, IndexError):

        await query.edit_message_text(
            "⚠️ خطا در شناسایی فصل.",
            reply_markup=banking_back_menu()
        )

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await query.edit_message_text(
            "❌ برای این فصل آزمونی ثبت نشده است.",
            reply_markup=banking_back_menu()
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
{len(questions)} سؤال

━━━━━━━━━━━━━━━━━━

📌 قوانین آزمون

• هر سؤال چهار گزینه دارد.
• فقط یک گزینه صحیح است.
• پاسخ هر سؤال بررسی می‌شود.
• امتیاز در پایان محاسبه می‌شود.

━━━━━━━━━━━━━━━━━━

🎯 پیشنهاد:

قبل از شروع آزمون،
درسنامه فصل را کامل مطالعه کنید.

هدف فقط حفظ کردن نیست؛
باید مفهوم را یاد بگیرید.

━━━━━━━━━━━━━━━━━━

👇 برای شروع آزمون روی دکمه زیر بزنید.
"""


    keyboard = [

        [
            InlineKeyboardButton(
                f"🚀 شروع آزمون فصل {chapter}",
                callback_data=f"banking_exam_start_{chapter}"
            )
        ],

        [
            InlineKeyboardButton(
                "📖 مرور درسنامه",
                callback_data=f"banking_chapter_{chapter}"
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
# شروع آزمون
# =========================================================

async def banking_exam_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.split("_")[-1]
        )

    except (ValueError, IndexError):

        await query.edit_message_text(
            "⚠️ خطا در شروع آزمون.",
            reply_markup=banking_back_menu()
        )

        return


    await show_banking_question(
        query=query,
        chapter=chapter,
        index=0,
        score=0
    )


# =========================================================
# نمایش سؤال
# =========================================================

async def show_banking_question(
    query,
    chapter,
    index,
    score
):

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

        await show_banking_result(
            query,
            chapter,
            score
        )

        return


    question = questions[index]


    text = f"""
📝 آزمون بانکداری

📘 فصل {chapter} | {CHAPTER_NAMES.get(chapter, "بانکداری")}

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
                        f"banking_answer:"
                        f"{chapter}:"
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
# پاسخ آزمون
# =========================================================

async def banking_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    try:

        data = query.data.split(":")

        chapter = int(data[1])
        index = int(data[2])
        selected = int(data[3])
        score = int(data[4])

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
                            "🔄 شروع دوباره",
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

        return


    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )


    if index < 0 or index >= len(questions):

        await query.edit_message_text(
            "⚠️ شماره سؤال نامعتبر است.",
            reply_markup=banking_back_menu()
        )

        return


    question = questions[index]

    correct = question["correct"]


    # =====================================================
    # بررسی پاسخ
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

    if next_index < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"banking_next:"
                        f"{chapter}:"
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


    else:

        await show_banking_result(
            query,
            chapter,
            score
        )


# =========================================================
# سؤال بعدی
# =========================================================

async def banking_next_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    try:

        data = query.data.split(":")

        chapter = int(data[1])
        index = int(data[2])
        score = int(data[3])

    except (IndexError, ValueError):

        await query.edit_message_text(
            "⚠️ خطا در ادامه آزمون.",
            reply_markup=banking_back_menu()
        )

        return


    await show_banking_question(
        query=query,
        chapter=chapter,
        index=index,
        score=score
    )


# =========================================================
# نتیجه آزمون
# =========================================================

async def show_banking_result(
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


    text, keyboard = banking_exam_result(
        chapter,
        score
    )


    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# آزمون جامع
# =========================================================

async def banking_full_exam_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    text = banking_full_exam_text()


    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع آزمون جامع",
                callback_data="banking_full_exam_start"
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
# آزمون جامع
# =========================================================

async def banking_full_exam_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    # فعلاً آزمون جامع از فصل‌ها به صورت ترکیبی
    # ساخته می‌شود.

    all_questions = []


    for chapter in range(1, 13):

        questions = BANKING_CHAPTER_QUESTIONS.get(
            chapter,
            []
        )

        for question in questions:

            all_questions.append(
                {
                    "chapter": chapter,
                    "question": question
                }
            )


    if not all_questions:

        await query.edit_message_text(
            "❌ سوالی برای آزمون جامع وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    # ذخیره آزمون جامع در user_data

    context.user_data["full_exam_questions"] = all_questions
    context.user_data["full_exam_index"] = 0
    context.user_data["full_exam_score"] = 0


    await show_full_exam_question(
        query,
        context
    )


# =========================================================
# نمایش سؤال آزمون جامع
# =========================================================

async def show_full_exam_question(
    query,
    context
):

    questions = context.user_data.get(
        "full_exam_questions",
        []
    )

    index = context.user_data.get(
        "full_exam_index",
        0
    )

    score = context.user_data.get(
        "full_exam_score",
        0
    )


    if index >= len(questions):

        await show_full_exam_result(
            query,
            context
        )

        return


    item = questions[index]

    chapter = item["chapter"]

    question = item["question"]


    text = f"""
🏆 آزمون جامع بانکداری

━━━━━━━━━━━━━━━━━━

📘 فصل: {chapter} | {CHAPTER_NAMES.get(chapter, "بانکداری")}

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز: {score}

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
                        f"full_answer:"
                        f"{index}:"
                        f"{option_index}"
                    )
                )
            ]
        )


    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# پاسخ آزمون جامع
# =========================================================

async def full_exam_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    try:

        data = query.data.split(":")

        index = int(data[1])
        selected = int(data[2])

    except (IndexError, ValueError):

        await query.edit_message_text(
            "⚠️ خطا در پردازش آزمون جامع.",
            reply_markup=banking_back_menu()
        )

        return


    questions = context.user_data.get(
        "full_exam_questions",
        []
    )


    if index < 0 or index >= len(questions):

        await query.edit_message_text(
            "⚠️ سؤال نامعتبر است.",
            reply_markup=banking_back_menu()
        )

        return


    item = questions[index]

    question = item["question"]

    correct = question["correct"]


    score = context.user_data.get(
        "full_exam_score",
        0
    )


    if selected == correct:

        score += 1

        result_text = """
✅ پاسخ صحیح است.

🎯 +۱ امتیاز
"""


    else:

        correct_option = question["options"][correct]

        result_text = f"""
❌ پاسخ صحیح نیست.

✅ پاسخ صحیح:

{correct_option}
"""


    context.user_data["full_exam_score"] = score

    next_index = index + 1

    context.user_data["full_exam_index"] = next_index


    if next_index < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data="full_exam_next"
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

        await show_full_exam_result(
            query,
            context
        )


# =========================================================
# سؤال بعدی جامع
# =========================================================

async def full_exam_next_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await show_full_exam_question(
        query,
        context
    )


# =========================================================
# نتیجه آزمون جامع
# =========================================================

async def show_full_exam_result(
    query,
    context
):

    questions = context.user_data.get(
        "full_exam_questions",
        []
    )

    score = context.user_data.get(
        "full_exam_score",
        0
    )


    total = len(questions)


    if total == 0:

        await query.edit_message_text(
            "❌ آزمون جامع وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return


    percentage = round(
        (score / total) * 100
    )


    if percentage >= 90:

        evaluation = "🏆 فوق‌العاده"

        message = (
            "تسلط شما بر مباحث بانکداری بسیار عالی است."
        )


    elif percentage >= 80:

        evaluation = "🥇 عالی"

        message = (
            "سطح آمادگی شما بسیار خوب است."
        )


    elif percentage >= 70:

        evaluation = "🥈 خوب"

        message = (
            "تسلط مناسبی دارید، اما مرور بعضی فصل‌ها مفید است."
        )


    elif percentage >= 50:

        evaluation = "🥉 متوسط"

        message = (
            "برای آزمون استخدامی، مرور و تست‌زنی بیشتر پیشنهاد می‌شود."
        )


    else:

        evaluation = "📚 نیازمند مطالعه"

        message = (
            "پیشنهاد می‌شود فصل‌های بانکداری را دوباره مطالعه کنید."
        )


    text = f"""
🏆 آزمون جامع بانکداری به پایان رسید.

━━━━━━━━━━━━━━━━━━

📊 نتیجه نهایی

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {total - score}

📈 درصد: {percentage}٪

🎯 ارزیابی: {evaluation}

━━━━━━━━━━━━━━━━━━

💡 {message}

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 آزمون دوباره",
                callback_data="banking_full_exam_start"
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
    # BANKING CHAPTERS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_chapter_callback,
            pattern=r"^banking_chapter_\d+$"
        )
    )


    # =====================================================
    # EXAM INTRO
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_intro_callback,
            pattern=r"^banking_exam_intro_\d+$"
        )
    )


    # =====================================================
    # EXAM START
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_start_callback,
            pattern=r"^banking_exam_start_\d+$"
        )
    )


    # =====================================================
    # EXAM ANSWER
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_answer_callback,
            pattern=r"^banking_answer:"
        )
    )


    # =====================================================
    # EXAM NEXT
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_next_callback,
            pattern=r"^banking_next:"
        )
    )


    # =====================================================
    # FULL EXAM
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_full_exam_callback,
            pattern=r"^banking_full_exam$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            banking_full_exam_start_callback,
            pattern=r"^banking_full_exam_start$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            full_exam_answer_callback,
            pattern=r"^full_answer:"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            full_exam_next_callback,
            pattern=r"^full_exam_next$"
        )
    )


    # =====================================================
    # TEMPORARY SECTIONS
    # =====================================================

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


    # =====================================================
    # RUN
    # =====================================================

    print(
        "🏛️ Andishkadeh Market Bot is running..."
    )

    application.run_polling()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()
