# =========================================================
# employment_exam.py
# 📝 سیستم آزمون استخدامی
# 🏛️ اندیشکده مدیریت و بازار
#
# نسخه حرفه‌ای:
# • دسته‌بندی بانک‌ها
# • بانک رفاه کارگران
# • بانک شهر
# • بانک مهر ایران
# • بانک‌های دولتی
# • سطح آسان / متوسط / سخت
# • آزمون موضوعی
# • آزمون شبیه‌سازی‌شده
# • سیستم امتیازدهی
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# BANK CATEGORIES
# =========================================================

BANK_CATEGORIES = {
    "refah": "🏦 بانک رفاه کارگران",
    "shahr": "🏙️ بانک شهر",
    "mehr": "🤝 بانک مهر ایران",
    "government": "🏛️ بانک‌های دولتی",
}


# =========================================================
# DIFFICULTY
# =========================================================

DIFFICULTY_NAMES = {
    "easy": "🟢 آسان",
    "medium": "🟡 متوسط",
    "hard": "🔴 سخت",
}


# =========================================================
# QUESTION BANK
#
# ساختار:
#
# {
#     "question": "...",
#     "options": [...],
#     "correct": 0,
#     "difficulty": "easy",
#     "category": "general"
# }
# =========================================================

EMPLOYMENT_QUESTIONS = {

    # =====================================================
    # GENERAL
    # =====================================================

    "general": [

        {
            "question": "کدام مورد از وظایف اصلی بانک‌ها محسوب می‌شود؟",
            "options": [
                "جمع‌آوری سپرده‌ها و اعطای تسهیلات",
                "تولید کالا",
                "تولید نفت",
                "تعیین مالیات"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "کدام گزینه نمونه‌ای از دارایی بانک است؟",
            "options": [
                "سپرده مشتریان",
                "تسهیلات اعطایی",
                "سرمایه پرداخت‌نشده",
                "بدهی به بانک مرکزی"
            ],
            "correct": 1,
            "difficulty": "medium"
        },

        {
            "question": "نقدینگی معمولاً شامل کدام موارد است؟",
            "options": [
                "فقط اسکناس",
                "فقط سکه",
                "پول و شبه‌پول",
                "فقط ارز خارجی"
            ],
            "correct": 2,
            "difficulty": "easy"
        },

        {
            "question": "کدام نهاد مسئول سیاست‌گذاری پولی در ایران است؟",
            "options": [
                "وزارت صمت",
                "بانک مرکزی",
                "سازمان امور مالیاتی",
                "اتاق بازرگانی"
            ],
            "correct": 1,
            "difficulty": "easy"
        },

        {
            "question": "افزایش نرخ بهره معمولاً چه اثری بر هزینه استقراض دارد؟",
            "options": [
                "کاهش می‌دهد",
                "افزایش می‌دهد",
                "هیچ اثری ندارد",
                "آن را حذف می‌کند"
            ],
            "correct": 1,
            "difficulty": "medium"
        },

        {
            "question": "کدام مورد می‌تواند ریسک اعتباری بانک را افزایش دهد؟",
            "options": [
                "کاهش مطالبات معوق",
                "افزایش بازپرداخت تسهیلات",
                "افزایش نکول تسهیلات‌گیرندگان",
                "افزایش سرمایه بانک"
            ],
            "correct": 2,
            "difficulty": "medium"
        },

        {
            "question": "کدام گزینه به مفهوم تورم نزدیک‌تر است؟",
            "options": [
                "کاهش عمومی قیمت‌ها",
                "افزایش مستمر و عمومی سطح قیمت‌ها",
                "افزایش تولید",
                "افزایش صادرات"
            ],
            "correct": 1,
            "difficulty": "easy"
        },

        {
            "question": "کدام گزینه از منابع اصلی بانک محسوب می‌شود؟",
            "options": [
                "سپرده‌های مشتریان",
                "تسهیلات پرداخت‌شده",
                "مطالبات مشکوک‌الوصول",
                "دارایی ثابت"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "کدام گزینه معمولاً نشان‌دهنده توان پرداخت تعهدات کوتاه‌مدت است؟",
            "options": [
                "نقدینگی",
                "تبلیغات",
                "فروش",
                "بازاریابی"
            ],
            "correct": 0,
            "difficulty": "medium"
        },

        {
            "question": "کدام مورد می‌تواند موجب کاهش سودآوری بانک شود؟",
            "options": [
                "افزایش درآمدهای سالم",
                "کاهش هزینه‌ها",
                "افزایش مطالبات معوق",
                "افزایش بهره‌وری"
            ],
            "correct": 2,
            "difficulty": "medium"
        },
    ],


    # =====================================================
    # BANKING
    # =====================================================

    "banking": [

        {
            "question": "سپرده دیداری چه ویژگی مهمی دارد؟",
            "options": [
                "امکان برداشت طبق شرایط حساب",
                "عدم امکان برداشت",
                "فقط برای بانک مرکزی است",
                "صرفاً ارزی است"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "کدام مورد از ریسک‌های مهم بانکی است؟",
            "options": [
                "ریسک اعتباری",
                "ریسک رنگ سازمانی",
                "ریسک تبلیغات تلویزیونی",
                "ریسک طراحی لوگو"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "ریسک نقدینگی به چه معناست؟",
            "options": [
                "ناتوانی در ایفای تعهدات در سررسید",
                "افزایش فروش",
                "افزایش مشتری",
                "افزایش سرمایه"
            ],
            "correct": 0,
            "difficulty": "medium"
        },

        {
            "question": "کدام گزینه بیشتر به ریسک عملیاتی مربوط است؟",
            "options": [
                "نقص فرآیندها و سیستم‌ها",
                "افزایش صادرات",
                "کاهش نرخ تورم",
                "افزایش سرمایه"
            ],
            "correct": 0,
            "difficulty": "medium"
        },

        {
            "question": "نسبت کفایت سرمایه در مدیریت بانک بیشتر با چه موضوعی مرتبط است؟",
            "options": [
                "توان بانک در پوشش ریسک‌ها",
                "تعداد شعب",
                "تعداد کارکنان",
                "تعداد مشتریان"
            ],
            "correct": 0,
            "difficulty": "hard"
        },
    ],


    # =====================================================
    # ACCOUNTING
    # =====================================================

    "accounting": [

        {
            "question": "معادله اصلی حسابداری کدام است؟",
            "options": [
                "دارایی = بدهی + سرمایه",
                "دارایی = درآمد + هزینه",
                "سرمایه = هزینه + درآمد",
                "بدهی = دارایی + درآمد"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "کدام مورد در سمت بدهکار ترازنامه قرار می‌گیرد؟",
            "options": [
                "دارایی",
                "بدهی",
                "سرمایه",
                "درآمد"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "افزایش بدهی معمولاً در کدام سمت ثبت می‌شود؟",
            "options": [
                "بدهکار",
                "بستانکار",
                "هر دو",
                "هیچ‌کدام"
            ],
            "correct": 1,
            "difficulty": "medium"
        },

        {
            "question": "صورت سود و زیان بیشتر چه چیزی را نشان می‌دهد؟",
            "options": [
                "عملکرد درآمد و هزینه طی دوره",
                "فقط دارایی‌ها",
                "فقط بدهی‌ها",
                "فقط موجودی نقد"
            ],
            "correct": 0,
            "difficulty": "easy"
        },
    ],


    # =====================================================
    # ECONOMICS
    # =====================================================

    "economics": [

        {
            "question": "قانون تقاضا در شرایط برابر چه رابطه‌ای را بیان می‌کند؟",
            "options": [
                "افزایش قیمت معمولاً کاهش مقدار تقاضا را به دنبال دارد",
                "افزایش قیمت همیشه تقاضا را دو برابر می‌کند",
                "کاهش قیمت همیشه عرضه را کاهش می‌دهد",
                "قیمت هیچ ارتباطی با تقاضا ندارد"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "سیاست پولی عمدتاً توسط چه نهادی اجرا می‌شود؟",
            "options": [
                "بانک مرکزی",
                "وزارت صمت",
                "شهرداری",
                "اتاق بازرگانی"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "سیاست مالی بیشتر به چه موضوعی مربوط است؟",
            "options": [
                "مخارج و درآمدهای دولت",
                "نرخ ارز صرافی",
                "مدیریت شعب بانک",
                "حسابداری شرکت"
            ],
            "correct": 0,
            "difficulty": "medium"
        },

        {
            "question": "GDP چه چیزی را اندازه‌گیری می‌کند؟",
            "options": [
                "ارزش کالاها و خدمات نهایی تولیدشده",
                "کل ثروت خانوارها",
                "کل پول نقد",
                "کل صادرات"
            ],
            "correct": 0,
            "difficulty": "medium"
        },
    ],


    # =====================================================
    # LAW
    # =====================================================

    "law": [

        {
            "question": "قرارداد در ساده‌ترین تعریف چیست؟",
            "options": [
                "توافق اراده‌ها برای ایجاد اثر حقوقی",
                "صرفاً یک نامه",
                "یک پیام تبلیغاتی",
                "یک سند بانکی"
            ],
            "correct": 0,
            "difficulty": "medium"
        },

        {
            "question": "کدام گزینه از ارکان عمومی قرارداد است؟",
            "options": [
                "قصد و رضا",
                "تبلیغات",
                "سود شرکت",
                "تعداد کارکنان"
            ],
            "correct": 0,
            "difficulty": "medium"
        },
    ],


    # =====================================================
    # ENGLISH
    # =====================================================

    "english": [

        {
            "question": "Choose the correct meaning of 'Bank'.",
            "options": [
                "بانک",
                "بازار",
                "بیمه",
                "مالیات"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "Choose the correct meaning of 'Interest Rate'.",
            "options": [
                "نرخ ارز",
                "نرخ بهره",
                "نرخ تورم",
                "نرخ مالیات"
            ],
            "correct": 1,
            "difficulty": "easy"
        },

        {
            "question": "Choose the correct option: 'The bank ___ loans.'",
            "options": [
                "provide",
                "provides",
                "providing",
                "provided"
            ],
            "correct": 1,
            "difficulty": "medium"
        },
    ],


    # =====================================================
    # ICDL
    # =====================================================

    "icdl": [

        {
            "question": "کدام نرم‌افزار برای پردازش متن استفاده می‌شود؟",
            "options": [
                "Microsoft Word",
                "Calculator",
                "Paint",
                "Notepad فقط برای محاسبات"
            ],
            "correct": 0,
            "difficulty": "easy"
        },

        {
            "question": "کلید میانبر Copy در ویندوز چیست؟",
            "options": [
                "Ctrl + X",
                "Ctrl + C",
                "Ctrl + V",
                "Ctrl + Z"
            ],
            "correct": 1,
            "difficulty": "easy"
        },

        {
            "question": "کلید میانبر Undo کدام است؟",
            "options": [
                "Ctrl + A",
                "Ctrl + S",
                "Ctrl + Z",
                "Ctrl + P"
            ],
            "correct": 2,
            "difficulty": "easy"
        },
    ],
}


# =========================================================
# BANK-SPECIFIC QUESTIONS
# =========================================================

BANK_SPECIFIC_QUESTIONS = {

    "refah": [
        {
            "question": "بانک رفاه کارگران بیشتر با چه جامعه‌ای پیوند تاریخی دارد؟",
            "options": [
                "کارگران و تأمین اجتماعی",
                "صنعت نفت فقط",
                "شهرداری‌ها",
                "صرافی‌ها"
            ],
            "correct": 0,
            "difficulty": "easy"
        }
    ],

    "shahr": [
        {
            "question": "بانک شهر در چه حوزه‌ای ارتباط ویژه‌ای با مدیریت شهری دارد؟",
            "options": [
                "خدمات و تأمین مالی مرتبط با شهر و مدیریت شهری",
                "کشاورزی فقط",
                "صنعت هوافضا",
                "تولید خودرو"
            ],
            "correct": 0,
            "difficulty": "easy"
        }
    ],

    "mehr": [
        {
            "question": "بانک مهر ایران در چه حوزه‌ای شناخته‌شده است؟",
            "options": [
                "بانکداری قرض‌الحسنه",
                "بانکداری سرمایه‌گذاری صرف",
                "تولید صنعتی",
                "بیمه"
            ],
            "correct": 0,
            "difficulty": "easy"
        }
    ],

    "government": [
        {
            "question": "بانک‌های دولتی تحت مالکیت چه نهادی قرار دارند؟",
            "options": [
                "دولت",
                "شهرداری",
                "شرکت خصوصی",
                "اشخاص حقیقی"
            ],
            "correct": 0,
            "difficulty": "easy"
        }
    ],
}


# =========================================================
# HELPERS
# =========================================================

def employment_exam_categories():

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
                "🤝 بانک مهر ایران",
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
                "📚 آزمون جامع",
                callback_data="employment_full_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 شبیه‌سازی آزمون واقعی",
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
# MAIN INTRO
# =========================================================

def employment_exam_text():

    return """
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

سیستم حرفه‌ای آمادگی آزمون‌های استخدامی

━━━━━━━━━━━━━━━━━━

🏦 بانک رفاه کارگران
🏙️ بانک شهر
🤝 بانک مهر ایران
🏛️ بانک‌های دولتی

━━━━━━━━━━━━━━━━━━

📚 دسته‌بندی موضوعی:

• بانکداری
• اقتصاد
• حسابداری
• حقوق
• زبان انگلیسی
• ICDL
• اطلاعات عمومی

━━━━━━━━━━━━━━━━━━

🎯 سطوح:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

👇 نوع آزمون را انتخاب کنید.
"""


# =========================================================
# REQUIRED FUNCTION
# employment_exam_callback
# =========================================================

async def employment_exam_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        employment_exam_text(),
        reply_markup=employment_exam_categories()
    )


# =========================================================
# BANK MENU
# =========================================================

def bank_exam_menu(bank):

    bank_name = BANK_CATEGORIES.get(
        bank,
        "آزمون بانکی"
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 سطح آسان",
                callback_data=f"employment_level_{bank}_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 سطح متوسط",
                callback_data=f"employment_level_{bank}_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سطح سخت",
                callback_data=f"employment_level_{bank}_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 آزمون جامع بانک",
                callback_data=f"employment_bank_exam_{bank}"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 شبیه‌سازی آزمون",
                callback_data=f"employment_sim_{bank}"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="employment_exam"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


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

    bank_name = BANK_CATEGORIES.get(
        bank,
        "بانک"
    )

    text = f"""
📝 آزمون استخدامی

{bank_name}

━━━━━━━━━━━━━━━━━━

سطح موردنظر خود را انتخاب کنید:

🟢 آسان
🟡 متوسط
🔴 سخت

یا یک آزمون جامع را شروع کنید.

━━━━━━━━━━━━━━━━━━
"""

    await query.edit_message_text(
        text,
        reply_markup=bank_exam_menu(bank)
    )


# =========================================================
# QUESTION BUILDER
# =========================================================

def get_questions(
    category=None,
    difficulty=None,
    bank=None
):

    questions = []

    if category:

        questions.extend(
            EMPLOYMENT_QUESTIONS.get(
                category,
                []
            )
        )

    else:

        for values in EMPLOYMENT_QUESTIONS.values():

            questions.extend(values)

    if bank:

        questions.extend(
            BANK_SPECIFIC_QUESTIONS.get(
                bank,
                []
            )
        )

    if difficulty:

        questions = [
            q for q in questions
            if q.get("difficulty") == difficulty
        ]

    return questions


# =========================================================
# LEVEL CALLBACK
# =========================================================

async def employment_level_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    parts = query.data.split("_")

    if len(parts) < 4:

        await query.edit_message_text(
            "❌ اطلاعات آزمون نامعتبر است.",
            reply_markup=employment_exam_categories()
        )

        return

    bank = parts[2]
    difficulty = parts[3]

    questions = get_questions(
        difficulty=difficulty,
        bank=bank
    )

    if not questions:

        await query.edit_message_text(
            "❌ هنوز سؤال کافی برای این سطح ثبت نشده است.",
            reply_markup=bank_exam_menu(bank)
        )

        return

    questions = questions[:10]

    context.user_data["employment_questions"] = questions
    context.user_data["employment_index"] = 0
    context.user_data["employment_score"] = 0
    context.user_data["employment_bank"] = bank

    await send_employment_question(
        query,
        context
    )


# =========================================================
# GENERAL FULL EXAM
# =========================================================

async def employment_full_exam_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    questions = get_questions()

    questions = questions[:20]

    context.user_data["employment_questions"] = questions
    context.user_data["employment_index"] = 0
    context.user_data["employment_score"] = 0
    context.user_data["employment_bank"] = None

    await send_employment_question(
        query,
        context
    )


# =========================================================
# SIMULATION
# =========================================================

async def employment_simulation_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    questions = get_questions()

    questions = questions[:30]

    context.user_data["employment_questions"] = questions
    context.user_data["employment_index"] = 0
    context.user_data["employment_score"] = 0
    context.user_data["employment_bank"] = None
    context.user_data["employment_simulation"] = True

    await send_employment_question(
        query,
        context
    )


# =========================================================
# BANK EXAM
# =========================================================

async def employment_bank_exam_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    bank = query.data.replace(
        "employment_bank_exam_",
        ""
    )

    questions = get_questions(
        bank=bank
    )

    questions = questions[:20]

    context.user_data["employment_questions"] = questions
    context.user_data["employment_index"] = 0
    context.user_data["employment_score"] = 0
    context.user_data["employment_bank"] = bank

    await send_employment_question(
        query,
        context
    )


# =========================================================
# BANK SIMULATION
# =========================================================

async def employment_bank_simulation_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    bank = query.data.replace(
        "employment_sim_",
        ""
    )

    questions = get_questions(
        bank=bank
    )

    questions = questions[:30]

    context.user_data["employment_questions"] = questions
    context.user_data["employment_index"] = 0
    context.user_data["employment_score"] = 0
    context.user_data["employment_bank"] = bank
    context.user_data["employment_simulation"] = True

    await send_employment_question(
        query,
        context
    )


# =========================================================
# SEND QUESTION
# =========================================================

async def send_employment_question(
    query,
    context
):

    questions = context.user_data.get(
        "employment_questions",
        []
    )

    index = context.user_data.get(
        "employment_index",
        0
    )

    score = context.user_data.get(
        "employment_score",
        0
    )

    if index >= len(questions):

        await employment_result(
            query,
            context
        )

        return

    question = questions[index]

    text = f"""
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز: {score}

📊 سطح:
{DIFFICULTY_NAMES.get(
    question.get("difficulty"),
    "نامشخص"
)}

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
                "🚪 خروج از آزمون",
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
            reply_markup=employment_exam_categories()
        )

        return

    questions = context.user_data.get(
        "employment_questions",
        []
    )

    if index >= len(questions):

        await employment_result(
            query,
            context
        )

        return

    question = questions[index]

    score = context.user_data.get(
        "employment_score",
        0
    )

    if selected == question["correct"]:

        score += 1

        result_text = """
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

آفرین 👏
"""

    else:

        correct_option = question["options"][
            question["correct"]
        ]

        result_text = f"""
❌ پاسخ اشتباه است.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{correct_option}
"""

    context.user_data["employment_score"] = score

    context.user_data["employment_index"] = index + 1

    next_index = index + 1

    if next_index < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data=(
                        f"employment_next"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    "🚪 خروج از آزمون",
                    callback_data="employment_exam"
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

        await employment_result(
            query,
            context
        )


# =========================================================
# NEXT QUESTION
# =========================================================

async def employment_next_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    await send_employment_question(
        query,
        context
    )


# =========================================================
# RESULT
# =========================================================

async def employment_result(
    query,
    context
):

    questions = context.user_data.get(
        "employment_questions",
        []
    )

    score = context.user_data.get(
        "employment_score",
        0
    )

    total = len(questions)

    if total == 0:

        await query.edit_message_text(
            "❌ آزمون خالی است.",
            reply_markup=employment_exam_categories()
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

━━━━━━━━━━━━━━━━━━

🎯 ارزیابی:

{evaluation}

━━━━━━━━━━━━━━━━━━

📚 پیشنهاد:

سؤالات اشتباه را دوباره مطالعه کنید
و سپس آزمون را تکرار کنید.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 آزمون مجدد",
                callback_data="employment_full_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 شبیه‌سازی آزمون",
                callback_data="employment_simulation"
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
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
