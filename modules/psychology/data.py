“””
Educational content for the Psychology & Social Work module.

Andishkadeh Management & Market
“””

from future import annotations

from typing import Any

MODULE_ID = “psychology”
MODULE_TITLE = “روانشناسی و مددکاری”

PSYCHOLOGY_CURRICULUM: list[dict[str, Any]] = [
{
“id”: “chapter_1”,
“title”: “مبانی روانشناسی”,
“lessons”: [
{
“id”: “lesson_1”,
“title”: “تعریف و مفهوم روانشناسی”,
“content”: (
“روانشناسی علم مطالعه علمی رفتار و فرایندهای ذهنی “
“انسان است. این علم تلاش می‌کند رفتار، شناخت، “
“هیجان و فرایندهای ذهنی را توصیف و تبیین کند.”
),
“special_points”: [
“روانشناسی بر مطالعه علمی رفتار و فرایندهای ذهنی تمرکز دارد.”,
“رفتار می‌تواند قابل مشاهده یا قابل اندازه‌گیری باشد.”,
“فرایندهای شناختی شامل توجه، حافظه، یادگیری و تفکر هستند.”,
],
“exam_points”: [
“تعریف روانشناسی را با مطالعه رفتار و فرایندهای ذهنی به خاطر بسپارید.”,
“بین رفتار قابل مشاهده و فرایند ذهنی تفاوت قائل شوید.”,
],
“example”: (
“بررسی علت کاهش تمرکز یک دانشجو هنگام مطالعه، “
“نمونه‌ای از بررسی یک فرایند روانشناختی است.”
),
“questions”: [
{
“question”: “روانشناسی به طور کلی چه چیزی را مطالعه می‌کند؟”,
“options”: [
“رفتار و فرایندهای ذهنی”,
“فقط ساختار بدن”,
“فقط بیماری‌های جسمی”,
“فقط روابط اقتصادی”,
],
“answer”: 0,
“explanation”: (
“روانشناسی به مطالعه علمی رفتار و فرایندهای ذهنی می‌پردازد.”
),
},
{
“question”: “کدام مورد نمونه‌ای از فرایند شناختی است؟”,
“options”: [
“حافظه”,
“رشد استخوان”,
“ضربان قلب”,
“فشار خون”,
],
“answer”: 0,
“explanation”: (
“حافظه یکی از فرایندهای شناختی انسان است.”
),
},
],
},
{
“id”: “lesson_2”,
“title”: “رفتار و فرایندهای ذهنی”,
“content”: (
“رفتار شامل فعالیت‌ها و واکنش‌هایی است که می‌توان “
“آن‌ها را به شکل مستقیم یا غیرمستقیم بررسی کرد. “
“فرایندهای ذهنی مانند ادراک، حافظه، تفکر و تصمیم‌گیری “
“نیز بخش مهمی از مطالعه روانشناسی هستند.”
),
“special_points”: [
“رفتار نتیجه تعامل عوامل زیستی، روانی و محیطی است.”,
“فرایندهای ذهنی همیشه به صورت مستقیم قابل مشاهده نیستند.”,
“برای مطالعه فرایندهای ذهنی از روش‌های علمی استفاده می‌شود.”,
],
“exam_points”: [
“رفتار با فرایند ذهنی یکسان نیست.”,
“عوامل محیطی می‌توانند بر رفتار اثر بگذارند.”,
],
“example”: (
“اضطراب قبل از یک آزمون ممکن است باعث تغییر در “
“رفتار، تمرکز و تصمیم‌گیری فرد شود.”
),
“questions”: [
{
“question”: “کدام مورد یک فرایند ذهنی محسوب می‌شود؟”,
“options”: [
“تفکر”,
“راه رفتن”,
“نوشتن”,
“دویدن”,
],
“answer”: 0,
“explanation”: (
“تفکر یک فرایند ذهنی و شناختی است.”
),
},
{
“question”: “رفتار انسان معمولاً تحت تأثیر چه عواملی قرار دارد؟”,
“options”: [
“عوامل زیستی، روانی و محیطی”,
“فقط عوامل اقتصادی”,
“فقط عوامل ژنتیکی”,
“فقط عوامل محیطی”,
],
“answer”: 0,
“explanation”: (
“رفتار انسان حاصل تعامل عوامل مختلف زیستی، روانی و محیطی است.”
),
},
],
},
],
},
{
“id”: “chapter_2”,
“title”: “روانشناسی رشد”,
“lessons”: [
{
“id”: “lesson_1”,
“title”: “مفهوم رشد و تحول”,
“content”: (
“روانشناسی رشد تغییرات جسمانی، شناختی، هیجانی و “
“اجتماعی انسان را در طول زندگی بررسی می‌کند.”
),
“special_points”: [
“رشد فقط به تغییرات جسمانی محدود نمی‌شود.”,
“تحول شناختی و اجتماعی نیز بخشی از رشد انسان است.”,
“رشد در دوره‌های مختلف زندگی ویژگی‌های متفاوتی دارد.”,
],
“exam_points”: [
“رشد را یک فرایند چندبعدی در نظر بگیرید.”,
“ابعاد جسمانی، شناختی، هیجانی و اجتماعی را تفکیک کنید.”,
],
“example”: (
“افزایش توانایی حل مسئله در دوران کودکی نمونه‌ای “
“از تحول شناختی است.”
),
“questions”: [
{
“question”: “کدام مورد یکی از ابعاد رشد انسان است؟”,
“options”: [
“رشد شناختی”,
“فقط رشد مالی”,
“فقط رشد شغلی”,
“فقط رشد اقتصادی”,
],
“answer”: 0,
“explanation”: (
“رشد شناختی یکی از ابعاد اصلی تحول انسان است.”
),
},
],
},
],
},
{
“id”: “chapter_3”,
“title”: “مددکاری اجتماعی”,
“lessons”: [
{
“id”: “lesson_1”,
“title”: “مفهوم مددکاری اجتماعی”,
“content”: (
“مددکاری اجتماعی حرفه‌ای است که با هدف کمک به افراد، “
“گروه‌ها و جوامع برای بهبود عملکرد اجتماعی، حل مسائل “
“و افزایش دسترسی به منابع و حمایت‌های اجتماعی فعالیت می‌کند.”
),
“special_points”: [
“مددکاری اجتماعی بر فرد و محیط اجتماعی او توجه دارد.”,
“توانمندسازی یکی از مفاهیم مهم در مددکاری اجتماعی است.”,
“مددکار باید اصول حرفه‌ای و اخلاقی را رعایت کند.”,
],
“exam_points”: [
“مددکاری اجتماعی را صرفاً کمک مالی در نظر نگیرید.”,
“توانمندسازی و حل مسئله از مفاهیم مهم این حوزه هستند.”,
],
“example”: (
“کمک به یک خانواده برای شناسایی منابع حمایتی و “
“دسترسی به خدمات اجتماعی نمونه‌ای از مداخله مددکاری است.”
),
“questions”: [
{
“question”: “یکی از اهداف مهم مددکاری اجتماعی چیست؟”,
“options”: [
“توانمندسازی و بهبود عملکرد اجتماعی”,
“جایگزینی کامل خانواده”,
“تشخیص همه بیماری‌های جسمی”,
“حذف کامل مشکلات اقتصادی جامعه”,
],
“answer”: 0,
“explanation”: (
“توانمندسازی و بهبود عملکرد اجتماعی از اهداف مهم مددکاری اجتماعی است.”
),
},
],
},
],
},
]

def get_chapters() -> list[dict[str, Any]]:
“”“Return all psychology chapters.”””
return PSYCHOLOGY_CURRICULUM.copy()

def get_chapter(
chapter_id: str,
) -> dict[str, Any] | None:
“”“Return one chapter by ID.”””
for chapter in PSYCHOLOGY_CURRICULUM:
if chapter.get(“id”) == chapter_id:
return chapter
return None

def get_lessons(
chapter_id: str,
) -> list[dict[str, Any]]:
“”“Return lessons for one chapter.”””
chapter = get_chapter(chapter_id)

if chapter is None:
    return []
lessons = chapter.get("lessons", [])
if not isinstance(lessons, list):
    return []
return lessons

def get_lesson(
chapter_id: str,
lesson_id: str,
) -> dict[str, Any] | None:
“”“Return one lesson.”””
for lesson in get_lessons(chapter_id):
if lesson.get(“id”) == lesson_id:
return lesson

return None

def get_all_lessons() -> list[dict[str, Any]]:
“”“Return all lessons with chapter metadata.”””
result: list[dict[str, Any]] = []

for chapter in PSYCHOLOGY_CURRICULUM:
    chapter_id = chapter.get("id")
    chapter_title = chapter.get("title", "")
    for lesson in chapter.get("lessons", []):
        item = dict(lesson)
        item["chapter_id"] = chapter_id
        item["chapter_title"] = chapter_title
        result.append(item)
return result

def get_quiz_questions(
chapter_id: str,
lesson_id: str,
) -> list[dict[str, Any]]:
“”“Return quiz questions for a lesson.”””
lesson = get_lesson(
chapter_id,
lesson_id,
)

if lesson is None:
    return []
questions = lesson.get("questions", [])
if not isinstance(questions, list):
    return []
return questions

def get_curriculum_statistics() -> dict[str, int]:
“”“Return basic curriculum statistics.”””
chapters = len(PSYCHOLOGY_CURRICULUM)
lessons = 0
questions = 0

for chapter in PSYCHOLOGY_CURRICULUM:
    for lesson in chapter.get("lessons", []):
        lessons += 1
        questions += len(
            lesson.get("questions", [])
        )
return {
    "chapters": chapters,
    "lessons": lessons,
    "questions": questions,
}
