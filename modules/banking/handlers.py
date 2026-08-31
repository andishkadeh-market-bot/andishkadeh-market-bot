"""
Banking Module Handlers
=======================

Andishkadeh Management & Market

Specialized Banking Module

Features:
- Banking main menu
- Chapters
- Lessons
- Lesson details
- Lesson completion
- Specialized quizzes
- Quiz answers
- Quiz cancellation
- Navigation
- Health check

Callback conventions:

    menu_banking

    banking_chapters
    banking_chapter:<chapter_id>

    banking_lesson:<chapter_id>:<lesson_id>
    banking_complete:<chapter_id>:<lesson_id>

    banking_quiz:<chapter_id>:<lesson_id>
    banking_quiz_answer:<chapter_id>:<lesson_id>:<question_index>

    banking_quiz_cancel

The handler layer intentionally keeps business/data logic
inside service.py and data.py.
"""

from __future__ import annotations

import logging
from html import escape
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from modules.banking import data
from modules.banking import service


logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = getattr(
    data,
    "MODULE_ID",
    "banking",
)

MODULE_TITLE = getattr(
    data,
    "MODULE_TITLE",
    "🏦 بانکداری تخصصی",
)

MODULE_DESCRIPTION = getattr(
    data,
    "MODULE_DESCRIPTION",
    "آموزش تخصصی و کاربردی بانکداری",
)


# ==========================================================
# Utility Functions
# ==========================================================

def _get_query(update: Update):
    """Return callback query when available."""

    return update.callback_query


async def _safe_answer(
    update: Update,
    text: str | None = None,
    show_alert: bool = False,
) -> None:
    """Safely answer callback query."""

    query = _get_query(update)

    if query is None:
        return

    try:
        await query.answer(
            text=text,
            show_alert=show_alert,
        )
    except Exception:
        logger.exception(
            "Failed to answer banking callback."
        )


async def _safe_edit(
    update: Update,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> bool:
    """Safely edit callback message."""

    query = _get_query(update)

    if query is None:
        return False

    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
        return True

    except Exception:
        logger.exception(
            "Failed to edit banking message."
        )
        return False


async def _safe_send(
    update: Update,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> bool:
    """Send a new banking message."""

    if update.message is None:
        return False

    try:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
        return True

    except Exception:
        logger.exception(
            "Failed to send banking message."
        )
        return False


def _normalize_id(value: Any) -> str:
    """Normalize identifiers."""

    return str(value)


def _chapter_id(chapter: Any) -> str | None:
    """Extract chapter identifier."""

    if not isinstance(chapter, dict):
        return None

    value = (
        chapter.get("id")
        or chapter.get("chapter_id")
    )

    if value is None:
        return None

    return _normalize_id(value)


def _chapter_title(chapter: Any) -> str:
    """Extract chapter title."""

    if not isinstance(chapter, dict):
        return "فصل بانکداری"

    return str(
        chapter.get("title")
        or chapter.get("name")
        or chapter.get("chapter_title")
        or chapter.get("id")
        or "فصل بانکداری"
    )


def _lesson_id(lesson: Any) -> str | None:
    """Extract lesson identifier."""

    if not isinstance(lesson, dict):
        return None

    value = (
        lesson.get("id")
        or lesson.get("lesson_id")
    )

    if value is None:
        return None

    return _normalize_id(value)


def _lesson_title(lesson: Any) -> str:
    """Extract lesson title."""

    if not isinstance(lesson, dict):
        return "درس بانکداری"

    return str(
        lesson.get("title")
        or lesson.get("name")
        or lesson.get("lesson_title")
        or lesson.get("id")
        or "درس بانکداری"
    )


def _get_value(
    item: Any,
    *keys: str,
    default: Any = None,
) -> Any:
    """Read first available key from dictionary."""

    if not isinstance(item, dict):
        return default

    for key in keys:
        if key in item and item[key] is not None:
            return item[key]

    return default


# ==========================================================
# Keyboard Builders
# ==========================================================

def banking_main_keyboard() -> InlineKeyboardMarkup:
    """Build Banking main menu."""

    keyboard = [
        [
            InlineKeyboardButton(
                "📚 فصل‌های بانکداری",
                callback_data="banking_chapters",
            ),
        ],
        [
            InlineKeyboardButton(
                "🎯 آزمون بانکداری",
                callback_data="banking_quiz:general:general",
            ),
        ],
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def banking_chapters_keyboard(
    chapters: list[Any],
) -> InlineKeyboardMarkup:
    """Build chapter selection keyboard."""

    keyboard: list[list[InlineKeyboardButton]] = []

    for chapter in chapters:

        chapter_id = _chapter_id(chapter)

        if not chapter_id:
            continue

        title = _chapter_title(chapter)

        keyboard.append(
            [
                InlineKeyboardButton(
                    title,
                    callback_data=(
                        f"banking_chapter:{chapter_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="menu_banking",
            ),
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            ),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def banking_lessons_keyboard(
    chapter_id: str,
    lessons: list[Any],
) -> InlineKeyboardMarkup:
    """Build lesson selection keyboard."""

    keyboard: list[list[InlineKeyboardButton]] = []

    for lesson in lessons:

        lesson_id = _lesson_id(lesson)

        if not lesson_id:
            continue

        title = _lesson_title(lesson)

        keyboard.append(
            [
                InlineKeyboardButton(
                    title,
                    callback_data=(
                        f"banking_lesson:"
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
                    f"banking_quiz:"
                    f"{chapter_id}:chapter"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 فصل‌ها",
                callback_data="banking_chapters",
            ),
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            ),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def banking_lesson_keyboard(
    chapter_id: str,
    lesson_id: str,
    has_quiz: bool = True,
) -> InlineKeyboardMarkup:
    """Build lesson navigation keyboard."""

    keyboard: list[list[InlineKeyboardButton]] = []

    keyboard.append(
        [
            InlineKeyboardButton(
                "✅ تکمیل درس",
                callback_data=(
                    f"banking_complete:"
                    f"{chapter_id}:"
                    f"{lesson_id}"
                ),
            )
        ]
    )

    if has_quiz:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📝 آزمون این درس",
                    callback_data=(
                        f"banking_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به فصل",
                callback_data=(
                    f"banking_chapter:{chapter_id}"
                ),
            ),
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            ),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def banking_quiz_keyboard(
    chapter_id: str,
    lesson_id: str,
    question_index: int,
    options: list[Any],
) -> InlineKeyboardMarkup:
    """Build quiz answer keyboard."""

    keyboard: list[list[InlineKeyboardButton]] = []

    for index, option in enumerate(options):

        if isinstance(option, dict):
            label = str(
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or option.get("title")
                or f"گزینه {index + 1}"
            )
        else:
            label = str(option)

        keyboard.append(
            [
                InlineKeyboardButton(
                    label,
                    callback_data=(
                        f"banking_quiz_answer:"
                        f"{chapter_id}:"
                        f"{lesson_id}:"
                        f"{question_index}:"
                        f"{index}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ پایان آزمون",
                callback_data="banking_quiz_cancel",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def banking_quiz_result_keyboard(
    chapter_id: str,
    lesson_id: str,
) -> InlineKeyboardMarkup:
    """Build quiz result keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔁 آزمون مجدد",
                    callback_data=(
                        f"banking_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 بازگشت به فصل‌ها",
                    callback_data="banking_chapters",
                ),
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="menu_main",
                ),
            ],
        ]
    )


# ==========================================================
# Data Access Helpers
# ==========================================================

def _load_chapters() -> list[Any]:
    """
    Load banking chapters.

    service.py is preferred when available.
    data.py is used as fallback.
    """

    try:

        getter = getattr(
            service,
            "get_chapters",
            None,
        )

        if callable(getter):

            result = getter()

            if isinstance(result, list):
                return result

    except Exception:
        logger.exception(
            "Service get_chapters failed."
        )

    try:

        getter = getattr(
            data,
            "get_chapters",
            None,
        )

        if callable(getter):

            result = getter()

            if isinstance(result, list):
                return result

    except Exception:
        logger.exception(
            "Data get_chapters failed."
        )

    return []


def _load_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Load one chapter."""

    try:

        getter = getattr(
            service,
            "get_chapter",
            None,
        )

        if callable(getter):

            result = getter(chapter_id)

            if isinstance(result, dict):
                return result

    except Exception:
        logger.exception(
            "Service get_chapter failed."
        )

    chapters = _load_chapters()

    for chapter in chapters:

        if _chapter_id(chapter) == chapter_id:

            if isinstance(chapter, dict):
                return chapter

    return None


def _load_lessons(
    chapter_id: str,
) -> list[Any]:
    """Load lessons for chapter."""

    try:

        getter = getattr(
            service,
            "get_lessons",
            None,
        )

        if callable(getter):

            result = getter(chapter_id)

            if isinstance(result, list):
                return result

    except Exception:
        logger.exception(
            "Service get_lessons failed."
        )

    try:

        getter = getattr(
            data,
            "get_lessons",
            None,
        )

        if callable(getter):

            result = getter(chapter_id)

            if isinstance(result, list):
                return result

    except Exception:
        logger.exception(
            "Data get_lessons failed."
        )

    chapter = _load_chapter(chapter_id)

    if isinstance(chapter, dict):

        lessons = (
            chapter.get("lessons")
            or []
        )

        if isinstance(lessons, list):
            return lessons

    return []


def _load_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Load a specific lesson."""

    try:

        getter = getattr(
            service,
            "get_lesson",
            None,
        )

        if callable(getter):

            result = getter(
                chapter_id,
                lesson_id,
            )

            if isinstance(result, dict):
                return result

    except Exception:
        logger.exception(
            "Service get_lesson failed."
        )

    lessons = _load_lessons(
        chapter_id
    )

    for lesson in lessons:

        if _lesson_id(lesson) == lesson_id:

            if isinstance(lesson, dict):
                return lesson

    return None


# ==========================================================
# Lesson Text Builder
# ==========================================================

def _build_lesson_text(
    chapter: dict[str, Any] | None,
    lesson: dict[str, Any],
) -> str:
    """
    Build detailed lesson message.

    Supports multiple data.py schemas so the handler
    remains compatible while the banking module evolves.
    """

    chapter_title = _chapter_title(
        chapter
        or {}
    )

    lesson_title = _lesson_title(
        lesson
    )

    description = _get_value(
        lesson,
        "description",
        "summary",
        "intro",
        "introduction",
        default="",
    )

    content = _get_value(
        lesson,
        "content",
        "text",
        "lesson",
        "body",
        "details",
        default="",
    )

    objectives = _get_value(
        lesson,
        "objectives",
        "learning_objectives",
        "goals",
        default=[],
    )

    key_points = _get_value(
        lesson,
        "key_points",
        "important_points",
        "highlights",
        default=[],
    )

    exam_points = _get_value(
        lesson,
        "exam_points",
        "exam_tips",
        "test_points",
        default=[],
    )

    examples = _get_value(
        lesson,
        "examples",
        "practical_examples",
        default=[],
    )

    sources = _get_value(
        lesson,
        "sources",
        "references",
        "resources",
        default=[],
    )

    sections = _get_value(
        lesson,
        "sections",
        "topics",
        "subtopics",
        default=[],
    )

    parts: list[str] = []

    parts.append(
        "🏦 <b>بانکداری تخصصی</b>"
    )

    parts.append(
        f"📚 <b>{escape(chapter_title)}</b>"
    )

    parts.append(
        f"📖 <b>{escape(lesson_title)}</b>"
    )

    if description:
        parts.append(
            "\n"
            f"📝 <b>معرفی درس</b>\n"
            f"{escape(str(description))}"
        )

    if objectives:

        parts.append(
            "\n🎯 <b>اهداف یادگیری</b>"
        )

        if isinstance(
            objectives,
            (list, tuple),
        ):

            for objective in objectives:

                parts.append(
                    f"• {escape(str(objective))}"
                )

        else:

            parts.append(
                escape(str(objectives))
            )

    if sections:

        parts.append(
            "\n🧩 <b>سرفصل‌های درس</b>"
        )

        if isinstance(
            sections,
            (list, tuple),
        ):

            for section in sections:

                if isinstance(
                    section,
                    dict,
                ):

                    title = (
                        section.get("title")
                        or section.get("name")
                        or ""
                    )

                    parts.append(
                        f"• {escape(str(title))}"
                    )

                else:

                    parts.append(
                        f"• {escape(str(section))}"
                    )

        else:

            parts.append(
                escape(str(sections))
            )

    if content:

        parts.append(
            "\n📚 <b>درسنامه تخصصی</b>\n"
            f"{escape(str(content))}"
        )

    if key_points:

        parts.append(
            "\n🔑 <b>نکات کلیدی</b>"
        )

        if isinstance(
            key_points,
            (list, tuple),
        ):

            for point in key_points:

                parts.append(
                    f"• {escape(str(point))}"
                )

        else:

            parts.append(
                escape(str(key_points))
            )

    if exam_points:

        parts.append(
            "\n🎯 <b>نکات آزمونی</b>"
        )

        if isinstance(
            exam_points,
            (list, tuple),
        ):

            for point in exam_points:

                parts.append(
                    f"• {escape(str(point))}"
                )

        else:

            parts.append(
                escape(str(exam_points))
            )

    if examples:

        parts.append(
            "\n💼 <b>مثال کاربردی</b>"
        )

        if isinstance(
            examples,
            (list, tuple),
        ):

            for example in examples:

                if isinstance(
                    example,
                    dict,
                ):

                    title = (
                        example.get("title")
                        or example.get("name")
                        or "مثال"
                    )

                    text = (
                        example.get("text")
                        or example.get("description")
                        or example.get("content")
                        or ""
                    )

                    parts.append(
                        f"<b>{escape(str(title))}</b>"
                    )

                    if text:
                        parts.append(
                            escape(str(text))
                        )

                else:

                    parts.append(
                        f"• {escape(str(example))}"
                    )

        else:

            parts.append(
                escape(str(examples))
            )

    if sources:

        parts.append(
            "\n📚 <b>منابع و مراجع</b>"
        )

        if isinstance(
            sources,
            (list, tuple),
        ):

            for source in sources:
                parts.append(
                    f"• {escape(str(source))}"
                )

        else:

            parts.append(
                escape(str(sources))
            )

    return "\n".join(parts)


# ==========================================================
# Main Banking Menu
# ==========================================================

async def show_banking_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show Banking main menu."""

    await _safe_answer(update)

    text = (
        f"🏦 <b>{escape(MODULE_TITLE)}</b>\n\n"
        f"{escape(MODULE_DESCRIPTION)}\n\n"
        "در این بخش آموزش بانکداری به صورت "
        "فصل‌بندی‌شده ارائه می‌شود.\n\n"
        "📚 درسنامه تخصصی\n"
        "🔑 نکات کلیدی\n"
        "🎯 نکات آزمونی\n"
        "💼 مثال‌های کاربردی\n"
        "📝 آزمون‌های تخصصی\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
    )

    if update.callback_query:

        await _safe_edit(
            update,
            text,
            banking_main_keyboard(),
        )
        return

    await _safe_send(
        update,
        text,
        banking_main_keyboard(),
    )


# ==========================================================
# Chapters
# ==========================================================

async def show_banking_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show all Banking chapters."""

    await _safe_answer(update)

    chapters = _load_chapters()

    if not chapters:

        text = (
            "🏦 <b>فصل‌های بانکداری</b>\n\n"
            "⚠️ در حال حاضر هیچ فصلی برای "
            "نمایش ثبت نشده است."
        )

        await _safe_edit(
            update,
            text,
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="menu_banking",
                        )
                    ]
                ]
            ),
        )

        return

    text = (
        "🏦 <b>فصل‌های بانکداری تخصصی</b>\n\n"
        "برای شروع، فصل موردنظر را انتخاب کنید:"
    )

    await _safe_edit(
        update,
        text,
        banking_chapters_keyboard(
            chapters
        ),
    )


# ==========================================================
# Chapter
# ==========================================================

async def show_banking_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show lessons of one Banking chapter."""

    await _safe_answer(update)

    query = _get_query(update)

    if query is None:
        return

    data_value = query.data or ""

    prefix = "banking_chapter:"

    if not data_value.startswith(prefix):
        return

    chapter_id = data_value[
        len(prefix):
    ]

    chapter = _load_chapter(
        chapter_id
    )

    lessons = _load_lessons(
        chapter_id
    )

    chapter_title = _chapter_title(
        chapter
        or {
            "id": chapter_id
        }
    )

    text = (
        "🏦 <b>بانکداری تخصصی</b>\n\n"
        f"📚 <b>{escape(chapter_title)}</b>\n\n"
        "درس‌های این فصل:"
    )

    if not lessons:

        text += (
            "\n\n"
            "⚠️ هنوز درسی برای این فصل ثبت نشده است."
        )

    await _safe_edit(
        update,
        text,
        banking_lessons_keyboard(
            chapter_id,
            lessons,
        ),
    )


# ==========================================================
# Lesson
# ==========================================================

async def show_banking_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show detailed Banking lesson."""

    await _safe_answer(update)

    query = _get_query(update)

    if query is None:
        return

    data_value = query.data or ""

    prefix = "banking_lesson:"

    if not data_value.startswith(prefix):
        return

    payload = data_value[
        len(prefix):
    ]

    parts = payload.split(
        ":",
        1,
    )

    if len(parts) != 2:
        await _safe_answer(
            update,
            "اطلاعات درس نامعتبر است.",
            show_alert=True,
        )
        return

    chapter_id, lesson_id = parts

    lesson = _load_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:

        await _safe_answer(
            update,
            "درس موردنظر پیدا نشد.",
            show_alert=True,
        )

        return

    chapter = _load_chapter(
        chapter_id
    )

    text = _build_lesson_text(
        chapter,
        lesson,
    )

    questions = _get_value(
        lesson,
        "questions",
        "quiz",
        "quiz_questions",
        default=[],
    )

    has_quiz = bool(
        questions
    )

    await _safe_edit(
        update,
        text,
        banking_lesson_keyboard(
            chapter_id,
            lesson_id,
            has_quiz=has_quiz,
        ),
    )


# ==========================================================
# Complete Lesson
# ==========================================================

async def complete_banking_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Mark a Banking lesson as completed."""

    await _safe_answer(update)

    query = _get_query(update)

    if query is None:
        return

    data_value = query.data or ""

    prefix = "banking_complete:"

    if not data_value.startswith(prefix):
        return

    payload = data_value[
        len(prefix):
    ]

    parts = payload.split(
        ":",
        1,
    )

    if len(parts) != 2:
        return

    chapter_id, lesson_id = parts

    user = update.effective_user

    if user is None:
        return

    completed = False

    try:

        getter = getattr(
            service,
            "complete_lesson",
            None,
        )

        if callable(getter):

            result = getter(
                user.id,
                chapter_id,
                lesson_id,
            )

            completed = bool(
                result
            )

    except TypeError:

        logger.exception(
            "Banking complete_lesson signature mismatch."
        )

    except Exception:

        logger.exception(
            "Banking lesson completion failed."
        )

    except BaseException:

        logger.exception(
            "Unexpected Banking completion error."
        )

    if completed:

        message = (
            "✅ <b>درس با موفقیت تکمیل شد.</b>\n\n"
            "پیشرفت شما در این بخش ثبت شد."
        )

    else:

        message = (
            "✅ <b>درس مطالعه شد.</b>\n\n"
            "برای ثبت پیشرفت کامل، می‌توانید "
            "آزمون همین درس را نیز انجام دهید."
        )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 آزمون درس",
                    callback_data=(
                        f"banking_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به درس",
                    callback_data=(
                        f"banking_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
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

    await _safe_edit(
        update,
        message,
        keyboard,
    )


# ==========================================================
# Quiz Data Helpers
# ==========================================================

def _load_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[Any]:
    """Load quiz questions."""

    try:

        getter = getattr(
            service,
            "get_quiz_questions",
            None,
        )

        if callable(getter):

            result = getter(
                chapter_id,
                lesson_id,
            )

            if isinstance(result, list):
                return result

    except Exception:
        logger.exception(
            "Service get_quiz_questions failed."
        )

    lesson = _load_lesson(
        chapter_id,
        lesson_id,
    )

    if isinstance(lesson, dict):

        questions = _get_value(
            lesson,
            "questions",
            "quiz",
            "quiz_questions",
            default=[],
        )

        if isinstance(
            questions,
            list,
        ):
            return questions

    return []


def _question_text(
    question: Any,
) -> str:
    """Extract question text."""

    if not isinstance(question, dict):
        return str(question)

    return str(
        question.get("question")
        or question.get("text")
        or question.get("title")
        or question.get("prompt")
        or "سؤال بانکداری"
    )


def _question_options(
    question: Any,
) -> list[Any]:
    """Extract question options."""

    if not isinstance(question, dict):
        return []

    options = (
        question.get("options")
        or question.get("choices")
        or question.get("answers")
        or []
    )

    if isinstance(
        options,
        list,
    ):
        return options

    return []


def _correct_option_index(
    question: Any,
) -> int | None:
    """Extract correct option index."""

    if not isinstance(question, dict):
        return None

    value = (
        question.get("correct_index")
        if "correct_index" in question
        else question.get("answer_index")
    )

    if value is None:
        value = question.get(
            "correct_answer_index"
        )

    if value is None:
        return None

    try:
        return int(value)
    except (
        TypeError,
        ValueError,
    ):
        return None


def _option_label(
    option: Any,
) -> str:
    """Extract visible option label."""

    if isinstance(
        option,
        dict,
    ):

        return str(
            option.get("text")
            or option.get("label")
            or option.get("answer")
            or option.get("title")
            or ""
        )

    return str(option)


# ==========================================================
# Quiz State
# ==========================================================

QUIZ_STATE_KEY = "banking_quiz"


def _set_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
    lesson_id: str,
    questions: list[Any],
) -> None:
    """Store Banking quiz state."""

    context.user_data[
        QUIZ_STATE_KEY
    ] = {
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "questions": questions,
        "current": 0,
        "score": 0,
        "answered": 0,
    }


def _get_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
    """Get Banking quiz state."""

    state = context.user_data.get(
        QUIZ_STATE_KEY
    )

    if not isinstance(
        state,
        dict,
    ):
        return None

    return state


def _clear_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Clear Banking quiz state."""

    context.user_data.pop(
        QUIZ_STATE_KEY,
        None,
    )


# ==========================================================
# Start Quiz
# ==========================================================

async def start_banking_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Start Banking quiz."""

    await _safe_answer(update)

    query = _get_query(update)

    if query is None:
        return

    data_value = query.data or ""

    prefix = "banking_quiz:"

    if not data_value.startswith(prefix):
        return

    payload = data_value[
        len(prefix):
    ]

    parts = payload.split(
        ":",
        1,
    )

    if len(parts) != 2:
        await _safe_answer(
            update,
            "اطلاعات آزمون نامعتبر است.",
            show_alert=True,
        )
        return

    chapter_id, lesson_id = parts

    questions = _load_quiz_questions(
        chapter_id,
        lesson_id,
    )

    if not questions:

        await _safe_edit(
            update,
            (
                "📝 <b>آزمون بانکداری</b>\n\n"
                "⚠️ برای این بخش هنوز سؤال "
                "آزمون ثبت نشده است."
            ),
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                f"banking_chapter:"
                                f"{chapter_id}"
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🏠 منوی اصلی",
                            callback_data="menu_main",
                        )
                    ],
                ]
            ),
        )

        return

    _set_quiz_state(
        context,
        chapter_id,
        lesson_id,
        questions,
    )

    await _show_current_quiz_question(
        update,
        context,
    )


# ==========================================================
# Show Current Quiz Question
# ==========================================================

async def _show_current_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Display current quiz question."""

    state = _get_quiz_state(
        context
    )

    if state is None:
        return

    questions = state.get(
        "questions",
        [],
    )

    current = int(
        state.get(
            "current",
            0,
        )
    )

    if current >= len(questions):

        await _finish_banking_quiz(
            update,
            context,
        )

        return

    question = questions[current]

    question_text = _question_text(
        question
    )

    options = _question_options(
        question
    )

    chapter_id = str(
        state.get(
            "chapter_id",
            "",
        )
    )

    lesson_id = str(
        state.get(
            "lesson_id",
            "",
        )
    )

    total = len(questions)

    score = int(
        state.get(
            "score",
            0,
        )
    )

    text = (
        "🏦 <b>آزمون بانکداری تخصصی</b>\n\n"
        f"❓ <b>سؤال {current + 1} از {total}</b>\n\n"
        f"{escape(question_text)}\n\n"
        f"📊 امتیاز فعلی: {score}"
    )

    await _safe_edit(
        update,
        text,
        banking_quiz_keyboard(
            chapter_id,
            lesson_id,
            current,
            options,
        ),
    )


# ==========================================================
# Answer Quiz
# ==========================================================

async def answer_banking_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Process Banking quiz answer."""

    await _safe_answer(update)

    query = _get_query(update)

    if query is None:
        return

    data_value = query.data or ""

    prefix = "banking_quiz_answer:"

    if not data_value.startswith(prefix):
        return

    payload = data_value[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 4:

        await _safe_answer(
            update,
            "پاسخ آزمون نامعتبر است.",
            show_alert=True,
        )

        return

    (
        chapter_id,
        lesson_id,
        question_index_text,
        selected_index_text,
    ) = parts

    try:

        question_index = int(
            question_index_text
        )

        selected_index = int(
            selected_index_text
        )

    except (
        TypeError,
        ValueError,
    ):

        await _safe_answer(
            update,
            "اطلاعات پاسخ نامعتبر است.",
            show_alert=True,
        )

        return

    state = _get_quiz_state(
        context
    )

    if state is None:

        await _safe_answer(
            update,
            "آزمون فعال نیست.",
            show_alert=True,
        )

        return

    current = int(
        state.get(
            "current",
            0,
        )
    )

    if current != question_index:

        await _safe_answer(
            update,
            "این سؤال دیگر فعال نیست.",
            show_alert=False,
        )

        return

    questions = state.get(
        "questions",
        [],
    )

    if not isinstance(
        questions,
        list,
    ):

        _clear_quiz_state(
            context
        )

        return

    if question_index >= len(questions):

        await _finish_banking_quiz(
            update,
            context,
        )

        return

    question = questions[
        question_index
    ]

    options = _question_options(
        question
    )

    if (
        selected_index < 0
        or selected_index >= len(options)
    ):

        await _safe_answer(
            update,
            "گزینه انتخاب‌شده معتبر نیست.",
            show_alert=True,
        )

        return

    correct_index = (
        _correct_option_index(
            question
        )
    )

    # ------------------------------------------------------
    # If service.py exposes answer validation, prefer it.
    # ------------------------------------------------------

    is_correct: bool | None = None

    try:

        validator = getattr(
            service,
            "check_quiz_answer",
            None,
        )

        if callable(validator):

            result = validator(
                chapter_id,
                lesson_id,
                question_index,
                selected_index,
            )

            if isinstance(
                result,
                bool,
            ):
                is_correct = result

    except Exception:
        logger.exception(
            "Banking service quiz validation failed."
        )

    # ------------------------------------------------------
    # Fallback to data question.
    # ------------------------------------------------------

    if is_correct is None:

        if correct_index is not None:

            is_correct = (
                selected_index
                == correct_index
            )

        else:

            # A question without a known answer
            # cannot be safely graded.
            is_correct = False

    if is_correct:

        state["score"] = int(
            state.get(
                "score",
                0,
            )
        ) + 1

    state["answered"] = int(
        state.get(
            "answered",
            0,
        )
    ) + 1

    state["current"] = current + 1

    # ------------------------------------------------------
    # Immediate feedback.
    # ------------------------------------------------------

    if is_correct:

        feedback = (
            "✅ <b>پاسخ شما صحیح بود.</b>"
        )

    else:

        feedback = (
            "❌ <b>پاسخ شما صحیح نبود.</b>"
        )

    if state["current"] >= len(
        questions
    ):

        await _finish_banking_quiz(
            update,
            context,
            prefix_text=feedback,
        )

        return

    next_question = questions[
        state["current"]
    ]

    next_text = (
        f"{feedback}\n\n"
        "⏭️ سؤال بعدی آماده است."
    )

    await _safe_edit(
        update,
        next_text,
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➡️ سؤال بعدی",
                        callback_data=(
                            "banking_quiz:"
                            f"{chapter_id}:"
                            f"{lesson_id}"
                        ),
                    )
                ]
            ]
        ),
    )


# ==========================================================
# Quiz Continue
# ==========================================================

async def continue_banking_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Continue Banking quiz after feedback.

    This function is intentionally available for future
    callback routing if the service layer evolves.
    """

    await _safe_answer(update)

    await _show_current_quiz_question(
        update,
        context,
    )


# ==========================================================
# Finish Quiz
# ==========================================================

async def _finish_banking_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    prefix_text: str = "",
) -> None:
    """Finish Banking quiz and show result."""

    state = _get_quiz_state(
        context
    )

    if state is None:
        return

    chapter_id = str(
        state.get(
            "chapter_id",
            "",
        )
    )

    lesson_id = str(
        state.get(
            "lesson_id",
            "",
        )
    )

    total = len(
        state.get(
            "questions",
            [],
        )
    )

    score = int(
        state.get(
            "score",
            0,
        )
    )

    answered = int(
        state.get(
            "answered",
            0,
        )
    )

    percentage = (
        (score / total) * 100
        if total
        else 0
    )

    if percentage >= 80:

        evaluation = (
            "🏆 عملکرد عالی"
        )

    elif percentage >= 60:

        evaluation = (
            "👍 عملکرد خوب"
        )

    elif percentage >= 40:

        evaluation = (
            "📖 نیاز به مرور بیشتر"
        )

    else:

        evaluation = (
            "🔄 پیشنهاد می‌شود درسنامه را دوباره مطالعه کنید."
        )

    text_parts = []

    if prefix_text:
        text_parts.append(
            prefix_text
        )

    text_parts.append(
        "🏁 <b>آزمون بانکداری به پایان رسید.</b>"
    )

    text_parts.append(
        f"📊 نتیجه: <b>{score}</b> از <b>{total}</b>"
    )

    text_parts.append(
        f"📝 پاسخ داده‌شده: <b>{answered}</b>"
    )

    text_parts.append(
        f"📈 درصد موفقیت: <b>{percentage:.0f}%</b>"
    )

    text_parts.append(
        f"\n{evaluation}"
    )

    text_parts.append(
        "\nبرای ادامه مطالعه می‌توانید "
        "به فصل موردنظر بازگردید."
    )

    _clear_quiz_state(
        context
    )

    await _safe_edit(
        update,
        "\n\n".join(text_parts),
        banking_quiz_result_keyboard(
            chapter_id,
            lesson_id,
        ),
    )


# ==========================================================
# Cancel Quiz
# ==========================================================

async def cancel_banking_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Cancel active Banking quiz."""

    await _safe_answer(update)

    state = _get_quiz_state(
        context
    )

    if state is None:

        await _safe_edit(
            update,
            (
                "📝 <b>آزمون بانکداری</b>\n\n"
                "آزمون فعالی وجود ندارد."
            ),
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🏦 بانکداری",
                            callback_data="menu_banking",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🏠 منوی اصلی",
                            callback_data="menu_main",
                        )
                    ],
                ]
            ),
        )

        return

    chapter_id = str(
        state.get(
            "chapter_id",
            "",
        )
    )

    _clear_quiz_state(
        context
    )

    await _safe_edit(
        update,
        (
            "❌ <b>آزمون لغو شد.</b>\n\n"
            "پاسخ‌های این آزمون در نتیجه نهایی "
            "محاسبه نمی‌شوند."
        ),
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 بازگشت به فصل",
                        callback_data=(
                            f"banking_chapter:"
                            f"{chapter_id}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏦 بانکداری",
                        callback_data="menu_banking",
                    ),
                    InlineKeyboardButton(
                        "🏠 منوی اصلی",
                        callback_data="menu_main",
                    ),
                ],
            ]
        ),
    )


# ==========================================================
# Central Banking Callback Router
# ==========================================================

async def route_banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Central Banking callback router.

    This router allows bot.py to register only one handler
    for the Banking module.
    """

    query = _get_query(update)

    if query is None:
        return

    callback_data = query.data or ""

    logger.info(
        "Banking callback received: %s",
        callback_data,
    )

    if callback_data == "menu_banking":

        await show_banking_menu(
            update,
            context,
        )

        return

    if callback_data == "banking_chapters":

        await show_banking_chapters(
            update,
            context,
        )

        return

    if callback_data.startswith(
        "banking_chapter:"
    ):

        await show_banking_chapter(
            update,
            context,
        )

        return

    if callback_data.startswith(
        "banking_lesson:"
    ):

        await show_banking_lesson(
            update,
            context,
        )

        return

    if callback_data.startswith(
        "banking_complete:"
    ):

        await complete_banking_lesson(
            update,
            context,
        )

        return

    if callback_data.startswith(
        "banking_quiz_answer:"
    ):

        await answer_banking_quiz(
            update,
            context,
        )

        return

    if callback_data.startswith(
        "banking_quiz:"
    ):

        await start_banking_quiz(
            update,
            context,
        )

        return

    if callback_data == "banking_quiz_cancel":

        await cancel_banking_quiz(
            update,
            context,
        )

        return

    await _safe_answer(
        update,
        "این گزینه مربوط به بانکداری نیست.",
        show_alert=False,
    )


# ==========================================================
# Health Check
# ==========================================================

def banking_handlers_health_check() -> bool:
    """
    Check Banking handlers.

    This does not contact Telegram.
    """

    try:

        handlers = [
            show_banking_menu,
            show_banking_chapters,
            show_banking_chapter,
            show_banking_lesson,
            complete_banking_lesson,
            start_banking_quiz,
            answer_banking_quiz,
            cancel_banking_quiz,
            route_banking_callback,
        ]

        if not all(
            callable(handler)
            for handler in handlers
        ):
            return False

        if not MODULE_ID:
            return False

        if not MODULE_TITLE:
            return False

        if not isinstance(
            banking_main_keyboard(),
            InlineKeyboardMarkup,
        ):
            return False

        logger.info(
            "Banking handlers health check: OK"
        )

        return True

    except Exception:

        logger.exception(
            "Banking handlers health check failed."
        )

        return False


# ==========================================================
# Public Aliases
# ==========================================================

# These aliases make integration easier if bot.py or
# future modules use slightly different naming conventions.

show_banking_module = show_banking_menu
show_banking_chapters_menu = show_banking_chapters
show_banking_lesson_details = show_banking_lesson
start_banking_exam = start_banking_quiz
answer_banking_exam = answer_banking_quiz
cancel_banking_exam = cancel_banking_quiz
