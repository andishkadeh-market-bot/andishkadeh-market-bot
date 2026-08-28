# =========================================================
# employment_exam.py
# 📝 سیستم آزمون استخدامی
# 🏛️ اندیشکده مدیریت و بازار
#
# نسخه نهایی و کامل
# دارای:
# • آزمون بانک رفاه
# • آزمون بانک شهر
# • آزمون بانک مهر
# • آزمون بانک‌های دولتی
# • آزمون جامع بانکی
# • سطح آسان / متوسط / سخت
# • دسته‌بندی دروس
# • بانک سؤال
# • آزمون تصادفی
# • آزمون شبیه‌سازی‌شده
# • نتیجه و تحلیل آزمون
# =========================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# =========================================================
# اطلاعات بانک‌ها
# =========================================================

BANK_NAMES = {
    "refah": "🏦 بانک رفاه کارگران",
    "shahr": "🏦 بانک شهر",
    "mehr": "🏦 بانک مهر ایران",
    "government": "🏛️ بانک‌های دولتی",
    "general": "🏦 آزمون جامع بانکی",
}

# =========================================================
# سطوح سؤال
# =========================================================

LEVEL_NAMES = {
    "easy": "🟢 آسان",
    "medium": "🟡 متوسط",
    "hard": "🔴 سخت",
}

# =========================================================
# دروس
# =========================================================

SUBJECT_NAMES = {
    "banking": "🏦 بانکداری",
    "math": "➗ ریاضی",
    "iq": "🧠 هوش و استعداد",
    "english": "🇬🇧 زبان انگلیسی",
    "icdl": "💻 ICDL",
    "economics": "💰 اقتصاد",
    "management": "📚 مدیریت",
    "marketing": "📈 بازاریابی",
    "trade": "🌍 تجارت بین‌الملل",
    "law": "⚖️ قوانین بانکی",
    "general": "🌐 اطلاعات عمومی",
}

# =========================================================
# بانک سؤال
# =========================================================
#
# ساختار هر سؤال:
#
# {
#     "question": "...",
#     "options": [...],
#     "correct": 0,
#     "subject": "banking",
#     "level": "easy",
#     "banks": ["refah", "shahr", "mehr", "government"],
#     "explanation": "..."
# }
#
# correct از صفر شروع می‌شود:
# 0 = گزینه اول
# 1 = گزینه دوم
# 2 = گزینه سوم
# 3 = گزینه چهارم
#
# =========================================================

EMPLOYMENT_QUESTIONS = [

    # -----------------------------------------------------
    # بانکداری - آسان
    # -----------------------------------------------------

    {
        "question": "بانک مرکزی مهم‌ترین نهاد سیاست‌گذار پولی کشور است.",
        "options": [
            "درست",
            "نادرست",
            "فقط در بخش خصوصی",
            "فقط در امور مالیاتی"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "بانک مرکزی مسئولیت‌های مهمی در حوزه سیاست پولی و ثبات مالی دارد.",
    },

    {
        "question": "کدام گزینه نمونه‌ای از سپرده بانکی است؟",
        "options": [
            "سپرده سرمایه‌گذاری",
            "مالیات",
            "اوراق هویتی",
            "مجوز کسب"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "سپرده‌های بانکی یکی از منابع اصلی تجهیز منابع بانک‌ها هستند.",
    },

    {
        "question": "کدام گزینه به مفهوم نقدینگی نزدیک‌تر است؟",
        "options": [
            "پول و شبه‌پول",
            "فقط اسکناس",
            "فقط طلا",
            "فقط ارز خارجی"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "در ادبیات اقتصادی ایران، نقدینگی معمولاً شامل پول و شبه‌پول است.",
    },

    {
        "question": "وظیفه اصلی بانک تجاری چیست؟",
        "options": [
            "تجهیز و تخصیص منابع مالی",
            "تعیین مالیات",
            "قانون‌گذاری کشور",
            "صدور شناسنامه"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "بانک‌ها منابع را جذب کرده و از طریق تسهیلات و خدمات مالی تخصیص می‌دهند.",
    },

    # -----------------------------------------------------
    # بانکداری - متوسط
    # -----------------------------------------------------

    {
        "question": "کدام گزینه بیشتر با عملیات بازار باز ارتباط دارد؟",
        "options": [
            "خرید و فروش اوراق توسط بانک مرکزی",
            "صدور شناسنامه",
            "وضع مالیات بر درآمد",
            "ثبت شرکت"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "عملیات بازار باز یکی از ابزارهای سیاست پولی است.",
    },

    {
        "question": "هدف اصلی قانون مبارزه با پولشویی چیست؟",
        "options": [
            "مقابله با تطهیر عواید حاصل از جرم",
            "افزایش فروش شرکت‌ها",
            "افزایش صادرات",
            "کاهش مالیات"
        ],
        "correct": 0,
        "subject": "law",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "قوانین مبارزه با پولشویی برای جلوگیری از ورود عواید مجرمانه به چرخه رسمی اقتصادی طراحی شده‌اند.",
    },

    {
        "question": "ریسک اعتباری در بانکداری به چه معناست؟",
        "options": [
            "احتمال عدم ایفای تعهدات توسط مشتری",
            "افزایش تعداد کارکنان",
            "کاهش هزینه تبلیغات",
            "افزایش شعب"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "ریسک اعتباری به احتمال زیان ناشی از ناتوانی یا عدم تمایل طرف مقابل به ایفای تعهدات مربوط است.",
    },

    # -----------------------------------------------------
    # بانکداری - سخت
    # -----------------------------------------------------

    {
        "question": "اگر بانک با افزایش مطالبات غیرجاری مواجه شود، کدام ریسک می‌تواند بیشتر شود؟",
        "options": [
            "ریسک اعتباری",
            "ریسک منابع انسانی",
            "ریسک تبلیغات",
            "ریسک برند"
        ],
        "correct": 0,
        "subject": "banking",
        "level": "hard",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "افزایش مطالبات غیرجاری می‌تواند نشانه افزایش ریسک اعتباری و احتمال زیان تسهیلات باشد.",
    },

    # -----------------------------------------------------
    # اقتصاد
    # -----------------------------------------------------

    {
        "question": "تورم به چه معناست؟",
        "options": [
            "افزایش مستمر و عمومی سطح قیمت‌ها",
            "افزایش قیمت یک کالا",
            "کاهش تولید یک شرکت",
            "افزایش دستمزد یک فرد"
        ],
        "correct": 0,
        "subject": "economics",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "تورم افزایش مستمر و عمومی سطح قیمت‌ها در اقتصاد است.",
    },

    {
        "question": "GDP مخفف کدام عبارت است؟",
        "options": [
            "Gross Domestic Product",
            "General Deposit Policy",
            "Global Development Price",
            "Government Debt Program"
        ],
        "correct": 0,
        "subject": "economics",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "GDP به معنای تولید ناخالص داخلی است.",
    },

    {
        "question": "در شرایط برابر، افزایش قیمت معمولاً چه اثری بر مقدار تقاضا دارد؟",
        "options": [
            "کاهش",
            "افزایش",
            "دو برابر شدن",
            "بدون اثر"
        ],
        "correct": 0,
        "subject": "economics",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "بر اساس قانون تقاضا، در شرایط برابر افزایش قیمت معمولاً باعث کاهش مقدار تقاضا می‌شود.",
    },

    {
        "question": "کدام مورد ابزار سیاست مالی است؟",
        "options": [
            "مالیات",
            "عملیات بازار باز",
            "ذخایر بانکی",
            "نرخ سیاستی"
        ],
        "correct": 0,
        "subject": "economics",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "مالیات و مخارج دولت از ابزارهای سیاست مالی هستند.",
    },

    # -----------------------------------------------------
    # ریاضی
    # -----------------------------------------------------

    {
        "question": "اگر قیمت کالایی ۲۰۰ هزار تومان باشد و ۱۰ درصد افزایش یابد، قیمت جدید چقدر است؟",
        "options": [
            "۲۱۰ هزار تومان",
            "۲۲۰ هزار تومان",
            "۲۳۰ هزار تومان",
            "۲۴۰ هزار تومان"
        ],
        "correct": 1,
        "subject": "math",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "۱۰ درصد ۲۰۰ هزار تومان برابر ۲۰ هزار تومان است، بنابراین قیمت جدید ۲۲۰ هزار تومان می‌شود.",
    },

    {
        "question": "اگر ۵۰ درصد یک عدد برابر ۴۰ باشد، عدد اصلی چند است؟",
        "options": [
            "۶۰",
            "۷۰",
            "۸۰",
            "۹۰"
        ],
        "correct": 2,
        "subject": "math",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "اگر نصف عدد ۴۰ باشد، کل عدد ۸۰ است.",
    },

    {
        "question": "اگر سود یک سرمایه ۱۰۰ میلیون تومانی برابر ۱۵ درصد باشد، سود چقدر است؟",
        "options": [
            "۱۰ میلیون",
            "۱۵ میلیون",
            "۲۰ میلیون",
            "۲۵ میلیون"
        ],
        "correct": 1,
        "subject": "math",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "۱۵ درصد از ۱۰۰ میلیون تومان برابر ۱۵ میلیون تومان است.",
    },

    # -----------------------------------------------------
    # هوش
    # -----------------------------------------------------

    {
        "question": "عدد بعدی را پیدا کنید: ۲، ۴، ۶، ۸، ؟",
        "options": [
            "۹",
            "۱۰",
            "۱۲",
            "۱۴"
        ],
        "correct": 1,
        "subject": "iq",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "اعداد هر بار ۲ واحد افزایش پیدا می‌کنند.",
    },

    {
        "question": "کدام گزینه با بقیه متفاوت است؟",
        "options": [
            "مربع",
            "مثلث",
            "دایره",
            "کتاب"
        ],
        "correct": 3,
        "subject": "iq",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "سه گزینه شکل هندسی هستند، اما کتاب شکل هندسی نیست.",
    },

    {
        "question": "عدد بعدی: ۳، ۶، ۱۲، ۲۴، ؟",
        "options": [
            "۳۰",
            "۳۶",
            "۴۸",
            "۵۰"
        ],
        "correct": 2,
        "subject": "iq",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "هر عدد دو برابر عدد قبلی است.",
    },

    # -----------------------------------------------------
    # زبان
    # -----------------------------------------------------

    {
        "question": "معنی کلمه Bank چیست؟",
        "options": [
            "بازار",
            "بانک",
            "فروشگاه",
            "شرکت"
        ],
        "correct": 1,
        "subject": "english",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "Bank در این کاربرد به معنی بانک است.",
    },

    {
        "question": "کدام گزینه به معنی Customer است؟",
        "options": [
            "مشتری",
            "کارمند",
            "مدیر",
            "بانکدار"
        ],
        "correct": 0,
        "subject": "english",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "Customer یعنی مشتری.",
    },

    # -----------------------------------------------------
    # ICDL
    # -----------------------------------------------------

    {
        "question": "کدام نرم‌افزار برای ایجاد و ویرایش اسناد متنی استفاده می‌شود؟",
        "options": [
            "Microsoft Word",
            "Microsoft Paint",
            "Calculator",
            "Notepad فقط"
        ],
        "correct": 0,
        "subject": "icdl",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "Microsoft Word نرم‌افزار پردازش متن است.",
    },

    {
        "question": "میانبر Ctrl+C معمولاً چه کاری انجام می‌دهد؟",
        "options": [
            "کپی",
            "چسباندن",
            "ذخیره",
            "حذف"
        ],
        "correct": 0,
        "subject": "icdl",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "Ctrl+C برای Copy استفاده می‌شود.",
    },

    # -----------------------------------------------------
    # مدیریت
    # -----------------------------------------------------

    {
        "question": "کدام مورد یکی از وظایف اصلی مدیریت است؟",
        "options": [
            "برنامه‌ریزی",
            "خرید شخصی",
            "رانندگی",
            "طراحی ساختمان"
        ],
        "correct": 0,
        "subject": "management",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "برنامه‌ریزی یکی از وظایف اساسی مدیریت است.",
    },

    {
        "question": "کنترل در مدیریت بیشتر به چه معناست؟",
        "options": [
            "مقایسه عملکرد با اهداف و اصلاح انحرافات",
            "افزایش تبلیغات",
            "استخدام بدون برنامه",
            "افزایش قیمت"
        ],
        "correct": 0,
        "subject": "management",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "کنترل شامل سنجش عملکرد، مقایسه با استانداردها و اقدام اصلاحی است.",
    },

    # -----------------------------------------------------
    # بازاریابی
    # -----------------------------------------------------

    {
        "question": "کدام گزینه یکی از عناصر آمیخته بازاریابی سنتی 4P است؟",
        "options": [
            "Product",
            "People فقط",
            "Politics",
            "Population"
        ],
        "correct": 0,
        "subject": "marketing",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "4P شامل Product، Price، Place و Promotion است.",
    },

    {
        "question": "Promotion در بازاریابی بیشتر به چه معناست؟",
        "options": [
            "ترفیع و فعالیت‌های ارتباطی",
            "تولید",
            "قیمت‌گذاری",
            "انبارداری"
        ],
        "correct": 0,
        "subject": "marketing",
        "level": "medium",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "Promotion به فعالیت‌های ترفیعی و ارتباطی برای معرفی و فروش محصول مربوط است.",
    },

    # -----------------------------------------------------
    # تجارت بین‌الملل
    # -----------------------------------------------------

    {
        "question": "صادرات به چه معناست؟",
        "options": [
            "فروش کالا یا خدمات به خارج از کشور",
            "خرید از خارج",
            "تولید داخلی",
            "مصرف داخلی"
        ],
        "correct": 0,
        "subject": "trade",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "صادرات به فروش کالا یا خدمات به بازارهای خارجی گفته می‌شود.",
    },

    {
        "question": "واردات به چه معناست؟",
        "options": [
            "خرید کالا یا خدمات از خارج",
            "فروش داخلی",
            "تولید داخلی",
            "پس‌انداز"
        ],
        "correct": 0,
        "subject": "trade",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "واردات به خرید کالا یا خدمات از خارج از کشور گفته می‌شود.",
    },

    # -----------------------------------------------------
    # اطلاعات عمومی
    # -----------------------------------------------------

    {
        "question": "پایتخت ایران کدام شهر است؟",
        "options": [
            "شیراز",
            "تهران",
            "تبریز",
            "اصفهان"
        ],
        "correct": 1,
        "subject": "general",
        "level": "easy",
        "banks": [
            "refah",
            "shahr",
            "mehr",
            "government"
        ],
        "explanation": "تهران پایتخت جمهوری اسلامی ایران است.",
    },

]


# =========================================================
# دسترسی سازگار با bot.py
# =========================================================

QUESTIONS = EMPLOYMENT_QUESTIONS


# =========================================================
# متن اصلی آزمون استخدامی
# =========================================================

def employment_exam_text():

    return """
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

سیستم جامع آمادگی آزمون‌های استخدامی

━━━━━━━━━━━━━━━━━━

🏦 بانک رفاه
🏦 بانک شهر
🏦 بانک مهر ایران
🏛️ بانک‌های دولتی
🏦 آزمون جامع بانکی

━━━━━━━━━━━━━━━━━━

🎯 امکانات:

📚 بانک سؤال
🟢 سطح آسان
🟡 سطح متوسط
🔴 سطح سخت

🧠 هوش و استعداد
➗ ریاضی
🇬🇧 زبان انگلیسی
💻 ICDL
🏦 بانکداری
⚖️ قوانین بانکی
💰 اقتصاد
📚 مدیریت
📈 بازاریابی
🌍 تجارت بین‌الملل

━━━━━━━━━━━━━━━━━━

👇 نوع آزمون را انتخاب کنید.
"""


# =========================================================
# منوی اصلی آزمون استخدامی
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
                "🏦 بانک شهر",
                callback_data="employment_bank_shahr"
            )
        ],

        [
            InlineKeyboardButton(
                "🏦 بانک مهر",
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
                "🏦 آزمون جامع بانکی",
                callback_data="employment_bank_general"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 آزمون شبیه‌سازی‌شده",
                callback_data="employment_simulation"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 بانک سؤال",
                callback_data="employment_question_bank"
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
# callback اصلی
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
# دسته‌بندی بانک
# =========================================================

def bank_menu(bank):

    name = BANK_NAMES.get(
        bank,
        "🏦 آزمون بانکی"
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 آسان",
                callback_data=f"employment_level_{bank}_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 متوسط",
                callback_data=f"employment_level_{bank}_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سخت",
                callback_data=f"employment_level_{bank}_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 همه سطوح",
                callback_data=f"employment_level_{bank}_all"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 آزمون شبیه‌سازی",
                callback_data=f"employment_sim_{bank}"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="employment_exam"
            )
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


async def employment_exam_category_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    bank = query.data.replace(
        "employment_bank_",
        ""
    )

    if bank not in BANK_NAMES:

        await query.edit_message_text(
            "❌ بانک انتخاب‌شده معتبر نیست.",
            reply_markup=employment_exam_menu()
        )

        return

    text = f"""
📝 آزمون استخدامی

{BANK_NAMES[bank]}

━━━━━━━━━━━━━━━━━━

سطح موردنظر را انتخاب کنید:

🟢 آسان
🟡 متوسط
🔴 سخت

یا می‌توانید آزمون شبیه‌سازی‌شده را انتخاب کنید.
"""

    await query.edit_message_text(
        text,
        reply_markup=bank_menu(bank)
    )


# =========================================================
# فیلتر سؤال
# =========================================================

def get_questions(
    bank=None,
    level=None,
    subject=None
):

    result = []

    for question in EMPLOYMENT_QUESTIONS:

        if bank:

            if bank not in question["banks"]:
                continue

        if level:

            if level != "all":

                if question["level"] != level:
                    continue

        if subject:

            if question["subject"] != subject:
                continue

        result.append(question)

    return result


# =========================================================
# متن بانک سؤال
# =========================================================

def question_bank_text():

    total = len(
        EMPLOYMENT_QUESTIONS
    )

    return f"""
📚 بانک سؤال استخدامی

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار

📊 تعداد سؤالات فعلی:
{total} سؤال

━━━━━━━━━━━━━━━━━━

🏦 بانک‌های تحت پوشش:

• بانک رفاه
• بانک شهر
• بانک مهر
• بانک‌های دولتی
• آزمون جامع بانکی

━━━━━━━━━━━━━━━━━━

🎯 سطوح:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

📚 دروس:

🏦 بانکداری
➗ ریاضی
🧠 هوش
🇬🇧 زبان
💻 ICDL
💰 اقتصاد
📚 مدیریت
📈 بازاریابی
🌍 تجارت
⚖️ قوانین بانکی

━━━━━━━━━━━━━━━━━━

بانک سؤال قابلیت توسعه به هزاران سؤال را دارد.
"""


async def question_bank_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 همه سؤالات",
                callback_data="employment_bank_questions_all"
            )
        ],

        [
            InlineKeyboardButton(
                "🟢 سؤالات آسان",
                callback_data="employment_bank_questions_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 سؤالات متوسط",
                callback_data="employment_bank_questions_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سؤالات سخت",
                callback_data="employment_bank_questions_hard"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="employment_exam"
            )
        ],

    ]

    await query.edit_message_text(
        question_bank_text(),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# شروع آزمون
# =========================================================

async def employment_exam_start_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    data = query.data.split("_")

    # employment_level_BANK_LEVEL
    # مثال:
    # employment_level_refah_easy

    if len(data) < 4:

        await query.edit_message_text(
            "❌ اطلاعات آزمون ناقص است.",
            reply_markup=employment_exam_menu()
        )

        return

    bank = data[2]
    level = data[3]

    questions = get_questions(
        bank=bank,
        level=level
    )

    if not questions:

        await query.edit_message_text(
            "❌ در این دسته هنوز سؤال ثبت نشده است.",
            reply_markup=bank_menu(bank)
        )

        return

    # ذخیره وضعیت آزمون برای کاربر
    context.user_data["employment_exam"] = {
        "bank": bank,
        "level": level,
        "questions": questions,
        "index": 0,
        "score": 0,
    }

    await show_employment_question(
        query,
        context
    )


# =========================================================
# نمایش سؤال
# =========================================================

async def show_employment_question(
    query,
    context
):

    exam = context.user_data.get(
        "employment_exam"
    )

    if not exam:

        await query.edit_message_text(
            "❌ آزمون فعال وجود ندارد.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = exam["questions"]
    index = exam["index"]
    score = exam["score"]

    if index >= len(questions):

        await show_employment_result(
            query,
            context
        )

        return

    question = questions[index]

    level = LEVEL_NAMES.get(
        question["level"],
        ""
    )

    subject = SUBJECT_NAMES.get(
        question["subject"],
        ""
    )

    text = f"""
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {len(questions)}

⭐ امتیاز: {score}

{level}
{subject}

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

    exam = context.user_data.get(
        "employment_exam"
    )

    if not exam:

        await query.edit_message_text(
            "❌ آزمون فعال وجود ندارد.",
            reply_markup=employment_exam_menu()
        )

        return

    questions = exam["questions"]

    if index >= len(questions):

        await show_employment_result(
            query,
            context
        )

        return

    question = questions[index]

    correct = question["correct"]

    if selected == correct:

        exam["score"] += 1

        result_text = f"""
✅ پاسخ صحیح است.

🎯 +۱ امتیاز

⭐ امتیاز فعلی:
{exam["score"]}

━━━━━━━━━━━━━━━━━━

آفرین 👏
"""

    else:

        correct_option = question[
            "options"
        ][correct]

        result_text = f"""
❌ پاسخ اشتباه است.

━━━━━━━━━━━━━━━━━━

✅ پاسخ صحیح:

{correct_option}

━━━━━━━━━━━━━━━━━━

💡 توضیح:

{question.get("explanation", "")}

━━━━━━━━━━━━━━━━━━

⭐ امتیاز فعلی:
{exam["score"]}
"""

    exam["index"] += 1

    if exam["index"] < len(questions):

        keyboard = [

            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data="employment_next"
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
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        keyboard = [

            [
                InlineKeyboardButton(
                    "🏁 مشاهده نتیجه",
                    callback_data="employment_next"
                )
            ]

        ]

        await query.edit_message_text(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
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

    await show_employment_question(
        query,
        context
    )


# =========================================================
# نتیجه آزمون
# =========================================================

async def show_employment_result(
    query,
    context
):

    exam = context.user_data.get(
        "employment_exam"
    )

    if not exam:

        await query.edit_message_text(
            "❌ اطلاعات آزمون پیدا نشد.",
            reply_markup=employment_exam_menu()
        )

        return

    total = len(
        exam["questions"]
    )

    score = exam["score"]

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

    bank_name = BANK_NAMES.get(
        exam["bank"],
        "آزمون استخدامی"
    )

    text = f"""
🏁 آزمون به پایان رسید.

{bank_name}

━━━━━━━━━━━━━━━━━━

📊 نتیجه آزمون

📝 تعداد سؤالات:
{total}

✅ صحیح:
{score}

❌ غلط:
{wrong}

📈 درصد:
{percentage}٪

━━━━━━━━━━━━━━━━━━

🎯 ارزیابی:

{evaluation}

━━━━━━━━━━━━━━━━━━

📚 پیشنهاد:

سؤالات غلط را بررسی کنید،
درس مربوطه را دوباره مطالعه کنید
و سپس آزمون را تکرار کنید.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 تکرار آزمون",
                callback_data=(
                    f"employment_level_"
                    f"{exam['bank']}_"
                    f"{exam['level']}"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "🏦 انتخاب آزمون دیگر",
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


# =========================================================
# آزمون شبیه‌سازی‌شده
# =========================================================

async def employment_simulation_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    text = """
🎯 آزمون شبیه‌سازی‌شده استخدامی

━━━━━━━━━━━━━━━━━━

این آزمون برای شبیه‌سازی شرایط آزمون استخدامی
طراحی شده است.

📚 ترکیب دروس:

🧠 هوش
➗ ریاضی
🇬🇧 زبان
💻 ICDL
🏦 بانکداری
💰 اقتصاد
📚 مدیریت
⚖️ قوانین بانکی

━━━━━━━━━━━━━━━━━━

🎯 سطح:

ترکیبی

📝 سؤال‌ها به‌صورت تصادفی انتخاب می‌شوند.

━━━━━━━━━━━━━━━━━━

👇 برای شروع:
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع شبیه‌سازی",
                callback_data="employment_sim_start"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="employment_exam"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def employment_sim_start_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    import random

    questions = list(
        EMPLOYMENT_QUESTIONS
    )

    random.shuffle(
        questions
    )

    # حداکثر 20 سؤال در نسخه فعلی
    questions = questions[
        :min(20, len(questions))
    ]

    context.user_data["employment_exam"] = {
        "bank": "general",
        "level": "all",
        "questions": questions,
        "index": 0,
        "score": 0,
    }

    await show_employment_question(
        query,
        context
    )


# =========================================================
# نمایش بانک سؤال بر اساس سطح
# =========================================================

async def employment_question_list_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    level = query.data.replace(
        "employment_bank_questions_",
        ""
    )

    questions = get_questions(
        level=level if level != "all" else None
    )

    if not questions:

        await query.edit_message_text(
            "❌ سؤالی در این دسته ثبت نشده است.",
            reply_markup=employment_exam_menu()
        )

        return

    text = f"""
📚 بانک سؤال

━━━━━━━━━━━━━━━━━━

📝 تعداد سؤال:
{len(questions)}

━━━━━━━━━━━━━━━━━━

سطح انتخاب‌شده:

{
    LEVEL_NAMES.get(level, "📚 همه سطوح")
    if level != "all"
    else "📚 همه سطوح"
}

━━━━━━━━━━━━━━━━━━

برای تمرین می‌توانید آزمون مربوط به سطح
موردنظر را انتخاب کنید.
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع تمرین",
                callback_data=(
                    f"employment_practice_{level}"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="employment_question_bank"
            )
        ],

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# تمرین بانک سؤال
# =========================================================

async def employment_practice_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    import random

    level = query.data.replace(
        "employment_practice_",
        ""
    )

    questions = get_questions(
        level=level if level != "all" else None
    )

    random.shuffle(
        questions
    )

    questions = questions[
        :min(10, len(questions))
    ]

    if not questions:

        await query.edit_message_text(
            "❌ سؤال کافی وجود ندارد.",
            reply_markup=employment_exam_menu()
        )

        return

    context.user_data["employment_exam"] = {
        "bank": "general",
        "level": level,
        "questions": questions,
        "index": 0,
        "score": 0,
    }

    await show_employment_question(
        query,
        context
    )


# =========================================================
# خروج از آزمون
# =========================================================

async def employment_exam_exit_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    context.user_data.pop(
        "employment_exam",
        None
    )

    await query.edit_message_text(
        employment_exam_text(),
        reply_markup=employment_exam_menu()
    )


# =========================================================
# سازگاری با نام‌های احتمالی bot.py
# =========================================================

employment_exam_intro_text = employment_exam_text

employment_questions = EMPLOYMENT_QUESTIONS

BANK_QUESTIONS = EMPLOYMENT_QUESTIONS


# =========================================================
# پایان فایل
# =========================================================
