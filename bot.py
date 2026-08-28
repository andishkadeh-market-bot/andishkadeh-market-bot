import os
import logging

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
    CHAPTER_NAMES,
    BANKING_CHAPTER_QUESTIONS,
)


# =========================================================
# تنظیمات اولیه
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
آموزش مفهومی مدیریت، تجارت، اقتصاد،
بازاریابی، بانکداری و مهارت‌های حرفه‌ای

📝 آزمون استخدامی
تمرین و آمادگی آزمون‌های استخدامی

🎲 سوالات تصادفی
تمرین سریع و سنجش دانش

🧠 روانشناسی و مددکاری
مفاهیم تخصصی روانشناسی،
مددکاری اجتماعی و مهارت‌های ارتباطی

🏦 بانکداری تخصصی
درسنامه + آزمون فصل + ارزیابی

🌍 تجارت بین‌الملل
مفاهیم تجارت، صادرات، واردات،
بازرگانی و بازارهای بین‌المللی

📈 بازاریابی و فروش
بازاریابی، رفتار مشتری،
فروش و توسعه بازار

💰 اقتصاد و بازار
اقتصاد، بازارها، پول، تورم
و مفاهیم اقتصادی

━━━━━━━━━━━━━━━━━━

🎯 هدف اندیشکده:

یادگیری مفهومی
+
تمرین
+
آزمون
+
تحلیل
+
توسعه مهارت

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

    text, keyboard = banking_intro_text()

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# 📖 نمایش فصل بانکداری
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

        text, _ = banking_chapter_text(chapter)

    except Exception as error:

        logger.exception(
            "Error loading banking chapter %s",
            chapter
        )

        await query.edit_message_text(
            """
⚠️ خطا در بارگذاری درسنامه.

لطفاً دوباره تلاش کنید.
""",
            reply_markup=banking_back_menu()
        )

        return


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
                    if chapter < 12
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
# 📝 معرفی آزمون فصل
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
• پاسخ‌ها بررسی می‌شوند.
• امتیاز شما محاسبه می‌شود.
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
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 نمایش سؤال بانکداری
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
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 📝 بررسی پاسخ
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

🎯 ارزیابی:
{evaluation}

━━━━━━━━━━━━━━━━━━

💡 {message}

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

یادگیری مفهومی
+
تست‌زنی
+
مرور هدفمند
+
آمادگی آزمون
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
# 🧠 روانشناسی و مددکاری اجتماعی
# =========================================================

async def psychology_socialwork_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🧠 روانشناسی و مددکاری اجتماعی

مرکز تخصصی آموزش مفاهیم روانشناسی،
مددکاری اجتماعی و مهارت‌های ارتباطی

━━━━━━━━━━━━━━━━━━

📚 محورهای آموزشی

🧠 روانشناسی عمومی
• ادراک
• یادگیری
• حافظه
• انگیزش
• هیجان
• شخصیت
• رفتار

👥 روانشناسی اجتماعی
• ارتباطات
• گروه
• نگرش
• نفوذ اجتماعی
• تعارض
• رفتار جمعی

🤝 مددکاری اجتماعی
• مفهوم مددکاری
• فرد، خانواده و جامعه
• ارزیابی اجتماعی
• مداخله
• مصاحبه مددکاری
• پرونده اجتماعی
• توانمندسازی
• حمایت اجتماعی

🗣️ مهارت‌های ارتباطی
• گوش دادن فعال
• همدلی
• ارتباط مؤثر
• حل تعارض
• مصاحبه
• ارتباط حرفه‌ای

━━━━━━━━━━━━━━━━━━

🎯 هدف این بخش:

یادگیری مفهومی
+
مهارت حرفه‌ای
+
آمادگی آزمون
+
تمرین

━━━━━━━━━━━━━━━━━━

⚠️ مطالب این بخش آموزشی هستند
و جایگزین تشخیص یا درمان تخصصی
توسط متخصص مربوطه نیستند.

━━━━━━━━━━━━━━━━━━
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🧠 روانشناسی عمومی",
                callback_data="psychology_general"
            )
        ],

        [
            InlineKeyboardButton(
                "👥 روانشناسی اجتماعی",
                callback_data="psychology_social"
            )
        ],

        [
            InlineKeyboardButton(
                "🤝 مددکاری اجتماعی",
                callback_data="social_work"
            )
        ],

        [
            InlineKeyboardButton(
                "🗣️ مهارت‌های ارتباطی",
                callback_data="communication_skills"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون روانشناسی و مددکاری",
                callback_data="psychology_exam"
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
# 📚 زیرمنوی روانشناسی
# =========================================================

async def psychology_general_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🧠 روانشناسی عمومی

━━━━━━━━━━━━━━━━━━

📌 روانشناسی چیست؟

روانشناسی علمی است که رفتار و
فرایندهای ذهنی را مطالعه می‌کند.

━━━━━━━━━━━━━━━━━━

📚 مباحث اصلی

1️⃣ ادراک

فرآیندی که طی آن اطلاعات حسی
سازمان‌دهی و تفسیر می‌شوند.

2️⃣ یادگیری

تغییر نسبتاً پایدار در رفتار یا
توانایی رفتاری در اثر تجربه و تمرین.

3️⃣ حافظه

فرآیندهای رمزگذاری، ذخیره‌سازی
و بازیابی اطلاعات.

4️⃣ انگیزش

فرآیندهایی که رفتار را فعال،
هدایت و حفظ می‌کنند.

5️⃣ هیجان

واکنش‌هایی شامل مؤلفه‌های
احساسی، فیزیولوژیک و رفتاری.

6️⃣ شخصیت

الگوهای نسبتاً پایدار افکار،
احساسات و رفتار فرد.

━━━━━━━━━━━━━━━━━━

🎯 نکته آموزشی

برای مطالعه روانشناسی فقط
تعریف‌ها را حفظ نکنید.

مفهوم
⬇️
مثال
⬇️
کاربرد
⬇️
تفاوت با مفاهیم مشابه

را بررسی کنید.
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
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# 👥 روانشناسی اجتماعی
# =========================================================

async def psychology_social_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
👥 روانشناسی اجتماعی

━━━━━━━━━━━━━━━━━━

روانشناسی اجتماعی به بررسی این
موضوع می‌پردازد که افکار، احساسات
و رفتار افراد چگونه تحت تأثیر
دیگران و موقعیت اجتماعی قرار می‌گیرد.

━━━━━━━━━━━━━━━━━━

📚 مباحث مهم

• نگرش
• کلیشه
• پیش‌داوری
• نفوذ اجتماعی
• همنوایی
• اطاعت
• رفتار گروهی
• ارتباطات
• تعارض
• همکاری
• تصمیم‌گیری گروهی

━━━━━━━━━━━━━━━━━━

🎯 کاربردها

🏢 محیط کار
👥 روابط اجتماعی
🎓 آموزش
🤝 مددکاری
📈 مدیریت
🗣️ ارتباطات

━━━━━━━━━━━━━━━━━━

⭐ نکته

رفتار انسان را نمی‌توان همیشه
صرفاً با یک عامل توضیح داد.

شخص
+
موقعیت
+
گروه
+
فرهنگ

می‌توانند بر رفتار اثر بگذارند.
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 روانشناسی و مددکاری",
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


# =========================================================
# 🤝 مددکاری اجتماعی
# =========================================================

async def social_work_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🤝 مددکاری اجتماعی

━━━━━━━━━━━━━━━━━━

مددکاری اجتماعی حرفه‌ای است که
با هدف کمک به افراد، خانواده‌ها
و گروه‌ها برای مواجهه با مسائل
اجتماعی و افزایش توانمندی آنان
فعالیت می‌کند.

━━━━━━━━━━━━━━━━━━

📚 مفاهیم مهم

1️⃣ مددجو

فرد، خانواده، گروه یا جامعه‌ای
که برای حل یا مدیریت یک مسئله
از خدمات حرفه‌ای استفاده می‌کند.

2️⃣ ارزیابی

شناخت مسئله، شرایط فرد،
منابع حمایتی، عوامل خطر
و ظرفیت‌های موجود.

3️⃣ مداخله

اقدامات حرفه‌ای برای کمک به
مدیریت یا کاهش مسئله و افزایش
توانمندی.

4️⃣ توانمندسازی

تقویت ظرفیت فرد یا جامعه برای
مشارکت و تصمیم‌گیری مؤثر.

5️⃣ حمایت اجتماعی

منابع رسمی و غیررسمی مانند
خانواده، دوستان، نهادها و خدمات
اجتماعی.

━━━━━━━━━━━━━━━━━━

🧩 سطوح مداخله

👤 فرد
👨‍👩‍👧 خانواده
👥 گروه
🏘️ جامعه

━━━━━━━━━━━━━━━━━━

⭐ مهارت‌های مهم مددکار

• گوش دادن فعال
• مصاحبه حرفه‌ای
• همدلی
• مشاهده
• ارزیابی
• مستندسازی
• ارتباط حرفه‌ای
• حفظ مرزهای حرفه‌ای
• ارجاع مناسب

━━━━━━━━━━━━━━━━━━

⚠️ اصل مهم

مددکاری حرفه‌ای باید بر اصول
اخلاقی، حفظ کرامت انسان،
محرمانگی و رعایت حدود حرفه‌ای
استوار باشد.
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 روانشناسی و مددکاری",
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


# =========================================================
# 🗣️ مهارت‌های ارتباطی
# =========================================================

async def communication_skills_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
🗣️ مهارت‌های ارتباطی

━━━━━━━━━━━━━━━━━━

ارتباط مؤثر فقط صحبت کردن نیست.

فرستنده
⬇️
پیام
⬇️
کانال
⬇️
گیرنده
⬇️
بازخورد

━━━━━━━━━━━━━━━━━━

🎯 مهارت‌های مهم

👂 گوش دادن فعال

• توجه به صحبت
• قطع نکردن بی‌مورد
• پرسش مناسب
• بازتاب پیام

❤️ همدلی

تلاش برای درک تجربه و دیدگاه
فرد مقابل بدون قضاوت عجولانه.

🗣️ بیان مؤثر

پیام باید روشن، دقیق و متناسب
با مخاطب باشد.

🤝 حل تعارض

• شناسایی مسئله
• شنیدن دیدگاه‌ها
• تفکیک شخص از مسئله
• پیدا کردن راه‌حل
• توافق

━━━━━━━━━━━━━━━━━━

⭐ نکته حرفه‌ای

همدلی به معنی تأیید تمام
رفتارها یا عقاید فرد نیست.

همدلی یعنی تلاش برای فهمیدن
تجربه او.
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 روانشناسی و مددکاری",
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


# =========================================================
# 📝 آزمون روانشناسی و مددکاری
# =========================================================

async def psychology_exam_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    text = """
📝 آزمون روانشناسی و مددکاری

━━━━━━━━━━━━━━━━━━

🚧 سیستم آزمون تخصصی این بخش
در مرحله طراحی است.

در نسخه کامل:

🧠 روانشناسی عمومی
👥 روانشناسی اجتماعی
🤝 مددکاری اجتماعی
🗣️ مهارت‌های ارتباطی

به‌صورت جداگانه آزمون خواهند داشت.

━━━━━━━━━━━━━━━━━━

🎯 ساختار آزمون:

سؤال
⬇️
چهار گزینه
⬇️
پاسخ
⬇️
تحلیل
⬇️
امتیاز
⬇️
ارزیابی عملکرد
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🧠 مطالعه روانشناسی",
                callback_data="psychology_general"
            )
        ],

        [
            InlineKeyboardButton(
                "🤝 مطالعه مددکاری",
                callback_data="social_work"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
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


# =========================================================
# 🚧 بخش‌های آموزشی موقت
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

هدف این قسمت ارائه محتوای تخصصی،
درسنامه، نمونه‌ها، تمرین‌ها و آزمون‌های
ساختاریافته است.

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
# ⚠️ مدیریت خطا
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.exception(
        "Exception while handling update:",
        exc_info=context.error
    )


# =========================================================
# ❓ Callback ناشناخته
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
    # PSYCHOLOGY / SOCIAL WORK
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            psychology_socialwork_callback,
            pattern=r"^psychology_socialwork$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            psychology_general_callback,
            pattern=r"^psychology_general$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            psychology_social_callback,
            pattern=r"^psychology_social$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            social_work_callback,
            pattern=r"^social_work$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            communication_skills_callback,
            pattern=r"^communication_skills$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            psychology_exam_callback,
            pattern=r"^psychology_exam$"
        )
    )


    # =====================================================
    # OTHER MAIN SECTIONS
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
    # UNKNOWN CALLBACK
    # باید آخرین Handler باشد
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

    application.run_polling()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()
