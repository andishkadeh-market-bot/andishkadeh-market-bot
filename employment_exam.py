# =========================================================
# employment_exam.py
# 📝 آزمون استخدامی
# 🏛️ اندیشکده مدیریت و بازار
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# SUBJECTS
# =========================================================

EMPLOYMENT_SUBJECTS = {
    "banking_laws": "🏦 قوانین و مقررات بانکی",
    "iq": "🧠 هوش و استعداد",
    "math": "➗ ریاضی و آمار",
    "english": "🇬🇧 زبان انگلیسی",
    "icdl": "💻 ICDL",
    "general": "🌐 اطلاعات عمومی",
}


# =========================================================
# QUESTIONS
# ساختار:
#
# {
#     "question": "...",
#     "options": ["...", "...", "...", "..."],
#     "correct": 0
# }
# =========================================================

EMPLOYMENT_QUESTIONS = {

    "banking_laws": [

        {
            "question": "کدام مورد از موضوعات مرتبط با قوانین بانکی است؟",
            "options": [
                "قانون عملیات بانکی بدون ربا",
                "قانون تجارت الکترونیک اروپا",
                "قانون راهنمایی و رانندگی",
                "قانون ثبت احوال"
            ],
            "correct": 0
        },

        {
            "question": "کدام نهاد نقش اصلی در سیاست‌گذاری پولی کشور دارد؟",
            "options": [
                "بانک مرکزی",
                "شهرداری",
                "وزارت ورزش",
                "سازمان ثبت احوال"
            ],
            "correct": 0
        },

        {
            "question": "کدام گزینه با مبارزه با پولشویی ارتباط مستقیم دارد؟",
            "options": [
                "شناسایی و احراز هویت مشتری",
                "افزایش تبلیغات",
                "کاهش ساعات کاری",
                "افزایش فروشگاه‌ها"
            ],
            "correct": 0
        },

        {
            "question": "منظور از احراز هویت مشتری چیست؟",
            "options": [
                "بررسی و تأیید هویت مشتری",
                "افزایش موجودی حساب",
                "پرداخت تسهیلات",
                "بستن حساب"
            ],
            "correct": 0
        },

        {
            "question": "کدام گزینه نمونه‌ای از عملیات بانکی است؟",
            "options": [
                "افتتاح حساب",
                "تولید خودرو",
                "ساخت ساختمان",
                "تولید محصولات کشاورزی"
            ],
            "correct": 0
        },

    ],

    "iq": [

        {
            "question": "عدد بعدی را مشخص کنید:\n\n2 ، 4 ، 6 ، 8 ، ؟",
            "options": [
                "9",
                "10",
                "11",
                "12"
            ],
            "correct": 1
        },

        {
            "question": "عدد بعدی را مشخص کنید:\n\n3 ، 6 ، 12 ، 24 ، ؟",
            "options": [
                "36",
                "42",
                "48",
                "54"
            ],
            "correct": 2
        },

        {
            "question": "اگر همه مدیران کارمند باشند و علی مدیر باشد، کدام گزینه درست است؟",
            "options": [
                "علی کارمند است",
                "علی مدیر نیست",
                "همه کارمندان مدیرند",
                "هیچ نتیجه‌ای نمی‌توان گرفت"
            ],
            "correct": 0
        },

        {
            "question": "کدام گزینه با بقیه متفاوت است؟",
            "options": [
                "مربع",
                "مثلث",
                "دایره",
                "مکعب"
            ],
            "correct": 3
        },

        {
            "question": "اگر امروز دوشنبه باشد، سه روز بعد چه روزی است؟",
            "options": [
                "سه‌شنبه",
                "چهارشنبه",
                "پنجشنبه",
                "جمعه"
            ],
            "correct": 2
        },

    ],

    "math": [

        {
            "question": "حاصل 15 + 27 چند است؟",
            "options": [
                "32",
                "42",
                "52",
                "62"
            ],
            "correct": 1
        },

        {
            "question": "20 درصد عدد 200 چند است؟",
            "options": [
                "20",
                "30",
                "40",
                "50"
            ],
            "correct": 2
        },

        {
            "question": "اگر قیمت کالایی 100 هزار تومان باشد و 10 درصد افزایش پیدا کند، قیمت جدید چقدر است؟",
            "options": [
                "105 هزار تومان",
                "110 هزار تومان",
                "115 هزار تومان",
                "120 هزار تومان"
            ],
            "correct": 1
        },

        {
            "question": "میانگین اعداد 10، 20 و 30 چند است؟",
            "options": [
                "15",
                "20",
                "25",
                "30"
            ],
            "correct": 1
        },

        {
            "question": "حاصل 8 × 7 چند است؟",
            "options": [
                "48",
                "54",
                "56",
                "64"
            ],
            "correct": 2
        },

    ],

    "english": [

        {
            "question": "معنی کلمه \"Bank\" چیست؟",
            "options": [
                "بازار",
                "بانک",
                "شرکت",
                "فروشگاه"
            ],
            "correct": 1
        },

        {
            "question": "معنی کلمه \"Market\" چیست؟",
            "options": [
                "بانک",
                "بازار",
                "پول",
                "کارمند"
            ],
            "correct": 1
        },

        {
            "question": "کدام گزینه معنی \"Manager\" است؟",
            "options": [
                "مدیر",
                "مشتری",
                "فروشنده",
                "حسابدار"
            ],
            "correct": 0
        },

        {
            "question": "گزینه صحیح را انتخاب کنید:\n\nShe ___ a manager.",
            "options": [
                "am",
                "are",
                "is",
                "be"
            ],
            "correct": 2
        },

        {
            "question": "معنی \"Customer\" چیست؟",
            "options": [
                "مشتری",
                "مدیر",
                "کارمند",
                "بانک"
            ],
            "correct": 0
        },

    ],

    "icdl": [

        {
            "question": "کدام نرم‌افزار برای پردازش متن استفاده می‌شود؟",
            "options": [
                "Microsoft Word",
                "Calculator",
                "Paint",
                "Media Player"
            ],
            "correct": 0
        },

        {
            "question": "کدام نرم‌افزار برای کار با جداول و محاسبات مناسب است؟",
            "options": [
                "Word",
                "Excel",
                "Paint",
                "Notepad"
            ],
            "correct": 1
        },

        {
            "question": "میانبر Copy در ویندوز چیست؟",
            "options": [
                "Ctrl + X",
                "Ctrl + C",
                "Ctrl + V",
                "Ctrl + Z"
            ],
            "correct": 1
        },

        {
            "question": "میانبر Paste چیست؟",
            "options": [
                "Ctrl + A",
                "Ctrl + C",
                "Ctrl + V",
                "Ctrl + S"
            ],
            "correct": 2
        },

        {
            "question": "کدام گزینه برای ذخیره فایل استفاده می‌شود؟",
            "options": [
                "Ctrl + S",
                "Ctrl + P",
                "Ctrl + X",
                "Ctrl + F"
            ],
            "correct": 0
        },

    ],

    "general": [

        {
            "question": "واحد پول رسمی ایران چیست؟",
            "options": [
                "دلار",
                "ریال",
                "یورو",
                "لیر"
            ],
            "correct": 1
        },

        {
            "question": "بانک مرکزی چه نقشی در اقتصاد دارد؟",
            "options": [
                "سیاست‌گذاری پولی",
                "تولید خودرو",
                "ساخت مسکن",
                "تولید مواد غذایی"
            ],
            "correct": 0
        },

        {
            "question": "کدام مورد از اجزای اصلی اقتصاد است؟",
            "options": [
                "عرضه و تقاضا",
                "فقط صادرات",
                "فقط واردات",
                "فقط مالیات"
            ],
            "correct": 0
        },

        {
            "question": "تورم به طور کلی به چه معناست؟",
            "options": [
                "کاهش عمومی قیمت‌ها",
                "افزایش مستمر و عمومی سطح قیمت‌ها",
                "افزایش تولید",
                "کاهش بیکاری"
            ],
            "correct": 1
        },

        {
            "question": "GDP مخفف چیست؟",
            "options": [
                "تولید ناخالص داخلی",
                "درآمد خالص بانک",
                "مالیات عمومی",
                "نرخ بهره"
            ],
            "correct": 0
        },

    ],
}


# =========================================================
# INTRO
# =========================================================

def employment_exam_intro_text():

    return """
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

سیستم تمرینی آزمون‌های استخدامی

━━━━━━━━━━━━━━━━━━

📚 سرفصل‌های موجود:

🏦 قوانین و مقررات بانکی
🧠 هوش و استعداد
➗ ریاضی و آمار
🇬🇧 زبان انگلیسی
💻 ICDL
🌐 اطلاعات عمومی

━━━━━━━━━━━━━━━━━━

🎯 هدف:

تمرین
+
آزمون
+
تحلیل اشتباهات
+
آمادگی استخدامی

👇 درس موردنظر را انتخاب کنید.
"""


# =========================================================
# MENU
# =========================================================

def employment_exam_menu():

    keyboard = []

    for key, name in EMPLOYMENT_SUBJECTS.items():

        keyboard.append(
            [
                InlineKeyboardButton(
                    name,
                    callback_data=f"employment_subject_{key}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🎯 آزمون جامع",
                callback_data="employment_full_exam"
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# SUBJECT INTRO
# =========================================================

def employment_subject_intro(
    subject
):

    if subject not in EMPLOYMENT_SUBJECTS:

        return (
            "❌ این درس وجود ندارد.",
            employment_exam_menu()
        )

    name = EMPLOYMENT_SUBJECTS[subject]

    questions = EMPLOYMENT_QUESTIONS.get(
        subject,
        []
    )

    text = f"""
📚 {name}

━━━━━━━━━━━━━━━━━━

📝 تعداد سؤالات:
{len(questions)} سؤال

🎯 نوع آزمون:
چهارگزینه‌ای

⭐ امتیاز:
هر پاسخ صحیح = ۱ امتیاز

━━━━━━━━━━━━━━━━━━

📌 بعد از هر پاسخ، جواب صحیح نمایش داده می‌شود.

👇 برای شروع:
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🚀 شروع آزمون",
                    callback_data=f"employment_exam_{subject}_0_0"
                )
            ],

            [
                InlineKeyboardButton(
                    "📝 آزمون جامع",
                    callback_data="employment_full_exam"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
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
    )

    return text, keyboard


# =========================================================
# GET QUESTIONS
# =========================================================

def get_subject_questions(
    subject
):

    return EMPLOYMENT_QUESTIONS.get(
        subject,
        []
    )


# =========================================================
# QUESTION
# =========================================================

def employment_question_data(
    subject,
    index,
    score
):

    questions = get_subject_questions(subject)

    if not questions:
        return None

    if index >= len(questions):
        return None

    question = questions[index]

    name = EMPLOYMENT_SUBJECTS.get(
        subject,
        "آزمون استخدامی"
    )

    text = f"""
📝 آزمون استخدامی

📚 {name}

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
                        f"employment_answer_"
                        f"{subject}_"
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

    return (
        text,
        InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# ANSWER
# =========================================================

def employment_answer_data(
    subject,
    index,
    selected,
    score
):

    questions = get_subject_questions(subject)

    if not questions:
        return None

    if index >= len(questions):
        return None

    question = questions[index]

    correct = question["correct"]

    is_correct = selected == correct

    if is_correct:

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
❌ پاسخ اشتباه است.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{correct_option}

━━━━━━━━━━━━━━━━━━

⭐ امتیاز فعلی: {score}
"""

    next_index = index + 1

    finished = next_index >= len(questions)

    return {
        "is_correct": is_correct,
        "score": score,
        "next_index": next_index,
        "finished": finished,
        "result_text": result_text,
    }


# =========================================================
# RESULT
# =========================================================

def employment_result_text(
    subject,
    score
):

    questions = get_subject_questions(subject)

    total = len(questions)

    if total == 0:
        return "❌ آزمونی برای این بخش وجود ندارد."

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

    name = EMPLOYMENT_SUBJECTS.get(
        subject,
        "آزمون استخدامی"
    )

    return f"""
🏁 آزمون به پایان رسید.

📚 {name}

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
📝 آزمون
+
🔍 بررسی اشتباهات
+
🔄 تکرار آزمون
"""


# =========================================================
# RESULT MENU
# =========================================================

def employment_result_menu(
    subject
):

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
                callback_data=(
                    f"employment_exam_{subject}_0_0"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "📚 انتخاب درس دیگر",
                callback_data="employment_exam"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 آزمون جامع",
                callback_data="employment_full_exam"
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
# FULL EXAM
# =========================================================

def get_full_exam_questions():

    questions = []

    for subject, subject_questions in EMPLOYMENT_QUESTIONS.items():

        for question in subject_questions:

            item = question.copy()

            item["subject"] = subject

            questions.append(item)

    return questions


def employment_full_exam_intro():

    questions = get_full_exam_questions()

    text = f"""
🎯 آزمون جامع استخدامی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

آزمون ترکیبی از سرفصل‌های:

🏦 قوانین بانکی
🧠 هوش
➗ ریاضی
🇬🇧 زبان
💻 ICDL
🌐 اطلاعات عمومی

━━━━━━━━━━━━━━━━━━

📝 تعداد سؤالات:
{len(questions)} سؤال

⭐ هر پاسخ صحیح:
۱ امتیاز

━━━━━━━━━━━━━━━━━━

🎯 مناسب برای:
آمادگی آزمون‌های استخدامی

👇 آماده‌ای؟ 
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🚀 شروع آزمون جامع",
                    callback_data="employment_full_0_0"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
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
    )

    return text, keyboard


def employment_full_question_data(
    index,
    score
):

    questions = get_full_exam_questions()

    if not questions:
        return None

    if index >= len(questions):
        return None

    question = questions[index]

    subject = EMPLOYMENT_SUBJECTS.get(
        question["subject"],
        "آزمون جامع"
    )

    text = f"""
🎯 آزمون جامع استخدامی

━━━━━━━━━━━━━━━━━━

📚 مبحث:
{subject}

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
                        f"employment_full_answer_"
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

    return (
        text,
        InlineKeyboardMarkup(keyboard)
    )


def employment_full_answer_data(
    index,
    selected,
    score
):

    questions = get_full_exam_questions()

    if not questions:
        return None

    if index >= len(questions):
        return None

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
❌ پاسخ اشتباه است.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{correct_option}

━━━━━━━━━━━━━━━━━━

⭐ امتیاز فعلی: {score}
"""

    next_index = index + 1

    return {
        "score": score,
        "next_index": next_index,
        "finished": next_index >= len(questions),
        "result_text": result_text,
    }


def employment_full_result_text(
    score
):

    questions = get_full_exam_questions()

    total = len(questions)

    wrong = total - score

    percentage = round(
        (score / total) * 100
    ) if total else 0

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

    return f"""
🏁 آزمون جامع استخدامی تمام شد.

━━━━━━━━━━━━━━━━━━

📊 نتیجه نهایی

📝 تعداد سؤالات: {total}

✅ پاسخ صحیح: {score}

❌ پاسخ غلط: {wrong}

📈 درصد: {percentage}٪

🎯 ارزیابی:

{evaluation}

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

مطالعه
+
تمرین
+
آزمون
+
تحلیل
=
پیشرفت
"""


def employment_full_result_menu():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 آزمون جامع مجدد",
                    callback_data="employment_full_exam"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 انتخاب درس",
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
    )
