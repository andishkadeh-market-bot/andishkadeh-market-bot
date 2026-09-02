"""
Finance handlers for Andishkadeh Management & Market.

Responsibilities:
- Show Finance main menu
- Show Finance chapters
- Show lessons inside a chapter
- Show full educational content of a lesson
- Navigate back between Finance screens
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .content import (
    content_health_check,
    get_lesson_content,
)
from .data import (
    get_chapters,
    get_lessons,
)


# =========================================================
# Callback constants
# =========================================================

FINANCE_MENU_CALLBACK = "finance_menu"
FINANCE_CHAPTER_PREFIX = "finance_chapter:"
FINANCE_LESSON_PREFIX = "finance_lesson:"
FINANCE_BACK_CALLBACK = "finance_back"
MAIN_MENU_CALLBACK = "menu_main"


# =========================================================
# Internal helpers
# =========================================================

def _get_chapters() -> list:
    """Return all Finance chapters."""
    return get_chapters()


def _get_lessons() -> list:
    """Return all Finance lessons."""
    return get_lessons()


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
    """Return lessons belonging to a specific chapter."""
    return [
        lesson
        for lesson in _get_lessons()
        if lesson.get("chapter_id") == chapter_id
    ]


def _finance_main_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for Finance main menu."""
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
        title = chapter.get("title", "فصل بدون عنوان")

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
    """Keyboard containing lessons of a Finance chapter."""
    rows = []

    for lesson in _get_chapter_lessons(chapter_id):
        lesson_id = lesson.get("lesson_id")
        title = lesson.get("title", "درس بدون عنوان")

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
    """
    Format a list of educational points.
    """
    if not points:
        return ""

    lines = [f"<b>{title}</b>"]

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
    Build the complete Telegram message for a Finance lesson.
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
        f"💰 <b>مدیریت مالی</b>\n"
        f"📖 <b>{title}</b>"
    )

    # -----------------------------------------------------
    # Lesson introduction
    # -----------------------------------------------------

    if lesson_text:
        sections.append(
            f"📝 <b>درسنامه</b>\n{lesson_text}"
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
            f"🎓 <b>آموزش مفصل</b>\n"
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
            f"💼 <b>مثال کاربردی</b>\n"
            f"{practical_example}"
        )

    # -----------------------------------------------------
    # Review
    # -----------------------------------------------------

    if review:
        sections.append(
            f"🔄 <b>مرور</b>\n"
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
    """
    Show Finance main menu.
    """

    query = update.callback_query

    if query:
        await query.answer()

        await query.edit_message_text(
            text=(
                "💰 <b>مدیریت مالی</b>\n\n"
                "به بخش آموزش مدیریت مالی "
                "اندیشکده مدیریت و بازار خوش آمدید.\n\n"
                "در این بخش می‌توانید فصل‌ها و "
                "درس‌های مدیریت مالی را مطالعه کنید."
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_main_keyboard(),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=(
                "💰 <b>مدیریت مالی</b>\n\n"
                "به بخش آموزش مدیریت مالی "
                "اندیشکده مدیریت و بازار خوش آمدید.\n\n"
                "در این بخش می‌توانید فصل‌ها و "
                "درس‌های مدیریت مالی را مطالعه کنید."
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_main_keyboard(),
        )


async def show_finance_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show all Finance chapters.
    """

    query = update.callback_query

    if query:
        await query.answer()

        await query.edit_message_text(
            text=(
                "📚 <b>فصل‌های مدیریت مالی</b>\n\n"
                "فصل موردنظر خود را انتخاب کنید:"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_chapters_keyboard(),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=(
                "📚 <b>فصل‌های مدیریت مالی</b>\n\n"
                "فصل موردنظر خود را انتخاب کنید:"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_chapters_keyboard(),
        )


async def show_finance_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
) -> None:
    """
    Show lessons belonging to a Finance chapter.
    """

    query = update.callback_query

    chapter = _find_chapter(chapter_id)

    if chapter is None:
        if query:
            await query.answer(
                "فصل موردنظر پیدا نشد.",
                show_alert=True,
            )
        return

    lessons = _get_chapter_lessons(chapter_id)

    title = chapter.get(
        "title",
        "فصل مدیریت مالی",
    )

    description = chapter.get(
        "description",
        "",
    )

    text_parts = [
        f"📘 <b>{title}</b>",
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
    Show complete educational content of a Finance lesson.
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

    content = get_lesson_content(lesson_id)

    if content is None:
        if query:
            await query.answer(
                "محتوای آموزشی این درس هنوز ثبت نشده است.",
                show_alert=True,
            )
        return

    chapter_id = lesson.get("chapter_id")

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
    """
    Route all Finance callbacks.
    """

    query = update.callback_query

    if not query:
        return

    callback_data = query.data or ""

    # -----------------------------------------------------
    # Finance main menu
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
    # Finance chapter
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
    # Finance lesson
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
    # Unknown Finance callback
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
    Validate Finance handlers and educational content integration.
    """

    try:
        if not callable(
            show_finance_menu
        ):
            return False

        if not callable(
            show_finance_chapters
        ):
            return False

        if not callable(
            show_finance_chapter
        ):
            return False

        if not callable(
            show_finance_lesson
        ):
            return False

        if not callable(
            route_finance_callback
        ):
            return False

        if not callable(
            get_lesson_content
        ):
            return False

        if not content_health_check():
            return False

        chapters = _get_chapters()
        lessons = _get_lessons()

        if not isinstance(
            chapters,
            list,
        ):
            return False

        if not isinstance(
            lessons,
            list,
        ):
            return False

        if len(chapters) != 12:
            return False

        if len(lessons) != 48:
            return False

        for lesson in lessons:
            lesson_id = lesson.get(
                "lesson_id"
            )

            if not lesson_id:
                return False

            content = get_lesson_content(
                lesson_id
            )

            if content is None:
                return False

        return True

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
