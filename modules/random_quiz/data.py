"""
Data definitions for Random Quiz module.
Andishkadeh Management & Market
"""
from __future__ import annotations
from typing import Any
# ==========================================================
# Random Quiz Configuration
# ==========================================================
RANDOM_QUIZ_CONFIG: dict[str, Any] = {
    "module_id": "random_quiz",
    "title": "🎲 سوالات تصادفی",
    "description": (
        "آزمون تصادفی از میان سوالات ثبت‌شده اندیشکده"
    ),
    "default_question_count": 10,
    "minimum_question_count": 1,
    "maximum_question_count": 20,
}
# ==========================================================
# Random Questions
# ==========================================================
#
# ساختار هر سؤال:
#
# {
#     "id": "rq_001",
#     "question": "متن سؤال",
#     "options": [
#         "گزینه اول",
#         "گزینه دوم",
#         "گزینه سوم",
#         "گزینه چهارم",
#     ],
#     "correct_answer": "گزینه صحیح",
# }
#
# فعلاً چند سؤال پایه برای تست عملکرد کامل ماژول قرار داده‌ایم.
# بانک سؤال اصلی را بعداً می‌توانیم به‌صورت گسترده تکمیل کنیم.
# ==========================================================
RANDOM_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "rq_001",
        "question": "مدیریت به چه معناست؟",
        "options": [
            "فرآیند برنامه‌ریزی، سازماندهی، هدایت و کنترل منابع",
            "فقط کنترل کارکنان",
            "فقط افزایش فروش",
            "فقط حسابداری",
        ],
        "correct_answer": (
            "فرآیند برنامه‌ریزی، سازماندهی، هدایت و کنترل منابع"
        ),
        "category": "management",
        "difficulty": "easy",
    },
    {
        "id": "rq_002",
        "question": "کدام مورد یکی از وظایف اصلی مدیریت است؟",
        "options": [
            "برنامه‌ریزی",
            "خوابیدن",
            "حذف اطلاعات",
            "نادیده گرفتن بازار",
        ],
        "correct_answer": "برنامه‌ریزی",
        "category": "management",
        "difficulty": "easy",
    },
    {
        "id": "rq_003",
        "question": "بازاریابی بیشتر بر چه موضوعی تمرکز دارد؟",
        "options": [
            "شناخت نیاز مشتری و ایجاد ارزش",
            "فقط کاهش هزینه",
            "فقط استخدام کارکنان",
            "فقط ثبت حساب‌ها",
        ],
        "correct_answer": "شناخت نیاز مشتری و ایجاد ارزش",
        "category": "marketing",
        "difficulty": "easy",
    },
    {
        "id": "rq_004",
        "question": "صادرات به چه معناست؟",
        "options": [
            "فروش کالا یا خدمات به بازار خارجی",
            "خرید کالا از بازار داخلی",
            "تولید کالا برای مصرف شخصی",
            "انتقال کالا بین دو فروشگاه داخلی",
        ],
        "correct_answer": "فروش کالا یا خدمات به بازار خارجی",
        "category": "international_trade",
        "difficulty": "easy",
    },
    {
        "id": "rq_005",
        "question": "واردات به چه معناست؟",
        "options": [
            "خرید کالا یا خدمات از خارج از کشور",
            "فروش کالا به خارج از کشور",
            "تولید داخلی کالا",
            "تبلیغات داخلی",
        ],
        "correct_answer": "خرید کالا یا خدمات از خارج از کشور",
        "category": "international_trade",
        "difficulty": "easy",
    },
    {
        "id": "rq_006",
        "question": "تورم به چه معناست؟",
        "options": [
            "افزایش مستمر سطح عمومی قیمت‌ها",
            "کاهش عمومی قیمت‌ها",
            "افزایش تولید بدون تغییر قیمت",
            "کاهش نرخ اشتغال",
        ],
        "correct_answer": "افزایش مستمر سطح عمومی قیمت‌ها",
        "category": "economics",
        "difficulty": "easy",
    },
    {
        "id": "rq_007",
        "question": "کدام گزینه یکی از ابزارهای سیاست پولی است؟",
        "options": [
            "نرخ بهره",
            "تبلیغات تلویزیونی",
            "بسته‌بندی محصول",
            "طراحی لوگو",
        ],
        "correct_answer": "نرخ بهره",
        "category": "banking",
        "difficulty": "medium",
    },
    {
        "id": "rq_008",
        "question": "بانک تجاری معمولاً چه نقشی دارد؟",
        "options": [
            "جذب سپرده و اعطای تسهیلات",
            "تولید خودرو",
            "تولید مواد غذایی",
            "طراحی ساختمان",
        ],
        "correct_answer": "جذب سپرده و اعطای تسهیلات",
        "category": "banking",
        "difficulty": "easy",
    },
    {
        "id": "rq_009",
        "question": "مزیت رقابتی چیست؟",
        "options": [
            "ویژگی یا قابلیتی که موجب برتری سازمان نسبت به رقبا می‌شود",
            "افزایش تعداد کارکنان بدون هدف",
            "افزایش هزینه‌های سازمان",
            "حذف مشتریان",
        ],
        "correct_answer": (
            "ویژگی یا قابلیتی که موجب برتری سازمان نسبت به رقبا می‌شود"
        ),
        "category": "management",
        "difficulty": "medium",
    },
    {
        "id": "rq_010",
        "question": "مشتری‌مداری در بازاریابی به چه معناست؟",
        "options": [
            "تمرکز بر نیازها و رضایت مشتری",
            "نادیده گرفتن بازخورد مشتری",
            "افزایش قیمت بدون بررسی بازار",
            "حذف خدمات پس از فروش",
        ],
        "correct_answer": "تمرکز بر نیازها و رضایت مشتری",
        "category": "marketing",
        "difficulty": "easy",
    },
]
# ==========================================================
# Public API
# ==========================================================
def get_random_quiz_config() -> dict[str, Any]:
    """
    Return a copy of the Random Quiz configuration.
    """
    return dict(
        RANDOM_QUIZ_CONFIG
    )
def get_random_questions() -> list[dict[str, Any]]:
    """
    Return a copy of the random quiz question bank.
    """
    return [
        dict(question)
        for question in RANDOM_QUESTIONS
    ]
def data_health_check() -> bool:
    """
    Validate Random Quiz data.
    """
    if not isinstance(
        RANDOM_QUIZ_CONFIG,
        dict,
    ):
        return False
    if not isinstance(
        RANDOM_QUESTIONS,
        list,
    ):
        return False
    if len(RANDOM_QUESTIONS) < 1:
        return False
    for question in RANDOM_QUESTIONS:
        if not isinstance(
            question,
            dict,
        ):
            return False
        if not question.get("question"):
            return False
        options = question.get(
            "options",
            [],
        )
        if not isinstance(
            options,
            list,
        ):
            return False
        if len(options) < 2:
            return False
        if "correct_answer" not in question:
            return False
    return True
