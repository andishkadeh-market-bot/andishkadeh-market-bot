# =========================================================
# bot.py
# 🏛️ اندیشکده مدیریت و بازار
# نسخه جامع
#
# اتصال:
# 🏦 بانکداری
# 🌍 تجارت بین‌الملل
# 📈 بازاریابی و فروش
# 💰 اقتصاد و بازار
# 📝 آزمون استخدامی حرفه‌ای
# 🧠 روانشناسی و مددکاری
# 🤝 حمایت از اندیشکده
#
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

import employment_exam

# =========================================================
# PSYCHOLOGY & SOCIAL WORK
# =========================================================

import psychology_socialwork

# =========================================================
# ECONOMICS QUESTIONS
# =========================================================

ECONOMICS_QUESTIONS = [

    {
        "question": "کدام گزینه تعریف مناسب‌تری از تورم است؟",
        "options": [
            "افزایش یک‌باره قیمت یک کالا",
            "افزایش مستمر و عمومی سطح قیمت‌ها",
            "کاهش سطح تولید",
            "افزایش درآمد خانوار"
        ],
        "correct": 1
    },

    {
        "question": "کدام گزینه بیشتر با سیاست پولی ارتباط دارد؟",
        "options": [
            "مخارج دولت",
            "مالیات",
            "نرخ بهره و نقدینگی",
            "بودجه عمرانی"
        ],
        "correct": 2
    },

    {
        "question": "تولید ناخالص داخلی چه چیزی را اندازه‌گیری می‌کند؟",
        "options": [
            "ارزش دارایی‌های خانوارها",
            "ارزش کالاها و خدمات نهایی تولیدشده در اقتصاد",
            "مقدار پول نقد مردم",
            "میزان صادرات یک کشور"
        ],
        "correct": 1
    },

    {
        "question": "در شرایط برابر، افزایش قیمت معمولاً چه اثری بر مقدار تقاضا دارد؟",
        "options": [
            "افزایش",
            "کاهش",
            "بدون تغییر قطعی",
            "دو برابر شدن"
        ],
        "correct": 1
    },

    {
        "question": "کدام مورد از ابزارهای سیاست مالی است؟",
        "options": [
            "مالیات",
            "عملیات بازار باز",
            "ذخایر بانکی",
            "نرخ سیاستی بانک مرکزی"
        ],
        "correct": 0
    },

    {
        "question": "نقدینگی معمولاً شامل چه اجزایی است؟",
        "options": [
            "فقط اسکناس",
            "فقط سکه",
            "پول و شبه‌پول",
            "فقط سپرده‌های بلندمدت"
        ],
        "correct": 2
    },

    {
        "question": "کدام گزینه می‌تواند به رشد اقتصادی کمک کند؟",
        "options": [
            "کاهش بهره‌وری",
            "کاهش سرمایه‌گذاری",
            "افزایش بهره‌وری و فناوری",
            "کاهش ظرفیت تولید"
        ],
        "correct": 2
    },

    {
        "question": "بازار از تعامل کدام دو عامل اصلی شکل می‌گیرد؟",
        "options": [
            "دولت و بانک",
            "عرضه و تقاضا",
            "صادرات و واردات",
            "تورم و بیکاری"
        ],
        "correct": 1
    },

    {
        "question": "سیاست مالی عمدتاً مربوط به کدام بخش است؟",
        "options": [
            "تصمیمات دولت درباره درآمدها و مخارج",
            "تنظیم حجم پول توسط بانک مرکزی",
            "تعیین قیمت سهام",
            "مدیریت شرکت‌های خصوصی"
        ],
        "correct": 0
    },

    {
        "question": "کدام مورد می‌تواند بر نرخ ارز اثر بگذارد؟",
        "options": [
            "نرخ بهره",
            "تورم",
            "عرضه و تقاضای ارز",
            "همه موارد"
        ],
        "correct": 3
    },

]

# =========================================================
# SETTINGS
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

PORT = int(
    os.getenv("PORT", "10000")
)

# =========================================================
# TOKEN CHECK
# =========================================================

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

        # آموزش
        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="education"
            )
        ],

        # آزمون و سوالات
        [
            InlineKeyboardButton(
                "📝 آزمون استخدامی",
                callback_data="employment_exam"
            ),
            InlineKeyboardButton(
                "🎲 سوالات تصادفی",
                callback_data="random_questions"
            )
        ],

        # روانشناسی و بانکداری
        [
            InlineKeyboardButton(
                "🧠 روانشناسی و مددکاری",
                callback_data="psychology_socialwork"
            ),
            InlineKeyboardButton(
                "🏦 بانکداری تخصصی",
                callback_data="banking"
            )
        ],

        # تجارت و بازاریابی
        [
            InlineKeyboardButton(
                "🌍 تجارت بین‌الملل",
                callback_data="international_trade"
            ),
            InlineKeyboardButton(
                "📈 بازاریابی و فروش",
                callback_data="marketing"
            )
        ],

        # اقتصاد و منابع
        [
            InlineKeyboardButton(
                "💰 اقتصاد و بازار",
                callback_data="economics"
            ),
            InlineKeyboardButton(
                "📂 فایل و منابع آموزشی",
                callback_data="files"
            )
        ],

        # شبکه‌های اجتماعی
        [
            InlineKeyboardButton(
                "📱 شبکه‌های اجتماعی",
                callback_data="social"
            )
        ],

        # حمایت
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
# PSYCHOLOGY & SOCIAL WORK
# =========================================================

async def psychology_socialwork_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        psychology_socialwork,
        "psychology_socialwork_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    intro_function = getattr(
        psychology_socialwork,
        "psychology_socialwork_intro_text",
        None
    )

    menu_function = getattr(
        psychology_socialwork,
        "psychology_socialwork_menu",
        None
    )

    if intro_function:

        try:

            text = intro_function()

        except Exception as error:

            print(
                f"❌ Psychology intro error: {error}"
            )

            text = """
🧠 روانشناسی و مددکاری

━━━━━━━━━━━━━━━━━━

مرکز آموزش مفاهیم روانشناسی،
مهارت‌های ارتباطی و مددکاری اجتماعی.

━━━━━━━━━━━━━━━━━━
"""

    else:

        text = """
🧠 روانشناسی و مددکاری

━━━━━━━━━━━━━━━━━━

مرکز آموزش:

🧠 مبانی روانشناسی
🤝 مددکاری اجتماعی
💬 مهارت‌های ارتباطی
👥 رفتار اجتماعی
🧩 شخصیت و رفتار
🎓 آمادگی آزمون

━━━━━━━━━━━━━━━━━━

👇 بخش موردنظر را انتخاب کنید.
"""

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


# =========================================================
# DEFAULT PSYCHOLOGY MENU
# =========================================================

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
# PSYCHOLOGY GENERIC CALLBACK
# =========================================================

async def psychology_generic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        psychology_socialwork,
        "psychology_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    data = query.data

    text_function_names = {

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

    function_name = text_function_names.get(
        data
    )

    function = getattr(
        psychology_socialwork,
        function_name,
        None
    ) if function_name else None

    if function:

        try:

            text = function()

        except TypeError:

            text = function(
                data
            )

        except Exception as error:

            print(
                f"❌ Psychology section error: {error}"
            )

            text = "⚠️ خطا در بارگذاری این بخش."

    else:

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

        text = f"""
{titles.get(data, "🧠 روانشناسی و مددکاری")}

━━━━━━━━━━━━━━━━━━

🚧 محتوای تخصصی این بخش در حال بارگذاری است.

🏛️ اندیشکده مدیریت و بازار
"""

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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# BANKING MAIN
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

        result = banking_chapter_text(
            chapter
        )

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

    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون فصل {chapter}",
                callback_data=(
                    f"banking_exam_intro_{chapter}"
                )
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

📌 قوانین آزمون

• هر سؤال چهار گزینه دارد.
• فقط یک گزینه صحیح است.
• پاسخ صحیح یک امتیاز دارد.
• نتیجه در پایان نمایش داده می‌شود.

━━━━━━━━━━━━━━━━━━

👇 برای شروع آزمون:
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

    if index >= len(questions):

        await show_banking_result(
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
# BANKING RESULT
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

مطالعه
+
آزمون
+
تحلیل اشتباهات
+
مرور
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

        text = international_trade_chapter_text(
            chapter
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

    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون فصل {chapter}",
                callback_data=(
                    f"trade_exam_intro_{chapter}"
                )
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
                    if chapter < len(TRADE_CHAPTER_NAMES)
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

    name = TRADE_CHAPTER_NAMES.get(
        chapter,
        "تجارت بین‌الملل"
    )

    text = f"""
📝 آزمون فصل {chapter}

🌍 {name}

━━━━━━━━━━━━━━━━━━

🎯 آزمون تخصصی تجارت بین‌الملل

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
                callback_data=(
                    f"trade_exam_{chapter}_0_0"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "📖 مطالعه فصل",
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

    except (
        IndexError,
        ValueError
    ):

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
            "❌ سوالی برای این فصل ثبت نشده است.",
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

    except (
        IndexError,
        ValueError
    ):

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
                callback_data=(
                    f"trade_exam_{chapter}_0_0"
                )
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

    result = marketing_intro_text()

    await query.edit_message_text(
        result,
        reply_markup=marketing_menu()
    )


async def marketing_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
                callback_data=(
                    f"marketing_exam_intro_{chapter}"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ فصل قبل",
                callback_data=(
                    f"marketing_chapter_{chapter - 1}"
                    if chapter > 1
                    else "marketing"
                )
            ),

            InlineKeyboardButton(
                "فصل بعد ➡️",
                callback_data=(
                    f"marketing_chapter_{chapter + 1}"
                    if chapter < len(MARKETING_CHAPTER_NAMES)
                    else "marketing"
                )
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


async def marketing_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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

    text = marketing_exam_intro_text(
        chapter
    )

    await query.edit_message_text(
        text,
        reply_markup=marketing_exam_menu(chapter)
    )


async def marketing_exam_question_callback(
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

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در اطلاعات آزمون.",
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


async def marketing_answer_callback(
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

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در پردازش پاسخ.",
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
                "📈 خروج از آزمون",
                callback_data="marketing"
            )
        ]

    ]

    await query.edit_message_text(
        result["result_text"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# ECONOMICS MENU
# =========================================================

def economics_menu():

    keyboard = [

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

    ]

    return InlineKeyboardMarkup(keyboard)


def economics_text():

    return """
💰 اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

مرکز آموزش مفاهیم اقتصاد، بازارهای مالی
و تحلیل متغیرهای اقتصادی

━━━━━━━━━━━━━━━━━━

📚 موضوعات:

• مبانی علم اقتصاد
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
• تولید ناخالص داخلی
• رکود و رونق اقتصادی
• بازارهای مالی

━━━━━━━━━━━━━━━━━━

🎯 هدف:

درک مفاهیم اقتصادی
+
تحلیل بازار
+
آمادگی آزمون
+
کاربرد در مدیریت و کسب‌وکار

👇 بخش موردنظر را انتخاب کنید.
"""


def economics_lessons_text():

    return """
📚 آموزش اقتصاد

━━━━━━━━━━━━━━━━━━

1️⃣ اقتصاد چیست؟

اقتصاد علمی است که بررسی می‌کند منابع محدود
چگونه برای تأمین نیازها و خواسته‌های نامحدود
انسان‌ها تخصیص پیدا می‌کنند.

━━━━━━━━━━━━━━━━━━

2️⃣ عرضه و تقاضا

🔹 عرضه:
مقدار کالا یا خدمتی که تولیدکنندگان حاضرند
در قیمت مشخص به بازار عرضه کنند.

🔹 تقاضا:
مقدار کالا یا خدمتی که مصرف‌کنندگان حاضرند
در قیمت مشخص خریداری کنند.

━━━━━━━━━━━━━━━━━━

3️⃣ قانون تقاضا

در شرایط برابر، با افزایش قیمت یک کالا،
مقدار تقاضا برای آن کاهش پیدا می‌کند.

━━━━━━━━━━━━━━━━━━

4️⃣ قانون عرضه

در شرایط برابر، افزایش قیمت معمولاً باعث
افزایش تمایل تولیدکنندگان به عرضه می‌شود.

━━━━━━━━━━━━━━━━━━

5️⃣ تعادل بازار

نقطه‌ای که در آن مقدار عرضه با مقدار تقاضا
برابر می‌شود، تعادل بازار نام دارد.
"""


def economics_concepts_text():

    return """
📊 مفاهیم مهم اقتصادی

━━━━━━━━━━━━━━━━━━

💰 تورم

افزایش مستمر و عمومی سطح قیمت کالاها و خدمات
در طول زمان.

━━━━━━━━━━━━━━━━━━

📈 رشد اقتصادی

افزایش ظرفیت تولید کالاها و خدمات در اقتصاد.

━━━━━━━━━━━━━━━━━━

👷 بیکاری

وضعیتی که فرد آماده و مایل به کار است اما
شغل مناسب پیدا نکرده است.

━━━━━━━━━━━━━━━━━━

🏭 تولید ناخالص داخلی

ارزش کالاها و خدمات نهایی تولیدشده در داخل
مرزهای یک کشور طی یک دوره مشخص.

━━━━━━━━━━━━━━━━━━

💧 نقدینگی

مجموع پول و شبه‌پول موجود در اقتصاد است.

━━━━━━━━━━━━━━━━━━

💵 نرخ بهره

هزینه استفاده از پول در طول زمان است.
"""


def economics_market_text():

    return """
💹 اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

بازار محلی برای تعامل عرضه‌کنندگان و
تقاضاکنندگان است.

━━━━━━━━━━━━━━━━━━

📈 بازار صعودی

روند عمومی قیمت‌ها و ارزش دارایی‌ها رو به افزایش.

📉 بازار نزولی

روند عمومی قیمت‌ها و ارزش دارایی‌ها رو به کاهش.

━━━━━━━━━━━━━━━━━━

🔹 عوامل مؤثر:

• تورم
• نرخ بهره
• نرخ ارز
• نقدینگی
• سیاست‌های دولت
• سیاست بانک مرکزی
• رشد اقتصادی
• انتظارات فعالان اقتصادی
• عرضه و تقاضا
• تحولات سیاسی و بین‌المللی
"""


def economics_monetary_text():

    return """
🏦 سیاست پولی

━━━━━━━━━━━━━━━━━━

سیاست پولی مجموعه اقداماتی است که بانک مرکزی
برای تأثیرگذاری بر حجم پول، اعتبار و شرایط
مالی اقتصاد انجام می‌دهد.

━━━━━━━━━━━━━━━━━━

🎯 اهداف:

• کنترل تورم
• ثبات قیمت‌ها
• ثبات مالی
• مدیریت نقدینگی
• مدیریت شرایط اعتباری

━━━━━━━━━━━━━━━━━━

🔹 ابزارها:

• نرخ‌های سیاستی
• عملیات بازار باز
• مدیریت ذخایر بانکی
• ابزارهای اعتباری
"""


def economics_fiscal_text():

    return """
🏛️ سیاست مالی

━━━━━━━━━━━━━━━━━━

سیاست مالی به تصمیمات دولت درباره درآمدها
و هزینه‌های عمومی مربوط می‌شود.

━━━━━━━━━━━━━━━━━━

💰 درآمدهای دولت:

• مالیات
• درآمد منابع
• عوارض
• سایر درآمدها

━━━━━━━━━━━━━━━━━━

💸 مخارج دولت:

• حقوق
• پروژه‌های عمرانی
• خدمات عمومی
• حمایت‌های اجتماعی

━━━━━━━━━━━━━━━━━━

📈 سیاست مالی انبساطی:

افزایش مخارج دولت یا کاهش مالیات‌ها.

📉 سیاست مالی انقباضی:

کاهش مخارج یا افزایش مالیات‌ها.
"""


def economics_inflation_growth_text():

    return """
📈 تورم و رشد اقتصادی

━━━━━━━━━━━━━━━━━━

🔥 تورم

افزایش مستمر و عمومی سطح قیمت‌ها.

━━━━━━━━━━━━━━━━━━

📊 انواع مهم:

• تورم ناشی از افزایش تقاضا
• تورم ناشی از افزایش هزینه
• تورم ساختاری

━━━━━━━━━━━━━━━━━━

📈 رشد اقتصادی

افزایش توان تولید کالاها و خدمات در اقتصاد.

━━━━━━━━━━━━━━━━━━

عوامل رشد:

• سرمایه‌گذاری
• نیروی کار
• بهره‌وری
• فناوری
• زیرساخت
• کیفیت نهادها
• ثبات اقتصادی
"""


def economics_currency_interest_text():

    return """
💵 ارز و نرخ بهره

━━━━━━━━━━━━━━━━━━

💱 نرخ ارز

قیمت یک واحد پول خارجی بر اساس پول داخلی
یا برعکس است.

━━━━━━━━━━━━━━━━━━

عوامل مؤثر:

• تورم
• نرخ بهره
• عرضه و تقاضای ارز
• صادرات و واردات
• انتظارات اقتصادی
• سیاست‌های پولی
• شرایط سیاسی و بین‌المللی

━━━━━━━━━━━━━━━━━━

📌 رابطه نرخ بهره و ارز همیشه ساده و قطعی نیست.
"""


async def economics_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        economics_text(),
        reply_markup=economics_menu()
    )


async def economics_subsection_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    section = query.data

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
        section,
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
        ]

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def economics_exam_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        """
📝 آزمون اقتصاد و بازار

━━━━━━━━━━━━━━━━━━

🎯 تعداد سؤالات:
10 سؤال

📌 سطح:
عمومی + مفهومی

📌 هر سؤال چهار گزینه

━━━━━━━━━━━━━━━━━━

👇 برای شروع:
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🚀 شروع آزمون",
                        callback_data="economics_exam_0_0"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💰 اقتصاد و بازار",
                        callback_data="economics"
                    )
                ]
            ]
        )
    )


async def economics_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
            "⚠️ خطا در اطلاعات آزمون اقتصاد.",
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
                        f"economics_answer_"
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
                "💰 خروج از آزمون",
                callback_data="economics"
            )
        ]
    )

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def economics_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
            "⚠️ خطا در پردازش پاسخ اقتصاد.",
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

    correct = question["correct"]

    if selected == correct:

        score += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {score}
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
                    "💰 خروج از آزمون",
                    callback_data="economics"
                )
            ]

        ]

        await query.edit_message_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await show_economics_result(
            query,
            score
        )


async def show_economics_result(
    query,
    score
):

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
        evaluation = "📚 نیازمند مطالعه بیشتر"

    text = f"""
🏁 آزمون اقتصاد و بازار به پایان رسید.

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی:

{evaluation}

━━━━━━━━━━━━━━━━━━

📖 مطالعه
+
📝 آزمون
+
🔍 بررسی اشتباهات
+
🔄 مرور
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
                "💰 اقتصاد و بازار",
                callback_data="economics"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ]

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

    handler = getattr(
        employment_exam,
        "employment_exam_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

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

    if menu_function:

        keyboard = menu_function()

    else:

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏦 بانک رفاه",
                        callback_data="employment_category_refah"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏦 بانک شهر",
                        callback_data="employment_category_shahr"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏦 بانک مهر",
                        callback_data="employment_category_mehr"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏛️ بانک‌های دولتی",
                        callback_data="employment_category_government"
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

    if intro_function:

        try:

            text = intro_function()

        except TypeError:

            text = "📝 آزمون استخدامی"

    else:

        text = """
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🎯 بانک سؤال حرفه‌ای اندیشکده

🏦 بانک رفاه
🏦 بانک شهر
🏦 بانک مهر
🏛️ بانک‌های دولتی

━━━━━━━━━━━━━━━━━━

📊 سطوح:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

🎯 آزمون شبیه‌سازی‌شده واقعی
"""

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def employment_exam_category_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        employment_exam,
        "employment_exam_category_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    category = query.data.replace(
        "employment_category_",
        ""
    )

    text_function = getattr(
        employment_exam,
        "employment_category_text",
        None
    )

    menu_function = getattr(
        employment_exam,
        "employment_category_menu",
        None
    )

    if text_function:

        try:

            text = text_function(
                category
            )

        except Exception:

            text = f"🏦 دسته آزمون: {category}"

    else:

        names = {
            "refah": "بانک رفاه",
            "shahr": "بانک شهر",
            "mehr": "بانک مهر",
            "government": "بانک‌های دولتی"
        }

        text = f"""
🏦 {names.get(category, "آزمون استخدامی")}

━━━━━━━━━━━━━━━━━━

سطح آزمون را انتخاب کنید:
"""

    if menu_function:

        try:

            keyboard = menu_function(
                category
            )

        except Exception:

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🟢 آسان",
                            callback_data=f"employment_difficulty_easy_{category}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🟡 متوسط",
                            callback_data=f"employment_difficulty_medium_{category}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔴 سخت",
                            callback_data=f"employment_difficulty_hard_{category}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📝 شبیه‌سازی واقعی",
                            callback_data=f"employment_simulation_{category}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📝 آزمون استخدامی",
                            callback_data="employment_exam"
                        )
                    ]
                ]
            )

    else:

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢 آسان",
                        callback_data=f"employment_difficulty_easy_{category}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🟡 متوسط",
                        callback_data=f"employment_difficulty_medium_{category}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔴 سخت",
                        callback_data=f"employment_difficulty_hard_{category}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 شبیه‌سازی واقعی",
                        callback_data=f"employment_simulation_{category}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 آزمون استخدامی",
                        callback_data="employment_exam"
                    )
                ]
            ]
        )

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def employment_difficulty_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        employment_exam,
        "employment_difficulty_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "🚧 این مرحله توسط نسخه بانک سؤال استخدامی مدیریت می‌شود.",
        reply_markup=InlineKeyboardMarkup(
            [
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
                ]
            ]
        )
    )


async def employment_simulation_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        employment_exam,
        "employment_simulation_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        """
🎯 آزمون شبیه‌سازی‌شده استخدامی

━━━━━━━━━━━━━━━━━━

📚 ترکیبی از موضوعات آزمون استخدامی

🏦 بانکداری
📊 اقتصاد
📈 مدیریت
💼 بازاریابی
🧠 هوش
💻 ICDL
🇬🇧 زبان انگلیسی

━━━━━━━━━━━━━━━━━━

🚧 در حال اتصال بانک سؤال حرفه‌ای
""",
        reply_markup=InlineKeyboardMarkup(
            [
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
                ]
            ]
        )
    )


async def employment_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        employment_exam,
        "employment_answer_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "⚠️ مدیریت پاسخ در employment_exam.py انجام می‌شود.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📝 آزمون استخدامی",
                        callback_data="employment_exam"
                    )
                ]
            ]
        )
    )


async def employment_next_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    handler = getattr(
        employment_exam,
        "employment_next_callback",
        None
    )

    if handler:

        return await handler(
            update,
            context
        )

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "⚠️ ادامه آزمون توسط employment_exam.py مدیریت می‌شود.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📝 آزمون استخدامی",
                        callback_data="employment_exam"
                    )
                ]
            ]
        )
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

محتوای تخصصی این قسمت در حال آماده‌سازی است.

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
# UNKNOWN CALLBACK
# =========================================================

async def unknown_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query:

        try:

            await query.answer(
                "این گزینه در حال حاضر فعال نیست."
            )

        except Exception as error:

            print(
                f"Callback answer error: {error}"
            )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update,
    context
):

    print(
        "❌ Telegram error:"
    )

    print(
        context.error
    )


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
    # PSYCHOLOGY & SOCIAL WORK
    # =====================================================

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
            economics_exam_start_callback,
            pattern=r"^economics_exam$"
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
            employment_exam_category_callback,
            pattern=r"^employment_category_(refah|shahr|mehr|government)$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_difficulty_callback,
            pattern=(
                r"^employment_difficulty_"
                r"(easy|medium|hard)"
                r"_[a-zA-Z0-9_]+$"
            )
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_simulation_callback,
            pattern=r"^employment_simulation_.*$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_answer_callback,
            pattern=r"^employment_answer_.*$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            employment_next_callback,
            pattern=r"^employment_next_.*$"
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
                r"random_questions|"
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
    # ERROR
    # =====================================================

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
        "📝 Employment Exam Module: LOADED"
    )

    print(
        "🧠 Psychology & Social Work Module: LOADED"
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
