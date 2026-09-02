"""
Finance handlers for Andishkadeh Management & Market.

Responsibilities:
- Show Finance main menu
- Show Finance chapters
- Show lessons inside a chapter
- Show complete educational content
- Navigate between Finance screens
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .content import get_lesson_content
from .data import get_chapters, get_lessons


# =========================================================
# Callback constants
# =========================================================

FINANCE_MENU_CALLBACK = "finance_menu"
FINANCE_CHAPTER_PREFIX = "finance_chapter:"
FINANCE_LESSON_PREFIX = "finance_lesson:"
FINANCE_BACK_CALLBACK = "finance_back"
MAIN_MENU_CALLBACK = "menu_main"


# =========================================================
# Data helpers
# =========================================================

def _get_chapters() -> list:
    """Return all Finance chapters."""
    try:
        return get_chapters()
    except Exception:
        return []


def _get_lessons() -> list:
    """Return all Finance lessons."""
    try:
        return get_lessons()
    except Exception:
        return []


def _find_chapter(chapter_id: str):
    """Find a Finance chapter by ID."""

    for chapter in _get_chapters():
        if chapter.get("chapter_id") == chapter_id:
            return chapter

    return None


def _find_lesson(lesson_id: str):
    """Find a Finance lesson by ID."""

    for lesson in _get_lessons():
        if lesson.get("lesson_id") == lesson_id:
            return lesson

    return None


def _get_chapter_lessons(chapter_id: str) -> list:
    """Return lessons belonging to a chapter."""

    return [
        lesson
        for lesson in _get_lessons()
        if lesson.get("chapter_id") == chapter_id
    ]


# =========================================================
# Keyboard helpers
# =========================================================

def _finance_main_keyboard() -> InlineKeyboardMarkup:
    """Finance main keyboard."""

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


def _finance_chapters_keyboard() -> InlineKeyboardMarkup:
    """Keyboard containing Finance chapters."""

    rows = []

    for chapter in _get_chapters():
        chapter_id = chapter.get("chapter_id")
        title = chapter.get(
            "title",
            "فصل بدون عنوان",
        )

        if not chapter_id:
            continue

        rows.append(
            [
                InlineKeyboardButton(
                    f"📘 {title}",
                    callback_data=(
                        f"{FINANCE_CHAPTER_PREFIX}{chapter_id}"
                    ),
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(rows)


def _finance_chapter_keyboard(
    chapter_id: str,
) -> InlineKeyboardMarkup:
    """Keyboard containing lessons of a chapter."""

    rows = []

    for lesson in _get_chapter_lessons(chapter_id):
        lesson_id = lesson.get("lesson_id")
        title = lesson.get(
            "title",
            "درس بدون عنوان",
        )

        if not lesson_id:
            continue

        rows.append(
            [
                InlineKeyboardButton(
                    f"📖 {title}",
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}{lesson_id}"
                    ),
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                "⬅️ بازگشت به فصل‌ها",
                callback_data=FINANCE_MENU_CALLBACK,
            )
        ]
    )

    rows.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(rows)


def _finance_lesson_keyboard(
    chapter_id: str | None = None,
) -> InlineKeyboardMarkup:
    """Keyboard for a Finance lesson."""

    rows = []

    if chapter_id:
        rows.append(
            [
                InlineKeyboardButton(
                    "⬅️ بازگشت به درس‌های فصل",
                    callback_data=(
                        f"{FINANCE_CHAPTER_PREFIX}{chapter_id}"
                    ),
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                "📚 فصل‌های مدیریت مالی",
                callback_data=FINANCE_MENU_CALLBACK,
            )
        ]
    )

    rows.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(rows)


# =========================================================
# Content formatting
# =========================================================

def _format_points(
    title: str,
    points: list,
    emoji: str = "•",
) -> str:
    """Format a list of educational points."""

    if not points:
        return ""

    lines = [
        f"<b>{title}</b>"
    ]

    for point in points:
        if point:
            lines.append(
                f"{emoji} {point}"
            )

    return "\n".join(lines)


def _format_lesson_content(
    content: dict,
) -> str:
    """
    Convert Finance lesson content into a Telegram message.
    """

    title = content.get(
        "title",
        "درس مدیریت مالی",
    )

    lesson_text = content.get(
        "lesson_text",
        "",
    )

    subtopics = content.get(
        "subtopics",
        [],
    )

    detailed_content = content.get(
        "detailed_content",
        "",
    )

    specialized_points = content.get(
        "specialized_points",
        [],
    )

    exam_points = content.get(
        "exam_points",
        [],
    )

    practical_example = content.get(
        "practical_example",
        "",
    )

    review = content.get(
        "review",
        "",
    )

    sections = []

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

    sections.append(
        "💰 <b>مدیریت مالی</b>\n"
        f"📖 <b>{title}</b>"
    )

    # -----------------------------------------------------
    # Lesson text
    # -----------------------------------------------------

    if lesson_text:
        sections.append(
            "📝 <b>درسنامه</b>\n"
            f"{lesson_text}"
        )

    # -----------------------------------------------------
    # Subtopics
    # -----------------------------------------------------

    if subtopics:
        sections.append(
            _format_points(
                "📌 زیرموضوع‌ها",
                subtopics,
                "▫️",
            )
        )

    # -----------------------------------------------------
    # Detailed content
    # -----------------------------------------------------

    if detailed_content:
        sections.append(
            "🎓 <b>آموزش مفصل</b>\n"
            f"{detailed_content}"
        )

    # -----------------------------------------------------
    # Specialized points
    # -----------------------------------------------------

    if specialized_points:
        sections.append(
            _format_points(
                "🔎 نکات تخصصی",
                specialized_points,
                "🔹",
            )
        )

    # -----------------------------------------------------
    # Exam points
    # -----------------------------------------------------

    if exam_points:
        sections.append(
            _format_points(
                "🎯 نکات آزمونی",
                exam_points,
                "✅",
            )
        )

    # -----------------------------------------------------
    # Practical example
    # -----------------------------------------------------

    if practical_example:
        sections.append(
            "💼 <b>مثال کاربردی</b>\n"
            f"{practical_example}"
        )

    # -----------------------------------------------------
    # Review
    # -----------------------------------------------------

    if review:
        sections.append(
            "🔄 <b>مرور</b>\n"
            f"{review}"
        )

    return "\n\n".join(
        section
        for section in sections
        if section
    )


# =========================================================
# Screens
# =========================================================

async def show_finance_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show Finance main menu."""

    query = update.callback_query

    text = (
        "💰 <b>مدیریت مالی</b>\n\n"
        "به بخش آموزش مدیریت مالی "
        "اندیشکده مدیریت و بازار خوش آمدید.\n\n"
        "در این بخش می‌توانید فصل‌ها و "
        "درس‌های مدیریت مالی را مطالعه کنید."
    )

    if query:
        await query.answer()

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_main_keyboard(),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_main_keyboard(),
        )


async def show_finance_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show all Finance chapters."""

    query = update.callback_query

    text = (
        "📚 <b>فصل‌های مدیریت مالی</b>\n\n"
        "فصل موردنظر خود را انتخاب کنید:"
    )

    if query:
        await query.answer()

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_chapters_keyboard(),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_chapters_keyboard(),
        )


async def show_finance_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
) -> None:
    """Show lessons inside a Finance chapter."""

    query = update.callback_query

    chapter = _find_chapter(chapter_id)

    if chapter is None:
        if query:
            await query.answer(
                "فصل موردنظر پیدا نشد.",
                show_alert=True,
            )
        return

    lessons = _get_chapter_lessons(
        chapter_id
    )

    title = chapter.get(
        "title",
        "فصل مدیریت مالی",
    )

    description = chapter.get(
        "description",
        "",
    )

    text_parts = [
        f"📘 <b>{title}</b>"
    ]

    if description:
        text_parts.append(
            description
        )

    text_parts.append(
        f"\n📖 تعداد درس‌ها: <b>{len(lessons)}</b>\n\n"
        "درس موردنظر را انتخاب کنید:"
    )

    text = "\n".join(text_parts)

    if query:
        await query.answer()

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_chapter_keyboard(
                chapter_id
            ),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_chapter_keyboard(
                chapter_id
            ),
        )


async def show_finance_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    lesson_id: str,
) -> None:
    """
    Show the complete educational content of a Finance lesson.
    """

    query = update.callback_query

    lesson = _find_lesson(lesson_id)

    if lesson is None:
        if query:
            await query.answer(
                "درس موردنظر پیدا نشد.",
                show_alert=True,
            )
        return

    content = get_lesson_content(
        lesson_id
    )

    if content is None:
        if query:
            await query.answer(
                "محتوای آموزشی این درس پیدا نشد.",
                show_alert=True,
            )
        return

    chapter_id = lesson.get(
        "chapter_id"
    )

    text = _format_lesson_content(
        content
    )

    if query:
        await query.answer()

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_lesson_keyboard(
                chapter_id
            ),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_lesson_keyboard(
                chapter_id
            ),
        )


# =========================================================
# Router
# =========================================================

async def route_finance_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route Finance callbacks."""

    query = update.callback_query

    if not query:
        return

    callback_data = query.data or ""

    # -----------------------------------------------------
    # Finance menu
    # -----------------------------------------------------

    if callback_data in {
        FINANCE_MENU_CALLBACK,
        FINANCE_BACK_CALLBACK,
        "menu_finance",
    }:
        await show_finance_chapters(
            update,
            context,
        )
        return

    # -----------------------------------------------------
    # Chapter
    # -----------------------------------------------------

    if callback_data.startswith(
        FINANCE_CHAPTER_PREFIX
    ):
        chapter_id = callback_data[
            len(FINANCE_CHAPTER_PREFIX):
        ]

        await show_finance_chapter(
            update,
            context,
            chapter_id,
        )
        return

    # -----------------------------------------------------
    # Lesson
    # -----------------------------------------------------

    if callback_data.startswith(
        FINANCE_LESSON_PREFIX
    ):
        lesson_id = callback_data[
            len(FINANCE_LESSON_PREFIX):
        ]

        await show_finance_lesson(
            update,
            context,
            lesson_id,
        )
        return

    # -----------------------------------------------------
    # Unknown callback
    # -----------------------------------------------------

    await query.answer(
        "گزینه مدیریت مالی شناسایی نشد.",
        show_alert=True,
    )


# =========================================================
# Health check
# =========================================================

def finance_handlers_health_check() -> bool:
    """
    Lightweight health check.

    This check intentionally verifies only the handler
    integration itself. Content validation is handled by
    the content module and should not prevent startup here.
    """

    try:
        required_functions = (
            show_finance_menu,
            show_finance_chapters,
            show_finance_chapter,
            show_finance_lesson,
            route_finance_callback,
            _format_lesson_content,
            get_lesson_content,
        )

        return all(
            callable(function)
            for function in required_functions
        )

    except Exception:
        return False


# =========================================================
# Public API
# =========================================================

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
