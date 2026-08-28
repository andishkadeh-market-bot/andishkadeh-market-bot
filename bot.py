# =========================================================
# bot.py
# 🏛️ اندیشکده مدیریت و بازار
# نسخه جامع + اتصال آزمون استخدامی
# سازگار با Render Free Web Service
# =========================================================

import os
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

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
# SUPPORT
# =========================================================

from support import (
    support_text,
    support_menu,
)

# =========================================================
# BANKING
# =========================================================

from banking import (
    banking_menu,
    banking_back_menu,
    banking_intro_text,
    banking_chapter_text,
    CHAPTER_NAMES as BANKING_CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
)

# =========================================================
# INTERNATIONAL TRADE
# =========================================================

from international_trade import (
    international_trade_menu,
    international_trade_back_menu,
    international_trade_intro_text,
    international_trade_chapter_text,
    CHAPTER_NAMES as TRADE_CHAPTER_NAMES,
    INTERNATIONAL_TRADE_QUESTIONS,
)

# =========================================================
# MARKETING
# =========================================================

from marketing import (
    marketing_menu,
    marketing_back_menu,
    marketing_intro_text,
    marketing_chapter_text,
    marketing_exam_menu,
    marketing_exam_intro_text,
    marketing_question_data,
    marketing_answer_data,
    marketing_result_text,
    marketing_result_menu,
    marketing_has_chapter,
    CHAPTER_NAMES as MARKETING_CHAPTER_NAMES,
)

# =========================================================
# EMPLOYMENT EXAM
# =========================================================

from employment_exam import (
    employment_exam_callback,
    employment_exam_menu,
    employment_bank_callback,
    employment_difficulty_callback,
    employment_start_callback,
    employment_random_callback,
    employment_simulation_callback,
    employment_simulation_start_callback,
    employment_answer_callback,
    employment_next_callback,
)

# =========================================================
# تنظیمات
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

PORT = int(
    os.getenv("PORT", "10000")
)

if not TOKEN:
    raise RuntimeError(
        "❌ BOT_TOKEN در Environment Variables تنظیم نشده است."
    )


# =========================================================
# HTTP SERVER
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path in ["/", "/health"]:

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/plain; charset=utf-8"
            )

            self.end_headers()

            self.wfile.write(
                "Andishkadeh Market Bot is running."
                .encode("utf-8")
            )

        else:

            self.send_response(404)

            self.end_headers()

    def log_message(self, format, *args):

        return


def start_http_server():

    server = HTTPServer(
        ("0.0.0.0", PORT),
        HealthHandler
    )

    print(
        f"🌐 HTTP server running on 0.0.0.0:{PORT}"
    )

    server.serve_forever()


def run_http_server():

    thread = Thread(
        target=start_http_server,
        daemon=True
    )

    thread.start()


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
🏦 بانکداری تخصصی
🌍 تجارت بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

🎯 سیستم آموزشی اندیشکده:

📖 آموزش مفهومی
+
📝 تمرین و آزمون
+
📊 ارزیابی
+
🔄 مرور و تکرار

━━━━━━━━━━━━━━━━━━

👇 بخش موردنظر خود را انتخاب کنید.
"""


# =========================================================
# START
# =========================================================

async def start(update, context):

    if update.message:

        await update.message.reply_text(
            welcome_text(),
            reply_markup=main_menu()
        )


# =========================================================
# HOME
# =========================================================

async def home_callback(update, context):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        welcome_text(),
        reply_markup=main_menu()
    )


# =========================================================
# SUPPORT
# =========================================================

async def support_callback(update, context):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        support_text(),
        reply_markup=support_menu()
    )


# =========================================================
# BANKING
# =========================================================

async def banking_callback(update, context):

    query = update.callback_query

    await query.answer()

    result = banking_intro_text()

    if isinstance(result, tuple):

        text = result[0]
        keyboard = result[1]

    else:

        text = result
        keyboard = banking_menu()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def banking_chapter_callback(update, context):

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

    if chapter not in BANKING_CHAPTER_NAMES:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return

    text = banking_chapter_text(chapter)

    if isinstance(text, tuple):

        text = text[0]

    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون فصل {chapter}",
                callback_data=f"banking_exam_intro_{chapter}"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ فصل قبل",
                callback_data=(
                    f"banking_chapter_{chapter - 1}"
                    if chapter > 1
                    else "banking"
                )
            ),

            InlineKeyboardButton(
                "فصل بعد ➡️",
                callback_data=(
                    f"banking_chapter_{chapter + 1}"
                    if chapter < len(BANKING_CHAPTER_NAMES)
                    else "banking"
                )
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


async def banking_exam_intro_callback(update, context):

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
            reply_markup=banking_back_menu()
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await query.edit_message_text(
            "❌ برای این فصل هنوز سؤال ثبت نشده است.",
            reply_markup=banking_back_menu()
        )

        return

    name = BANKING_CHAPTER_NAMES.get(
        chapter,
        "بانکداری"
    )

    text = f"""
📝 آزمون پایان فصل {chapter}

🏦 {name}

━━━━━━━━━━━━━━━━━━

📝 تعداد سؤالات:
{len(questions)}

━━━━━━━━━━━━━━━━━━

👇 برای شروع آزمون:
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع آزمون",
                callback_data=f"banking_exam_{chapter}_0_0"
            )
        ],

        [
            InlineKeyboardButton(
                "📖 بازگشت به درسنامه",
                callback_data=f"banking_chapter_{chapter}"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def banking_exam_question_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در اطلاعات آزمون.",
            reply_markup=banking_back_menu()
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if index >= len(questions):

        await show_banking_result(
            query,
            chapter,
            score
        )

        return

    question = questions[index]

    name = BANKING_CHAPTER_NAMES.get(
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

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def banking_answer_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در پردازش پاسخ.",
            reply_markup=banking_back_menu()
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    question = questions[index]

    if selected == question["correct"]:

        score += 1

        result = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز: {score}
"""

    else:

        result = f"""
❌ پاسخ اشتباه است.

✅ پاسخ صحیح:

{question["options"][question["correct"]]}

⭐ امتیاز: {score}
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
                    "🏦 خروج",
                    callback_data="banking"
                )
            ]

        ]

        await query.edit_message_text(
            result,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await show_banking_result(
            query,
            chapter,
            score
        )


async def show_banking_result(query, chapter, score):

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    total = len(questions)

    if total == 0:

        await query.edit_message_text(
            "❌ آزمون وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return

    percentage = round(
        (score / total) * 100
    )

    wrong = total - score

    if percentage >= 90:
        evaluation = "🏆 فوق‌العاده"
    elif percentage >= 80:
        evaluation = "🥇 عالی"
    elif percentage >= 70:
        evaluation = "🥈 خوب"
    elif percentage >= 50:
        evaluation = "🟡 متوسط"
    else:
        evaluation = "📚 نیازمند مطالعه"

    text = f"""
🏁 آزمون پایان یافت.

━━━━━━━━━━━━━━━━━━

📝 کل سوالات: {total}

✅ صحیح: {score}

❌ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی:

{evaluation}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار",
                callback_data=f"banking_exam_{chapter}_0_0"
            )
        ],

        [
            InlineKeyboardButton(
                "📖 مرور فصل",
                callback_data=f"banking_chapter_{chapter}"
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
# INTERNATIONAL TRADE
# =========================================================

async def international_trade_callback(update, context):

    query = update.callback_query

    await query.answer()

    result = international_trade_intro_text()

    if isinstance(result, tuple):

        text = result[0]
        keyboard = result[1]

    else:

        text = result
        keyboard = international_trade_menu()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def international_trade_chapter_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "international_trade_chapter_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=international_trade_back_menu()
        )

        return

    if chapter not in TRADE_CHAPTER_NAMES:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=international_trade_back_menu()
        )

        return

    text = international_trade_chapter_text(
        chapter
    )

    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون فصل {chapter}",
                callback_data=f"trade_exam_intro_{chapter}"
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
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def trade_exam_intro_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "trade_exam_intro_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=international_trade_back_menu()
        )

        return

    questions = INTERNATIONAL_TRADE_QUESTIONS.get(
        chapter,
        []
    )

    text = f"""
📝 آزمون تجارت بین‌الملل

📘 فصل {chapter}

━━━━━━━━━━━━━━━━━━

📝 تعداد سوالات:
{len(questions)}

━━━━━━━━━━━━━━━━━━
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع آزمون",
                callback_data=f"trade_exam_{chapter}_0_0"
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 تجارت بین‌الملل",
                callback_data="international_trade"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def trade_exam_question_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در آزمون.",
            reply_markup=international_trade_back_menu()
        )

        return

    questions = INTERNATIONAL_TRADE_QUESTIONS.get(
        chapter,
        []
    )

    if index >= len(questions):

        await show_trade_result(
            query,
            chapter,
            score
        )

        return

    question = questions[index]

    text = f"""
📝 آزمون تجارت بین‌الملل

📘 فصل {chapter}

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز: {score}

━━━━━━━━━━━━━━━━━━

{question["question"]}
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
                        f"trade_answer_"
                        f"{chapter}_"
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


async def trade_answer_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا.",
            reply_markup=international_trade_back_menu()
        )

        return

    questions = INTERNATIONAL_TRADE_QUESTIONS.get(
        chapter,
        []
    )

    question = questions[index]

    if selected == question["correct"]:

        score += 1

        result = "✅ پاسخ صحیح است.\n\n🎯 +۱ امتیاز"

    else:

        result = (
            "❌ پاسخ اشتباه است.\n\n"
            "✅ پاسخ صحیح:\n\n"
            + question["options"][question["correct"]]
        )

    next_index = index + 1

    if next_index < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"trade_exam_"
                        f"{chapter}_"
                        f"{next_index}_"
                        f"{score}"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    "🌍 خروج",
                    callback_data="international_trade"
                )
            ]

        ]

        await query.edit_message_text(
            result,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await show_trade_result(
            query,
            chapter,
            score
        )


async def show_trade_result(query, chapter, score):

    questions = INTERNATIONAL_TRADE_QUESTIONS.get(
        chapter,
        []
    )

    total = len(questions)

    if total == 0:

        await query.edit_message_text(
            "❌ آزمون وجود ندارد.",
            reply_markup=international_trade_back_menu()
        )

        return

    percentage = round(
        (score / total) * 100
    )

    wrong = total - score

    if percentage >= 90:
        evaluation = "🏆 فوق‌العاده"
    elif percentage >= 80:
        evaluation = "🥇 عالی"
    elif percentage >= 70:
        evaluation = "🥈 خوب"
    elif percentage >= 50:
        evaluation = "🟡 متوسط"
    else:
        evaluation = "📚 نیازمند مطالعه"

    text = f"""
🏁 آزمون پایان یافت.

📝 کل سوالات: {total}

✅ صحیح: {score}

❌ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 {evaluation}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار",
                callback_data=f"trade_exam_{chapter}_0_0"
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
# MARKETING
# =========================================================

async def marketing_callback(update, context):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        marketing_intro_text(),
        reply_markup=marketing_menu()
    )


async def marketing_chapter_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "marketing_chapter_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=marketing_back_menu()
        )

        return

    if not marketing_has_chapter(chapter):

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=marketing_back_menu()
        )

        return

    text = marketing_chapter_text(
        chapter
    )

    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون فصل {chapter}",
                callback_data=f"marketing_exam_intro_{chapter}"
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
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def marketing_exam_intro_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "marketing_exam_intro_",
                ""
            )
        )

    except ValueError:

        await query.edit_message_text(
            "❌ شماره فصل نامعتبر است.",
            reply_markup=marketing_back_menu()
        )

        return

    await query.edit_message_text(
        marketing_exam_intro_text(chapter),
        reply_markup=marketing_exam_menu(chapter)
    )


async def marketing_exam_question_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا.",
            reply_markup=marketing_back_menu()
        )

        return

    result = marketing_question_data(
        chapter,
        index,
        score
    )

    if result is None:

        await query.edit_message_text(
            marketing_result_text(
                chapter,
                score
            ),
            reply_markup=marketing_result_menu(
                chapter
            )
        )

        return

    text, keyboard = result

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def marketing_answer_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا.",
            reply_markup=marketing_back_menu()
        )

        return

    result = marketing_answer_data(
        chapter,
        index,
        selected,
        score
    )

    if result is None:

        await query.edit_message_text(
            "❌ خطا در آزمون.",
            reply_markup=marketing_back_menu()
        )

        return

    if result["finished"]:

        await query.edit_message_text(
            marketing_result_text(
                chapter,
                result["score"]
            ),
            reply_markup=marketing_result_menu(
                chapter
            )
        )

        return

    keyboard = [

        [
            InlineKeyboardButton(
                "➡️ سؤال بعدی",
                callback_data=(
                    f"marketing_exam_"
                    f"{chapter}_"
                    f"{result['next_index']}_"
                    f"{result['score']}"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "📈 خروج",
                callback_data="marketing"
            )
        ]

    ]

    await query.edit_message_text(
        result["result_text"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# ECONOMICS
# =========================================================

def economics_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📚 آموزش اقتصاد",
                callback_data="economics_lessons"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 مفاهیم اقتصادی",
                callback_data="economics_concepts"
            )
        ],

        [
            InlineKeyboardButton(
                "💹 اقتصاد و بازار",
                callback_data="economics_market"
            )
        ],

        [
            InlineKeyboardButton(
                "🏦 سیاست پولی",
                callback_data="economics_monetary"
            )
        ],

        [
            InlineKeyboardButton(
                "🏛️ سیاست مالی",
                callback_data="economics_fiscal"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 تورم و رشد اقتصادی",
                callback_data="economics_inflation_growth"
            )
        ],

        [
            InlineKeyboardButton(
                "💵 ارز و نرخ بهره",
                callback_data="economics_currency_interest"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون اقتصاد",
                callback_data="economics_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ])


def economics_text():

    return """
💰 اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

مرکز آموزش مفاهیم اقتصاد، بازارهای مالی
و تحلیل متغیرهای اقتصادی

━━━━━━━━━━━━━━━━━━

📚 مباحث:

• مبانی اقتصاد
• عرضه و تقاضا
• بازار و قیمت
• تورم
• رشد اقتصادی
• بیکاری
• سیاست پولی
• سیاست مالی
• نرخ بهره
• نرخ ارز
• بانک مرکزی
• نقدینگی
• GDP
• رکود و رونق
• بازارهای مالی
"""


def economics_lessons_text():

    return """
📚 آموزش اقتصاد

━━━━━━━━━━━━━━━━━━

اقتصاد علمی است که نحوه تخصیص منابع
محدود برای نیازهای نامحدود را بررسی می‌کند.

━━━━━━━━━━━━━━━━━━

🔹 عرضه

مقدار کالا یا خدماتی که فروشندگان حاضر
به عرضه آن هستند.

🔹 تقاضا

مقدار کالا یا خدماتی که خریداران حاضر
به خرید آن هستند.

━━━━━━━━━━━━━━━━━━

📌 در شرایط برابر:

افزایش قیمت → کاهش مقدار تقاضا

افزایش قیمت → افزایش تمایل به عرضه
"""


def economics_concepts_text():

    return """
📊 مفاهیم مهم اقتصادی

━━━━━━━━━━━━━━━━━━

🔥 تورم:
افزایش مستمر و عمومی سطح قیمت‌ها.

📈 رشد اقتصادی:
افزایش ظرفیت تولید کالا و خدمات.

👷 بیکاری:
فرد آماده و مایل به کار است ولی شغل ندارد.

🏭 GDP:
ارزش کالاها و خدمات نهایی تولیدشده
در اقتصاد طی یک دوره مشخص.

💧 نقدینگی:
پول و شبه‌پول موجود در اقتصاد.

💵 نرخ بهره:
هزینه استفاده از پول در طول زمان.
"""


def economics_market_text():

    return """
💹 اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

عوامل مهم:

• تورم
• نرخ بهره
• نرخ ارز
• نقدینگی
• سیاست دولت
• سیاست بانک مرکزی
• رشد اقتصادی
• عرضه و تقاضا
• انتظارات
• شرایط سیاسی
"""


def economics_monetary_text():

    return """
🏦 سیاست پولی

━━━━━━━━━━━━━━━━━━

سیاست پولی مجموعه اقدامات بانک مرکزی
برای اثرگذاری بر پول، اعتبار و شرایط
مالی اقتصاد است.

ابزارها:

• نرخ‌های سیاستی
• عملیات بازار باز
• مدیریت ذخایر
• ابزارهای اعتباری
"""


def economics_fiscal_text():

    return """
🏛️ سیاست مالی

━━━━━━━━━━━━━━━━━━

سیاست مالی مربوط به درآمدها و مخارج دولت است.

💰 درآمد:
• مالیات
• درآمدهای عمومی
• عوارض

💸 مخارج:
• خدمات عمومی
• پروژه‌های عمرانی
• حقوق
• حمایت‌های اجتماعی

📈 انبساطی:
افزایش مخارج یا کاهش مالیات.

📉 انقباضی:
کاهش مخارج یا افزایش مالیات.
"""


def economics_inflation_growth_text():

    return """
📈 تورم و رشد اقتصادی

━━━━━━━━━━━━━━━━━━

تورم با رشد اقتصادی یکسان نیست.

رشد اقتصادی به افزایش تولید و ظرفیت تولید
اقتصاد مربوط می‌شود.

عوامل رشد:

• سرمایه‌گذاری
• نیروی کار
• بهره‌وری
• فناوری
• زیرساخت
• کیفیت نهادها
"""


def economics_currency_interest_text():

    return """
💵 ارز و نرخ بهره

━━━━━━━━━━━━━━━━━━

نرخ ارز قیمت یک پول نسبت به پول دیگر است.

عوامل مؤثر:

• تورم
• نرخ بهره
• عرضه و تقاضای ارز
• صادرات
• واردات
• انتظارات
• سیاست پولی
• شرایط بین‌المللی
"""


ECONOMICS_QUESTIONS = [

    {
        "question": "کدام گزینه تعریف مناسب‌تری از تورم است؟",
        "options": [
            "افزایش یک کالا",
            "افزایش مستمر و عمومی سطح قیمت‌ها",
            "کاهش تولید",
            "افزایش درآمد"
        ],
        "correct": 1
    },

    {
        "question": "کدام گزینه با سیاست پولی ارتباط بیشتری دارد؟",
        "options": [
            "مالیات",
            "بودجه دولت",
            "نرخ بهره و نقدینگی",
            "هزینه عمرانی"
        ],
        "correct": 2
    },

    {
        "question": "GDP چه چیزی را اندازه‌گیری می‌کند؟",
        "options": [
            "دارایی خانوارها",
            "ارزش کالاها و خدمات نهایی تولیدشده",
            "پول نقد",
            "فقط صادرات"
        ],
        "correct": 1
    },

    {
        "question": "در شرایط برابر، افزایش قیمت چه اثری بر مقدار تقاضا دارد؟",
        "options": [
            "افزایش",
            "کاهش",
            "دو برابر",
            "بدون تغییر قطعی"
        ],
        "correct": 1
    },

    {
        "question": "کدام مورد ابزار سیاست مالی است؟",
        "options": [
            "مالیات",
            "عملیات بازار باز",
            "ذخایر بانکی",
            "نرخ سیاستی"
        ],
        "correct": 0
    },

]


async def economics_exam_callback(update, context):

    query = update.callback_query

    await query.answer()

    context.user_data["economics_questions"] = (
        ECONOMICS_QUESTIONS
    )

    await economics_exam_question_callback(
        update,
        context
    )


async def economics_exam_question_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        index = int(data[2])
        score = int(data[3])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در آزمون اقتصاد.",
            reply_markup=economics_menu()
        )

        return

    if index >= len(ECONOMICS_QUESTIONS):

        await show_economics_result(
            query,
            score
        )

        return

    question = ECONOMICS_QUESTIONS[index]

    text = f"""
📝 آزمون اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(ECONOMICS_QUESTIONS)}

⭐ امتیاز: {score}

━━━━━━━━━━━━━━━━━━

{question["question"]}
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
                        f"economics_answer_"
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


async def economics_answer_callback(update, context):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        index = int(data[2])
        selected = int(data[3])
        score = int(data[4])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا.",
            reply_markup=economics_menu()
        )

        return

    question = ECONOMICS_QUESTIONS[index]

    if selected == question["correct"]:

        score += 1

        result = "✅ پاسخ صحیح است.\n\n🎯 +۱ امتیاز"

    else:

        result = (
            "❌ پاسخ اشتباه است.\n\n"
            "✅ پاسخ صحیح:\n\n"
            + question["options"][question["correct"]]
        )

    next_index = index + 1

    if next_index < len(ECONOMICS_QUESTIONS):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"economics_exam_"
                        f"{next_index}_"
                        f"{score}"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    "💰 خروج",
                    callback_data="economics"
                )
            ]

        ]

        await query.edit_message_text(
            result,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await show_economics_result(
            query,
            score
        )


async def show_economics_result(query, score):

    total = len(ECONOMICS_QUESTIONS)

    wrong = total - score

    percentage = round(
        (score / total) * 100
    )

    if percentage >= 90:
        evaluation = "🏆 فوق‌العاده"
    elif percentage >= 80:
        evaluation = "🥇 عالی"
    elif percentage >= 70:
        evaluation = "🥈 خوب"
    elif percentage >= 50:
        evaluation = "🟡 متوسط"
    else:
        evaluation = "📚 نیازمند مطالعه"

    text = f"""
🏁 آزمون اقتصاد پایان یافت.

━━━━━━━━━━━━━━━━━━

📝 سوالات: {total}

✅ صحیح: {score}

❌ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 {evaluation}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
                callback_data="economics_exam_0_0"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 آموزش اقتصاد",
                callback_data="economics_lessons"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 اقتصاد",
                callback_data="economics"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def economics_callback(update, context):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        economics_text(),
        reply_markup=economics_menu()
    )


async def economics_subsection_callback(update, context):

    query = update.callback_query

    await query.answer()

    texts = {

        "economics_lessons":
            economics_lessons_text(),

        "economics_concepts":
            economics_concepts_text(),

        "economics_market":
            economics_market_text(),

        "economics_monetary":
            economics_monetary_text(),

        "economics_fiscal":
            economics_fiscal_text(),

        "economics_inflation_growth":
            economics_inflation_growth_text(),

        "economics_currency_interest":
            economics_currency_interest_text(),

    }

    text = texts.get(
        query.data,
        "❌ این بخش وجود ندارد."
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "💰 اقتصاد و بازار",
                callback_data="economics"
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
# TEMPORARY
# =========================================================

async def temporary_section(update, context):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        """
🚧 این بخش در حال توسعه است.

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
# UNKNOWN
# =========================================================

async def unknown_callback(update, context):

    query = update.callback_query

    if query:

        try:

            await query.answer(
                "این گزینه در حال حاضر فعال نیست."
            )

        except Exception:
            pass


# =========================================================
# ERROR
# =========================================================

async def error_handler(update, context):

    print("❌ Telegram error:")
    print(context.error)


# =========================================================
# APPLICATION
# =========================================================

def create_application():

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

    # =====================================================
    # EMPLOYMENT EXAM
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            employment_exam_callback,
            pattern=r"^employment_exam$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_bank_callback,
            pattern=r"^employment_bank_(refah|shahr|mehr|government)$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_difficulty_callback,
            pattern=r"^employment_difficulty_(easy|medium|hard)$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_start_callback,
            pattern=(
                r"^employment_start_"
                r"(bank_(refah|shahr|mehr|government)_(easy|medium|hard|all)"
                r"|difficulty_(easy|medium|hard))$"
            )
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_random_callback,
            pattern=r"^employment_random$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_simulation_callback,
            pattern=r"^employment_simulation$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_simulation_start_callback,
            pattern=r"^employment_simulation_start$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_answer_callback,
            pattern=r"^employment_answer_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_next_callback,
            pattern=r"^employment_next_[0-9]+_[0-9]+$"
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

    application.add_handler(
        CallbackQueryHandler(
            banking_chapter_callback,
            pattern=r"^banking_chapter_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_intro_callback,
            pattern=r"^banking_exam_intro_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_question_callback,
            pattern=r"^banking_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            banking_answer_callback,
            pattern=r"^banking_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    # =====================================================
    # INTERNATIONAL TRADE
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            international_trade_callback,
            pattern=r"^international_trade$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            international_trade_chapter_callback,
            pattern=r"^international_trade_chapter_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            trade_exam_intro_callback,
            pattern=r"^trade_exam_intro_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            trade_exam_question_callback,
            pattern=r"^trade_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            trade_answer_callback,
            pattern=r"^trade_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    # =====================================================
    # MARKETING
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            marketing_callback,
            pattern=r"^marketing$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            marketing_chapter_callback,
            pattern=r"^marketing_chapter_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            marketing_exam_intro_callback,
            pattern=r"^marketing_exam_intro_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            marketing_exam_question_callback,
            pattern=r"^marketing_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            marketing_answer_callback,
            pattern=r"^marketing_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    # =====================================================
    # ECONOMICS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            economics_callback,
            pattern=r"^economics$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            economics_subsection_callback,
            pattern=(
                r"^(economics_lessons|"
                r"economics_concepts|"
                r"economics_market|"
                r"economics_monetary|"
                r"economics_fiscal|"
                r"economics_inflation_growth|"
                r"economics_currency_interest)$"
            )
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            economics_exam_question_callback,
            pattern=r"^economics_exam_[0-9]+_[0-9]+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            economics_answer_callback,
            pattern=r"^economics_answer_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    # =====================================================
    # TEMPORARY
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(education|"
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

    application.add_error_handler(
        error_handler
    )

    return application


# =========================================================
# MAIN
# =========================================================

def main():

    print(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    print(
        "🏛️ Andishkadeh Market Bot"
    )

    print(
        "🚀 Starting..."
    )

    print(
        f"🌐 Render PORT: {PORT}"
    )

    print(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    run_http_server()

    application = create_application()

    print(
        "🤖 Telegram application starting..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()
