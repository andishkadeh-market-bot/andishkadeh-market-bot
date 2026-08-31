“”“Question bank for the General Exam module.

Andishkadeh Management & Market
“””

from future import annotations

from typing import TypedDict

class ExamQuestion(TypedDict):
“”“Structure of one general-exam question.”””

question: str
options: list[str]
correct_index: int

GENERAL_EXAM_QUESTIONS: list[ExamQuestion] = [
{
“question”: “کدام گزینه تعریف درست‌تری از مدیریت ارائه می‌دهد؟”,
“options”: [
“فرآیند برنامه‌ریزی، سازماندهی، هدایت و کنترل منابع برای دستیابی به اهداف”,
“فرآیند ثبت و نگهداری اطلاعات مالی سازمان”,
“فرآیند تولید کالا بدون توجه به منابع سازمان”,
“فرآیند تبلیغات و فروش محصولات”,
],
“correct_index”: 0,
},
{
“question”: “کدام مورد یکی از وظایف اصلی مدیریت است؟”,
“options”: [
“برنامه‌ریزی”,
“حذف کامل ریسک”,
“توقف تصمیم‌گیری”,
“حذف ساختار سازمانی”,
],
“correct_index”: 0,
},
{
“question”: “هدف اصلی برنامه‌ریزی در سازمان چیست؟”,
“options”: [
“تعیین اهداف و مسیر مناسب برای دستیابی به آن‌ها”,
“افزایش هزینه‌های سازمان”,
“حذف تمام کارکنان”,
“جلوگیری از ارزیابی عملکرد”,
],
“correct_index”: 0,
},
{
“question”: “کدام گزینه نمونه‌ای از یک منبع سازمانی محسوب می‌شود؟”,
“options”: [
“منابع انسانی”,
“شایعات بازار”,
“حدس‌های بدون اطلاعات”,
“تصمیم‌های تصادفی”,
],
“correct_index”: 0,
},
{
“question”: “در بازاریابی، بازار هدف به چه معناست؟”,
“options”: [
“گروهی از مشتریان که سازمان قصد ارائه محصول یا خدمت به آن‌ها را دارد”,
“تمام افراد جامعه بدون هیچ دسته‌بندی”,
“فقط کارکنان شرکت”,
“فقط تأمین‌کنندگان شرکت”,
],
“correct_index”: 0,
},
{
“question”: “کدام گزینه یکی از عناصر معروف آمیخته بازاریابی 4P است؟”,
“options”: [
“Product”,
“Policy”,
“Personnel”,
“Performance”,
],
“correct_index”: 0,
},
{
“question”: “تورم به طور کلی به چه معناست؟”,
“options”: [
“افزایش مستمر سطح عمومی قیمت‌ها”,
“کاهش عمومی قیمت‌ها”,
“افزایش ارزش پول در برابر کالاها”,
“افزایش تولید بدون تغییر قیمت‌ها”,
],
“correct_index”: 0,
},
{
“question”: “کدام گزینه نمونه‌ای از تجارت بین‌الملل است؟”,
“options”: [
“صادرات کالا از یک کشور به کشور دیگر”,
“فروش کالا در داخل یک فروشگاه”,
“تولید کالا برای مصرف شخصی”,
“جابجایی کالا بین دو انبار یک شرکت در یک شهر”,
],
“correct_index”: 0,
},
{
“question”: “مزیت رقابتی یک شرکت به چه چیزی اشاره دارد؟”,
“options”: [
“توانایی ایجاد ارزش بیشتر یا عملکرد بهتر نسبت به رقبا”,
“افزایش هزینه‌ها بدون ایجاد ارزش”,
“حذف مشتریان از بازار”,
“کاهش کیفیت محصولات”,
],
“correct_index”: 0,
},
{
“question”: “کدام گزینه برای تصمیم‌گیری مدیریتی اهمیت بیشتری دارد؟”,
“options”: [
“اطلاعات معتبر و مرتبط”,
“شایعات بدون منبع”,
“تصمیم‌گیری کاملاً تصادفی”,
“نادیده گرفتن شرایط محیطی”,
],
“correct_index”: 0,
},
]

def get_general_exam_questions() -> list[ExamQuestion]:
“”“Return a copy of the general exam question bank.”””

return [
    {
        "question": item["question"],
        "options": list(item["options"]),
        "correct_index": item["correct_index"],
    }
    for item in GENERAL_EXAM_QUESTIONS
]

def get_general_exam_question_count() -> int:
“”“Return the number of available general-exam questions.”””

return len(GENERAL_EXAM_QUESTIONS)

def validate_question_bank() -> bool:
“”“Validate the structure of the general exam question bank.”””

if not GENERAL_EXAM_QUESTIONS:
    return False
for item in GENERAL_EXAM_QUESTIONS:
    if not item.get("question"):
        return False
    options = item.get("options")
    if not isinstance(options, list):
        return False
    if len(options) != 4:
        return False
    if any(
        not isinstance(option, str) or not option.strip()
        for option in options
    ):
        return False
    correct_index = item.get("correct_index")
    if not isinstance(correct_index, int):
        return False
    if correct_index < 0 or correct_index >= len(options):
        return False
return True

def data_health_check() -> bool:
“”“Health check for the general-exam question bank.”””

try:
    return validate_question_bank()
except Exception:
    return False
