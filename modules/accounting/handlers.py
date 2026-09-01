"""
Telegram handlers for Accounting Module.

Andishkadeh Management & Market

Features:
- Main accounting menu
- Chapter navigation
- Lesson navigation
- Detailed lessons
- Lesson quiz
- Chapter quiz
- Comprehensive quiz
- Statistics
- Back navigation
- Compatibility aliases
"""

from __future__ import annotations

import html
import logging
from typing import Any

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from modules.accounting.service import (
    get_module_info,
    get_accounting_chapters,
    get_accounting_chapter,
    get_accounting_lessons,
    get_accounting_lesson,
    get_accounting_quiz,
    get_all_quiz_questions,
    get_curriculum_stats,
)


logger = logging.getLogger(__name__)


# ==========================================================
# Context Keys
# ==========================================================

QUIZ_QUESTIONS_KEY = "accounting_quiz_questions"
QUIZ_INDEX_KEY = "accounting_quiz_index"
QUIZ_SCORE_KEY = "accounting_quiz_score"
QUIZ_CHAPTER_KEY = "accounting_quiz_chapter"
QUIZ_LESSON_KEY = "accounting_quiz_lesson"


# ==========================================================
# Helpers
# ==========================================================

async def _answer_callback(
    update: Update,
) -> None:

    query = update.callback_query

    if query is None:
        return

    try:
        await query.answer()
    except Exception:
        logger.exception(
            "Unable to answer accounting callback."
        )


async def _edit_or_reply(
    update: Update,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:

    query = update.callback_query

    if query is not None:

        try:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
            return

        except Exception:
            logger.exception(
                "Unable to edit accounting message."
            )

    message = update.effective_message

    if message is not None:

        try:
            await message.reply_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )

        except Exception:
            logger.exception(
                "Unable to send accounting message."
            )


def _safe_text(
    value: Any,
) -> str:

    return html.escape(
        str(value or "")
    )


def _lesson_content(
    lesson: dict[str, Any],
) -> str:

    for key in (
        "content",
        "text",
        "description",
        "lesson_content",
        "body",
        "details",
    ):

        value = lesson.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return "محتوای این درس هنوز ثبت نشده است."


def _list_section(
    title: str,
    values: Any,
) -> str:

    if not isinstance(values, list) or not values:
        return ""

    lines = [
        title,
    ]

    for item in values:

        if isinstance(item, dict):

            text = (
                item.get("text")
                or item.get("title")
                or item.get("description")
                or ""
            )

        else:
            text = item

        if text:
            lines.append(
                f"• {_safe_text(text)}"
            )

    return "\n".join(lines)


# ==========================================================
# Main Menu
# ==========================================================

async def show_accounting_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await _answer_callback(update)

    info = get_module_info()
    chapters = get_accounting_chapters()

    keyboard: list[list[InlineKeyboardButton]] = []

    for chapter in chapters:

        chapter_id = str(
            chapter.get("id")
            or ""
        ).strip()

        if not chapter_id:
            continue

        title = str(
            chapter.get(
                "title",
                chapter_id,
            )
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    title,
                    callback_data=(
                        "accounting_chapter:"
                        f"{chapter_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "📝 آزمون جامع حسابداری",
                callback_data="accounting_quiz_all",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "📊 آمار دوره",
                callback_data="accounting_statistics",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="menu_main",
            )
        ]
    )

    text = (
        f"🧾 <b>{_safe_text(info['title'])}</b>\n\n"
        f"{_safe_text(info['description'])}\n\n"
        "🎓 <b>مسیر حرفه‌ای حسابداری</b>\n\n"
        "از مبانی حسابداری و ثبت دوطرفه تا حسابداری مالی، "
        "مدیریتی، صنعتی، مالیاتی، شرکت‌ها، حسابرسی، "
        "تحلیل صورت‌های مالی، IFRS و فناوری‌های نوین.\n\n"
        f"📚 تعداد فصل‌ها: <b>{len(chapters)}</b>\n\n"
        "فصل موردنظر را انتخاب کنید:"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(keyboard),
    )


# ==========================================================
# Chapter
# ==========================================================

async def show_accounting_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
) -> None:

    await _answer_callback(update)

    query = update.callback_query

    if chapter_id is None and query is not None:

        data = query.data or ""

        if data.startswith(
            "accounting_chapter:"
        ):
            chapter_id = data.split(
                ":",
                1,
            )[1]

    if not chapter_id:

        await show_accounting_menu(
            update,
            context,
        )
        return

    chapter = get_accounting_chapter(
        chapter_id
    )

    if chapter is None:

        await _edit_or_reply(
            update,
            "❌ فصل حسابداری پیدا نشد.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="menu_accounting",
                        )
                    ]
                ]
            ),
        )
        return

    lessons = get_accounting_lessons(
        chapter_id
    )

    keyboard: list[list[InlineKeyboardButton]] = []

    for lesson in lessons:

        lesson_id = str(
            lesson.get("id")
            or ""
        ).strip()

        if not lesson_id:
            continue

        title = str(
            lesson.get(
                "title",
                lesson_id,
            )
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 {title}",
                    callback_data=(
                        "accounting_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "📝 آزمون فصل",
                callback_data=(
                    "accounting_quiz_chapter:"
                    f"{chapter_id}"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به فصل‌ها",
                callback_data="menu_accounting",
            )
        ]
    )

    text = (
        f"📚 <b>{_safe_text(chapter.get('title'))}</b>\n\n"
        f"{_safe_text(chapter.get('description'))}\n\n"
        f"📖 تعداد درس‌ها: <b>{len(lessons)}</b>\n\n"
        "درس موردنظر را انتخاب کنید:"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(keyboard),
    )


# ==========================================================
# Lesson
# ==========================================================

async def show_accounting_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> None:

    await _answer_callback(update)

    query = update.callback_query

    if query is not None:

        data = query.data or ""

        if data.startswith(
            "accounting_lesson:"
        ):

            parts = data.split(":")

            if len(parts) >= 3:
                chapter_id = parts[1]
                lesson_id = parts[2]

    if not chapter_id or not lesson_id:

        await show_accounting_menu(
            update,
            context,
        )
        return

    lesson = get_accounting_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:

        await _edit_or_reply(
            update,
            "❌ درس حسابداری پیدا نشد.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                "accounting_chapter:"
                                f"{chapter_id}"
                            ),
                        )
                    ]
                ]
            ),
        )
        return

    title = _safe_text(
        lesson.get(
            "title",
            lesson_id,
        )
    )

    content = _lesson_content(
        lesson
    )

    text_parts = [
        f"📘 <b>{title}</b>",
        "",
        "📚 <b>درسنامه تخصصی:</b>",
        _safe_text(content),
        _list_section(
            "🎯 <b>نکات تخصصی:</b>",
            lesson.get(
                "specialized_tips",
                [],
            ),
        ),
        _list_section(
            "📝 <b>نکات آزمونی:</b>",
            lesson.get(
                "exam_tips",
                [],
            ),
        ),
        _list_section(
            "💡 <b>مثال‌های کاربردی:</b>",
            lesson.get(
                "examples",
                [],
            ),
        ),
        _list_section(
            "🔑 <b>کلیدواژه‌های تخصصی:</b>",
            lesson.get(
                "keywords",
                [],
            ),
        ),
    ]

    text = "\n\n".join(
        part
        for part in text_parts
        if part
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 آزمون این درس",
                    callback_data=(
                        "accounting_quiz_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به فصل",
                    callback_data=(
                        "accounting_chapter:"
                        f"{chapter_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🧾 منوی حسابداری",
                    callback_data="menu_accounting",
                )
            ],
        ]
    )

    await _edit_or_reply(
        update,
        text,
        keyboard,
    )


# ==========================================================
# Quiz Preparation
# ==========================================================

def _normalize_question(
    question: dict[str, Any],
) -> dict[str, Any]:

    item = dict(question)

    options = item.get(
        "options",
        [],
    )

    if not isinstance(options, list):
        options = []

    normalized_options: list[str] = []

    for option in options:

        if isinstance(option, dict):

            value = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or ""
            )

        else:
            value = option

        normalized_options.append(
            str(value)
        )

    item["options"] = normalized_options

    correct = item.get(
        "correct_index",
        item.get(
            "answer_index",
            0,
        ),
    )

    try:
        item["correct_index"] = int(correct)
    except Exception:
        item["correct_index"] = 0

    return item


def _prepare_quiz(
    context: ContextTypes.DEFAULT_TYPE,
    questions: list[dict[str, Any]],
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> bool:

    normalized = [
        _normalize_question(question)
        for question in questions
        if isinstance(question, dict)
    ]

    valid_questions = []

    for question in normalized:

        options = question.get(
            "options",
            [],
        )

        correct_index = question.get(
            "correct_index",
            -1,
        )

        if (
            len(options) >= 2
            and 0 <= correct_index < len(options)
        ):
            valid_questions.append(
                question
            )

    if not valid_questions:
        return False

    context.user_data[
        QUIZ_QUESTIONS_KEY
    ] = valid_questions

    context.user_data[
        QUIZ_INDEX_KEY
    ] = 0

    context.user_data[
        QUIZ_SCORE_KEY
    ] = 0

    context.user_data[
        QUIZ_CHAPTER_KEY
    ] = chapter_id

    context.user_data[
        QUIZ_LESSON_KEY
    ] = lesson_id

    return True


# ==========================================================
# Start Quiz
# ==========================================================

async def start_accounting_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await _answer_callback(update)

    query = update.callback_query

    chapter_id = None
    lesson_id = None

    if query is not None:

        data = query.data or ""

        if data.startswith(
            "accounting_quiz_lesson:"
        ):

            parts = data.split(":")

            if len(parts) >= 3:
                chapter_id = parts[1]
                lesson_id = parts[2]

    if chapter_id and lesson_id:

        questions = get_accounting_quiz(
            chapter_id,
            lesson_id,
        )

    else:

        questions = get_all_quiz_questions()

    if not _prepare_quiz(
        context,
        questions,
        chapter_id,
        lesson_id,
    ):

        await _edit_or_reply(
            update,
            "⚠️ برای این بخش هنوز سؤال آزمون ثبت نشده است.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="menu_accounting",
                        )
                    ]
                ]
            ),
        )
        return

    await _show_next_quiz_question(
        update,
        context,
    )


# ==========================================================
# Chapter Quiz
# ==========================================================

async def start_accounting_chapter_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await _answer_callback(update)

    query = update.callback_query

    chapter_id = None

    if query is not None:

        data = query.data or ""

        if data.startswith(
            "accounting_quiz_chapter:"
        ):
            chapter_id = data.split(
                ":",
                1,
            )[1]

    if not chapter_id:

        await show_accounting_menu(
            update,
            context,
        )
        return

    questions: list[dict[str, Any]] = []

    for lesson in get_accounting_lessons(
        chapter_id
    ):

        lesson_id = str(
            lesson.get("id")
            or ""
        ).strip()

        if not lesson_id:
            continue

        questions.extend(
            get_accounting_quiz(
                chapter_id,
                lesson_id,
            )
        )

    if not _prepare_quiz(
        context,
        questions,
        chapter_id,
        None,
    ):

        await _edit_or_reply(
            update,
            "⚠️ برای این فصل هنوز آزمون ثبت نشده است.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                "accounting_chapter:"
                                f"{chapter_id}"
                            ),
                        )
                    ]
                ]
            ),
        )
        return

    await _show_next_quiz_question(
        update,
        context,
    )


# ==========================================================
# Show Quiz Question
# ==========================================================

async def _show_next_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY,
        [],
    )

    index = context.user_data.get(
        QUIZ_INDEX_KEY,
        0,
    )

    if index >= len(questions):

        await finish_accounting_quiz(
            update,
            context,
        )
        return

    question = questions[index]

    options = question.get(
        "options",
        [],
    )

    keyboard: list[list[InlineKeyboardButton]] = []

    for option_index, option in enumerate(options):

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{chr(65 + option_index)}. {str(option)}",
                    callback_data=(
                        "accounting_quiz_answer:"
                        f"{option_index}"
                    ),
                )
            ]
        )

    total = len(questions)

    text = (
        "🧾 <b>آزمون حسابداری</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"سؤال <b>{index + 1}</b> از <b>{total}</b>\n\n"
        f"❓ {_safe_text(question.get('question', ''))}"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(keyboard),
    )


# ==========================================================
# Answer Quiz
# ==========================================================

async def answer_accounting_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await _answer_callback(update)

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if not data.startswith(
        "accounting_quiz_answer:"
    ):
        return

    try:

        selected = int(
            data.split(
                ":",
                1,
            )[1]
        )

    except Exception:
        return

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY,
        [],
    )

    index = context.user_data.get(
        QUIZ_INDEX_KEY,
        0,
    )

    if not questions or index >= len(questions):
        return

    question = questions[index]

    correct_index = int(
        question.get(
            "correct_index",
            -1,
        )
    )

    if selected == correct_index:

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
            "✅ <b>پاسخ شما درست بود.</b>"
        )

    else:

        options = question.get(
            "options",
            [],
        )

        correct_text = ""

        if (
            0 <= correct_index < len(options)
        ):
            correct_text = str(
                options[correct_index]
            )

        result_text = (
            "❌ <b>پاسخ شما نادرست بود.</b>\n\n"
            "پاسخ صحیح: "
            f"<b>{_safe_text(correct_text)}</b>"
        )

    context.user_data[
        QUIZ_INDEX_KEY
    ] = index + 1

    await _edit_or_reply(
        update,
        result_text,
    )

    await _show_next_quiz_question(
        update,
        context,
    )


# ==========================================================
# Finish Quiz
# ==========================================================

async def finish_accounting_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY,
        [],
    )

    total = len(questions)

    score = int(
        context.user_data.get(
            QUIZ_SCORE_KEY,
            0,
        )
    )

    wrong = max(
        total - score,
        0,
    )

    percentage = (
        (score / total) * 100
        if total
        else 0
    )

    text = (
        "🏁 <b>آزمون حسابداری به پایان رسید</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 تعداد سوالات: <b>{total}</b>\n"
        f"✅ پاسخ صحیح: <b>{score}</b>\n"
        f"❌ پاسخ غلط: <b>{wrong}</b>\n"
        f"📊 نمره: <b>{percentage:.2f}%</b>\n\n"
        "نتیجه آزمون ثبت شد."
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 آزمون مجدد",
                    callback_data="accounting_quiz_all",
                )
            ],
            [
                InlineKeyboardButton(
                    "🧾 بازگشت به حسابداری",
                    callback_data="menu_accounting",
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="menu_main",
                )
            ],
        ]
    )

    await _edit_or_reply(
        update,
        text,
        keyboard,
    )

    for key in (
        QUIZ_QUESTIONS_KEY,
        QUIZ_INDEX_KEY,
        QUIZ_SCORE_KEY,
        QUIZ_CHAPTER_KEY,
        QUIZ_LESSON_KEY,
    ):

        context.user_data.pop(
            key,
            None,
        )


# ==========================================================
# Statistics
# ==========================================================

async def show_accounting_statistics(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await _answer_callback(update)

    stats = get_curriculum_stats()

    text = (
        "📊 <b>آمار آموزش حسابداری</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 فصل‌ها: <b>{stats['chapters']}</b>\n"
        f"📘 درس‌ها: <b>{stats['lessons']}</b>\n"
        f"📝 سوالات: <b>{stats['quiz_questions']}</b>\n\n"
        "🎓 سطح دوره: پایه تا فوق‌تخصصی\n\n"
        "موضوعات دوره شامل حسابداری مالی، مدیریت، صنعتی، "
        "مالیاتی، شرکت‌ها، حسابرسی، تحلیل مالی، IFRS و "
        "فناوری‌های نوین حسابداری است."
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data="menu_accounting",
                    )
                ]
            ]
        ),
    )


# ==========================================================
# Compatibility Aliases
# ==========================================================

show_accounting = show_accounting_menu

show_accounting_chapters = show_accounting_menu

show_accounting_chapter_menu = show_accounting_chapter

show_accounting_lesson_content = show_accounting_lesson

start_accounting_quiz_lesson = start_accounting_quiz

start_accounting_quiz_all = start_accounting_quiz

handle_accounting_quiz_answer = answer_accounting_quiz


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "show_accounting_menu",
    "show_accounting",
    "show_accounting_chapters",
    "show_accounting_chapter",
    "show_accounting_chapter_menu",
    "show_accounting_lesson",
    "show_accounting_lesson_content",
    "start_accounting_quiz",
    "start_accounting_quiz_all",
    "start_accounting_quiz_lesson",
    "start_accounting_chapter_quiz",
    "answer_accounting_quiz",
    "handle_accounting_quiz_answer",
    "finish_accounting_quiz",
    "show_accounting_statistics",
]
