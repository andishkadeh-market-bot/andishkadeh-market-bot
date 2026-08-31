“”“Telegram handlers for the General Exam module.

Andishkadeh Management & Market

Features:

* Start general exam
* Display questions
* Receive answers
* Show immediate answer feedback
* Save quiz statistics
* Update lesson progress
* Cancel an active exam
* Safe navigation back to main menu
    “””

from future import annotations

import html
import logging
from typing import Any

from telegram import (
InlineKeyboardButton,
InlineKeyboardMarkup,
Update,
)
from telegram.ext import ContextTypes

from core.keyboards import main_menu_keyboard

from modules.exam.service import (
create_exam_session,
get_current_question,
submit_answer,
cancel_exam,
)

==========================================================

Logging

==========================================================

logger = logging.getLogger(name)

==========================================================

Constants

==========================================================

EXAM_SESSION_KEY = “general_exam_session”

CALLBACK_START = “exam_general_start”
CALLBACK_CANCEL = “exam_general_cancel”
CALLBACK_ANSWER_PREFIX = “exam_general_answer:”

==========================================================

Keyboards

==========================================================

def exam_start_keyboard() -> InlineKeyboardMarkup:
“”“Return the general exam start keyboard.”””

return InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "▶️ شروع آزمون",
                callback_data=CALLBACK_START,
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

def exam_question_keyboard(
question: dict[str, Any],
) -> InlineKeyboardMarkup:
“”“Build answer buttons for one question.”””

options = question.get("options", [])
keyboard: list[list[InlineKeyboardButton]] = []
option_labels = [
    "الف",
    "ب",
    "ج",
    "د",
]
for index, option in enumerate(options):
    if index >= len(option_labels):
        break
    keyboard.append(
        [
            InlineKeyboardButton(
                f"{option_labels[index]}) {option}",
                callback_data=(
                    f"{CALLBACK_ANSWER_PREFIX}"
                    f"{index}"
                ),
            )
        ]
    )
keyboard.append(
    [
        InlineKeyboardButton(
            "❌ لغو آزمون",
            callback_data=CALLBACK_CANCEL,
        )
    ]
)
return InlineKeyboardMarkup(
    keyboard
)

def exam_result_keyboard() -> InlineKeyboardMarkup:
“”“Return keyboard displayed after exam completion.”””

return InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "🔁 آزمون مجدد",
                callback_data=CALLBACK_START,
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

==========================================================

Text helpers

==========================================================

def format_question(
session: dict[str, Any],
question: dict[str, Any],
) -> str:
“”“Format the current exam question.”””

questions = session.get(
    "questions",
    [],
)
current_index = int(
    session.get(
        "current_index",
        0,
    )
)
total_questions = len(
    questions
)
question_number = current_index + 1
question_text = html.escape(
    str(
        question.get(
            "question",
            "",
        )
    )
)
return (
    "📝 <b>آزمون عمومی</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    f"❓ سؤال <b>{question_number}</b> "
    f"از <b>{total_questions}</b>\n\n"
    f"<b>{question_text}</b>\n\n"
    "یکی از گزینه‌ها را انتخاب کنید:"
)

def format_result(
result: dict[str, Any],
) -> str:
“”“Format the final exam result.”””

score = float(
    result.get(
        "score",
        0,
    )
)
correct = int(
    result.get(
        "correct_answers",
        0,
    )
)
wrong = int(
    result.get(
        "wrong_answers",
        0,
    )
)
total = int(
    result.get(
        "total_questions",
        0,
    )
)
passed = bool(
    result.get(
        "passed",
        False,
    )
)
if passed:
    status = "🎉 <b>قبول شدید</b>"
else:
    status = "📚 <b>نیاز به مرور و تمرین بیشتر دارید</b>"
return (
    "🏁 <b>آزمون عمومی به پایان رسید</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    f"📊 نمره: <b>{score:.2f}%</b>\n"
    f"❓ تعداد سوال: <b>{total}</b>\n"
    f"✅ پاسخ صحیح: <b>{correct}</b>\n"
    f"❌ پاسخ غلط: <b>{wrong}</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    f"{status}\n\n"
    "نتیجه آزمون در آمار کاربر ثبت شد."
)

==========================================================

Start screen

==========================================================

async def show_general_exam(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show the general exam introduction screen.”””

query = update.callback_query
if query is not None:
    await query.answer()
    await query.edit_message_text(
        "📝 <b>آزمون عمومی</b>\n\n"
        "در این بخش می‌توانید در آزمون عمومی "
        "اندیشکده شرکت کنید.\n\n"
        "📊 نتیجه آزمون پس از پایان ثبت می‌شود.\n"
        "📚 شروع و تکمیل آزمون نیز در Progress ثبت خواهد شد.\n\n"
        "برای شروع روی دکمه زیر بزنید:",
        parse_mode="HTML",
        reply_markup=exam_start_keyboard(),
    )
    return
if update.message is not None:
    await update.message.reply_text(
        "📝 <b>آزمون عمومی</b>\n\n"
        "برای شروع آزمون روی دکمه زیر بزنید:",
        parse_mode="HTML",
        reply_markup=exam_start_keyboard(),
    )

==========================================================

Start exam

==========================================================

async def start_general_exam(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Create and start a new general exam session.”””

query = update.callback_query
if query is None:
    return
await query.answer()
user = update.effective_user
if user is None:
    await query.edit_message_text(
        "❌ اطلاعات کاربر قابل دریافت نیست.",
        reply_markup=exam_start_keyboard(),
    )
    return
try:
    session = create_exam_session(
        telegram_id=user.id,
    )
    context.user_data[
        EXAM_SESSION_KEY
    ] = session
    question = get_current_question(
        session
    )
    if question is None:
        context.user_data.pop(
            EXAM_SESSION_KEY,
            None,
        )
        await query.edit_message_text(
            "❌ آزمون در حال حاضر سوالی ندارد.",
            reply_markup=exam_start_keyboard(),
        )
        return
    await query.edit_message_text(
        format_question(
            session,
            question,
        ),
        parse_mode="HTML",
        reply_markup=exam_question_keyboard(
            question
        ),
    )
except Exception:
    logger.exception(
        "Failed to start general exam for user %s.",
        user.id,
    )
    context.user_data.pop(
        EXAM_SESSION_KEY,
        None,
    )
    await query.edit_message_text(
        "❌ خطایی هنگام شروع آزمون رخ داد.\n"
        "لطفاً دوباره تلاش کنید.",
        reply_markup=exam_start_keyboard(),
    )

==========================================================

Answer

==========================================================

async def answer_general_exam(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Process an answer submitted by the user.”””

query = update.callback_query
if query is None:
    return
await query.answer()
session = context.user_data.get(
    EXAM_SESSION_KEY
)
if not isinstance(session, dict):
    await query.edit_message_text(
        "⚠️ آزمون فعالی پیدا نشد.\n\n"
        "برای شروع دوباره آزمون را انتخاب کنید.",
        reply_markup=exam_start_keyboard(),
    )
    return
data = query.data or ""
if not data.startswith(
    CALLBACK_ANSWER_PREFIX
):
    return
raw_index = data[
    len(CALLBACK_ANSWER_PREFIX):
]
try:
    answer_index = int(
        raw_index
    )
except ValueError:
    await query.answer(
        "❌ پاسخ نامعتبر است.",
        show_alert=True,
    )
    return
try:
    result = submit_answer(
        session=session,
        answer_index=answer_index,
    )
    if result.get("finished"):
        final_result = result.get(
            "result"
        )
        if not isinstance(
            final_result,
            dict,
        ):
            raise ValueError(
                "Exam result was not returned."
            )
        context.user_data.pop(
            EXAM_SESSION_KEY,
            None,
        )
        await query.edit_message_text(
            format_result(
                final_result
            ),
            parse_mode="HTML",
            reply_markup=exam_result_keyboard(),
        )
        return
    next_question = get_current_question(
        session
    )
    if next_question is None:
        raise ValueError(
            "Next exam question was not found."
        )
    await query.edit_message_text(
        format_question(
            session,
            next_question,
        ),
        parse_mode="HTML",
        reply_markup=exam_question_keyboard(
            next_question
        ),
    )
except ValueError as exc:
    logger.warning(
        "Invalid general exam answer: %s",
        exc,
    )
    await query.answer(
        "❌ پاسخ قابل پردازش نیست.",
        show_alert=True,
    )
except Exception:
    logger.exception(
        "Failed to process general exam answer."
    )
    context.user_data.pop(
        EXAM_SESSION_KEY,
        None,
    )
    await query.edit_message_text(
        "❌ خطایی هنگام ثبت پاسخ رخ داد.\n"
        "آزمون متوقف شد.",
        reply_markup=exam_start_keyboard(),
    )

==========================================================

Cancel

==========================================================

async def cancel_general_exam(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Cancel the current general exam.”””

query = update.callback_query
if query is None:
    return
await query.answer()
session = context.user_data.get(
    EXAM_SESSION_KEY
)
if isinstance(session, dict):
    cancel_exam(
        session
    )
context.user_data.pop(
    EXAM_SESSION_KEY,
    None,
)
await query.edit_message_text(
    "❌ <b>آزمون لغو شد.</b>\n\n"
    "نتیجه‌ای برای آزمون لغوشده ثبت نمی‌شود.",
    parse_mode="HTML",
    reply_markup=exam_start_keyboard(),
)

==========================================================

Callback router

==========================================================

async def route_exam_callback(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“””
Route callbacks belonging to the General Exam module.

This router should run before a generic callback fallback.
"""
query = update.callback_query
if query is None:
    return
data = query.data or ""
if data == CALLBACK_START:
    await start_general_exam(
        update,
        context,
    )
    return
if data.startswith(
    CALLBACK_ANSWER_PREFIX
):
    await answer_general_exam(
        update,
        context,
    )
    return
if data == CALLBACK_CANCEL:
    await cancel_general_exam(
        update,
        context,
    )
    return

==========================================================

Health check

==========================================================

def exam_handlers_health_check() -> bool:
“”“Basic health check for the Telegram exam handlers.”””

try:
    return all(
        (
            bool(EXAM_SESSION_KEY),
            bool(CALLBACK_START),
            bool(CALLBACK_CANCEL),
            bool(CALLBACK_ANSWER_PREFIX),
        )
    )
except Exception:
    return False
