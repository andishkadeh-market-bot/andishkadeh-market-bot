import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest, TelegramError
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
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
    banking_full_exam_text,
)


# =========================================================
# تنظیمات Logging
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# TOKEN
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set in Render Environment Variables."
    )


# =========================================================
# تنظیمات کلی
# =========================================================

TOTAL_BANKING_CHAPTERS = 12


# =========================================================
# Callback امن
# =========================================================

async def safe_answer(query, text=None):
    """
    پاسخ امن به CallbackQuery.

    اگر Callback منقضی شده باشد،
    باعث Crash شدن ربات نمی‌شود.
    """

    if not query:
        return

    try:

        if text:
            await query.answer(text)
        else:
            await query.answer()

    except BadRequest as error:

        error_text = str(error).lower()

        if (
            "query is too old" in error_text
            or "query id is invalid" in error_text
            or "response timeout expired" in error_text
        ):

            logger.warning(
                "Expired callback query ignored: %s",
                error
            )

        else:

            logger.error(
                "Telegram BadRequest in callback answer: %s",
                error
            )

    except TelegramError as error:

        logger.error(
            "Telegram error in callback answer: %s",
            error
        )

    except Exception as error:

        logger.exception(
            "Unexpected callback answer error: %s",
            error
        )


# =========================================================
# Edit Message امن
# =========================================================

async def safe_edit_message(
    query,
    text,
    reply_markup=None
):
    """
    ویرایش امن پیام.

    خطاهای رایج مثل:
    Message is not modified
    Query is too old
    را مدیریت می‌کند.
    """

    if not query:
        return False

    try:

        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )

        return True

    except BadRequest as error:

        error_text = str(error).lower()

        if "message is not modified" in error_text:

            logger.info(
                "Message was already identical."
            )

            return True

        if (
            "query is too old" in error_text
            or "query id is invalid" in error_text
            or "response timeout expired" in error_text
        ):

            logger.warning(
                "Expired callback while editing message: %s",
                error
            )

            return False

        if "message to edit not found" in error_text:

            logger.warning(
                "Message to edit was not found."
            )

            return False

        logger.error(
            "BadRequest while editing message: %s",
            error
        )

        return False

    except TelegramError as error:

        logger.error(
            "Telegram error while editing message: %s",
            error
        )

        return False

    except Exception as error:

        logger.exception(
            "Unexpected edit error: %s",
            error
        )

        return False


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
📂 فایل و منابع آموزشی

━━━━━━━━━━━━━━━━━━

🎯 سیستم آموزشی اندیشکده:

📖 آموزش مفهومی
⬇️
🧠 یادگیری تخصصی
⬇️
📝 آزمون
⬇️
📊 ارزیابی
⬇️
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

    if not update.message:
        return

    try:

        await update.message.reply_text(
            welcome_text(),
            reply_markup=main_menu()
        )

    except TelegramError as error:

        logger.error(
            "Start command error: %s",
            error
        )


# =========================================================
# 🏠 خانه
# =========================================================

async def home_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    await safe_edit_message(
        query,
        welcome_text(),
        main_menu()
    )


# =========================================================
# 🤝 حمایت
# =========================================================

async def support_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        text = support_text()
        keyboard = support_menu()

    except Exception as error:

        logger.exception(
            "Support section error: %s",
            error
        )

        text = """
⚠️ خطا در بارگذاری بخش حمایت.

لطفاً دوباره تلاش کنید.
"""

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏠 منوی اصلی",
                        callback_data="home"
                    )
                ]
            ]
        )

    await safe_edit_message(
        query,
        text,
        keyboard
    )


# =========================================================
# 🏦 منوی بانکداری
# =========================================================

async def banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        text, keyboard = banking_intro_text()

    except Exception as error:

        logger.exception(
            "Banking intro error: %s",
            error
        )

        text = """
⚠️ خطا در بارگذاری بخش بانکداری.

لطفاً دوباره تلاش کنید.
"""

        keyboard = banking_back_menu()

    await safe_edit_message(
        query,
        text,
        keyboard
    )


# =========================================================
# 📚 نمایش فصل بانکداری
# =========================================================

async def banking_chapter_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        chapter = int(
            query.data.replace(
                "banking_chapter_",
                ""
            )
        )

    except (ValueError, AttributeError):

        await safe_edit_message(
            query,
            "❌ شماره فصل نامعتبر است.",
            banking_back_menu()
        )

        return

    # -----------------------------------------------------
    # بررسی فصل
    # -----------------------------------------------------

    if chapter not in CHAPTER_NAMES:

        await safe_edit_message(
            query,
            "❌ این فصل وجود ندارد.",
            banking_back_menu()
        )

        return

    # -----------------------------------------------------
    # دریافت متن فصل
    # -----------------------------------------------------

    try:

        result = banking_chapter_text(chapter)

        if isinstance(result, tuple):

            text, default_keyboard = result

        else:

            text = result
            default_keyboard = banking_back_menu()

    except Exception as error:

        logger.exception(
            "Chapter %s loading error: %s",
            chapter,
            error
        )

        await safe_edit_message(
            query,
            """
⚠️ خطا در بارگذاری درسنامه.

لطفاً دوباره تلاش کنید.
""",
            banking_back_menu()
        )

        return

    # -----------------------------------------------------
    # دکمه‌ها
    # -----------------------------------------------------

    keyboard = [

        [
            InlineKeyboardButton(
                f"📝 آزمون فصل {chapter}",
                callback_data=f"banking_exam_intro_{chapter}"
            )
        ],

    ]

    if chapter > 1:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⬅️ فصل قبل",
                    callback_data=f"banking_chapter_{chapter - 1}"
                ),

                InlineKeyboardButton(
                    "فصل بعد ➡️",
                    callback_data=f"banking_chapter_{chapter + 1}"
                )
            ]
        )

    else:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "فصل بعد ➡️",
                    callback_data="banking_chapter_2"
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

    await safe_edit_message(
        query,
        text,
        InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 معرفی آزمون فصل
# =========================================================

async def banking_exam_intro_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        chapter = int(
            query.data.replace(
                "banking_exam_intro_",
                ""
            )
        )

    except (ValueError, AttributeError):

        await safe_edit_message(
            query,
            "❌ شماره فصل نامعتبر است.",
            banking_back_menu()
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await safe_edit_message(
            query,
            """
❌ برای این فصل هنوز سؤال آزمون ثبت نشده است.
""",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📖 مشاهده درسنامه",
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
• پاسخ‌ها بررسی می‌شوند.
• امتیاز شما محاسبه می‌شود.
• نتیجه در پایان نمایش داده می‌شود.

━━━━━━━━━━━━━━━━━━

🎯 مسیر پیشنهادی:

📖 مطالعه درسنامه
⬇️
📝 آزمون
⬇️
❌ بررسی اشتباهات
⬇️
🔄 مرور فصل

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

        [
            InlineKeyboardButton(
                "🏦 بانکداری",
                callback_data="banking"
            )
        ],

    ]

    await safe_edit_message(
        query,
        text,
        InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 سؤال آزمون
# =========================================================

async def banking_exam_question_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        score = int(data[4])

    except (IndexError, ValueError, AttributeError):

        await safe_edit_message(
            query,
            """
⚠️ اطلاعات آزمون نامعتبر است.

لطفاً آزمون را دوباره شروع کنید.
""",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 بازگشت به بانکداری",
                            callback_data="banking"
                        )
                    ]
                ]
            )
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await safe_edit_message(
            query,
            "❌ سوالی برای این فصل وجود ندارد.",
            banking_back_menu()
        )

        return

    # -----------------------------------------------------
    # پایان آزمون
    # -----------------------------------------------------

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

    await safe_edit_message(
        query,
        text,
        InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 پاسخ سؤال
# =========================================================

async def banking_answer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        data = query.data.split("_")

        chapter = int(data[2])
        index = int(data[3])
        selected = int(data[4])
        score = int(data[5])

    except (IndexError, ValueError, AttributeError):

        await safe_edit_message(
            query,
            """
⚠️ خطایی در پردازش پاسخ رخ داد.

لطفاً آزمون را دوباره شروع کنید.
""",
            banking_back_menu()
        )

        return

    questions = BANKING_CHAPTER_QUESTIONS.get(
        chapter,
        []
    )

    if not questions:

        await safe_edit_message(
            query,
            "❌ سوالی برای این فصل وجود ندارد.",
            banking_back_menu()
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

    # -----------------------------------------------------
    # پاسخ صحیح
    # -----------------------------------------------------

    if selected == correct:

        score += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {score}

━━━━━━━━━━━━━━━━━━

👏 عملکرد خوبی داشتید.

به سؤال بعدی بروید.
"""

    # -----------------------------------------------------
    # پاسخ غلط
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
    # سؤال بعدی
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
                    "📖 مشاهده درسنامه",
                    callback_data=f"banking_chapter_{chapter}"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏦 خروج از آزمون",
                    callback_data="banking"
                )
            ],

        ]

        await safe_edit_message(
            query,
            result_text,
            InlineKeyboardMarkup(keyboard)
        )

    # -----------------------------------------------------
    # پایان آزمون
    # -----------------------------------------------------

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

        await safe_edit_message(
            query,
            "❌ آزمونی برای این فصل وجود ندارد.",
            banking_back_menu()
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

🎯 مسیر پیشنهادی:

📖 مرور درسنامه
+
❌ بررسی اشتباهات
+
📝 تکرار آزمون
+
📘 مطالعه فصل بعد

━━━━━━━━━━━━━━━━━━
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

    ]

    if chapter < TOTAL_BANKING_CHAPTERS:

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 ورود به فصل {chapter + 1}",
                    callback_data=f"banking_chapter_{chapter + 1}"
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

    await safe_edit_message(
        query,
        text,
        InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 🏆 آزمون جامع بانکداری
# =========================================================

async def banking_full_exam_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    try:

        text, keyboard = banking_full_exam_text()

    except Exception as error:

        logger.exception(
            "Full banking exam error: %s",
            error
        )

        text = """
🏆 آزمون جامع بانکداری

⚠️ این بخش در حال آماده‌سازی است.
"""

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

    await safe_edit_message(
        query,
        text,
        keyboard
    )


# =========================================================
# 🏆 شروع آزمون جامع
# =========================================================

async def banking_full_exam_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await safe_answer(query)

    await safe_edit_message(
        query,
        """
🏆 آزمون جامع بانکداری

━━━━━━━━━━━━━━━━━━

🚧 سیستم آزمون جامع در حال توسعه است.

این بخش قرار است شامل:

📘 مبانی بانکداری
💰 سپرده‌ها
💳 تسهیلات
📑 عقود
⚖️ قوانین
🧾 چک
🔐 پولشویی
📊 اعتبارسنجی
💻 بانکداری الکترونیک
📈 مدیریت ریسک
🏛️ بانک مرکزی
🕌 بانکداری اسلامی

باشد.

━━━━━━━━━━━━━━━━━━

نسخه تخصصی آزمون جامع
در مرحله بعدی به سیستم اضافه می‌شود.
""",
        InlineKeyboardMarkup(
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

    await safe_answer(query)

    await safe_edit_message(
        query,
        """
🚧 این بخش در حال توسعه است.

محتوای تخصصی این قسمت به‌صورت
ماژول مستقل در حال آماده‌سازی است.

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
""",
        InlineKeyboardMarkup(
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

    await safe_answer(
        query,
        "این گزینه در حال حاضر فعال نیست."
    )


# =========================================================
# خطای عمومی Application
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.exception(
        "Unhandled bot error:",
        exc_info=context.error
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
    # BANKING FULL EXAM
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

    # =====================================================
    # BANKING CHAPTERS
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
    # BANKING EXAM QUESTIONS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_exam_question_callback,
            pattern=r"^banking_exam_[0-9]+_[0-9]+_[0-9]+$"
        )
    )

    # =====================================================
    # BANKING ANSWERS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            banking_answer_callback,
            pattern=r"^banking_answer_[0-9]+_[0-9]+_[0-9]+_[0-9]+$"
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
    # UNKNOWN CALLBACK
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
