# =========================================================
# employment_exam.py
# 📝 سیستم جامع آزمون استخدامی
# 🏛️ اندیشکده مدیریت و بازار
#
# نسخه حرفه‌ای:
# - بانک رفاه
# - بانک شهر
# - بانک مهر
# - بانک‌های دولتی
# - بانک جامع
# - سطح آسان / متوسط / سخت
# - آزمون شبیه‌سازی‌شده
#
# این فایل مستقل از bot.py طراحی شده است.
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


# =========================================================
# CATEGORY NAMES
# =========================================================

EMPLOYMENT_CATEGORIES = {

    "refah": "🏦 آزمون بانک رفاه",

    "shahr": "🏙️ آزمون بانک شهر",

    "mehr": "🤝 آزمون بانک مهر",

    "government": "🏛️ آزمون بانک‌های دولتی",

    "general": "📚 بانک جامع آزمون استخدامی",

}


# =========================================================
# DIFFICULTY NAMES
# =========================================================

DIFFICULTY_NAMES = {

    "easy": "🟢 آسان",

    "medium": "🟡 متوسط",

    "hard": "🔴 سخت",

}


# =========================================================
# SUBJECT NAMES
# =========================================================

SUBJECT_NAMES = {

    "banking": "🏦 بانکداری",

    "law": "⚖️ قوانین و مقررات",

    "management": "📚 مدیریت",

    "accounting": "🧮 حسابداری",

    "economics": "💰 اقتصاد",

    "marketing": "📈 بازاریابی و فروش",

    "icdl": "💻 فناوری اطلاعات و ICDL",

    "english": "🇬🇧 زبان انگلیسی",

    "math": "➗ ریاضی و آمار",

    "intelligence": "🧠 هوش و استعداد",

    "general": "📖 عمومی",

}


# =========================================================
# QUESTION BANK
# =========================================================
#
# ساختار هر سؤال:
#
# {
#     "category": "refah",
#     "subject": "banking",
#     "difficulty": "easy",
#     "question": "...",
#     "options": [
#         "...",
#         "...",
#         "...",
#         "..."
#     ],
#     "correct": 0,
#     "explanation": "..."
# }
#
# correct از صفر شروع می‌شود:
# 0 = گزینه اول
# 1 = گزینه دوم
# 2 = گزینه سوم
# 3 = گزینه چهارم
# =========================================================

EMPLOYMENT_QUESTION_BANK = [

    # =====================================================
    # BANKING - EASY
    # =====================================================

    {
        "category": "general",
        "subject": "banking",
        "difficulty": "easy",
        "question": "بانک چیست؟",
        "options": [
            "مؤسسه‌ای برای دریافت و پرداخت و ارائه خدمات مالی",
            "شرکت تولیدکننده کالا",
            "مرجع قانون‌گذاری کشور",
            "شرکت بیمه"
        ],
        "correct": 0,
        "explanation": "بانک یک نهاد مالی است که خدماتی مانند دریافت سپرده، پرداخت تسهیلات و انتقال وجوه ارائه می‌کند."
    },

    {
        "category": "refah",
        "subject": "banking",
        "difficulty": "easy",
        "question": "یکی از وظایف اصلی بانک‌ها کدام است؟",
        "options": [
            "تولید کالا",
            "جمع‌آوری سپرده‌ها و تخصیص منابع",
            "تعیین مالیات",
            "صدور شناسنامه"
        ],
        "correct": 1,
        "explanation": "یکی از مهم‌ترین وظایف بانک‌ها تجهیز و تخصیص منابع مالی است."
    },

    {
        "category": "shahr",
        "subject": "banking",
        "difficulty": "easy",
        "question": "حساب جاری بیشتر برای چه منظوری استفاده می‌شود؟",
        "options": [
            "انجام عملیات دریافت و پرداخت",
            "سرمایه‌گذاری بلندمدت",
            "خرید سهام شرکت‌ها",
            "پرداخت مالیات دولت"
        ],
        "correct": 0,
        "explanation": "حساب جاری برای انجام عملیات روزمره دریافت و پرداخت و استفاده از ابزارهای پرداخت طراحی شده است."
    },

    {
        "category": "mehr",
        "subject": "banking",
        "difficulty": "easy",
        "question": "کدام مورد از خدمات معمول بانکی است؟",
        "options": [
            "انتقال وجه",
            "تولید خودرو",
            "ساخت مسکن",
            "تولید مواد غذایی"
        ],
        "correct": 0,
        "explanation": "انتقال وجه یکی از خدمات پایه شبکه بانکی است."
    },

    # =====================================================
    # BANKING - MEDIUM
    # =====================================================

    {
        "category": "government",
        "subject": "banking",
        "difficulty": "medium",
        "question": "کدام گزینه به مفهوم تجهیز منابع در بانکداری نزدیک‌تر است؟",
        "options": [
            "جمع‌آوری سپرده‌ها و منابع مالی",
            "فروش دارایی‌های ثابت بانک",
            "افزایش هزینه‌های اداری",
            "کاهش تعداد شعب"
        ],
        "correct": 0,
        "explanation": "تجهیز منابع به فرآیند جذب منابع مالی از جمله سپرده‌ها مربوط است."
    },

    {
        "category": "refah",
        "subject": "banking",
        "difficulty": "medium",
        "question": "تخصیص منابع بانکی عمدتاً به چه معناست؟",
        "options": [
            "پرداخت تسهیلات و تأمین مالی فعالیت‌ها",
            "افزایش تعداد کارکنان",
            "خرید تجهیزات اداری",
            "تغییر نام شعب"
        ],
        "correct": 0,
        "explanation": "تخصیص منابع یعنی منابع جذب‌شده در قالب تسهیلات و سایر فعالیت‌های مجاز مالی به متقاضیان اختصاص یابد."
    },

    {
        "category": "shahr",
        "subject": "banking",
        "difficulty": "medium",
        "question": "نقدینگی در اقتصاد معمولاً شامل چه مواردی است؟",
        "options": [
            "فقط اسکناس",
            "فقط سپرده‌های بلندمدت",
            "پول و شبه‌پول",
            "فقط سکه"
        ],
        "correct": 2,
        "explanation": "در تعریف رایج، نقدینگی شامل پول و شبه‌پول است."
    },

    {
        "category": "mehr",
        "subject": "banking",
        "difficulty": "medium",
        "question": "افزایش نرخ بهره معمولاً چه اثری بر هزینه استقراض دارد؟",
        "options": [
            "کاهش می‌دهد",
            "افزایش می‌دهد",
            "هیچ اثری ندارد",
            "همیشه آن را صفر می‌کند"
        ],
        "correct": 1,
        "explanation": "در شرایط معمول، افزایش نرخ بهره هزینه تأمین مالی و استقراض را افزایش می‌دهد."
    },

    # =====================================================
    # BANKING - HARD
    # =====================================================

    {
        "category": "general",
        "subject": "banking",
        "difficulty": "hard",
        "question": "کدام مورد می‌تواند ریسک نقدینگی بانک را افزایش دهد؟",
        "options": [
            "عدم تطابق سررسید دارایی‌ها و بدهی‌ها",
            "افزایش سرمایه بانک",
            "بهبود مدیریت نقدینگی",
            "افزایش دارایی‌های نقد"
        ],
        "correct": 0,
        "explanation": "عدم تطابق سررسید دارایی‌ها و بدهی‌ها می‌تواند توان بانک برای ایفای تعهدات کوتاه‌مدت را تحت فشار قرار دهد."
    },

    {
        "category": "refah",
        "subject": "banking",
        "difficulty": "hard",
        "question": "کدام گزینه بهتر بیانگر ریسک اعتباری است؟",
        "options": [
            "احتمال ناتوانی مشتری در ایفای تعهدات",
            "احتمال خرابی سیستم رایانه‌ای",
            "احتمال تغییر نرخ ارز",
            "احتمال افزایش هزینه برق"
        ],
        "correct": 0,
        "explanation": "ریسک اعتباری به احتمال عدم ایفای تعهدات مالی توسط طرف مقابل مربوط است."
    },

    # =====================================================
    # LAW
    # =====================================================

    {
        "category": "government",
        "subject": "law",
        "difficulty": "easy",
        "question": "قانون عملیات بانکی بدون ربا با چه هدف کلی تدوین شده است؟",
        "options": [
            "تنظیم عملیات بانکی بر اساس موازین مربوط به بانکداری بدون ربا",
            "تعیین نرخ مالیات بر درآمد",
            "تنظیم صادرات کالا",
            "تعیین قوانین راهنمایی و رانندگی"
        ],
        "correct": 0,
        "explanation": "این قانون چارچوب عملیات بانکی بدون ربا در نظام بانکی ایران را مشخص می‌کند."
    },

    {
        "category": "refah",
        "subject": "law",
        "difficulty": "medium",
        "question": "هدف اصلی قوانین مبارزه با پولشویی چیست؟",
        "options": [
            "جلوگیری از ورود و گردش وجوه با منشأ غیرقانونی",
            "افزایش تبلیغات بانکی",
            "افزایش تعداد شعب",
            "کاهش ساعات کاری بانک"
        ],
        "correct": 0,
        "explanation": "قوانین مبارزه با پولشویی برای شناسایی، پیشگیری و مقابله با گردش عواید حاصل از جرم طراحی شده‌اند."
    },

    {
        "category": "government",
        "subject": "law",
        "difficulty": "hard",
        "question": "کدام مورد در چارچوب مبارزه با پولشویی اهمیت بیشتری دارد؟",
        "options": [
            "شناخت مشتری و بررسی معاملات مشکوک",
            "افزایش تبلیغات",
            "کاهش تعداد کارکنان",
            "افزایش دکوراسیون شعب"
        ],
        "correct": 0,
        "explanation": "شناخت مشتری و پایش معاملات از اجزای مهم نظام مبارزه با پولشویی هستند."
    },

    # =====================================================
    # ECONOMICS
    # =====================================================

    {
        "category": "general",
        "subject": "economics",
        "difficulty": "easy",
        "question": "تورم چیست؟",
        "options": [
            "افزایش مستمر و عمومی سطح قیمت‌ها",
            "افزایش قیمت یک کالا",
            "کاهش درآمد دولت",
            "افزایش تولید یک شرکت"
        ],
        "correct": 0,
        "explanation": "تورم به افزایش مستمر و عمومی سطح قیمت کالاها و خدمات گفته می‌شود."
    },

    {
        "category": "shahr",
        "subject": "economics",
        "difficulty": "medium",
        "question": "کدام مورد از عوامل مؤثر بر نرخ ارز است؟",
        "options": [
            "عرضه و تقاضای ارز",
            "تورم",
            "نرخ بهره",
            "همه موارد"
        ],
        "correct": 3,
        "explanation": "نرخ ارز تحت تأثیر مجموعه‌ای از عوامل اقتصادی و انتظارات قرار می‌گیرد."
    },

    {
        "category": "government",
        "subject": "economics",
        "difficulty": "hard",
        "question": "کدام گزینه بیشتر به سیاست پولی مربوط است؟",
        "options": [
            "نرخ‌های سیاستی و مدیریت نقدینگی",
            "بودجه عمرانی دولت",
            "مالیات بر درآمد",
            "مخارج دولت"
        ],
        "correct": 0,
        "explanation": "سیاست پولی از ابزارهای پولی و اعتباری برای اثرگذاری بر اقتصاد استفاده می‌کند."
    },

    # =====================================================
    # MANAGEMENT
    # =====================================================

    {
        "category": "general",
        "subject": "management",
        "difficulty": "easy",
        "question": "کدام گزینه یکی از وظایف اصلی مدیریت است؟",
        "options": [
            "برنامه‌ریزی",
            "تولید اسکناس",
            "صدور گذرنامه",
            "قانون‌گذاری"
        ],
        "correct": 0,
        "explanation": "برنامه‌ریزی از وظایف اصلی مدیریت است."
    },

    {
        "category": "refah",
        "subject": "management",
        "difficulty": "medium",
        "question": "کنترل در مدیریت به چه معناست؟",
        "options": [
            "مقایسه عملکرد واقعی با استانداردها و اصلاح انحرافات",
            "فقط استخدام کارکنان",
            "افزایش هزینه‌ها",
            "حذف برنامه‌ریزی"
        ],
        "correct": 0,
        "explanation": "کنترل شامل سنجش عملکرد، مقایسه با استاندارد و اقدامات اصلاحی است."
    },

    {
        "category": "shahr",
        "subject": "management",
        "difficulty": "hard",
        "question": "در تحلیل SWOT کدام گزینه جزء عوامل داخلی سازمان محسوب می‌شود؟",
        "options": [
            "نقاط قوت و ضعف",
            "فرصت‌ها و تهدیدها",
            "تورم کشور",
            "رقبای خارجی"
        ],
        "correct": 0,
        "explanation": "نقاط قوت و ضعف عوامل داخلی و فرصت‌ها و تهدیدها عوامل محیطی هستند."
    },

    # =====================================================
    # ACCOUNTING
    # =====================================================

    {
        "category": "general",
        "subject": "accounting",
        "difficulty": "easy",
        "question": "معادله اساسی حسابداری کدام است؟",
        "options": [
            "دارایی = بدهی + سرمایه",
            "دارایی = درآمد - هزینه",
            "بدهی = دارایی + سرمایه",
            "سرمایه = دارایی + بدهی"
        ],
        "correct": 0,
        "explanation": "معادله اساسی حسابداری عبارت است از دارایی برابر با بدهی به علاوه سرمایه."
    },

    {
        "category": "refah",
        "subject": "accounting",
        "difficulty": "medium",
        "question": "کدام مورد ماهیت بدهکار دارد؟",
        "options": [
            "دارایی",
            "بدهی",
            "سرمایه",
            "درآمد"
        ],
        "correct": 0,
        "explanation": "حساب‌های دارایی در حالت معمول ماهیت بدهکار دارند."
    },

    {
        "category": "government",
        "subject": "accounting",
        "difficulty": "hard",
        "question": "اگر دارایی‌های یک شرکت افزایش یابد و سایر عوامل ثابت باشند، اثر آن بر سرمایه چگونه است؟",
        "options": [
            "لزوماً سرمایه افزایش می‌یابد",
            "لزوماً سرمایه کاهش می‌یابد",
            "بدون اطلاعات بیشتر نمی‌توان نتیجه قطعی گرفت",
            "سرمایه همیشه صفر می‌شود"
        ],
        "correct": 2,
        "explanation": "افزایش دارایی می‌تواند در مقابل افزایش بدهی یا سرمایه قرار گیرد و بدون دانستن طرف معامله نتیجه قطعی درباره سرمایه ممکن نیست."
    },

    # =====================================================
    # MARKETING
    # =====================================================

    {
        "category": "general",
        "subject": "marketing",
        "difficulty": "easy",
        "question": "بازاریابی بیشتر بر چه موضوعی تمرکز دارد؟",
        "options": [
            "شناخت نیاز مشتری و ایجاد ارزش",
            "فقط تولید محصول",
            "فقط حسابداری",
            "فقط استخدام کارکنان"
        ],
        "correct": 0,
        "explanation": "بازاریابی فرآیندی برای شناخت نیازها، ایجاد ارزش و برقراری ارتباط با بازار هدف است."
    },

    {
        "category": "shahr",
        "subject": "marketing",
        "difficulty": "medium",
        "question": "کدام مورد یکی از عناصر آمیخته بازاریابی سنتی 4P است؟",
        "options": [
            "Product",
            "People",
            "Process",
            "Performance"
        ],
        "correct": 0,
        "explanation": "در مدل 4P، محصول، قیمت، توزیع و ترفیع قرار دارند."
    },

    {
        "category": "refah",
        "subject": "marketing",
        "difficulty": "hard",
        "question": "تقسیم‌بندی بازار با چه هدفی انجام می‌شود؟",
        "options": [
            "شناسایی گروه‌های نسبتاً مشابه مشتریان",
            "حذف تمام مشتریان",
            "افزایش هزینه تولید",
            "کاهش اطلاعات بازار"
        ],
        "correct": 0,
        "explanation": "هدف از بخش‌بندی بازار، شناسایی گروه‌های دارای ویژگی‌ها و نیازهای مشابه برای بازاریابی هدفمند است."
    },

    # =====================================================
    # ICDL
    # =====================================================

    {
        "category": "general",
        "subject": "icdl",
        "difficulty": "easy",
        "question": "کدام نرم‌افزار بیشتر برای محاسبات و جداول استفاده می‌شود؟",
        "options": [
            "Microsoft Excel",
            "Microsoft Word",
            "Paint",
            "Notepad"
        ],
        "correct": 0,
        "explanation": "Excel نرم‌افزار صفحه گسترده و مناسب محاسبات و تحلیل داده است."
    },

    {
        "category": "government",
        "subject": "icdl",
        "difficulty": "medium",
        "question": "میانبر Ctrl+C معمولاً چه عملی انجام می‌دهد؟",
        "options": [
            "کپی",
            "چسباندن",
            "حذف",
            "ذخیره"
        ],
        "correct": 0,
        "explanation": "Ctrl+C برای Copy یا کپی‌کردن استفاده می‌شود."
    },

    {
        "category": "general",
        "subject": "icdl",
        "difficulty": "hard",
        "question": "در Excel، فرمول‌ها معمولاً با چه علامتی آغاز می‌شوند؟",
        "options": [
            "=",
            "+",
            "#",
            "@"
        ],
        "correct": 0,
        "explanation": "فرمول‌های Excel معمولاً با علامت مساوی شروع می‌شوند."
    },

    # =====================================================
    # ENGLISH
    # =====================================================

    {
        "category": "general",
        "subject": "english",
        "difficulty": "easy",
        "question": "معنی کلمه Bank کدام است؟",
        "options": [
            "بانک",
            "بازار",
            "شرکت",
            "فروشگاه"
        ],
        "correct": 0,
        "explanation": "Bank به معنی بانک است."
    },

    {
        "category": "government",
        "subject": "english",
        "difficulty": "medium",
        "question": "کدام گزینه معنی Customer است؟",
        "options": [
            "مشتری",
            "کارمند",
            "مدیر",
            "حسابدار"
        ],
        "correct": 0,
        "explanation": "Customer یعنی مشتری."
    },

    {
        "category": "refah",
        "subject": "english",
        "difficulty": "hard",
        "question": "کدام گزینه نزدیک‌ترین معنی Financial را دارد؟",
        "options": [
            "مالی",
            "حقوقی",
            "بازاریابی",
            "اداری"
        ],
        "correct": 0,
        "explanation": "Financial به امور مالی مربوط است."
    },

    # =====================================================
    # MATH
    # =====================================================

    {
        "category": "general",
        "subject": "math",
        "difficulty": "easy",
        "question": "اگر قیمت کالایی 100 باشد و 10 درصد افزایش یابد، قیمت جدید چقدر است؟",
        "options": [
            "105",
            "110",
            "115",
            "120"
        ],
        "correct": 1,
        "explanation": "10 درصد 100 برابر 10 است، بنابراین قیمت جدید 110 می‌شود."
    },

    {
        "category": "government",
        "subject": "math",
        "difficulty": "medium",
        "question": "اگر 20 درصد مبلغی برابر 40 باشد، کل مبلغ چقدر است؟",
        "options": [
            "100",
            "150",
            "200",
            "250"
        ],
        "correct": 2,
        "explanation": "اگر 20 درصد برابر 40 باشد، 100 درصد برابر 200 خواهد بود."
    },

    {
        "category": "shahr",
        "subject": "math",
        "difficulty": "hard",
        "question": "میانگین اعداد 10، 20، 30 و 40 چند است؟",
        "options": [
            "20",
            "25",
            "30",
            "35"
        ],
        "correct": 1,
        "explanation": "مجموع 100 است و با تقسیم بر 4، میانگین 25 به دست می‌آید."
    },

    # =====================================================
    # INTELLIGENCE
    # =====================================================

    {
        "category": "general",
        "subject": "intelligence",
        "difficulty": "easy",
        "question": "عدد بعدی را پیدا کنید: 2، 4، 6، 8، ؟",
        "options": [
            "9",
            "10",
            "11",
            "12"
        ],
        "correct": 1,
        "explanation": "هر عدد دو واحد بیشتر از عدد قبلی است."
    },

    {
        "category": "refah",
        "subject": "intelligence",
        "difficulty": "medium",
        "question": "عدد بعدی چیست؟ 3، 6، 12، 24، ؟",
        "options": [
            "36",
            "42",
            "48",
            "54"
        ],
        "correct": 2,
        "explanation": "هر عدد دو برابر عدد قبلی است."
    },

    {
        "category": "government",
        "subject": "intelligence",
        "difficulty": "hard",
        "question": "اگر تمام Aها، B باشند و هیچ Bای C نباشد، کدام گزینه درست است؟",
        "options": [
            "هیچ Aای C نیست",
            "تمام Cها A هستند",
            "تمام Bها A هستند",
            "برخی Aها حتماً C هستند"
        ],
        "correct": 0,
        "explanation": "اگر A زیرمجموعه B باشد و B با C اشتراک نداشته باشد، A نیز با C اشتراک ندارد."
    },

]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_all_questions():
    """
    تمام سؤالات بانک را برمی‌گرداند.
    """

    return EMPLOYMENT_QUESTION_BANK.copy()


def get_questions_by_category(category):
    """
    دریافت سؤالات یک بانک خاص.
    """

    return [
        question
        for question in EMPLOYMENT_QUESTION_BANK
        if question["category"] == category
        or (
            category == "general"
            and question["category"] == "general"
        )
    ]


def get_questions_by_difficulty(difficulty):
    """
    دریافت سؤالات بر اساس سطح.
    """

    return [
        question
        for question in EMPLOYMENT_QUESTION_BANK
        if question["difficulty"] == difficulty
    ]


def get_questions_by_subject(subject):
    """
    دریافت سؤالات یک درس خاص.
    """

    return [
        question
        for question in EMPLOYMENT_QUESTION_BANK
        if question["subject"] == subject
    ]


def get_category_questions(category):
    """
    دریافت سؤالات دسته انتخاب‌شده.
    """

    if category == "general":
        return EMPLOYMENT_QUESTION_BANK.copy()

    return [
        question
        for question in EMPLOYMENT_QUESTION_BANK
        if question["category"] == category
    ]


def get_filtered_questions(
    category="general",
    difficulty="all",
    subject="all"
):
    """
    فیلتر حرفه‌ای سؤالات بر اساس:
    بانک + سطح + درس
    """

    questions = []

    for question in EMPLOYMENT_QUESTION_BANK:

        if category != "general":

            if question["category"] != category:
                continue

        if difficulty != "all":

            if question["difficulty"] != difficulty:
                continue

        if subject != "all":

            if question["subject"] != subject:
                continue

        questions.append(question)

    return questions


# =========================================================
# MAIN EMPLOYMENT MENU
# =========================================================

def employment_exam_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🏦 بانک رفاه",
                callback_data="employment_category_refah"
            )
        ],

        [
            InlineKeyboardButton(
                "🏙️ بانک شهر",
                callback_data="employment_category_shahr"
            )
        ],

        [
            InlineKeyboardButton(
                "🤝 بانک مهر",
                callback_data="employment_category_mehr"
            )
        ],

        [
            InlineKeyboardButton(
                "🏛️ بانک‌های دولتی",
                callback_data="employment_category_government"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 بانک جامع سؤالات",
                callback_data="employment_category_general"
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
                "🟢 آزمون آسان",
                callback_data="employment_difficulty_easy"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 آزمون متوسط",
                callback_data="employment_difficulty_medium"
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 آزمون سخت",
                callback_data="employment_difficulty_hard"
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
# INTRO TEXT
# =========================================================

def employment_exam_intro_text():

    total = len(EMPLOYMENT_QUESTION_BANK)

    return f"""
📝 آزمون استخدامی

🏛️ اندیشکده مدیریت و بازار

━━━━━━━━━━━━━━━━━━

🎯 بانک حرفه‌ای سؤالات استخدامی

در این بخش می‌توانید به مجموعه‌ای از
سؤالات تخصصی و عمومی آزمون‌های استخدامی
دسترسی داشته باشید.

━━━━━━━━━━━━━━━━━━

🏦 بانک رفاه
🏙️ بانک شهر
🤝 بانک مهر
🏛️ بانک‌های دولتی

━━━━━━━━━━━━━━━━━━

📊 سطح‌بندی:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

📚 دروس:

🏦 بانکداری
⚖️ قوانین
📚 مدیریت
🧮 حسابداری
💰 اقتصاد
📈 بازاریابی
💻 ICDL
🇬🇧 زبان
➗ ریاضی
🧠 هوش

━━━━━━━━━━━━━━━━━━

📦 تعداد فعلی سؤالات بانک:

{total} سؤال

━━━━━━━━━━━━━━━━━━

🎯 هدف:

تمرین
+
ارزیابی
+
تحلیل اشتباهات
+
آمادگی آزمون استخدامی
"""


# =========================================================
# CATEGORY TEXT
# =========================================================

def employment_category_text(category):

    name = EMPLOYMENT_CATEGORIES.get(
        category,
        "آزمون استخدامی"
    )

    questions = get_category_questions(
        category
    )

    return f"""
{name}

━━━━━━━━━━━━━━━━━━

📊 تعداد سؤالات موجود:

{len(questions)} سؤال

━━━━━━━━━━━━━━━━━━

🎯 سطح‌بندی آزمون:

🟢 آسان
🟡 متوسط
🔴 سخت

━━━━━━━━━━━━━━━━━━

📚 می‌توانید آزمون را
بر اساس سطح انتخاب کنید.

👇 سطح موردنظر را انتخاب کنید.
"""


# =========================================================
# CATEGORY MENU
# =========================================================

def employment_category_menu(category):

    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 آسان",
                callback_data=(
                    f"employment_start_"
                    f"{category}_easy"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 متوسط",
                callback_data=(
                    f"employment_start_"
                    f"{category}_medium"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "🔴 سخت",
                callback_data=(
                    f"employment_start_"
                    f"{category}_hard"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 ترکیبی",
                callback_data=(
                    f"employment_start_"
                    f"{category}_all"
                )
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ آزمون استخدامی",
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

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# DIFFICULTY TEXT
# =========================================================

def employment_difficulty_text(difficulty):

    name = DIFFICULTY_NAMES.get(
        difficulty,
        "آزمون"
    )

    questions = get_questions_by_difficulty(
        difficulty
    )

    return f"""
{name}

━━━━━━━━━━━━━━━━━━

📝 تعداد سؤالات:

{len(questions)} سؤال

━━━━━━━━━━━━━━━━━━

📚 دروس متنوع:

🏦 بانکداری
⚖️ قوانین
📚 مدیریت
🧮 حسابداری
💰 اقتصاد
📈 بازاریابی
💻 ICDL
🇬🇧 زبان
➗ ریاضی
🧠 هوش

━━━━━━━━━━━━━━━━━━

👇 برای شروع آزمون آماده شوید.
"""


# =========================================================
# DIFFICULTY MENU
# =========================================================

def employment_difficulty_menu(difficulty):

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع آزمون",
                callback_data=(
                    f"employment_difficulty_start_"
                    f"{difficulty}"
                )
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

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# SIMULATION
# =========================================================

def employment_simulation_text():

    return """
🎯 آزمون شبیه‌سازی‌شده استخدامی

━━━━━━━━━━━━━━━━━━

این آزمون با ترکیبی از سؤالات
عمومی و تخصصی طراحی شده است.

📚 موضوعات:

🏦 بانکداری
⚖️ قوانین
📚 مدیریت
🧮 حسابداری
💰 اقتصاد
📈 بازاریابی
💻 ICDL
🇬🇧 زبان
➗ ریاضی
🧠 هوش

━━━━━━━━━━━━━━━━━━

📊 ویژگی آزمون:

• سؤالات ترکیبی
• سطح‌های مختلف
• محاسبه درصد
• نمایش پاسخ صحیح
• ارزیابی نهایی

━━━━━━━━━━━━━━━━━━

🎯 هدف:

شبیه‌سازی فضای آزمون استخدامی

━━━━━━━━━━━━━━━━━━

👇 برای شروع:
"""


def employment_simulation_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 شروع آزمون شبیه‌سازی",
                callback_data="employment_simulation_start"
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

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# QUESTION TEXT
# =========================================================

def employment_question_text(
    question,
    index,
    total,
    score
):

    subject = SUBJECT_NAMES.get(
        question["subject"],
        "📚 عمومی"
    )

    difficulty = DIFFICULTY_NAMES.get(
        question["difficulty"],
        "🟡 متوسط"
    )

    return f"""
📝 آزمون استخدامی

━━━━━━━━━━━━━━━━━━

❓ سؤال {index + 1} از {total}

⭐ امتیاز فعلی: {score}

📚 درس: {subject}

🎯 سطح: {difficulty}

━━━━━━━━━━━━━━━━━━

{question["question"]}

━━━━━━━━━━━━━━━━━━

👇 گزینه صحیح را انتخاب کنید:
"""


# =========================================================
# QUESTION KEYBOARD
# =========================================================

def employment_question_keyboard(
    category,
    index,
    score
):

    keyboard = []

    for option_index, option in enumerate(
        category[index]["options"]
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
                "🛑 خروج از آزمون",
                callback_data="employment_exam"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# RESULT TEXT
# =========================================================

def employment_result_text(
    score,
    total
):

    if total == 0:

        return """
❌ آزمونی برای نمایش نتیجه وجود ندارد.
"""

    wrong = total - score

    percentage = round(
        (score / total) * 100
    )

    if percentage >= 90:

        evaluation = "🏆 فوق‌العاده"

        message = (
            "عملکرد شما در سطح بسیار بالایی قرار دارد."
        )

    elif percentage >= 80:

        evaluation = "🥇 عالی"

        message = (
            "عملکرد بسیار خوبی دارید."
        )

    elif percentage >= 70:

        evaluation = "🥈 خوب"

        message = (
            "پایه شما مناسب است، اما هنوز جای پیشرفت دارید."
        )

    elif percentage >= 50:

        evaluation = "🟡 متوسط"

        message = (
            "نیاز به مرور و تمرین بیشتری دارید."
        )

    else:

        evaluation = "📚 نیازمند مطالعه"

        message = (
            "پیشنهاد می‌شود ابتدا درسنامه‌ها را مرور کنید."
        )

    return f"""
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

{message}

━━━━━━━━━━━━━━━━━━

📚 مسیر پیشنهادی:

مطالعه
+
تمرین
+
آزمون
+
تحلیل اشتباهات
+
مرور
"""


# =========================================================
# RESULT MENU
# =========================================================

def employment_result_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 آزمون مجدد",
                callback_data="employment_exam"
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
                "📚 بانک سؤالات",
                callback_data="employment_category_general"
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
# QUESTION SELECTION
# =========================================================

def prepare_exam_questions(
    category="general",
    difficulty="all",
    count=None
):
    """
    آماده‌سازی سؤالات آزمون.

    برای نسخه فعلی سؤال‌ها به ترتیب بانک انتخاب می‌شوند.
    در نسخه بعدی می‌توانیم انتخاب تصادفی،
    جلوگیری از تکرار و سیستم آزمون هوشمند را اضافه کنیم.
    """

    questions = get_filtered_questions(
        category=category,
        difficulty=difficulty
    )

    if count is not None:

        questions = questions[:count]

    return questions


# =========================================================
# SIMULATION QUESTIONS
# =========================================================

def prepare_simulation_questions(
    count=20
):
    """
    آزمون شبیه‌سازی‌شده.

    از کل بانک سؤال انتخاب می‌شود.
    """

    questions = EMPLOYMENT_QUESTION_BANK.copy()

    return questions[:count]


# =========================================================
# STATISTICS
# =========================================================

def employment_statistics():

    total = len(
        EMPLOYMENT_QUESTION_BANK
    )

    statistics = {

        "total": total,

        "categories": {},

        "difficulties": {},

        "subjects": {},

    }

    # -----------------------------------------------------
    # CATEGORIES
    # -----------------------------------------------------

    for category in EMPLOYMENT_CATEGORIES:

        statistics["categories"][category] = len(
            get_category_questions(category)
        )

    # -----------------------------------------------------
    # DIFFICULTIES
    # -----------------------------------------------------

    for difficulty in DIFFICULTY_NAMES:

        statistics["difficulties"][difficulty] = len(
            get_questions_by_difficulty(
                difficulty
            )
        )

    # -----------------------------------------------------
    # SUBJECTS
    # -----------------------------------------------------

    for subject in SUBJECT_NAMES:

        statistics["subjects"][subject] = len(
            get_questions_by_subject(
                subject
            )
        )

    return statistics


# =========================================================
# STATISTICS TEXT
# =========================================================

def employment_statistics_text():

    stats = employment_statistics()

    category_text = ""

    for category, count in stats[
        "categories"
    ].items():

        name = EMPLOYMENT_CATEGORIES.get(
            category,
            category
        )

        category_text += (
            f"{name}: {count}\n"
        )

    difficulty_text = ""

    for difficulty, count in stats[
        "difficulties"
    ].items():

        name = DIFFICULTY_NAMES.get(
            difficulty,
            difficulty
        )

        difficulty_text += (
            f"{name}: {count}\n"
        )

    return f"""
📊 آمار بانک آزمون استخدامی

━━━━━━━━━━━━━━━━━━

📚 مجموع سؤالات:

{stats["total"]} سؤال

━━━━━━━━━━━━━━━━━━

🏦 دسته‌بندی بانک‌ها:

{category_text}

━━━━━━━━━━━━━━━━━━

🎯 سطح سؤالات:

{difficulty_text}

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
"""


# =========================================================
# STATISTICS MENU
# =========================================================

def employment_statistics_menu():

    keyboard = [

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

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# EXPORTS
# =========================================================

__all__ = [

    "EMPLOYMENT_CATEGORIES",

    "DIFFICULTY_NAMES",

    "SUBJECT_NAMES",

    "EMPLOYMENT_QUESTION_BANK",

    "employment_exam_menu",

    "employment_exam_intro_text",

    "employment_category_text",

    "employment_category_menu",

    "employment_difficulty_text",

    "employment_difficulty_menu",

    "employment_simulation_text",

    "employment_simulation_menu",

    "employment_question_text",

    "employment_question_keyboard",

    "employment_result_text",

    "employment_result_menu",

    "prepare_exam_questions",

    "prepare_simulation_questions",

    "employment_statistics",

    "employment_statistics_text",

    "employment_statistics_menu",

    "get_all_questions",

    "get_questions_by_category",

    "get_questions_by_difficulty",

    "get_questions_by_subject",

    "get_filtered_questions",

]
