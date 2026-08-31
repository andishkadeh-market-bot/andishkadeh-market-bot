"""
Telegram handlers for the Management educational module.

Andishkadeh Management & Market
--------------------------------
This module provides Telegram handlers for:
- Management chapters
- Management lessons
- Lesson details
- Specialized tips
- Exam tips
- Practical examples
- Review points

The content source is modules.management.data.
"""

from __future__ import annotations

import logging
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
# Helpers
# ==========================================================

def _chapter_button_text(chapter: dict[str, Any]) -> str:
    """Return the visible title of a chapter."""
    return str(chapter.get("title", "فصل بدون عنوان"))


def _lesson_button_text(lesson: dict[str, Any]) -> str:
    """Return the visible title of a lesson."""
    return str(lesson.get("title", "درس بدون عنوان"))


def _chapter_keyboard(
    chapters: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build the Management chapter keyboard."""

    keyboard: list[list[InlineKeyboardButton]] = []

    for chapter in chapters:
        chapter_id = chapter.get("id")

        if not chapter_id:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    _chapter_button_text(chapter),
                    callback_data=f"management:chapter:{chapter_id}",
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

    return InlineKeyboardMarkup(keyboard)


def _lesson_keyboard(
    chapter_id: str,
    lessons: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build the lesson keyboard for a chapter."""

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
                "🔙 بازگشت به فصل‌ها",
                callback_data="management:menu",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def _lesson_detail_keyboard(
    chapter_id: str,
) -> InlineKeyboardMarkup:
    """Build navigation keyboard for a lesson."""

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
    """Format a list of educational points."""

    if not items:
        return ""

    lines = [f"\n<b>{title}</b>"]

    for item in items:
        lines.append(f"• {item}")

    return "\n".join(lines)


def _format_lesson(
    chapter: dict[str, Any],
    lesson: dict[str, Any],
) -> str:
    """Create the full Telegram lesson message."""

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

    message_parts: list[str] = [
        f"📚 <b>{MODULE_TITLE}</b>",
        f"📖 <b>{chapter_title}</b>",
        f"📝 <b>{lesson_title}</b>",
    ]

    if summary:
        message_parts.extend(
            [
                "",
                f"📌 <b>خلاصه درس</b>",
                str(summary),
            ]
        )

    if content:
        message_parts.extend(
            [
                "",
                "📖 <b>درسنامه</b>",
                str(content),
            ]
        )

    specialized_text = _format_list(
        "🎯 نکات تخصصی",
        specialized_tips,
    )

    if specialized_text:
        message_parts.append(
            specialized_text
        )

    exam_text = _format_list(
        "📝 نکات آزمونی",
        exam_tips,
    )

    if exam_text:
        message_parts.append(
            exam_text
        )

    examples_text = _format_list(
        "💡 مثال‌های کاربردی",
        examples,
    )

    if examples_text:
        message_parts.append(
            examples_text
        )

    review_text = _format_list(
        "🔄 مرور",
        review,
    )

    if review_text:
        message_parts.append(
            review_text
        )

    return "\n".join(
        message_parts
    )


# ==========================================================
# Public menu handlers
# ==========================================================

async def show_management_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show the Management module menu.
    """

    if update.callback_query:
        query = update.callback_query
        await query.answer()

        text = (
            "📚 <b>آموزش مدیریت</b>\n\n"
            f"{MODULE_DESCRIPTION}\n\n"
            "یکی از فصل‌های زیر را انتخاب کنید:"
        )

        await query.edit_message_text(
            text=text,
            reply_markup=_chapter_keyboard(
                get_management_chapters()
            ),
            parse_mode="HTML",
        )

        return

    if update.message:
        text = (
            "📚 <b>آموزش مدیریت</b>\n\n"
            f"{MODULE_DESCRIPTION}\n\n"
            "یکی از فصل‌های زیر را انتخاب کنید:"
        )

        await update.message.reply_text(
            text=text,
            reply_markup=_chapter_keyboard(
                get_management_chapters()
            ),
            parse_mode="HTML",
        )


# Compatibility alias
show_management = show_management_menu


async def show_management_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show Management chapters."""

    await show_management_menu(
        update,
        context,
    )


# ==========================================================
# Chapter handlers
# ==========================================================

async def show_management_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show lessons belonging to a Management chapter.

    Expected callback:
        management:chapter:<chapter_id>
    """

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


# Compatibility aliases
show_chapter = show_management_chapter
show_management_chapter_menu = show_management_chapter


# ==========================================================
# Lesson handlers
# ==========================================================

async def show_management_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show one Management lesson.

    Expected callback:
        management:lesson:<chapter_id>:<lesson_id>
    """

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


# Compatibility aliases
show_lesson = show_management_lesson
show_management_lesson_detail = show_management_lesson


# ==========================================================
# Callback router
# ==========================================================

async def management_callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route Management callback queries.

    Supported callbacks:
        management:menu
        management:back
        management:chapter:<chapter_id>
        management:lesson:<chapter_id>:<lesson_id>
    """

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
    """
    Validate Management handler dependencies.
    """

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


# Compatibility alias
handlers_health_check = (
    management_handlers_health_check
)


# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "show_management_menu",
    "show_management",
    "show_management_chapters",
    "show_management_chapter",
    "show_management_chapter_menu",
    "show_management_lesson",
    "show_management_lesson_detail",
    "show_chapter",
    "show_lesson",
    "management_callback_handler",
    "management_handlers_health_check",
    "handlers_health_check",
    "MANAGEMENT_CHAPTERS",
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
]
