# =========================================================
# bot.py
# 🏛️ اندیشکده مدیریت و بازار
# نسخه جامع و پایدار
#
# Compatible with Render Free Web Service
# =========================================================

import os
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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

import employment_exam


# =========================================================
# PSYCHOLOGY & SOCIAL WORK
# =========================================================

import psychology_socialwork


# =========================================================
# ECONOMICS
# =========================================================

try:
    import economics
    ECONOMICS_AVAILABLE = True
except ImportError:
    economics = None
    ECONOMICS_AVAILABLE = False


# =========================================================
# TOKEN / PORT
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

if not TOKEN:
    raise RuntimeError(
        "❌ BOT_TOKEN در Environment Variables تنظیم نشده است."
    )


# =========================================================
# HTTP SERVER FOR RENDER
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
# PSYCHOLOGY MAIN
# =========================================================

async def psychology_socialwork_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    handler = getattr(
        psychology_socialwork,
        "psychology_socialwork_callback",
        None
    )

    if handler:

        try:

            return await handler(
                update,
                context
            )

        except Exception as error:

            print(
                f"❌ Psychology callback error: {error}"
            )

    menu_function = getattr(
        psychology_socialwork,
        "psychology_socialwork_menu",
        None
    )

    intro_function = getattr(
        psychology_socialwork,
        "psychology_socialwork_intro_text",
        None
    )

    if intro_function:

        try:

            text = intro_function()

        except Exception as error:

            print(
                f"❌ Psychology intro error: {error}"
            )

            text = psychology_default_text()

    else:

        text = psychology_default_text()

    if menu_function:

        try:

            keyboard = menu_function()

        except Exception as error:

            print(
                f"❌ Psychology menu error: {error}"
            )

            keyboard = psychology_default_menu()

    else:

        keyboard = psychology_default_menu()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


def psychology_default_text():

    return """
🧠 روانشناسی و مددکاری اجتماعی

━━━━━━━━━━━━━━━━━━

مرکز تخصصی آموزش:

🧠 مبانی روانشناسی
🤝 مددکاری اجتماعی
💬 مهارت‌های ارتباطی
👥 رفتار و شخصیت
🧩 روانشناسی اجتماعی
🎓 آمادگی آزمون

━━━━━━━━━━━━━━━━━━

🎯 هدف:

افزایش دانش روانشناختی
+
تقویت مهارت‌های ارتباطی
+
شناخت رفتار انسان
+
آمادگی آزمون‌های تخصصی

━━━━━━━━━━━━━━━━━━

👇 بخش موردنظر را انتخاب کنید.
"""


def psychology_default_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 آموزش روانشناسی",
                callback_data="psychology_lessons"
            )
        ],

        [
            InlineKeyboardButton(
                "🤝 مددکاری اجتماعی",
                callback_data="socialwork"
            )
        ],

        [
            InlineKeyboardButton(
                "🧠 مفاهیم روانشناسی",
                callback_data="psychology_concepts"
            )
        ],

        [
            InlineKeyboardButton(
                "💬 مهارت‌های ارتباطی",
                callback_data="psychology_communication"
            )
        ],

        [
            InlineKeyboardButton(
                "👥 رفتار و شخصیت",
                callback_data="psychology_behavior"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون روانشناسی",
                callback_data="psychology_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون مددکاری",
                callback_data="socialwork_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# PSYCHOLOGY SUBSECTIONS
# =========================================================

async def psychology_generic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    handler = getattr(
        psychology_socialwork,
        "psychology_callback",
        None
    )

    if handler:

        try:

            return await handler(
                update,
                context
            )

        except Exception as error:

            print(
                f"❌ Psychology module error: {error}"
            )

    data = query.data

    functions = {

        "psychology_lessons":
            "psychology_lessons_text",

        "psychology_concepts":
            "psychology_concepts_text",

        "psychology_communication":
            "psychology_communication_text",

        "psychology_behavior":
            "psychology_behavior_text",

        "socialwork":
            "socialwork_text",

        "psychology_exam":
            "psychology_exam_intro_text",

        "socialwork_exam":
            "socialwork_exam_intro_text",

    }

    function_name = functions.get(data)

    function = getattr(
        psychology_socialwork,
        function_name,
        None
    ) if function_name else None

    if function:

        try:

            text = function()

        except TypeError:

            try:

                text = function(data)

            except Exception as error:

                print(
                    f"❌ Psychology function error: {error}"
                )

                text = psychology_fallback_text(data)

        except Exception as error:

            print(
                f"❌ Psychology section error: {error}"
            )

            text = psychology_fallback_text(data)

    else:

        text = psychology_fallback_text(data)

    keyboard = [

        [
            InlineKeyboardButton(
                "🧠 روانشناسی و مددکاری",
                callback_data="psychology_socialwork"
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


def psychology_fallback_text(data):

    titles = {

        "psychology_lessons":
            "📚 آموزش روانشناسی",

        "psychology_concepts":
            "🧠 مفاهیم روانشناسی",

        "psychology_communication":
            "💬 مهارت‌های ارتباطی",

        "psychology_behavior":
            "👥 رفتار و شخصیت",

        "socialwork":
            "🤝 مددکاری اجتماعی",

        "psychology_exam":
            "📝 آزمون روانشناسی",

        "socialwork_exam":
            "📝 آزمون مددکاری",

    }

    return f"""
{titles.get(data, "🧠 روانشناسی و مددکاری")}

━━━━━━━━━━━━━━━━━━

🚧 محتوای این بخش در حال آماده‌سازی است.

🏛️ اندیشکده مدیریت و بازار
"""


# =========================================================
# BANKING
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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

    if chapter not in BANKING_CHAPTER_NAMES:

        await query.edit_message_text(
            "❌ این فصل وجود ندارد.",
            reply_markup=banking_back_menu()
        )

        return

    try:

        result = banking_chapter_text(chapter)

        text = (
            result[0]
            if isinstance(result, tuple)
            else result
        )

    except Exception as error:

        print(
            f"❌ Banking chapter error: {error}"
        )

        await query.edit_message_text(
            "⚠️ خطا در بارگذاری درسنامه بانکداری.",
            reply_markup=banking_back_menu()
        )

        return

    total_chapters = len(BANKING_CHAPTER_NAMES)

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
                    if chapter < total_chapters
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
            reply_markup=banking_back_menu()
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await query.edit_message_text(
            "❌ برای این فصل هنوز سؤال آزمون ثبت نشده است.",
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

🎯 آزمون تخصصی و مفهومی

📝 تعداد سؤالات:
{len(questions)} سؤال

━━━━━━━━━━━━━━━━━━

📌 هر سؤال چهار گزینه دارد.
📌 فقط یک گزینه صحیح است.
📌 نتیجه در پایان نمایش داده می‌شود.

━━━━━━━━━━━━━━━━━━
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
            "⚠️ خطا در اطلاعات آزمون.",
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

{question.get("question", "")}

━━━━━━━━━━━━━━━━━━

👇 گزینه صحیح را انتخاب کنید:
"""

    keyboard = []

    for option_index, option in enumerate(
        question.get("options", [])
    ):

        keyboard.append(
            [
                InlineKeyboardButton(
                    str(option),
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
            "⚠️ خطا در پردازش پاسخ.",
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

    correct = question.get(
        "correct",
        0
    )

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

        options = question.get(
            "options",
            []
        )

        correct_option = (
            options[correct]
            if correct < len(options)
            else "نامشخص"
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

    name = BANKING_CHAPTER_NAMES.get(
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

🎯 مسیر یادگیری:

📖 مطالعه
+
📝 آزمون
+
🔍 تحلیل اشتباهات
+
🔄 مرور
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
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

async def international_trade_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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


async def international_trade_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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

    try:

        result = international_trade_chapter_text(
            chapter
        )

        text = (
            result[0]
            if isinstance(result, tuple)
            else result
        )

    except Exception as error:

        print(
            f"❌ Trade chapter error: {error}"
        )

        await query.edit_message_text(
            "⚠️ خطا در بارگذاری درسنامه تجارت بین‌الملل.",
            reply_markup=international_trade_back_menu()
        )

        return

    total_chapters = len(
        TRADE_CHAPTER_NAMES
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
                "⬅️ فصل قبل",
                callback_data=(
                    f"international_trade_chapter_{chapter - 1}"
                    if chapter > 1
                    else "international_trade"
                )
            ),

            InlineKeyboardButton(
                "فصل بعد ➡️",
                callback_data=(
                    f"international_trade_chapter_{chapter + 1}"
                    if chapter < total_chapters
                    else "international_trade"
                )
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
# TRADE EXAM INTRO
# =========================================================

async def trade_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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

    if not questions:

        await query.edit_message_text(
            "❌ برای این فصل هنوز سؤال آزمون ثبت نشده است.",
            reply_markup=international_trade_back_menu()
        )

        return

    name = TRADE_CHAPTER_NAMES.get(
        chapter,
        "تجارت بین‌الملل"
    )

    text = f"""
📝 آزمون پایان فصل {chapter}

🌍 {name}

━━━━━━━━━━━━━━━━━━

🎯 آزمون تخصصی و مفهومی

📝 تعداد سؤالات:
{len(questions)} سؤال

━━━━━━━━━━━━━━━━━━

📌 هر سؤال چهار گزینه دارد.
📌 فقط یک گزینه صحیح است.
📌 نتیجه در پایان نمایش داده می‌شود.

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
                "📖 بازگشت به درسنامه",
                callback_data=(
                    f"international_trade_chapter_{chapter}"
                )
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


# =========================================================
# TRADE EXAM QUESTION
# =========================================================

async def trade_exam_question_callback(
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
            "⚠️ خطا در اطلاعات آزمون.",
            reply_markup=international_trade_back_menu()
        )

        return

    questions = INTERNATIONAL_TRADE_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await query.edit_message_text(
            "❌ سوالی برای این فصل وجود ندارد.",
            reply_markup=international_trade_back_menu()
        )

        return

    if index >= len(questions):

        await show_trade_result(
            query,
            chapter,
            score
        )

        return

    question = questions[index]

    name = TRADE_CHAPTER_NAMES.get(
        chapter,
        "تجارت بین‌الملل"
    )

    text = f"""
📝 آزمون تجارت بین‌الملل

📘 فصل {chapter}
🌍 {name}

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

{question.get("question", "")}

━━━━━━━━━━━━━━━━━━

👇 گزینه صحیح را انتخاب کنید:
"""

    keyboard = []

    for option_index, option in enumerate(
        question.get("options", [])
    ):

        keyboard.append(
            [
                InlineKeyboardButton(
                    str(option),
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

    keyboard.append(
        [
            InlineKeyboardButton(
                "🌍 خروج از آزمون",
                callback_data="international_trade"
            )
        ]
    )

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# TRADE EXAM ANSWER
# =========================================================

async def trade_answer_callback(
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
            "⚠️ خطا در پردازش پاسخ.",
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

    correct = question.get(
        "correct",
        0
    )

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

        options = question.get(
            "options",
            []
        )

        correct_option = (
            options[correct]
            if correct < len(options)
            else "نامشخص"
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
                        f"trade_exam_"
                        f"{chapter}_"
                        f"{next_index}_"
                        f"{score}"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    "🌍 خروج از آزمون",
                    callback_data="international_trade"
                )
            ],

        ]

        await query.edit_message_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await show_trade_result(
            query,
            chapter,
            score
        )


# =========================================================
# TRADE RESULT
# =========================================================

async def show_trade_result(
    query,
    chapter,
    score
):

    questions = INTERNATIONAL_TRADE_QUESTIONS.get(
        chapter,
        []
    )

    total = len(questions)

    if total == 0:

        await query.edit_message_text(
            "❌ آزمونی برای این فصل وجود ندارد.",
            reply_markup=international_trade_back_menu()
        )

        return

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

    name = TRADE_CHAPTER_NAMES.get(
        chapter,
        "تجارت بین‌الملل"
    )

    text = f"""
🏁 آزمون فصل {chapter} به پایان رسید.

🌍 {name}

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی:

{evaluation}

━━━━━━━━━━━━━━━━━━

🎯 مسیر یادگیری:

📖 مطالعه
+
📝 آزمون
+
🔍 تحلیل اشتباهات
+
🔄 مرور
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
                callback_data=f"trade_exam_{chapter}_0_0"
            )
        ],

        [
            InlineKeyboardButton(
                "📖 مرور فصل",
                callback_data=(
                    f"international_trade_chapter_{chapter}"
                )
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

async def marketing_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        result = marketing_intro_text()

        if isinstance(result, tuple):

            text = result[0]
            keyboard = result[1]

        else:

            text = result
            keyboard = marketing_menu()

    except Exception as error:

        print(
            f"❌ Marketing intro error: {error}"
        )

        text = """
📈 بازاریابی و فروش

━━━━━━━━━━━━━━━━━━

مرکز آموزش تخصصی بازاریابی،
فروش و توسعه بازار.

🚧 محتوای این بخش در حال آماده‌سازی است.
"""

        keyboard = [

            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="home"
                )
            ]

        ]

        keyboard = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def marketing_generic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    # تلاش برای استفاده از callback اختصاصی ماژول
    handler = getattr(
        __import__("marketing"),
        "marketing_callback",
        None
    )

    if handler:

        try:

            return await handler(
                update,
                context
            )

        except Exception as error:

            print(
                f"❌ Marketing callback error: {error}"
            )

    # فصل بازاریابی
    if data.startswith("marketing_chapter_"):

        try:

            chapter = int(
                data.replace(
                    "marketing_chapter_",
                    ""
                )
            )

            result = marketing_chapter_text(
                chapter
            )

            text = (
                result[0]
                if isinstance(result, tuple)
                else result
            )

            keyboard = [

                [
                    InlineKeyboardButton(
                        f"📝 آزمون فصل {chapter}",
                        callback_data=(
                            f"marketing_exam_intro_{chapter}"
                        )
                    )
                ],

                [
                    InlineKeyboardButton(
                        "📈 بازاریابی",
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

            return

        except Exception as error:

            print(
                f"❌ Marketing chapter error: {error}"
            )

    # آزمون بازاریابی
    if data.startswith("marketing_exam_intro_"):

        try:

            chapter = int(
                data.replace(
                    "marketing_exam_intro_",
                    ""
                )
            )

            result = marketing_exam_intro_text(
                chapter
            )

            if isinstance(result, tuple):

                text = result[0]
                keyboard = result[1]

            else:

                text = result

                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🚀 شروع آزمون",
                                callback_data=(
                                    f"marketing_exam_"
                                    f"{chapter}_0_0"
                                )
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "📈 بازاریابی",
                                callback_data="marketing"
                            )
                        ]
                    ]
                )

            await query.edit_message_text(
                text,
                reply_markup=keyboard
            )

            return

        except Exception as error:

            print(
                f"❌ Marketing exam intro error: {error}"
            )

    await query.edit_message_text(
        """
📈 بازاریابی و فروش

━━━━━━━━━━━━━━━━━━

🚧 این بخش در حال آماده‌سازی است.
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📈 بازاریابی",
                        callback_data="marketing"
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
# ECONOMICS
# =========================================================

def economics_default_text():

    return """
💰 اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

مرکز آموزش مفاهیم اقتصادی،
بازار، تورم، پول، بانک و شاخص‌های اقتصادی.

🚧 محتوای این بخش در حال توسعه است.
"""


def economics_default_menu():

    return InlineKeyboardMarkup(
        [

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

        ]
    )


async def economics_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if ECONOMICS_AVAILABLE:

        handler = getattr(
            economics,
            "economics_callback",
            None
        )

        if handler:

            try:

                return await handler(
                    update,
                    context
                )

            except Exception as error:

                print(
                    f"❌ Economics callback error: {error}"
                )

        menu_function = getattr(
            economics,
            "economics_menu",
            None
        )

        intro_function = getattr(
            economics,
            "economics_intro_text",
            None
        )

        try:

            text = (
                intro_function()
                if intro_function
                else economics_default_text()
            )

            keyboard = (
                menu_function()
                if menu_function
                else economics_default_menu()
            )

            await query.edit_message_text(
                text,
                reply_markup=keyboard
            )

            return

        except Exception as error:

            print(
                f"❌ Economics menu error: {error}"
            )

    await query.edit_message_text(
        economics_default_text(),
        reply_markup=economics_default_menu()
    )


async def economics_generic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if ECONOMICS_AVAILABLE:

        handler = getattr(
            economics,
            "economics_callback",
            None
        )

        if handler:

            try:

                return await handler(
                    update,
                    context
                )

            except Exception as error:

                print(
                    f"❌ Economics section error: {error}"
                )

    data = query.data

    titles = {

        "economics_lessons":
            "📚 آموزش اقتصاد",

        "economics_concepts":
            "📊 مفاهیم اقتصادی",

        "economics_exam":
            "📝 آزمون اقتصاد",

    }

    text = f"""
{titles.get(data, "💰 اقتصاد و بازار")}

━━━━━━━━━━━━━━━━━━

🚧 این بخش در حال آماده‌سازی است.

🏛️ اندیشکده مدیریت و بازار
"""

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
# EMPLOYMENT EXAM
# =========================================================

async def employment_exam_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    handler = getattr(
        employment_exam,
        "employment_exam_callback",
        None
    )

    if handler:

        try:

            return await handler(
                update,
                context
            )

        except Exception as error:

            print(
                f"❌ Employment exam error: {error}"
            )

    menu_function = getattr(
        employment_exam,
        "employment_exam_menu",
        None
    )

    intro_function = getattr(
        employment_exam,
        "employment_exam_intro_text",
        None
    )

    if intro_function:

        try:

            text = intro_function()

        except Exception:

            text = employment_default_text()

    else:

        text = employment_default_text()

    if menu_function:

        try:

            keyboard = menu_function()

        except Exception:

            keyboard = employment_default_menu()

    else:

        keyboard = employment_default_menu()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


def employment_default_text():

    return """
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

آمادگی برای آزمون‌های استخدامی

🏦 بانک‌ها
🏢 دستگاه‌های اجرایی
📚 دروس عمومی
📖 دروس تخصصی
🧠 هوش و استعداد
💻 ICDL
🇬🇧 زبان انگلیسی

━━━━━━━━━━━━━━━━━━

🚧 بخش آزمون در حال توسعه است.
"""


def employment_default_menu():

    return InlineKeyboardMarkup(
        [

            [
                InlineKeyboardButton(
                    "📚 دروس عمومی",
                    callback_data="employment_general"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏦 دروس تخصصی بانکداری",
                    callback_data="employment_banking"
                )
            ],

            [
                InlineKeyboardButton(
                    "🧠 هوش و استعداد",
                    callback_data="employment_iq"
                )
            ],

            [
                InlineKeyboardButton(
                    "💻 ICDL",
                    callback_data="employment_icdl"
                )
            ],

            [
                InlineKeyboardButton(
                    "🇬🇧 زبان انگلیسی",
                    callback_data="employment_english"
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


async def employment_generic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    handler = getattr(
        employment_exam,
        "employment_exam_section_callback",
        None
    )

    if handler:

        try:

            return await handler(
                update,
                context
            )

        except Exception as error:

            print(
                f"❌ Employment section error: {error}"
            )

    text = """
📝 بخش آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🚧 محتوای این بخش در حال آماده‌سازی است.

🏛️ اندیشکده مدیریت و بازار
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "📝 آزمون استخدامی",
                callback_data="employment_exam"
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
# EDUCATION
# =========================================================

async def education_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
📚 آموزش تخصصی

━━━━━━━━━━━━━━━━━━

مرکز آموزش تخصصی اندیشکده

📚 مدیریت
🌍 تجارت بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار
🏦 بانکداری

━━━━━━━━━━━━━━━━━━

👇 یکی از حوزه‌ها را انتخاب کنید.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 مدیریت",
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
# MANAGEMENT
# =========================================================

async def management_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
📚 آموزش مدیریت

━━━━━━━━━━━━━━━━━━

🎯 مبانی مدیریت
👥 رفتار سازمانی
📊 مدیریت استراتژیک
💼 مدیریت منابع انسانی
💰 مدیریت مالی
📈 مدیریت بازاریابی
🏢 مدیریت عملیات

━━━━━━━━━━━━━━━━━━

🚧 محتوای تخصصی این بخش در حال توسعه است.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="education"
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
# FILES
# =========================================================

async def files_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
📂 فایل و منابع آموزشی

━━━━━━━━━━━━━━━━━━

📚 جزوات آموزشی
📝 نمونه سؤالات
📖 منابع آزمون
📄 فایل‌های تخصصی
🎓 منابع دانشگاهی

━━━━━━━━━━━━━━━━━━

🚧 فایل‌ها به‌تدریج در این بخش قرار می‌گیرند.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="education"
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
# SOCIAL
# =========================================================

async def social_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
📱 شبکه‌های اجتماعی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

📸 اینستاگرام
▶️ یوتیوب
📣 تلگرام
💬 واتساپ

━━━━━━━━━━━━━━━━━━

🎯 هدف ما:

آموزش کاربردی
+
توسعه مهارت
+
آمادگی آزمون
+
آشنایی با بازار و تجارت
"""

    keyboard = [

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
# RANDOM QUESTIONS
# =========================================================

async def random_questions_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🎲 سوالات تصادفی

━━━━━━━━━━━━━━━━━━

🎯 سیستم سوالات تصادفی اندیشکده

در این بخش می‌توان از حوزه‌های مختلف
سؤال دریافت کرد:

🏦 بانکداری
🌍 تجارت بین‌الملل
📈 بازاریابی
💰 اقتصاد
📚 مدیریت

━━━━━━━━━━━━━━━━━━

🚧 بانک سوالات تصادفی در حال توسعه است.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🏦 بانکداری",
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
                "📈 بازاریابی",
                callback_data="marketing"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 اقتصاد",
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
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    print(
        f"❌ Bot error: {context.error}"
    )


# =========================================================
# APPLICATION
# =========================================================

def build_application():

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # -----------------------------------------------------
    # COMMANDS
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # -----------------------------------------------------
    # MAIN MENU
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            home_callback,
            pattern=r"^home$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            education_callback,
            pattern=r"^education$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            management_callback,
            pattern=r"^management$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            files_callback,
            pattern=r"^files$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            social_callback,
            pattern=r"^social$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            random_questions_callback,
            pattern=r"^random_questions$"
        )
    )

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

    application.add_handler(
        CallbackQueryHandler(
            banking_chapter_callback,
            pattern=r"^banking_chapter_\d+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_intro_callback,
            pattern=r"^banking_exam_intro_\d+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            banking_answer_callback,
            pattern=r"^banking_answer_\d+_\d+_\d+_\d+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_question_callback,
            pattern=r"^banking_exam_\d+_\d+_\d+$"
        )
    )

    # -----------------------------------------------------
    # INTERNATIONAL TRADE
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            international_trade_callback,
            pattern=r"^international_trade$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            international_trade_chapter_callback,
            pattern=r"^international_trade_chapter_\d+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            trade_exam_intro_callback,
            pattern=r"^trade_exam_intro_\d+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            trade_answer_callback,
            pattern=r"^trade_answer_\d+_\d+_\d+_\d+$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            trade_exam_question_callback,
            pattern=r"^trade_exam_\d+_\d+_\d+$"
        )
    )

    # -----------------------------------------------------
    # MARKETING
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            marketing_callback,
            pattern=r"^marketing$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            marketing_generic_callback,
            pattern=(
                r"^marketing_"
            )
        )
    )

    # -----------------------------------------------------
    # ECONOMICS
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            economics_callback,
            pattern=r"^economics$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            economics_generic_callback,
            pattern=r"^economics_"
        )
    )

    # -----------------------------------------------------
    # EMPLOYMENT EXAM
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            employment_exam_callback,
            pattern=r"^employment_exam$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_generic_callback,
            pattern=r"^employment_"
        )
    )

    # -----------------------------------------------------
    # PSYCHOLOGY
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            psychology_socialwork_callback,
            pattern=r"^psychology_socialwork$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            psychology_generic_callback,
            pattern=(
                r"^(psychology_lessons|"
                r"psychology_concepts|"
                r"psychology_communication|"
                r"psychology_behavior|"
                r"socialwork|"
                r"psychology_exam|"
                r"socialwork_exam)$"
            )
        )
    )

    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    return application


# =========================================================
# MAIN
# =========================================================

def main():

    print(
        "🏛️ Andishkadeh Market Bot starting..."
    )

    print(
        "📚 Banking module loaded."
    )

    print(
        "🌍 International Trade module loaded."
    )

    print(
        "📈 Marketing module loaded."
    )

    print(
        "📝 Employment Exam module loaded."
    )

    print(
        "🧠 Psychology & Social Work module loaded."
    )

    if ECONOMICS_AVAILABLE:

        print(
            "💰 Economics module loaded."
        )

    else:

        print(
            "⚠️ Economics module not found. "
            "Fallback mode enabled."
        )

    run_http_server()

    application = build_application()

    print(
        "🤖 Telegram bot is running..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()
