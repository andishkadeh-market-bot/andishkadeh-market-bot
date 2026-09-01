"""
Telegram handlers for the Random Quiz module.
Andishkadeh Management & Market
Features:
- Random quiz start
- Random question selection
- Central QuizEngine integration
- Statistics integration
- Progress integration
- Safe quiz cancellation
- Quiz completion
- Multi-user isolation
This handler uses the central QuizEngine instance.
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
    global_quiz_engine,
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
# Keyboards
# ==========================================================
def random_quiz_start_keyboard() -> InlineKeyboardMarkup:
    """Return Random Quiz start keyboard."""
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
# ==========================================================
# Question helpers
# ==========================================================
def _question_text(
    question: dict[str, Any],
) -> str:
    """Extract question text."""
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
    """Extract question options."""
    options = question.get(
        "options",
        [],
    )
    if not isinstance(
        options,
        list,
    ):
        return []
    return options
def _question_answer(
    question: dict[str, Any],
) -> Any:
    """Extract correct answer."""
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
    """Convert an option to display text."""
    if isinstance(
        option,
        dict,
    ):
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
) -> str:
    """Convert an option to its comparable value."""
    if isinstance(
        option,
        dict,
    ):
        if "value" in option:
            return str(option["value"])
        if "id" in option:
            return str(option["id"])
        if "text" in option:
            return str(option["text"])
        if "label" in option:
            return str(option["label"])
    return str(option)
# ==========================================================
# Question pool
# ==========================================================
def get_random_question_pool() -> list[dict[str, Any]]:
    """
    Return valid Random Quiz questions.
    """
    if not isinstance(
        RANDOM_QUESTIONS,
        list,
    ):
        return []
    valid_questions: list[
        dict[str, Any]
    ] = []
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
        answer_text = str(answer)
        option_values = [
            _option_value(option)
            for option in options
        ]
        if answer_text not in option_values:
            continue
        valid_questions.append(
            question
        )
    return valid_questions
# ==========================================================
# Random question selection
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
# Display question
# ==========================================================
async def _show_current_question(
    update: Update,
    telegram_id: int,
) -> None:
    """
    Display the current question from the central engine.
    """
    query = update.callback_query
    if query is None:
        return
    session = (
        global_quiz_engine.get_active_session(
            telegram_id
        )
    )
    if session is None:
        await query.edit_message_text(
            "⚠️ آزمون فعالی برای شما پیدا نشد.",
            reply_markup=random_quiz_start_keyboard(),
        )
        return
    question = (
        global_quiz_engine.get_current_question(
            telegram_id
        )
    )
    if question is None:
        await finish_random_quiz(
            update,
            telegram_id,
        )
        return
    question_number = (
        session.current_index + 1
    )
    total_questions = (
        session.total_questions()
    )
    keyboard: list[
        list[InlineKeyboardButton]
    ] = []
    for index, option in enumerate(
        question.options
    ):
        keyboard.append(
            [
                InlineKeyboardButton(
                    str(option),
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
    text = (
        "🎲 <b>آزمون سوالات تصادفی</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"❓ سوال <b>{question_number}</b> "
        f"از <b>{total_questions}</b>\n\n"
        f"<b>{question.question}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "پاسخ خود را انتخاب کنید:"
    )
    await query.edit_message_text(
        text,
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
    Start a new Random Quiz using the central QuizEngine.
    """
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    user = update.effective_user
    if user is None:
        return
    telegram_id = user.id
    # ------------------------------------------------------
    # Select random questions
    # ------------------------------------------------------
    questions = select_random_questions()
    if not questions:
        await query.edit_message_text(
            "❌ در حال حاضر سوال معتبری برای "
            "آزمون تصادفی ثبت نشده است.",
            reply_markup=random_quiz_start_keyboard(),
        )
        return
    # ------------------------------------------------------
    # Start central engine session
    # ------------------------------------------------------
    try:
        session = (
            global_quiz_engine.start_quiz(
                telegram_id=telegram_id,
                module_id=RANDOM_QUIZ_MODULE_ID,
                chapter_id=RANDOM_QUIZ_CHAPTER_ID,
                lesson_id=RANDOM_QUIZ_LESSON_ID,
                questions=questions,
                replace_existing=True,
            )
        )
    except Exception:
        logger.exception(
            "Failed to start Random Quiz: telegram_id=%s",
            telegram_id,
        )
        await query.edit_message_text(
            "❌ خطایی هنگام شروع آزمون رخ داد.\n"
            "لطفاً دوباره تلاش کنید.",
            reply_markup=random_quiz_start_keyboard(),
        )
        return
    logger.info(
        "Random Quiz started: telegram_id=%s questions=%s",
        telegram_id,
        session.total_questions(),
    )
    await _show_current_question(
        update,
        telegram_id,
    )
# ==========================================================
# Answer quiz
# ==========================================================
async def answer_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Process one Random Quiz answer through central QuizEngine.
    """
    query = update.callback_query
    if query is None:
        return
    user = update.effective_user
    if user is None:
        return
    telegram_id = user.id
    await query.answer()
    # ------------------------------------------------------
    # Validate active session
    # ------------------------------------------------------
    session = (
        global_quiz_engine.get_active_session(
            telegram_id
        )
    )
    if session is None:
        await query.edit_message_text(
            "⚠️ آزمون فعالی برای شما پیدا نشد.",
            reply_markup=random_quiz_start_keyboard(),
        )
        return
    # ------------------------------------------------------
    # Parse callback
    # ------------------------------------------------------
    data = query.data or ""
    try:
        parts = data.split(":")
        if len(parts) != 3:
            raise ValueError
        answer_index = int(
            parts[2]
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
    # ------------------------------------------------------
    # Current question
    # ------------------------------------------------------
    current_question = (
        global_quiz_engine.get_current_question(
            telegram_id
        )
    )
    if current_question is None:
        await query.answer(
            "⚠️ این آزمون دیگر فعال نیست.",
            show_alert=True,
        )
        return
    options = list(
        current_question.options
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
    selected_answer = str(
        options[answer_index]
    )
    # ------------------------------------------------------
    # Submit answer
    # ------------------------------------------------------
    try:
        result = (
            global_quiz_engine.submit_answer(
                telegram_id=telegram_id,
                answer=selected_answer,
            )
        )
    except ValueError:
        await query.answer(
            "❌ پاسخ انتخاب‌شده معتبر نیست.",
            show_alert=True,
        )
        return
    except Exception:
        logger.exception(
            "Failed to submit Random Quiz answer: "
            "telegram_id=%s",
            telegram_id,
        )
        await query.answer(
            "❌ خطایی هنگام ثبت پاسخ رخ داد.",
            show_alert=True,
        )
        return
    # ------------------------------------------------------
    # Answer feedback
    # ------------------------------------------------------
    if result.get("is_correct"):
        feedback = "✅ پاسخ شما صحیح بود."
    else:
        feedback = (
            "❌ پاسخ شما اشتباه بود.\n"
            f"پاسخ صحیح: "
            f"<b>{result.get('correct_answer')}</b>"
        )
    explanation = result.get(
        "explanation"
    )
    if explanation:
        feedback += (
            f"\n\n💡 <b>توضیح:</b>\n"
            f"{explanation}"
        )
    # ------------------------------------------------------
    # Finished
    # ------------------------------------------------------
    if result.get("finished"):
        await query.answer(
            feedback.replace(
                "<b>",
                "",
            ).replace(
                "</b>",
                "",
            )[:200],
            show_alert=True,
        )
        await finish_random_quiz(
            update,
            telegram_id,
        )
        return
    # ------------------------------------------------------
    # Next question
    # ------------------------------------------------------
    await query.answer(
        feedback.replace(
            "<b>",
            "",
        ).replace(
            "</b>",
            "",
        )[:200],
        show_alert=True,
    )
    await _show_current_question(
        update,
        telegram_id,
    )
# ==========================================================
# Finish quiz
# ==========================================================
async def finish_random_quiz(
    update: Update,
    telegram_id: int,
) -> None:
    """
    Complete quiz and persist Statistics + Progress.
    """
    query = update.callback_query
    if query is None:
        return
    result = (
        global_quiz_engine.get_result(
            telegram_id
        )
    )
    if result is None:
        await query.edit_message_text(
            "⚠️ نتیجه آزمون پیدا نشد.",
            reply_markup=random_quiz_start_keyboard(),
        )
        return
    total_questions = (
        result.total_questions
    )
    correct_answers = (
        result.correct_answers
    )
    score = result.score
    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------
    if result.status == "completed":
        try:
            record_quiz_result(
                telegram_id=telegram_id,
                module_id=RANDOM_QUIZ_MODULE_ID,
                chapter_id=RANDOM_QUIZ_CHAPTER_ID,
                lesson_id=RANDOM_QUIZ_LESSON_ID,
                total_questions=total_questions,
                correct_answers=correct_answers,
                score=score,
            )
        except Exception:
            logger.exception(
                "Failed to record Random Quiz statistics: "
                "telegram_id=%s",
                telegram_id,
            )
        # --------------------------------------------------
        # Progress
        # --------------------------------------------------
        try:
            mark_lesson_completed(
                telegram_id=telegram_id,
                module_id=RANDOM_QUIZ_MODULE_ID,
                chapter_id=RANDOM_QUIZ_CHAPTER_ID,
                lesson_id=RANDOM_QUIZ_LESSON_ID,
            )
        except Exception:
            logger.exception(
                "Failed to record Random Quiz progress: "
                "telegram_id=%s",
                telegram_id,
            )
    # ------------------------------------------------------
    # Level
    # ------------------------------------------------------
    if score >= 90:
        level = "🏆 عالی"
    elif score >= 75:
        level = "🟢 خیلی خوب"
    elif score >= 50:
        level = "🟡 قابل قبول"
    else:
        level = "🔴 نیاز به مرور"
    wrong_answers = (
        result.wrong_answers
    )
    # ------------------------------------------------------
    # Result message
    # ------------------------------------------------------
    text = (
        "🎲 <b>آزمون تصادفی به پایان رسید</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📝 تعداد سوالات: "
        f"<b>{total_questions}</b>\n"
        f"✅ پاسخ صحیح: "
        f"<b>{correct_answers}</b>\n"
        f"❌ پاسخ غلط: "
        f"<b>{wrong_answers}</b>\n"
        f"📊 نمره: "
        f"<b>{score:.2f}%</b>\n"
        f"🎯 وضعیت: "
        f"<b>{level}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "نتیجه آزمون در Statistics ثبت شد "
        "و Progress نیز به‌روزرسانی شد."
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=random_quiz_result_keyboard(),
    )
    logger.info(
        "Random Quiz completed: telegram_id=%s "
        "score=%.2f correct=%s total=%s",
        telegram_id,
        score,
        correct_answers,
        total_questions,
    )
    # ------------------------------------------------------
    # Remove completed runtime session
    # ------------------------------------------------------
    global_quiz_engine.remove_session(
        telegram_id
    )
# ==========================================================
# Cancel quiz
# ==========================================================
async def cancel_random_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Cancel the active Random Quiz.
    Cancelled quizzes are not recorded as completed
    attempts and do not mark the lesson completed.
    """
    query = update.callback_query
    if query is None:
        return
    user = update.effective_user
    if user is None:
        return
    telegram_id = user.id
    await query.answer(
        "آزمون لغو شد.",
        show_alert=False,
    )
    session = (
        global_quiz_engine.get_active_session(
            telegram_id
        )
    )
    if session is not None:
        try:
            global_quiz_engine.cancel_quiz(
                telegram_id
            )
        except Exception:
            logger.exception(
                "Failed to cancel Random Quiz: "
                "telegram_id=%s",
                telegram_id,
            )
    global_quiz_engine.remove_session(
        telegram_id
    )
    await query.edit_message_text(
        "❌ <b>آزمون تصادفی لغو شد.</b>\n\n"
        "هیچ نتیجه‌ای برای این آزمون در "
        "Statistics ثبت نشد.",
        parse_mode="HTML",
        reply_markup=random_quiz_start_keyboard(),
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
        f"📚 تعداد سوالات موجود: "
        f"<b>{pool_size}</b>\n"
        f"📝 تعداد سوالات آزمون: "
        f"<b>{DEFAULT_QUESTION_COUNT}</b>\n\n"
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
    Basic health check for Random Quiz handlers.
    """
    try:
        pool = get_random_question_pool()
        if not isinstance(
            pool,
            list,
        ):
            return False
        if not pool:
            return False
        if not global_quiz_engine.health_check():
            return False
        return True
    except Exception:
        logger.exception(
            "Random Quiz handlers health check failed."
        )
        return False
