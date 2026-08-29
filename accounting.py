# =========================================================
# ACCOUNTING MODULE
# =========================================================

ACCOUNTING_QUESTIONS = [

    {
        "question": "کدام گزینه معادله اصلی حسابداری را نشان می‌دهد؟",
        "options": [
            "دارایی = بدهی + سرمایه",
            "دارایی = درآمد + هزینه",
            "سرمایه = دارایی + بدهی",
            "بدهی = دارایی + سرمایه",
        ],
        "correct": 0,
    },

    {
        "question": "کدام مورد جزء دارایی‌های جاری است؟",
        "options": [
            "زمین",
            "ساختمان",
            "موجودی کالا",
            "سرمایه",
        ],
        "correct": 2,
    },

    {
        "question": "حساب صندوق در کدام گروه قرار می‌گیرد؟",
        "options": [
            "دارایی",
            "بدهی",
            "سرمایه",
            "درآمد",
        ],
        "correct": 0,
    },

    {
        "question": "خرید کالا به صورت نقدی چه اثری دارد؟",
        "options": [
            "افزایش دارایی و افزایش بدهی",
            "افزایش یک دارایی و کاهش دارایی دیگر",
            "کاهش سرمایه",
            "افزایش درآمد",
        ],
        "correct": 1,
    },

    {
        "question": "کدام گزینه نمونه‌ای از بدهی است؟",
        "options": [
            "صندوق",
            "بانک",
            "حساب‌های پرداختنی",
            "موجودی کالا",
        ],
        "correct": 2,
    },

    {
        "question": "صورت سود و زیان برای چه منظوری تهیه می‌شود؟",
        "options": [
            "محاسبه دارایی‌ها",
            "تعیین سود یا زیان دوره",
            "ثبت موجودی نقد",
            "محاسبه بدهی‌ها",
        ],
        "correct": 1,
    },

    {
        "question": "اگر درآمد از هزینه بیشتر باشد، نتیجه چیست؟",
        "options": [
            "زیان",
            "سود",
            "بدهی",
            "کاهش دارایی",
        ],
        "correct": 1,
    },

    {
        "question": "کدام مورد جزء صورت‌های مالی اساسی است؟",
        "options": [
            "صورت وضعیت مالی",
            "دفتر روزنامه",
            "دفتر کل",
            "سند حسابداری",
        ],
        "correct": 0,
    },

    {
        "question": "ثبت افزایش دارایی معمولاً در کدام طرف حساب انجام می‌شود؟",
        "options": [
            "بستانکار",
            "بدهکار",
            "سرمایه",
            "تراز",
        ],
        "correct": 1,
    },

    {
        "question": "ثبت افزایش بدهی معمولاً در کدام طرف حساب انجام می‌شود؟",
        "options": [
            "بدهکار",
            "بستانکار",
            "هزینه",
            "دارایی",
        ],
        "correct": 1,
    },

]


# =========================================================
# ACCOUNTING MENU
# =========================================================

def accounting_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📚 آموزش حسابداری",
                callback_data="accounting_lessons"
            )
        ],

        [
            InlineKeyboardButton(
                "📖 مفاهیم پایه",
                callback_data="accounting_concepts"
            )
        ],

        [
            InlineKeyboardButton(
                "🧮 ثبت‌های حسابداری",
                callback_data="accounting_entries"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 صورت‌های مالی",
                callback_data="accounting_financial_statements"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 حسابداری مالی",
                callback_data="accounting_financial"
            )
        ],

        [
            InlineKeyboardButton(
                "🏢 حسابداری شرکت‌ها",
                callback_data="accounting_companies"
            )
        ],

        [
            InlineKeyboardButton(
                "🧾 مالیات و حسابداری",
                callback_data="accounting_tax"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون حسابداری",
                callback_data="accounting_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ])


# =========================================================
# ACCOUNTING MAIN TEXT
# =========================================================

def accounting_text():

    return """
🧾 حسابداری

━━━━━━━━━━━━━━━━━━

📚 آموزش تخصصی حسابداری

حسابداری فرآیند شناسایی، ثبت، طبقه‌بندی،
خلاصه‌سازی و گزارش اطلاعات مالی است.

━━━━━━━━━━━━━━━━━━

🎯 سرفصل‌های حسابداری:

📖 مفاهیم پایه
🧮 ثبت‌های حسابداری
📊 صورت‌های مالی
💰 حسابداری مالی
🏢 حسابداری شرکت‌ها
🧾 مالیات و حسابداری
📝 آزمون حسابداری

━━━━━━━━━━━━━━━━━━

📌 مناسب برای:

🎓 دانشجویان مدیریت و حسابداری
💼 کارجویان
🏦 داوطلبان آزمون‌های استخدامی
📚 علاقه‌مندان به امور مالی
"""


# =========================================================
# ACCOUNTING CALLBACK
# =========================================================

async def accounting_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        accounting_text(),
        reply_markup=accounting_menu()
    )


# =========================================================
# ACCOUNTING LESSONS
# =========================================================

def accounting_lessons_text():

    return """
📚 آموزش حسابداری

━━━━━━━━━━━━━━━━━━

1️⃣ حسابداری چیست؟

حسابداری فرآیند ثبت، طبقه‌بندی،
تلخیص و گزارش رویدادهای مالی است.

━━━━━━━━━━━━━━━━━━

2️⃣ هدف حسابداری

ارائه اطلاعات مالی قابل استفاده برای
تصمیم‌گیری مدیران، سرمایه‌گذاران،
طلبکاران و سایر استفاده‌کنندگان.

━━━━━━━━━━━━━━━━━━

3️⃣ معادله حسابداری

دارایی = بدهی + سرمایه

━━━━━━━━━━━━━━━━━━

4️⃣ عناصر اصلی

💰 دارایی
💳 بدهی
👤 سرمایه
📈 درآمد
💸 هزینه

━━━━━━━━━━━━━━━━━━

📌 این مفاهیم پایه، اساس یادگیری
حسابداری هستند.
"""


# =========================================================
# ACCOUNTING CONCEPTS
# =========================================================

def accounting_concepts_text():

    return """
📖 مفاهیم پایه حسابداری

━━━━━━━━━━━━━━━━━━

💰 دارایی

منابع اقتصادی تحت کنترل واحد تجاری
که دارای منافع اقتصادی آتی هستند.

مثال:

• صندوق
• بانک
• موجودی کالا
• حساب‌های دریافتنی
• ساختمان
• تجهیزات

━━━━━━━━━━━━━━━━━━

💳 بدهی

تعهدات واحد تجاری در برابر اشخاص
و واحدهای دیگر.

مثال:

• حساب‌های پرداختنی
• وام پرداختنی
• اسناد پرداختنی

━━━━━━━━━━━━━━━━━━

👤 سرمایه

حقوق مالک نسبت به دارایی‌های واحد تجاری.

━━━━━━━━━━━━━━━━━━

📈 درآمد

افزایش منافع اقتصادی ناشی از فعالیت‌های
واحد تجاری.

━━━━━━━━━━━━━━━━━━

💸 هزینه

کاهش منافع اقتصادی برای ایجاد درآمد.
"""


# =========================================================
# ACCOUNTING ENTRIES
# =========================================================

def accounting_entries_text():

    return """
🧮 ثبت‌های حسابداری

━━━━━━━━━━━━━━━━━━

هر رویداد مالی باید در سیستم حسابداری
به صورت بدهکار و بستانکار ثبت شود.

━━━━━━━━━━━━━━━━━━

📌 مثال:

خرید تجهیزات به صورت نقدی

تجهیزات ← بدهکار
صندوق ← بستانکار

━━━━━━━━━━━━━━━━━━

📌 مثال:

دریافت وجه از مشتری

صندوق ← بدهکار
حساب‌های دریافتنی ← بستانکار

━━━━━━━━━━━━━━━━━━

📌 مثال:

پرداخت بدهی به فروشنده

حساب‌های پرداختنی ← بدهکار
صندوق ← بستانکار

━━━━━━━━━━━━━━━━━━

🎯 اصل مهم:

جمع مبالغ بدهکار
=
جمع مبالغ بستانکار
"""


# =========================================================
# FINANCIAL STATEMENTS
# =========================================================

def accounting_financial_statements_text():

    return """
📊 صورت‌های مالی

━━━━━━━━━━━━━━━━━━

صورت‌های مالی اطلاعات مالی یک واحد
تجاری را به شکل منظم ارائه می‌کنند.

━━━━━━━━━━━━━━━━━━

📋 مهم‌ترین صورت‌ها:

1️⃣ صورت وضعیت مالی

نمایش دارایی‌ها، بدهی‌ها و حقوق مالکانه.

━━━━━━━━━━━━━━━━━━

2️⃣ صورت سود و زیان

نمایش درآمدها و هزینه‌ها و تعیین سود
یا زیان دوره.

━━━━━━━━━━━━━━━━━━

3️⃣ صورت جریان وجوه نقد

نمایش جریان‌های ورود و خروج وجه نقد.

━━━━━━━━━━━━━━━━━━

4️⃣ صورت تغییرات حقوق مالکانه

نمایش تغییرات حقوق مالکانه در دوره مالی.
"""


# =========================================================
# FINANCIAL ACCOUNTING
# =========================================================

def accounting_financial_text():

    return """
💰 حسابداری مالی

━━━━━━━━━━━━━━━━━━

حسابداری مالی بر ثبت و گزارش اطلاعات
مالی برای استفاده‌کنندگان داخل و خارج
از واحد تجاری تمرکز دارد.

━━━━━━━━━━━━━━━━━━

🎯 موضوعات مهم:

• ثبت معاملات
• تهیه صورت‌های مالی
• حساب‌های دریافتنی
• حساب‌های پرداختنی
• موجودی کالا
• دارایی‌های ثابت
• استهلاک
• درآمد
• هزینه
"""


# =========================================================
# COMPANY ACCOUNTING
# =========================================================

def accounting_companies_text():

    return """
🏢 حسابداری شرکت‌ها

━━━━━━━━━━━━━━━━━━

در حسابداری شرکت‌ها، معاملات و
رویدادهای مالی شرکت ثبت و گزارش می‌شوند.

━━━━━━━━━━━━━━━━━━

📌 موضوعات مهم:

• سرمایه شرکت
• افزایش سرمایه
• کاهش سرمایه
• سود و زیان
• تقسیم سود
• حساب جاری شرکا
• دارایی‌های شرکت
• بدهی‌های شرکت
• صورت‌های مالی
"""


# =========================================================
# TAX ACCOUNTING
# =========================================================

def accounting_tax_text():

    return """
🧾 مالیات و حسابداری

━━━━━━━━━━━━━━━━━━

حسابداری و مالیات ارتباط نزدیکی
با یکدیگر دارند.

━━━━━━━━━━━━━━━━━━

📌 موضوعات مهم:

• درآمد مشمول مالیات
• هزینه‌های قابل قبول
• اظهارنامه مالیاتی
• اسناد و مدارک مالی
• مالیات بر ارزش افزوده
• تکالیف مالیاتی
• نگهداری سوابق حسابداری

━━━━━━━━━━━━━━━━━━

⚠️ قوانین مالیاتی ممکن است تغییر کنند.
برای تصمیم‌گیری عملی باید مقررات
روز بررسی شود.
"""


# =========================================================
# ACCOUNTING SUBSECTION CALLBACK
# =========================================================

async def accounting_subsection_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    section = query.data

    texts = {

        "accounting_lessons":
            accounting_lessons_text(),

        "accounting_concepts":
            accounting_concepts_text(),

        "accounting_entries":
            accounting_entries_text(),

        "accounting_financial_statements":
            accounting_financial_statements_text(),

        "accounting_financial":
            accounting_financial_text(),

        "accounting_companies":
            accounting_companies_text(),

        "accounting_tax":
            accounting_tax_text(),

    }

    text = texts.get(
        section,
        "❌ این بخش وجود ندارد."
    )

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🧾 حسابداری",
                callback_data="accounting"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ])

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


# =========================================================
# ACCOUNTING EXAM START
# =========================================================

async def accounting_exam_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        f"""
📝 آزمون حسابداری

━━━━━━━━━━━━━━━━━━

🎯 تعداد سؤالات:

{len(ACCOUNTING_QUESTIONS)} سؤال

📌 سطح:

عمومی + مفهومی

📌 هر سؤال:

چهار گزینه‌ای

━━━━━━━━━━━━━━━━━━

👇 برای شروع آزمون روی گزینه
زیر کلیک کنید:
""",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🚀 شروع آزمون",
                    callback_data="accounting_exam_0_0"
                )
            ],

            [
                InlineKeyboardButton(
                    "🧾 حسابداری",
                    callback_data="accounting"
                )
            ],

        ])
    )


# =========================================================
# ACCOUNTING EXAM QUESTION
# =========================================================

async def accounting_exam_question_callback(
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
            "⚠️ خطا در اطلاعات آزمون حسابداری.",
            reply_markup=accounting_menu()
        )

        return

    if index >= len(ACCOUNTING_QUESTIONS):

        await show_accounting_result(
            query,
            score
        )

        return

    question = ACCOUNTING_QUESTIONS[index]

    text = f"""
📝 آزمون حسابداری

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1}
از {len(ACCOUNTING_QUESTIONS)}

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

        keyboard.append([

            InlineKeyboardButton(
                option,
                callback_data=(
                    f"accounting_answer_"
                    f"{index}_"
                    f"{option_index}_"
                    f"{score}"
                )
            )

        ])

    keyboard.append([

        InlineKeyboardButton(
            "🧾 خروج از آزمون",
            callback_data="accounting"
        )

    ])

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================================================
# ACCOUNTING ANSWER
# =========================================================

async def accounting_answer_callback(
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
            "⚠️ خطا در پردازش پاسخ حسابداری.",
            reply_markup=accounting_menu()
        )

        return

    question = ACCOUNTING_QUESTIONS[index]

    correct = question["correct"]

    if selected == correct:

        score += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی: {score}
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

    if next_index < len(ACCOUNTING_QUESTIONS):

        keyboard = [

            [

                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"accounting_exam_"
                        f"{next_index}_"
                        f"{score}"
                    )
                )

            ],

            [

                InlineKeyboardButton(
                    "🧾 خروج از آزمون",
                    callback_data="accounting"
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

        await show_accounting_result(
            query,
            score
        )


# =========================================================
# ACCOUNTING RESULT
# =========================================================

async def show_accounting_result(
    query,
    score
):

    total = len(
        ACCOUNTING_QUESTIONS
    )

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
🏁 آزمون حسابداری به پایان رسید.

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
                callback_data="accounting_exam_0_0"
            )

        ],

        [

            InlineKeyboardButton(
                "📚 آموزش حسابداری",
                callback_data="accounting_lessons"
            )

        ],

        [

            InlineKeyboardButton(
                "🧾 حسابداری",
                callback_data="accounting"
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
