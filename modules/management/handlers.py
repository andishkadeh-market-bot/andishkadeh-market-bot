"""
Telegram handlers for the Management educational module.

Andishkadeh Management & Market
--------------------------------
Management module handlers including:
- Management menu
- Chapters
- Lessons
- Lesson details
- Specialized tips
- Exam tips
- Practical examples
- Review
- Management quiz

Content source:
    modules.management.data
"""

from __future__ import annotations

import logging
import random
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from modules.management.data import (
    MODULE_ID,
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    MANAGEMENT_CHAPTERS,
    get_management_chapters,
    get_management_chapter,
    get_management_lessons,
    get_management_lesson,
    management_data_health_check,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Compatibility data
# ==========================================================

# Some older parts of the project may still import this name.
# It is generated automatically from MANAGEMENT_CHAPTERS.

MANAGEMENT_CHAPTER_LESSONS: dict[str, list[dict[str, Any]]] = {
    str(chapter.get("id")): list(
        chapter.get("lessons", [])
    )
    for chapter in MANAGEMENT_CHAPTERS
    if chapter.get("id")
}


# ==========================================================
# General helpers
# ==========================================================

def _chapter_button_text(
    chapter: dict[str, Any],
) -> str:
    return str(
        chapter.get(
            "title",
            "فصل بدون عنوان",
        )
    )


def _lesson_button_text(
    lesson: dict[str, Any],
) -> str:
    return str(
        lesson.get(
            "title",
            "درس بدون عنوان",
        )
    )


def _chapter_keyboard(
    chapters: list[dict[str, Any]],
) -> InlineKeyboardMarkup:

    keyboard: list[list[InlineKeyboardButton]] = []

    for chapter in chapters:

        chapter_id = chapter.get("id")

        if not chapter_id:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    _chapter_button_text(chapter),
                    callback_data=(
                        f"management:chapter:{chapter_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🎯 آزمون مدیریت",
                callback_data="management:quiz",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="management:back",
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


def _lesson_keyboard(
    chapter_id: str,
    lessons: list[dict[str, Any]],
) -> InlineKeyboardMarkup:

    keyboard: list[list[InlineKeyboardButton]] = []

    for lesson in lessons:

        lesson_id = lesson.get("id")

        if not lesson_id:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    _lesson_button_text(lesson),
                    callback_data=(
                        f"management:lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🎯 آزمون مدیریت",
                callback_data="management:quiz",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به فصل‌ها",
                callback_data="management:menu",
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


def _lesson_detail_keyboard(
    chapter_id: str,
) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به درس‌ها",
                    callback_data=(
                        f"management:chapter:{chapter_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 فهرست مدیریت",
                    callback_data="management:menu",
                )
            ],
        ]
    )


def _format_list(
    title: str,
    items: list[Any],
) -> str:

    if not items:
        return ""

    lines = [
        f"\n<b>{title}</b>"
    ]

    for item in items:
        lines.append(
            f"• {item}"
        )

    return "\n".join(
        lines
    )


def _format_lesson(
    chapter: dict[str, Any],
    lesson: dict[str, Any],
) -> str:

    chapter_title = chapter.get(
        "title",
        "فصل",
    )

    lesson_title = lesson.get(
        "title",
        "درس",
    )

    summary = lesson.get(
        "summary",
        "",
    )

    content = lesson.get(
        "content",
        "",
    )

    specialized_tips = lesson.get(
        "specialized_tips",
        [],
    )

    exam_tips = lesson.get(
        "exam_tips",
        [],
    )

    examples = lesson.get(
        "examples",
        [],
    )

    review = lesson.get(
        "review",
        [],
    )

    parts: list[str] = [
        f"📚 <b>{MODULE_TITLE}</b>",
        f"📖 <b>{chapter_title}</b>",
        f"📝 <b>{lesson_title}</b>",
    ]

    if summary:

        parts.extend(
            [
                "",
                "📌 <b>خلاصه درس</b>",
                str(summary),
            ]
        )

    if content:

        parts.extend(
            [
                "",
                "📖 <b>درسنامه</b>",
                str(content),
            ]
        )

    specialized = _format_list(
        "🎯 نکات تخصصی",
        specialized_tips,
    )

    if specialized:
        parts.append(
            specialized
        )

    exam = _format_list(
        "📝 نکات آزمونی",
        exam_tips,
    )

    if exam:
        parts.append(
            exam
        )

    examples_text = _format_list(
        "💡 مثال‌های کاربردی",
        examples,
    )

    if examples_text:
        parts.append(
            examples_text
        )

    review_text = _format_list(
        "🔄 مرور",
        review,
    )

    if review_text:
        parts.append(
            review_text
        )

    return "\n".join(
        parts
    )


# ==========================================================
# Management main menu
# ==========================================================

async def show_management_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    text = (
        "📚 <b>آموزش مدیریت</b>\n\n"
        f"{MODULE_DESCRIPTION}\n\n"
        "یکی از فصل‌های زیر را انتخاب کنید:"
    )

    keyboard = _chapter_keyboard(
        get_management_chapters()
    )

    if update.callback_query:

        query = update.callback_query

        await query.answer()

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

        return

    if update.message:

        await update.message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


# Compatibility aliases

show_management = show_management_menu

show_management_chapters = show_management_menu


# ==========================================================
# Chapter handler
# ==========================================================

async def show_management_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    prefix = "management:chapter:"

    if not data.startswith(prefix):
        return

    chapter_id = data[
        len(prefix):
    ]

    chapter = get_management_chapter(
        chapter_id
    )

    if chapter is None:

        await query.edit_message_text(
            "❌ فصل موردنظر پیدا نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="management:menu",
                        )
                    ]
                ]
            ),
        )

        return

    lessons = get_management_lessons(
        chapter_id
    )

    if not lessons:

        logger.warning(
            "Management chapter '%s' has no lessons.",
            chapter_id,
        )

        await query.edit_message_text(
            (
                f"📖 <b>{chapter.get('title', 'فصل')}</b>\n\n"
                "⚠️ برای این فصل هنوز درسی ثبت نشده است."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به فصل‌ها",
                            callback_data="management:menu",
                        )
                    ]
                ]
            ),
            parse_mode="HTML",
        )

        return

    text = (
        f"📖 <b>{chapter.get('title', 'فصل')}</b>\n\n"
        f"{chapter.get('description', '')}\n\n"
        "📝 <b>درس‌های این فصل:</b>"
    )

    await query.edit_message_text(
        text=text,
        reply_markup=_lesson_keyboard(
            chapter_id,
            lessons,
        ),
        parse_mode="HTML",
    )


show_chapter = show_management_chapter

show_management_chapter_menu = (
    show_management_chapter
)


# ==========================================================
# Lesson handler
# ==========================================================

async def show_management_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    prefix = "management:lesson:"

    if not data.startswith(prefix):
        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":",
        1,
    )

    if len(parts) != 2:

        await query.edit_message_text(
            "❌ اطلاعات درس نامعتبر است."
        )

        return

    chapter_id, lesson_id = parts

    chapter = get_management_chapter(
        chapter_id
    )

    if chapter is None:

        await query.edit_message_text(
            "❌ فصل موردنظر پیدا نشد."
        )

        return

    lesson = get_management_lesson(
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    if lesson is None:

        await query.edit_message_text(
            "❌ درس موردنظر پیدا نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                f"management:chapter:{chapter_id}"
                            ),
                        )
                    ]
                ]
            ),
        )

        return

    text = _format_lesson(
        chapter,
        lesson,
    )

    await query.edit_message_text(
        text=text,
        reply_markup=_lesson_detail_keyboard(
            chapter_id
        ),
        parse_mode="HTML",
    )


show_lesson = show_management_lesson

show_management_lesson_detail = (
    show_management_lesson
)


# ==========================================================
# Management Quiz
# ==========================================================

def _build_management_quiz_questions() -> list[dict[str, Any]]:
    """
    Build quiz questions from Management lessons.

    Each lesson review item becomes a question prompt
    only when an explicit question bank is available.

    If no dedicated quiz bank exists, the function returns
    an empty list rather than inventing answer keys.
    """

    questions: list[dict[str, Any]] = []

    for chapter in MANAGEMENT_CHAPTERS:

        lessons = chapter.get(
            "lessons",
            [],
        )

        for lesson in lessons:

            lesson_questions = lesson.get(
                "questions",
                [],
            )

            if not isinstance(
                lesson_questions,
                list,
            ):
                continue

            for question in lesson_questions:

                if not isinstance(
                    question,
                    dict,
                ):
                    continue

                if not question.get(
                    "question"
                ):
                    continue

                options = question.get(
                    "options"
                )

                correct_index = question.get(
                    "correct_index"
                )

                if not isinstance(
                    options,
                    list,
                ):
                    continue

                if len(options) != 4:
                    continue

                if not isinstance(
                    correct_index,
                    int,
                ):
                    continue

                if (
                    correct_index < 0
                    or correct_index >= len(options)
                ):
                    continue

                questions.append(
                    {
                        "question": question[
                            "question"
                        ],
                        "options": list(
                            options
                        ),
                        "correct_index": correct_index,
                    }
                )

    return questions


async def start_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start the Management quiz.

    The function is intentionally compatible with
    core.menu imports.

    If the Management data file does not yet contain
    a dedicated question bank, the user receives a
    clear message instead of a fake quiz.
    """

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    questions = _build_management_quiz_questions()

    if not questions:

        await query.edit_message_text(
            (
                "🎯 <b>آزمون مدیریت</b>\n\n"
                "بانک سوالات اختصاصی مدیریت هنوز "
                "در داده‌های این ماژول ثبت نشده است.\n\n"
                "📚 ابتدا از بخش درسنامه استفاده کنید."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📚 آموزش مدیریت",
                            callback_data="management:menu",
                        )
                    ]
                ]
            ),
            parse_mode="HTML",
        )

        return

    question = random.choice(
        questions
    )

    question_text = str(
        question["question"]
    )

    options = question["options"]

    keyboard: list[list[InlineKeyboardButton]] = []

    for index, option in enumerate(
        options
    ):

        keyboard.append(
            [
                InlineKeyboardButton(
                    str(option),
                    callback_data=(
                        f"management:quiz_answer:"
                        f"{question_text[:20]}:"
                        f"{index}:"
                        f"{question['correct_index']}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="management:menu",
            )
        ]
    )

    await query.edit_message_text(
        (
            "🎯 <b>آزمون مدیریت</b>\n\n"
            f"❓ {question_text}\n\n"
            "گزینه صحیح را انتخاب کنید:"
        ),
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
        parse_mode="HTML",
    )


# ==========================================================
# Quiz answer handler
# ==========================================================

async def management_quiz_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    prefix = "management:quiz_answer:"

    if not data.startswith(prefix):
        return

    payload = data[
        len(prefix):
    ]

    parts = payload.rsplit(
        ":",
        2,
    )

    if len(parts) != 3:

        await query.edit_message_text(
            "❌ پاسخ آزمون نامعتبر است."
        )

        return

    _question_preview, selected_raw, correct_raw = parts

    try:

        selected_index = int(
            selected_raw
        )

        correct_index = int(
            correct_raw
        )

    except ValueError:

        await query.edit_message_text(
            "❌ پاسخ آزمون نامعتبر است."
        )

        return

    if selected_index == correct_index:

        result = (
            "✅ <b>پاسخ شما صحیح است.</b>\n\n"
            "آفرین. یک امتیاز برای شما ثبت شد."
        )

    else:

        result = (
            "❌ <b>پاسخ شما صحیح نیست.</b>\n\n"
            "پاسخ صحیح را از طریق مرور درس بررسی کنید."
        )

    await query.edit_message_text(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎯 سوال بعدی",
                        callback_data="management:quiz",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 آموزش مدیریت",
                        callback_data="management:menu",
                    )
                ],
            ]
        ),
        parse_mode="HTML",
    )


# ==========================================================
# Callback router
# ==========================================================

async def management_callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if data in {
        "management:menu",
        "management:back",
    }:

        await show_management_menu(
            update,
            context,
        )

        return

    if data == "management:quiz":

        await start_management_quiz(
            update,
            context,
        )

        return

    if data.startswith(
        "management:quiz_answer:"
    ):

        await management_quiz_answer(
            update,
            context,
        )

        return

    if data.startswith(
        "management:chapter:"
    ):

        await show_management_chapter(
            update,
            context,
        )

        return

    if data.startswith(
        "management:lesson:"
    ):

        await show_management_lesson(
            update,
            context,
        )

        return


# ==========================================================
# Health check
# ==========================================================

def management_handlers_health_check() -> bool:

    try:

        if not management_data_health_check():
            return False

        chapters = get_management_chapters()

        if not chapters:
            return False

        for chapter in chapters:

            chapter_id = chapter.get(
                "id"
            )

            if not chapter_id:
                return False

            lessons = chapter.get(
                "lessons",
                [],
            )

            if not isinstance(
                lessons,
                list,
            ):
                return False

        return True

    except Exception:

        logger.exception(
            "Management handlers health check failed."
        )

        return False


handlers_health_check = (
    management_handlers_health_check
)


# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "MANAGEMENT_CHAPTERS",
    "MANAGEMENT_CHAPTER_LESSONS",
    "show_management_menu",
    "show_management",
    "show_management_chapters",
    "show_management_chapter",
    "show_management_chapter_menu",
    "show_management_lesson",
    "show_management_lesson_detail",
    "show_chapter",
    "show_lesson",
    "start_management_quiz",
    "management_quiz_answer",
    "management_callback_handler",
    "management_handlers_health_check",
    "handlers_health_check",
]
