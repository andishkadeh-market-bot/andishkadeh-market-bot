"""
International Trade Telegram Handlers

Features:
- International Trade main menu
- Chapter navigation
- Lesson navigation
- Lesson completion
- Interactive 4-option quiz
- Quiz result
- Quiz cancellation
- Progress integration
- Deep Link quiz support

Deep Link format:
https://t.me/andishkadehmarketbot?start=quiz_international_trade_chapter_01_lesson_01_01
"""

from __future__ import annotations

import logging
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.progress import (
    mark_lesson_completed,
    mark_lesson_started,
)

from modules.international_trade.data import (
    MODULE_ID,
    MODULE_TITLE,
    get_chapter,
    get_chapters,
    get_lesson,
    get_lessons,
    get_quiz_questions,
)

from modules.international_trade.service import (
    save_quiz_result,
)


logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

QUIZ_STATE_KEY = "international_trade_quiz"

QUESTIONS_PER_QUIZ = 5


# ==========================================================
# Safe Helpers
# ==========================================================

def _safe_text(
    value: Any,
    default: str = "",
) -> str:
    """
    Safely convert a value to string.
    """

    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def _safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """
    Safely convert a value to int.
    """

    try:
        return int(value)

    except (TypeError, ValueError):
        return default


def _get_user_id(
    update: Update,
) -> int | None:
    """
    Get Telegram user ID safely.
    """

    user = update.effective_user

    if user is None:
        return None

    return user.id


# ==========================================================
# Lesson / Chapter Helpers
# ==========================================================

def _load_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """
    Load one International Trade lesson.

    Supports both direct dictionary return and
    object-like return values.
    """

    try:

        lesson = get_lesson(
            chapter_id,
            lesson_id,
        )

    except Exception:

        logger.exception(
            (
                "Failed to load International Trade lesson: "
                "chapter=%s lesson=%s"
            ),
            chapter_id,
            lesson_id,
        )

        return None

    if lesson is None:
        return None

    if isinstance(
        lesson,
        dict,
    ):

        return lesson

    # ------------------------------------------------------
    # Object fallback
    # ------------------------------------------------------

    result: dict[str, Any] = {}

    for key in (
        "id",
        "lesson_id",
        "title",
        "content",
        "description",
        "example",
        "examples",
        "tips",
        "exam_tips",
        "specialized_tips",
    ):

        if hasattr(
            lesson,
            key,
        ):

            result[key] = getattr(
                lesson,
                key,
            )

    return result or None


def _load_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """
    Load one International Trade chapter.
    """

    try:

        chapter = get_chapter(
            chapter_id
        )

    except Exception:

        logger.exception(
            "Failed to load International Trade chapter: %s",
            chapter_id,
        )

        return None

    if chapter is None:
        return None

    if isinstance(
        chapter,
        dict,
    ):

        return chapter

    result: dict[str, Any] = {}

    for key in (
        "id",
        "chapter_id",
        "title",
        "description",
    ):

        if hasattr(
            chapter,
            key,
        ):

            result[key] = getattr(
                chapter,
                key,
            )

    return result or None


# ==========================================================
# Quiz Helpers
# ==========================================================

def _load_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """
    Load quiz questions for a lesson.
    """

    try:

        questions = get_quiz_questions(
            chapter_id,
            lesson_id,
        )

    except Exception:

        logger.exception(
            (
                "Failed to load quiz questions: "
                "chapter=%s lesson=%s"
            ),
            chapter_id,
            lesson_id,
        )

        return []

    if not isinstance(
        questions,
        list,
    ):

        return []

    normalized: list[
        dict[str, Any]
    ] = []

    for index, question in enumerate(
        questions,
        start=1,
    ):

        if not isinstance(
            question,
            dict,
        ):
            continue

        normalized_question = dict(
            question
        )

        # --------------------------------------------------
        # Normalize question ID
        # --------------------------------------------------

        if not normalized_question.get(
            "id"
        ):

            normalized_question[
                "id"
            ] = (
                f"it_{chapter_id}_"
                f"{lesson_id}_q{index:02d}"
            )

        # --------------------------------------------------
        # Normalize question text
        # --------------------------------------------------

        if not normalized_question.get(
            "question"
        ):

            normalized_question[
                "question"
            ] = normalized_question.get(
                "text",
                "",
            )

        # --------------------------------------------------
        # Normalize options
        # --------------------------------------------------

        options = normalized_question.get(
            "options",
            [],
        )

        normalized_options: list[
            dict[str, str]
        ] = []

        if isinstance(
            options,
            dict,
        ):

            for option_id, option_text in options.items():

                normalized_options.append(
                    {
                        "id": str(
                            option_id
                        ).upper(),
                        "text": _safe_text(
                            option_text
                        ),
                    }
                )

        elif isinstance(
            options,
            list,
        ):

            for option_index, option in enumerate(
                options
            ):

                if isinstance(
                    option,
                    dict,
                ):

                    option_id = (
                        option.get("id")
                        or option.get("key")
                        or chr(
                            65 + option_index
                        )
                    )

                    option_text = (
                        option.get("text")
                        or option.get("title")
                        or option.get("value")
                        or ""
                    )

                    normalized_options.append(
                        {
                            "id": str(
                                option_id
                            ).upper(),
                            "text": _safe_text(
                                option_text
                            ),
                        }
                    )

                else:

                    normalized_options.append(
                        {
                            "id": chr(
                                65 + option_index
                            ),
                            "text": _safe_text(
                                option
                            ),
                        }
                    )

        normalized_question[
            "options"
        ] = normalized_options

        # --------------------------------------------------
        # Normalize answer
        # --------------------------------------------------

        answer = (
            normalized_question.get(
                "answer"
            )
            or normalized_question.get(
                "correct_answer"
            )
        )

        if answer is not None:

            answer = str(
                answer
            ).strip().upper()

            normalized_question[
                "answer"
            ] = answer

            normalized_question[
                "correct_answer"
            ] = answer

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        if not normalized_question.get(
            "explanation"
        ):

            normalized_question[
                "explanation"
            ] = ""

        normalized.append(
            normalized_question
        )

    return normalized


def _question_text(
    question: dict[str, Any],
    question_index: int,
    total_questions: int,
) -> str:
    """
    Build quiz question text.
    """

    text = _safe_text(
        question.get(
            "question"
        ),
        "سؤال بدون متن",
    )

    return (
        f"📝 <b>آزمون تجارت بین‌الملل</b>\n\n"
        f"سؤال {question_index + 1} از "
        f"{total_questions}\n\n"
        f"{text}"
    )


def _question_keyboard(
    chapter_id: str,
    lesson_id: str,
    question_index: int,
    question: dict[str, Any],
) -> InlineKeyboardMarkup:
    """
    Build answer keyboard.
    """

    options = question.get(
        "options",
        [],
    )

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for option in options:

        if not isinstance(
            option,
            dict,
        ):
            continue

        option_id = _safe_text(
            option.get(
                "id"
            )
        ).upper()

        option_text = _safe_text(
            option.get(
                "text"
            )
        )

        if not option_id:
            continue

        callback_data = (
            "trade_quiz_answer:"
            f"{chapter_id}:"
            f"{lesson_id}:"
            f"{question_index}:"
            f"{option_id}"
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{option_id}) "
                        f"{option_text}"
                    ),
                    callback_data=callback_data,
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="❌ لغو آزمون",
                callback_data=(
                    "trade_quiz_cancel:"
                    f"{chapter_id}:"
                    f"{lesson_id}"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================================
# Quiz State
# ==========================================================

def _set_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
    lesson_id: str,
    questions: list[dict[str, Any]],
) -> None:
    """
    Store quiz state in user_data.
    """

    context.user_data[
        QUIZ_STATE_KEY
    ] = {
        "module_id": MODULE_ID,
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "questions": questions,
        "current": 0,
        "correct": 0,
        "answered": 0,
    }


def _get_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
    """
    Get active quiz state.
    """

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
    """
    Clear active quiz.
    """

    context.user_data.pop(
        QUIZ_STATE_KEY,
        None,
    )


# ==========================================================
# Common Quiz Starter
# ==========================================================

async def _start_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
    lesson_id: str,
) -> bool:
    """
    Common quiz-start logic.

    This function is intentionally independent of whether
    the quiz was started from:

    - Telegram callback button
    - Telegram /start Deep Link

    Returns:
        True  -> quiz started
        False -> quiz could not be started
    """

    chapter_id = _safe_text(
        chapter_id
    )

    lesson_id = _safe_text(
        lesson_id
    )

    if not chapter_id or not lesson_id:

        logger.warning(
            "Invalid quiz target."
        )

        return False

    # ------------------------------------------------------
    # Validate lesson
    # ------------------------------------------------------

    lesson = _load_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:

        logger.warning(
            (
                "Quiz requested for missing lesson: "
                "chapter=%s lesson=%s"
            ),
            chapter_id,
            lesson_id,
        )

        target_message = (
            update.message
            if update.message is not None
            else None
        )

        target_query = (
            update.callback_query
            if update.callback_query is not None
            else None
        )

        error_text = (
            "❌ درس موردنظر پیدا نشد.\n\n"
            "لطفاً از فهرست درس‌ها دوباره وارد شوید."
        )

        if target_query is not None:

            await target_query.answer(
                "درس پیدا نشد.",
                show_alert=True,
            )

        elif target_message is not None:

            await target_message.reply_text(
                error_text
            )

        return False

    # ------------------------------------------------------
    # Load questions
    # ------------------------------------------------------

    questions = _load_quiz_questions(
        chapter_id,
        lesson_id,
    )

    if not questions:

        logger.warning(
            (
                "No quiz questions found: "
                "chapter=%s lesson=%s"
            ),
            chapter_id,
            lesson_id,
        )

        target_message = (
            update.message
            if update.message is not None
            else None
        )

        target_query = (
            update.callback_query
            if update.callback_query is not None
            else None
        )

        error_text = (
            "⚠️ برای این درس هنوز سؤال آزمون ثبت نشده است.\n\n"
            "لطفاً درس دیگری را انتخاب کنید."
        )

        if target_query is not None:

            await target_query.answer(
                "برای این درس سؤال آزمون وجود ندارد.",
                show_alert=True,
            )

        elif target_message is not None:

            await target_message.reply_text(
                error_text
            )

        return False

    # ------------------------------------------------------
    # Limit quiz size
    # ------------------------------------------------------

    questions = questions[
        :QUESTIONS_PER_QUIZ
    ]

    # ------------------------------------------------------
    # Mark lesson started
    # ------------------------------------------------------

    user_id = _get_user_id(
        update
    )

    if user_id is not None:

        try:

            mark_lesson_started(
                user_id,
                MODULE_ID,
                chapter_id,
                lesson_id,
            )

        except TypeError:

            # Compatibility with alternate signatures
            try:

                mark_lesson_started(
                    telegram_id=user_id,
                    module_id=MODULE_ID,
                    chapter_id=chapter_id,
                    lesson_id=lesson_id,
                )

            except Exception:

                logger.exception(
                    "Failed to mark International Trade lesson started."
                )

        except Exception:

            logger.exception(
                "Failed to mark International Trade lesson started."
            )

    # ------------------------------------------------------
    # Save quiz state
    # ------------------------------------------------------

    _set_quiz_state(
        context=context,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        questions=questions,
    )

    # ------------------------------------------------------
    # Show first question
    # ------------------------------------------------------

    await _show_trade_quiz_question(
        update,
        context,
    )

    return True


# ==========================================================
# Quiz Start From Callback
# ==========================================================

async def start_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start International Trade quiz from callback button.

    Expected callback:

        trade_quiz:<chapter_id>:<lesson_id>
    """

    query = update.callback_query

    if query is None:

        return

    await query.answer()

    data = _safe_text(
        query.data
    )

    prefix = "trade_quiz:"

    if not data.startswith(
        prefix
    ):

        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 2:

        await query.answer(
            "اطلاعات آزمون نامعتبر است.",
            show_alert=True,
        )

        return

    chapter_id = parts[0]
    lesson_id = parts[1]

    await _start_international_trade_quiz(
        update,
        context,
        chapter_id,
        lesson_id,
    )


# ==========================================================
# Quiz Start From Deep Link
# ==========================================================

async def start_international_trade_quiz_from_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
    lesson_id: str,
) -> None:
    """
    Start International Trade quiz from /start Deep Link.

    Example:

        /start
        quiz_international_trade_chapter_01_lesson_01_01

    Unlike callback-based quiz start, there is no
    callback query here. The first question is therefore
    sent as a new Telegram message.
    """

    if update.message is None:

        logger.warning(
            (
                "Deep Link quiz start called without message: "
                "chapter=%s lesson=%s"
            ),
            chapter_id,
            lesson_id,
        )

        return

    await _start_international_trade_quiz(
        update,
        context,
        chapter_id,
        lesson_id,
    )


# ==========================================================
# Show Quiz Question
# ==========================================================

async def _show_trade_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show current quiz question.

    Supports both:
    - callback query -> edit existing message
    - /start deep link -> send new message
    """

    state = _get_quiz_state(
        context
    )

    if state is None:

        return

    questions = state.get(
        "questions",
        [],
    )

    current = _safe_int(
        state.get(
            "current",
            0,
        )
    )

    chapter_id = _safe_text(
        state.get(
            "chapter_id"
        )
    )

    lesson_id = _safe_text(
        state.get(
            "lesson_id"
        )
    )

    if not questions:

        _clear_quiz_state(
            context
        )

        if update.message is not None:

            await update.message.reply_text(
                "❌ سؤالات آزمون در دسترس نیست."
            )

        return

    # ------------------------------------------------------
    # Quiz completed
    # ------------------------------------------------------

    if current >= len(
        questions
    ):

        await finish_international_trade_quiz(
            update,
            context,
        )

        return

    question = questions[
        current
    ]

    text = _question_text(
        question=question,
        question_index=current,
        total_questions=len(
            questions
        ),
    )

    keyboard = _question_keyboard(
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        question_index=current,
        question=question,
    )

    query = update.callback_query

    # ------------------------------------------------------
    # Callback mode
    # ------------------------------------------------------

    if query is not None:

        try:

            await query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

            return

        except Exception:

            logger.exception(
                "Failed to edit quiz question message."
            )

            with suppress_exceptions():

                await query.message.reply_text(
                    text=text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )

            return

    # ------------------------------------------------------
    # Deep Link / Message mode
    # ------------------------------------------------------

    if update.message is not None:

        await update.message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


# ==========================================================
# Quiz Answer
# ==========================================================

async def answer_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Process an International Trade quiz answer.

    Callback format:

        trade_quiz_answer:
        <chapter_id>:
        <lesson_id>:
        <question_index>:
        <answer>
    """

    query = update.callback_query

    if query is None:

        return

    await query.answer()

    data = _safe_text(
        query.data
    )

    prefix = (
        "trade_quiz_answer:"
    )

    if not data.startswith(
        prefix
    ):

        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 4:

        await query.answer(
            "پاسخ نامعتبر است.",
            show_alert=True,
        )

        return

    chapter_id = parts[0]
    lesson_id = parts[1]

    question_index = _safe_int(
        parts[2],
        default=-1,
    )

    selected_answer = _safe_text(
        parts[3]
    ).upper()

    state = _get_quiz_state(
        context
    )

    if state is None:

        await query.answer(
            "آزمون فعالی وجود ندارد.",
            show_alert=True,
        )

        return

    state_chapter = _safe_text(
        state.get(
            "chapter_id"
        )
    )

    state_lesson = _safe_text(
        state.get(
            "lesson_id"
        )
    )

    if (
        state_chapter != chapter_id
        or state_lesson != lesson_id
    ):

        await query.answer(
            "این آزمون دیگر فعال نیست.",
            show_alert=True,
        )

        return

    current = _safe_int(
        state.get(
            "current",
            0,
        )
    )

    if question_index != current:

        await query.answer(
            "این سؤال قبلاً پاسخ داده شده است.",
            show_alert=True,
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

        await query.answer(
            "اطلاعات آزمون خراب شده است.",
            show_alert=True,
        )

        _clear_quiz_state(
            context
        )

        return

    if current < 0 or current >= len(
        questions
    ):

        await query.answer(
            "شماره سؤال نامعتبر است.",
            show_alert=True,
        )

        return

    question = questions[
        current
    ]

    correct_answer = (
        question.get(
            "correct_answer"
        )
        or question.get(
            "answer"
        )
    )

    correct_answer = _safe_text(
        correct_answer
    ).upper()

    is_correct = (
        selected_answer
        == correct_answer
    )

    if is_correct:

        state[
            "correct"
        ] = (
            _safe_int(
                state.get(
                    "correct",
                    0,
                )
            )
            + 1
        )

    state[
        "answered"
    ] = (
        _safe_int(
            state.get(
                "answered",
                0,
            )
        )
        + 1
    )

    # ------------------------------------------------------
    # Show immediate feedback
    # ------------------------------------------------------

    explanation = _safe_text(
        question.get(
            "explanation"
        )
    )

    if is_correct:

        feedback = (
            "✅ <b>پاسخ صحیح است.</b>"
        )

    else:

        feedback = (
            "❌ <b>پاسخ نادرست است.</b>\n"
            f"پاسخ صحیح: <b>{correct_answer}</b>"
        )

    if explanation:

        feedback += (
            "\n\n"
            f"💡 <b>توضیح:</b>\n"
            f"{explanation}"
        )

    next_index = current + 1

    state[
        "current"
    ] = next_index

    # ------------------------------------------------------
    # If this was the final question
    # ------------------------------------------------------

    if next_index >= len(
        questions
    ):

        try:

            await query.edit_message_text(
                text=feedback,
                parse_mode="HTML",
            )

        except Exception:

            logger.exception(
                "Failed to show final quiz feedback."
            )

        await finish_international_trade_quiz(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Next question button
    # ------------------------------------------------------

    next_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="➡️ سؤال بعدی",
                    callback_data=(
                        "trade_quiz_next:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ لغو آزمون",
                    callback_data=(
                        "trade_quiz_cancel:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
        ]
    )

    try:

        await query.edit_message_text(
            text=feedback,
            reply_markup=next_keyboard,
            parse_mode="HTML",
        )

    except Exception:

        logger.exception(
            "Failed to show quiz feedback."
        )


# ==========================================================
# Show Next Quiz Question
# ==========================================================

async def show_next_trade_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show next question after answer feedback.
    """

    query = update.callback_query

    if query is None:

        return

    await query.answer()

    data = _safe_text(
        query.data
    )

    prefix = "trade_quiz_next:"

    if not data.startswith(
        prefix
    ):

        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 2:

        return

    chapter_id = parts[0]
    lesson_id = parts[1]

    state = _get_quiz_state(
        context
    )

    if state is None:

        await query.answer(
            "آزمون فعال نیست.",
            show_alert=True,
        )

        return

    if (
        _safe_text(
            state.get(
                "chapter_id"
            )
        )
        != chapter_id
    ):

        return

    if (
        _safe_text(
            state.get(
                "lesson_id"
            )
        )
        != lesson_id
    ):

        return

    await _show_trade_quiz_question(
        update,
        context,
    )


# ==========================================================
# Finish Quiz
# ==========================================================

async def finish_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Finish quiz and save result.
    """

    state = _get_quiz_state(
        context
    )

    if state is None:

        return

    chapter_id = _safe_text(
        state.get(
            "chapter_id"
        )
    )

    lesson_id = _safe_text(
        state.get(
            "lesson_id"
        )
    )

    questions = state.get(
        "questions",
        [],
    )

    total = len(
        questions
    )

    correct = _safe_int(
        state.get(
            "correct",
            0,
        )
    )

    answered = _safe_int(
        state.get(
            "answered",
            0,
        )
    )

    user_id = _get_user_id(
        update
    )

    percentage = 0

    if total > 0:

        percentage = round(
            (
                correct
                / total
            )
            * 100
        )

    # ------------------------------------------------------
    # Save result
    # ------------------------------------------------------

    if user_id is not None:

        try:

            save_quiz_result(
                user_id=user_id,
                module_id=MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                score=correct,
                total=total,
                percentage=percentage,
            )

        except TypeError:

            # Compatibility fallback for alternate service
            # signatures.
            try:

                save_quiz_result(
                    user_id,
                    MODULE_ID,
                    chapter_id,
                    lesson_id,
                    correct,
                    total,
                )

            except Exception:

                logger.exception(
                    "Failed to save International Trade quiz result."
                )

        except Exception:

            logger.exception(
                "Failed to save International Trade quiz result."
            )

    # ------------------------------------------------------
    # Mark lesson completed
    # ------------------------------------------------------

    if (
        user_id is not None
        and total > 0
        and correct == total
    ):

        try:

            mark_lesson_completed(
                user_id,
                MODULE_ID,
                chapter_id,
                lesson_id,
            )

        except TypeError:

            try:

                mark_lesson_completed(
                    telegram_id=user_id,
                    module_id=MODULE_ID,
                    chapter_id=chapter_id,
                    lesson_id=lesson_id,
                )

            except Exception:

                logger.exception(
                    "Failed to mark International Trade lesson completed."
                )

        except Exception:

            logger.exception(
                "Failed to mark International Trade lesson completed."
            )

    # ------------------------------------------------------
    # Result message
    # ------------------------------------------------------

    if percentage >= 80:

        level_text = (
            "🏆 عالی! تسلط شما بسیار خوب است."
        )

    elif percentage >= 60:

        level_text = (
            "👍 خوب است، اما مرور دوباره درس مفید خواهد بود."
        )

    elif percentage >= 40:

        level_text = (
            "📚 نیاز به مرور و تمرین بیشتری دارید."
        )

    else:

        level_text = (
            "🔄 پیشنهاد می‌شود درس را دوباره مطالعه کنید."
        )

    result_text = (
        "🎯 <b>نتیجه آزمون تجارت بین‌الملل</b>\n\n"
        f"📖 فصل: <b>{chapter_id}</b>\n"
        f"📘 درس: <b>{lesson_id}</b>\n\n"
        f"✅ پاسخ صحیح: <b>{correct}</b>\n"
        f"📝 تعداد سؤالات: <b>{total}</b>\n"
        f"📊 درصد: <b>{percentage}%</b>\n"
        f"📌 پاسخ داده‌شده: <b>{answered}</b>\n\n"
        f"{level_text}"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📚 بازگشت به فصل",
                    callback_data=(
                        f"trade_chapter:{chapter_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 تجارت بین‌الملل",
                    callback_data=(
                        "menu_international_trade"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 منوی اصلی",
                    callback_data="menu_main",
                )
            ],
        ]
    )

    query = update.callback_query

    if query is not None:

        try:

            await query.edit_message_text(
                text=result_text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

        except Exception:

            logger.exception(
                "Failed to edit quiz result message."
            )

            if query.message is not None:

                await query.message.reply_text(
                    text=result_text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )

    elif update.message is not None:

        await update.message.reply_text(
            text=result_text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    _clear_quiz_state(
        context
    )


# ==========================================================
# Cancel Quiz
# ==========================================================

async def cancel_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Cancel active International Trade quiz.
    """

    query = update.callback_query

    if query is None:

        return

    await query.answer()

    data = _safe_text(
        query.data
    )

    prefix = (
        "trade_quiz_cancel:"
    )

    if not data.startswith(
        prefix
    ):

        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 2:

        return

    chapter_id = parts[0]
    lesson_id = parts[1]

    state = _get_quiz_state(
        context
    )

    if state is not None:

        if (
            _safe_text(
                state.get(
                    "chapter_id"
                )
            )
            == chapter_id
            and
            _safe_text(
                state.get(
                    "lesson_id"
                )
            )
            == lesson_id
        ):

            _clear_quiz_state(
                context
            )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📖 بازگشت به درس",
                    callback_data=(
                        f"trade_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 بازگشت به فصل",
                    callback_data=(
                        f"trade_chapter:"
                        f"{chapter_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 منوی اصلی",
                    callback_data="menu_main",
                )
            ],
        ]
    )

    text = (
        "❌ <b>آزمون لغو شد.</b>\n\n"
        "پیشرفت فعلی آزمون ثبت نشد."
    )

    try:

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    except Exception:

        logger.exception(
            "Failed to edit quiz cancellation message."
        )


# ==========================================================
# International Trade Main Menu
# ==========================================================

async def show_international_trade_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show International Trade module menu.
    """

    query = update.callback_query

    if query is not None:

        await query.answer()

    chapters = get_chapters()

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for chapter in chapters:

        if not isinstance(
            chapter,
            dict,
        ):
            continue

        chapter_id = (
            chapter.get("id")
            or chapter.get("chapter_id")
        )

        title = (
            chapter.get("title")
            or chapter.get("name")
            or chapter_id
        )

        if not chapter_id:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📚 {title}",
                    callback_data=(
                        f"trade_chapter:{chapter_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🏠 منوی اصلی",
                callback_data="menu_main",
            )
        ]
    )

    text = (
        "🌍 <b>تجارت بین‌الملل</b>\n\n"
        "مسیر آموزشی تجارت بین‌الملل را انتخاب کنید:"
    )

    markup = InlineKeyboardMarkup(
        keyboard
    )

    if query is not None:

        try:

            await query.edit_message_text(
                text=text,
                reply_markup=markup,
                parse_mode="HTML",
            )

        except Exception:

            logger.exception(
                "Failed to edit International Trade menu."
            )

    elif update.message is not None:

        await update.message.reply_text(
            text=text,
            reply_markup=markup,
            parse_mode="HTML",
        )


# ==========================================================
# Show Chapter
# ==========================================================

async def show_international_trade_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str | None = None,
) -> None:
    """
    Show lessons of a chapter.
    """

    query = update.callback_query

    if query is not None:

        await query.answer()

        data = _safe_text(
            query.data
        )

        if data.startswith(
            "trade_chapter:"
        ):

            chapter_id = data[
                len("trade_chapter:"):
            ]

    if not chapter_id:

        return

    chapter = _load_chapter(
        chapter_id
    )

    if chapter is None:

        if query is not None:

            await query.answer(
                "فصل پیدا نشد.",
                show_alert=True,
            )

        return

    chapter_title = (
        chapter.get(
            "title"
        )
        or chapter.get(
            "name"
        )
        or chapter_id
    )

    lessons = get_lessons(
        chapter_id
    )

    keyboard: list[
        list[InlineKeyboardButton]
    ] = []

    for lesson in lessons:

        if not isinstance(
            lesson,
            dict,
        ):
            continue

        lesson_id = (
            lesson.get("id")
            or lesson.get("lesson_id")
        )

        lesson_title = (
            lesson.get("title")
            or lesson.get("name")
            or lesson_id
        )

        if not lesson_id:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📖 {lesson_title}",
                    callback_data=(
                        f"trade_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ تجارت بین‌الملل",
                callback_data=(
                    "menu_international_trade"
                ),
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🏠 منوی اصلی",
                callback_data="menu_main",
            )
        ]
    )

    text = (
        "📚 <b>"
        f"{chapter_title}"
        "</b>\n\n"
        "درس موردنظر را انتخاب کنید:"
    )

    markup = InlineKeyboardMarkup(
        keyboard
    )

    if query is not None:

        try:

            await query.edit_message_text(
                text=text,
                reply_markup=markup,
                parse_mode="HTML",
            )

        except Exception:

            logger.exception(
                "Failed to show International Trade chapter."
            )

    elif update.message is not None:

        await update.message.reply_text(
            text=text,
            reply_markup=markup,
            parse_mode="HTML",
        )


# ==========================================================
# Show Lesson
# ==========================================================

async def show_international_trade_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show lesson content.
    """

    query = update.callback_query

    if query is None:

        return

    await query.answer()

    data = _safe_text(
        query.data
    )

    prefix = "trade_lesson:"

    if not data.startswith(
        prefix
    ):

        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 2:

        return

    chapter_id = parts[0]
    lesson_id = parts[1]

    lesson = _load_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:

        await query.answer(
            "درس پیدا نشد.",
            show_alert=True,
        )

        return

    title = (
        lesson.get(
            "title"
        )
        or lesson.get(
            "name"
        )
        or lesson_id
    )

    content = (
        lesson.get(
            "content"
        )
        or lesson.get(
            "text"
        )
        or lesson.get(
            "description"
        )
        or ""
    )

    example = (
        lesson.get(
            "example"
        )
        or ""
    )

    exam_tips = (
        lesson.get(
            "exam_tips"
        )
        or lesson.get(
            "specialized_tips"
        )
        or lesson.get(
            "tips"
        )
        or ""
    )

    text_parts = [
        f"📖 <b>{title}</b>",
    ]

    if content:

        text_parts.append(
            f"\n{content}"
        )

    if example:

        text_parts.append(
            "\n\n💡 <b>مثال:</b>\n"
            f"{example}"
        )

    if exam_tips:

        text_parts.append(
            "\n\n🎯 <b>نکات آزمونی:</b>\n"
            f"{exam_tips}"
        )

    text = "".join(
        text_parts
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📝 شروع آزمون این درس",
                    callback_data=(
                        f"trade_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ بازگشت به فصل",
                    callback_data=(
                        f"trade_chapter:"
                        f"{chapter_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌍 تجارت بین‌الملل",
                    callback_data=(
                        "menu_international_trade"
                    ),
                )
            ],
        ]
    )

    try:

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    except Exception:

        logger.exception(
            "Failed to show International Trade lesson."
        )


# ==========================================================
# Complete Lesson
# ==========================================================

async def complete_international_trade_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Mark lesson as completed manually.
    """

    query = update.callback_query

    if query is None:

        return

    await query.answer()

    data = _safe_text(
        query.data
    )

    prefix = (
        "trade_complete:"
    )

    if not data.startswith(
        prefix
    ):

        return

    payload = data[
        len(prefix):
    ]

    parts = payload.split(
        ":"
    )

    if len(parts) != 2:

        return

    chapter_id = parts[0]
    lesson_id = parts[1]

    user_id = _get_user_id(
        update
    )

    if user_id is not None:

        try:

            mark_lesson_completed(
                user_id,
                MODULE_ID,
                chapter_id,
                lesson_id,
            )

        except TypeError:

            try:

                mark_lesson_completed(
                    telegram_id=user_id,
                    module_id=MODULE_ID,
                    chapter_id=chapter_id,
                    lesson_id=lesson_id,
                )

            except Exception:

                logger.exception(
                    "Failed to complete International Trade lesson."
                )

        except Exception:

            logger.exception(
                "Failed to complete International Trade lesson."
            )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📝 آزمون این درس",
                    callback_data=(
                        f"trade_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ بازگشت به فصل",
                    callback_data=(
                        f"trade_chapter:"
                        f"{chapter_id}"
                    ),
                )
            ],
        ]
    )

    text = (
        "✅ <b>درس با موفقیت تکمیل شد.</b>\n\n"
        "پیشرفت شما ثبت شد.\n\n"
        "حالا می‌توانید در آزمون این درس شرکت کنید."
    )

    try:

        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    except Exception:

        logger.exception(
            "Failed to show lesson completion message."
        )


# ==========================================================
# Callback Router
# ==========================================================

async def route_international_trade_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Central International Trade callback router.
    """

    query = update.callback_query

    if query is None:

        return

    data = _safe_text(
        query.data
    )

    logger.info(
        "International Trade callback: %s",
        data,
    )

    # ------------------------------------------------------
    # Main Menu
    # ------------------------------------------------------

    if data in (
        "menu_international_trade",
        "menu_trade",
    ):

        await show_international_trade_menu(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Chapter
    # ------------------------------------------------------

    if data.startswith(
        "trade_chapter:"
    ):

        await show_international_trade_chapter(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Lesson
    # ------------------------------------------------------

    if data.startswith(
        "trade_lesson:"
    ):

        await show_international_trade_lesson(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Complete Lesson
    # ------------------------------------------------------

    if data.startswith(
        "trade_complete:"
    ):

        await complete_international_trade_lesson(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Quiz Start
    # ------------------------------------------------------

    if data.startswith(
        "trade_quiz:"
    ):

        await start_international_trade_quiz(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Quiz Answer
    # ------------------------------------------------------

    if data.startswith(
        "trade_quiz_answer:"
    ):

        await answer_international_trade_quiz(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Next Question
    # ------------------------------------------------------

    if data.startswith(
        "trade_quiz_next:"
    ):

        await show_next_trade_quiz_question(
            update,
            context,
        )

        return

    # ------------------------------------------------------
    # Quiz Cancel
    # ------------------------------------------------------

    if data.startswith(
        "trade_quiz_cancel:"
    ):

        await cancel_international_trade_quiz(
            update,
            context,
        )

        return

    logger.warning(
        "Unhandled International Trade callback: %s",
        data,
    )

    await query.answer(
        "دستور ناشناخته است.",
        show_alert=True,
    )


# ==========================================================
# Health Check
# ==========================================================

def international_trade_handlers_health_check() -> bool:
    """
    Verify International Trade handlers.
    """

    required_handlers = (
        route_international_trade_callback,
        start_international_trade_quiz,
        start_international_trade_quiz_from_start,
        answer_international_trade_quiz,
        cancel_international_trade_quiz,
        finish_international_trade_quiz,
        show_international_trade_menu,
        show_international_trade_chapter,
        show_international_trade_lesson,
        complete_international_trade_lesson,
    )

    for handler in required_handlers:

        if not callable(
            handler
        ):

            logger.error(
                "International Trade handler is not callable: %r",
                handler,
            )

            return False

    try:

        chapters = get_chapters()

        if not isinstance(
            chapters,
            list,
        ):

            logger.error(
                "International Trade chapters are invalid."
            )

            return False

        if len(chapters) < 1:

            logger.error(
                "International Trade contains no chapters."
            )

            return False

    except Exception:

        logger.exception(
            "International Trade handler health check failed."
        )

        return False

    logger.info(
        "International Trade handlers health check: OK"
    )

    return True


# ==========================================================
# Compatibility Alias
# ==========================================================

# Some parts of the project may use shorter function names.
# Keep aliases to avoid breaking existing imports.

show_trade_menu = (
    show_international_trade_menu
)

show_trade_chapter = (
    show_international_trade_chapter
)

show_trade_lesson = (
    show_international_trade_lesson
)

complete_trade_lesson = (
    complete_international_trade_lesson
)


# ==========================================================
# Simple Context Manager Helper
# ==========================================================

class suppress_exceptions:
    """
    Small local context manager used only for UI fallback
    operations where the original Telegram message may no
    longer be editable.
    """

    def __enter__(
        self,
    ):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return True


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "start_international_trade_quiz",
    "start_international_trade_quiz_from_start",
    "answer_international_trade_quiz",
    "cancel_international_trade_quiz",
    "finish_international_trade_quiz",
    "show_next_trade_quiz_question",
    "show_international_trade_menu",
    "show_international_trade_chapter",
    "show_international_trade_lesson",
    "complete_international_trade_lesson",
    "route_international_trade_callback",
    "international_trade_handlers_health_check",
    "show_trade_menu",
    "show_trade_chapter",
    "show_trade_lesson",
    "complete_trade_lesson",
]
