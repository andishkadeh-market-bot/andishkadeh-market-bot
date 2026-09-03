"""
Finance Handlers
Andishkadeh Management & Market

مدیریت رابط کاربری ماژول مدیریت مالی:
- منوی مدیریت مالی
- فصل‌ها
- درس‌ها
- محتوای آموزشی
- آزمون
- انتخاب گزینه
- بررسی پاسخ
- نمایش سؤال بعدی
- ثبت نتیجه نهایی
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from .service import (
    get_finance_chapters,
    get_finance_chapter,
    get_finance_lessons,
    get_finance_lesson,
    get_complete_lesson,
    get_finance_quiz,
    get_quiz_question,
    calculate_quiz_result,
    complete_quiz_attempt,
    finance_health_check,
)


# ============================================================
# Constants
# ============================================================

FINANCE_MENU_CALLBACK = "finance_menu"
FINANCE_CHAPTER_PREFIX = "finance_chapter:"
FINANCE_LESSON_PREFIX = "finance_lesson:"
FINANCE_BACK_CALLBACK = "finance_back"
MAIN_MENU_CALLBACK = "menu_main"

FINANCE_LESSON_QUIZ_SUFFIX = ":quiz"

FINANCE_ANSWER_MARKER = ":answer:"
FINANCE_QUIZ_STATE_KEY = "finance_quiz_state"


# ============================================================
# Helpers
# ============================================================

def _normalize_text(value: Any, default: str = "") -> str:
    if value is None:
        return default

    return str(value).strip()


def _normalize_list(value: Any) -> List[Any]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, set):
        return list(value)

    return [value]


def _get_id(item: Any) -> str:
    if isinstance(item, dict):
        return _normalize_text(
            item.get("id")
            or item.get("chapter_id")
            or item.get("lesson_id")
        )

    return _normalize_text(
        getattr(item, "id", None)
        or getattr(item, "chapter_id", None)
        or getattr(item, "lesson_id", None)
    )


def _get_title(item: Any) -> str:
    if isinstance(item, dict):
        return _normalize_text(
            item.get("title")
            or item.get("name")
        )

    return _normalize_text(
        getattr(item, "title", None)
        or getattr(item, "name", None)
    )


def _safe_edit(
    query: Any,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
) -> None:
    """
    فقط برای مستندسازی نوع عملیات.
    عملیات واقعی در handlerهای async انجام می‌شود.
    """
    return None


# ============================================================
# Keyboards
# ============================================================

def _finance_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📚 فصل‌های مدیریت مالی",
                    callback_data=FINANCE_MENU_CALLBACK,
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data=MAIN_MENU_CALLBACK,
                )
            ],
        ]
    )


def _finance_chapters_keyboard(
    chapters: List[Dict[str, Any]],
) -> InlineKeyboardMarkup:

    buttons: List[List[InlineKeyboardButton]] = []

    for chapter in chapters:

        chapter_id = _normalize_text(
            chapter.get("id")
        )

        title = _normalize_text(
            chapter.get("title"),
            chapter_id,
        )

        if not chapter_id:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    title,
                    callback_data=(
                        f"{FINANCE_CHAPTER_PREFIX}"
                        f"{chapter_id}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(
        buttons
    )


def _finance_chapter_keyboard(
    chapter_id: str,
    lessons: List[Dict[str, Any]],
) -> InlineKeyboardMarkup:

    buttons: List[List[InlineKeyboardButton]] = []

    for lesson in lessons:

        lesson_id = _normalize_text(
            lesson.get("id")
        )

        title = _normalize_text(
            lesson.get("title"),
            lesson_id,
        )

        if not lesson_id:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    title,
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}"
                        f"{lesson_id}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "⬅️ فصل‌ها",
                callback_data=FINANCE_MENU_CALLBACK,
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(
        buttons
    )


def _finance_lesson_keyboard(
    lesson_id: str,
) -> InlineKeyboardMarkup:

    buttons: List[List[InlineKeyboardButton]] = []

    if lesson_id:

        buttons.append(
            [
                InlineKeyboardButton(
                    "📝 آزمون این درس",
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}"
                        f"{lesson_id}"
                        f"{FINANCE_LESSON_QUIZ_SUFFIX}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "⬅️ بازگشت به فصل",
                callback_data=FINANCE_BACK_CALLBACK,
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=MAIN_MENU_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(
        buttons
    )


def _finance_quiz_keyboard(
    lesson_id: str,
    question_index: int,
    options: List[str],
) -> InlineKeyboardMarkup:

    buttons: List[List[InlineKeyboardButton]] = []

    option_labels = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
    ]

    for index, option in enumerate(options):

        if index >= 4:
            break

        label = _normalize_text(
            option
        )

        if not label:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    f"{option_labels[index]} {label}",
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}"
                        f"{lesson_id}"
                        f"{FINANCE_ANSWER_MARKER}"
                        f"{question_index}:"
                        f"{index}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "❌ خروج از آزمون",
                callback_data=(
                    f"{FINANCE_LESSON_PREFIX}"
                    f"{lesson_id}"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(
        buttons
    )


def _finance_quiz_result_keyboard(
    lesson_id: str,
) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 شروع دوباره آزمون",
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}"
                        f"{lesson_id}"
                        f"{FINANCE_LESSON_QUIZ_SUFFIX}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 بازگشت به درس",
                    callback_data=(
                        f"{FINANCE_LESSON_PREFIX}"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data=MAIN_MENU_CALLBACK,
                )
            ],
        ]
    )


# ============================================================
# Formatting
# ============================================================

def _format_lesson_content(
    lesson: Dict[str, Any],
) -> str:

    title = _normalize_text(
        lesson.get("title"),
        "درس مدیریت مالی",
    )

    text_parts: List[str] = []

    text_parts.append(
        f"📖 {title}"
    )

    lesson_text = _normalize_text(
        lesson.get("lesson_text")
    )

    if lesson_text:
        text_parts.append(
            f"\n{lesson_text}"
        )

    subtopics = _normalize_list(
        lesson.get("subtopics")
    )

    if subtopics:

        text_parts.append(
            "\n\n📌 سرفصل‌های درس"
        )

        for item in subtopics:

            item_text = _normalize_text(
                item
            )

            if item_text:
                text_parts.append(
                    f"\n• {item_text}"
                )

    detailed_content = _normalize_text(
        lesson.get("detailed_content")
    )

    if detailed_content:

        text_parts.append(
            "\n\n📚 آموزش تفصیلی"
        )

        text_parts.append(
            f"\n{detailed_content}"
        )

    specialized_points = _normalize_list(
        lesson.get("specialized_points")
    )

    if specialized_points:

        text_parts.append(
            "\n\n🎓 نکات تخصصی"
        )

        for item in specialized_points:

            item_text = _normalize_text(
                item
            )

            if item_text:
                text_parts.append(
                    f"\n• {item_text}"
                )

    exam_points = _normalize_list(
        lesson.get("exam_points")
    )

    if exam_points:

        text_parts.append(
            "\n\n📝 نکات آزمونی"
        )

        for item in exam_points:

            item_text = _normalize_text(
                item
            )

            if item_text:
                text_parts.append(
                    f"\n• {item_text}"
                )

    practical_example = lesson.get(
        "practical_example"
    )

    if practical_example:

        text_parts.append(
            "\n\n💼 مثال کاربردی"
        )

        for item in _normalize_list(
            practical_example
        ):

            item_text = _normalize_text(
                item
            )

            if item_text:
                text_parts.append(
                    f"\n• {item_text}"
                )

    review = lesson.get(
        "review"
    )

    if review:

        text_parts.append(
            "\n\n🔁 مرور"
        )

        for item in _normalize_list(
            review
        ):

            item_text = _normalize_text(
                item
            )

            if item_text:
                text_parts.append(
                    f"\n• {item_text}"
                )

    return "".join(
        text_parts
    )


def _format_quiz_question(
    lesson_title: str,
    question: Dict[str, Any],
    question_index: int,
    total_questions: int,
) -> str:

    question_text = _normalize_text(
        question.get("question"),
        "سؤال آزمون",
    )

    return (
        "📝 آزمون درس مدیریت مالی\n"
        f"📖 {lesson_title}\n\n"
        f"سؤال {question_index + 1} "
        f"از {total_questions}\n\n"
        f"{question_text}\n\n"
        "👇 یکی از گزینه‌ها را انتخاب کنید:"
    )


# ============================================================
# Quiz State
# ============================================================

def _create_quiz_state(
    lesson_id: str,
    chapter_id: str,
    quiz: List[Dict[str, Any]],
) -> Dict[str, Any]:

    return {
        "lesson_id": lesson_id,
        "chapter_id": chapter_id,
        "quiz": quiz,
        "current_index": 0,
        "answers": [
            None
            for _ in quiz
        ],
    }


def _get_quiz_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> Optional[Dict[str, Any]]:

    state = context.user_data.get(
        FINANCE_QUIZ_STATE_KEY
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

    context.user_data.pop(
        FINANCE_QUIZ_STATE_KEY,
        None,
    )


# ============================================================
# Main Finance Menu
# ============================================================

async def show_finance_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query:
        await query.answer()

        await query.edit_message_text(
            "💰 مدیریت مالی\n\n"
            "دوره تخصصی مدیریت مالی\n"
            "از مبانی مالی تا تحلیل و تصمیم‌گیری پیشرفته.",
            reply_markup=_finance_menu_keyboard(),
        )

        return

    if update.message:

        await update.message.reply_text(
            "💰 مدیریت مالی\n\n"
            "دوره تخصصی مدیریت مالی\n"
            "از مبانی مالی تا تحلیل و تصمیم‌گیری پیشرفته.",
            reply_markup=_finance_menu_keyboard(),
        )


# ============================================================
# Chapters
# ============================================================

async def show_finance_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query:
        await query.answer()

    chapters = get_finance_chapters()

    if not chapters:

        text = (
            "💰 مدیریت مالی\n\n"
            "در حال حاضر فصلی برای نمایش وجود ندارد."
        )

        if query:
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🏠 منوی اصلی",
                                callback_data=MAIN_MENU_CALLBACK,
                            )
                        ]
                    ]
                ),
            )

        return

    text = (
        "💰 مدیریت مالی\n\n"
        "📚 فصل‌های دوره را انتخاب کنید:"
    )

    if query:

        await query.edit_message_text(
            text,
            reply_markup=_finance_chapters_keyboard(
                chapters
            ),
        )


# ============================================================
# Chapter
# ============================================================

async def show_finance_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
) -> None:

    query = update.callback_query

    if query:
        await query.answer()

    chapter = get_finance_chapter(
        chapter_id
    )

    if chapter is None:

        if query:

            await query.edit_message_text(
                "❌ فصل موردنظر پیدا نشد.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⬅️ فصل‌ها",
                                callback_data=FINANCE_MENU_CALLBACK,
                            )
                        ]
                    ]
                ),
            )

        return

    lessons = get_finance_lessons(
        chapter_id
    )

    chapter_title = _normalize_text(
        chapter.get("title"),
        chapter_id,
    )

    text = (
        f"💰 {chapter_title}\n\n"
        f"📚 تعداد درس‌ها: {len(lessons)}\n\n"
        "یک درس را انتخاب کنید:"
    )

    if query:

        await query.edit_message_text(
            text,
            reply_markup=_finance_chapter_keyboard(
                chapter_id,
                lessons,
            ),
        )


# ============================================================
# Lesson
# ============================================================

async def show_finance_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
    lesson_id: str,
) -> None:

    query = update.callback_query

    if query:
        await query.answer()

    lesson = get_complete_lesson(
        chapter_id,
        lesson_id,
    )

    if not lesson:

        if query:

            await query.edit_message_text(
                "❌ محتوای درس پیدا نشد.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🏠 منوی اصلی",
                                callback_data=MAIN_MENU_CALLBACK,
                            )
                        ]
                    ]
                ),
            )

        return

    text = _format_lesson_content(
        lesson
    )

    keyboard = _finance_lesson_keyboard(
        lesson_id
    )

    if query:

        await query.edit_message_text(
            text,
            reply_markup=keyboard,
        )


# ============================================================
# Quiz Start
# ============================================================

async def show_finance_lesson_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chapter_id: str,
    lesson_id: str,
) -> None:

    query = update.callback_query

    if query:
        await query.answer()

    lesson = get_finance_lesson(
        chapter_id,
        lesson_id,
    )

    if lesson is None:

        if query:
            await query.edit_message_text(
                "❌ درس موردنظر پیدا نشد."
            )

        return

    quiz = get_finance_quiz(
        chapter_id,
        lesson_id,
    )

    if not quiz:

        if query:

            await query.edit_message_text(
                "📝 آزمون این درس هنوز آماده نشده است.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "📖 بازگشت به درس",
                                callback_data=(
                                    f"{FINANCE_LESSON_PREFIX}"
                                    f"{lesson_id}"
                                ),
                            )
                        ]
                    ]
                ),
            )

        return

    state = _create_quiz_state(
        lesson_id=lesson_id,
        chapter_id=chapter_id,
        quiz=quiz,
    )

    context.user_data[
        FINANCE_QUIZ_STATE_KEY
    ] = state

    question = get_quiz_question(
        quiz,
        0,
    )

    if question is None:

        _clear_quiz_state(
            context
        )

        if query:

            await query.edit_message_text(
                "❌ سؤال معتبر برای این آزمون پیدا نشد."
            )

        return

    lesson_title = _normalize_text(
        lesson.get("title"),
        "مدیریت مالی",
    )

    options = _normalize_list(
        question.get(
            "options",
            [],
        )
    )

    text = _format_quiz_question(
        lesson_title,
        question,
        0,
        len(quiz),
    )

    keyboard = _finance_quiz_keyboard(
        lesson_id,
        0,
        options,
    )

    if query:

        await query.edit_message_text(
            text,
            reply_markup=keyboard,
        )


# ============================================================
# Quiz Answer
# ============================================================

async def handle_finance_quiz_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    lesson_id: str,
    question_index: int,
    option_index: int,
) -> None:

    query = update.callback_query

    if query:
        await query.answer()

    state = _get_quiz_state(
        context
    )

    if state is None:

        if query:

            await query.edit_message_text(
                "⚠️ آزمون فعالی وجود ندارد.\n"
                "لطفاً آزمون را دوباره شروع کنید.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "📝 شروع آزمون",
                                callback_data=(
                                    f"{FINANCE_LESSON_PREFIX}"
                                    f"{lesson_id}"
                                    f"{FINANCE_LESSON_QUIZ_SUFFIX}"
                                ),
                            )
                        ]
                    ]
                ),
            )

        return

    state_lesson_id = _normalize_text(
        state.get("lesson_id")
    )

    if state_lesson_id != lesson_id:

        if query:
            await query.edit_message_text(
                "⚠️ وضعیت آزمون با این درس مطابقت ندارد."
            )

        return

    quiz = _normalize_list(
        state.get("quiz")
    )

    answers = _normalize_list(
        state.get("answers")
    )

    try:
        question_index = int(
            question_index
        )

        option_index = int(
            option_index
        )

    except (
        TypeError,
        ValueError,
    ):

        return

    if (
        question_index < 0
        or question_index >= len(quiz)
    ):
        return

    question = get_quiz_question(
        quiz,
        question_index,
    )

    if question is None:
        return

    options = _normalize_list(
        question.get(
            "options",
            [],
        )
    )

    if (
        option_index < 0
        or option_index >= len(options)
    ):
        return

    while len(answers) < len(quiz):
        answers.append(None)

    answers[
        question_index
    ] = option_index

    state["answers"] = answers

    next_index = (
        question_index + 1
    )

    if next_index < len(quiz):

        state["current_index"] = next_index

        next_question = get_quiz_question(
            quiz,
            next_index,
        )

        if next_question is None:
            return

        chapter_id = _normalize_text(
            state.get(
                "chapter_id"
            )
        )

        lesson = get_finance_lesson(
            chapter_id,
            lesson_id,
        )

        lesson_title = _normalize_text(
            lesson.get("title")
            if lesson
            else None,
            "مدیریت مالی",
        )

        next_options = _normalize_list(
            next_question.get(
                "options",
                [],
            )
        )

        text = _format_quiz_question(
            lesson_title,
            next_question,
            next_index,
            len(quiz),
        )

        keyboard = _finance_quiz_keyboard(
            lesson_id,
            next_index,
            next_options,
        )

        if query:

            await query.edit_message_text(
                text,
                reply_markup=keyboard,
            )

        return

    # ========================================================
    # Quiz Finished
    # ========================================================

    chapter_id = _normalize_text(
        state.get(
            "chapter_id"
        )
    )

    result = complete_quiz_attempt(
        telegram_id=(
            update.effective_user.id
            if update.effective_user
            else 0
        ),
        module_id="finance",
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        quiz=quiz,
        answers=answers,
    )

    _clear_quiz_state(
        context
    )

    total_questions = result.get(
        "total_questions",
        len(quiz),
    )

    correct_answers = result.get(
        "correct_answers",
        0,
    )

    wrong_answers = result.get(
        "wrong_answers",
        0,
    )

    unanswered_questions = result.get(
        "unanswered_questions",
        0,
    )

    score = result.get(
        "score",
        0,
    )

    attempt_id = result.get(
        "attempt_id"
    )

    saved = result.get(
        "saved",
        False,
    )

    if score >= 90:

        level = "🏆 عالی"

    elif score >= 75:

        level = "🥇 بسیار خوب"

    elif score >= 50:

        level = "🥈 متوسط"

    else:

        level = "📚 نیازمند مرور"

    save_status = (
        "💾 نتیجه در سوابق آزمون ثبت شد."
        if saved
        else "⚠️ نتیجه محاسبه شد، اما ثبت سوابق انجام نشد."
    )

    attempt_text = ""

    if attempt_id is not None:

        attempt_text = (
            f"\nشناسه آزمون: {attempt_id}"
        )

    text = (
        "🎯 پایان آزمون مدیریت مالی\n\n"
        f"📊 نتیجه: {level}\n\n"
        f"📝 تعداد سؤالات: {total_questions}\n"
        f"✅ پاسخ صحیح: {correct_answers}\n"
        f"❌ پاسخ غلط: {wrong_answers}\n"
        f"⚪ بدون پاسخ: {unanswered_questions}\n"
        f"📈 درصد نهایی: {score}%\n\n"
        f"{save_status}"
        f"{attempt_text}"
    )

    if query:

        await query.edit_message_text(
            text,
            reply_markup=_finance_quiz_result_keyboard(
                lesson_id
            ),
        )


# ============================================================
# Callback Router
# ============================================================

async def route_finance_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if query is None:
        return

    callback_data = _normalize_text(
        query.data
    )

    if not callback_data:
        await query.answer()
        return

    # --------------------------------------------------------
    # Main Finance Menu
    # --------------------------------------------------------

    if callback_data == "menu_finance":

        _clear_quiz_state(
            context
        )

        await show_finance_menu(
            update,
            context,
        )

        return

    if callback_data in {
        FINANCE_MENU_CALLBACK,
        FINANCE_BACK_CALLBACK,
    }:

        _clear_quiz_state(
            context
        )

        await show_finance_chapters(
            update,
            context,
        )

        return

    # --------------------------------------------------------
    # Finance Lesson Callbacks
    # --------------------------------------------------------

    if callback_data.startswith(
        FINANCE_LESSON_PREFIX
    ):

        payload = callback_data[
            len(FINANCE_LESSON_PREFIX):
        ]

        # ====================================================
        # Answer Callback
        # ====================================================

        if FINANCE_ANSWER_MARKER in payload:

            try:

                lesson_id, answer_data = payload.split(
                    FINANCE_ANSWER_MARKER,
                    1,
                )

                question_index_text, option_index_text = (
                    answer_data.split(
                        ":",
                        1,
                    )
                )

                question_index = int(
                    question_index_text
                )

                option_index = int(
                    option_index_text
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

            await handle_finance_quiz_answer(
                update,
                context,
                lesson_id,
                question_index,
                option_index,
            )

            return

        # ====================================================
        # Quiz Start Callback
        # ====================================================

        if payload.endswith(
            FINANCE_LESSON_QUIZ_SUFFIX
        ):

            real_lesson_id = payload[
                : -len(
                    FINANCE_LESSON_QUIZ_SUFFIX
                )
            ]

            state = _get_quiz_state(
                context
            )

            chapter_id = ""

            if state:

                state_lesson_id = _normalize_text(
                    state.get(
                        "lesson_id"
                    )
                )

                if (
                    state_lesson_id
                    == real_lesson_id
                ):

                    chapter_id = _normalize_text(
                        state.get(
                            "chapter_id"
                        )
                    )

            if not chapter_id:

                for chapter in get_finance_chapters():

                    current_chapter_id = _normalize_text(
                        chapter.get(
                            "id"
                        )
                    )

                    lessons = get_finance_lessons(
                        current_chapter_id
                    )

                    for lesson in lessons:

                        if (
                            _normalize_text(
                                lesson.get(
                                    "id"
                                )
                            )
                            == real_lesson_id
                        ):

                            chapter_id = (
                                current_chapter_id
                            )

                            break

                    if chapter_id:
                        break

            if not chapter_id:

                await query.answer(
                    "❌ فصل این درس پیدا نشد.",
                    show_alert=True,
                )

                return

            await show_finance_lesson_quiz(
                update,
                context,
                chapter_id,
                real_lesson_id,
            )

            return

        # ====================================================
        # Normal Lesson Callback
        # ====================================================

        lesson_id = payload

        state = _get_quiz_state(
            context
        )

        if state:

            state_lesson_id = _normalize_text(
                state.get(
                    "lesson_id"
                )
            )

            if state_lesson_id == lesson_id:

                _clear_quiz_state(
                    context
                )

        chapter_id = ""

        for chapter in get_finance_chapters():

            current_chapter_id = _normalize_text(
                chapter.get(
                    "id"
                )
            )

            lessons = get_finance_lessons(
                current_chapter_id
            )

            for lesson in lessons:

                if (
                    _normalize_text(
                        lesson.get(
                            "id"
                        )
                    )
                    == lesson_id
                ):

                    chapter_id = (
                        current_chapter_id
                    )

                    break

            if chapter_id:
                break

        if not chapter_id:

            await query.answer(
                "❌ فصل درس پیدا نشد.",
                show_alert=True,
            )

            return

        await show_finance_lesson(
            update,
            context,
            chapter_id,
            lesson_id,
        )

        return

    # --------------------------------------------------------
    # Chapter
    # --------------------------------------------------------

    if callback_data.startswith(
        FINANCE_CHAPTER_PREFIX
    ):

        _clear_quiz_state(
            context
        )

        chapter_id = callback_data[
            len(FINANCE_CHAPTER_PREFIX):
        ]

        await show_finance_chapter(
            update,
            context,
            chapter_id,
        )

        return

    # --------------------------------------------------------
    # Main Menu
    # --------------------------------------------------------

    if callback_data == MAIN_MENU_CALLBACK:

        _clear_quiz_state(
            context
        )

        await query.answer()

        await query.edit_message_text(
            "🏠 منوی اصلی",
        )

        return

    # --------------------------------------------------------
    # Unknown Callback
    # --------------------------------------------------------

    await query.answer(
        "⚠️ این گزینه دیگر فعال نیست.",
        show_alert=True,
    )


# ============================================================
# Health Check
# ============================================================

def finance_handlers_health_check() -> Dict[str, Any]:
    """
    بررسی سلامت Handlerهای Finance.
    """
    try:

        service_health = finance_health_check()

        return {
            "module_id": "finance",
            "status": (
                "healthy"
                if service_health.get(
                    "valid",
                    False,
                )
                else "warning"
            ),
            "service": service_health,
            "quiz_answer_handler": True,
            "quiz_state": FINANCE_QUIZ_STATE_KEY,
        }

    except Exception as exc:

        return {
            "module_id": "finance",
            "status": "error",
            "quiz_answer_handler": False,
            "error": str(exc),
        }


# ============================================================
# Public API
# ============================================================

__all__ = [
    "show_finance_menu",
    "show_finance_chapters",
    "show_finance_chapter",
    "show_finance_lesson",
    "show_finance_lesson_quiz",
    "handle_finance_quiz_answer",
    "route_finance_callback",
    "finance_handlers_health_check",
]
