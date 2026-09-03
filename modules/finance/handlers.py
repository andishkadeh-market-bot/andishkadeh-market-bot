"""
Finance Handlers
Andishkadeh Management & Market

Responsibilities:
- Show Finance chapters directly
- Show lessons inside a chapter
- Show complete educational content
- Show lesson quizzes
- Navigate between Finance screens
- Use Finance Service Layer as the single data access point
"""

from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .service import (
    get_finance_chapters,
    get_finance_chapter,
    get_finance_lessons,
    get_finance_lesson,
    get_complete_lesson,
    get_finance_quiz,
    finance_health_check,
)


# =========================================================
# Callback constants
# =========================================================

FINANCE_MENU_CALLBACK = "finance_menu"
FINANCE_CHAPTER_PREFIX = "finance_chapter:"
FINANCE_LESSON_PREFIX = "finance_lesson:"
FINANCE_BACK_CALLBACK = "finance_back"
MAIN_MENU_CALLBACK = "menu_main"

# Quiz callback is intentionally embedded under
# finance_lesson:* so it remains compatible with the
# existing bot.py Finance callback pattern.
FINANCE_LESSON_QUIZ_SUFFIX = ":quiz"


# =========================================================
# Data helpers
# =========================================================

def _get_chapters() -> list:
    """Return all Finance chapters through Service Layer."""
    try:
        return get_finance_chapters()
    except Exception:
        return []


def _get_chapter(chapter_id: str):
    """Return a Finance chapter through Service Layer."""
    try:
        return get_finance_chapter(chapter_id)
    except Exception:
        return None


def _get_lessons(chapter_id: str) -> list:
    """Return lessons of a chapter through Service Layer."""
    try:
        return get_finance_lessons(chapter_id)
    except Exception:
        return []


def _get_lesson(chapter_id: str, lesson_id: str):
    """Return a Finance lesson through Service Layer."""
    try:
        return get_finance_lesson(
            chapter_id,
            lesson_id,
        )
    except Exception:
        return None


def _get_quiz(chapter_id: str, lesson_id: str) -> list:
    """Return lesson quiz questions through Service Layer."""
    try:
        quiz = get_finance_quiz(
            chapter_id,
            lesson_id,
        )

        if isinstance(quiz, list):
            return quiz

        return []

    except Exception:
        return []


def _get_id(item: dict) -> str | None:
    """
    Return the identifier of a chapter or lesson.

    Supports:
    - id
    - chapter_id
    - lesson_id
    """
    if not isinstance(item, dict):
        return None

    return (
        item.get("id")
        or item.get("chapter_id")
        or item.get("lesson_id")
    )


def _find_chapter(chapter_id: str):
    """Find a Finance chapter by ID."""
    return _get_chapter(chapter_id)


def _find_lesson(lesson_id: str):
    """
    Find a Finance lesson by ID.

    The Service Layer normally handles chapter-aware access,
    but this compatibility helper searches all chapters.
    """
    for chapter in _get_chapters():
        chapter_id = _get_id(chapter)

        if not chapter_id:
            continue

        lesson = _get_lesson(
            chapter_id,
            lesson_id,
        )

        if lesson is not None:
            return lesson

    return None


def _get_chapter_lessons(chapter_id: str) -> list:
    """Return lessons belonging to a specific chapter."""
    return _get_lessons(chapter_id)


# =========================================================
# Quiz helpers
# =========================================================

def _get_quiz_value(question: dict, key: str, default=None):
    """Safely read a quiz field."""
    if not isinstance(question, dict):
        return default

    return question.get(key, default)


def _get_quiz_question_text(question: dict) -> str:
    """
    Extract quiz question text.

    Supports common keys:
    - question
    - text
    - title
    """
    return (
        _get_quiz_value(question, "question")
        or _get_quiz_value(question, "text")
        or _get_quiz_value(question, "title")
        or "سؤال بدون متن"
    )


def _get_quiz_options(question: dict) -> list:
    """
    Extract quiz options.

    Supports:
    - options
    """
    options = _get_quiz_value(
        question,
        "options",
        [],
    )

    if isinstance(options, list):
        return options

    return []


def _get_quiz_correct_index(question: dict):
    """
    Extract correct answer index.

    Supports:
    - correct_index
    - answer
    - correct_answer
    """
    if not isinstance(question, dict):
        return None

    if "correct_index" in question:
        return question.get("correct_index")

    if "answer" in question:
        return question.get("answer")

    if "correct_answer" in question:
        return question.get("correct_answer")

    return None


# =========================================================
# Keyboard helpers
# =========================================================

def _finance_chapters_keyboard() -> InlineKeyboardMarkup:
    """Keyboard containing Finance chapters."""
    rows = []

    for chapter in _get_chapters():
        chapter_id = _get_id(chapter)

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
        lesson_id = _get_id(lesson)

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
    lesson_id: str | None = None,
) -> InlineKeyboardMarkup:
    """
    Keyboard for a Finance lesson.

    Includes:
    - Lesson quiz
    - Back to chapter lessons
    - Finance chapters
    - Main menu
    """
    rows = []

    # -----------------------------------------------------
    # Lesson quiz button
    # -----------------------------------------------------

    if lesson_id:
        rows.append(
            [
                InlineKeyboardButton(
                    "📝 آزمون این درس",
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}"
                        f"{lesson_id}"
                        f"{FINANCE_LESSON_QUIZ_SUFFIX}"
                    ),
                )
            ]
        )

    # -----------------------------------------------------
    # Back to chapter lessons
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Finance chapters
    # -----------------------------------------------------

    rows.append(
        [
            InlineKeyboardButton(
                "📚 فصل‌های مدیریت مالی",
                callback_data=FINANCE_MENU_CALLBACK,
            )
        ]
    )

    # -----------------------------------------------------
    # Main menu
    # -----------------------------------------------------

    rows.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(rows)


def _finance_quiz_keyboard(
    chapter_id: str,
    lesson_id: str,
) -> InlineKeyboardMarkup:
    """Keyboard for Finance lesson quiz."""
    rows = [
        [
            InlineKeyboardButton(
                "⬅️ بازگشت به درس",
                callback_data=(
                    f"{FINANCE_LESSON_PREFIX}{lesson_id}"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ بازگشت به درس‌های فصل",
                callback_data=(
                    f"{FINANCE_CHAPTER_PREFIX}{chapter_id}"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ],
    ]

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

    Expected structure:
    - title
    - lesson_text
    - subtopics
    - detailed_content
    - specialized_points
    - exam_points
    - practical_example
    - review
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
# Quiz formatting
# =========================================================

def _format_quiz(
    chapter_id: str,
    lesson_id: str,
    lesson: dict,
    quiz: list,
) -> str:
    """Format Finance lesson quiz for Telegram."""

    lesson_title = lesson.get(
        "title",
        "درس مدیریت مالی",
    )

    if not quiz:
        return (
            "📝 <b>آزمون درس</b>\n\n"
            f"📖 <b>{lesson_title}</b>\n\n"
            "⚠️ برای این درس هنوز سؤال آزمون ثبت نشده است."
        )

    lines = [
        "📝 <b>آزمون درس مدیریت مالی</b>",
        f"📖 <b>{lesson_title}</b>",
        "",
        f"تعداد سؤالات: <b>{len(quiz)}</b>",
        "",
    ]

    for index, question in enumerate(
        quiz,
        start=1,
    ):
        question_text = _get_quiz_question_text(
            question
        )

        lines.append(
            f"<b>سؤال {index}</b>\n"
            f"{question_text}"
        )

        options = _get_quiz_options(
            question
        )

        if options:
            for option_index, option in enumerate(
                options,
                start=1,
            ):
                if isinstance(option, dict):
                    option_text = (
                        option.get("text")
                        or option.get("title")
                        or option.get("label")
                        or str(option)
                    )
                else:
                    option_text = str(option)

                lines.append(
                    f"{option_index}. {option_text}"
                )

        lines.append("")

    return "\n".join(lines)


# =========================================================
# Screens
# =========================================================

async def show_finance_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show Finance chapters directly.

    The previous welcome screen has intentionally
    been removed.
    """

    query = update.callback_query

    chapters = _get_chapters()

    text = (
        "📚 <b>فصل‌های مدیریت مالی</b>\n\n"
        f"تعداد فصل‌ها: <b>{len(chapters)}</b>\n\n"
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


async def show_finance_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show all Finance chapters."""

    query = update.callback_query

    chapters = _get_chapters()

    text = (
        "📚 <b>فصل‌های مدیریت مالی</b>\n\n"
        f"تعداد فصل‌ها: <b>{len(chapters)}</b>\n\n"
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

    chapter = _find_chapter(
        chapter_id
    )

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

    text = "\n".join(
        text_parts
    )

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
    """Show complete educational content of a Finance lesson."""

    query = update.callback_query

    lesson = _find_lesson(
        lesson_id
    )

    if lesson is None:
        if query:
            await query.answer(
                "درس موردنظر پیدا نشد.",
                show_alert=True,
            )

        return

    chapter_id = lesson.get(
        "chapter_id"
    )

    if not chapter_id:
        if query:
            await query.answer(
                "فصل مربوط به این درس پیدا نشد.",
                show_alert=True,
            )

        return

    content = get_complete_lesson(
        chapter_id,
        lesson_id,
    )

    if not content:
        if query:
            await query.answer(
                "محتوای آموزشی این درس پیدا نشد.",
                show_alert=True,
            )

        return

    text = _format_lesson_content(
        content
    )

    if query:
        await query.answer()

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_lesson_keyboard(
                chapter_id=chapter_id,
                lesson_id=lesson_id,
            ),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_lesson_keyboard(
                chapter_id=chapter_id,
                lesson_id=lesson_id,
            ),
        )


async def show_finance_lesson_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    lesson_id: str,
) -> None:
    """Show the quiz questions of a Finance lesson."""

    query = update.callback_query

    lesson = _find_lesson(
        lesson_id
    )

    if lesson is None:
        if query:
            await query.answer(
                "درس موردنظر پیدا نشد.",
                show_alert=True,
            )

        return

    chapter_id = lesson.get(
        "chapter_id"
    )

    if not chapter_id:
        if query:
            await query.answer(
                "فصل مربوط به این درس پیدا نشد.",
                show_alert=True,
            )

        return

    quiz = _get_quiz(
        chapter_id,
        lesson_id,
    )

    text = _format_quiz(
        chapter_id,
        lesson_id,
        lesson,
        quiz,
    )

    if query:
        await query.answer()

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_quiz_keyboard(
                chapter_id,
                lesson_id,
            ),
        )

        return

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=_finance_quiz_keyboard(
                chapter_id,
                lesson_id,
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
    # Finance main menu
    # -----------------------------------------------------

    if callback_data == "menu_finance":
        await show_finance_menu(
            update,
            context,
        )

        return

    # -----------------------------------------------------
    # Finance chapter list
    # -----------------------------------------------------

    if callback_data in {
        FINANCE_MENU_CALLBACK,
        FINANCE_BACK_CALLBACK,
    }:
        await show_finance_chapters(
            update,
            context,
        )

        return

    # -----------------------------------------------------
    # Lesson / Lesson Quiz
    # -----------------------------------------------------

    if callback_data.startswith(
        FINANCE_LESSON_PREFIX
    ):
        lesson_id = callback_data[
            len(FINANCE_LESSON_PREFIX):
        ]

        # -------------------------------------------------
        # Quiz callback
        # Format:
        # finance_lesson:<lesson_id>:quiz
        # -------------------------------------------------

        if lesson_id.endswith(
            FINANCE_LESSON_QUIZ_SUFFIX
        ):
            real_lesson_id = lesson_id[
                : -len(FINANCE_LESSON_QUIZ_SUFFIX)
            ]

            await show_finance_lesson_quiz(
                update,
                context,
                real_lesson_id,
            )

            return

        # -------------------------------------------------
        # Normal lesson callback
        # -------------------------------------------------

        await show_finance_lesson(
            update,
            context,
            lesson_id,
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
    # Unknown callback
    # -----------------------------------------------------

    await query.answer(
        "گزینه مدیریت مالی شناسایی نشد.",
        show_alert=True,
    )


# =========================================================
# Health Check
# =========================================================

def finance_handlers_health_check() -> bool:
    """
    Lightweight health check for Finance handlers.

    The actual module validation is delegated to
    Finance Service Layer.
    """

    try:
        required_functions = (
            show_finance_menu,
            show_finance_chapters,
            show_finance_chapter,
            show_finance_lesson,
            show_finance_lesson_quiz,
            route_finance_callback,
            _format_lesson_content,
            _format_quiz,
            _finance_lesson_keyboard,
            _finance_quiz_keyboard,
            get_finance_chapters,
            get_finance_chapter,
            get_finance_lessons,
            get_finance_lesson,
            get_complete_lesson,
            get_finance_quiz,
            finance_health_check,
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
    "FINANCE_LESSON_QUIZ_SUFFIX",
    "show_finance_menu",
    "show_finance_chapters",
    "show_finance_chapter",
    "show_finance_lesson",
    "show_finance_lesson_quiz",
    "route_finance_callback",
    "finance_handlers_health_check",
]
