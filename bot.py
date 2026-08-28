# =========================================================
# bot.py
# 🏛️ اندیشکده مدیریت و بازار
# نسخه اصلی - Render Free Web Service
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
# 🤝 SUPPORT
# =========================================================
from support import (
    support_text,
    support_menu,
)
# =========================================================
# 🏦 BANKING
# =========================================================
from banking import (
    banking_menu,
    banking_back_menu,
    banking_intro_text,
    banking_chapter_text,
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
)
# =========================================================
# 🌍 INTERNATIONAL TRADE
# =========================================================
from international_trade import (
    international_trade_intro_text,
    international_trade_menu,
    international_trade_back_menu,
    international_trade_chapter_text,
    international_trade_chapter_menu,
    CHAPTER_NAMES as TRADE_CHAPTER_NAMES,
    TRADE_CHAPTER_QUESTIONS,
    international_trade_exam_intro_text,
    international_trade_exam_menu,
    international_trade_result_text,
)
# =========================================================
# ⚙️ تنظیمات
# =========================================================
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(
    os.getenv("PORT", "10000")
)
# =========================================================
# 🔐 بررسی توکن
# =========================================================
if not TOKEN:
    raise RuntimeError(
        "❌ BOT_TOKEN در Environment Variables تنظیم نشده است."
    )
# =========================================================
# 🌐 HTTP SERVER برای Render
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
# 🚀 اجرای HTTP Server
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
# 🧵 اجرای HTTP در Thread جداگانه
# =========================================================
def run_http_server():
    thread = Thread(
        target=start_http_server,
        daemon=True
    )
    thread.start()
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
🏦 بانکداری تخصصی
🌍 تجارت بین‌الملل
📈 بازاریابی و فروش
💰 اقتصاد و بازار
📂 فایل و منابع آموزشی
📱 شبکه‌های اجتماعی
━━━━━━━━━━━━━━━━━━
🎯 سیستم آموزشی اندیشکده:
📖 آموزش مفهومی
+
💡 مثال کاربردی
+
📝 آزمون
+
📊 ارزیابی
+
🔄 مرور و تکرار
━━━━━━━━━━━━━━━━━━
👇 بخش موردنظر را انتخاب کنید.
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
# 🏠 HOME
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
# 🤝 SUPPORT
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
# 🏦 BANKING
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
# 📖 BANKING CHAPTER
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
        else:
            text = result
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
# 📝 BANKING EXAM INTRO
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
📌 قوانین:
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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )
# =========================================================
# 📝 BANKING EXAM QUESTION
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
        await show_banking_exam_result(
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
# 📝 BANKING ANSWER
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
        await show_banking_exam_result(
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
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )
    else:
        await show_banking_exam_result(
            query,
            chapter,
            score
        )
# =========================================================
# 🏁 BANKING RESULT
# =========================================================
async def show_banking_exam_result(
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
📚 پیشنهاد:
درسنامه فصل را مرور کنید و آزمون
را دوباره انجام دهید.
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
# 🌍 INTERNATIONAL TRADE
# =========================================================
async def international_trade_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        international_trade_intro_text(),
        reply_markup=international_trade_menu()
    )
# =========================================================
# 📖 TRADE CHAPTER
# =========================================================
async def trade_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    try:
        chapter = int(
            query.data.replace(
                "trade_chapter_",
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
    await query.edit_message_text(
        text,
        reply_markup=international_trade_chapter_menu(
            chapter
        )
    )
# =========================================================
# 📝 TRADE EXAM INTRO
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
    questions = TRADE_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )
    if not questions:
        await query.edit_message_text(
            "❌ برای این فصل سؤال آزمون ثبت نشده است.",
            reply_markup=international_trade_back_menu()
        )
        return
    await query.edit_message_text(
        international_trade_exam_intro_text(
            chapter
        ),
        reply_markup=international_trade_exam_menu(
            chapter
        )
    )
# =========================================================
# 📝 TRADE EXAM QUESTION
# =========================================================
async def trade_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    try:
        data = query.data.split("_")
        # trade_exam_1_0_0
        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])
    except (
        IndexError,
        ValueError
    ):
        await query.edit_message_text(
            "⚠️ خطا در اطلاعات آزمون تجارت بین‌الملل.",
            reply_markup=international_trade_back_menu()
        )
        return
    questions = TRADE_CHAPTER_QUESTIONS.get(
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
        await show_trade_exam_result(
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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )
# =========================================================
# 📝 TRADE ANSWER
# =========================================================
async def trade_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    try:
        data = query.data.split("_")
        # trade_answer_1_0_0_0
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
    questions = TRADE_CHAPTER_QUESTIONS.get(
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
        await show_trade_exam_result(
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
                    "📖 مشاهده درسنامه",
                    callback_data=(
                        f"trade_chapter_{chapter}"
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
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )
    else:
        await show_trade_exam_result(
            query,
            chapter,
            score
        )
# =========================================================
# 🏁 TRADE RESULT
# =========================================================
async def show_trade_exam_result(
    query,
    chapter,
    score
):
    questions = TRADE_CHAPTER_QUESTIONS.get(
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
    text = international_trade_result_text(
        chapter,
        score
    )
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
                    f"trade_chapter_{chapter}"
                )
            )
        ],
    ]
    if chapter < len(TRADE_CHAPTER_NAMES):
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 ورود به فصل {chapter + 1}",
                    callback_data=(
                        f"trade_chapter_{chapter + 1}"
                    )
                )
            ]
        )
    keyboard.extend(
        [
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
    )
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )
# =========================================================
# 🚧 بخش‌های هنوز ساخته نشده
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
                        "🏠 منوی اصلی",
                        callback_data="home"
                    )
                ]
            ]
        )
    )
# =========================================================
# ⚠️ UNKNOWN CALLBACK
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
# ❌ ERROR HANDLER
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
# 🤖 CREATE APPLICATION
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
    # 🌍 INTERNATIONAL TRADE
    # =====================================================
    application.add_handler(
        CallbackQueryHandler(
            international_trade_callback,
            pattern=r"^international_trade$"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            trade_chapter_callback,
            pattern=r"^trade_chapter_[0-9]+$"
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
    # 🚧 بخش‌های موقت
    # =====================================================
    application.add_handler(
        CallbackQueryHandler(
            temporary_section,
            pattern=(
                r"^(education|"
                r"employment_exam|"
                r"random_questions|"
                r"psychology_socialwork|"
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
# 🚀 MAIN
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
    # TELEGRAM
    # =====================================================
    application = create_application()
    print(
        "🤖 Telegram application starting..."
    )
    # =====================================================
    # POLLING
    # =====================================================
    application.run_polling(
        drop_pending_updates=True
    )
# =========================================================
# START
# =========================================================
if __name__ == "__main__":
    main()
