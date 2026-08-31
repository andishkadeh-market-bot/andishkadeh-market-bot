"""
Telegram handlers for Psychology & Social Work.

Andishkadeh Management & Market
"""

from __future__ import annotations

import html
import logging
import random
from typing import Any

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from core.quiz_engine import QuizEngine

from modules.psychology.data import (
    MODULE_ID,
    MODULE_TITLE,
    get_chapter,
    get_chapters,
    get_quiz_questions,
    get_lesson,
    get_lessons,
)
from modules.psychology.service import (
    complete_lesson,
    save_quiz_result,
    start_lesson,
)


logger = logging.getLogger(__name__)

PSYCHOLOGY_QUIZ_KEY = "psychology_quiz"


def _safe_text(
    value: Any,
    default: str = "-",
) -> str:
    """Escape text for Telegram HTML."""

    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return html.escape(text)


def _get_user_id(
    update: Update,
) -> int | None:
    """Return Telegram user ID."""

    user = update.effective_user

    if user is None:
        return None

    return user.id


def _get_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
    """Return current Psychology quiz state."""

    state = context.user_data.get(
        PSYCHOLOGY_QUIZ_KEY
    )

    if not isinstance(state, dict):
        return None

    return state


# ==========================================================
# Keyboards
# ==========================================================


def psychology_main_keyboard() -> InlineKeyboardMarkup:
    """Build Psychology module keyboard."""

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for chapter in get_chapters():
        chapter_id = chapter.get("id")

        if not chapter_id:
            continue

        chapter_title = _safe_text(
            chapter.get(
                "title",
                chapter_id,
            )
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📖 {chapter_title}",
                    callback_data=(
                        f"psychology_chapter:{chapter_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 منوی اصلی",
                callback_data="menu_main",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def psychology_chapter_keyboard(
    chapter_id: str,
) -> InlineKeyboardMarkup:
    """Build chapter lesson keyboard."""

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for lesson in get_lessons(chapter_id):
        lesson_id = lesson.get("id")

        if not lesson_id:
            continue

        lesson_title = _safe_text(
            lesson.get(
                "title",
                lesson_id,
            )
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📚 {lesson_title}",
                    callback_data=(
                        f"psychology_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 روانشناسی و مددکاری",
                callback_data="menu_psychology",
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def psychology_lesson_keyboard(
    chapter_id: str,
    lesson_id: str,
    has_quiz: bool = True,
) -> InlineKeyboardMarkup:
    """Build lesson keyboard."""

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    if has_quiz:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📝 شروع آزمون",
                    callback_data=(
                        f"psychology_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "✅ تکمیل درس",
                callback_data=(
                    f"psychology_complete:"
                    f"{chapter_id}:"
                    f"{lesson_id}"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 فصل",
                callback_data=(
                    f"psychology_chapter:"
                    f"{chapter_id}"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="menu_main",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def psychology_quiz_answer_keyboard(
    question_index: int,
    options: list[str],
) -> InlineKeyboardMarkup:
    """Build quiz answer keyboard."""

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    labels = [
        "الف",
        "ب",
        "ج",
        "د",
    ]

    for index, option in enumerate(options):
        if index >= len(labels):
            break

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{labels[index]}. {_safe_text(option)}",
                    callback_data=(
                        f"psychology_quiz_answer:"
                        f"{question_index}:"
                        f"{index}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ لغو آزمون",
                callback_data=(
                    "psychology_quiz_cancel"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# ==========================================================
# Main Menu
# ==========================================================


async def show_psychology_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show Psychology module menu."""

    query = update.callback_query

    text = (
        f"🧠 <b>{_safe_text(MODULE_TITLE)}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "در این بخش می‌توانید مباحث روانشناسی "
        "و مددکاری اجتماعی را به‌صورت فصل‌به‌فصل "
        "مطالعه کنید.\n\n"
        "📚 فصل موردنظر را انتخاب کنید:"
    )

    if query is not None:
        await query.answer()

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=psychology_main_keyboard(),
        )

        return

    if update.message is not None:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=psychology_main_keyboard(),
        )


# ==========================================================
# Chapter
# ==========================================================


async def show_psychology_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show lessons of a Psychology chapter."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    try:
        _, chapter_id = data.split(
            ":",
            1,
        )
    except ValueError:
        await query.edit_message_text(
            "❌ فصل نامعتبر است.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    chapter = get_chapter(
        chapter_id,
    )

    if chapter is None:
        await query.edit_message_text(
            "❌ فصل پیدا نشد.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    lessons = get_lessons(
        chapter_id,
    )

    if not lessons:
        await query.edit_message_text(
            (
                f"📖 <b>{_safe_text(chapter.get('title'))}</b>\n\n"
                "هنوز درسی برای این فصل ثبت نشده است."
            ),
            parse_mode="HTML",
            reply_markup=psychology_main_keyboard(),
        )
        return

    text_lines = [
        f"📖 <b>{_safe_text(chapter.get('title'))}</b>",
        "━━━━━━━━━━━━━━━━━━",
        "",
        "درس موردنظر را انتخاب کنید:",
    ]

    for index, lesson in enumerate(
        lessons,
        start=1,
    ):
        text_lines.insert(
            -1,
            (
                f"{index}. 📚 "
                f"{_safe_text(lesson.get('title'))}"
            ),
        )

    await query.edit_message_text(
        "\n".join(text_lines),
        parse_mode="HTML",
        reply_markup=psychology_chapter_keyboard(
            chapter_id,
        ),
    )


# ==========================================================
# Lesson
# ==========================================================


async def show_psychology_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show a Psychology lesson."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 3:
        await query.edit_message_text(
            "❌ اطلاعات درس نامعتبر است.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    _, chapter_id, lesson_id = parts

    user_id = _get_user_id(update)

    if user_id is None:
        return

    lesson = start_lesson(
        telegram_id=user_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    if lesson is None:
        await query.edit_message_text(
            "❌ درس پیدا نشد.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    title = _safe_text(
        lesson.get(
            "title",
            lesson_id,
        )
    )

    content = _safe_text(
        lesson.get(
            "content",
            "محتوای درس ثبت نشده است.",
        )
    )

    special_points = lesson.get(
        "special_points",
        [],
    )

    exam_points = lesson.get(
        "exam_points",
        [],
    )

    example = _safe_text(
        lesson.get(
            "example",
            "-",
        )
    )

    if not isinstance(
        special_points,
        list,
    ):
        special_points = []

    if not isinstance(
        exam_points,
        list,
    ):
        exam_points = []

    special_text = "\n".join(
        f"• {_safe_text(item)}"
        for item in special_points
    )

    exam_text = "\n".join(
        f"• {_safe_text(item)}"
        for item in exam_points
    )

    questions = get_quiz_questions(
        chapter_id,
        lesson_id,
    )

    has_quiz = bool(questions)

    text = (
        f"🧠 <b>{title}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{content}\n\n"
        "🎯 <b>نکات تخصصی</b>\n"
        f"{special_text or '• موردی ثبت نشده است.'}\n\n"
        "📝 <b>نکات آزمونی</b>\n"
        f"{exam_text or '• موردی ثبت نشده است.'}\n\n"
        "💡 <b>مثال کاربردی</b>\n"
        f"{example}\n\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=psychology_lesson_keyboard(
            chapter_id,
            lesson_id,
            has_quiz=has_quiz,
        ),
    )


# ==========================================================
# Complete Lesson
# ==========================================================


async def complete_psychology_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Mark Psychology lesson as completed."""

    query = update.callback_query

    if query is None:
        return

    await query.answer(
        "درس تکمیل شد.",
        show_alert=False,
    )

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 3:
        return

    _, chapter_id, lesson_id = parts

    user_id = _get_user_id(update)

    if user_id is None:
        return

    completed = complete_lesson(
        telegram_id=user_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )

    if not completed:
        await query.edit_message_text(
            "❌ تکمیل درس انجام نشد.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    await query.edit_message_text(
        (
            "✅ <b>درس با موفقیت تکمیل شد.</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "پیشرفت شما ثبت شد.\n\n"
            "می‌توانید آزمون این درس را نیز انجام دهید."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📝 شروع آزمون",
                        callback_data=(
                            f"psychology_quiz:"
                            f"{chapter_id}:"
                            f"{lesson_id}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 فصل",
                        callback_data=(
                            f"psychology_chapter:"
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


# ==========================================================
# Start Quiz
# ==========================================================


async def start_psychology_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Start a Psychology lesson quiz."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 3:
        await query.edit_message_text(
            "❌ اطلاعات آزمون نامعتبر است.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    _, chapter_id, lesson_id = parts

    questions = get_quiz_questions(
        chapter_id,
        lesson_id,
    )

    if not questions:
        await query.edit_message_text(
            "❌ برای این درس هنوز سوالی ثبت نشده است.",
            reply_markup=psychology_lesson_keyboard(
                chapter_id,
                lesson_id,
                has_quiz=False,
            ),
        )
        return

    user_id = _get_user_id(update)

    if user_id is None:
        return

    selected_questions = list(
        questions
    )

    if len(selected_questions) > 10:
        selected_questions = random.sample(
            selected_questions,
            10,
        )

    normalized_questions: list[
        dict[str, Any]
    ] = []

    for index, question in enumerate(
        selected_questions,
        start=1,
    ):
        item = dict(question)

        if not item.get("id"):
            item["id"] = (
                f"{chapter_id}_"
                f"{lesson_id}_q{index}"
            )

        normalized_questions.append(
            item
        )

    engine = QuizEngine(
        shuffle_questions=False,
        shuffle_options=False,
    )

    try:
        session = engine.start_quiz(
            telegram_id=user_id,
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            questions=normalized_questions,
            replace_existing=True,
        )
    except Exception:
        logger.exception(
            "Failed to start Psychology quiz."
        )

        await query.edit_message_text(
            "❌ خطا در آماده‌سازی آزمون.",
            reply_markup=psychology_lesson_keyboard(
                chapter_id,
                lesson_id,
                has_quiz=True,
            ),
        )
        return

    context.user_data[
        PSYCHOLOGY_QUIZ_KEY
    ] = {
        "engine": engine,
        "telegram_id": user_id,
        "module_id": MODULE_ID,
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "total_questions": session.total_questions(),
    }

    await _show_current_psychology_question(
        update,
        context,
    )


# ==========================================================
# Show Current Question
# ==========================================================


async def _show_current_psychology_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Display current Psychology quiz question."""

    query = update.callback_query

    if query is None:
        return

    state = _get_quiz_state(
        context
    )

    if state is None:
        await query.edit_message_text(
            "❌ آزمون فعالی وجود ندارد.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    engine = state.get(
        "engine"
    )

    telegram_id = state.get(
        "telegram_id"
    )

    if not isinstance(
        engine,
        QuizEngine,
    ):
        await query.edit_message_text(
            "❌ موتور آزمون در دسترس نیست.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    if not isinstance(
        telegram_id,
        int,
    ):
        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    session = engine.get_active_session(
        telegram_id
    )

    if session is None:
        await finish_psychology_quiz(
            update,
            context,
        )
        return

    question = engine.get_current_question(
        telegram_id
    )

    if question is None:
        await finish_psychology_quiz(
            update,
            context,
        )
        return

    current_index = session.current_index
    total = session.total_questions()

    text = (
        "🧠 <b>آزمون روانشناسی و مددکاری</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"سوال <b>{current_index + 1}</b> "
        f"از <b>{total}</b>\n\n"
        f"{_safe_text(question.question)}"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=psychology_quiz_answer_keyboard(
            current_index,
            list(question.options),
        ),
    )


# ==========================================================
# Answer Quiz
# ==========================================================


async def answer_psychology_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Process one Psychology quiz answer."""

    query = update.callback_query

    if query is None:
        return

    state = _get_quiz_state(
        context
    )

    if state is None:
        await query.answer(
            "آزمون فعالی وجود ندارد.",
            show_alert=True,
        )
        return

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 3:
        await query.answer(
            "پاسخ نامعتبر است.",
            show_alert=True,
        )
        return

    try:
        question_index = int(
            parts[1]
        )

        answer_index = int(
            parts[2]
        )

    except ValueError:
        await query.answer(
            "پاسخ نامعتبر است.",
            show_alert=True,
        )
        return

    engine = state.get(
        "engine"
    )

    telegram_id = state.get(
        "telegram_id"
    )

    if not isinstance(
        engine,
        QuizEngine,
    ):
        await query.answer(
            "موتور آزمون در دسترس نیست.",
            show_alert=True,
        )
        return

    if not isinstance(
        telegram_id,
        int,
    ):
        await query.answer(
            "شناسه کاربر نامعتبر است.",
            show_alert=True,
        )
        return

    session = engine.get_active_session(
        telegram_id
    )

    if session is None:
        await query.answer(
            "آزمون فعال نیست.",
            show_alert=True,
        )
        return

    if question_index != session.current_index:
        await query.answer(
            "این سوال دیگر فعال نیست.",
            show_alert=True,
        )
        return

    question = engine.get_current_question(
        telegram_id
    )

    if question is None:
        await query.answer(
            "سوال پیدا نشد.",
            show_alert=True,
        )
        return

    options = list(
        question.options
    )

    if (
        answer_index < 0
        or answer_index >= len(options)
    ):
        await query.answer(
            "گزینه نامعتبر است.",
            show_alert=True,
        )
        return

    selected_answer = options[
        answer_index
    ]

    try:
        result = engine.submit_answer(
            telegram_id=telegram_id,
            answer=selected_answer,
        )
    except Exception:
        logger.exception(
            "Failed to submit Psychology quiz answer."
        )

        await query.answer(
            "خطا در ثبت پاسخ.",
            show_alert=True,
        )
        return

    if result.get("is_correct"):
        await query.answer(
            "✅ پاسخ صحیح",
            show_alert=False,
        )
    else:
        await query.answer(
            "❌ پاسخ ثبت شد",
            show_alert=False,
        )

    if result.get("result") == "finished":
        await finish_psychology_quiz(
            update,
            context,
        )
        return

    await _show_current_psychology_question(
        update,
        context,
    )


# ==========================================================
# Finish Quiz
# ==========================================================


async def finish_psychology_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Finish quiz and save Statistics."""

    query = update.callback_query

    if query is None:
        return

    state = _get_quiz_state(
        context
    )

    if state is None:
        await query.edit_message_text(
            "❌ اطلاعات آزمون پیدا نشد.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    engine = state.get(
        "engine"
    )

    telegram_id = state.get(
        "telegram_id"
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

    if not isinstance(
        engine,
        QuizEngine,
    ):
        context.user_data.pop(
            PSYCHOLOGY_QUIZ_KEY,
            None,
        )

        await query.edit_message_text(
            "❌ موتور آزمون در دسترس نیست.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    if not isinstance(
        telegram_id,
        int,
    ):
        context.user_data.pop(
            PSYCHOLOGY_QUIZ_KEY,
            None,
        )

        await query.edit_message_text(
            "❌ شناسه کاربر نامعتبر است.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    session = engine.get_session(
        telegram_id
    )

    if session is None:
        context.user_data.pop(
            PSYCHOLOGY_QUIZ_KEY,
            None,
        )

        await query.edit_message_text(
            "❌ جلسه آزمون پیدا نشد.",
            reply_markup=psychology_main_keyboard(),
        )
        return

    total_questions = session.total_questions()
    correct_answers = session.correct_answers()
    wrong_answers = session.wrong_answers()
    score = session.score()

    try:
        save_quiz_result(
            telegram_id=telegram_id,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            total_questions=total_questions,
            correct_answers=correct_answers,
        )

        complete_lesson(
            telegram_id=telegram_id,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )

    except Exception:
        logger.exception(
            "Failed to save Psychology quiz result."
        )

        await query.edit_message_text(
            (
                "❌ نتیجه آزمون ثبت نشد.\n\n"
                "لطفاً دوباره تلاش کنید."
            ),
            reply_markup=psychology_main_keyboard(),
        )
        return

    context.user_data.pop(
        PSYCHOLOGY_QUIZ_KEY,
        None,
    )

    await query.edit_message_text(
        (
            "🎉 <b>آزمون به پایان رسید</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"📚 تعداد سوالات: <b>{total_questions}</b>\n"
            f"✅ پاسخ صحیح: <b>{correct_answers}</b>\n"
            f"❌ پاسخ غلط: <b>{wrong_answers}</b>\n"
            f"📊 نمره: <b>{score:.2f}%</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📊 نتیجه در Statistics ثبت شد.\n"
            "📚 پیشرفت درس نیز به‌روزرسانی شد."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 بازگشت به درس",
                        callback_data=(
                            f"psychology_lesson:"
                            f"{chapter_id}:"
                            f"{lesson_id}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🧠 روانشناسی و مددکاری",
                        callback_data="menu_psychology",
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


# ==========================================================
# Cancel Quiz
# ==========================================================


async def cancel_psychology_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Cancel active Psychology quiz."""

    query = update.callback_query

    if query is None:
        return

    await query.answer(
        "آزمون لغو شد.",
        show_alert=False,
    )

    context.user_data.pop(
        PSYCHOLOGY_QUIZ_KEY,
        None,
    )

    await query.edit_message_text(
        (
            "❌ <b>آزمون لغو شد.</b>\n\n"
            "هیچ نتیجه‌ای برای این آزمون در Statistics ثبت نشد."
        ),
        parse_mode="HTML",
        reply_markup=psychology_main_keyboard(),
    )


# ==========================================================
# Callback Router
# ==========================================================


async def route_psychology_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route Psychology callbacks."""

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if data == "menu_psychology":
        await show_psychology_menu(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_chapter:"
    ):
        await show_psychology_chapter(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_lesson:"
    ):
        await show_psychology_lesson(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_complete:"
    ):
        await complete_psychology_lesson(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_quiz:"
    ):
        await start_psychology_quiz(
            update,
            context,
        )
        return

    if data.startswith(
        "psychology_quiz_answer:"
    ):
        await answer_psychology_quiz(
            update,
            context,
        )
        return

    if data == "psychology_quiz_cancel":
        await cancel_psychology_quiz(
            update,
            context,
        )
        return


def psychology_handlers_health_check() -> bool:
    """Basic Psychology handlers health check."""

    try:
        return bool(
            MODULE_ID
            and MODULE_TITLE
            and psychology_main_keyboard
            and psychology_chapter_keyboard
            and psychology_lesson_keyboard
            and start_psychology_quiz
            and answer_psychology_quiz
        )

    except Exception:
        return False
