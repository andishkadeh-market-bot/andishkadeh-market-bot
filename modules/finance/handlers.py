"""
Finance handlers for Andishkadeh Management & Market.

Responsibilities:
- Show the Finance module menu
- Show finance chapters
- Show lessons inside a chapter
- Show lesson content
- Handle navigation callbacks
- Keep finance UI isolated from core/menu.py

This module does not modify database progress directly.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .data import (
    MODULE_ID,
    MODULE_TITLE,
    MODULE_DESCRIPTION,
    get_chapters,
    get_lessons,
    data_health_check,
)


# ============================================================
# Callback prefixes
# ============================================================

FINANCE_MENU_CALLBACK = "finance_menu"
FINANCE_CHAPTER_PREFIX = "finance_chapter:"
FINANCE_LESSON_PREFIX = "finance_lesson:"
FINANCE_BACK_CALLBACK = "finance_back"
MAIN_MENU_CALLBACK = "menu_main"


# ============================================================
# Helpers
# ============================================================

def _get_chapters():
    """Return finance chapters safely."""
    try:
        return get_chapters()
    except Exception:
        return []


def _get_lessons():
    """Return finance lessons safely."""
    try:
        return get_lessons()
    except Exception:
        return []


def _find_chapter(chapter_id: str):
    """Find a chapter by ID."""
    for chapter in _get_chapters():
        if str(chapter.get("id")) == str(chapter_id):
            return chapter
    return None


def _find_lesson(lesson_id: str):
    """Find a lesson by ID."""
    for lesson in _get_lessons():
        if str(lesson.get("id")) == str(lesson_id):
            return lesson
    return None


def _get_chapter_lessons(chapter_id: str):
    """Return lessons belonging to a chapter."""
    return [
        lesson
        for lesson in _get_lessons()
        if str(lesson.get("chapter_id")) == str(chapter_id)
    ]


def _main_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for the finance main menu."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📚 فصل‌های مدیریت مالی",
                    callback_data=FINANCE_MENU_CALLBACK,
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data=MAIN_MENU_CALLBACK,
                )
            ],
        ]
    )


def _chapters_keyboard() -> InlineKeyboardMarkup:
    """Keyboard containing all finance chapters."""
    buttons = []

    for chapter in _get_chapters():
        chapter_id = str(chapter.get("id", "")).strip()
        title = str(chapter.get("title", "فصل بدون عنوان")).strip()

        if not chapter_id:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    f"📖 {title}",
                    callback_data=f"{FINANCE_CHAPTER_PREFIX}{chapter_id}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "🔙 مدیریت مالی",
                callback_data=FINANCE_BACK_CALLBACK,
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


def _chapter_keyboard(chapter_id: str) -> InlineKeyboardMarkup:
    """Keyboard containing lessons of a chapter."""
    buttons = []

    for lesson in _get_chapter_lessons(chapter_id):
        lesson_id = str(lesson.get("id", "")).strip()
        title = str(lesson.get("title", "درس بدون عنوان")).strip()

        if not lesson_id:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    f"📘 {title}",
                    callback_data=f"{FINANCE_LESSON_PREFIX}{lesson_id}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "🔙 فصل‌های مدیریت مالی",
                callback_data=FINANCE_MENU_CALLBACK,
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


def _lesson_keyboard(chapter_id: str) -> InlineKeyboardMarkup:
    """Keyboard for lesson navigation."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 فهرست فصل",
                    callback_data=f"{FINANCE_CHAPTER_PREFIX}{chapter_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 همه فصل‌ها",
                    callback_data=FINANCE_MENU_CALLBACK,
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data=MAIN_MENU_CALLBACK,
                )
            ],
        ]
    )


# ============================================================
# Screens
# ============================================================

async def show_finance_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show the main Finance module screen."""
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    chapters = _get_chapters()
    lessons = _get_lessons()

    text = (
        f"💰 <b>{MODULE_TITLE}</b>\n\n"
        f"{MODULE_DESCRIPTION}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"📚 تعداد فصل‌ها: {len(chapters)}\n"
        f"📖 تعداد درس‌ها: {len(lessons)}\n"
        "━━━━━━━━━━━━━━\n\n"
        "از بخش زیر یک گزینه را انتخاب کنید:"
    )

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=_main_keyboard(),
    )


async def show_finance_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show all Finance chapters."""
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    chapters = _get_chapters()

    if not chapters:
        await query.edit_message_text(
            "❌ هیچ فصلی برای مدیریت مالی ثبت نشده است.",
            reply_markup=_main_keyboard(),
        )
        return

    lines = [
        f"💰 <b>{MODULE_TITLE}</b>",
        "",
        "📚 <b>فهرست فصل‌ها</b>",
        "",
    ]

    for index, chapter in enumerate(chapters, start=1):
        title = str(
            chapter.get("title", "فصل بدون عنوان")
        ).strip()

        description = str(
            chapter.get("description", "")
        ).strip()

        lines.append(f"<b>فصل {index}: {title}</b>")

        if description:
            lines.append(description)

        lines.append("")

    await query.edit_message_text(
        "\n".join(lines),
        parse_mode=ParseMode.HTML,
        reply_markup=_chapters_keyboard(),
    )


async def show_finance_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
) -> None:
    """Show lessons of a selected Finance chapter."""
    query = update.callback_query

    if query is None:
        return

    chapter = _find_chapter(chapter_id)

    if chapter is None:
        await query.answer(
            "❌ فصل موردنظر پیدا نشد.",
            show_alert=True,
        )
        return

    await query.answer()

    title = str(
        chapter.get("title", "فصل بدون عنوان")
    ).strip()

    description = str(
        chapter.get("description", "")
    ).strip()

    lessons = _get_chapter_lessons(chapter_id)

    lines = [
        f"💰 <b>{MODULE_TITLE}</b>",
        "",
        f"📖 <b>{title}</b>",
    ]

    if description:
        lines.extend(
            [
                "",
                description,
            ]
        )

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━",
            f"📚 تعداد درس‌ها: {len(lessons)}",
            "━━━━━━━━━━━━━━",
            "",
            "یک درس را انتخاب کنید:",
        ]
    )

    await query.edit_message_text(
        "\n".join(lines),
        parse_mode=ParseMode.HTML,
        reply_markup=_chapter_keyboard(chapter_id),
    )


async def show_finance_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    lesson_id: str,
) -> None:
    """Show a Finance lesson."""
    query = update.callback_query

    if query is None:
        return

    lesson = _find_lesson(lesson_id)

    if lesson is None:
        await query.answer(
            "❌ درس موردنظر پیدا نشد.",
            show_alert=True,
        )
        return

    await query.answer()

    chapter_id = str(
        lesson.get("chapter_id", "")
    ).strip()

    title = str(
        lesson.get("title", "درس بدون عنوان")
    ).strip()

    description = str(
        lesson.get("description", "")
    ).strip()

    chapter = _find_chapter(chapter_id)

    chapter_title = ""

    if chapter is not None:
        chapter_title = str(
            chapter.get("title", "")
        ).strip()

    lines = [
        f"💰 <b>{MODULE_TITLE}</b>",
        "",
    ]

    if chapter_title:
        lines.append(f"📖 <b>{chapter_title}</b>")
        lines.append("")

    lines.extend(
        [
            f"📘 <b>{title}</b>",
            "",
            "━━━━━━━━━━━━━━",
            "",
        ]
    )

    if description:
        lines.append(description)
    else:
        lines.append(
            "محتوای آموزشی این درس در حال تکمیل است."
        )

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━",
            "",
            "🎓 <b>درس مدیریت مالی</b>",
            "",
            "برای ادامه آموزش از دکمه‌های زیر استفاده کنید.",
        ]
    )

    await query.edit_message_text(
        "\n".join(lines),
        parse_mode=ParseMode.HTML,
        reply_markup=_lesson_keyboard(chapter_id),
    )


# ============================================================
# Callback Router
# ============================================================

async def route_finance_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route Finance callbacks.

    Supported callbacks:
    - finance_menu
    - finance_back
    - finance_chapter:<chapter_id>
    - finance_lesson:<lesson_id>
    """
    query = update.callback_query

    if query is None:
        return

    callback_data = query.data or ""

    if callback_data == FINANCE_MENU_CALLBACK:
        await show_finance_chapters(update, context)
        return

    if callback_data == FINANCE_BACK_CALLBACK:
        await show_finance_menu(update, context)
        return

    if callback_data.startswith(FINANCE_CHAPTER_PREFIX):
        chapter_id = callback_data[
            len(FINANCE_CHAPTER_PREFIX):
        ].strip()

        if chapter_id:
            await show_finance_chapter(
                update,
                context,
                chapter_id,
            )

        return

    if callback_data.startswith(FINANCE_LESSON_PREFIX):
        lesson_id = callback_data[
            len(FINANCE_LESSON_PREFIX):
        ].strip()

        if lesson_id:
            await show_finance_lesson(
                update,
                context,
                lesson_id,
            )

        return


# ============================================================
# Health Check
# ============================================================

def finance_handlers_health_check() -> dict:
    """Return health information for Finance handlers."""
    result = {
        "module": "finance.handlers",
        "status": "ok",
        "module_id": MODULE_ID,
        "dependencies": {},
    }

    try:
        health = data_health_check()

        result["dependencies"]["finance.data"] = health

        if isinstance(health, dict):
            status = health.get("status")

            if status not in (None, "ok", "healthy"):
                result["status"] = "warning"

    except Exception as exc:
        result["status"] = "error"
        result["dependencies"]["finance.data"] = {
            "status": "error",
            "error": str(exc),
        }

    try:
        chapters = _get_chapters()
        lessons = _get_lessons()

        result["chapters"] = len(chapters)
        result["lessons"] = len(lessons)

    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)

    return result


# ============================================================
# Public API
# ============================================================

__all__ = [
    "FINANCE_MENU_CALLBACK",
    "FINANCE_CHAPTER_PREFIX",
    "FINANCE_LESSON_PREFIX",
    "FINANCE_BACK_CALLBACK",
    "MAIN_MENU_CALLBACK",
    "show_finance_menu",
    "show_finance_chapters",
    "show_finance_chapter",
    "show_finance_lesson",
    "route_finance_callback",
    "finance_handlers_health_check",
]
