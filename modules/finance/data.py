"""
Finance Module Curriculum Data
Andishkadeh Management & Market

مدیریت مالی حرفه‌ای و تخصصی

ساختار:
- Module Information
- 12 Chapters
- 48 Lessons
- Lesson Metadata
- Lesson Quiz Bank
- Curriculum Statistics
- Validation
- Health Check
- Compatibility APIs

این فایل با:
    modules.finance.service
    modules.finance.content
    core.content_initializer
هماهنگ طراحی شده است.
"""

from __future__ import annotations

from typing import Any, Dict, List


# ============================================================
# Module Information
# ============================================================

MODULE_ID = "finance"

MODULE_TITLE = "💰 مدیریت مالی حرفه‌ای"

MODULE_DESCRIPTION = (
    "دوره جامع و تخصصی مدیریت مالی شامل مبانی مدیریت مالی، "
    "تحلیل صورت‌های مالی، سرمایه در گردش، نقدینگی، بودجه‌بندی، "
    "ارزش زمانی پول، سرمایه‌گذاری، هزینه سرمایه، تأمین مالی، "
    "ساختار سرمایه، مدیریت ریسک و تصمیم‌گیری مالی."
)

MODULE_LEVEL = "تخصصی → حرفه‌ای → پیشرفته"

MODULE_VERSION = "2.0.0"

MODULE_KEYWORDS = [
    "Financial Management",
    "Corporate Finance",
    "Financial Analysis",
    "Financial Statements",
    "Working Capital",
    "Liquidity",
    "Budgeting",
    "Time Value of Money",
    "Investment",
    "Capital Budgeting",
    "NPV",
    "IRR",
    "Cost of Capital",
    "Financing",
    "Capital Structure",
    "Financial Leverage",
    "Risk Management",
    "Financial Decision Making",
]


# ============================================================
# Chapters
# ============================================================

CHAPTERS: List[Dict[str, Any]] = [
    {
        "id": "finance_ch1",
        "title": "مبانی مدیریت مالی",
        "description": (
            "آشنایی با مفهوم، اهمیت و جایگاه مدیریت مالی در سازمان."
        ),
    },
    {
        "id": "finance_ch2",
        "title": "اهداف و وظایف مدیریت مالی",
        "description": (
            "بررسی اهداف مالی و وظایف اصلی مدیر مالی."
        ),
    },
    {
        "id": "finance_ch3",
        "title": "صورت‌های مالی و تحلیل مالی",
        "description": (
            "آشنایی با صورت‌های مالی و روش‌های تحلیل وضعیت مالی."
        ),
    },
    {
        "id": "finance_ch4",
        "title": "مدیریت سرمایه در گردش",
        "description": (
            "بررسی دارایی‌ها و بدهی‌های جاری و مدیریت سرمایه در گردش."
        ),
    },
    {
        "id": "finance_ch5",
        "title": "مدیریت نقدینگی",
        "description": (
            "بررسی جریان نقدی و روش‌های مدیریت وجوه نقد."
        ),
    },
    {
        "id": "finance_ch6",
        "title": "بودجه‌بندی مالی",
        "description": (
            "آشنایی با بودجه، پیش‌بینی مالی و کنترل بودجه."
        ),
    },
    {
        "id": "finance_ch7",
        "title": "ارزش زمانی پول",
        "description": (
            "آشنایی با ارزش فعلی، ارزش آتی و مفهوم بهره."
        ),
    },
    {
        "id": "finance_ch8",
        "title": "تصمیمات سرمایه‌گذاری",
        "description": (
            "بررسی ارزیابی پروژه‌های سرمایه‌گذاری و تصمیم‌گیری مالی."
        ),
    },
    {
        "id": "finance_ch9",
        "title": "هزینه سرمایه و تأمین مالی",
        "description": (
            "بررسی منابع تأمین مالی و هزینه استفاده از سرمایه."
        ),
    },
    {
        "id": "finance_ch10",
        "title": "ساختار سرمایه",
        "description": (
            "بررسی ترکیب بدهی و حقوق صاحبان سهام."
        ),
    },
    {
        "id": "finance_ch11",
        "title": "مدیریت ریسک مالی",
        "description": (
            "شناخت ریسک‌های مالی و روش‌های کنترل و مدیریت آن‌ها."
        ),
    },
    {
        "id": "finance_ch12",
        "title": "تصمیم‌گیری مالی",
        "description": (
            "بررسی تصمیمات مالی کوتاه‌مدت و بلندمدت مدیران."
        ),
    },
]


# ============================================================
# Lessons
# ============================================================

LESSONS: List[Dict[str, Any]] = [
    {
        "id": "finance_l1",
        "chapter_id": "finance_ch1",
        "title": "مفهوم مدیریت مالی",
        "description": "تعریف مدیریت مالی و نقش آن در سازمان.",
    },
    {
        "id": "finance_l2",
        "chapter_id": "finance_ch1",
        "title": "اهمیت مدیریت مالی",
        "description": "بررسی اهمیت تصمیمات مالی برای سازمان.",
    },
    {
        "id": "finance_l3",
        "chapter_id": "finance_ch1",
        "title": "نقش مدیر مالی",
        "description": "آشنایی با وظایف و مسئولیت‌های مدیر مالی.",
    },
    {
        "id": "finance_l4",
        "chapter_id": "finance_ch1",
        "title": "محیط مالی سازمان",
        "description": "بررسی ارتباط سازمان با بازارها و نهادهای مالی.",
    },

    {
        "id": "finance_l5",
        "chapter_id": "finance_ch2",
        "title": "هدف مدیریت مالی",
        "description": "بررسی اهداف اصلی مدیریت مالی.",
    },
    {
        "id": "finance_l6",
        "chapter_id": "finance_ch2",
        "title": "حداکثرسازی ثروت سهامداران",
        "description": "آشنایی با مفهوم حداکثرسازی ثروت.",
    },
    {
        "id": "finance_l7",
        "chapter_id": "finance_ch2",
        "title": "تصمیمات سرمایه‌گذاری",
        "description": "بررسی تصمیمات مربوط به تخصیص منابع.",
    },
    {
        "id": "finance_l8",
        "chapter_id": "finance_ch2",
        "title": "تصمیمات تأمین مالی",
        "description": "بررسی انتخاب منابع مالی سازمان.",
    },

    {
        "id": "finance_l9",
        "chapter_id": "finance_ch3",
        "title": "ترازنامه",
        "description": "آشنایی با ساختار و اجزای ترازنامه.",
    },
    {
        "id": "finance_l10",
        "chapter_id": "finance_ch3",
        "title": "صورت سود و زیان",
        "description": "بررسی درآمدها، هزینه‌ها و سود.",
    },
    {
        "id": "finance_l11",
        "chapter_id": "finance_ch3",
        "title": "صورت جریان وجوه نقد",
        "description": (
            "بررسی جریان‌های نقدی عملیاتی، سرمایه‌گذاری و تأمین مالی."
        ),
    },
    {
        "id": "finance_l12",
        "chapter_id": "finance_ch3",
        "title": "تحلیل نسبت‌های مالی",
        "description": "آشنایی با نسبت‌های مالی مهم.",
    },

    {
        "id": "finance_l13",
        "chapter_id": "finance_ch4",
        "title": "مفهوم سرمایه در گردش",
        "description": "تعریف سرمایه در گردش و اهمیت آن.",
    },
    {
        "id": "finance_l14",
        "chapter_id": "finance_ch4",
        "title": "دارایی‌های جاری",
        "description": "بررسی وجه نقد، موجودی کالا و حساب‌های دریافتنی.",
    },
    {
        "id": "finance_l15",
        "chapter_id": "finance_ch4",
        "title": "بدهی‌های جاری",
        "description": "بررسی تعهدات کوتاه‌مدت سازمان.",
    },
    {
        "id": "finance_l16",
        "chapter_id": "finance_ch4",
        "title": "چرخه تبدیل وجه نقد",
        "description": "آشنایی با چرخه عملیاتی و تبدیل نقد.",
    },

    {
        "id": "finance_l17",
        "chapter_id": "finance_ch5",
        "title": "مفهوم نقدینگی",
        "description": "تعریف نقدینگی و اهمیت آن.",
    },
    {
        "id": "finance_l18",
        "chapter_id": "finance_ch5",
        "title": "پیش‌بینی جریان نقدی",
        "description": "آشنایی با پیش‌بینی ورود و خروج وجه نقد.",
    },
    {
        "id": "finance_l19",
        "chapter_id": "finance_ch5",
        "title": "مدیریت موجودی نقد",
        "description": "بررسی روش‌های مدیریت موجودی نقد.",
    },
    {
        "id": "finance_l20",
        "chapter_id": "finance_ch5",
        "title": "کسری و مازاد نقدینگی",
        "description": "بررسی راهکارهای مقابله با کسری یا مازاد نقد.",
    },

    {
        "id": "finance_l21",
        "chapter_id": "finance_ch6",
        "title": "مفهوم بودجه",
        "description": "تعریف بودجه و کاربرد آن در سازمان.",
    },
    {
        "id": "finance_l22",
        "chapter_id": "finance_ch6",
        "title": "بودجه عملیاتی",
        "description": "بررسی بودجه مربوط به فعالیت‌های عملیاتی.",
    },
    {
        "id": "finance_l23",
        "chapter_id": "finance_ch6",
        "title": "بودجه نقدی",
        "description": "آشنایی با بودجه دریافت‌ها و پرداخت‌های نقدی.",
    },
    {
        "id": "finance_l24",
        "chapter_id": "finance_ch6",
        "title": "کنترل بودجه",
        "description": "بررسی مقایسه عملکرد واقعی با بودجه.",
    },

    {
        "id": "finance_l25",
        "chapter_id": "finance_ch7",
        "title": "مفهوم ارزش زمانی پول",
        "description": "آشنایی با اصل ارزش زمانی پول.",
    },
    {
        "id": "finance_l26",
        "chapter_id": "finance_ch7",
        "title": "ارزش آتی",
        "description": "محاسبه و مفهوم ارزش آتی جریان‌های مالی.",
    },
    {
        "id": "finance_l27",
        "chapter_id": "finance_ch7",
        "title": "ارزش فعلی",
        "description": "محاسبه و مفهوم ارزش فعلی.",
    },
    {
        "id": "finance_l28",
        "chapter_id": "finance_ch7",
        "title": "بهره ساده و مرکب",
        "description": "مقایسه بهره ساده و مرکب.",
    },

    {
        "id": "finance_l29",
        "chapter_id": "finance_ch8",
        "title": "مفهوم سرمایه‌گذاری",
        "description": "آشنایی با مفهوم سرمایه‌گذاری و پروژه‌های سرمایه‌ای.",
    },
    {
        "id": "finance_l30",
        "chapter_id": "finance_ch8",
        "title": "ارزش فعلی خالص",
        "description": "آشنایی با روش NPV در ارزیابی پروژه‌ها.",
    },
    {
        "id": "finance_l31",
        "chapter_id": "finance_ch8",
        "title": "نرخ بازده داخلی",
        "description": "آشنایی با روش IRR.",
    },
    {
        "id": "finance_l32",
        "chapter_id": "finance_ch8",
        "title": "دوره بازگشت سرمایه",
        "description": "بررسی روش دوره بازگشت سرمایه.",
    },

    {
        "id": "finance_l33",
        "chapter_id": "finance_ch9",
        "title": "مفهوم هزینه سرمایه",
        "description": "آشنایی با هزینه استفاده از منابع مالی.",
    },
    {
        "id": "finance_l34",
        "chapter_id": "finance_ch9",
        "title": "تأمین مالی از طریق بدهی",
        "description": "بررسی تأمین مالی از طریق بدهی.",
    },
    {
        "id": "finance_l35",
        "chapter_id": "finance_ch9",
        "title": "تأمین مالی از طریق حقوق صاحبان سهام",
        "description": "بررسی منابع مالی مبتنی بر حقوق صاحبان سهام.",
    },
    {
        "id": "finance_l36",
        "chapter_id": "finance_ch9",
        "title": "انتخاب منبع تأمین مالی",
        "description": "بررسی معیارهای انتخاب منابع مالی.",
    },

    {
        "id": "finance_l37",
        "chapter_id": "finance_ch10",
        "title": "مفهوم ساختار سرمایه",
        "description": "تعریف ساختار سرمایه.",
    },
    {
        "id": "finance_l38",
        "chapter_id": "finance_ch10",
        "title": "نسبت بدهی",
        "description": "بررسی میزان استفاده از بدهی در ساختار مالی.",
    },
    {
        "id": "finance_l39",
        "chapter_id": "finance_ch10",
        "title": "اهرم مالی",
        "description": "آشنایی با مفهوم اهرم مالی.",
    },
    {
        "id": "finance_l40",
        "chapter_id": "finance_ch10",
        "title": "ساختار سرمایه بهینه",
        "description": "بررسی مفهوم ترکیب مطلوب منابع مالی.",
    },

    {
        "id": "finance_l41",
        "chapter_id": "finance_ch11",
        "title": "مفهوم ریسک مالی",
        "description": "تعریف ریسک و عدم اطمینان مالی.",
    },
    {
        "id": "finance_l42",
        "chapter_id": "finance_ch11",
        "title": "ریسک کسب‌وکار",
        "description": "بررسی ریسک ناشی از فعالیت‌های عملیاتی.",
    },
    {
        "id": "finance_l43",
        "chapter_id": "finance_ch11",
        "title": "ریسک مالی",
        "description": "بررسی ریسک ناشی از ساختار تأمین مالی.",
    },
    {
        "id": "finance_l44",
        "chapter_id": "finance_ch11",
        "title": "روش‌های مدیریت ریسک",
        "description": "آشنایی با روش‌های شناسایی و کنترل ریسک.",
    },

    {
        "id": "finance_l45",
        "chapter_id": "finance_ch12",
        "title": "تصمیمات مالی کوتاه‌مدت",
        "description": "بررسی تصمیمات مالی کوتاه‌مدت.",
    },
    {
        "id": "finance_l46",
        "chapter_id": "finance_ch12",
        "title": "تصمیمات مالی بلندمدت",
        "description": "بررسی تصمیمات مالی بلندمدت.",
    },
    {
        "id": "finance_l47",
        "chapter_id": "finance_ch12",
        "title": "تحلیل و تصمیم‌گیری مالی",
        "description": "استفاده از اطلاعات مالی برای تصمیم‌گیری.",
    },
    {
        "id": "finance_l48",
        "chapter_id": "finance_ch12",
        "title": "جمع‌بندی مدیریت مالی",
        "description": "مرور مفاهیم اصلی مدیریت مالی.",
    },
]


# ============================================================
# Quiz Question Helper
# ============================================================

def _q(
    question: str,
    options: List[str],
    correct_index: int,
) -> Dict[str, Any]:
    """ساخت استاندارد یک سؤال چهارگزینه‌ای."""

    if len(options) != 4:
        raise ValueError(
            "Each finance quiz question must have exactly 4 options."
        )

    if not 0 <= correct_index < 4:
        raise ValueError(
            "correct_index must be between 0 and 3."
        )

    return {
        "question": question,
        "options": list(options),
        "correct_index": correct_index,
    }


# ============================================================
# Finance Quiz Bank
#
# حداقل یک سؤال برای هر درس
# ============================================================

FINANCE_QUIZ_QUESTIONS: Dict[
    tuple[str, str],
    List[Dict[str, Any]],
] = {

    # --------------------------------------------------------
    # Chapter 1
    # --------------------------------------------------------

    ("finance_ch1", "finance_l1"): [
        _q(
            "مهم‌ترین موضوع در مدیریت مالی سازمان چیست؟",
            [
                "تصمیم‌گیری درباره تأمین، تخصیص و استفاده از منابع مالی",
                "تنظیم برنامه حضور کارکنان",
                "مدیریت فرآیند تولید بدون توجه به منابع مالی",
                "کنترل تبلیغات سازمان",
            ],
            0,
        )
    ],

    ("finance_ch1", "finance_l2"): [
        _q(
            "چرا مدیریت مالی برای سازمان اهمیت دارد؟",
            [
                "زیرا تصمیمات مالی بر ارزش، نقدینگی و تداوم فعالیت اثر می‌گذارند",
                "زیرا تمام تصمیمات سازمان فقط مالی هستند",
                "زیرا مدیریت مالی جایگزین مدیریت منابع انسانی است",
                "زیرا مدیریت مالی فقط برای محاسبه حقوق کارکنان استفاده می‌شود",
            ],
            0,
        )
    ],

    ("finance_ch1", "finance_l3"): [
        _q(
            "کدام گزینه یکی از وظایف اصلی مدیر مالی است؟",
            [
                "تحلیل و اتخاذ تصمیمات سرمایه‌گذاری و تأمین مالی",
                "طراحی محصول به‌عنوان تنها وظیفه",
                "تعیین شیفت کارکنان به‌عنوان تنها وظیفه",
                "مدیریت انبار بدون ارتباط با منابع مالی",
            ],
            0,
        )
    ],

    ("finance_ch1", "finance_l4"): [
        _q(
            "محیط مالی سازمان بیشتر با کدام مجموعه ارتباط دارد؟",
            [
                "بازارهای مالی، نهادهای مالی و شرایط اقتصادی",
                "فقط واحد منابع انسانی",
                "فقط واحد تولید",
                "فقط مشتریان داخلی",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 2
    # --------------------------------------------------------

    ("finance_ch2", "finance_l5"): [
        _q(
            "هدف بنیادین مدیریت مالی در رویکرد مالی نوین چیست؟",
            [
                "کمک به افزایش ارزش اقتصادی سازمان",
                "افزایش فروش بدون توجه به هزینه",
                "کاهش دائمی دارایی‌های سازمان",
                "افزایش بدهی بدون توجه به ریسک",
            ],
            0,
        )
    ],

    ("finance_ch2", "finance_l6"): [
        _q(
            "حداکثرسازی ثروت سهامداران بر چه مفهومی تأکید دارد؟",
            [
                "افزایش ارزش اقتصادی سرمایه‌گذاری سهامداران",
                "افزایش تعداد کارکنان",
                "افزایش موجودی کالا بدون توجه به فروش",
                "افزایش هزینه‌های عملیاتی",
            ],
            0,
        )
    ],

    ("finance_ch2", "finance_l7"): [
        _q(
            "تصمیم سرمایه‌گذاری عمدتاً درباره چیست؟",
            [
                "انتخاب پروژه‌ها و دارایی‌هایی که منابع مالی به آن‌ها تخصیص یابد",
                "انتخاب نام تجاری شرکت",
                "تعیین ساختار سازمانی منابع انسانی",
                "تنظیم قراردادهای استخدامی",
            ],
            0,
        )
    ],

    ("finance_ch2", "finance_l8"): [
        _q(
            "تصمیم تأمین مالی به کدام موضوع مربوط است؟",
            [
                "انتخاب ترکیب مناسب منابع مالی مورد نیاز سازمان",
                "تعیین روش بسته‌بندی محصول",
                "انتخاب محل انبار",
                "تعیین ساعات کاری کارکنان",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 3
    # --------------------------------------------------------

    ("finance_ch3", "finance_l9"): [
        _q(
            "ترازنامه در یک تاریخ مشخص چه چیزی را نشان می‌دهد؟",
            [
                "دارایی‌ها، بدهی‌ها و حقوق صاحبان سهام",
                "فقط درآمدهای دوره",
                "فقط جریان‌های نقدی",
                "فقط هزینه‌های عملیاتی",
            ],
            0,
        )
    ],

    ("finance_ch3", "finance_l10"): [
        _q(
            "صورت سود و زیان عمدتاً عملکرد مالی طی چه چیزی را گزارش می‌کند؟",
            [
                "یک دوره مالی",
                "یک لحظه مشخص بدون دوره زمانی",
                "فقط یک روز کاری",
                "فقط زمان تأسیس شرکت",
            ],
            0,
        )
    ],

    ("finance_ch3", "finance_l11"): [
        _q(
            "کدام مورد یکی از طبقات اصلی جریان وجوه نقد است؟",
            [
                "فعالیت‌های عملیاتی",
                "فعالیت‌های منابع انسانی",
                "فعالیت‌های تبلیغاتی",
                "فعالیت‌های اداری بدون جریان نقد",
            ],
            0,
        )
    ],

    ("finance_ch3", "finance_l12"): [
        _q(
            "نسبت جاری برای سنجش کدام موضوع کاربرد بیشتری دارد؟",
            [
                "توان پوشش بدهی‌های جاری با دارایی‌های جاری",
                "سودآوری هر سهم",
                "رشد فروش خارجی",
                "بازده دارایی‌های ثابت",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 4
    # --------------------------------------------------------

    ("finance_ch4", "finance_l13"): [
        _q(
            "سرمایه در گردش خالص معمولاً چگونه محاسبه می‌شود؟",
            [
                "دارایی‌های جاری منهای بدهی‌های جاری",
                "دارایی‌های ثابت منهای بدهی‌های بلندمدت",
                "فروش منهای هزینه",
                "وجه نقد منهای سرمایه ثبت‌شده",
            ],
            0,
        )
    ],

    ("finance_ch4", "finance_l14"): [
        _q(
            "کدام گزینه یک دارایی جاری محسوب می‌شود؟",
            [
                "حساب‌های دریافتنی",
                "زمین",
                "ساختمان",
                "سرمایه‌گذاری بلندمدت",
            ],
            0,
        )
    ],

    ("finance_ch4", "finance_l15"): [
        _q(
            "بدهی جاری معمولاً چه ویژگی دارد؟",
            [
                "انتظار می‌رود در چرخه عملیاتی یا کوتاه‌مدت تسویه شود",
                "همیشه بیش از ده سال سررسید دارد",
                "جزء حقوق صاحبان سهام است",
                "هرگز نیاز به پرداخت ندارد",
            ],
            0,
        )
    ],

    ("finance_ch4", "finance_l16"): [
        _q(
            "چرخه تبدیل وجه نقد چه چیزی را اندازه‌گیری می‌کند؟",
            [
                "مدت زمانی که منابع نقدی در چرخه عملیاتی درگیر می‌شوند",
                "نرخ مالیات شرکت",
                "تعداد کارکنان شرکت",
                "ارزش دفتری دارایی ثابت",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 5
    # --------------------------------------------------------

    ("finance_ch5", "finance_l17"): [
        _q(
            "نقدینگی به چه مفهومی اشاره دارد؟",
            [
                "توان ایفای تعهدات کوتاه‌مدت با منابع نقدشونده",
                "توان افزایش قیمت سهام",
                "توان افزایش تولید بدون سرمایه",
                "توان کاهش مالیات بدون تغییر عملیات",
            ],
            0,
        )
    ],

    ("finance_ch5", "finance_l18"): [
        _q(
            "هدف اصلی پیش‌بینی جریان نقدی چیست؟",
            [
                "برآورد زمان و مقدار ورود و خروج وجه نقد",
                "پیش‌بینی تعداد کارکنان",
                "تعیین نرخ استهلاک دارایی ثابت",
                "محاسبه ارزش اسمی سهام",
            ],
            0,
        )
    ],

    ("finance_ch5", "finance_l19"): [
        _q(
            "نگهداری وجه نقد بیش از نیاز عملیاتی چه اثری می‌تواند داشته باشد؟",
            [
                "ایجاد هزینه فرصت برای منابع بلااستفاده",
                "حذف کامل ریسک مالی",
                "افزایش خودکار سودآوری",
                "افزایش خودکار فروش",
            ],
            0,
        )
    ],

    ("finance_ch5", "finance_l20"): [
        _q(
            "در شرایط کسری نقدینگی، کدام اقدام می‌تواند منطقی باشد؟",
            [
                "مدیریت دریافت‌ها، پرداخت‌ها و استفاده مناسب از منابع تأمین مالی",
                "افزایش همه هزینه‌ها",
                "خرید دارایی‌های غیرضروری",
                "افزایش موجودی نقد بدون بررسی منابع",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 6
    # --------------------------------------------------------

    ("finance_ch6", "finance_l21"): [
        _q(
            "بودجه چیست؟",
            [
                "برنامه کمی و مالی برای فعالیت‌ها و منابع طی یک دوره مشخص",
                "گزارش عملکرد گذشته بدون برنامه آینده",
                "صورت وضعیت کارکنان",
                "فهرست دارایی‌های ثابت",
            ],
            0,
        )
    ],

    ("finance_ch6", "finance_l22"): [
        _q(
            "بودجه عملیاتی بیشتر بر چه چیزی تمرکز دارد؟",
            [
                "فعالیت‌های اصلی و عملیاتی سازمان",
                "فقط ساختار سرمایه",
                "فقط سرمایه‌گذاری بلندمدت",
                "فقط بدهی‌های بلندمدت",
            ],
            0,
        )
    ],

    ("finance_ch6", "finance_l23"): [
        _q(
            "بودجه نقدی بیشتر چه چیزی را پیش‌بینی می‌کند؟",
            [
                "دریافت‌ها و پرداخت‌های نقدی",
                "فقط سود حسابداری",
                "فقط استهلاک",
                "فقط تعداد کارکنان",
            ],
            0,
        )
    ],

    ("finance_ch6", "finance_l24"): [
        _q(
            "کنترل بودجه بر چه مبنایی انجام می‌شود؟",
            [
                "مقایسه عملکرد واقعی با مقادیر بودجه‌ای",
                "مقایسه کارکنان با رقبا",
                "مقایسه دارایی ثابت با فروش",
                "مقایسه قیمت سهام با مالیات",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 7
    # --------------------------------------------------------

    ("finance_ch7", "finance_l25"): [
        _q(
            "اصل ارزش زمانی پول بیانگر چیست؟",
            [
                "ارزش یک مبلغ به زمان دریافت یا پرداخت آن وابسته است",
                "ارزش پول در همه زمان‌ها همیشه یکسان است",
                "تورم هیچ اثری بر پول ندارد",
                "پول آینده همیشه ارزش بیشتری دارد",
            ],
            0,
        )
    ],

    ("finance_ch7", "finance_l26"): [
        _q(
            "ارزش آتی یک مبلغ به چه معناست؟",
            [
                "ارزش آن مبلغ در یک زمان آینده با درنظرگرفتن نرخ بازده",
                "ارزش تاریخی مبلغ",
                "ارزش اسمی بدون توجه به زمان",
                "ارزش دفتری دارایی",
            ],
            0,
        )
    ],

    ("finance_ch7", "finance_l27"): [
        _q(
            "ارزش فعلی یک جریان نقدی آینده چه مفهومی دارد؟",
            [
                "ارزش امروز جریان نقدی آینده پس از تنزیل",
                "مقدار اسمی جریان نقدی بدون تنزیل",
                "ارزش دفتری دارایی",
                "مبلغ فروش آینده بدون نرخ تنزیل",
            ],
            0,
        )
    ],

    ("finance_ch7", "finance_l28"): [
        _q(
            "در بهره مرکب، بهره دوره‌های قبل چه وضعیتی دارد؟",
            [
                "می‌تواند خود نیز در دوره‌های بعدی مبنای محاسبه بهره قرار گیرد",
                "همیشه از اصل پول جدا می‌شود",
                "هرگز دوباره محاسبه نمی‌شود",
                "فقط در اولین دوره محاسبه می‌شود",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 8
    # --------------------------------------------------------

    ("finance_ch8", "finance_l29"): [
        _q(
            "سرمایه‌گذاری مالی در مدیریت مالی معمولاً به چه معناست؟",
            [
                "تخصیص منابع با انتظار دریافت منافع اقتصادی آینده",
                "مصرف منابع بدون انتظار منفعت",
                "افزایش هزینه‌های جاری",
                "کاهش دائمی دارایی‌ها",
            ],
            0,
        )
    ],

    ("finance_ch8", "finance_l30"): [
        _q(
            "در روش NPV، پروژه‌ای که NPV مثبت دارد از نظر معیار NPV چه وضعیتی دارد؟",
            [
                "ارزش اقتصادی ایجاد می‌کند و در شرایط سایر فرض‌های ثابت قابل پذیرش است",
                "حتماً زیان‌ده است",
                "هیچ جریان نقدی ندارد",
                "حتماً باید رد شود",
            ],
            0,
        )
    ],

    ("finance_ch8", "finance_l31"): [
        _q(
            "IRR به چه مفهومی اشاره دارد؟",
            [
                "نرخی که NPV پروژه را برابر صفر می‌کند",
                "نرخ مالیات شرکت",
                "نرخ رشد فروش",
                "نرخ استهلاک",
            ],
            0,
        )
    ],

    ("finance_ch8", "finance_l32"): [
        _q(
            "دوره بازگشت سرمایه چه چیزی را اندازه می‌گیرد؟",
            [
                "مدت زمان لازم برای بازیابی سرمایه اولیه از جریان‌های نقدی",
                "نرخ بازده داخلی",
                "هزینه سرمایه",
                "نرخ تورم",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 9
    # --------------------------------------------------------

    ("finance_ch9", "finance_l33"): [
        _q(
            "هزینه سرمایه به چه مفهومی مربوط است؟",
            [
                "حداقل بازده مورد انتظار برای تأمین‌کنندگان منابع مالی",
                "هزینه حقوق کارکنان",
                "هزینه تبلیغات",
                "هزینه خرید موجودی کالا",
            ],
            0,
        )
    ],

    ("finance_ch9", "finance_l34"): [
        _q(
            "یکی از ویژگی‌های اصلی تأمین مالی از طریق بدهی چیست؟",
            [
                "ایجاد تعهد قراردادی برای پرداخت اصل و هزینه تأمین مالی",
                "حذف کامل تعهدات",
                "عدم وجود هیچ‌گونه ریسک",
                "افزایش خودکار حقوق صاحبان سهام",
            ],
            0,
        )
    ],

    ("finance_ch9", "finance_l35"): [
        _q(
            "تأمین مالی از طریق حقوق صاحبان سهام چه تفاوت اساسی با بدهی دارد؟",
            [
                "معمولاً تعهد قراردادی مشابه بدهی برای پرداخت اصل سرمایه ندارد",
                "همیشه هزینه کمتری از بدهی دارد",
                "هیچ ریسکی ندارد",
                "باعث حذف کامل مالکیت سهامداران می‌شود",
            ],
            0,
        )
    ],

    ("finance_ch9", "finance_l36"): [
        _q(
            "انتخاب منبع تأمین مالی باید بر اساس چه عواملی انجام شود؟",
            [
                "هزینه، ریسک، انعطاف‌پذیری، سررسید و شرایط مالی سازمان",
                "فقط اندازه شرکت",
                "فقط تعداد کارکنان",
                "فقط قیمت محصول",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 10
    # --------------------------------------------------------

    ("finance_ch10", "finance_l37"): [
        _q(
            "ساختار سرمایه به چه ترکیبی اشاره دارد؟",
            [
                "ترکیب منابع مالی بلندمدت مانند بدهی و حقوق صاحبان سهام",
                "ترکیب کارکنان سازمان",
                "ترکیب محصولات شرکت",
                "ترکیب دارایی‌های جاری",
            ],
            0,
        )
    ],

    ("finance_ch10", "finance_l38"): [
        _q(
            "افزایش نسبت بدهی در ساختار مالی معمولاً چه اثری دارد؟",
            [
                "می‌تواند ریسک مالی و تعهدات ثابت شرکت را افزایش دهد",
                "همیشه ریسک را حذف می‌کند",
                "همیشه سود را افزایش می‌دهد",
                "همیشه هزینه سرمایه را صفر می‌کند",
            ],
            0,
        )
    ],

    ("finance_ch10", "finance_l39"): [
        _q(
            "اهرم مالی بیشتر با کدام موضوع ارتباط دارد؟",
            [
                "استفاده از منابع دارای هزینه ثابت مانند بدهی",
                "افزایش موجودی کالا",
                "افزایش تعداد کارکنان",
                "افزایش فروش نقدی",
            ],
            0,
        )
    ],

    ("finance_ch10", "finance_l40"): [
        _q(
            "ساختار سرمایه بهینه به چه ترکیبی اشاره دارد؟",
            [
                "ترکیبی که با توجه به شرایط، هزینه سرمایه و ریسک را به شکل مطلوب مدیریت کند",
                "بیشترین مقدار ممکن بدهی",
                "کمترین مقدار ممکن دارایی",
                "بیشترین هزینه تأمین مالی",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 11
    # --------------------------------------------------------

    ("finance_ch11", "finance_l41"): [
        _q(
            "ریسک مالی به چه معناست؟",
            [
                "عدم اطمینان درباره نتایج مالی و توان ایفای تعهدات مالی",
                "فقط احتمال کاهش فروش",
                "فقط خرابی تجهیزات",
                "فقط تغییر تعداد کارکنان",
            ],
            0,
        )
    ],

    ("finance_ch11", "finance_l42"): [
        _q(
            "ریسک کسب‌وکار عمدتاً از چه چیزی ناشی می‌شود؟",
            [
                "عدم اطمینان در فعالیت‌های عملیاتی و درآمدهای کسب‌وکار",
                "فقط میزان بدهی",
                "فقط نرخ بهره بدهی",
                "فقط ساختار سرمایه",
            ],
            0,
        )
    ],

    ("finance_ch11", "finance_l43"): [
        _q(
            "ریسک مالی در یک شرکت دارای بدهی معمولاً با چه چیزی ارتباط دارد؟",
            [
                "تعهدات ثابت ناشی از تأمین مالی و ساختار سرمایه",
                "تعداد محصولات",
                "تعداد مشتریان",
                "موجودی کالا به‌تنهایی",
            ],
            0,
        )
    ],

    ("finance_ch11", "finance_l44"): [
        _q(
            "نخستین گام منطقی در مدیریت ریسک چیست؟",
            [
                "شناسایی و ارزیابی ریسک‌ها",
                "نادیده‌گرفتن ریسک",
                "افزایش همه هزینه‌ها",
                "حذف اطلاعات مالی",
            ],
            0,
        )
    ],

    # --------------------------------------------------------
    # Chapter 12
    # --------------------------------------------------------

    ("finance_ch12", "finance_l45"): [
        _q(
            "کدام مورد نمونه‌ای از تصمیم مالی کوتاه‌مدت است؟",
            [
                "مدیریت سرمایه در گردش و نقدینگی",
                "انتخاب ساختار بلندمدت سرمایه",
                "ارزیابی خرید یک شرکت برای ده سال آینده",
                "تعیین سیاست بلندمدت سرمایه‌گذاری",
            ],
            0,
        )
    ],

    ("finance_ch12", "finance_l46"): [
        _q(
            "کدام مورد نمونه‌ای از تصمیم مالی بلندمدت است؟",
            [
                "ارزیابی پروژه سرمایه‌گذاری بلندمدت",
                "پرداخت قبض جاری",
                "تنظیم موجودی روزانه صندوق",
                "پیگیری یک دریافت کوتاه‌مدت",
            ],
            0,
        )
    ],

    ("finance_ch12", "finance_l47"): [
        _q(
            "تصمیم‌گیری مالی حرفه‌ای باید بر چه چیزی تکیه داشته باشد؟",
            [
                "تحلیل جریان‌های نقدی، ریسک، بازده و اطلاعات مالی مرتبط",
                "حدس و گمان بدون اطلاعات",
                "فقط میزان فروش",
                "فقط مقدار دارایی ثابت",
            ],
            0,
        )
    ],

    ("finance_ch12", "finance_l48"): [
        _q(
            "کدام مجموعه، هسته اصلی مدیریت مالی را بهتر نشان می‌دهد؟",
            [
                "سرمایه‌گذاری، تأمین مالی، سرمایه در گردش و مدیریت ریسک",
                "فقط فروش و تبلیغات",
                "فقط منابع انسانی",
                "فقط حسابداری حقوق کارکنان",
            ],
            0,
        )
    ],
}


# ============================================================
# Compatibility Alias
# ============================================================

FINANCE_CHAPTERS = CHAPTERS
FINANCE_LESSONS = LESSONS
FINANCE_QUIZ = FINANCE_QUIZ_QUESTIONS


# ============================================================
# Module Information API
# ============================================================

def get_module_info() -> Dict[str, Any]:
    """Return complete Finance module information."""

    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "title": MODULE_TITLE,
        "description": MODULE_DESCRIPTION,
        "level": MODULE_LEVEL,
        "version": MODULE_VERSION,
        "keywords": list(MODULE_KEYWORDS),
        "chapter_count": len(CHAPTERS),
        "lesson_count": len(LESSONS),
        "quiz_count": len(
            get_all_quiz_questions()
        ),
    }


# ============================================================
# Chapter API
# ============================================================

def get_chapters() -> List[Dict[str, Any]]:
    """Return all chapters."""

    return [
        dict(chapter)
        for chapter in CHAPTERS
    ]


def get_chapter(
    chapter_id: str,
) -> Dict[str, Any] | None:
    """Return one chapter by ID."""

    chapter_id = str(
        chapter_id or ""
    ).strip()

    for chapter in CHAPTERS:
        if chapter["id"] == chapter_id:
            return dict(chapter)

    return None


# ============================================================
# Lesson API
# ============================================================

def get_lessons() -> List[Dict[str, Any]]:
    """Return all lessons."""

    return [
        dict(lesson)
        for lesson in LESSONS
    ]


def get_chapter_lessons(
    chapter_id: str,
) -> List[Dict[str, Any]]:
    """Return lessons belonging to one chapter."""

    chapter_id = str(
        chapter_id or ""
    ).strip()

    return [
        dict(lesson)
        for lesson in LESSONS
        if lesson.get("chapter_id") == chapter_id
    ]


def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> Dict[str, Any] | None:
    """Return one lesson by chapter and lesson ID."""

    chapter_id = str(
        chapter_id or ""
    ).strip()

    lesson_id = str(
        lesson_id or ""
    ).strip()

    for lesson in LESSONS:
        if (
            lesson.get("chapter_id") == chapter_id
            and lesson.get("id") == lesson_id
        ):
            return dict(lesson)

    return None


# ============================================================
# Quiz API
# ============================================================

def get_quiz(
    chapter_id: str,
    lesson_id: str,
) -> List[Dict[str, Any]]:
    """
    Return quiz questions for one lesson.
    """

    chapter_id = str(
        chapter_id or ""
    ).strip()

    lesson_id = str(
        lesson_id or ""
    ).strip()

    questions = FINANCE_QUIZ_QUESTIONS.get(
        (chapter_id, lesson_id),
        [],
    )

    return [
        dict(question)
        for question in questions
    ]


def get_chapter_quiz(
    chapter_id: str,
) -> List[Dict[str, Any]]:
    """
    Return all quiz questions belonging to a chapter.
    """

    chapter_id = str(
        chapter_id or ""
    ).strip()

    questions: List[Dict[str, Any]] = []

    for lesson in get_chapter_lessons(
        chapter_id
    ):
        lesson_id = lesson.get("id")

        if not lesson_id:
            continue

        for question in get_quiz(
            chapter_id,
            lesson_id,
        ):
            item = dict(question)

            item["chapter_id"] = chapter_id
            item["lesson_id"] = lesson_id

            questions.append(item)

    return questions


def get_all_quiz_questions() -> List[Dict[str, Any]]:
    """
    Return all Finance quiz questions.

    Every question includes:
        chapter_id
        lesson_id
        question
        options
        correct_index
    """

    questions: List[Dict[str, Any]] = []

    for (
        chapter_id,
        lesson_id,
    ), values in FINANCE_QUIZ_QUESTIONS.items():

        for question in values:
            item = dict(question)

            item["chapter_id"] = chapter_id
            item["lesson_id"] = lesson_id

            questions.append(item)

    return questions


# ============================================================
# Quiz Statistics
# ============================================================

def get_quiz_statistics() -> Dict[str, Any]:
    """Return quiz statistics."""

    all_questions = get_all_quiz_questions()

    lessons_with_quiz = len(
        {
            (
                question.get("chapter_id"),
                question.get("lesson_id"),
            )
            for question in all_questions
        }
    )

    chapters_with_quiz = len(
        {
            question.get("chapter_id")
            for question in all_questions
        }
    )

    return {
        "module_id": MODULE_ID,
        "questions": len(all_questions),
        "lessons_with_quiz": lessons_with_quiz,
        "chapters_with_quiz": chapters_with_quiz,
        "average_questions_per_lesson": (
            round(
                len(all_questions) / len(LESSONS),
                2,
            )
            if LESSONS
            else 0
        ),
    }


# ============================================================
# Curriculum Statistics
# ============================================================

def get_curriculum_statistics() -> Dict[str, Any]:
    """Return curriculum statistics."""

    quiz_statistics = get_quiz_statistics()

    return {
        "module_id": MODULE_ID,
        "module_title": MODULE_TITLE,
        "chapters": len(CHAPTERS),
        "lessons": len(LESSONS),
        "quiz_questions": quiz_statistics[
            "questions"
        ],
        "lessons_with_quiz": quiz_statistics[
            "lessons_with_quiz"
        ],
        "chapters_with_quiz": quiz_statistics[
            "chapters_with_quiz"
        ],
    }


def get_statistics() -> Dict[str, Any]:
    """Compatibility alias."""

    return get_curriculum_statistics()


# ============================================================
# Validation
# ============================================================

def validate_curriculum() -> Dict[str, Any]:
    """
    Comprehensive Finance curriculum validation.
    """

    errors: List[str] = []
    warnings: List[str] = []

    # --------------------------------------------------------
    # Module
    # --------------------------------------------------------

    if not MODULE_ID.strip():
        errors.append(
            "MODULE_ID is empty."
        )

    if not MODULE_TITLE.strip():
        errors.append(
            "MODULE_TITLE is empty."
        )

    if not MODULE_DESCRIPTION.strip():
        errors.append(
            "MODULE_DESCRIPTION is empty."
        )

    # --------------------------------------------------------
    # Chapters
    # --------------------------------------------------------

    if len(CHAPTERS) != 12:
        errors.append(
            f"Expected 12 chapters, found {len(CHAPTERS)}."
        )

    chapter_ids: List[str] = []

    for index, chapter in enumerate(
        CHAPTERS,
        start=1,
    ):
        chapter_id = str(
            chapter.get("id", "")
        ).strip()

        title = str(
            chapter.get("title", "")
        ).strip()

        if not chapter_id:
            errors.append(
                f"Chapter #{index} has no ID."
            )

        if not title:
            errors.append(
                f"Chapter #{index} has no title."
            )

        if chapter_id:
            chapter_ids.append(
                chapter_id
            )

    duplicate_chapter_ids = sorted(
        {
            chapter_id
            for chapter_id in chapter_ids
            if chapter_ids.count(chapter_id) > 1
        }
    )

    if duplicate_chapter_ids:
        errors.append(
            "Duplicate chapter IDs: "
            f"{duplicate_chapter_ids}"
        )

    # --------------------------------------------------------
    # Lessons
    # --------------------------------------------------------

    if len(LESSONS) != 48:
        errors.append(
            f"Expected 48 lessons, found {len(LESSONS)}."
        )

    lesson_ids: List[str] = []
    lessons_per_chapter: Dict[str, int] = {}

    for index, lesson in enumerate(
        LESSONS,
        start=1,
    ):
        lesson_id = str(
            lesson.get("id", "")
        ).strip()

        chapter_id = str(
            lesson.get("chapter_id", "")
        ).strip()

        title = str(
            lesson.get("title", "")
        ).strip()

        if not lesson_id:
            errors.append(
                f"Lesson #{index} has no ID."
            )
        else:
            lesson_ids.append(
                lesson_id
            )

        if not chapter_id:
            errors.append(
                f"Lesson '{lesson_id}' has no chapter_id."
            )

        elif chapter_id not in chapter_ids:
            errors.append(
                f"Lesson '{lesson_id}' references "
                f"unknown chapter '{chapter_id}'."
            )

        else:
            lessons_per_chapter[
                chapter_id
            ] = (
                lessons_per_chapter.get(
                    chapter_id,
                    0,
                )
                + 1
            )

        if not title:
            errors.append(
                f"Lesson '{lesson_id}' has no title."
            )

    duplicate_lesson_ids = sorted(
        {
            lesson_id
            for lesson_id in lesson_ids
            if lesson_ids.count(lesson_id) > 1
        }
    )

    if duplicate_lesson_ids:
        errors.append(
            "Duplicate lesson IDs: "
            f"{duplicate_lesson_ids}"
        )

    # --------------------------------------------------------
    # Four lessons per chapter
    # --------------------------------------------------------

    for chapter_id in chapter_ids:
        count = lessons_per_chapter.get(
            chapter_id,
            0,
        )

        if count != 4:
            errors.append(
                f"Chapter '{chapter_id}' "
                f"should contain 4 lessons, found {count}."
            )

    # --------------------------------------------------------
    # Sequential IDs
    # --------------------------------------------------------

    expected_chapters = {
        f"finance_ch{number}"
        for number in range(1, 13)
    }

    actual_chapters = set(
        chapter_ids
    )

    missing_chapters = sorted(
        expected_chapters - actual_chapters
    )

    unexpected_chapters = sorted(
        actual_chapters - expected_chapters
    )

    if missing_chapters:
        errors.append(
            f"Missing chapter IDs: {missing_chapters}"
        )

    if unexpected_chapters:
        errors.append(
            f"Unexpected chapter IDs: {unexpected_chapters}"
        )

    expected_lessons = {
        f"finance_l{number}"
        for number in range(1, 49)
    }

    actual_lessons = set(
        lesson_ids
    )

    missing_lessons = sorted(
        expected_lessons - actual_lessons
    )

    unexpected_lessons = sorted(
        actual_lessons - expected_lessons
    )

    if missing_lessons:
        errors.append(
            f"Missing lesson IDs: {missing_lessons}"
        )

    if unexpected_lessons:
        errors.append(
            f"Unexpected lesson IDs: {unexpected_lessons}"
        )

    # --------------------------------------------------------
    # Quiz validation
    # --------------------------------------------------------

    if not FINANCE_QUIZ_QUESTIONS:
        errors.append(
            "Finance quiz bank is empty."
        )

    lesson_quiz_keys = set(
        FINANCE_QUIZ_QUESTIONS.keys()
    )

    for lesson in LESSONS:
        chapter_id = lesson.get(
            "chapter_id"
        )

        lesson_id = lesson.get(
            "id"
        )

        key = (
            chapter_id,
            lesson_id,
        )

        if key not in lesson_quiz_keys:
            warnings.append(
                f"No quiz found for lesson '{lesson_id}'."
            )

    for key, questions in (
        FINANCE_QUIZ_QUESTIONS.items()
    ):
        if not isinstance(key, tuple):
            errors.append(
                f"Invalid quiz key: {key}"
            )
            continue

        if len(key) != 2:
            errors.append(
                f"Invalid quiz key length: {key}"
            )
            continue

        chapter_id, lesson_id = key

        if chapter_id not in actual_chapters:
            errors.append(
                f"Quiz references unknown chapter: "
                f"{chapter_id}"
            )

        if lesson_id not in actual_lessons:
            errors.append(
                f"Quiz references unknown lesson: "
                f"{lesson_id}"
            )

        if not isinstance(
            questions,
            list,
        ):
            errors.append(
                f"Quiz for '{lesson_id}' is not a list."
            )
            continue

        if not questions:
            warnings.append(
                f"Quiz for '{lesson_id}' is empty."
            )

        for index, question in enumerate(
            questions,
            start=1,
        ):
            if not isinstance(
                question,
                dict,
            ):
                errors.append(
                    f"Quiz question #{index} "
                    f"for '{lesson_id}' is invalid."
                )
                continue

            question_text = str(
                question.get(
                    "question",
                    "",
                )
            ).strip()

            options = question.get(
                "options",
                [],
            )

            correct_index = question.get(
                "correct_index"
            )

            if not question_text:
                errors.append(
                    f"Empty quiz question for "
                    f"'{lesson_id}'."
                )

            if not isinstance(
                options,
                list,
            ):
                errors.append(
                    f"Options for '{lesson_id}' "
                    f"must be a list."
                )
                continue

            if len(options) != 4:
                errors.append(
                    f"Quiz question for '{lesson_id}' "
                    f"must have exactly 4 options."
                )

            if not isinstance(
                correct_index,
                int,
            ):
                errors.append(
                    f"Invalid correct_index for "
                    f"'{lesson_id}'."
                )

            elif not 0 <= correct_index < len(options):
                errors.append(
                    f"correct_index out of range "
                    f"for '{lesson_id}'."
                )

            for option in options:
                if not str(
                    option
                ).strip():
                    errors.append(
                        f"Empty option in quiz for "
                        f"'{lesson_id}'."
                    )

    return {
        "module": MODULE_ID,
        "status": (
            "ok"
            if not errors
            else "error"
        ),
        "valid": not errors,
        "chapters": len(CHAPTERS),
        "lessons": len(LESSONS),
        "lessons_per_chapter": lessons_per_chapter,
        "quiz_questions": len(
            get_all_quiz_questions()
        ),
        "errors": errors,
        "warnings": warnings,
    }


# ============================================================
# Health Check
# ============================================================

def data_health_check() -> bool:
    """
    Boolean health check used by the central system.
    """

    result = validate_curriculum()

    return result["valid"]


def finance_health_check() -> Dict[str, Any]:
    """
    Detailed Finance health check.
    """

    validation = validate_curriculum()

    return {
        "module_id": MODULE_ID,
        "status": (
            "healthy"
            if validation["valid"]
            else "error"
        ),
        "valid": validation["valid"],
        "chapters": validation["chapters"],
        "lessons": validation["lessons"],
        "quizzes": validation[
            "quiz_questions"
        ],
        "errors": validation["errors"],
        "warnings": validation["warnings"],
    }


# ============================================================
# Compatibility API
# ============================================================

get_all_lessons = get_lessons
get_all_questions = get_all_quiz_questions
get_quizzes = get_all_quiz_questions
get_chapters_list = get_chapters
get_lessons_list = get_lessons


# ============================================================
# Public API
# ============================================================

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "MODULE_LEVEL",
    "MODULE_VERSION",
    "MODULE_KEYWORDS",

    "CHAPTERS",
    "LESSONS",

    "FINANCE_CHAPTERS",
    "FINANCE_LESSONS",
    "FINANCE_QUIZ_QUESTIONS",
    "FINANCE_QUIZ",

    "get_module_info",

    "get_chapters",
    "get_chapter",

    "get_lessons",
    "get_chapter_lessons",
    "get_lesson",
    "get_all_lessons",

    "get_quiz",
    "get_chapter_quiz",
    "get_all_quiz_questions",
    "get_all_questions",
    "get_quiz_statistics",

    "get_curriculum_statistics",
    "get_statistics",

    "validate_curriculum",
    "data_health_check",
    "finance_health_check",
]


# ============================================================
# Local Test
# ============================================================

if __name__ == "__main__":

    print("Finance Module")
    print("=" * 60)

    print(
        f"Module ID: {MODULE_ID}"
    )

    print(
        f"Title: {MODULE_TITLE}"
    )

    print(
        f"Version: {MODULE_VERSION}"
    )

    print()

    statistics = get_curriculum_statistics()

    print("Curriculum Statistics")
    print("-" * 60)

    for key, value in statistics.items():
        print(
            f"{key}: {value}"
        )

    print()

    quiz_statistics = get_quiz_statistics()

    print("Quiz Statistics")
    print("-" * 60)

    for key, value in quiz_statistics.items():
        print(
            f"{key}: {value}"
        )

    print()

    validation = validate_curriculum()

    print("Validation")
    print("-" * 60)

    print(
        f"Status: {validation['status']}"
    )

    print(
        f"Valid: {validation['valid']}"
    )

    if validation["errors"]:
        print()
        print("Errors:")

        for error in validation["errors"]:
            print(
                f"- {error}"
            )

    if validation["warnings"]:
        print()
        print("Warnings:")

        for warning in validation["warnings"]:
            print(
                f"- {warning}"
            )

    print()

    print(
        f"Health Check: {data_health_check()}"
    )
