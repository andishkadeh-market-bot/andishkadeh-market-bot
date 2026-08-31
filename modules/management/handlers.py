"""
Telegram handlers for the Management educational module.
Andishkadeh Management & Market
--------------------------------
Responsibilities:
- Show Management menu
- Show Management chapters
- Show Management lessons
- Show lesson content
- Start Management quiz
- Answer Management quiz
- Provide navigation back to previous menus
This file is intentionally compatible with the central menu
and the Management data module.
"""
from __future__ import annotations
import logging
from typing import Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modules.management.data import (
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    MANAGEMENT_CHAPTERS,
    get_management_chapters,
    get_management_chapter,
    get_management_lessons,
    get_management_lesson,
)
logger = logging.getLogger(__name__)
# ==========================================================
# Constants
# ==========================================================
QUIZ_QUESTION_KEY = "management_quiz_question"
QUIZ_SCORE_KEY = "management_quiz_score"
QUIZ_TOTAL_KEY = "management_quiz_total"
QUIZ_ACTIVE_KEY = "management_quiz_active"
# ==========================================================
# Safe callback helpers
# ==========================================================
async def _edit_or_reply(
    update: Update,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Edit an existing callback message when possible.
    Otherwise send a normal reply.
    """
    query = update.callback_query
    if query is not None:
        try:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup,
            )
            return
        except Exception:
            logger.exception(
                "Unable to edit callback message."
            )
    message = update.effective_message
    if message is not None:
        await message.reply_text(
            text=text,
            reply_markup=reply_markup,
        )
# ==========================================================
# Main Management menu
# ==========================================================
async def show_management_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Display the main Management module menu.
    """
    keyboard: list[list[InlineKeyboardButton]] = []
    chapters = get_management_chapters()
    for chapter in chapters:
        keyboard.append(
            [
                InlineKeyboardButton(
                    chapter["title"],
                    callback_data=f"management_chapter:{chapter['id']}",
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "📝 آزمون مدیریت",
                callback_data="management_quiz_start",
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="main_menu",
            )
        ]
    )
    await _edit_or_reply(
        update,
        (
            f"📚 {MODULE_TITLE}\n\n"
            f"{MODULE_DESCRIPTION}\n\n"
            "یکی از فصل‌ها را انتخاب کنید:"
        ),
        InlineKeyboardMarkup(keyboard),
    )
# ==========================================================
# Chapter menu
# ==========================================================
async def show_management_chapter_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
) -> None:
    """
    Display lessons belonging to one Management chapter.
    """
    query = update.callback_query
    if chapter_id is None and query is not None:
        data = query.data or ""
        if data.startswith("management_chapter:"):
            chapter_id = data.split(
                ":",
                1,
            )[1]
    if not chapter_id:
        await show_management_menu(
            update,
            context,
        )
        return
    chapter = get_management_chapter(
        chapter_id
    )
    if chapter is None:
        await _edit_or_reply(
            update,
            "❌ فصل موردنظر پیدا نشد.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="management_menu",
                        )
                    ]
                ]
            ),
        )
        return
    lessons = get_management_lessons(
        chapter_id
    )
    keyboard: list[list[InlineKeyboardButton]] = []
    for lesson in lessons:
        keyboard.append(
            [
                InlineKeyboardButton(
                    lesson["title"],
                    callback_data=(
                        f"management_lesson:"
                        f"{chapter_id}:"
                        f"{lesson['id']}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "📝 آزمون مدیریت",
                callback_data="management_quiz_start",
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به فصل‌ها",
                callback_data="management_menu",
            )
        ]
    )
    await _edit_or_reply(
        update,
        (
            f"📖 {chapter['title']}\n\n"
            f"{chapter.get('description', '')}\n\n"
            "درس موردنظر را انتخاب کنید:"
        ),
        InlineKeyboardMarkup(keyboard),
    )
# ==========================================================
# Lesson display
# ==========================================================
async def show_management_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> None:
    """
    Display one Management lesson.
    """
    query = update.callback_query
    if query is not None:
        data = query.data or ""
        if data.startswith("management_lesson:"):
            parts = data.split(":")
            if len(parts) >= 3:
                chapter_id = parts[1]
                lesson_id = parts[2]
    if not chapter_id or not lesson_id:
        await show_management_menu(
            update,
            context,
        )
        return
    lesson = get_management_lesson(
        chapter_id,
        lesson_id,
    )
    if lesson is None:
        await _edit_or_reply(
            update,
            "❌ درس موردنظر پیدا نشد.",
        )
        return
    text_parts: list[str] = []
    text_parts.append(
        f"📘 {lesson['title']}"
    )
    summary = lesson.get(
        "summary",
        "",
    )
    if summary:
        text_parts.append(
            f"\n📝 خلاصه:\n{summary}"
        )
    content = lesson.get(
        "content",
        "",
    )
    if content:
        text_parts.append(
            f"\n📚 درسنامه:\n{content}"
        )
    specialized_tips = lesson.get(
        "specialized_tips",
        [],
    )
    if specialized_tips:
        text_parts.append(
            "\n🎯 نکات تخصصی:"
        )
        for item in specialized_tips:
            text_parts.append(
                f"• {item}"
            )
    exam_tips = lesson.get(
        "exam_tips",
        [],
    )
    if exam_tips:
        text_parts.append(
            "\n📝 نکات آزمونی:"
        )
        for item in exam_tips:
            text_parts.append(
                f"• {item}"
            )
    examples = lesson.get(
        "examples",
        [],
    )
    if examples:
        text_parts.append(
            "\n💡 مثال کاربردی:"
        )
        for item in examples:
            text_parts.append(
                f"• {item}"
            )
    review = lesson.get(
        "review",
        [],
    )
    if review:
        text_parts.append(
            "\n🔄 مرور:"
        )
        for item in review:
            text_parts.append(
                f"• {item}"
            )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 آزمون مدیریت",
                    callback_data="management_quiz_start",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به فصل",
                    callback_data=(
                        f"management_chapter:{chapter_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 منوی مدیریت",
                    callback_data="management_menu",
                )
            ],
        ]
    )
    await _edit_or_reply(
        update,
        "\n".join(text_parts),
        keyboard,
    )
# ==========================================================
# Quiz data
# ==========================================================
MANAGEMENT_QUIZ_QUESTIONS: list[dict[str, Any]] = [
    {
        "question": "کدام گزینه تعریف مناسب‌تری از مدیریت ارائه می‌دهد؟",
        "options": [
            "فرایند برنامه‌ریزی، سازماندهی، رهبری و کنترل منابع برای دستیابی به اهداف",
            "فرایند ثبت اطلاعات مالی سازمان",
            "فرایند تبلیغات و فروش محصولات",
            "فرایند تولید کالا بدون توجه به منابع",
        ],
        "correct_index": 0,
    },
    {
        "question": "کدام گزینه از وظایف اصلی مدیریت است؟",
        "options": [
            "برنامه‌ریزی",
            "حذف کامل ریسک",
            "توقف تصمیم‌گیری",
            "حذف ساختار سازمانی",
        ],
        "correct_index": 0,
    },
    {
        "question": "اثربخشی در مدیریت بیشتر به چه مفهومی اشاره دارد؟",
        "options": [
            "دستیابی به اهداف",
            "کاهش تعداد کارکنان",
            "افزایش هزینه‌ها",
            "استفاده از منابع بدون توجه به هدف",
        ],
        "correct_index": 0,
    },
    {
        "question": "کدام مورد بیشتر با مدیریت علمی مرتبط است؟",
        "options": [
            "فردریک تیلور",
            "آبراهام مازلو",
            "الکساندر گراهام بل",
            "پیتر دراکر",
        ],
        "correct_index": 0,
    },
    {
        "question": "کدام مفهوم با هنری فایول ارتباط بیشتری دارد؟",
        "options": [
            "اصول عمومی مدیریت",
            "نظریه انتظار",
            "بازاریابی رابطه‌مند",
            "حسابداری صنعتی",
        ],
        "correct_index": 0,
    },
    {
        "question": "در تحلیل SWOT، کدام مورد معمولاً عامل داخلی محسوب می‌شود؟",
        "options": [
            "نقطه قوت",
            "فرصت بازار",
            "تهدید رقبا",
            "تغییر قوانین",
        ],
        "correct_index": 0,
    },
    {
        "question": "هدف اصلی برنامه‌ریزی چیست؟",
        "options": [
            "تعیین اهداف و مسیر دستیابی به آنها",
            "افزایش هزینه‌های سازمان",
            "حذف ارزیابی عملکرد",
            "جلوگیری از تصمیم‌گیری",
        ],
        "correct_index": 0,
    },
    {
        "question": "حیطه نظارت به چه چیزی اشاره دارد؟",
        "options": [
            "تعداد افرادی که مستقیماً تحت نظارت یک مدیر هستند",
            "تعداد کل کارکنان سازمان",
            "تعداد شعب سازمان",
            "تعداد مشتریان سازمان",
        ],
        "correct_index": 0,
    },
    {
        "question": "در مدیریت منابع انسانی، انتخاب کارکنان به چه معناست؟",
        "options": [
            "گزینش فرد مناسب برای شغل موردنظر",
            "انتشار آگهی استخدام",
            "پرداخت حقوق کارکنان",
            "طراحی تبلیغات شرکت",
        ],
        "correct_index": 0,
    },
    {
        "question": "کدام مفهوم بیشتر با رهبری ارتباط دارد؟",
        "options": [
            "نفوذ و اثرگذاری بر افراد",
            "ثبت اسناد حسابداری",
            "خرید تجهیزات اداری",
            "محاسبه مالیات",
        ],
        "correct_index": 0,
    },
]
# ==========================================================
# Quiz helpers
# ==========================================================
def _get_quiz_questions() -> list[dict[str, Any]]:
    """
    Return a safe copy of the quiz questions.
    """
    return [
        {
            "question": item["question"],
            "options": list(
                item["options"]
            ),
            "correct_index": item["correct_index"],
        }
        for item in MANAGEMENT_QUIZ_QUESTIONS
    ]
def _get_current_quiz_question(
    context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
    """
    Return the current quiz question.
    """
    index = context.user_data.get(
        QUIZ_QUESTION_KEY,
        0,
    )
    questions = _get_quiz_questions()
    if not questions:
        return None
    if index < 0 or index >= len(questions):
        return None
    return questions[index]
# ==========================================================
# Start Management quiz
# ==========================================================
async def start_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start the Management quiz.
    This function exists explicitly because core/menu.py
    imports it.
    """
    questions = _get_quiz_questions()
    if not questions:
        await _edit_or_reply(
            update,
            "❌ در حال حاضر سوالی برای آزمون مدیریت ثبت نشده است.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="management_menu",
                        )
                    ]
                ]
            ),
        )
        return
    context.user_data[QUIZ_QUESTION_KEY] = 0
    context.user_data[QUIZ_SCORE_KEY] = 0
    context.user_data[QUIZ_TOTAL_KEY] = len(
        questions
    )
    context.user_data[QUIZ_ACTIVE_KEY] = True
    await _send_management_quiz_question(
        update,
        context,
    )
# ==========================================================
# Send quiz question
# ==========================================================
async def _send_management_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Send current Management quiz question.
    """
    question = _get_current_quiz_question(
        context
    )
    if question is None:
        await _finish_management_quiz(
            update,
            context,
        )
        return
    index = context.user_data.get(
        QUIZ_QUESTION_KEY,
        0,
    )
    total = context.user_data.get(
        QUIZ_TOTAL_KEY,
        len(MANAGEMENT_QUIZ_QUESTIONS),
    )
    keyboard: list[list[InlineKeyboardButton]] = []
    for option_index, option in enumerate(
        question["options"]
    ):
        keyboard.append(
            [
                InlineKeyboardButton(
                    option,
                    callback_data=(
                        f"management_quiz_answer:"
                        f"{option_index}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ پایان آزمون",
                callback_data="management_quiz_stop",
            )
        ]
    )
    await _edit_or_reply(
        update,
        (
            f"📝 آزمون مدیریت\n\n"
            f"سؤال {index + 1} از {total}\n\n"
            f"{question['question']}"
        ),
        InlineKeyboardMarkup(keyboard),
    )
# ==========================================================
# Answer Management quiz
# ==========================================================
async def answer_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Process a Management quiz answer.
    This function exists explicitly because core/menu.py
    imports it.
    """
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    if not data.startswith(
        "management_quiz_answer:"
    ):
        return
    if not context.user_data.get(
        QUIZ_ACTIVE_KEY,
        False,
    ):
        await _edit_or_reply(
            update,
            "⚠️ آزمون فعالی وجود ندارد.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📝 شروع آزمون",
                            callback_data="management_quiz_start",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="management_menu",
                        )
                    ],
                ]
            ),
        )
        return
    try:
        selected_index = int(
            data.split(
                ":",
                1,
            )[1]
        )
    except (
        ValueError,
        IndexError,
    ):
        await _edit_or_reply(
            update,
            "❌ پاسخ نامعتبر است.",
        )
        return
    question = _get_current_quiz_question(
        context
    )
    if question is None:
        await _finish_management_quiz(
            update,
            context,
        )
        return
    options = question.get(
        "options",
        [],
    )
    correct_index = question.get(
        "correct_index",
        -1,
    )
    if (
        selected_index < 0
        or selected_index >= len(options)
    ):
        await _edit_or_reply(
            update,
            "❌ گزینه انتخاب‌شده معتبر نیست.",
        )
        return
    if selected_index == correct_index:
        context.user_data[
            QUIZ_SCORE_KEY
        ] = (
            context.user_data.get(
                QUIZ_SCORE_KEY,
                0,
            )
            + 1
        )
        result_text = (
            "✅ پاسخ شما درست بود."
        )
    else:
        correct_answer = options[
            correct_index
        ]
        result_text = (
            "❌ پاسخ شما نادرست بود.\n\n"
            f"پاسخ صحیح: {correct_answer}"
        )
    current_index = context.user_data.get(
        QUIZ_QUESTION_KEY,
        0,
    )
    context.user_data[
        QUIZ_QUESTION_KEY
    ] = current_index + 1
    next_question = _get_current_quiz_question(
        context
    )
    if next_question is None:
        score = context.user_data.get(
            QUIZ_SCORE_KEY,
            0,
        )
        total = context.user_data.get(
            QUIZ_TOTAL_KEY,
            len(MANAGEMENT_QUIZ_QUESTIONS),
        )
        context.user_data[
            QUIZ_ACTIVE_KEY
        ] = False
        await _edit_or_reply(
            update,
            (
                f"{result_text}\n\n"
                "🏁 آزمون به پایان رسید.\n\n"
                f"📊 نتیجه: {score} از {total}"
            ),
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 آزمون مجدد",
                            callback_data="management_quiz_start",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📚 منوی مدیریت",
                            callback_data="management_menu",
                        )
                    ],
                ]
            ),
        )
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➡️ سؤال بعدی",
                    callback_data="management_quiz_next",
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ پایان آزمون",
                    callback_data="management_quiz_stop",
                )
            ],
        ]
    )
    await _edit_or_reply(
        update,
        result_text,
        keyboard,
    )
# ==========================================================
# Next quiz question
# ==========================================================
async def next_management_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show the next Management quiz question.
    """
    if not context.user_data.get(
        QUIZ_ACTIVE_KEY,
        False,
    ):
        await start_management_quiz(
            update,
            context,
        )
        return
    await _send_management_quiz_question(
        update,
        context,
    )
# ==========================================================
# Finish quiz
# ==========================================================
async def _finish_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Finish Management quiz and show score.
    """
    score = context.user_data.get(
        QUIZ_SCORE_KEY,
        0,
    )
    total = context.user_data.get(
        QUIZ_TOTAL_KEY,
        len(MANAGEMENT_QUIZ_QUESTIONS),
    )
    context.user_data[
        QUIZ_ACTIVE_KEY
    ] = False
    await _edit_or_reply(
        update,
        (
            "🏁 آزمون مدیریت به پایان رسید.\n\n"
            f"📊 امتیاز شما: {score} از {total}"
        ),
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔄 آزمون مجدد",
                        callback_data="management_quiz_start",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 منوی مدیریت",
                        callback_data="management_menu",
                    )
                ],
            ]
        ),
    )
# ==========================================================
# Stop quiz
# ==========================================================
async def stop_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Stop the current Management quiz.
    """
    score = context.user_data.get(
        QUIZ_SCORE_KEY,
        0,
    )
    total = context.user_data.get(
        QUIZ_TOTAL_KEY,
        len(MANAGEMENT_QUIZ_QUESTIONS),
    )
    context.user_data[
        QUIZ_ACTIVE_KEY
    ] = False
    await _edit_or_reply(
        update,
        (
            "⏹ آزمون متوقف شد.\n\n"
            f"📊 نتیجه فعلی: {score} از {total}"
        ),
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔄 شروع دوباره",
                        callback_data="management_quiz_start",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 منوی مدیریت",
                        callback_data="management_menu",
                    )
                ],
            ]
        ),
    )
# ==========================================================
# Health check
# ==========================================================
def management_handlers_health_check() -> bool:
    """
    Basic health check for the Management handlers.
    """
    try:
        required_functions = (
            show_management_menu,
            show_management_chapter_menu,
            show_management_lesson,
            start_management_quiz,
            answer_management_quiz,
            next_management_quiz_question,
            stop_management_quiz,
        )
        return all(
            callable(function)
            for function in required_functions
        )
    except Exception:
        return False
# ==========================================================
# Public exports
# ==========================================================
__all__ = [
    "show_management_menu",
    "show_management_chapter_menu",
    "show_management_lesson",
    "start_management_quiz",
    "answer_management_quiz",
    "next_management_quiz_question",
    "stop_management_quiz",
    "management_handlers_health_check",
]
