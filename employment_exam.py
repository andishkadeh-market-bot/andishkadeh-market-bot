# =========================================================
# employment_exam.py
# 📝 سیستم جامع آزمون استخدامی
# 🏛️ اندیشکده مدیریت و بازار
#
# نسخه پایدار اتصال به bot.py
#
# امکانات:
# 🏦 بانک رفاه
# 🏙️ بانک شهر
# 🏦 بانک مهر
# 🏛️ بانک‌های دولتی
#
# 🟢 آسان
# 🟡 متوسط
# 🔴 سخت
#
# 🎯 آزمون تمرینی
# 🏆 آزمون شبیه‌سازی‌شده
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# دسته‌بندی بانک‌ها
# =========================================================

BANK_CATEGORIES = {
    "refah": "🏦 بانک رفاه",
    "shahr": "🏙️ بانک شهر",
    "mehr": "🏦 بانک مهر",
    "government": "🏛️ بانک‌های دولتی",
}


# =========================================================
# سطوح دشواری
# =========================================================

DIFFICULTY_NAMES = {
    "easy": "🟢 آسان",
    "medium": "🟡 متوسط",
    "hard": "🔴 سخت",
}


# =========================================================
# موضوعات
# =========================================================

CATEGORY_NAMES = {
    "banking": "🏦 بانکداری",
    "economics": "💰 اقتصاد",
    "management": "📚 مدیریت",
    "accounting": "🧮 حسابداری",
    "general": "📖 عمومی",
    "language": "🇬🇧 زبان انگلیسی",
    "icdl": "💻 ICDL",
    "intelligence": "🧠 هوش و استعداد",
    "law": "⚖️ قوانین",
}


# =========================================================
# بانک سؤال
#
# هر سؤال:
#
# bank
# difficulty
# category
# question
# options
# correct
# =========================================================

EMPLOYMENT_QUESTIONS = [

    # =====================================================
    # بانک رفاه
    # =====================================================

    {
        "bank": "refah",
        "difficulty": "easy",
        "category": "banking",
        "question": "کدام گزینه بیشتر با فعالیت اصلی بانک‌ها ارتباط دارد؟",
        "options": [
            "تولید کالا",
            "واسطه‌گری مالی",
            "تولید خودرو",
            "کشاورزی"
        ],
        "correct": 1,
    },

    {
        "bank": "refah",
        "difficulty": "medium",
        "category": "banking",
        "question": "کدام مورد از وظایف مهم بانک مرکزی است؟",
        "options": [
            "تولید کالا",
            "تنظیم و نظارت بر نظام پولی و بانکی",
            "فروش کالا",
            "تولید محصولات صنعتی"
        ],
        "correct": 1,
    },

    {
        "bank": "refah",
        "difficulty": "hard",
        "category": "banking",
        "question": "ریسک اعتباری در بانکداری به چه معناست؟",
        "options": [
            "احتمال نوسان نرخ ارز",
            "احتمال ناتوانی مشتری در ایفای تعهدات",
            "احتمال افزایش هزینه کارکنان",
            "احتمال کاهش قیمت سهام"
        ],
        "correct": 1,
    },

    {
        "bank": "refah",
        "difficulty": "medium",
        "category": "economics",
        "question": "افزایش نرخ بهره معمولاً چه اثری بر هزینه استقراض دارد؟",
        "options": [
            "کاهش می‌دهد",
            "افزایش می‌دهد",
            "هیچ اثری ندارد",
            "همیشه آن را حذف می‌کند"
        ],
        "correct": 1,
    },

    # =====================================================
    # بانک شهر
    # =====================================================

    {
        "bank": "shahr",
        "difficulty": "easy",
        "category": "banking",
        "question": "بانک‌ها عمدتاً با کدام مورد سروکار دارند؟",
        "options": [
            "پول و اعتبار",
            "کشاورزی",
            "حمل‌ونقل",
            "تولید خودرو"
        ],
        "correct": 0,
    },

    {
        "bank": "shahr",
        "difficulty": "medium",
        "category": "economics",
        "question": "تورم به چه معناست؟",
        "options": [
            "کاهش عمومی قیمت‌ها",
            "افزایش مستمر و عمومی سطح قیمت‌ها",
            "افزایش تولید",
            "کاهش جمعیت"
        ],
        "correct": 1,
    },

    {
        "bank": "shahr",
        "difficulty": "hard",
        "category": "economics",
        "question": "افزایش شدید نقدینگی بدون رشد متناسب تولید می‌تواند چه اثری داشته باشد؟",
        "options": [
            "کاهش قطعی قیمت‌ها",
            "افزایش فشارهای تورمی",
            "حذف کامل بیکاری",
            "افزایش قطعی صادرات"
        ],
        "correct": 1,
    },

    {
        "bank": "shahr",
        "difficulty": "medium",
        "category": "management",
        "question": "کدام مورد یکی از وظایف اصلی مدیریت است؟",
        "options": [
            "برنامه‌ریزی",
            "حذف سازمان",
            "کاهش اطلاعات",
            "عدم تصمیم‌گیری"
        ],
        "correct": 0,
    },

    # =====================================================
    # بانک مهر
    # =====================================================

    {
        "bank": "mehr",
        "difficulty": "easy",
        "category": "banking",
        "question": "سپرده بانکی چیست؟",
        "options": [
            "وجهی که مشتری نزد بانک قرار می‌دهد",
            "مالیات",
            "وام پرداخت‌شده",
            "هزینه اداری"
        ],
        "correct": 0,
    },

    {
        "bank": "mehr",
        "difficulty": "medium",
        "category": "banking",
        "question": "کدام مورد در اعتبارسنجی مشتری اهمیت دارد؟",
        "options": [
            "توان بازپرداخت",
            "نادیده گرفتن سوابق",
            "عدم بررسی درآمد",
            "عدم توجه به بدهی‌ها"
        ],
        "correct": 0,
    },

    {
        "bank": "mehr",
        "difficulty": "hard",
        "category": "banking",
        "question": "هدف اصلی مدیریت ریسک در بانک چیست؟",
        "options": [
            "حذف تمام فعالیت‌های بانکی",
            "شناسایی، ارزیابی و کنترل ریسک‌ها",
            "کاهش تعداد مشتریان",
            "افزایش هزینه‌ها"
        ],
        "correct": 1,
    },

    {
        "bank": "mehr",
        "difficulty": "medium",
        "category": "economics",
        "question": "کدام گزینه نمونه‌ای از سیاست پولی است؟",
        "options": [
            "تغییر نرخ سیاستی",
            "افزایش بودجه عمرانی دولت",
            "تغییر مالیات",
            "افزایش مخارج دولت"
        ],
        "correct": 0,
    },

    # =====================================================
    # بانک‌های دولتی
    # =====================================================

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "economics",
        "question": "تولید ناخالص داخلی چه چیزی را اندازه‌گیری می‌کند؟",
        "options": [
            "ارزش کالاها و خدمات نهایی تولیدشده",
            "مقدار پول نقد",
            "تعداد بانک‌ها",
            "میزان مالیات"
        ],
        "correct": 0,
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "category": "economics",
        "question": "کدام مورد ابزار سیاست مالی محسوب می‌شود؟",
        "options": [
            "مالیات",
            "عملیات بازار باز",
            "نرخ سیاستی",
            "ذخایر بانکی"
        ],
        "correct": 0,
    },

    {
        "bank": "government",
        "difficulty": "hard",
        "category": "economics",
        "question": "سیاست پولی انقباضی معمولاً با چه هدفی اجرا می‌شود؟",
        "options": [
            "افزایش فشار تورمی",
            "کاهش فشارهای تورمی",
            "افزایش قطعی مصرف",
            "افزایش مخارج دولت"
        ],
        "correct": 1,
    },

    # =====================================================
    # عمومی
    # =====================================================

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "general",
        "question": "کدام گزینه یک سیستم‌عامل است؟",
        "options": [
            "Windows",
            "Excel",
            "Word",
            "PowerPoint"
        ],
        "correct": 0,
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "category": "icdl",
        "question": "کدام نرم‌افزار برای کار با جداول و محاسبات مناسب‌تر است؟",
        "options": [
            "Excel",
            "Paint",
            "Notepad",
            "Browser"
        ],
        "correct": 0,
    },

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "language",
        "question": "معنی کلمه Bank در زمینه مالی چیست؟",
        "options": [
            "بازار",
            "بانک",
            "فروشگاه",
            "شرکت"
        ],
        "correct": 1,
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "category": "intelligence",
        "question": "اگر عدد 2 برابر شود و سپس 3 واحد به آن اضافه شود، حاصل برای عدد 5 چیست؟",
        "options": [
            "10",
            "11",
            "13",
            "15"
        ],
        "correct": 1,
    },

    # =====================================================
    # حسابداری
    # =====================================================

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "accounting",
        "question": "کدام گزینه در معادله حسابداری قرار دارد؟",
        "options": [
            "دارایی",
            "فقط فروش",
            "فقط هزینه",
            "فقط مالیات"
        ],
        "correct": 0,
    },

    {
        "bank": "government",
        "difficulty": "medium",
        "category": "accounting",
        "question": "معادله اساسی حسابداری کدام است؟",
        "options": [
            "دارایی = بدهی + سرمایه",
            "دارایی = فروش + هزینه",
            "سرمایه = فروش - دارایی",
            "بدهی = دارایی + سرمایه"
        ],
        "correct": 0,
    },

    # =====================================================
    # مدیریت
    # =====================================================

    {
        "bank": "government",
        "difficulty": "easy",
        "category": "management",
        "question": "کدام مورد یکی از وظایف اصلی مدیریت است؟",
        "options": [
            "برنامه‌ریزی",
            "حذف کارکنان",
            "حذف اهداف",
            "عدم کنترل"
        ],
        "correct": 0,
    },

    {
        "bank": "government",
        "difficulty": "hard",
        "category": "management",
        "question": "کنترل در مدیریت عمدتاً با چه هدفی انجام می‌شود؟",
        "options": [
            "مقایسه عملکرد با اهداف و اصلاح انحرافات",
            "حذف برنامه‌ریزی",
            "افزایش بی‌هدف هزینه‌ها",
            "کاهش اطلاعات"
        ],
        "correct": 0,
    },

]


# =========================================================
# وضعیت آزمون کاربر
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
            "simulation": False,
        }

    return context.user_data["employment_exam"]


# =========================================================
# منوی اصلی آزمون
# =========================================================

def employment_exam_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🏦 بانک رفاه",
                callback_data="employment_category_refah"
            ),
            InlineKeyboardButton(
                "🏙️ بانک شهر",
                callback_data="employment_category_shahr"
            ),
        ],

        [
            InlineKeyboardButton(
                "🏦 بانک مهر",
                callback_data="employment_category_mehr"
            ),
            InlineKeyboardButton(
                "🏛️ بانک‌های دولتی",
                callback_data="employment_category_government"
            ),
        ],

        [
            InlineKeyboardButton(
                "🟢 سطح آسان",
                callback_data="employment_difficulty_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 سطح متوسط",
                callback_data="employment_difficulty_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سطح سخت",
                callback_data="employment_difficulty_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "🏆 آزمون شبیه‌سازی‌شده",
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
# متن اصلی
# =========================================================

def employment_exam_text():

    return f"""
📝 آزمون استخدامی

🏛️ اندیشکده مدیریت و بازار

━━━━━━━━━━━━━━━━━━

🎯 بانک جامع سؤال استخدامی

🏦 بانک رفاه
🏙️ بانک شهر
🏦 بانک مهر
🏛️ بانک‌های دولتی

━━━━━━━━━━━━━━━━━━

📊 سطح‌بندی:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

📚 موضوعات:

🏦 بانکداری
💰 اقتصاد
📚 مدیریت
🧮 حسابداری
💻 ICDL
🧠 هوش
🇬🇧 زبان
📖 عمومی

━━━━━━━━━━━━━━━━━━

📊 تعداد سؤال فعلی:
{len(EMPLOYMENT_QUESTIONS)}

━━━━━━━━━━━━━━━━━━

🏆 آزمون شبیه‌سازی‌شده نیز
در دسترس است.
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
# CALLBACK دسته‌بندی
#
# این همان تابعی است که bot.py فعلی
# به دنبال آن می‌گردد.
# =========================================================

async def employment_exam_category_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    category = query.data.replace(
        "employment_category_",
        ""
    )

    if category not in BANK_CATEGORIES:

        await query.edit_message_text(
            "❌ دسته‌بندی انتخاب‌شده معتبر نیست.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = [
        q
        for q in EMPLOYMENT_QUESTIONS
        if q["bank"] == category
    ]

    bank_name = BANK_CATEGORIES[category]

    if not questions:

        await query.edit_message_text(
            f"""
❌ برای {bank_name}
هنوز سؤال ثبت نشده است.
""",
            reply_markup=employment_exam_menu()
        )

        return

    # -----------------------------------------------------
    # ذخیره آزمون
    # -----------------------------------------------------

    context.user_data["employment_exam"] = {
        "questions": questions,
        "index": 0,
        "score": 0,
        "answered": False,
        "simulation": False,
    }

    await show_question(
        query,
        context
    )


# =========================================================
# انتخاب بانک
#
# نام جایگزین برای سازگاری بیشتر
# =========================================================

async def employment_bank_callback(
    update,
    context
):

    return await employment_exam_category_callback(
        update,
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
            "❌ سطح انتخاب‌شده معتبر نیست.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = [
        q
        for q in EMPLOYMENT_QUESTIONS
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
        "simulation": False,
    }

    await show_question(
        query,
        context
    )


# =========================================================
# آزمون شبیه‌سازی‌شده
# =========================================================

async def employment_simulation_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

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

    category = CATEGORY_NAMES.get(
        question["category"],
        ""
    )

    text = f"""
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🏦 {bank_name}

📚 موضوع: {category}

📊 سطح: {difficulty}

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

📚 پاسخ درست را یاد بگیرید.
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

🎯 مسیر پیشنهادی:

📖 مطالعه
+
📝 تست
+
🔍 تحلیل اشتباهات
+
🔄 مرور
+
🏆 آزمون شبیه‌سازی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
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
                "🏆 آزمون شبیه‌سازی",
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
# توابع آماری
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
            q
            for q in EMPLOYMENT_QUESTIONS
            if q["bank"] == bank
        ]
    )


def get_difficulty_question_count(
    difficulty
):

    return len(
        [
            q
            for q in EMPLOYMENT_QUESTIONS
            if q["difficulty"] == difficulty
        ]
    )


def get_category_question_count(
    category
):

    return len(
        [
            q
            for q in EMPLOYMENT_QUESTIONS
            if q["category"] == category
        ]
    )


# =========================================================
# پایان employment_exam.py
# =========================================================
