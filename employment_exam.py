# =========================================================
# employment_exam.py
# 📝 سیستم جامع آزمون استخدامی
# 🏛️ اندیشکده مدیریت و بازار
#
# نسخه:
# بانک سؤال + دسته‌بندی بانک‌ها + سطح دشواری
# آسان / متوسط / سخت
# آزمون تمرینی
# آزمون شبیه‌سازی‌شده
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# بانک‌های هدف
# =========================================================

BANK_CATEGORIES = {
    "refah": "🏦 بانک رفاه",
    "shahr": "🏙️ بانک شهر",
    "mehr": "🏦 بانک مهر",
    "government": "🏛️ بانک‌های دولتی",
}


# =========================================================
# سطوح
# =========================================================

DIFFICULTY_NAMES = {
    "easy": "🟢 آسان",
    "medium": "🟡 متوسط",
    "hard": "🔴 سخت",
}


# =========================================================
# بانک سؤال
#
# ساختار:
#
# {
#     "bank": "refah",
#     "difficulty": "easy",
#     "category": "banking",
#     "question": "...",
#     "options": [...],
#     "correct": 0
# }
# =========================================================

EMPLOYMENT_QUESTIONS = [

    # -----------------------------------------------------
    # بانک رفاه
    # -----------------------------------------------------

    {
        "bank": "refah",
        "difficulty": "easy",
        "category": "banking",
        "question": "کدام گزینه بیشتر با فعالیت اصلی بانک‌ها ارتباط دارد؟",
        "options": [
            "تولید کالا",
            "واسطه‌گری مالی",
            "تولید مواد غذایی",
            "تولید خودرو"
        ],
        "correct": 1
    },

    {
        "bank": "refah",
        "difficulty": "medium",
        "category": "banking",
        "question": "کدام مورد از وظایف مهم بانک مرکزی است؟",
        "options": [
            "تولید کالاهای مصرفی",
            "تنظیم و نظارت بر نظام پولی و بانکی",
            "فروش محصولات صنعتی",
            "تأمین مواد اولیه کارخانه‌ها"
        ],
        "correct": 1
    },

    {
        "bank": "refah",
        "difficulty": "hard",
        "category": "banking",
        "question": "کدام گزینه مفهوم مناسب‌تری از ریسک اعتباری را بیان می‌کند؟",
        "options": [
            "احتمال تغییر نرخ ارز",
            "احتمال ناتوانی مشتری در ایفای تعهدات مالی",
            "احتمال افزایش هزینه کارکنان",
            "احتمال کاهش قیمت سهام"
        ],
        "correct": 1
    },

    # -----------------------------------------------------
    # بانک شهر
    # -----------------------------------------------------

    {
        "bank": "shahr",
        "difficulty": "easy",
        "category": "banking",
        "question": "بانک‌ها عمدتاً با کدام یک از موارد زیر سروکار دارند؟",
        "options": [
            "پول و اعتبار",
            "کشاورزی",
            "ساختمان‌سازی",
            "حمل‌ونقل"
        ],
        "correct": 0
    },

    {
        "bank": "shahr",
        "difficulty": "medium",
        "category": "economics",
        "question": "افزایش نرخ بهره معمولاً چه اثری بر هزینه استقراض دارد؟",
        "options": [
            "کاهش می‌دهد",
            "افزایش می‌دهد",
            "هیچ اثری ندارد",
            "همیشه آن را حذف می‌کند"
        ],
        "correct": 1
    },

    {
        "bank": "shahr",
        "difficulty": "hard",
        "category": "economics",
        "question": "کدام مورد می‌تواند یکی از پیامدهای افزایش شدید نقدینگی بدون رشد متناسب تولید باشد؟",
        "options": [
            "کاهش قطعی قیمت‌ها",
            "فشارهای تورمی",
            "حذف کامل بیکاری",
            "افزایش قطعی صادرات"
        ],
        "correct": 1
    },

    # -----------------------------------------------------
    # بانک مهر
    # -----------------------------------------------------

    {
        "bank": "mehr",
        "difficulty": "easy",
        "category": "banking",
        "question": "سپرده بانکی چیست؟",
        "options": [
            "وجهی که مشتری نزد بانک قرار می‌دهد",
            "وام پرداخت‌شده توسط بانک",
            "مالیات پرداختی",
            "هزینه اداری بانک"
        ],
        "correct": 0
    },

    {
        "bank": "mehr",
        "difficulty": "medium",
        "category": "banking",
        "question": "کدام گزینه از ویژگی‌های یک اعتبارسنجی مناسب مشتری است؟",
        "options": [
            "بررسی توان بازپرداخت",
            "نادیده گرفتن سوابق مالی",
            "عدم بررسی درآمد",
            "عدم توجه به تعهدات قبلی"
        ],
        "correct": 0
    },

    {
        "bank": "mehr",
        "difficulty": "hard",
        "category": "banking",
        "question": "هدف اصلی مدیریت ریسک در بانک چیست؟",
        "options": [
            "حذف تمام فعالیت‌های بانکی",
            "شناسایی، ارزیابی و کنترل ریسک‌ها",
            "افزایش هزینه‌ها",
            "کاهش تعداد مشتریان"
        ],
        "correct": 1
    },

    # -----------------------------------------------------
    # بانک‌های دولتی
    # -----------------------------------------------------

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "economics",
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
        "bank": "government",
        "difficulty": "medium",
        "category": "economics",
        "question": "تولید ناخالص داخلی معمولاً چه چیزی را اندازه‌گیری می‌کند؟",
        "options": [
            "ارزش کالاها و خدمات نهایی تولیدشده",
            "مقدار پول نقد مردم",
            "تعداد بانک‌ها",
            "میزان مالیات"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "hard",
        "category": "economics",
        "question": "سیاست پولی انقباضی معمولاً با چه هدفی اجرا می‌شود؟",
        "options": [
            "افزایش فشارهای تورمی",
            "کاهش فشارهای تورمی",
            "افزایش قطعی مصرف",
            "افزایش مخارج دولت"
        ],
        "correct": 1
    },

    # -----------------------------------------------------
    # عمومی
    # -----------------------------------------------------

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "general",
        "question": "کدام گزینه یک سیستم‌عامل محسوب می‌شود؟",
        "options": [
            "Windows",
            "Excel",
            "Word",
            "PowerPoint"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "category": "general",
        "question": "کدام گزینه برای محاسبات عددی و جدول‌بندی مناسب‌تر است؟",
        "options": [
            "Excel",
            "Paint",
            "Notepad",
            "Browser"
        ],
        "correct": 0
    },

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "language",
        "question": "معنی کلمه 'Bank' در عبارت‌های مالی چیست؟",
        "options": [
            "بازار",
            "بانک",
            "شرکت",
            "فروشگاه"
        ],
        "correct": 1
    },

]


# =========================================================
# وضعیت آزمون
#
# برای هر کاربر وضعیت جداگانه نگهداری می‌شود.
# =========================================================

def _get_exam_state(context):

    if not hasattr(context, "user_data"):
        return {}

    if "employment_exam" not in context.user_data:
        context.user_data["employment_exam"] = {
            "questions": [],
            "index": 0,
            "score": 0,
            "answered": False,
        }

    return context.user_data["employment_exam"]


# =========================================================
# منوی اصلی آزمون استخدامی
# =========================================================

def employment_exam_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🏦 آزمون بانک رفاه",
                callback_data="employment_bank_refah"
            )
        ],

        [
            InlineKeyboardButton(
                "🏙️ آزمون بانک شهر",
                callback_data="employment_bank_shahr"
            )
        ],

        [
            InlineKeyboardButton(
                "🏦 آزمون بانک مهر",
                callback_data="employment_bank_mehr"
            )
        ],

        [
            InlineKeyboardButton(
                "🏛️ آزمون بانک‌های دولتی",
                callback_data="employment_bank_government"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 آزمون سطح آسان",
                callback_data="employment_difficulty_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 آزمون سطح متوسط",
                callback_data="employment_difficulty_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 آزمون سطح سخت",
                callback_data="employment_difficulty_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "🏆 شبیه‌سازی آزمون استخدامی",
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
# متن اصلی آزمون
# =========================================================

def employment_exam_text():

    return """
📝 آزمون استخدامی

🏛️ اندیشکده مدیریت و بازار

━━━━━━━━━━━━━━━━━━

سیستم جامع آزمون استخدامی

📚 بانک سؤال
+
🎯 دسته‌بندی بر اساس بانک
+
📊 سطح‌بندی دشواری
+
🏆 آزمون شبیه‌سازی‌شده

━━━━━━━━━━━━━━━━━━

🏦 بانک رفاه
🏙️ بانک شهر
🏦 بانک مهر
🏛️ بانک‌های دولتی

━━━━━━━━━━━━━━━━━━

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

🎯 در نسخه‌های بعدی بانک سؤال
به‌صورت گسترده‌تر توسعه داده می‌شود.
"""


# =========================================================
# CALLBACK اصلی
# =========================================================

async def employment_exam_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        employment_exam_text(),
        reply_markup=employment_exam_menu()
    )


# =========================================================
# انتخاب بانک
# =========================================================

async def employment_bank_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    bank = query.data.replace(
        "employment_bank_",
        ""
    )

    if bank not in BANK_CATEGORIES:

        await query.edit_message_text(
            "❌ بانک انتخاب‌شده معتبر نیست.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = [
        q for q in EMPLOYMENT_QUESTIONS
        if q["bank"] == bank
    ]

    if not questions:

        await query.edit_message_text(
            "❌ هنوز سؤال برای این بانک ثبت نشده است.",
            reply_markup=employment_exam_menu()
        )

        return

    context.user_data["employment_exam"] = {
        "questions": questions,
        "index": 0,
        "score": 0,
        "answered": False,
    }

    await show_question(
        query,
        context
    )


# =========================================================
# انتخاب سطح
# =========================================================

async def employment_difficulty_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    difficulty = query.data.replace(
        "employment_difficulty_",
        ""
    )

    if difficulty not in DIFFICULTY_NAMES:

        await query.edit_message_text(
            "❌ سطح آزمون معتبر نیست.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = [
        q for q in EMPLOYMENT_QUESTIONS
        if q["difficulty"] == difficulty
    ]

    if not questions:

        await query.edit_message_text(
            "❌ برای این سطح سؤال ثبت نشده است.",
            reply_markup=employment_exam_menu()
        )

        return

    context.user_data["employment_exam"] = {
        "questions": questions,
        "index": 0,
        "score": 0,
        "answered": False,
    }

    await show_question(
        query,
        context
    )


# =========================================================
# آزمون شبیه‌سازی
# =========================================================

async def employment_simulation_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    # فعلاً تمام بانک سؤال استفاده می‌شود.
    # در توسعه بعدی می‌توان تعداد و ترکیب را
    # دقیقاً مشابه آزمون واقعی تنظیم کرد.

    questions = list(
        EMPLOYMENT_QUESTIONS
    )

    if not questions:

        await query.edit_message_text(
            "❌ بانک سؤال خالی است.",
            reply_markup=employment_exam_menu()
        )

        return

    context.user_data["employment_exam"] = {
        "questions": questions,
        "index": 0,
        "score": 0,
        "answered": False,
        "simulation": True,
    }

    await show_question(
        query,
        context
    )


# =========================================================
# نمایش سؤال
# =========================================================

async def show_question(
    query,
    context
):

    state = _get_exam_state(
        context
    )

    questions = state.get(
        "questions",
        []
    )

    index = state.get(
        "index",
        0
    )

    score = state.get(
        "score",
        0
    )

    if index >= len(questions):

        await show_result(
            query,
            context
        )

        return

    question = questions[index]

    bank_name = BANK_CATEGORIES.get(
        question["bank"],
        "آزمون استخدامی"
    )

    difficulty = DIFFICULTY_NAMES.get(
        question["difficulty"],
        ""
    )

    text = f"""
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🏦 {bank_name}

📊 سطح: {difficulty}

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
                        f"{option_index}"
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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# پاسخ سؤال
# =========================================================

async def employment_answer_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        index = int(data[2])
        selected = int(data[3])

    except (
        IndexError,
        ValueError
    ):

        await query.edit_message_text(
            "⚠️ خطا در پردازش پاسخ.",
            reply_markup=employment_exam_menu()
        )

        return

    state = _get_exam_state(
        context
    )

    questions = state.get(
        "questions",
        []
    )

    if index >= len(questions):

        await show_result(
            query,
            context
        )

        return

    question = questions[index]

    correct = question["correct"]

    if selected == correct:

        state["score"] += 1

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

━━━━━━━━━━━━━━━━━━

📚 پاسخ درست را یاد بگیرید و
در آزمون بعدی دوباره تلاش کنید.
"""

    state["index"] = index + 1

    score = state["score"]

    if state["index"] < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data="employment_next"
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
            result_text +
            f"\n\n⭐ امتیاز فعلی: {score}",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    else:

        await show_result(
            query,
            context
        )


# =========================================================
# سؤال بعدی
# =========================================================

async def employment_next_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    await show_question(
        query,
        context
    )


# =========================================================
# نتیجه آزمون
# =========================================================

async def show_result(
    query,
    context
):

    state = _get_exam_state(
        context
    )

    questions = state.get(
        "questions",
        []
    )

    score = state.get(
        "score",
        0
    )

    total = len(
        questions
    )

    if total == 0:

        await query.edit_message_text(
            "❌ آزمونی انجام نشده است.",
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

🎯 پیشنهاد اندیشکده:

📖 مطالعه مباحث
+
📝 حل تست
+
🔍 تحلیل اشتباهات
+
🔄 مرور
+
🏆 آزمون شبیه‌سازی

━━━━━━━━━━━━━━━━━━

آزمون‌های بعدی با بانک سؤال
گسترده‌تر قابل توسعه هستند.
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
                "🏆 شبیه‌سازی آزمون",
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
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# توابع کمکی
# =========================================================

def get_question_count():

    return len(
        EMPLOYMENT_QUESTIONS
    )


def get_bank_question_count(
    bank
):

    return len(
        [
            q for q in EMPLOYMENT_QUESTIONS
            if q["bank"] == bank
        ]
    )


def get_difficulty_question_count(
    difficulty
):

    return len(
        [
            q for q in EMPLOYMENT_QUESTIONS
            if q["difficulty"] == difficulty
        ]
    )


# =========================================================
# پایان فایل
# =========================================================
