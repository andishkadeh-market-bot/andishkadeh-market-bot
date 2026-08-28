# =========================================================
# employment_exam.py
# 📝 سیستم آزمون استخدامی
# اندیشکده مدیریت و بازار
#
# شامل:
# 🏦 بانک رفاه
# 🏙️ بانک شهر
# 🟢 بانک مهر
# 🏛️ بانک‌های دولتی
#
# سطوح:
# 🟢 آسان
# 🟡 متوسط
# 🔴 سخت
#
# 🎯 آزمون موضوعی
# 🎲 سوال تصادفی
# 🧪 شبیه‌سازی آزمون واقعی
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# BANKS
# =========================================================

BANKS = {
    "refah": "🏦 بانک رفاه",
    "shahr": "🏙️ بانک شهر",
    "mehr": "🟢 بانک مهر",
    "government": "🏛️ بانک‌های دولتی",
}


DIFFICULTIES = {
    "easy": "🟢 آسان",
    "medium": "🟡 متوسط",
    "hard": "🔴 سخت",
}


# =========================================================
# QUESTION BANK
# =========================================================

EMPLOYMENT_QUESTIONS = [

    # -----------------------------------------------------
    # بانک رفاه - آسان
    # -----------------------------------------------------

    {
        "bank": "refah",
        "difficulty": "easy",
        "subject": "banking",
        "question": "کدام مورد از وظایف اصلی بانک‌ها محسوب می‌شود؟",
        "options": [
            "تولید کالا",
            "واسطه‌گری مالی",
            "تولید مواد اولیه",
            "تعیین مالیات"
        ],
        "correct": 1
    },

    {
        "bank": "refah",
        "difficulty": "easy",
        "subject": "banking",
        "question": "سپرده دیداری معمولاً چه ویژگی‌ای دارد؟",
        "options": [
            "امکان برداشت و استفاده در معاملات",
            "عدم امکان برداشت",
            "فقط برای خرید سهام",
            "فقط برای صادرات"
        ],
        "correct": 0
    },

    {
        "bank": "refah",
        "difficulty": "easy",
        "subject": "economics",
        "question": "تورم به چه معناست؟",
        "options": [
            "کاهش عمومی قیمت‌ها",
            "افزایش مستمر و عمومی سطح قیمت‌ها",
            "افزایش تولید",
            "کاهش نقدینگی"
        ],
        "correct": 1
    },

    {
        "bank": "refah",
        "difficulty": "easy",
        "subject": "general",
        "question": "کدام گزینه جزء مهارت‌های عمومی کار با رایانه است؟",
        "options": [
            "ICDL",
            "حسابداری صنعتی",
            "بازاریابی بین‌الملل",
            "اقتصاد کلان"
        ],
        "correct": 0
    },

    # -----------------------------------------------------
    # بانک رفاه - متوسط
    # -----------------------------------------------------

    {
        "bank": "refah",
        "difficulty": "medium",
        "subject": "banking",
        "question": "کدام گزینه بیشتر با سیاست پولی ارتباط دارد؟",
        "options": [
            "مالیات",
            "مخارج عمرانی دولت",
            "نرخ بهره و حجم پول",
            "بودجه عمومی"
        ],
        "correct": 2
    },

    {
        "bank": "refah",
        "difficulty": "medium",
        "subject": "economics",
        "question": "افزایش نرخ بهره معمولاً چه اثری بر هزینه استقراض دارد؟",
        "options": [
            "کاهش می‌دهد",
            "افزایش می‌دهد",
            "بدون اثر است",
            "آن را حذف می‌کند"
        ],
        "correct": 1
    },

    {
        "bank": "refah",
        "difficulty": "medium",
        "subject": "banking",
        "question": "نقدینگی معمولاً شامل چه اجزایی است؟",
        "options": [
            "فقط اسکناس",
            "فقط سکه",
            "پول و شبه‌پول",
            "فقط ارز خارجی"
        ],
        "correct": 2
    },

    {
        "bank": "refah",
        "difficulty": "medium",
        "subject": "general",
        "question": "کدام مورد نمونه‌ای از احراز هویت مشتری است؟",
        "options": [
            "بررسی مشخصات هویتی",
            "افزایش قیمت کالا",
            "کاهش نرخ ارز",
            "افزایش تولید"
        ],
        "correct": 0
    },

    # -----------------------------------------------------
    # بانک رفاه - سخت
    # -----------------------------------------------------

    {
        "bank": "refah",
        "difficulty": "hard",
        "subject": "banking",
        "question": "هدف اصلی مقررات مبارزه با پولشویی چیست؟",
        "options": [
            "افزایش صادرات",
            "جلوگیری از ورود وجوه حاصل از فعالیت‌های مجرمانه به چرخه رسمی اقتصاد",
            "افزایش نرخ بهره",
            "کاهش مالیات"
        ],
        "correct": 1
    },

    {
        "bank": "refah",
        "difficulty": "hard",
        "subject": "economics",
        "question": "در شرایط عادی، سیاست پولی انقباضی با چه هدفی به کار گرفته می‌شود؟",
        "options": [
            "افزایش فشارهای تورمی",
            "کاهش تقاضای کل و فشارهای تورمی",
            "افزایش کسری بودجه",
            "افزایش واردات"
        ],
        "correct": 1
    },

    # -----------------------------------------------------
    # بانک شهر
    # -----------------------------------------------------

    {
        "bank": "shahr",
        "difficulty": "easy",
        "subject": "banking",
        "question": "بانک چه نقشی در اقتصاد دارد؟",
        "options": [
            "واسطه‌گری بین صاحبان منابع و متقاضیان منابع",
            "تولید خودرو",
            "تولید مواد غذایی",
            "تعیین نرخ مالیات"
        ],
        "correct": 0
    },

    {
        "bank": "shahr",
        "difficulty": "easy",
        "subject": "economics",
        "question": "قانون تقاضا در شرایط برابر چه رابطه‌ای را بیان می‌کند؟",
        "options": [
            "افزایش قیمت معمولاً باعث کاهش مقدار تقاضا می‌شود",
            "افزایش قیمت همیشه تقاضا را دو برابر می‌کند",
            "قیمت هیچ اثری بر تقاضا ندارد",
            "افزایش قیمت عرضه را کاهش می‌دهد"
        ],
        "correct": 0
    },

    {
        "bank": "shahr",
        "difficulty": "medium",
        "subject": "banking",
        "question": "ریسک اعتباری به چه معناست؟",
        "options": [
            "احتمال ناتوانی طرف مقابل در ایفای تعهدات",
            "احتمال افزایش فروش",
            "احتمال کاهش هزینه اداری",
            "افزایش سرمایه بانک"
        ],
        "correct": 0
    },

    {
        "bank": "shahr",
        "difficulty": "medium",
        "subject": "economics",
        "question": "تولید ناخالص داخلی چه چیزی را اندازه‌گیری می‌کند؟",
        "options": [
            "ارزش کالاها و خدمات نهایی تولیدشده در اقتصاد",
            "کل دارایی خانوارها",
            "کل پول نقد مردم",
            "فقط میزان صادرات"
        ],
        "correct": 0
    },

    {
        "bank": "shahr",
        "difficulty": "hard",
        "subject": "banking",
        "question": "کدام گزینه نمونه‌ای از ریسک نقدینگی است؟",
        "options": [
            "ناتوانی در تأمین تعهدات سررسیدشده",
            "افزایش بهره‌وری",
            "افزایش فروش",
            "کاهش هزینه تبلیغات"
        ],
        "correct": 0
    },

    {
        "bank": "shahr",
        "difficulty": "hard",
        "subject": "economics",
        "question": "اگر نرخ تورم از نرخ رشد اسمی درآمد بیشتر باشد، قدرت خرید واقعی چه وضعیتی پیدا می‌کند؟",
        "options": [
            "افزایش می‌یابد",
            "کاهش می‌یابد",
            "حتماً ثابت می‌ماند",
            "دو برابر می‌شود"
        ],
        "correct": 1
    },

    # -----------------------------------------------------
    # بانک مهر
    # -----------------------------------------------------

    {
        "bank": "mehr",
        "difficulty": "easy",
        "subject": "banking",
        "question": "هدف اصلی واسطه‌گری مالی چیست؟",
        "options": [
            "ارتباط میان پس‌اندازکنندگان و متقاضیان منابع",
            "تولید کالا",
            "تعیین مالیات",
            "تعیین قیمت ارز"
        ],
        "correct": 0
    },

    {
        "bank": "mehr",
        "difficulty": "easy",
        "subject": "economics",
        "question": "کدام گزینه یکی از عوامل مؤثر بر رشد اقتصادی است؟",
        "options": [
            "بهره‌وری",
            "کاهش فناوری",
            "کاهش سرمایه‌گذاری",
            "کاهش ظرفیت تولید"
        ],
        "correct": 0
    },

    {
        "bank": "mehr",
        "difficulty": "medium",
        "subject": "banking",
        "question": "اعتبارسنجی مشتری بیشتر با چه هدفی انجام می‌شود؟",
        "options": [
            "بررسی توان و سابقه ایفای تعهدات",
            "افزایش قیمت کالا",
            "تعیین مالیات",
            "افزایش صادرات"
        ],
        "correct": 0
    },

    {
        "bank": "mehr",
        "difficulty": "medium",
        "subject": "general",
        "question": "کدام گزینه برای ارتباط مؤثر با مشتری اهمیت بیشتری دارد؟",
        "options": [
            "گوش دادن فعال",
            "قطع کردن صحبت مشتری",
            "بی‌توجهی",
            "ارائه اطلاعات نادرست"
        ],
        "correct": 0
    },

    {
        "bank": "mehr",
        "difficulty": "hard",
        "subject": "banking",
        "question": "تنوع‌بخشی در مدیریت ریسک معمولاً با چه هدفی انجام می‌شود؟",
        "options": [
            "کاهش تمرکز ریسک",
            "افزایش تمرکز ریسک",
            "افزایش قطعی سود",
            "حذف کامل ریسک"
        ],
        "correct": 0
    },

    # -----------------------------------------------------
    # بانک‌های دولتی
    # -----------------------------------------------------

    {
        "bank": "government",
        "difficulty": "easy",
        "subject": "banking",
        "question": "بانک مرکزی معمولاً چه نقشی دارد؟",
        "options": [
            "سیاست‌گذاری پولی و نظارت بر نظام پولی",
            "تولید کالا",
            "فروشگاه‌داری",
            "تولید خودرو"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "easy",
        "subject": "economics",
        "question": "بیکاری به طور کلی به چه وضعیتی اشاره دارد؟",
        "options": [
            "فرد آماده و مایل به کار است ولی شغل ندارد",
            "فرد دارای شغل است",
            "فرد بازنشسته است",
            "فرد دانش‌آموز است"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "subject": "banking",
        "question": "عملیات بازار باز بیشتر در حوزه کدام سیاست قرار می‌گیرد؟",
        "options": [
            "سیاست پولی",
            "سیاست مالی",
            "سیاست تجاری",
            "سیاست صنعتی"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "subject": "economics",
        "question": "کدام مورد ابزار سیاست مالی است؟",
        "options": [
            "مالیات",
            "عملیات بازار باز",
            "ذخایر بانکی",
            "نرخ سیاستی بانک مرکزی"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "hard",
        "subject": "banking",
        "question": "کدام مورد می‌تواند از پیامدهای ضعف مدیریت نقدینگی بانک باشد؟",
        "options": [
            "مشکل در ایفای تعهدات کوتاه‌مدت",
            "افزایش قطعی سود",
            "کاهش ریسک",
            "افزایش خودکار سرمایه"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "hard",
        "subject": "economics",
        "question": "سیاست مالی انبساطی معمولاً شامل کدام اقدام است؟",
        "options": [
            "افزایش مخارج دولت یا کاهش مالیات",
            "کاهش مخارج دولت و افزایش مالیات",
            "افزایش نرخ بهره",
            "کاهش نقدینگی توسط بانک مرکزی"
        ],
        "correct": 0
    },

    # -----------------------------------------------------
    # عمومی مشترک
    # -----------------------------------------------------

    {
        "bank": "government",
        "difficulty": "easy",
        "subject": "general",
        "question": "کدام گزینه یک موتور جست‌وجوی اینترنتی است؟",
        "options": [
            "Google",
            "Excel",
            "Windows",
            "PowerPoint"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "subject": "general",
        "question": "در Excel تابع SUM معمولاً برای چه کاری استفاده می‌شود؟",
        "options": [
            "جمع کردن مقادیر",
            "حذف فایل",
            "ارسال ایمیل",
            "ایجاد تصویر"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "hard",
        "subject": "general",
        "question": "کدام گزینه برای امنیت حساب کاربری مناسب‌تر است؟",
        "options": [
            "استفاده از رمز عبور قوی و احراز هویت چندمرحله‌ای",
            "استفاده از یک رمز ساده برای همه حساب‌ها",
            "ارسال رمز برای دیگران",
            "ذخیره رمز در پیام عمومی"
        ],
        "correct": 0
    },
]


# =========================================================
# TEXT
# =========================================================

def employment_exam_text():

    return """
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

بانک سؤال تخصصی آزمون‌های استخدامی

━━━━━━━━━━━━━━━━━━

🏦 بانک رفاه
🏙️ بانک شهر
🟢 بانک مهر
🏛️ بانک‌های دولتی

━━━━━━━━━━━━━━━━━━

🎯 امکانات:

🟢 سطح آسان
🟡 سطح متوسط
🔴 سطح سخت

🎲 سوالات تصادفی

🧪 شبیه‌سازی آزمون واقعی

━━━━━━━━━━━━━━━━━━

با مطالعه، تمرین و تحلیل اشتباهات
آمادگی خود را مرحله‌به‌مرحله افزایش دهید.
"""


# =========================================================
# MAIN MENU
# =========================================================

def employment_exam_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🏦 بانک رفاه",
                callback_data="employment_bank_refah"
            )
        ],

        [
            InlineKeyboardButton(
                "🏙️ بانک شهر",
                callback_data="employment_bank_shahr"
            )
        ],

        [
            InlineKeyboardButton(
                "🟢 بانک مهر",
                callback_data="employment_bank_mehr"
            )
        ],

        [
            InlineKeyboardButton(
                "🏛️ بانک‌های دولتی",
                callback_data="employment_bank_government"
            )
        ],

        [
            InlineKeyboardButton(
                "🟢 آسان",
                callback_data="employment_difficulty_easy"
            ),
            InlineKeyboardButton(
                "🟡 متوسط",
                callback_data="employment_difficulty_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سخت",
                callback_data="employment_difficulty_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "🎲 سوالات تصادفی",
                callback_data="employment_random"
            )
        ],

        [
            InlineKeyboardButton(
                "🧪 شبیه‌سازی آزمون واقعی",
                callback_data="employment_simulation"
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
# CALLBACK MAIN
# =========================================================

async def employment_exam_callback(update, context):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        employment_exam_text(),
        reply_markup=employment_exam_menu()
    )


# =========================================================
# FILTER
# =========================================================

def get_questions(bank=None, difficulty=None):

    questions = EMPLOYMENT_QUESTIONS.copy()

    if bank:
        questions = [
            q for q in questions
            if q["bank"] == bank
        ]

    if difficulty:
        questions = [
            q for q in questions
            if q["difficulty"] == difficulty
        ]

    return questions


# =========================================================
# BANK MENU CALLBACK
# =========================================================

async def employment_bank_callback(update, context):

    query = update.callback_query

    await query.answer()

    bank = query.data.replace(
        "employment_bank_",
        ""
    )

    if bank not in BANKS:

        await query.edit_message_text(
            "❌ بانک موردنظر پیدا نشد.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = get_questions(
        bank=bank
    )

    text = f"""
{BANKS[bank]}

━━━━━━━━━━━━━━━━━━

📝 تعداد سوالات موجود:
{len(questions)}

🎯 سطح آزمون را انتخاب کنید:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 آسان",
                callback_data=f"employment_start_bank_{bank}_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 متوسط",
                callback_data=f"employment_start_bank_{bank}_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سخت",
                callback_data=f"employment_start_bank_{bank}_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 همه سطوح",
                callback_data=f"employment_start_bank_{bank}_all"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="employment_exam"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# DIFFICULTY CALLBACK
# =========================================================

async def employment_difficulty_callback(update, context):

    query = update.callback_query

    await query.answer()

    difficulty = query.data.replace(
        "employment_difficulty_",
        ""
    )

    if difficulty not in DIFFICULTIES:

        await query.edit_message_text(
            "❌ سطح نامعتبر است.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = get_questions(
        difficulty=difficulty
    )

    text = f"""
{DIFFICULTIES[difficulty]}

━━━━━━━━━━━━━━━━━━

📝 تعداد سوالات:
{len(questions)}

🎯 بانک‌های مختلف در این آزمون
بر اساس سطح انتخاب‌شده ترکیب شده‌اند.

━━━━━━━━━━━━━━━━━━
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع آزمون",
                callback_data=f"employment_start_difficulty_{difficulty}"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="employment_exam"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# START FILTERED EXAM
# =========================================================

async def employment_start_callback(update, context):

    query = update.callback_query

    await query.answer()

    data = query.data.split("_")

    # employment_start_bank_bankname_difficulty
    if len(data) >= 5 and data[2] == "bank":

        bank = data[3]
        difficulty = data[4]

        if difficulty == "all":
            questions = get_questions(bank=bank)
        else:
            questions = get_questions(
                bank=bank,
                difficulty=difficulty
            )

    # employment_start_difficulty_difficulty
    elif len(data) >= 4 and data[2] == "difficulty":

        difficulty = data[3]

        questions = get_questions(
            difficulty=difficulty
        )

    else:

        await query.edit_message_text(
            "❌ اطلاعات آزمون نامعتبر است.",
            reply_markup=employment_exam_menu()
        )

        return

    if not questions:

        await query.edit_message_text(
            "❌ در این بخش هنوز سؤال کافی ثبت نشده است.",
            reply_markup=employment_exam_menu()
        )

        return

    context.user_data["employment_questions"] = questions

    await show_question(
        query,
        questions,
        0,
        0
    )


# =========================================================
# RANDOM
# =========================================================

async def employment_random_callback(update, context):

    query = update.callback_query

    await query.answer()

    import random

    questions = EMPLOYMENT_QUESTIONS.copy()

    random.shuffle(questions)

    questions = questions[:10]

    context.user_data["employment_questions"] = questions

    await show_question(
        query,
        questions,
        0,
        0
    )


# =========================================================
# SIMULATION
# =========================================================

async def employment_simulation_callback(update, context):

    query = update.callback_query

    await query.answer()

    import random

    questions = EMPLOYMENT_QUESTIONS.copy()

    random.shuffle(questions)

    questions = questions[:20]

    context.user_data["employment_questions"] = questions

    text = """
🧪 شبیه‌سازی آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🎯 آزمون ترکیبی

📝 تعداد سؤالات:
20 سؤال

⏱️ فعلاً بدون محدودیت زمانی

🏦 شامل:
بانکداری
اقتصاد
مهارت‌های عمومی

━━━━━━━━━━━━━━━━━━

سؤالات به صورت ترکیبی انتخاب شده‌اند.

👇 آزمون را شروع کنید:
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع شبیه‌سازی",
                callback_data="employment_simulation_start"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="employment_exam"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def employment_simulation_start_callback(update, context):

    query = update.callback_query

    await query.answer()

    questions = context.user_data.get(
        "employment_questions",
        []
    )

    if not questions:

        await query.edit_message_text(
            "❌ آزمون شبیه‌سازی پیدا نشد.",
            reply_markup=employment_exam_menu()
        )

        return

    await show_question(
        query,
        questions,
        0,
        0
    )


# =========================================================
# SHOW QUESTION
# =========================================================

async def show_question(
    query,
    questions,
    index,
    score
):

    if index >= len(questions):

        await show_result(
            query,
            questions,
            score
        )

        return

    question = questions[index]

    bank_name = BANKS.get(
        question["bank"],
        "آزمون استخدامی"
    )

    difficulty_name = DIFFICULTIES.get(
        question["difficulty"],
        ""
    )

    text = f"""
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

{bank_name}

{difficulty_name}

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
                        f"employment_answer_"
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
                "❌ خروج از آزمون",
                callback_data="employment_exam"
            )
        ]
    )

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# ANSWER
# =========================================================

async def employment_answer_callback(update, context):

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
            "⚠️ خطا در پردازش پاسخ.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = context.user_data.get(
        "employment_questions",
        []
    )

    if not questions:

        await query.edit_message_text(
            "❌ آزمون منقضی شده است.",
            reply_markup=employment_exam_menu()
        )

        return

    if index >= len(questions):

        await show_result(
            query,
            questions,
            score
        )

        return

    question = questions[index]

    correct = question["correct"]

    if selected == correct:

        score += 1

        result_text = """
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

آفرین 👏
"""

    else:

        correct_option = question["options"][correct]

        result_text = f"""
❌ پاسخ اشتباه است.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{correct_option}
"""

    next_index = index + 1

    if next_index >= len(questions):

        await show_result(
            query,
            questions,
            score,
            prefix=result_text
        )

        return

    keyboard = [

        [
            InlineKeyboardButton(
                "➡️ سؤال بعدی",
                callback_data=(
                    f"employment_next_"
                    f"{next_index}_"
                    f"{score}"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "❌ خروج از آزمون",
                callback_data="employment_exam"
            )
        ],

    ]

    await query.edit_message_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# NEXT
# =========================================================

async def employment_next_callback(update, context):

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
            "⚠️ خطا در اطلاعات آزمون.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = context.user_data.get(
        "employment_questions",
        []
    )

    await show_question(
        query,
        questions,
        index,
        score
    )


# =========================================================
# RESULT
# =========================================================

async def show_result(
    query,
    questions,
    score,
    prefix=""
):

    total = len(questions)

    if total == 0:

        await query.edit_message_text(
            "❌ آزمون بدون سؤال است.",
            reply_markup=employment_exam_menu()
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
        evaluation = "📚 نیازمند مطالعه بیشتر"

    text = f"""
{prefix}

🏁 آزمون استخدامی به پایان رسید.

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی:

{evaluation}

━━━━━━━━━━━━━━━━━━

🎯 پیشنهاد:

📖 مطالعه مباحث
+
📝 تمرین بیشتر
+
🔍 بررسی اشتباهات
+
🔄 تکرار آزمون
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 آزمون مجدد",
                callback_data="employment_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🎲 سوالات تصادفی",
                callback_data="employment_random"
            )
        ],

        [
            InlineKeyboardButton(
                "🧪 شبیه‌سازی",
                callback_data="employment_simulation"
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
