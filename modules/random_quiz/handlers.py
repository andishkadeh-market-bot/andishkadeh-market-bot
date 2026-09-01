“””
Random Quiz Handlers
Andishkadeh Management & Market

Responsibilities:

* Show Random Quiz menu
* Start random quizzes
* Display questions
* Handle answers
* Show final result
* Cancel active quiz
* Provide module health check

This module is independent from other quiz handlers
and uses the central QuizEngine.
“””

from future import annotations

import random
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.quiz_engine import (
QuizEngine,
STATUS_ACTIVE,
STATUS_CANCELLED,
STATUS_COMPLETED,
quiz_engine,
)

from modules.random_quiz.data import (
RANDOM_QUIZ_CONFIG,
RANDOM_QUESTIONS,
data_health_check,
)

==========================================================

Constants

==========================================================

MODULE_ID = str(
RANDOM_QUIZ_CONFIG.get(
“module_id”,
“random_quiz”,
)
)

MODULE_TITLE = str(
RANDOM_QUIZ_CONFIG.get(
“title”,
“🎲 سوالات تصادفی”,
)
)

MODULE_DESCRIPTION = str(
RANDOM_QUIZ_CONFIG.get(
“description”,
“آزمون تصادفی از میان سوالات ثبت‌شده اندیشکده”,
)
)

DEFAULT_QUESTION_COUNT = int(
RANDOM_QUIZ_CONFIG.get(
“default_question_count”,
10,
)
)

MINIMUM_QUESTION_COUNT = int(
RANDOM_QUIZ_CONFIG.get(
“minimum_question_count”,
1,
)
)

MAXIMUM_QUESTION_COUNT = int(
RANDOM_QUIZ_CONFIG.get(
“maximum_question_count”,
20,
)
)

==========================================================

Helpers

==========================================================

def _safe_question_count(
requested_count: int | None,
) -> int:
“””
Normalize requested question count.
“””

if requested_count is None:
    requested_count = DEFAULT_QUESTION_COUNT
try:
    count = int(requested_count)
except (TypeError, ValueError):
    count = DEFAULT_QUESTION_COUNT
count = max(
    MINIMUM_QUESTION_COUNT,
    count,
)
count = min(
    MAXIMUM_QUESTION_COUNT,
    count,
)
count = min(
    count,
    len(RANDOM_QUESTIONS),
)
return max(
    1,
    count,
)

def _get_random_questions(
count: int,
) -> list[dict[str, Any]]:
“””
Select random questions from the question bank.
“””

if not RANDOM_QUESTIONS:
    return []
normalized_count = _safe_question_count(
    count
)
return random.sample(
    RANDOM_QUESTIONS,
    k=normalized_count,
)

def _main_menu_keyboard() -> InlineKeyboardMarkup:
“””
Keyboard for Random Quiz main menu.
“””

keyboard = [
    [
        InlineKeyboardButton(
            "🎯 شروع آزمون",
            callback_data="random_quiz_start",
        ),
    ],
    [
        InlineKeyboardButton(
            "🔟 آزمون ۱۰ سوالی",
            callback_data="random_quiz_count:10",
        ),
    ],
    [
        InlineKeyboardButton(
            "5️⃣ آزمون ۵ سوالی",
            callback_data="random_quiz_count:5",
        ),
    ],
    [
        InlineKeyboardButton(
            "↩️ بازگشت",
            callback_data="main_menu",
        ),
    ],
]
return InlineKeyboardMarkup(
    keyboard
)

def _quiz_keyboard(
options: tuple[str, …],
) -> InlineKeyboardMarkup:
“””
Build answer buttons.

The answer index is used instead of placing the
complete answer text inside callback_data.
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

def _result_keyboard() -> InlineKeyboardMarkup:
“””
Keyboard shown after quiz completion.
“””

return InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "🎲 آزمون جدید",
                callback_data="random_quiz_start",
            ),
        ],
        [
            InlineKeyboardButton(
                "↩️ بازگشت",
                callback_data="main_menu",
            ),
        ],
    ]
)

async def _edit_or_reply(
update: Update,
text: str,
reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
“””
Edit callback message when possible.
Otherwise send a new message.
“””

query = update.callback_query
if query is not None:
    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
        )
        return
    except Exception:
        pass
if update.message is not None:
    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )

==========================================================

Module Menu

==========================================================

async def show_random_quiz_menu(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“””
Display Random Quiz module menu.
“””

query = update.callback_query
if query is not None:
    await query.answer()
text = (
    f"{MODULE_TITLE}\n\n"
    f"{MODULE_DESCRIPTION}\n\n"
    "📌 در این بخش، سوالات به‌صورت تصادفی "
    "از بانک سوالات اندیشکده انتخاب می‌شوند.\n\n"
    f"🔢 تعداد پیش‌فرض: {DEFAULT_QUESTION_COUNT} سوال\n"
    f"📊 حداقل: {MINIMUM_QUESTION_COUNT} سوال\n"
    f"📊 حداکثر: {MAXIMUM_QUESTION_COUNT} سوال\n\n"
    "یکی از گزینه‌های زیر را انتخاب کنید:"
)
await _edit_or_reply(
    update,
    text,
    _main_menu_keyboard(),
)

==========================================================

Start Quiz

==========================================================

async def start_random_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
question_count: int | None = None,
) -> None:
“””
Start a new Random Quiz session.
“””

user = update.effective_user
if user is None:
    return
query = update.callback_query
if query is not None:
    await query.answer()
count = _safe_question_count(
    question_count
)
existing = quiz_engine.get_active_session(
    user.id
)
if existing is not None:
    await _edit_or_reply(
        update,
        (
            "⚠️ شما در حال حاضر یک آزمون فعال دارید.\n\n"
            f"📊 پیشرفت: "
            f"{existing.answered_questions()}/"
            f"{existing.total_questions()}\n\n"
            "ابتدا آزمون فعلی را لغو کنید."
        ),
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❌ لغو آزمون فعلی",
                        callback_data=(
                            "random_quiz_cancel"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "↩️ بازگشت",
                        callback_data="main_menu",
                    )
                ],
            ]
        ),
    )
    return
questions = _get_random_questions(
    count
)
if not questions:
    await _edit_or_reply(
        update,
        (
            "❌ بانک سوالات تصادفی خالی است.\n\n"
            "لطفاً بعداً دوباره تلاش کنید."
        ),
    )
    return
try:
    session = quiz_engine.start_quiz(
        telegram_id=user.id,
        module_id=MODULE_ID,
        chapter_id="random",
        lesson_id="random_quiz",
        questions=questions,
        replace_existing=False,
    )
except Exception as exc:
    await _edit_or_reply(
        update,
        (
            "❌ شروع آزمون با خطا مواجه شد.\n\n"
            f"جزئیات: {exc}"
        ),
    )
    return
await _show_current_question(
    update,
    session,
)

==========================================================

Current Question

==========================================================

async def _show_current_question(
update: Update,
session: Any,
) -> None:
“””
Display current question.
“””

question = session.current_question()
if question is None:
    return
question_number = (
    session.current_index + 1
)
total = session.total_questions()
text = (
    f"{MODULE_TITLE}\n\n"
    f"❓ سوال {question_number} از {total}\n\n"
    f"{question.question}\n\n"
    "👇 پاسخ صحیح را انتخاب کنید:"
)
await _edit_or_reply(
    update,
    text,
    _quiz_keyboard(
        question.options
    ),
)

==========================================================

Answer

==========================================================

async def answer_random_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“””
Handle an answer callback.

Callback format:
    random_quiz_answer:<index>
"""
query = update.callback_query
if query is None:
    return
user = update.effective_user
if user is None:
    await query.answer(
        "کاربر شناسایی نشد.",
        show_alert=True,
    )
    return
data = query.data or ""
try:
    _, index_text = data.split(
        ":",
        1,
    )
    option_index = int(
        index_text
    )
except (
    ValueError,
    TypeError,
):
    await query.answer(
        "❌ پاسخ نامعتبر است.",
        show_alert=True,
    )
    return
session = quiz_engine.get_active_session(
    user.id
)
if session is None:
    await query.answer(
        "⚠️ آزمون فعالی برای شما وجود ندارد.",
        show_alert=True,
    )
    return
question = session.current_question()
if question is None:
    await query.answer(
        "⚠️ سوال فعلی پیدا نشد.",
        show_alert=True,
    )
    return
if (
    option_index < 0
    or option_index >= len(
        question.options
    )
):
    await query.answer(
        "❌ گزینه نامعتبر است.",
        show_alert=True,
    )
    return
selected_answer = question.options[
    option_index
]
try:
    result = quiz_engine.submit_answer(
        telegram_id=user.id,
        answer=selected_answer,
    )
except Exception as exc:
    await query.answer(
        f"❌ خطا: {exc}",
        show_alert=True,
    )
    return
is_correct = bool(
    result.get(
        "is_correct",
        False,
    )
)
correct_answer = result.get(
    "correct_answer",
    "",
)
explanation = result.get(
    "explanation",
    "",
)
finished = bool(
    result.get(
        "finished",
        False,
    )
)
await query.answer(
    "✅ پاسخ صحیح بود!"
    if is_correct
    else "❌ پاسخ اشتباه بود.",
)
if finished:
    await _show_final_result(
        update,
        result,
    )
    return
feedback = (
    "✅ پاسخ شما صحیح بود."
    if is_correct
    else (
        "❌ پاسخ شما اشتباه بود.\n"
        f"✅ پاسخ صحیح: {correct_answer}"
    )
)
if explanation:
    feedback += (
        f"\n\n💡 توضیح:\n{explanation}"
    )
next_session = quiz_engine.get_active_session(
    user.id
)
if next_session is None:
    return
question = next_session.current_question()
if question is None:
    return
question_number = (
    next_session.current_index + 1
)
total = next_session.total_questions()
text = (
    f"{MODULE_TITLE}\n\n"
    f"{feedback}\n\n"
    "━━━━━━━━━━━━━━\n\n"
    f"❓ سوال {question_number} از {total}\n\n"
    f"{question.question}\n\n"
    "👇 پاسخ صحیح را انتخاب کنید:"
)
await _edit_or_reply(
    update,
    text,
    _quiz_keyboard(
        question.options
    ),
)

==========================================================

Final Result

==========================================================

async def _show_final_result(
update: Update,
answer_result: dict[str, Any],
) -> None:
“””
Show final quiz result.
“””

user = update.effective_user
if user is None:
    return
result = quiz_engine.get_result(
    user.id
)
if result is None:
    return
total = result.total_questions
correct = result.correct_answers
wrong = result.wrong_answers
score = result.score
if score >= 90:
    level = "🏆 عالی"
    message = "عملکرد فوق‌العاده‌ای داشتی."
elif score >= 70:
    level = "🥇 خوب"
    message = "عملکرد خوبی داشتی."
elif score >= 50:
    level = "🥈 متوسط"
    message = "بد نبود، ولی هنوز جا برای پیشرفت هست."
else:
    level = "📚 نیازمند مرور"
    message = "چند دور مرور درس‌ها بد نیست. مغز هم گاهی نیاز به تعمیرات دارد."
text = (
    f"{MODULE_TITLE}\n\n"
    "🎉 آزمون به پایان رسید!\n\n"
    "━━━━━━━━━━━━━━\n"
    f"📊 تعداد سوالات: {total}\n"
    f"✅ پاسخ صحیح: {correct}\n"
    f"❌ پاسخ غلط: {wrong}\n"
    f"📈 درصد موفقیت: {score:.2f}%\n"
    f"🏅 نتیجه: {level}\n"
    "━━━━━━━━━━━━━━\n\n"
    f"{message}\n\n"
    "آزمون دیگری را می‌توانید از همین بخش شروع کنید."
)
await _edit_or_reply(
    update,
    text,
    _result_keyboard(),
)

==========================================================

Cancel

==========================================================

async def cancel_random_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“””
Cancel current Random Quiz.
“””

query = update.callback_query
if query is not None:
    await query.answer()
user = update.effective_user
if user is None:
    return
session = quiz_engine.get_active_session(
    user.id
)
if session is None:
    await _edit_or_reply(
        update,
        (
            "ℹ️ در حال حاضر آزمون فعالی ندارید."
        ),
        _main_menu_keyboard(),
    )
    return
try:
    result = quiz_engine.cancel_quiz(
        user.id
    )
except Exception as exc:
    await _edit_or_reply(
        update,
        (
            "❌ لغو آزمون با خطا مواجه شد.\n\n"
            f"جزئیات: {exc}"
        ),
    )
    return
text = (
    f"{MODULE_TITLE}\n\n"
    "❌ آزمون لغو شد.\n\n"
    f"📊 تعداد پاسخ داده‌شده: "
    f"{result.answered_questions}/"
    f"{result.total_questions}\n"
    f"✅ صحیح: {result.correct_answers}\n"
    f"❌ غلط: {result.wrong_answers}\n\n"
    "برای شروع آزمون جدید می‌توانید دوباره اقدام کنید."
)
await _edit_or_reply(
    update,
    text,
    _main_menu_keyboard(),
)

==========================================================

Count Selection

==========================================================

async def handle_random_quiz_count(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“””
Start quiz with selected question count.

Callback format:
    random_quiz_count:<count>
"""
query = update.callback_query
if query is None:
    return
data = query.data or ""
try:
    _, count_text = data.split(
        ":",
        1,
    )
    count = int(
        count_text
    )
except (
    ValueError,
    TypeError,
):
    await query.answer(
        "❌ تعداد سوالات نامعتبر است.",
        show_alert=True,
    )
    return
await start_random_quiz(
    update,
    context,
    question_count=count,
)

==========================================================

Main Callback Router

==========================================================

async def route_random_quiz_callback(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“””
Route all Random Quiz callbacks.

Supported callbacks:
- menu_random_quiz
- random_quiz
- random_quiz_start
- random_quiz_count:<n>
- random_quiz_answer:<index>
- random_quiz_cancel
"""
query = update.callback_query
if query is None:
    return
data = query.data or ""
if data in {
    "menu_random_quiz",
    "random_quiz",
}:
    await show_random_quiz_menu(
        update,
        context,
    )
    return
if data == "random_quiz_start":
    await start_random_quiz(
        update,
        context,
    )
    return
if data.startswith(
    "random_quiz_count:"
):
    await handle_random_quiz_count(
        update,
        context,
    )
    return
if data.startswith(
    "random_quiz_answer:"
):
    await answer_random_quiz(
        update,
        context,
    )
    return
if data == "random_quiz_cancel":
    await cancel_random_quiz(
        update,
        context,
    )
    return
await query.answer(
    "❌ دستور ناشناخته است.",
    show_alert=True,
)

==========================================================

Health Check

==========================================================

def random_quiz_handlers_health_check() -> bool:
“””
Check Random Quiz handlers and dependencies.
“””

try:
    if not data_health_check():
        return False
    if not MODULE_ID:
        return False
    if not MODULE_TITLE:
        return False
    if not isinstance(
        DEFAULT_QUESTION_COUNT,
        int,
    ):
        return False
    if DEFAULT_QUESTION_COUNT < 1:
        return False
    if MINIMUM_QUESTION_COUNT < 1:
        return False
    if MAXIMUM_QUESTION_COUNT < MINIMUM_QUESTION_COUNT:
        return False
    if not RANDOM_QUESTIONS:
        return False
    # Verify that the central engine is available.
    if not isinstance(
        quiz_engine,
        QuizEngine,
    ):
        return False
    # Verify that the engine can normalize
    # the Random Quiz question bank.
    normalized = (
        quiz_engine.normalize_questions(
            RANDOM_QUESTIONS
        )
    )
    if not normalized:
        return False
    return True
except Exception:
    return False

==========================================================

Module Information

==========================================================

def get_random_quiz_module_info() -> dict[str, Any]:
“””
Return public module information.
“””

return {
    "module_id": MODULE_ID,
    "title": MODULE_TITLE,
    "description": MODULE_DESCRIPTION,
    "default_question_count": (
        DEFAULT_QUESTION_COUNT
    ),
    "minimum_question_count": (
        MINIMUM_QUESTION_COUNT
    ),
    "maximum_question_count": (
        MAXIMUM_QUESTION_COUNT
    ),
    "question_count": len(
        RANDOM_QUESTIONS
    ),
    "health": (
        random_quiz_handlers_health_check()
    ),
}

==========================================================

Compatibility Aliases

==========================================================

show_random_quiz = show_random_quiz_menu
start_quiz = start_random_quiz
answer_quiz = answer_random_quiz
cancel_quiz = cancel_random_quiz
random_quiz_health_check = (
random_quiz_handlers_health_check
)
