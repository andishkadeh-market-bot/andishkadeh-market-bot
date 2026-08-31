“””
Telegram handlers for Psychology & Social Work.

Andishkadeh Management & Market
“””

from future import annotations

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
get_lesson,
get_lessons,
get_quiz_questions,
)
from modules.psychology.service import (
complete_lesson,
save_quiz_result,
start_lesson,
)

logger = logging.getLogger(name)

PSYCHOLOGY_QUIZ_KEY = “psychology_quiz”

def psychology_main_keyboard() -> InlineKeyboardMarkup:
“”“Build Psychology module keyboard.”””

keyboard: list[list[InlineKeyboardButton]] = []
for chapter in get_chapters():
    chapter_id = chapter.get("id")
    if not chapter_id:
        continue
    keyboard.append(
        [
            InlineKeyboardButton(
                f"📖 {chapter.get('title', chapter_id)}",
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
“”“Build chapter lesson keyboard.”””

keyboard: list[list[InlineKeyboardButton]] = []
for lesson in get_lessons(chapter_id):
    lesson_id = lesson.get("id")
    if not lesson_id:
        continue
    keyboard.append(
        [
            InlineKeyboardButton(
                f"📚 {lesson.get('title', lesson_id)}",
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
) -> InlineKeyboardMarkup:
“”“Build lesson keyboard.”””

return InlineKeyboardMarkup(
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
                "✅ تکمیل درس",
                callback_data=(
                    f"psychology_complete:"
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
)

def psychology_quiz_cancel_keyboard() -> InlineKeyboardMarkup:
“”“Build quiz cancellation keyboard.”””

return InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "❌ لغو آزمون",
                callback_data="psychology_quiz_cancel",
            )
        ]
    ]
)

def psychology_quiz_answer_keyboard(
question_index: int,
options: list[str],
) -> InlineKeyboardMarkup:
“”“Build answer buttons.”””

keyboard: list[list[InlineKeyboardButton]] = []
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
                f"{labels[index]}. {option}",
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
            callback_data="psychology_quiz_cancel",
        )
    ]
)
return InlineKeyboardMarkup(keyboard)

def _get_user_id(
update: Update,
) -> int | None:
“”“Return Telegram user ID.”””

user = update.effective_user
if user is None:
    return None
return user.id

def _get_quiz_state(
context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
“”“Return current Psychology quiz state.”””

state = context.user_data.get(
    PSYCHOLOGY_QUIZ_KEY
)
if not isinstance(state, dict):
    return None
return state

async def show_psychology_menu(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show Psychology module menu.”””

query = update.callback_query
if query is not None:
    await query.answer()
    await query.edit_message_text(
        (
            f"🧠 <b>{html.escape(MODULE_TITLE)}</b>\n\n"
            "فصل موردنظر را انتخاب کنید:"
        ),
        parse_mode="HTML",
        reply_markup=psychology_main_keyboard(),
    )
    return
if update.message is not None:
    await update.message.reply_text(
        (
            f"🧠 <b>{html.escape(MODULE_TITLE)}</b>\n\n"
            "فصل موردنظر را انتخاب کنید:"
        ),
        parse_mode="HTML",
        reply_markup=psychology_main_keyboard(),
    )

async def show_psychology_chapter(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show lessons of a Psychology chapter.”””

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
    chapter_id
)
if chapter is None:
    await query.edit_message_text(
        "❌ فصل پیدا نشد.",
        reply_markup=psychology_main_keyboard(),
    )
    return
await query.edit_message_text(
    (
        f"📖 <b>{html.escape(str(chapter.get('title', chapter_id)))}</b>\n\n"
        "درس موردنظر را انتخاب کنید:"
    ),
    parse_mode="HTML",
    reply_markup=psychology_chapter_keyboard(
        chapter_id
    ),
)

async def show_psychology_lesson(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show a Psychology lesson.”””

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
content = html.escape(
    str(
        lesson.get(
            "content",
            "محتوای درس ثبت نشده است.",
        )
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
special_text = "\n".join(
    f"• {html.escape(str(item))}"
    for item in special_points
)
exam_text = "\n".join(
    f"• {html.escape(str(item))}"
    for item in exam_points
)
example = html.escape(
    str(
        lesson.get(
            "example",
            "-",
        )
    )
)
text = (
    f"📚 <b>{html.escape(str(lesson.get('title', lesson_id)))}</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    f"{content}\n\n"
    "🎯 <b>نکات تخصصی</b>\n"
    f"{special_text or '• موردی ثبت نشده است.'}\n\n"
    "📝 <b>نکات آزمونی</b>\n"
    f"{exam_text or '• موردی ثبت نشده است.'}\n\n"
    "💡 <b>مثال کاربردی</b>\n"
    f"{example}"
)
await query.edit_message_text(
    text,
    parse_mode="HTML",
    reply_markup=psychology_lesson_keyboard(
        chapter_id,
        lesson_id,
    ),
)

async def complete_psychology_lesson(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Mark Psychology lesson as completed.”””

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
        "✅ <b>درس با موفقیت تکمیل شد.</b>\n\n"
        "پیشرفت شما ثبت شد.\n\n"
        "حالا می‌توانید آزمون این درس را انجام دهید."
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

async def start_psychology_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Start a Psychology lesson quiz.”””

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
        ),
    )
    return
user_id = _get_user_id(update)
if user_id is None:
    return
try:
    engine = QuizEngine(
        questions=questions
    )
except TypeError:
    try:
        engine = QuizEngine(
            questions
        )
    except Exception:
        logger.exception(
            "Failed to initialize Psychology QuizEngine."
        )
        await query.edit_message_text(
            "❌ خطا در آماده‌سازی آزمون.",
            reply_markup=psychology_lesson_keyboard(
                chapter_id,
                lesson_id,
            ),
        )
        return
except Exception:
    logger.exception(
        "Failed to initialize Psychology QuizEngine."
    )
    await query.edit_message_text(
        "❌ خطا در آماده‌سازی آزمون.",
        reply_markup=psychology_lesson_keyboard(
            chapter_id,
            lesson_id,
        ),
    )
    return
selected_questions = list(questions)
if len(selected_questions) > 10:
    selected_questions = random.sample(
        selected_questions,
        10,
    )
context.user_data[
    PSYCHOLOGY_QUIZ_KEY
] = {
    "module_id": MODULE_ID,
    "chapter_id": chapter_id,
    "lesson_id": lesson_id,
    "questions": selected_questions,
    "engine": engine,
    "current_index": 0,
    "correct_answers": 0,
    "total_questions": len(selected_questions),
}
await _show_current_psychology_question(
    update,
    context,
)

async def _show_current_psychology_question(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Display current Psychology quiz question.”””

state = _get_quiz_state(
    context
)
query = update.callback_query
if state is None or query is None:
    return
questions = state.get(
    "questions",
    [],
)
current_index = int(
    state.get(
        "current_index",
        0,
    )
)
if current_index >= len(questions):
    await finish_psychology_quiz(
        update,
        context,
    )
    return
question = questions[current_index]
question_text = html.escape(
    str(
        question.get(
            "question",
            "",
        )
    )
)
options = question.get(
    "options",
    [],
)
if not isinstance(options, list):
    options = []
text = (
    "🧠 <b>آزمون روانشناسی و مددکاری</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    f"سوال <b>{current_index + 1}</b> "
    f"از <b>{len(questions)}</b>\n\n"
    f"{question_text}"
)
await query.edit_message_text(
    text,
    parse_mode="HTML",
    reply_markup=psychology_quiz_answer_keyboard(
        current_index,
        [
            str(option)
            for option in options
        ],
    ),
)

async def answer_psychology_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Process one Psychology quiz answer.”””

query = update.callback_query
if query is None:
    return
await query.answer()
state = _get_quiz_state(
    context
)
if state is None:
    await query.edit_message_text(
        "❌ آزمون فعالی وجود ندارد.",
        reply_markup=psychology_main_keyboard(),
    )
    return
data = query.data or ""
parts = data.split(":")
if len(parts) != 3:
    await query.edit_message_text(
        "❌ پاسخ نامعتبر است.",
        reply_markup=psychology_main_keyboard(),
    )
    return
try:
    question_index = int(parts[1])
    answer_index = int(parts[2])
except ValueError:
    await query.edit_message_text(
        "❌ پاسخ نامعتبر است.",
        reply_markup=psychology_main_keyboard(),
    )
    return
current_index = int(
    state.get(
        "current_index",
        0,
    )
)
if question_index != current_index:
    await query.answer(
        "این سوال دیگر فعال نیست.",
        show_alert=True,
    )
    return
questions = state.get(
    "questions",
    [],
)
if current_index >= len(questions):
    await finish_psychology_quiz(
        update,
        context,
    )
    return
question = questions[current_index]
options = question.get(
    "options",
    [],
)
if (
    not isinstance(options, list)
    or answer_index < 0
    or answer_index >= len(options)
):
    await query.answer(
        "گزینه نامعتبر است.",
        show_alert=True,
    )
    return
correct_index = question.get(
    "answer"
)
try:
    correct_index = int(
        correct_index
    )
except (TypeError, ValueError):
    correct_index = -1
if answer_index == correct_index:
    state["correct_answers"] = (
        int(
            state.get(
                "correct_answers",
                0,
            )
        )
        + 1
    )
state["current_index"] = (
    current_index + 1
)
context.user_data[
    PSYCHOLOGY_QUIZ_KEY
] = state
if (
    state["current_index"]
    >= len(questions)
):
    await finish_psychology_quiz(
        update,
        context,
    )
    return
await _show_current_psychology_question(
    update,
    context,
)

async def finish_psychology_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Finish quiz and save Statistics.”””

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
user_id = _get_user_id(update)
if user_id is None:
    return
total_questions = int(
    state.get(
        "total_questions",
        0,
    )
)
correct_answers = int(
    state.get(
        "correct_answers",
        0,
    )
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
if total_questions <= 0:
    await query.edit_message_text(
        "❌ آزمون سوالی برای ثبت ندارد.",
        reply_markup=psychology_main_keyboard(),
    )
    context.user_data.pop(
        PSYCHOLOGY_QUIZ_KEY,
        None,
    )
    return
try:
    save_quiz_result(
        telegram_id=user_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
    )
    score = round(
        correct_answers
        / total_questions
        * 100,
        2,
    )
    complete_lesson(
        telegram_id=user_id,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
    )
except Exception:
    logger.exception(
        "Failed to save Psychology quiz result."
    )
    await query.edit_message_text(
        "❌ نتیجه آزمون ثبت نشد. لطفاً دوباره تلاش کنید.",
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
        "━━━━━━━━━━━━━━━━━━\n"
        f"تعداد سوالات: <b>{total_questions}</b>\n"
        f"پاسخ صحیح: <b>{correct_answers}</b>\n"
        f"پاسخ غلط: <b>{total_questions - correct_answers}</b>\n"
        f"نمره: <b>{score}%</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📊 نتیجه در Statistics ثبت شد.\n"
        "📚 پیشرفت درس نیز به‌روزرسانی شد."
    ),
    parse_mode="HTML",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📚 درس",
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

async def cancel_psychology_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Cancel active Psychology quiz.”””

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
