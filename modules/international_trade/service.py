"""
Telegram handlers for the International Trade module.

Andishkadeh Management & Market
--------------------------------

Features:
- International Trade main menu
- Chapter navigation
- Lesson navigation
- Lesson progress tracking
- Quiz start
- Quiz answer handling
- Quiz cancellation
- Statistics integration
- Safe navigation
- Compatible with core.quiz_engine
- Compatible with modules.international_trade.service

This file is the Telegram UI layer only.
Business/content logic remains in service.py.
"""

from __future__ import annotations

import html
import logging
from typing import Any

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from core.progress import (
    mark_lesson_completed,
    mark_lesson_started,
)

from core.statistics import (
    record_quiz_attempt,
)

from core.quiz_engine import (
    QuizEngine,
)

from modules.international_trade.service import (
    get_trade_chapters,
    get_trade_chapter,
    get_trade_lessons,
    get_trade_lesson,
    get_trade_quiz,
)


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

MODULE_ID = "international_trade"

MODULE_TITLE = "تجارت بین‌الملل"

CALLBACK_MAIN = "international_trade"

CALLBACK_CHAPTER = "trade_chapter"

CALLBACK_LESSON = "trade_lesson"

CALLBACK_QUIZ = "trade_quiz"

CALLBACK_QUIZ_ANSWER = "trade_quiz_answer"

CALLBACK_QUIZ_CANCEL = "trade_quiz_cancel"


# ==========================================================
# Helpers
# ==========================================================

def get_telegram_id(update: Update) -> int | None:
    """Return the Telegram ID of the current user."""

    user = update.effective_user

    if user is None:
        return None

    return int(user.id)


def safe_text(value: Any) -> str:
    """Escape dynamic text for Telegram HTML."""

    if value is None:
        return "-"

    return html.escape(str(value))


def get_id(
    item: dict[str, Any],
    default: str = "",
) -> str:
    """Extract a stable ID from a content item."""

    value = (
        item.get("id")
        or item.get("lesson_id")
        or item.get("chapter_id")
    )

    if value is None:
        return default

    return str(value)


# ==========================================================
# Keyboards
# ==========================================================

def trade_main_keyboard(
    chapters: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build International Trade chapter menu."""

    keyboard: list[list[InlineKeyboardButton]] = []

    for chapter in chapters:

        chapter_id = get_id(chapter)

        if not chapter_id:
            continue

        title = (
            chapter.get("title")
            or chapter.get("name")
            or chapter_id
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 {title}",
                    callback_data=(
                        f"{CALLBACK_CHAPTER}:{chapter_id}"
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


def trade_chapter_keyboard(
    module_id: str,
    chapter_id: str,
    lessons: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build lesson list for a chapter."""

    keyboard: list[list[InlineKeyboardButton]] = []

    for lesson in lessons:

        lesson_id = get_id(lesson)

        if not lesson_id:
            continue

        title = (
            lesson.get("title")
            or lesson.get("name")
            or lesson_id
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📖 {title}",
                    callback_data=(
                        f"{CALLBACK_LESSON}:"
                        f"{module_id}:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 تجارت بین‌الملل",
                callback_data=CALLBACK_MAIN,
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


def trade_lesson_keyboard(
    module_id: str,
    chapter_id: str,
    lesson_id: str,
) -> InlineKeyboardMarkup:
    """Build lesson action keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📝 آزمون درس",
                    callback_data=(
                        f"{CALLBACK_QUIZ}:"
                        f"{module_id}:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به فصل",
                    callback_data=(
                        f"{CALLBACK_CHAPTER}:"
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
    )


def quiz_cancel_keyboard() -> InlineKeyboardMarkup:
    """Build quiz cancellation keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❌ لغو آزمون",
                    callback_data=CALLBACK_QUIZ_CANCEL,
                )
            ]
        ]
    )


# ==========================================================
# Quiz state helpers
# ==========================================================

QUIZ_STATE_KEY = "international_trade_quiz"


def get_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
    """Return current International Trade quiz state."""

    value = context.user_data.get(
        QUIZ_STATE_KEY
    )

    if not isinstance(value, dict):
        return None

    return value


def clear_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Clear current quiz state."""

    context.user_data.pop(
        QUIZ_STATE_KEY,
        None,
    )


# ==========================================================
# Quiz engine
# ==========================================================

def create_quiz_engine(
    questions: list[dict[str, Any]],
) -> QuizEngine:
    """
    Create a QuizEngine instance.

    The implementation attempts the common constructor
    patterns used by the project.
    """

    try:
        return QuizEngine(
            questions=questions,
        )
    except TypeError:

        try:
            return QuizEngine(
                questions,
            )
        except TypeError:

            engine = QuizEngine()

            if hasattr(
                engine,
                "load_questions",
            ):
                engine.load_questions(
                    questions
                )

            elif hasattr(
                engine,
                "set_questions",
            ):
                engine.set_questions(
                    questions
                )

            else:
                raise

            return engine


def serialize_quiz_engine(
    engine: QuizEngine,
) -> dict[str, Any]:
    """
    Serialize the quiz engine when supported.

    If the engine already exposes a state dictionary,
    preserve it.
    """

    if hasattr(
        engine,
        "to_dict",
    ):
        result = engine.to_dict()

        if isinstance(result, dict):
            return result

    if hasattr(
        engine,
        "serialize",
    ):
        result = engine.serialize()

        if isinstance(result, dict):
            return result

    state: dict[str, Any] = {}

    for attribute in (
        "questions",
        "current_index",
        "current_question",
        "score",
        "correct_answers",
        "answers",
    ):

        if hasattr(
            engine,
            attribute,
        ):
            state[attribute] = getattr(
                engine,
                attribute,
            )

    return state


def restore_quiz_engine(
    state: dict[str, Any],
) -> QuizEngine:
    """Restore QuizEngine from stored state."""

    if hasattr(
        QuizEngine,
        "from_dict",
    ):
        return QuizEngine.from_dict(
            state
        )

    if hasattr(
        QuizEngine,
        "deserialize",
    ):
        return QuizEngine.deserialize(
            state
        )

    questions = state.get(
        "questions",
        [],
    )

    engine = create_quiz_engine(
        questions
    )

    for attribute in (
        "current_index",
        "current_question",
        "score",
        "correct_answers",
        "answers",
    ):

        if attribute in state:

            try:
                setattr(
                    engine,
                    attribute,
                    state[attribute],
                )
            except Exception:
                pass

    return engine


# ==========================================================
# Main module menu
# ==========================================================

async def show_international_trade_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show International Trade main menu."""

    query = update.callback_query

    if query is not None:
        await query.answer()

    try:

        chapters = get_trade_chapters()

    except Exception:

        logger.exception(
            "Failed to load International Trade chapters."
        )

        text = (
            "❌ <b>خطا در بارگذاری تجارت بین‌الملل</b>\n\n"
            "اطلاعات آموزشی در حال حاضر قابل دریافت نیست."
        )

        if query is not None:

            await query.edit_message_text(
                text,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🏠 منوی اصلی",
                                callback_data="menu_main",
                            )
                        ]
                    ]
                ),
            )

        return

    text = (
        "🌍 <b>تجارت بین‌الملل</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "آموزش تخصصی مفاهیم و مباحث تجارت بین‌الملل\n\n"
        "لطفاً فصل موردنظر را انتخاب کنید:"
    )

    keyboard = trade_main_keyboard(
        chapters
    )

    if query is not None:

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        return

    if update.message is not None:

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )


# ==========================================================
# Chapter
# ==========================================================

async def show_international_trade_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show lessons inside an International Trade chapter."""

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
            "❌ شناسه فصل نامعتبر است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    try:

        chapter = get_trade_chapter(
            chapter_id
        )

        lessons = get_trade_lessons(
            chapter_id
        )

    except Exception:

        logger.exception(
            "Failed to load trade chapter %s.",
            chapter_id,
        )

        await query.edit_message_text(
            "❌ خطا در دریافت فصل.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    if not chapter:

        await query.edit_message_text(
            "❌ فصل موردنظر پیدا نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    chapter_title = (
        chapter.get("title")
        or chapter.get("name")
        or chapter_id
    )

    if not lessons:

        text = (
            f"📘 <b>{safe_text(chapter_title)}</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "هنوز درسی برای این فصل ثبت نشده است."
        )

    else:

        text = (
            f"📘 <b>{safe_text(chapter_title)}</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "درس موردنظر را انتخاب کنید:"
        )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=trade_chapter_keyboard(
            MODULE_ID,
            chapter_id,
            lessons,
        ),
    )


# ==========================================================
# Lesson
# ==========================================================

async def show_international_trade_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show one International Trade lesson."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 4:

        await query.edit_message_text(
            "❌ اطلاعات درس نامعتبر است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    _, module_id, chapter_id, lesson_id = parts

    if module_id != MODULE_ID:

        await query.edit_message_text(
            "❌ ماژول نامعتبر است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    try:

        lesson = get_trade_lesson(
            chapter_id,
            lesson_id,
        )

    except Exception:

        logger.exception(
            "Failed to load trade lesson %s/%s.",
            chapter_id,
            lesson_id,
        )

        await query.edit_message_text(
            "❌ خطا در دریافت درس.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    if not lesson:

        await query.edit_message_text(
            "❌ درس موردنظر پیدا نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    telegram_id = get_telegram_id(
        update
    )

    if telegram_id is not None:

        try:

            mark_lesson_started(
                telegram_id=telegram_id,
                module_id=MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
            )

        except Exception:

            logger.exception(
                "Failed to mark trade lesson as started."
            )

    title = (
        lesson.get("title")
        or lesson.get("name")
        or lesson_id
    )

    content = (
        lesson.get("content")
        or lesson.get("text")
        or lesson.get("description")
        or ""
    )

    summary = lesson.get(
        "summary"
    )

    tips = lesson.get(
        "tips"
    )

    text_parts = [
        f"🌍 <b>{safe_text(title)}</b>",
        "━━━━━━━━━━━━━━━━━━",
    ]

    if content:

        text_parts.append(
            safe_text(content)
        )

    if summary:

        text_parts.extend(
            [
                "",
                "📌 <b>خلاصه</b>",
                safe_text(summary),
            ]
        )

    if tips:

        text_parts.extend(
            [
                "",
                "🎯 <b>نکات مهم</b>",
                safe_text(tips),
            ]
        )

    text_parts.extend(
        [
            "",
            "━━━━━━━━━━━━━━━━━━",
            "پس از مطالعه می‌توانید در آزمون درس شرکت کنید.",
        ]
    )

    await query.edit_message_text(
        "\n".join(text_parts),
        parse_mode="HTML",
        reply_markup=trade_lesson_keyboard(
            MODULE_ID,
            chapter_id,
            lesson_id,
        ),
    )


# ==========================================================
# Start quiz
# ==========================================================

async def start_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Start a lesson quiz."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 4:

        await query.edit_message_text(
            "❌ اطلاعات آزمون نامعتبر است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🏠 منوی اصلی",
                            callback_data="menu_main",
                        )
                    ]
                ]
            ),
        )

        return

    _, module_id, chapter_id, lesson_id = parts

    if module_id != MODULE_ID:

        await query.edit_message_text(
            "❌ ماژول نامعتبر است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🏠 منوی اصلی",
                            callback_data="menu_main",
                        )
                    ]
                ]
            ),
        )

        return

    try:

        questions = get_trade_quiz(
            chapter_id,
            lesson_id,
        )

    except Exception:

        logger.exception(
            "Failed to load trade quiz %s/%s.",
            chapter_id,
            lesson_id,
        )

        await query.edit_message_text(
            "❌ خطا در دریافت سوالات آزمون.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🏠 منوی اصلی",
                            callback_data="menu_main",
                        )
                    ]
                ]
            ),
        )

        return

    if not questions:

        await query.edit_message_text(
            "📝 برای این درس هنوز سوالی ثبت نشده است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به درس",
                            callback_data=(
                                f"{CALLBACK_LESSON}:"
                                f"{MODULE_ID}:"
                                f"{chapter_id}:"
                                f"{lesson_id}"
                            ),
                        )
                    ]
                ]
            ),
        )

        return

    try:

        engine = create_quiz_engine(
            questions
        )

        context.user_data[
            QUIZ_STATE_KEY
        ] = {
            "module_id": MODULE_ID,
            "chapter_id": chapter_id,
            "lesson_id": lesson_id,
            "engine": serialize_quiz_engine(
                engine
            ),
        }

        await render_current_question(
            update,
            context,
            engine,
        )

    except Exception:

        logger.exception(
            "Failed to start International Trade quiz."
        )

        clear_quiz_state(
            context
        )

        await query.edit_message_text(
            "❌ خطا در شروع آزمون.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🏠 منوی اصلی",
                            callback_data="menu_main",
                        )
                    ]
                ]
            ),
        )


# ==========================================================
# Render question
# ==========================================================

async def render_current_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    engine: QuizEngine,
) -> None:
    """Render the current quiz question."""

    query = update.callback_query

    if query is None:
        return

    question: Any = None

    for method_name in (
        "current_question",
        "get_current_question",
        "next_question",
    ):

        method = getattr(
            engine,
            method_name,
            None,
        )

        if callable(method):

            try:

                question = method()

            except TypeError:
                continue

            if question is not None:
                break

    if question is None:

        await finish_international_trade_quiz(
            update,
            context,
            engine,
        )

        return

    if isinstance(
        question,
        dict,
    ):

        question_text = (
            question.get("question")
            or question.get("text")
            or question.get("title")
            or "سوال"
        )

        options = (
            question.get("options")
            or question.get("answers")
            or []
        )

    else:

        question_text = str(
            question
        )

        options = []

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for index, option in enumerate(
        options
    ):

        if isinstance(
            option,
            dict,
        ):

            option_text = (
                option.get("text")
                or option.get("label")
                or option.get("answer")
                or str(option)
            )

            option_value = (
                option.get("id")
                or option.get("value")
                or index
            )

        else:

            option_text = str(
                option
            )

            option_value = index

        keyboard.append(
            [
                InlineKeyboardButton(
                    str(option_text),
                    callback_data=(
                        f"{CALLBACK_QUIZ_ANSWER}:"
                        f"{option_value}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ لغو آزمون",
                callback_data=CALLBACK_QUIZ_CANCEL,
            )
        ]
    )

    await query.edit_message_text(
        (
            "📝 <b>آزمون تجارت بین‌الملل</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"{safe_text(question_text)}"
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
    )


# ==========================================================
# Answer quiz
# ==========================================================

async def answer_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Process a quiz answer."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    state = get_quiz_state(
        context
    )

    if state is None:

        await query.edit_message_text(
            "⚠️ آزمون فعالی وجود ندارد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🌍 تجارت بین‌الملل",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )

        return

    data = query.data or ""

    try:

        _, raw_answer = data.split(
            ":",
            1,
        )

    except ValueError:

        await query.edit_message_text(
            "❌ پاسخ نامعتبر است.",
            reply_markup=quiz_cancel_keyboard(),
        )

        return

    try:

        answer_value: Any = int(
            raw_answer
        )

    except ValueError:

        answer_value = raw_answer

    try:

        engine = restore_quiz_engine(
            state["engine"]
        )

        result: Any = None

        for method_name in (
            "answer",
            "submit_answer",
            "check_answer",
            "answer_question",
        ):

            method = getattr(
                engine,
                method_name,
                None,
            )

            if callable(method):

                result = method(
                    answer_value
                )

                break

        if result is None:

            raise RuntimeError(
                "QuizEngine does not expose an answer method."
            )

        state["engine"] = (
            serialize_quiz_engine(
                engine
            )
        )

        context.user_data[
            QUIZ_STATE_KEY
        ] = state

        completed = False

        if isinstance(
            result,
            dict,
        ):

            completed = bool(
                result.get("completed")
                or result.get("finished")
                or result.get("is_finished")
            )

        if hasattr(
            engine,
            "is_finished",
        ):

            value = getattr(
                engine,
                "is_finished",
            )

            completed = completed or bool(
                value() if callable(value) else value
            )

        if completed:

            await finish_international_trade_quiz(
                update,
                context,
                engine,
            )

            return

        await render_current_question(
            update,
            context,
            engine,
        )

    except Exception:

        logger.exception(
            "Failed to process International Trade quiz answer."
        )

        await query.edit_message_text(
            "❌ خطا در ثبت پاسخ آزمون.",
            reply_markup=quiz_cancel_keyboard(),
        )


# ==========================================================
# Finish quiz
# ==========================================================

async def finish_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    engine: QuizEngine,
) -> None:
    """Finish quiz and record progress/statistics."""

    query = update.callback_query

    if query is None:
        return

    state = get_quiz_state(
        context
    )

    if state is None:
        return

    module_id = state.get(
        "module_id",
        MODULE_ID,
    )

    chapter_id = state.get(
        "chapter_id",
        "",
    )

    lesson_id = state.get(
        "lesson_id",
        "",
    )

    total_questions = 0

    correct_answers = 0

    score = 0.0

    for attribute in (
        "total_questions",
        "question_count",
        "total",
    ):

        if hasattr(
            engine,
            attribute,
        ):

            value = getattr(
                engine,
                attribute,
            )

            try:
                total_questions = int(
                    value() if callable(value) else value
                )

            except (
                TypeError,
                ValueError,
            ):
                pass

            if total_questions:
                break

    for attribute in (
        "correct_answers",
        "correct_count",
        "score",
    ):

        if hasattr(
            engine,
            attribute,
        ):

            value = getattr(
                engine,
                attribute,
            )

            try:

                numeric_value = float(
                    value() if callable(value) else value
                )

                if attribute == "score":

                    score = numeric_value

                else:

                    correct_answers = int(
                        numeric_value
                    )

            except (
                TypeError,
                ValueError,
            ):
                pass

    if total_questions <= 0:

        questions = getattr(
            engine,
            "questions",
            [],
        )

        if isinstance(
            questions,
            list,
        ):
            total_questions = len(
                questions
            )

    if score <= 0 and total_questions > 0:

        score = (
            correct_answers
            / total_questions
            * 100
        )

    if score > 100:

        score = 100.0

    telegram_id = get_telegram_id(
        update
    )

    if telegram_id is not None:

        try:

            mark_lesson_completed(
                telegram_id=telegram_id,
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
            )

        except Exception:

            logger.exception(
                "Failed to mark trade lesson completed."
            )

        try:

            record_quiz_attempt(
                telegram_id=telegram_id,
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                total_questions=total_questions,
                correct_answers=correct_answers,
                score=score,
            )

        except Exception:

            logger.exception(
                "Failed to record trade quiz statistics."
            )

    clear_quiz_state(
        context
    )

    await query.edit_message_text(
        (
            "🏆 <b>آزمون تجارت بین‌الملل به پایان رسید</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"❓ تعداد سوالات: <b>{total_questions}</b>\n"
            f"✅ پاسخ صحیح: <b>{correct_answers}</b>\n"
            f"❌ پاسخ غلط: "
            f"<b>{max(total_questions - correct_answers, 0)}</b>\n"
            f"📊 نمره: <b>{score:.2f}%</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "پیشرفت آموزشی و آمار آزمون شما ثبت شد."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌍 تجارت بین‌الملل",
                        callback_data=CALLBACK_MAIN,
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
# Cancel quiz
# ==========================================================

async def cancel_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Cancel current quiz safely."""

    query = update.callback_query

    if query is None:
        return

    await query.answer(
        "آزمون لغو شد."
    )

    clear_quiz_state(
        context
    )

    await query.edit_message_text(
        (
            "❌ <b>آزمون لغو شد</b>\n\n"
            "هیچ نمره‌ای برای این آزمون ثبت نشد."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌍 تجارت بین‌الملل",
                        callback_data=CALLBACK_MAIN,
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
# Callback router
# ==========================================================

async def route_international_trade_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route all International Trade callbacks.

    This router is intended to be registered in bot.py
    before a generic callback fallback.
    """

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if data == CALLBACK_MAIN:

        await show_international_trade_menu(
            update,
            context,
        )

        return

    if data.startswith(
        f"{CALLBACK_CHAPTER}:"
    ):

        await show_international_trade_chapter(
            update,
            context,
        )

        return

    if data.startswith(
        f"{CALLBACK_LESSON}:"
    ):

        await show_international_trade_lesson(
            update,
            context,
        )

        return

    if data.startswith(
        f"{CALLBACK_QUIZ}:"
    ):

        await start_international_trade_quiz(
            update,
            context,
        )

        return

    if data.startswith(
        f"{CALLBACK_QUIZ_ANSWER}:"
    ):

        await answer_international_trade_quiz(
            update,
            context,
        )

        return

    if data == CALLBACK_QUIZ_CANCEL:

        await cancel_international_trade_quiz(
            update,
            context,
        )

        return


# ==========================================================
# Health check
# ==========================================================

def international_trade_handlers_health_check() -> bool:
    """
    Basic handler health check.

    Does not contact Telegram or SQLite.
    """

    required = (
        show_international_trade_menu,
        show_international_trade_chapter,
        show_international_trade_lesson,
        start_international_trade_quiz,
        answer_international_trade_quiz,
        cancel_international_trade_quiz,
        route_international_trade_callback,
    )

    return all(
        callable(item)
        for item in required
    )
