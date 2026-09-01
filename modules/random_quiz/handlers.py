"""
Random Quiz handlers for Andishkadeh Management & Market.

Responsibilities:
- Show Random Quiz menu
- Start random quizzes
- Select random questions
- Display questions
- Handle answers
- Show result
- Cancel quiz
- Work with the central Quiz Engine
- Remain independent from main bot entry point
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

from modules.random_quiz.data import (
    RANDOM_QUIZ_CONFIG,
    get_random_questions,
)

from core.quiz_engine import (
    QuizEngine,
    quiz_engine,
    STATUS_ACTIVE,
    STATUS_COMPLETED,
    STATUS_CANCELLED,
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
RANDOM_QUIZ_LESSON_ID = "random_quiz"

RANDOM_QUIZ_CHAPTER_TITLE = "🎲 سوالات تصادفی"
RANDOM_QUIZ_LESSON_TITLE = "🎲 آزمون تصادفی"


# ==========================================================
# Helpers
# ==========================================================

def _get_user_id(
    update: Update,
) -> int | None:
    """Return Telegram user ID."""

    user = update.effective_user

    if user is None:
        return None

    return user.id


def _safe_callback_answer(
    update: Update,
) -> None:
    """
    Compatibility helper.

    CallbackQuery.answer() is async, therefore this helper
    is intentionally not used for direct answering.
    """
    return


def _build_main_keyboard() -> InlineKeyboardMarkup:
    """Build Random Quiz main menu keyboard."""

    keyboard = [
        [
            InlineKeyboardButton(
                "🎯 شروع آزمون تصادفی",
                callback_data="random_quiz_start",
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 آزمون جدید",
                callback_data="random_quiz_start",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="main_menu",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def _build_cancel_keyboard() -> InlineKeyboardMarkup:
    """Build quiz cancellation keyboard."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❌ لغو آزمون",
                    callback_data="random_quiz_cancel",
                )
            ],
        ]
    )


def _build_question_keyboard(
    options: tuple[str, ...],
) -> InlineKeyboardMarkup:
    """
    Build answer buttons.

    Answers are referenced by their numeric index.
    This keeps callback_data short and avoids putting
    long Persian text inside Telegram callback data.
    """

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for index, option in enumerate(
        options
    ):
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{index + 1}. {option}",
                    callback_data=(
                        f"random_quiz_answer:{index}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ لغو آزمون",
                callback_data="random_quiz_cancel",
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


def _get_question_count() -> int:
    """
    Return valid default question count.

    The available question bank may currently contain
    fewer questions than the configured maximum.
    """

    configured_count = int(
        RANDOM_QUIZ_CONFIG.get(
            "default_question_count",
            10,
        )
    )

    minimum_count = int(
        RANDOM_QUIZ_CONFIG.get(
            "minimum_question_count",
            1,
        )
    )

    maximum_count = int(
        RANDOM_QUIZ_CONFIG.get(
            "maximum_question_count",
            20,
        )
    )

    questions = get_random_questions()

    available_count = len(
        questions
    )

    if available_count <= 0:
        raise RuntimeError(
            "Random Quiz question bank is empty."
        )

    configured_count = max(
        configured_count,
        minimum_count,
    )

    configured_count = min(
        configured_count,
        maximum_count,
    )

    configured_count = min(
        configured_count,
        available_count,
    )

    return configured_count


def _select_random_questions() -> list[
    dict[str, Any]
]:
    """
    Select random questions from the question bank.
    """

    questions = get_random_questions()

    if not questions:
        raise RuntimeError(
            "Random Quiz question bank is empty."
        )

    question_count = (
        _get_question_count()
    )

    return random.sample(
        questions,
        k=question_count,
    )


async def _show_current_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    edit_message: bool = True,
) -> None:
    """
    Display the current question from Quiz Engine.
    """

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        return

    question = (
        quiz_engine.get_current_question(
            user_id
        )
    )

    if question is None:
        result = quiz_engine.get_result(
            user_id
        )

        if result is not None:
            await _show_final_result(
                update,
                context,
                result=result.to_dict(),
                edit_message=edit_message,
            )

        return

    state = quiz_engine.get_state(
        user_id
    )

    if state is None:
        return

    current_number = (
        state["current_index"] + 1
    )

    total_questions = (
        state["total_questions"]
    )

    text = (
        "🎲 <b>آزمون سوالات تصادفی</b>\n\n"
        f"📝 سؤال {current_number} از "
        f"{total_questions}\n\n"
        f"<b>{question.question}</b>\n\n"
        "👇 یکی از گزینه‌ها را انتخاب کنید:"
    )

    keyboard = _build_question_keyboard(
        question.options
    )

    try:
        if (
            edit_message
            and update.callback_query is not None
            and update.callback_query.message is not None
        ):
            await update.callback_query.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

        elif update.message is not None:
            await update.message.reply_text(
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

    except Exception:
        logger.exception(
            "Failed to display Random Quiz question."
        )


async def _show_final_result(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    result: dict[str, Any],
    edit_message: bool = True,
) -> None:
    """Display final quiz result."""

    total_questions = int(
        result.get(
            "total_questions",
            0,
        )
    )

    answered_questions = int(
        result.get(
            "answered_questions",
            0,
        )
    )

    correct_answers = int(
        result.get(
            "correct_answers",
            0,
        )
    )

    wrong_answers = int(
        result.get(
            "wrong_answers",
            0,
        )
    )

    score = float(
        result.get(
            "score",
            0,
        )
    )

    status = result.get(
        "status",
        STATUS_COMPLETED,
    )

    if status == STATUS_CANCELLED:
        title = "❌ آزمون لغو شد"
    else:
        title = "🏆 نتیجه آزمون تصادفی"

    if score >= 90:
        evaluation = "🌟 عالی"
    elif score >= 70:
        evaluation = "👏 بسیار خوب"
    elif score >= 50:
        evaluation = "👍 قابل قبول"
    else:
        evaluation = "📚 نیاز به مرور بیشتر"

    text = (
        f"{title}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📊 تعداد سوالات: {total_questions}\n"
        f"✅ پاسخ صحیح: {correct_answers}\n"
        f"❌ پاسخ غلط: {wrong_answers}\n"
        f"📝 پاسخ داده‌شده: {answered_questions}\n"
        f"🎯 امتیاز: {score:.2f}%\n"
        f"{evaluation}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🎲 می‌توانید یک آزمون جدید شروع کنید."
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 آزمون جدید",
                    callback_data="random_quiz_start",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="main_menu",
                )
            ],
        ]
    )

    try:
        if (
            edit_message
            and update.callback_query is not None
            and update.callback_query.message is not None
        ):
            await update.callback_query.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

        elif update.message is not None:
            await update.message.reply_text(
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

    except Exception:
        logger.exception(
            "Failed to display Random Quiz result."
        )


# ==========================================================
# Main Random Quiz Menu
# ==========================================================

async def show_random_quiz_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Display Random Quiz module menu.
    """

    query = update.callback_query

    if query is not None:
        await query.answer()

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        return

    active_session = (
        quiz_engine.get_active_session(
            user_id
        )
    )

    if active_session is not None:
        state = quiz_engine.get_state(
            user_id
        )

        current_index = (
            state["current_index"] + 1
            if state
            else 1
        )

        total_questions = (
            state["total_questions"]
            if state
            else 0
        )

        text = (
            "🎲 <b>سوالات تصادفی</b>\n\n"
            "⚠️ شما یک آزمون فعال دارید.\n\n"
            f"📝 سؤال فعلی: "
            f"{current_index} از "
            f"{total_questions}\n\n"
            "می‌توانید آزمون فعلی را ادامه دهید "
            "یا آن را لغو کرده و آزمون جدیدی شروع کنید."
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "▶️ ادامه آزمون",
                        callback_data=(
                            "random_quiz_continue"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔄 شروع آزمون جدید",
                        callback_data=(
                            "random_quiz_restart"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ لغو آزمون",
                        callback_data=(
                            "random_quiz_cancel"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data="main_menu",
                    )
                ],
            ]
        )

    else:
        question_count = _get_question_count()

        text = (
            "🎲 <b>سوالات تصادفی</b>\n\n"
            "در این بخش، سوالات به‌صورت تصادفی "
            "از بانک سوالات اندیشکده انتخاب می‌شوند.\n\n"
            f"📝 تعداد سوالات این آزمون: "
            f"<b>{question_count}</b>\n\n"
            "🎯 سوالات می‌توانند از موضوعات مختلف "
            "مدیریت، بازاریابی، تجارت بین‌الملل، "
            "اقتصاد و بانکداری باشند.\n\n"
            "برای شروع، روی دکمه زیر بزنید."
        )

        keyboard = _build_main_keyboard()

    if query is not None and query.message is not None:
        await query.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    elif update.message is not None:
        await update.message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


# ==========================================================
# Start Random Quiz
# ==========================================================

async def start_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start a new Random Quiz session.
    """

    query = update.callback_query

    if query is not None:
        await query.answer(
            "🎲 در حال آماده‌سازی آزمون..."
        )

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        return

    try:
        selected_questions = (
            _select_random_questions()
        )

        session = quiz_engine.start_quiz(
            telegram_id=user_id,
            module_id=RANDOM_QUIZ_MODULE_ID,
            chapter_id=RANDOM_QUIZ_CHAPTER_ID,
            lesson_id=RANDOM_QUIZ_LESSON_ID,
            questions=selected_questions,
            replace_existing=False,
        )

        logger.info(
            (
                "Random Quiz started: "
                "telegram_id=%s questions=%s"
            ),
            user_id,
            session.total_questions(),
        )

        await _show_current_question(
            update,
            context,
            edit_message=True,
        )

    except RuntimeError as exc:

        logger.warning(
            (
                "Random Quiz could not start: "
                "telegram_id=%s error=%s"
            ),
            user_id,
            exc,
        )

        active_session = (
            quiz_engine.get_active_session(
                user_id
            )
        )

        if active_session is not None:
            text = (
                "⚠️ شما در حال حاضر یک آزمون فعال دارید.\n\n"
                "ابتدا آزمون فعلی را ادامه دهید "
                "یا آن را لغو کنید."
            )

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "▶️ ادامه آزمون",
                            callback_data=(
                                "random_quiz_continue"
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "❌ لغو آزمون",
                            callback_data=(
                                "random_quiz_cancel"
                            ),
                        )
                    ],
                ]
            )

        else:
            text = (
                "❌ امکان شروع آزمون وجود ندارد.\n\n"
                "بانک سوالات تصادفی خالی است "
                "یا مشکلی در آماده‌سازی آزمون ایجاد شده است."
            )

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="main_menu",
                        )
                    ]
                ]
            )

        if (
            query is not None
            and query.message is not None
        ):
            await query.message.edit_text(
                text=text,
                reply_markup=keyboard,
            )

    except Exception:
        logger.exception(
            (
                "Unexpected error while starting "
                "Random Quiz: telegram_id=%s"
            ),
            user_id,
        )

        if (
            query is not None
            and query.message is not None
        ):
            await query.message.edit_text(
                text=(
                    "❌ خطایی هنگام شروع آزمون رخ داد.\n\n"
                    "لطفاً دوباره تلاش کنید."
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔙 بازگشت",
                                callback_data="main_menu",
                            )
                        ]
                    ]
                ),
            )


# ==========================================================
# Continue Random Quiz
# ==========================================================

async def continue_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Continue an active Random Quiz."""

    query = update.callback_query

    if query is not None:
        await query.answer(
            "▶️ ادامه آزمون"
        )

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        return

    session = (
        quiz_engine.get_active_session(
            user_id
        )
    )

    if session is None:
        await show_random_quiz_menu(
            update,
            context,
        )
        return

    await _show_current_question(
        update,
        context,
        edit_message=True,
    )


# ==========================================================
# Restart Random Quiz
# ==========================================================

async def restart_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Cancel current quiz and start a new one.
    """

    query = update.callback_query

    if query is not None:
        await query.answer(
            "🔄 آماده‌سازی آزمون جدید..."
        )

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        return

    try:
        active_session = (
            quiz_engine.get_active_session(
                user_id
            )
        )

        if active_session is not None:
            quiz_engine.cancel_quiz(
                user_id
            )

        quiz_engine.remove_session(
            user_id
        )

        await start_random_quiz(
            update,
            context,
        )

    except Exception:
        logger.exception(
            (
                "Failed to restart Random Quiz: "
                "telegram_id=%s"
            ),
            user_id,
        )

        if (
            query is not None
            and query.message is not None
        ):
            await query.message.edit_text(
                text=(
                    "❌ شروع آزمون جدید با خطا مواجه شد."
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔙 بازگشت",
                                callback_data="main_menu",
                            )
                        ]
                    ]
                ),
            )


# ==========================================================
# Answer Random Quiz
# ==========================================================

async def answer_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Handle Random Quiz answer callback.
    """

    query = update.callback_query

    if query is None:
        return

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        await query.answer()
        return

    callback_data = (
        query.data or ""
    )

    try:
        prefix = (
            "random_quiz_answer:"
        )

        if not callback_data.startswith(
            prefix
        ):
            await query.answer(
                "❌ پاسخ نامعتبر است."
            )
            return

        answer_index_text = (
            callback_data[
                len(prefix):
            ]
        )

        answer_index = int(
            answer_index_text
        )

    except (
        ValueError,
        TypeError,
    ):
        await query.answer(
            "❌ پاسخ نامعتبر است."
        )
        return

    session = (
        quiz_engine.get_active_session(
            user_id
        )
    )

    if session is None:
        await query.answer(
            "⚠️ آزمون فعالی وجود ندارد."
        )

        await show_random_quiz_menu(
            update,
            context,
        )

        return

    question = (
        session.current_question()
    )

    if question is None:
        await query.answer()
        return

    if (
        answer_index < 0
        or answer_index
        >= len(question.options)
    ):
        await query.answer(
            "❌ گزینه نامعتبر است."
        )
        return

    selected_answer = (
        question.options[
            answer_index
        ]
    )

    try:
        result = quiz_engine.submit_answer(
            telegram_id=user_id,
            answer=selected_answer,
        )

        is_correct = bool(
            result.get(
                "is_correct",
                False,
            )
        )

        finished = bool(
            result.get(
                "finished",
                False,
            )
        )

        if is_correct:
            await query.answer(
                "✅ پاسخ صحیح است!",
                show_alert=False,
            )
        else:
            await query.answer(
                "❌ پاسخ اشتباه است.",
                show_alert=False,
            )

        if finished:
            final_result = (
                quiz_engine.get_result(
                    user_id
                )
            )

            if final_result is not None:
                await _show_final_result(
                    update,
                    context,
                    result=final_result.to_dict(),
                    edit_message=True,
                )

            logger.info(
                (
                    "Random Quiz completed: "
                    "telegram_id=%s score=%s"
                ),
                user_id,
                result.get("score"),
            )

            return

        await _show_current_question(
            update,
            context,
            edit_message=True,
        )

    except (
        RuntimeError,
        ValueError,
    ) as exc:

        logger.warning(
            (
                "Random Quiz answer rejected: "
                "telegram_id=%s error=%s"
            ),
            user_id,
            exc,
        )

        await query.answer(
            "❌ امکان ثبت پاسخ وجود ندارد.",
            show_alert=True,
        )

    except Exception:

        logger.exception(
            (
                "Unexpected Random Quiz answer error: "
                "telegram_id=%s"
            ),
            user_id,
        )

        await query.answer(
            "❌ خطایی هنگام ثبت پاسخ رخ داد.",
            show_alert=True,
        )


# ==========================================================
# Cancel Random Quiz
# ==========================================================

async def cancel_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Cancel active Random Quiz.
    """

    query = update.callback_query

    if query is not None:
        await query.answer(
            "❌ آزمون لغو شد."
        )

    user_id = _get_user_id(
        update
    )

    if user_id is None:
        return

    try:
        session = (
            quiz_engine.get_session(
                user_id
            )
        )

        if session is None:
            await show_random_quiz_menu(
                update,
                context,
            )
            return

        if session.status == STATUS_ACTIVE:
            result = quiz_engine.cancel_quiz(
                user_id
            )

        elif session.status in (
            STATUS_COMPLETED,
            STATUS_CANCELLED,
        ):
            result = session.to_result()

        else:
            result = session.to_result()

        await _show_final_result(
            update,
            context,
            result=result.to_dict(),
            edit_message=True,
        )

        logger.info(
            (
                "Random Quiz cancelled: "
                "telegram_id=%s"
            ),
            user_id,
        )

    except Exception:
        logger.exception(
            (
                "Failed to cancel Random Quiz: "
                "telegram_id=%s"
            ),
            user_id,
        )

        if (
            query is not None
            and query.message is not None
        ):
            await query.message.edit_text(
                text=(
                    "❌ خطایی هنگام لغو آزمون رخ داد."
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔙 بازگشت",
                                callback_data="main_menu",
                            )
                        ]
                    ]
                ),
            )


# ==========================================================
# Route Callback
# ==========================================================

async def route_random_quiz_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Central callback router for Random Quiz module.

    Supported callbacks:
    - menu_random_quiz
    - random_quiz
    - random_quiz_start
    - random_quiz_continue
    - random_quiz_restart
    - random_quiz_answer:<index>
    - random_quiz_cancel
    """

    query = update.callback_query

    if query is None:
        return

    callback_data = (
        query.data or ""
    )

    try:

        if callback_data in (
            "menu_random_quiz",
            "random_quiz",
        ):
            await show_random_quiz_menu(
                update,
                context,
            )
            return

        if callback_data == (
            "random_quiz_start"
        ):
            await start_random_quiz(
                update,
                context,
            )
            return

        if callback_data == (
            "random_quiz_continue"
        ):
            await continue_random_quiz(
                update,
                context,
            )
            return

        if callback_data == (
            "random_quiz_restart"
        ):
            await restart_random_quiz(
                update,
                context,
            )
            return

        if callback_data.startswith(
            "random_quiz_answer:"
        ):
            await answer_random_quiz(
                update,
                context,
            )
            return

        if callback_data == (
            "random_quiz_cancel"
        ):
            await cancel_random_quiz(
                update,
                context,
            )
            return

        logger.warning(
            "Unknown Random Quiz callback: %s",
            callback_data,
        )

        await query.answer(
            "❌ عملیات نامعتبر است.",
            show_alert=True,
        )

    except Exception:
        logger.exception(
            (
                "Random Quiz callback router failed: "
                "callback=%s"
            ),
            callback_data,
        )

        try:
            await query.answer(
                "❌ خطایی رخ داد.",
                show_alert=True,
            )
        except Exception:
            pass


# ==========================================================
# Health Check
# ==========================================================

def random_quiz_handlers_health_check() -> bool:
    """
    Validate Random Quiz handlers and their dependencies.
    """

    try:
        if not isinstance(
            RANDOM_QUIZ_CONFIG,
            dict,
        ):
            return False

        questions = (
            get_random_questions()
        )

        if not isinstance(
            questions,
            list,
        ):
            return False

        if len(questions) < 1:
            return False

        for question in questions:

            if not isinstance(
                question,
                dict,
            ):
                return False

            if not question.get(
                "id"
            ):
                return False

            if not question.get(
                "question"
            ):
                return False

            options = question.get(
                "options"
            )

            if not isinstance(
                options,
                list,
            ):
                return False

            if len(options) < 2:
                return False

            if question.get(
                "correct_answer"
            ) not in options:
                return False

        test_engine = QuizEngine()

        test_questions = [
            {
                "id": "random_health_001",
                "question": "Health?",
                "options": [
                    "yes",
                    "no",
                ],
                "correct_answer": "yes",
            }
        ]

        session = (
            test_engine.start_quiz(
                telegram_id=999999999,
                module_id=RANDOM_QUIZ_MODULE_ID,
                chapter_id=RANDOM_QUIZ_CHAPTER_ID,
                lesson_id=RANDOM_QUIZ_LESSON_ID,
                questions=test_questions,
            )
        )

        if (
            session.total_questions()
            != 1
        ):
            return False

        answer_result = (
            test_engine.submit_answer(
                telegram_id=999999999,
                answer="yes",
            )
        )

        if not answer_result.get(
            "is_correct"
        ):
            return False

        result = test_engine.get_result(
            999999999
        )

        if result is None:
            return False

        if result.status != (
            STATUS_COMPLETED
        ):
            return False

        if result.correct_answers != 1:
            return False

        if result.score != 100.0:
            return False

        return True

    except Exception:
        logger.exception(
            "Random Quiz handlers health check failed."
        )
        return False


# ==========================================================
# Backward-compatible aliases
# ==========================================================

show_random_quiz = (
    show_random_quiz_menu
)

random_quiz_start = (
    start_random_quiz
)

random_quiz_answer = (
    answer_random_quiz
)

random_quiz_cancel = (
    cancel_random_quiz
)


# ==========================================================
# Module-level Health Check
# ==========================================================

if __name__ == "__main__":

    print(
        "Random Quiz handlers health:",
        random_quiz_handlers_health_check(),
    )
