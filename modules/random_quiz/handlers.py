"""
Telegram handlers for the Random Quiz module.

Andishkadeh Management & Market

Features:
- Random quiz start
- Random question selection
- Quiz Engine integration
- Statistics integration
- Progress integration
- Safe quiz cancellation
- Quiz completion
- Multi-user isolation
"""

from __future__ import annotations

import logging
import random
from typing import Any

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from core.quiz_engine import (
    QuizEngine,
)

from core.statistics import (
    record_quiz_result,
)

from core.progress import (
    mark_lesson_completed,
)

from modules.random_quiz.data import (
    RANDOM_QUESTIONS,
)


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

RANDOM_QUIZ_MODULE_ID = "random_quiz"

RANDOM_QUIZ_CHAPTER_ID = "random"

RANDOM_QUIZ_LESSON_ID = "random_questions"

DEFAULT_QUESTION_COUNT = 10

MIN_QUESTION_COUNT = 1

MAX_QUESTION_COUNT = 20


# ==========================================================
# Context keys
# ==========================================================

QUIZ_CONTEXT_KEY = "random_quiz_engine"

QUIZ_QUESTIONS_KEY = "random_quiz_questions"

QUIZ_INDEX_KEY = "random_quiz_index"

QUIZ_CORRECT_KEY = "random_quiz_correct"

QUIZ_TOTAL_KEY = "random_quiz_total"

QUIZ_STARTED_KEY = "random_quiz_started"


# ==========================================================
# Keyboards
# ==========================================================

def random_quiz_cancel_keyboard() -> InlineKeyboardMarkup:
    """Return quiz cancellation keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❌ لغو آزمون",
                    callback_data="random_quiz_cancel",
                )
            ]
        ]
    )


def random_quiz_result_keyboard() -> InlineKeyboardMarkup:
    """Return keyboard shown after quiz completion."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎲 آزمون تصادفی جدید",
                    callback_data="random_quiz:start",
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


def random_quiz_start_keyboard() -> InlineKeyboardMarkup:
    """Return random quiz start keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎲 شروع آزمون",
                    callback_data="random_quiz:start",
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


# ==========================================================
# Question normalization
# ==========================================================

def _question_text(question: dict[str, Any]) -> str:
    """
    Extract question text from supported data formats.
    """

    return str(
        question.get(
            "question",
            question.get(
                "text",
                "",
            ),
        )
    )


def _question_options(
    question: dict[str, Any],
) -> list[Any]:
    """
    Extract options from supported question formats.
    """

    options = question.get(
        "options",
        [],
    )

    if not isinstance(options, list):
        return []

    return options


def _question_answer(
    question: dict[str, Any],
) -> Any:
    """
    Extract the correct answer.
    """

    if "correct_answer" in question:
        return question["correct_answer"]

    if "answer" in question:
        return question["answer"]

    if "correct" in question:
        return question["correct"]

    return None


def _option_text(
    option: Any,
) -> str:
    """
    Convert an option into display text.
    """

    if isinstance(option, dict):

        return str(
            option.get(
                "text",
                option.get(
                    "label",
                    option.get(
                        "value",
                        "",
                    ),
                ),
            )
        )

    return str(option)


def _option_value(
    option: Any,
) -> Any:
    """
    Extract the comparable option value.
    """

    if isinstance(option, dict):

        if "value" in option:
            return option["value"]

        if "id" in option:
            return option["id"]

        if "text" in option:
            return option["text"]

        if "label" in option:
            return option["label"]

    return option


# ==========================================================
# Question pool
# ==========================================================

def get_random_question_pool() -> list[dict[str, Any]]:
    """
    Return valid random quiz questions.
    """

    if not isinstance(
        RANDOM_QUESTIONS,
        list,
    ):
        return []

    valid_questions = []

    for question in RANDOM_QUESTIONS:

        if not isinstance(
            question,
            dict,
        ):
            continue

        text = _question_text(
            question
        )

        options = _question_options(
            question
        )

        answer = _question_answer(
            question
        )

        if not text:
            continue

        if len(options) < 2:
            continue

        if answer is None:
            continue

        valid_questions.append(
            question
        )

    return valid_questions


# ==========================================================
# Question selection
# ==========================================================

def select_random_questions(
    count: int = DEFAULT_QUESTION_COUNT,
) -> list[dict[str, Any]]:
    """
    Select unique random questions.
    """

    if count < MIN_QUESTION_COUNT:
        count = MIN_QUESTION_COUNT

    if count > MAX_QUESTION_COUNT:
        count = MAX_QUESTION_COUNT

    pool = get_random_question_pool()

    if not pool:
        return []

    count = min(
        count,
        len(pool),
    )

    return random.sample(
        pool,
        count,
    )


# ==========================================================
# Engine creation
# ==========================================================

def _create_engine(
    questions: list[dict[str, Any]],
) -> QuizEngine | None:
    """
    Create a QuizEngine instance.

    The engine is isolated per Telegram user through
    user-specific context storage.
    """

    try:
        return QuizEngine(
            questions=questions
        )
    except TypeError:

        try:
            return QuizEngine(
                questions
            )
        except Exception:

            logger.exception(
                "Failed to create QuizEngine."
            )

            return None

    except Exception:

        logger.exception(
            "Failed to create QuizEngine."
        )

        return None


# ==========================================================
# Engine helpers
# ==========================================================

def _engine_current_question(
    engine: QuizEngine,
) -> dict[str, Any] | None:
    """
    Retrieve current question from QuizEngine.

    Supports common engine method names.
    """

    for method_name in (
        "current_question",
        "get_current_question",
    ):

        method = getattr(
            engine,
            method_name,
            None,
        )

        if callable(method):

            try:
                result = method()

                if isinstance(
                    result,
                    dict,
                ):
                    return result

            except Exception:
                logger.exception(
                    "QuizEngine current question failed."
                )

    return None


def _engine_answer(
    engine: QuizEngine,
    answer: Any,
) -> bool:
    """
    Submit an answer through QuizEngine.

    Supports common engine method names.
    """

    for method_name in (
        "answer",
        "submit_answer",
        "check_answer",
    ):

        method = getattr(
            engine,
            method_name,
            None,
        )

        if callable(method):

            try:
                return bool(
                    method(answer)
                )

            except TypeError:
                continue

            except Exception:

                logger.exception(
                    "QuizEngine answer failed."
                )

                return False

    return False


def _engine_is_finished(
    engine: QuizEngine,
) -> bool:
    """
    Check whether the engine has completed the quiz.
    """

    for attribute_name in (
        "is_finished",
        "finished",
        "completed",
    ):

        value = getattr(
            engine,
            attribute_name,
            None,
        )

        if isinstance(
            value,
            bool,
        ):
            return value

        if callable(value):

            try:
                return bool(
                    value()
                )
            except Exception:
                pass

    for method_name in (
        "is_complete",
        "is_completed",
        "has_finished",
    ):

        method = getattr(
            engine,
            method_name,
            None,
        )

        if callable(method):

            try:
                return bool(
                    method()
                )
            except Exception:
                pass

    return False


def _engine_score(
    engine: QuizEngine,
) -> int:
    """
    Read the number of correct answers.
    """

    for attribute_name in (
        "correct_answers",
        "correct_count",
        "score",
    ):

        value = getattr(
            engine,
            attribute_name,
            None,
        )

        if isinstance(
            value,
            (int, float),
        ):

            return int(value)

    for method_name in (
        "get_correct_answers",
        "get_score",
    ):

        method = getattr(
            engine,
            method_name,
            None,
        )

        if callable(method):

            try:
                return int(
                    method()
                )
            except Exception:
                pass

    return 0


# ==========================================================
# Display question
# ==========================================================

async def _show_question(
    update: Update,
    question: dict[str, Any],
    question_number: int,
    total_questions: int,
) -> None:
    """Display one random quiz question."""

    query = update.callback_query

    if query is None:
        return

    text = _question_text(
        question
    )

    options = _question_options(
        question
    )

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for index, option in enumerate(
        options
    ):

        option_text = _option_text(
            option
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    option_text,
                    callback_data=(
                        "random_quiz:answer:"
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
                    "random_quiz:cancel"
                ),
            )
        ]
    )

    message = (
        "🎲 <b>آزمون سوالات تصادفی</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"❓ سوال <b>{question_number}</b> "
        f"از <b>{total_questions}</b>\n\n"
        f"<b>{text}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "پاسخ خود را انتخاب کنید:"
    )

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
    )


# ==========================================================
# Start quiz
# ==========================================================

async def start_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start a new random quiz.
    """

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    user = update.effective_user

    if user is None:
        return

    questions = select_random_questions()

    if not questions:

        await query.edit_message_text(
            "❌ در حال حاضر سوالی برای آزمون تصادفی ثبت نشده است.",
            reply_markup=random_quiz_start_keyboard(),
        )

        return

    engine = _create_engine(
        questions
    )

    if engine is None:

        await query.edit_message_text(
            "❌ موتور آزمون در حال حاضر قابل استفاده نیست.",
            reply_markup=random_quiz_start_keyboard(),
        )

        return

    context.user_data[
        QUIZ_CONTEXT_KEY
    ] = engine

    context.user_data[
        QUIZ_QUESTIONS_KEY
    ] = questions

    context.user_data[
        QUIZ_INDEX_KEY
    ] = 0

    context.user_data[
        QUIZ_CORRECT_KEY
    ] = 0

    context.user_data[
        QUIZ_TOTAL_KEY
    ] = len(questions)

    context.user_data[
        QUIZ_STARTED_KEY
    ] = True

    logger.info(
        "Random quiz started: telegram_id=%s questions=%s",
        user.id,
        len(questions),
    )

    question = _engine_current_question(
        engine
    )

    if question is None:
        question = questions[0]

    await _show_question(
        update=update,
        question=question,
        question_number=1,
        total_questions=len(questions),
    )


# ==========================================================
# Answer quiz
# ==========================================================

async def answer_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Process one random quiz answer.
    """

    query = update.callback_query

    if query is None:
        return

    user = update.effective_user

    if user is None:
        return

    await query.answer()

    engine = context.user_data.get(
        QUIZ_CONTEXT_KEY
    )

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY
    )

    if engine is None or not questions:

        await query.edit_message_text(
            "⚠️ آزمون فعالی برای شما پیدا نشد.",
            reply_markup=random_quiz_start_keyboard(),
        )

        return

    data = query.data or ""

    try:

        _, _, answer_raw = data.split(
            ":",
            2,
        )

        answer_index = int(
            answer_raw
        )

    except (
        ValueError,
        IndexError,
    ):

        await query.answer(
            "❌ پاسخ نامعتبر است.",
            show_alert=True,
        )

        return

    current_index = int(
        context.user_data.get(
            QUIZ_INDEX_KEY,
            0,
        )
    )

    if current_index >= len(
        questions
    ):

        await finish_random_quiz(
            update,
            context,
        )

        return

    current_question = questions[
        current_index
    ]

    options = _question_options(
        current_question
    )

    if (
        answer_index < 0
        or answer_index >= len(options)
    ):

        await query.answer(
            "❌ گزینه نامعتبر است.",
            show_alert=True,
        )

        return

    selected_option = options[
        answer_index
    ]

    selected_value = _option_value(
        selected_option
    )

    correct_value = _question_answer(
        current_question
    )

    is_correct = _engine_answer(
        engine,
        selected_value,
    )

    if not is_correct:

        is_correct = (
            selected_value
            == correct_value
        )

    if is_correct:

        context.user_data[
            QUIZ_CORRECT_KEY
        ] = (
            int(
                context.user_data.get(
                    QUIZ_CORRECT_KEY,
                    0,
                )
            )
            + 1
        )

    current_index += 1

    context.user_data[
        QUIZ_INDEX_KEY
    ] = current_index

    total_questions = int(
        context.user_data.get(
            QUIZ_TOTAL_KEY,
            len(questions),
        )
    )

    if (
        current_index >= total_questions
        or _engine_is_finished(engine)
    ):

        await finish_random_quiz(
            update,
            context,
        )

        return

    next_question = _engine_current_question(
        engine
    )

    if next_question is None:
        next_question = questions[
            current_index
        ]

    await _show_question(
        update=update,
        question=next_question,
        question_number=current_index + 1,
        total_questions=total_questions,
    )


# ==========================================================
# Finish quiz
# ==========================================================

async def finish_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Complete the quiz and persist Statistics + Progress.
    """

    query = update.callback_query

    if query is None:
        return

    user = update.effective_user

    if user is None:
        return

    questions = context.user_data.get(
        QUIZ_QUESTIONS_KEY,
        [],
    )

    total_questions = int(
        context.user_data.get(
            QUIZ_TOTAL_KEY,
            len(questions),
        )
    )

    correct_answers = int(
        context.user_data.get(
            QUIZ_CORRECT_KEY,
            0,
        )
    )

    if total_questions <= 0:
        total_questions = len(
            questions
        )

    score = (
        round(
            correct_answers
            / total_questions
            * 100,
            2,
        )
        if total_questions > 0
        else 0.0
    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    try:

        record_quiz_result(
            telegram_id=user.id,
            module_id=RANDOM_QUIZ_MODULE_ID,
            chapter_id=RANDOM_QUIZ_CHAPTER_ID,
            lesson_id=RANDOM_QUIZ_LESSON_ID,
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
        )

    except Exception:

        logger.exception(
            "Failed to record random quiz statistics: telegram_id=%s",
            user.id,
        )

    # ------------------------------------------------------
    # Progress
    # ------------------------------------------------------

    try:

        mark_lesson_completed(
            telegram_id=user.id,
            module_id=RANDOM_QUIZ_MODULE_ID,
            chapter_id=RANDOM_QUIZ_CHAPTER_ID,
            lesson_id=RANDOM_QUIZ_LESSON_ID,
        )

    except Exception:

        logger.exception(
            "Failed to record random quiz progress: telegram_id=%s",
            user.id,
        )

    # ------------------------------------------------------
    # Result
    # ------------------------------------------------------

    if score >= 90:
        level = "🏆 عالی"
    elif score >= 75:
        level = "🟢 خیلی خوب"
    elif score >= 50:
        level = "🟡 قابل قبول"
    else:
        level = "🔴 نیاز به مرور"

    text = (
        "🎲 <b>آزمون تصادفی به پایان رسید</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 کاربر: <code>{user.id}</code>\n"
        f"📝 تعداد سوالات: <b>{total_questions}</b>\n"
        f"✅ پاسخ صحیح: <b>{correct_answers}</b>\n"
        f"❌ پاسخ غلط: "
        f"<b>{total_questions - correct_answers}</b>\n"
        f"📊 نمره: <b>{score:.2f}%</b>\n"
        f"🎯 وضعیت: <b>{level}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "نتیجه شما در Statistics ثبت شد و Progress نیز به‌روزرسانی شد."
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=random_quiz_result_keyboard(),
    )

    logger.info(
        (
            "Random quiz completed: "
            "telegram_id=%s score=%.2f correct=%s total=%s"
        ),
        user.id,
        score,
        correct_answers,
        total_questions,
    )

    _clear_quiz_context(
        context
    )


# ==========================================================
# Cancel quiz
# ==========================================================

async def cancel_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Cancel the active random quiz.

    Cancelled quizzes are not recorded as completed
    attempts and do not mark the lesson completed.
    """

    query = update.callback_query

    if query is None:
        return

    await query.answer(
        "آزمون لغو شد.",
        show_alert=False,
    )

    _clear_quiz_context(
        context
    )

    await query.edit_message_text(
        "❌ <b>آزمون تصادفی لغو شد.</b>\n\n"
        "هیچ نتیجه‌ای برای این آزمون در Statistics ثبت نشد.",
        parse_mode="HTML",
        reply_markup=random_quiz_start_keyboard(),
    )


# ==========================================================
# Clear quiz context
# ==========================================================

def _clear_quiz_context(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Clear all active random quiz state."""

    for key in (
        QUIZ_CONTEXT_KEY,
        QUIZ_QUESTIONS_KEY,
        QUIZ_INDEX_KEY,
        QUIZ_CORRECT_KEY,
        QUIZ_TOTAL_KEY,
        QUIZ_STARTED_KEY,
    ):

        context.user_data.pop(
            key,
            None,
        )


# ==========================================================
# Callback router
# ==========================================================

async def route_random_quiz_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Route Random Quiz callbacks.
    """

    query = update.callback_query

    if query is None:
        return

    data = query.data or ""

    if data == "random_quiz:start":

        await start_random_quiz(
            update,
            context,
        )

        return

    if data.startswith(
        "random_quiz:answer:"
    ):

        await answer_random_quiz(
            update,
            context,
        )

        return

    if data == "random_quiz:cancel":

        await cancel_random_quiz(
            update,
            context,
        )

        return


# ==========================================================
# Random Quiz entry menu
# ==========================================================

async def show_random_quiz_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show Random Quiz introduction menu.
    """

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    pool_size = len(
        get_random_question_pool()
    )

    text = (
        "🎲 <b>سوالات تصادفی</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "در این بخش سوالات به‌صورت تصادفی "
        "از بانک سوالات انتخاب می‌شوند.\n\n"
        f"📚 تعداد سوالات موجود: <b>{pool_size}</b>\n"
        f"📝 تعداد سوالات آزمون: <b>{DEFAULT_QUESTION_COUNT}</b>\n\n"
        "نتیجه آزمون در Statistics ذخیره می‌شود "
        "و وضعیت Progress نیز ثبت خواهد شد.\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=random_quiz_start_keyboard(),
    )


# ==========================================================
# Health check
# ==========================================================

def random_quiz_handlers_health_check() -> bool:
    """
    Basic health check for the Random Quiz handlers.
    """

    try:

        pool = get_random_question_pool()

        return isinstance(
            pool,
            list,
        )

    except Exception:

        logger.exception(
            "Random Quiz handlers health check failed."
        )

        return False
