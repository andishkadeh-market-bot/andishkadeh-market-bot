"""
Telegram handlers for the Accounting module.
Andishkadeh Management & Market

Features:
- Accounting module menu
- Chapter navigation
- Lesson navigation
- Detailed lesson display
- Specialized tips
- Exam tips
- Practical examples
- Keywords
- Lesson quiz
- Chapter quiz
- Comprehensive accounting quiz
- Quiz scoring
- Result display
- Statistics
- Back navigation
- Compatibility aliases

Expected structure:

modules/
└── accounting/
    ├── __init__.py
    ├── data.py
    ├── service.py
    └── handlers.py
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
    get_module_title,
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
# Safe Helpers
# ==========================================================

async def _answer_callback(
    update: Update,
) -> None:
    """
    Safely answer a Telegram callback query.
    """

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
    """
    Edit the existing callback message when possible.

    If editing fails, send a normal reply.
    """

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
    """
    Escape text for Telegram HTML parsing.
    """

    return html.escape(
        str(value or "")
    )


def _lesson_content(
    lesson: dict[str, Any],
) -> str:
    """
    Support multiple possible lesson content keys.
    """

    possible_keys = (
        "content",
        "text",
        "description",
        "lesson_content",
        "body",
        "details",
        "explanation",
        "article",
    )

    for key in possible_keys:

        value = lesson.get(key)

        if isinstance(value, str) and value.strip():

            return value.strip()

    return (
        "محتوای این درس هنوز ثبت نشده است."
    )


def _list_section(
    title: str,
    values: Any,
) -> str:
    """
    Render a list section safely.
    """

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
                or item.get("content")
                or ""
            )

        else:
            text = item

        if text:

            lines.append(
                f"• {_safe_text(text)}"
            )

    return "\n".join(lines)


def _get_id(
    item: dict[str, Any],
    default: str = "",
) -> str:
    """
    Extract a generic id from a data object.
    """

    value = (
        item.get("id")
        or item.get("chapter_id")
        or item.get("lesson_id")
        or default
    )

    return str(value).strip()


def _get_title(
    item: dict[str, Any],
    default: str = "",
) -> str:
    """
    Extract a generic title.
    """

    return str(
        item.get(
            "title",
            default,
        )
        or default
    )


# ==========================================================
# Main Accounting Menu
# ==========================================================

async def show_accounting_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Display the main Accounting & Financial Reporting menu.
    """

    await _answer_callback(
        update
    )

    chapters = get_accounting_chapters()

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for chapter in chapters:

        if not isinstance(chapter, dict):
            continue

        chapter_id = _get_id(
            chapter
        )

        if not chapter_id:
            continue

        title = _get_title(
            chapter,
            chapter_id,
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📚 {title}",
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
                callback_data=(
                    "accounting_quiz_all"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "📊 آمار دوره",
                callback_data=(
                    "accounting_statistics"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به منوی اصلی",
                callback_data="menu_main",
            )
        ]
    )

    info = get_module_info()

    title = _safe_text(
        info.get(
            "title",
            get_module_title(),
        )
    )

    description = _safe_text(
        info.get(
            "description",
            "",
        )
    )

    text = (
        f"🧾 <b>{title}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{description}\n\n"
        "🎓 <b>مسیر تخصصی حسابداری و گزارشگری مالی</b>\n\n"
        "از مبانی حسابداری، ثبت رویدادهای مالی و "
        "چرخه حسابداری تا حسابداری مالی، حسابداری "
        "مدیریت، بهای تمام‌شده، مالیات، حسابرسی، "
        "تحلیل صورت‌های مالی، استانداردهای گزارشگری "
        "مالی و کاربردهای حرفه‌ای حسابداری.\n\n"
        "📌 فصل موردنظر را انتخاب کنید:"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(
            keyboard
        ),
    )


# ==========================================================
# Chapter Menu
# ==========================================================

async def show_accounting_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
) -> None:
    """
    Display lessons belonging to an accounting chapter.
    """

    await _answer_callback(
        update
    )

    query = update.callback_query

    if (
        chapter_id is None
        and query is not None
    ):

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
            "❌ فصل موردنظر پیدا نشد.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                "menu_accounting"
                            ),
                        )
                    ]
                ]
            ),
        )

        return

    lessons = get_accounting_lessons(
        chapter_id
    )

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for lesson in lessons:

        if not isinstance(lesson, dict):
            continue

        lesson_id = _get_id(
            lesson
        )

        if not lesson_id:
            continue

        title = _get_title(
            lesson,
            lesson_id,
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
                callback_data=(
                    "menu_accounting"
                ),
            )
        ]
    )

    title = _safe_text(
        chapter.get(
            "title",
            chapter_id,
        )
    )

    description = _safe_text(
        chapter.get(
            "description",
            "",
        )
    )

    text = (
        f"📚 <b>{title}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
    )

    if description:

        text += (
            f"{description}\n\n"
        )

    text += (
        f"📖 تعداد درس‌ها: "
        f"<b>{len(lessons)}</b>\n\n"
        "📌 درس موردنظر را انتخاب کنید:"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(
            keyboard
        ),
    )


async def show_accounting_chapter_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
) -> None:
    """
    Compatibility wrapper.
    """

    await show_accounting_chapter(
        update,
        context,
        chapter_id,
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
    """
    Display detailed accounting lesson.
    """

    await _answer_callback(
        update
    )

    query = update.callback_query

    if query is not None:

        data = query.data or ""

        if data.startswith(
            "accounting_lesson:"
        ):

            parts = data.split(
                ":"
            )

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
            "❌ درس موردنظر پیدا نشد.",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به فصل",
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

    content = _safe_text(
        _lesson_content(
            lesson
        )
    )

    text_parts = [
        f"📘 <b>{title}</b>",
        "",
        "📚 <b>درسنامه تخصصی:</b>",
        content,
    ]

    specialized = _list_section(
        "🎯 <b>نکات تخصصی و حرفه‌ای:</b>",
        lesson.get(
            "specialized_tips",
            lesson.get(
                "professional_tips",
                [],
            ),
        ),
    )

    if specialized:
        text_parts.append(
            specialized
        )

    exam_tips = _list_section(
        "📝 <b>نکات آزمونی:</b>",
        lesson.get(
            "exam_tips",
            [],
        ),
    )

    if exam_tips:
        text_parts.append(
            exam_tips
        )

    examples = _list_section(
        "💡 <b>مثال‌های کاربردی:</b>",
        lesson.get(
            "examples",
            [],
        ),
    )

    if examples:
        text_parts.append(
            examples
        )

    keywords = _list_section(
        "🔑 <b>کلیدواژه‌های تخصصی:</b>",
        lesson.get(
            "keywords",
            [],
        ),
    )

    if keywords:
        text_parts.append(
            keywords
        )

    standards = _list_section(
        "📑 <b>استانداردها و مراجع مرتبط:</b>",
        lesson.get(
            "standards",
            lesson.get(
                "references",
                [],
            ),
        ),
    )

    if standards:
        text_parts.append(
            standards
        )

    formulas = _list_section(
        "🧮 <b>فرمول‌ها و روابط مهم:</b>",
        lesson.get(
            "formulas",
            [],
        ),
    )

    if formulas:
        text_parts.append(
            formulas
        )

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
                    callback_data=(
                        "menu_accounting"
                    ),
                )
            ],
        ]
    )

    await _edit_or_reply(
        update,
        text,
        keyboard,
    )


async def show_accounting_lesson_content(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> None:
    """
    Compatibility wrapper.
    """

    await show_accounting_lesson(
        update,
        context,
        chapter_id,
        lesson_id,
    )


# ==========================================================
# Quiz Normalization
# ==========================================================

def _normalize_question(
    question: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize different quiz data formats into one format.
    """

    item = dict(
        question
    )

    options = item.get(
        "options",
        [],
    )

    if not isinstance(
        options,
        list,
    ):

        options = []

    normalized_options: list[str] = []

    for option in options:

        if isinstance(
            option,
            dict,
        ):

            value = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or option.get("title")
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
            item.get(
                "correct_answer",
                item.get(
                    "answer",
                    0,
                ),
            ),
        ),
    )

    try:

        item["correct_index"] = int(
            correct
        )

    except Exception:

        item["correct_index"] = 0

    return item


# ==========================================================
# Quiz Preparation
# ==========================================================

def _prepare_quiz(
    context: ContextTypes.DEFAULT_TYPE,
    questions: list[dict[str, Any]],
    chapter_id: str | None = None,
    lesson_id: str | None = None,
) -> bool:
    """
    Validate and initialize an accounting quiz.
    """

    normalized = [
        _normalize_question(
            question
        )
        for question in questions
        if isinstance(
            question,
            dict,
        )
    ]

    valid_questions: list[
        dict[str, Any]
    ] = []

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
# Start Lesson / Comprehensive Quiz
# ==========================================================

async def start_accounting_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start lesson quiz or comprehensive quiz.
    """

    await _answer_callback(
        update
    )

    query = update.callback_query

    chapter_id: str | None = None
    lesson_id: str | None = None

    if query is not None:

        data = query.data or ""

        if data.startswith(
            "accounting_quiz_lesson:"
        ):

            parts = data.split(
                ":"
            )

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
            (
                "⚠️ برای این بخش هنوز "
                "سؤال آزمون ثبت نشده است."
            ),
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                "menu_accounting"
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
# Chapter Quiz
# ==========================================================

async def start_accounting_chapter_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start all quiz questions belonging to one chapter.
    """

    await _answer_callback(
        update
    )

    query = update.callback_query

    chapter_id: str | None = None

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

    questions: list[
        dict[str, Any]
    ] = []

    lessons = get_accounting_lessons(
        chapter_id
    )

    for lesson in lessons:

        if not isinstance(
            lesson,
            dict,
        ):
            continue

        lesson_id = _get_id(
            lesson
        )

        if not lesson_id:
            continue

        lesson_questions = get_accounting_quiz(
            chapter_id,
            lesson_id,
        )

        if isinstance(
            lesson_questions,
            list,
        ):

            questions.extend(
                lesson_questions
            )

    if not _prepare_quiz(
        context,
        questions,
        chapter_id,
        None,
    ):

        await _edit_or_reply(
            update,
            (
                "⚠️ برای این فصل هنوز "
                "سؤال آزمون ثبت نشده است."
            ),
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به فصل",
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
    """
    Display current quiz question.
    """

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY,
        [],
    )

    index = int(
        context.user_data.get(
            QUIZ_INDEX_KEY,
            0,
        )
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

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for option_index, option in enumerate(
        options
    ):

        keyboard.append(
            [
                InlineKeyboardButton(
                    (
                        f"{chr(65 + option_index)}. "
                        f"{str(option)}"
                    ),
                    callback_data=(
                        "accounting_quiz_answer:"
                        f"{option_index}"
                    ),
                )
            ]
        )

    total = len(
        questions
    )

    question_text = _safe_text(
        question.get(
            "question",
            "",
        )
    )

    text = (
        "🧾 <b>آزمون حسابداری</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📌 سؤال <b>{index + 1}</b> از "
        f"<b>{total}</b>\n\n"
        f"❓ {question_text}"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(
            keyboard
        ),
    )


# ==========================================================
# Answer Quiz
# ==========================================================

async def answer_accounting_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Process selected quiz answer.
    """

    await _answer_callback(
        update
    )

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

    index = int(
        context.user_data.get(
            QUIZ_INDEX_KEY,
            0,
        )
    )

    if (
        not questions
        or index >= len(questions)
    ):

        return

    question = questions[index]

    try:

        correct_index = int(
            question.get(
                "correct_index",
                -1,
            )
        )

    except Exception:

        correct_index = -1

    if selected == correct_index:

        context.user_data[
            QUIZ_SCORE_KEY
        ] = (
            int(
                context.user_data.get(
                    QUIZ_SCORE_KEY,
                    0,
                )
            )
            + 1
        )

        result_text = (
            "✅ <b>پاسخ شما درست بود.</b>\n\n"
            "امتیاز شما برای این سؤال ثبت شد."
        )

    else:

        options = question.get(
            "options",
            [],
        )

        correct_text = ""

        if (
            0 <= correct_index
            < len(options)
        ):

            correct_text = str(
                options[
                    correct_index
                ]
            )

        result_text = (
            "❌ <b>پاسخ شما نادرست بود.</b>\n\n"
            f"پاسخ صحیح: "
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
    """
    Display final accounting quiz result.
    """

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY,
        [],
    )

    total = len(
        questions
    )

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

    if percentage >= 90:

        level_text = (
            "🏆 سطح عملکرد: ممتاز"
        )

    elif percentage >= 75:

        level_text = (
            "🥇 سطح عملکرد: بسیار خوب"
        )

    elif percentage >= 60:

        level_text = (
            "🥈 سطح عملکرد: قابل قبول"
        )

    else:

        level_text = (
            "📚 سطح عملکرد: نیازمند مرور"
        )

    text = (
        "🏁 <b>آزمون حسابداری به پایان رسید</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 تعداد سوالات: <b>{total}</b>\n"
        f"✅ پاسخ صحیح: <b>{score}</b>\n"
        f"❌ پاسخ غلط: <b>{wrong}</b>\n"
        f"📊 نمره: <b>{percentage:.2f}%</b>\n\n"
        f"{level_text}\n\n"
        "نتیجه آزمون ثبت شد."
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 آزمون مجدد",
                    callback_data=(
                        "accounting_quiz_all"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🧾 بازگشت به حسابداری",
                    callback_data=(
                        "menu_accounting"
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
    """
    Display accounting curriculum statistics.
    """

    await _answer_callback(
        update
    )

    try:

        stats = get_curriculum_stats()

    except Exception:

        logger.exception(
            "Unable to load accounting statistics."
        )

        stats = {
            "chapters": 0,
            "lessons": 0,
            "quiz_questions": 0,
        }

    chapters = int(
        stats.get(
            "chapters",
            0,
        )
    )

    lessons = int(
        stats.get(
            "lessons",
            0,
        )
    )

    quiz_questions = int(
        stats.get(
            "quiz_questions",
            0,
        )
    )

    text = (
        "📊 <b>آمار آموزش حسابداری</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 تعداد فصل‌ها: <b>{chapters}</b>\n"
        f"📘 تعداد درس‌ها: <b>{lessons}</b>\n"
        f"📝 تعداد سوالات: <b>{quiz_questions}</b>\n\n"
        "🎓 سطح دوره: تخصصی تا فوق‌تخصصی\n"
        "📑 رویکرد: آموزشی، کاربردی و آزمون‌محور\n"
        "💼 تمرکز: حسابداری مالی، مدیریت، بهای تمام‌شده، "
        "گزارشگری و تحلیل مالی"
    )

    await _edit_or_reply(
        update,
        text,
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data=(
                            "menu_accounting"
                        ),
                    )
                ]
            ]
        ),
    )


# ==========================================================
# Cancel Quiz
# ==========================================================

async def cancel_accounting_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Cancel active accounting quiz.
    """

    await _answer_callback(
        update
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

    await show_accounting_menu(
        update,
        context,
    )


# ==========================================================
# Compatibility Aliases
# ==========================================================

show_accounting = (
    show_accounting_menu
)

show_accounting_chapters = (
    show_accounting_menu
)

show_accounting_chapter_lessons = (
    show_accounting_chapter
)

show_accounting_lesson_menu = (
    show_accounting_chapter
)

start_accounting_quiz_lesson = (
    start_accounting_quiz
)

start_accounting_quiz_all = (
    start_accounting_quiz
)

handle_accounting_quiz_answer = (
    answer_accounting_quiz
)

stop_accounting_quiz = (
    cancel_accounting_quiz
)


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "show_accounting_menu",
    "show_accounting",
    "show_accounting_chapters",
    "show_accounting_chapter",
    "show_accounting_chapter_menu",
    "show_accounting_chapter_lessons",
    "show_accounting_lesson",
    "show_accounting_lesson_menu",
    "show_accounting_lesson_content",
    "start_accounting_quiz",
    "start_accounting_quiz_all",
    "start_accounting_quiz_lesson",
    "start_accounting_chapter_quiz",
    "answer_accounting_quiz",
    "handle_accounting_quiz_answer",
    "finish_accounting_quiz",
    "cancel_accounting_quiz",
    "stop_accounting_quiz",
    "show_accounting_statistics",
]
