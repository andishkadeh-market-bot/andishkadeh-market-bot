# =========================================================
# bot.py
# 🏛️ اندیشکده مدیریت و بازار
# نسخه سازگار با Render Free Web Service
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

# =========================================================
# 🧠 روانشناسی و مددکاری
# =========================================================

from psychology import (
    psychology_menu,
    psychology_back_menu,
    psychology_intro_text,
    psychology_chapter_text,
    psychology_topic_text,
    psychology_special_points_text,
    psychology_exam_points_text,
    psychology_example_text,
    psychology_exam_intro_text,
    psychology_question_text,
    psychology_exam_result_text,
    check_answer,
    CHAPTER_NAMES as PSYCHOLOGY_CHAPTER_NAMES,
)


# =========================================================
# تنظیمات
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

PORT = int(
    os.getenv("PORT", "10000")
)


# =========================================================
# بررسی توکن
# =========================================================

if not TOKEN:

    raise RuntimeError(
        "❌ BOT_TOKEN در Environment Variables تنظیم نشده است."
    )


# =========================================================
# HTTP SERVER برای Render
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


    def log_message(
        self,
        format,
        *args
    ):

        return


# =========================================================
# اجرای HTTP Server
# =========================================================

def start_http_server():

    server = HTTPServer(
        ("0.0.0.0", PORT),
        HealthHandler
    )

    print(
        f"🌐 HTTP server running on 0.0.0.0:{PORT}"
    )

    server.serve_forever()


# =========================================================
# اجرای HTTP در Thread جداگانه
# =========================================================

def run_http_server():

    thread = Thread(
        target=start_http_server,
        daemon=True
    )

    thread.start()


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
# 🏠 منوی اصلی
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
# 🏦 بانکداری
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

        result = banking_chapter_text(
            chapter
        )

        if isinstance(result, tuple):

            text = result[0]
            chapter_keyboard = result[1]

        else:

            text = result
            chapter_keyboard = None


    except Exception as error:

        print(
            f"❌ Banking chapter error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری درسنامه بانکداری.

لطفاً دوباره تلاش کنید.
""",
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
                    if chapter < len(CHAPTER_NAMES)
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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# 📝 معرفی آزمون فصل بانکداری
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
• پاسخ صحیح امتیاز دارد.
• امتیاز در طول آزمون محاسبه می‌شود.
• نتیجه در پایان نمایش داده می‌شود.

━━━━━━━━━━━━━━━━━━

💡 پیشنهاد:

ابتدا درسنامه را مطالعه کنید،
سپس آزمون را انجام دهید.

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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# 📝 سؤال آزمون بانکداری
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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# 📝 پاسخ بانکداری
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

به سؤال بعدی بروید.
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
# 🏁 نتیجه آزمون بانکداری
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

🎯 ارزیابی:
{evaluation}

━━━━━━━━━━━━━━━━━━

💡 {message}

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

    ]


    if chapter < len(CHAPTER_NAMES):

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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# 🧠 روانشناسی و مددکاری
# =========================================================

async def psychology_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        result = psychology_intro_text()

        if isinstance(result, tuple):

            text = result[0]
            keyboard = result[1]

        else:

            text = result
            keyboard = psychology_menu()

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except Exception as error:

        print(
            f"❌ Psychology intro error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری بخش روانشناسی و مددکاری.

لطفاً دوباره تلاش کنید.
""",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# 📘 فصل روانشناسی
# =========================================================

async def psychology_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "psychology_chapter_",
                ""
            )
        )

        if chapter not in PSYCHOLOGY_CHAPTER_NAMES:

            raise ValueError(
                "Invalid psychology chapter"
            )

        result = psychology_chapter_text(
            chapter
        )

        if isinstance(result, tuple):

            text = result[0]
            keyboard = result[1]

        else:

            text = result
            keyboard = psychology_back_menu()

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except Exception as error:

        print(
            f"❌ Psychology chapter error: {error}"
        )

        await query.edit_message_text(
            "❌ فصل موردنظر پیدا نشد.",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# 📖 زیرموضوع روانشناسی
# =========================================================

async def psychology_topic_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        # psychology_topic_1_0

        chapter = int(data[2])
        topic_index = int(data[3])

        result = psychology_topic_text(
            chapter,
            topic_index
        )

        if isinstance(result, tuple):

            text = result[0]
            keyboard = result[1]

        else:

            text = result
            keyboard = psychology_back_menu()

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except (
        IndexError,
        ValueError,
        Exception
    ) as error:

        print(
            f"❌ Psychology topic error: {error}"
        )

        await query.edit_message_text(
            "❌ زیرموضوع موردنظر پیدا نشد.",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# 🎯 نکات تخصصی روانشناسی
# =========================================================

async def psychology_special_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "psychology_special_",
                ""
            )
        )

        result = psychology_special_points_text(
            chapter
        )

        await query.edit_message_text(
            result[0],
            reply_markup=result[1]
        )

    except Exception as error:

        print(
            f"❌ Psychology special error: {error}"
        )

        await query.edit_message_text(
            "❌ خطا در بارگذاری نکات تخصصی.",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# 📝 نکات آزمونی روانشناسی
# =========================================================

async def psychology_exam_points_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "psychology_exam_points_",
                ""
            )
        )

        result = psychology_exam_points_text(
            chapter
        )

        await query.edit_message_text(
            result[0],
            reply_markup=result[1]
        )

    except Exception as error:

        print(
            f"❌ Psychology exam points error: {error}"
        )

        await query.edit_message_text(
            "❌ خطا در بارگذاری نکات آزمونی.",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# 💼 مثال کاربردی روانشناسی
# =========================================================

async def psychology_example_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "psychology_example_",
                ""
            )
        )

        result = psychology_example_text(
            chapter
        )

        await query.edit_message_text(
            result[0],
            reply_markup=result[1]
        )

    except Exception as error:

        print(
            f"❌ Psychology example error: {error}"
        )

        await query.edit_message_text(
            "❌ خطا در بارگذاری مثال کاربردی.",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# 📝 معرفی آزمون روانشناسی
# =========================================================

async def psychology_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        chapter = int(
            query.data.replace(
                "psychology_exam_intro_",
                ""
            )
        )

        result = psychology_exam_intro_text(
            chapter
        )

        await query.edit_message_text(
            result[0],
            reply_markup=result[1]
        )

    except Exception as error:

        print(
            f"❌ Psychology exam intro error: {error}"
        )

        await query.edit_message_text(
            "❌ خطا در آماده‌سازی آزمون.",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# ❓ سؤال آزمون روانشناسی
# =========================================================

async def psychology_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        # psychology_exam_1_0_0

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

        result = psychology_question_text(
            chapter,
            index,
            score
        )

        if isinstance(result, tuple):

            text = result[0]
            keyboard = result[1]

        else:

            text = result
            keyboard = psychology_back_menu()

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

    except (
        IndexError,
        ValueError,
        Exception
    ) as error:

        print(
            f"❌ Psychology question error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در اطلاعات آزمون.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=psychology_back_menu()
        )


# =========================================================
# ✅ پاسخ آزمون روانشناسی
# =========================================================

async def psychology_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        # psychology_answer_1_0_0_0

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

        result = check_answer(
            chapter,
            index,
            selected,
            score
        )

        if not result["valid"]:

            await query.edit_message_text(
                """
⚠️ سؤال موردنظر پیدا نشد.

لطفاً آزمون را دوباره شروع کنید.
""",
                reply_markup=psychology_back_menu()
            )

            return


        new_score = result["score"]


        if result["correct"]:

            result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {new_score}

━━━━━━━━━━━━━━━━━━

آفرین 👏

{result["explanation"]}
"""

        else:

            result_text = f"""
❌ پاسخ صحیح نیست.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{result["correct_option"]}

━━━━━━━━━━━━━━━━━━

⭐ امتیاز فعلی: {new_score}

💡 توضیح:

{result["explanation"]}
"""


        from psychology import (
            PSYCHOLOGY_QUESTIONS
        )

        questions = PSYCHOLOGY_QUESTIONS.get(
            chapter,
            []
        )

        next_index = index + 1


        if next_index < len(questions):

            keyboard = [

                [
                    InlineKeyboardButton(
                        "➡️ سؤال بعدی",
                        callback_data=(
                            f"psychology_exam_"
                            f"{chapter}_"
                            f"{next_index}_"
                            f"{new_score}"
                        )
                    )
                ],

                [
                    InlineKeyboardButton(
                        "📖 مشاهده درسنامه",
                        callback_data=(
                            f"psychology_chapter_{chapter}"
                        )
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🧠 خروج از آزمون",
                        callback_data=(
                            "psychology_socialwork"
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

            final_result = psychology_exam_result_text(
                chapter,
                new_score
            )

            await query.edit_message_text(
                final_result[0],
                reply_markup=final_result[1]
            )

    except (
        IndexError,
        ValueError,
        Exception
    ) as error:

        print(
            f"❌ Psychology answer error: {error}"
        )

        await query.edit_message_text(
            """
⚠️ خطا در پردازش پاسخ.

لطفاً آزمون را دوباره شروع کنید.
""",
            reply_markup=psychology_back_menu()
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
# ⚠️ Callback ناشناخته
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
# ساخت Application
# =========================================================

def create_application():

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
    # 🧠 PSYCHOLOGY
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_callback,
            pattern=r"^psychology_socialwork$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY CHAPTER
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_chapter_callback,
            pattern=r"^psychology_chapter_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY TOPIC
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_topic_callback,
            pattern=r"^psychology_topic_[0-9]+_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY SPECIAL POINTS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_special_callback,
            pattern=r"^psychology_special_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY EXAM POINTS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_exam_points_callback,
            pattern=r"^psychology_exam_points_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY EXAMPLE
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_example_callback,
            pattern=r"^psychology_example_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY EXAM INTRO
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_exam_intro_callback,
            pattern=r"^psychology_exam_intro_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY EXAM QUESTION
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_exam_question_callback,
            pattern=r"^psychology_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )


    # =====================================================
    # 🧠 PSYCHOLOGY ANSWER
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_answer_callback,
            pattern=r"^psychology_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
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
    # ERROR HANDLER
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
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )


    # =====================================================
    # HTTP SERVER
    # =====================================================

    run_http_server()


    # =====================================================
    # Telegram Application
    # =====================================================

    application = create_application()


    print(
        "🤖 Telegram application starting..."
    )


    # =====================================================
    # Polling
    # =====================================================

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()
