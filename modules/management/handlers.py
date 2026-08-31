"""
Telegram handlers for the Management module.
Andishkadeh Management & Market
--------------------------------
Responsibilities:
- Management main menu
- Chapter navigation
- Lesson navigation
- Lesson content display
- Automatic lesson progress tracking
- Management quiz flow
- Direct integration with Quiz Engine
- Direct integration with Progress
- Direct integration with Statistics
- Safe cancellation
- Safe navigation
Dependencies:
    modules.management.data
    modules.management.service
    core.progress
    core.statistics
    core.quiz_engine
This file is intentionally self-contained at the Telegram handler layer.
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
    record_quiz_result,
)
from core.quiz_engine import (
    global_quiz_engine,
)
from modules.management.service import (
    get_management_chapter,
    get_management_lesson,
    get_management_chapters,
    get_management_lesson_quiz,
    get_management_lessons,
    management_service_health_check,
)
# ==========================================================
# Logging
# ==========================================================
logger = logging.getLogger(__name__)
# ==========================================================
# Constants
# ==========================================================
MODULE_ID = "management"
MODULE_TITLE = "آموزش مدیریت"
CALLBACK_MAIN = "menu_management"
CALLBACK_CHAPTER = "management_chapter"
CALLBACK_LESSON = "management_lesson"
CALLBACK_QUIZ = "management_quiz"
CALLBACK_ANSWER = "quiz_answer"
CALLBACK_CANCEL = "quiz_cancel"
CALLBACK_MAIN_MENU = "menu_main"
# ==========================================================
# Compatibility exports
# ==========================================================
# Kept for compatibility with existing bot.py / registry code.
MANAGEMENT_CHAPTER_LESSONS: dict[str, list[dict[str, Any]]] = {}
# ==========================================================
# Safe helpers
# ==========================================================
def _safe_text(value: Any, default: str = "-") -> str:
    """Return HTML-safe text."""
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    return html.escape(text)
def _get_user_id(update: Update) -> int | None:
    """Return Telegram user ID."""
    user = update.effective_user
    if user is None:
        return None
    return int(user.id)
def _parse_callback(
    update: Update,
) -> tuple[str, str] | None:
    """
    Parse callback data.
    Returns:
        (prefix, value) or None
    """
    query = update.callback_query
    if query is None:
        return None
    data = query.data or ""
    if ":" not in data:
        return None
    prefix, value = data.split(
        ":",
        1,
    )
    if not prefix or not value:
        return None
    return (
        prefix,
        value,
    )
# ==========================================================
# Keyboard helpers
# ==========================================================
def management_main_keyboard(
    chapters: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build the Management main menu."""
    keyboard: list[list[InlineKeyboardButton]] = []
    for chapter in chapters:
        chapter_id = str(
            chapter.get(
                "id",
                "",
            )
        )
        chapter_title = _safe_text(
            chapter.get(
                "title",
                chapter_id,
            )
        )
        if not chapter_id:
            continue
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 {chapter_title}",
                    callback_data=(
                        f"{CALLBACK_CHAPTER}:"
                        f"{chapter_id}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=CALLBACK_MAIN_MENU,
            )
        ]
    )
    return InlineKeyboardMarkup(
        keyboard
    )
def chapter_keyboard(
    chapter_id: str,
    lessons: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build lesson keyboard for a chapter."""
    keyboard: list[list[InlineKeyboardButton]] = []
    for lesson in lessons:
        lesson_id = str(
            lesson.get(
                "id",
                "",
            )
        )
        lesson_title = _safe_text(
            lesson.get(
                "title",
                lesson_id,
            )
        )
        if not lesson_id:
            continue
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📖 {lesson_title}",
                    callback_data=(
                        f"{CALLBACK_LESSON}:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 آموزش مدیریت",
                callback_data=CALLBACK_MAIN,
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data=CALLBACK_MAIN_MENU,
            )
        ]
    )
    return InlineKeyboardMarkup(
        keyboard
    )
def lesson_keyboard(
    chapter_id: str,
    lesson_id: str,
    has_quiz: bool = True,
) -> InlineKeyboardMarkup:
    """Build lesson action keyboard."""
    keyboard: list[list[InlineKeyboardButton]] = []
    if has_quiz:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📝 شروع آزمون درس",
                    callback_data=(
                        f"{CALLBACK_QUIZ}:"
                        f"{MODULE_ID}:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "📚 بازگشت به فصل",
                callback_data=(
                    f"{CALLBACK_CHAPTER}:"
                    f"{chapter_id}"
                ),
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🏠 آموزش مدیریت",
                callback_data=CALLBACK_MAIN,
            )
        ]
    )
    return InlineKeyboardMarkup(
        keyboard
    )
def quiz_answer_keyboard(
    question_index: int,
    options: list[Any],
) -> InlineKeyboardMarkup:
    """
    Build answer keyboard.
    Callback format:
        quiz_answer:<question_index>:<option_index>
    """
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
        if isinstance(option, dict):
            label = (
                option.get("label")
                or option.get("text")
                or option.get("answer")
                or str(option)
            )
        else:
            label = str(option)
        button_text = (
            f"{labels[index]}) "
            f"{_safe_text(label)}"
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    button_text,
                    callback_data=(
                        f"{CALLBACK_ANSWER}:"
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
                callback_data=CALLBACK_CANCEL,
            )
        ]
    )
    return InlineKeyboardMarkup(
        keyboard
    )
def quiz_result_keyboard(
    chapter_id: str,
    lesson_id: str,
) -> InlineKeyboardMarkup:
    """Build quiz result navigation keyboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📖 بازگشت به درس",
                    callback_data=(
                        f"{CALLBACK_LESSON}:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 آموزش مدیریت",
                    callback_data=CALLBACK_MAIN,
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data=CALLBACK_MAIN_MENU,
                )
            ],
        ]
    )
# ==========================================================
# Quiz session helpers
# ==========================================================
QUIZ_CONTEXT_KEY = "management_quiz_session"
def _get_quiz_session(
    context: ContextTypes.DEFAULT_TYPE,
) -> dict[str, Any] | None:
    """Return current Management quiz session."""
    session = context.user_data.get(
        QUIZ_CONTEXT_KEY
    )
    if not isinstance(
        session,
        dict,
    ):
        return None
    return session
def _clear_quiz_session(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Remove current quiz session."""
    context.user_data.pop(
        QUIZ_CONTEXT_KEY,
        None,
    )
def _store_quiz_session(
    context: ContextTypes.DEFAULT_TYPE,
    session: dict[str, Any],
) -> None:
    """Store current quiz session."""
    context.user_data[
        QUIZ_CONTEXT_KEY
    ] = session
# ==========================================================
# Management main menu
# ==========================================================
async def show_management_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show Management module."""
    query = update.callback_query
    if query is not None:
        await query.answer()
    try:
        chapters = get_management_chapters()
    except Exception:
        logger.exception(
            "Failed to load Management chapters."
        )
        text = (
            "❌ <b>خطا در بارگذاری آموزش مدیریت</b>\n\n"
            "در حال حاضر امکان دریافت فصل‌ها وجود ندارد."
        )
        if query is not None:
            await query.edit_message_text(
                text,
                parse_mode="HTML",
            )
        elif update.message is not None:
            await update.message.reply_text(
                text,
                parse_mode="HTML",
            )
        return
    text = (
        "<b>📚 آموزش مدیریت</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "فصل موردنظر خود را انتخاب کنید:"
    )
    keyboard = management_main_keyboard(
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
async def show_management_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show lessons of a Management chapter."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    parsed = _parse_callback(
        update
    )
    if parsed is None:
        await query.edit_message_text(
            "❌ اطلاعات فصل نامعتبر است."
        )
        return
    _, chapter_id = parsed
    try:
        chapter = get_management_chapter(
            chapter_id
        )
        lessons = get_management_lessons(
            chapter_id
        )
    except Exception:
        logger.exception(
            "Failed to load Management chapter %s.",
            chapter_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت اطلاعات فصل.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 آموزش مدیریت",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )
        return
    if chapter is None:
        await query.edit_message_text(
            "❌ فصل موردنظر پیدا نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 آموزش مدیریت",
                            callback_data=CALLBACK_MAIN,
                        )
                    ]
                ]
            ),
        )
        return
    chapter_title = _safe_text(
        chapter.get(
            "title",
            chapter_id,
        )
    )
    text = (
        f"<b>📘 {chapter_title}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"تعداد درس‌ها: <b>{len(lessons)}</b>\n\n"
        "درس موردنظر را انتخاب کنید:"
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=chapter_keyboard(
            chapter_id=chapter_id,
            lessons=lessons,
        ),
    )
# ==========================================================
# Lesson
# ==========================================================
async def show_management_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show one Management lesson."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    parts = data.split(
        ":"
    )
    if len(parts) != 3:
        await query.edit_message_text(
            "❌ اطلاعات درس نامعتبر است."
        )
        return
    _, chapter_id, lesson_id = parts
    telegram_id = _get_user_id(
        update
    )
    if telegram_id is None:
        await query.edit_message_text(
            "❌ اطلاعات کاربر قابل دریافت نیست."
        )
        return
    try:
        lesson = get_management_lesson(
            chapter_id,
            lesson_id,
        )
    except Exception:
        logger.exception(
            (
                "Failed to load lesson "
                "%s/%s."
            ),
            chapter_id,
            lesson_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت محتوای درس.",
            reply_markup=lesson_keyboard(
                chapter_id,
                lesson_id,
                False,
            ),
        )
        return
    if lesson is None:
        await query.edit_message_text(
            "❌ درس موردنظر پیدا نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data=(
                                f"{CALLBACK_CHAPTER}:"
                                f"{chapter_id}"
                            ),
                        )
                    ]
                ]
            ),
        )
        return
    # ------------------------------------------------------
    # Progress: lesson started
    # ------------------------------------------------------
    try:
        mark_lesson_started(
            telegram_id=telegram_id,
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )
    except Exception:
        logger.exception(
            (
                "Failed to mark lesson started: "
                "user=%s lesson=%s/%s"
            ),
            telegram_id,
            chapter_id,
            lesson_id,
        )
    title = _safe_text(
        lesson.get(
            "title",
            lesson_id,
        )
    )
    summary = _safe_text(
        lesson.get(
            "summary",
            "",
        ),
        "",
    )
    content = _safe_text(
        lesson.get(
            "content",
            "",
        ),
        "",
    )
    specialized_tips = _safe_text(
        lesson.get(
            "specialized_tips",
            "",
        ),
        "",
    )
    exam_tips = _safe_text(
        lesson.get(
            "exam_tips",
            "",
        ),
        "",
    )
    examples = _safe_text(
        lesson.get(
            "examples",
            "",
        ),
        "",
    )
    review = _safe_text(
        lesson.get(
            "review",
            "",
        ),
        "",
    )
    sections: list[str] = []
    sections.append(
        f"<b>📖 {title}</b>"
    )
    sections.append(
        "━━━━━━━━━━━━━━━━━━"
    )
    if summary:
        sections.append(
            f"<b>📌 خلاصه درس</b>\n{summary}"
        )
    if content:
        sections.append(
            f"<b>📚 آموزش</b>\n{content}"
        )
    if specialized_tips:
        sections.append(
            (
                "<b>💡 نکات تخصصی</b>\n"
                f"{specialized_tips}"
            )
        )
    if exam_tips:
        sections.append(
            (
                "<b>🎯 نکات آزمونی</b>\n"
                f"{exam_tips}"
            )
        )
    if examples:
        sections.append(
            (
                "<b>🧩 مثال کاربردی</b>\n"
                f"{examples}"
            )
        )
    if review:
        sections.append(
            (
                "<b>🔄 مرور</b>\n"
                f"{review}"
            )
        )
    text = "\n\n".join(
        sections
    )
    # Telegram has a message length limit.
    # Keep the lesson readable instead of letting
    # one enormous educational brick explode.
    if len(text) > 4000:
        text = (
            text[:3900]
            + "\n\n…"
        )
    try:
        quiz = get_management_lesson_quiz(
            chapter_id,
            lesson_id,
        )
    except Exception:
        logger.exception(
            (
                "Failed to load quiz for "
                "lesson %s/%s."
            ),
            chapter_id,
            lesson_id,
        )
        quiz = []
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=lesson_keyboard(
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            has_quiz=bool(quiz),
        ),
    )
# ==========================================================
# Quiz normalization
# ==========================================================
def _normalize_quiz_questions(
    quiz_data: Any,
) -> list[dict[str, Any]]:
    """
    Normalize Management quiz data into a stable structure.
    Supported shapes:
    [
        {
            "question": "...",
            "options": [...],
            "answer": 0
        }
    ]
    or
    [
        {
            "question": "...",
            "options": [...],
            "correct_answer": 0
        }
    ]
    The Quiz Engine receives normalized questions.
    """
    if not isinstance(
        quiz_data,
        list,
    ):
        return []
    normalized: list[dict[str, Any]] = []
    for item in quiz_data:
        if not isinstance(
            item,
            dict,
        ):
            continue
        question = (
            item.get("question")
            or item.get("text")
            or item.get("title")
        )
        options = (
            item.get("options")
            or item.get("answers")
            or []
        )
        correct_answer = item.get(
            "correct_answer"
        )
        if correct_answer is None:
            correct_answer = item.get(
                "answer"
            )
        if correct_answer is None:
            correct_answer = item.get(
                "correct"
            )
        if not question:
            continue
        if not isinstance(
            options,
            list,
        ):
            continue
        if len(options) < 2:
            continue
        try:
            correct_index = int(
                correct_answer
            )
        except (
            TypeError,
            ValueError,
        ):
            continue
        if not (
            0
            <= correct_index
            < len(options)
        ):
            continue
        normalized.append(
            {
                "question": str(
                    question
                ),
                "options": options,
                "correct_answer": correct_index,
            }
        )
    return normalized
# ==========================================================
# Start quiz
# ==========================================================
async def start_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Start Management lesson quiz.
    Flow:
        Service
        ↓
        Quiz Engine
        ↓
        Telegram
    """
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    parts = data.split(
        ":"
    )
    if len(parts) != 4:
        await query.edit_message_text(
            "❌ اطلاعات آزمون نامعتبر است."
        )
        return
    _, module_id, chapter_id, lesson_id = parts
    if module_id != MODULE_ID:
        await query.edit_message_text(
            "❌ ماژول آزمون نامعتبر است."
        )
        return
    telegram_id = _get_user_id(
        update
    )
    if telegram_id is None:
        await query.edit_message_text(
            "❌ اطلاعات کاربر قابل دریافت نیست."
        )
        return
    try:
        quiz_data = get_management_lesson_quiz(
            chapter_id,
            lesson_id,
        )
    except Exception:
        logger.exception(
            (
                "Failed to load Management "
                "quiz %s/%s."
            ),
            chapter_id,
            lesson_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت سوالات آزمون."
        )
        return
    questions = _normalize_quiz_questions(
        quiz_data
    )
    if not questions:
        await query.edit_message_text(
            "📭 برای این درس هنوز آزمونی ثبت نشده است.",
            reply_markup=lesson_keyboard(
                chapter_id,
                lesson_id,
                False,
            ),
        )
        return
    # ------------------------------------------------------
    # Cancel any stale local session
    # ------------------------------------------------------
    _clear_quiz_session(
        context
    )
    # ------------------------------------------------------
    # Start Quiz Engine session
    # ------------------------------------------------------
    try:
        session = global_quiz_engine.start_quiz(
            telegram_id=telegram_id,
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            questions=questions,
        )
    except Exception:
        logger.exception(
            (
                "Failed to start Quiz Engine "
                "for user=%s lesson=%s/%s"
            ),
            telegram_id,
            chapter_id,
            lesson_id,
        )
        await query.edit_message_text(
            "❌ خطا در شروع آزمون.",
            reply_markup=lesson_keyboard(
                chapter_id,
                lesson_id,
                True,
            ),
        )
        return
    # ------------------------------------------------------
    # Store local handler session
    # ------------------------------------------------------
    _store_quiz_session(
        context,
        {
            "telegram_id": telegram_id,
            "module_id": MODULE_ID,
            "chapter_id": chapter_id,
            "lesson_id": lesson_id,
            "questions": questions,
            "engine_session": session,
            "current_question": 0,
        },
    )
    await _render_current_question(
        update,
        context,
    )
# ==========================================================
# Render question
# ==========================================================
async def _render_current_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Render the current quiz question."""
    query = update.callback_query
    if query is None:
        return
    session = _get_quiz_session(
        context
    )
    if session is None:
        await query.edit_message_text(
            "❌ جلسه آزمون پیدا نشد.",
        )
        return
    questions = session.get(
        "questions",
        [],
    )
    question_index = int(
        session.get(
            "current_question",
            0,
        )
    )
    if question_index >= len(
        questions
    ):
        await _complete_management_quiz(
            update,
            context,
        )
        return
    question = questions[
        question_index
    ]
    question_text = _safe_text(
        question.get(
            "question",
            "سوال",
        )
    )
    options = question.get(
        "options",
        [],
    )
    text = (
        "<b>📝 آزمون مدیریت</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"سوال <b>{question_index + 1}</b> "
        f"از <b>{len(questions)}</b>\n\n"
        f"<b>{question_text}</b>\n\n"
        "گزینه صحیح را انتخاب کنید:"
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=quiz_answer_keyboard(
            question_index,
            options,
        ),
    )
# ==========================================================
# Answer quiz
# ==========================================================
async def answer_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Process one Management quiz answer."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    session = _get_quiz_session(
        context
    )
    if session is None:
        await query.edit_message_text(
            "❌ جلسه آزمون پیدا نشد.",
        )
        return
    data = query.data or ""
    parts = data.split(
        ":"
    )
    if len(parts) != 3:
        await query.edit_message_text(
            "❌ پاسخ آزمون نامعتبر است."
        )
        return
    try:
        question_index = int(
            parts[1]
        )
        option_index = int(
            parts[2]
        )
    except (
        TypeError,
        ValueError,
    ):
        await query.edit_message_text(
            "❌ پاسخ آزمون نامعتبر است."
        )
        return
    current_question = int(
        session.get(
            "current_question",
            0,
        )
    )
    if question_index != current_question:
        await query.answer(
            "این سوال دیگر فعال نیست.",
            show_alert=True,
        )
        return
    questions = session.get(
        "questions",
        [],
    )
    if not (
        0
        <= question_index
        < len(questions)
    ):
        await query.edit_message_text(
            "❌ سوال موردنظر پیدا نشد."
        )
        return
    question = questions[
        question_index
    ]
    options = question.get(
        "options",
        [],
    )
    if not (
        0
        <= option_index
        < len(options)
    ):
        await query.answer(
            "گزینه نامعتبر است.",
            show_alert=True,
        )
        return
    # ------------------------------------------------------
    # Submit answer to Quiz Engine
    # ------------------------------------------------------
    try:
        result = global_quiz_engine.submit_answer(
            telegram_id=int(
                session["telegram_id"]
            ),
            answer_index=option_index,
        )
    except Exception:
        logger.exception(
            (
                "Quiz Engine answer failed: "
                "user=%s question=%s"
            ),
            session.get(
                "telegram_id"
            ),
            question_index,
        )
        await query.edit_message_text(
            "❌ خطا در ثبت پاسخ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "❌ لغو آزمون",
                            callback_data=CALLBACK_CANCEL,
                        )
                    ]
                ]
            ),
        )
        return
    # ------------------------------------------------------
    # Handle answer result
    # ------------------------------------------------------
    if isinstance(
        result,
        dict,
    ):
        is_correct = bool(
            result.get(
                "is_correct",
                result.get(
                    "correct",
                    False,
                ),
            )
        )
    else:
        is_correct = bool(
            result
        )
    if is_correct:
        feedback = (
            "✅ <b>پاسخ صحیح است.</b>"
        )
    else:
        feedback = (
            "❌ <b>پاسخ نادرست است.</b>"
        )
    # ------------------------------------------------------
    # Advance question
    # ------------------------------------------------------
    session["current_question"] = (
        question_index + 1
    )
    _store_quiz_session(
        context,
        session,
    )
    # ------------------------------------------------------
    # Show short feedback before next question
    # ------------------------------------------------------
    if (
        question_index + 1
        < len(questions)
    ):
        next_text = (
            f"{feedback}\n\n"
            "سوال بعدی:"
        )
        await query.edit_message_text(
            next_text,
            parse_mode="HTML",
        )
        await _render_current_question(
            update,
            context,
        )
        return
    await _complete_management_quiz(
        update,
        context,
    )
# ==========================================================
# Complete quiz
# ==========================================================
async def _complete_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Complete Management quiz.
    Statistics:
        record_quiz_result()
    Progress:
        mark_lesson_completed()
    """
    query = update.callback_query
    if query is None:
        return
    session = _get_quiz_session(
        context
    )
    if session is None:
        await query.edit_message_text(
            "❌ جلسه آزمون پیدا نشد."
        )
        return
    telegram_id = int(
        session["telegram_id"]
    )
    module_id = str(
        session["module_id"]
    )
    chapter_id = str(
        session["chapter_id"]
    )
    lesson_id = str(
        session["lesson_id"]
    )
    questions = session.get(
        "questions",
        [],
    )
    total_questions = len(
        questions
    )
    # ------------------------------------------------------
    # Complete Quiz Engine
    # ------------------------------------------------------
    try:
        engine_result = (
            global_quiz_engine.complete_quiz(
                telegram_id=telegram_id
            )
        )
    except Exception:
        logger.exception(
            (
                "Failed to complete Quiz Engine "
                "session for user=%s."
            ),
            telegram_id,
        )
        engine_result = None
    # ------------------------------------------------------
    # Extract result
    # ------------------------------------------------------
    correct_answers = 0
    score = 0.0
    if isinstance(
        engine_result,
        dict,
    ):
        correct_answers = int(
            engine_result.get(
                "correct_answers",
                engine_result.get(
                    "correct",
                    0,
                ),
            )
        )
        total_questions = int(
            engine_result.get(
                "total_questions",
                total_questions,
            )
        )
        score = float(
            engine_result.get(
                "score",
                0,
            )
        )
    else:
        # Fallback for engines that expose
        # the result through attributes.
        if engine_result is not None:
            correct_answers = int(
                getattr(
                    engine_result,
                    "correct_answers",
                    0,
                )
            )
            total_questions = int(
                getattr(
                    engine_result,
                    "total_questions",
                    total_questions,
                )
            )
            score = float(
                getattr(
                    engine_result,
                    "score",
                    0,
                )
            )
    # ------------------------------------------------------
    # Safety normalization
    # ------------------------------------------------------
    if total_questions < 0:
        total_questions = 0
    if correct_answers < 0:
        correct_answers = 0
    if correct_answers > total_questions:
        correct_answers = total_questions
    if (
        score <= 0
        and total_questions > 0
    ):
        score = round(
            correct_answers
            / total_questions
            * 100,
            2,
        )
    if score < 0:
        score = 0.0
    if score > 100:
        score = 100.0
    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------
    statistics_saved = False
    if total_questions > 0:
        try:
            record_quiz_result(
                telegram_id=telegram_id,
                module_id=module_id,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
                total_questions=total_questions,
                correct_answers=correct_answers,
                score=score,
            )
            statistics_saved = True
        except Exception:
            logger.exception(
                (
                    "Failed to save Statistics: "
                    "user=%s lesson=%s/%s"
                ),
                telegram_id,
                chapter_id,
                lesson_id,
            )
    # ------------------------------------------------------
    # Progress
    # ------------------------------------------------------
    progress_saved = False
    try:
        mark_lesson_completed(
            telegram_id=telegram_id,
            module_id=module_id,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )
        progress_saved = True
    except Exception:
        logger.exception(
            (
                "Failed to mark lesson completed: "
                "user=%s lesson=%s/%s"
            ),
            telegram_id,
            chapter_id,
            lesson_id,
        )
    # ------------------------------------------------------
    # Clear session
    # ------------------------------------------------------
    _clear_quiz_session(
        context
    )
    # ------------------------------------------------------
    # Result message
    # ------------------------------------------------------
    if score >= 90:
        performance = (
            "🏆 عملکرد عالی"
        )
    elif score >= 75:
        performance = (
            "🌟 عملکرد بسیار خوب"
        )
    elif score >= 60:
        performance = (
            "👍 عملکرد قابل قبول"
        )
    else:
        performance = (
            "📚 نیاز به مرور بیشتر"
        )
    status_lines = []
    if statistics_saved:
        status_lines.append(
            "📊 آمار آزمون ثبت شد."
        )
    if progress_saved:
        status_lines.append(
            "📚 پیشرفت درس ثبت شد."
        )
    text = (
        "<b>🎉 آزمون به پایان رسید</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"تعداد سوالات: <b>{total_questions}</b>\n"
        f"پاسخ صحیح: <b>{correct_answers}</b>\n"
        f"پاسخ غلط: "
        f"<b>{total_questions - correct_answers}</b>\n"
        f"نمره: <b>{score:.2f}%</b>\n\n"
        f"<b>{performance}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
    )
    if status_lines:
        text += (
            "\n".join(
                status_lines
            )
            + "\n"
        )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=quiz_result_keyboard(
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        ),
    )
# ==========================================================
# Cancel quiz
# ==========================================================
async def cancel_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Cancel active Management quiz."""
    query = update.callback_query
    if query is None:
        return
    await query.answer(
        "آزمون لغو شد."
    )
    session = _get_quiz_session(
        context
    )
    if session is not None:
        telegram_id = int(
            session.get(
                "telegram_id",
                0,
            )
        )
        if telegram_id:
            try:
                global_quiz_engine.cancel_quiz(
                    telegram_id=telegram_id
                )
            except Exception:
                logger.exception(
                    (
                        "Failed to cancel "
                        "Quiz Engine session "
                        "for user=%s."
                    ),
                    telegram_id,
                )
        chapter_id = str(
            session.get(
                "chapter_id",
                "",
            )
        )
        lesson_id = str(
            session.get(
                "lesson_id",
                "",
            )
        )
    else:
        chapter_id = ""
        lesson_id = ""
    _clear_quiz_session(
        context
    )
    if chapter_id and lesson_id:
        keyboard = lesson_keyboard(
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            has_quiz=True,
        )
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 آموزش مدیریت",
                        callback_data=CALLBACK_MAIN,
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 منوی اصلی",
                        callback_data=CALLBACK_MAIN_MENU,
                    )
                ],
            ]
        )
    await query.edit_message_text(
        (
            "❌ <b>آزمون لغو شد.</b>\n\n"
            "نتیجه‌ای برای این آزمون ثبت نشد."
        ),
        parse_mode="HTML",
        reply_markup=keyboard,
    )
# ==========================================================
# Callback router
# ==========================================================
async def route_management_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Optional dedicated Management callback router.
    This can be used when bot.py prefers a module-specific
    CallbackQueryHandler instead of routing through core.menu.
    """
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    if data == CALLBACK_MAIN:
        await show_management_menu(
            update,
            context,
        )
        return
    if data.startswith(
        f"{CALLBACK_CHAPTER}:"
    ):
        await show_management_chapter(
            update,
            context,
        )
        return
    if data.startswith(
        f"{CALLBACK_LESSON}:"
    ):
        await show_management_lesson(
            update,
            context,
        )
        return
    if data.startswith(
        f"{CALLBACK_QUIZ}:"
    ):
        await start_management_quiz(
            update,
            context,
        )
        return
    if data.startswith(
        f"{CALLBACK_ANSWER}:"
    ):
        await answer_management_quiz(
            update,
            context,
        )
        return
    if data == CALLBACK_CANCEL:
        await cancel_management_quiz(
            update,
            context,
        )
        return
# ==========================================================
# Health check
# ==========================================================
def management_handlers_health_check() -> bool:
    """
    Check whether the Management handler dependencies
    are available.
    Does not contact Telegram.
    """
    try:
        if not management_service_health_check():
            return False
        if not callable(
            mark_lesson_started
        ):
            return False
        if not callable(
            mark_lesson_completed
        ):
            return False
        if not callable(
            record_quiz_result
        ):
            return False
        if global_quiz_engine is None:
            return False
        return True
    except Exception:
        logger.exception(
            "Management handlers health check failed."
        )
        return False
# ==========================================================
# Module initialization
# ==========================================================
def initialize_management_handlers() -> bool:
    """
    Initialize Management handler compatibility data.
    The actual curriculum remains owned by data.py/service.py.
    """
    global MANAGEMENT_CHAPTER_LESSONS
    try:
        chapters = get_management_chapters()
        registry_data: dict[
            str,
            list[dict[str, Any]],
        ] = {}
        for chapter in chapters:
            chapter_id = str(
                chapter.get(
                    "id",
                    "",
                )
            )
            if not chapter_id:
                continue
            try:
                lessons = get_management_lessons(
                    chapter_id
                )
            except Exception:
                logger.exception(
                    (
                        "Failed to load lessons "
                        "for chapter %s."
                    ),
                    chapter_id,
                )
                lessons = []
            registry_data[
                chapter_id
            ] = lessons
        MANAGEMENT_CHAPTER_LESSONS = (
            registry_data
        )
        logger.info(
            (
                "Management handlers initialized: "
                "chapters=%s lessons=%s"
            ),
            len(registry_data),
            sum(
                len(items)
                for items in registry_data.values()
            ),
        )
        return True
    except Exception:
        logger.exception(
            "Failed to initialize Management handlers."
        )
        return False
# ==========================================================
# Automatic initialization
# ==========================================================
try:
    initialize_management_handlers()
except Exception:
    logger.exception(
        "Management handler auto initialization failed."
    )
