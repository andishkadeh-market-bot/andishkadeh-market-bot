"""
Telegram handlers for the International Trade module.
Andishkadeh Management & Market
Features:
- International Trade main menu
- Chapter list
- Lesson list
- Lesson content
- Progress integration
- Quiz Engine integration
- Statistics integration
- Safe navigation
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
from core.quiz_engine import (
    QuizEngine,
)
from core.statistics import (
    record_quiz_result,
)
from modules.international_trade.service import (
    get_chapters,
    get_lesson,
    get_lessons,
    get_module_info,
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
# ==========================================================
# Helpers
# ==========================================================
def _safe_text(value: Any, default: str = "-") -> str:
    """Convert a value to safe Telegram HTML text."""
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    return html.escape(text)
def _get_chapter_id(
    chapter: dict[str, Any],
) -> str | None:
    """Extract chapter ID from supported data formats."""
    value = (
        chapter.get("id")
        or chapter.get("chapter_id")
    )
    if value is None:
        return None
    return str(value)
def _get_lesson_id(
    lesson: dict[str, Any],
) -> str | None:
    """Extract lesson ID from supported data formats."""
    value = (
        lesson.get("id")
        or lesson.get("lesson_id")
    )
    if value is None:
        return None
    return str(value)
def _get_title(
    item: dict[str, Any],
    fallback: str = "-",
) -> str:
    """Extract a title from a data object."""
    return str(
        item.get("title")
        or item.get("name")
        or fallback
    )
# ==========================================================
# Keyboards
# ==========================================================
def international_trade_menu_keyboard() -> InlineKeyboardMarkup:
    """Main keyboard for International Trade."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📚 فصل‌ها",
                    callback_data="trade_chapters",
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
def chapters_keyboard(
    chapters: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build chapter keyboard."""
    keyboard: list[
        list[InlineKeyboardButton]
    ] = []
    for chapter in chapters:
        chapter_id = _get_chapter_id(
            chapter
        )
        if not chapter_id:
            continue
        title = _get_title(
            chapter,
            chapter_id,
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📘 {title}",
                    callback_data=(
                        f"trade_chapter:{chapter_id}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 تجارت بین‌الملل",
                callback_data="menu_international_trade",
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
    return InlineKeyboardMarkup(
        keyboard
    )
def lessons_keyboard(
    chapter_id: str,
    lessons: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Build lesson keyboard."""
    keyboard: list[
        list[InlineKeyboardButton]
    ] = []
    for lesson in lessons:
        lesson_id = _get_lesson_id(
            lesson
        )
        if not lesson_id:
            continue
        title = _get_title(
            lesson,
            lesson_id,
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📖 {title}",
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
                "🔙 فصل‌ها",
                callback_data="trade_chapters",
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
    return InlineKeyboardMarkup(
        keyboard
    )
def lesson_keyboard(
    chapter_id: str,
    lesson_id: str,
    has_quiz: bool = False,
) -> InlineKeyboardMarkup:
    """Build lesson navigation keyboard."""
    keyboard: list[
        list[InlineKeyboardButton]
    ] = []
    if has_quiz:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📝 آزمون درس",
                    callback_data=(
                        f"trade_quiz:"
                        f"{chapter_id}:"
                        f"{lesson_id}"
                    ),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "✅ تکمیل درس",
                callback_data=(
                    f"trade_complete:"
                    f"{chapter_id}:"
                    f"{lesson_id}"
                ),
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 درس‌ها",
                callback_data=(
                    f"trade_chapter:"
                    f"{chapter_id}"
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
    return InlineKeyboardMarkup(
        keyboard
    )
def quiz_keyboard(
    chapter_id: str,
    lesson_id: str,
    question_index: int,
    options: list[str],
) -> InlineKeyboardMarkup:
    """Build quiz answer keyboard."""
    keyboard: list[
        list[InlineKeyboardButton]
    ] = []
    for index, option in enumerate(
        options
    ):
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{chr(65 + index)}) {option}",
                    callback_data=(
                        f"trade_quiz_answer:"
                        f"{chapter_id}:"
                        f"{lesson_id}:"
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
                callback_data=(
                    f"trade_quiz_cancel:"
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
# Main menu
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
        module_info = get_module_info()
        title = _safe_text(
            module_info.get(
                "title",
                MODULE_TITLE,
            )
        )
        description = _safe_text(
            module_info.get(
                "description",
                "آموزش تخصصی تجارت بین‌الملل",
            )
        )
    except Exception:
        logger.exception(
            "Failed to load International Trade module info."
        )
        title = MODULE_TITLE
        description = (
            "آموزش تخصصی تجارت بین‌الملل"
        )
    text = (
        f"🌍 <b>{title}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{description}\n\n"
        "در این بخش می‌توانید مباحث تجارت بین‌الملل "
        "را به‌صورت فصل‌به‌فصل مطالعه کنید."
    )
    if query is not None:
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    if update.message is not None:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=international_trade_menu_keyboard(),
        )
# ==========================================================
# Chapters
# ==========================================================
async def show_international_trade_chapters(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show International Trade chapters."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    try:
        chapters = get_chapters()
    except Exception:
        logger.exception(
            "Failed to load International Trade chapters."
        )
        await query.edit_message_text(
            "❌ خطا در دریافت فصل‌های تجارت بین‌الملل.",
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
    if not chapters:
        await query.edit_message_text(
            (
                "🌍 <b>تجارت بین‌الملل</b>\n\n"
                "هنوز فصلی برای این ماژول ثبت نشده است."
            ),
            parse_mode="HTML",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    text_lines = [
        "🌍 <b>فصل‌های تجارت بین‌الملل</b>",
        "━━━━━━━━━━━━━━━━━━",
    ]
    for index, chapter in enumerate(
        chapters,
        start=1,
    ):
        title = _safe_text(
            _get_title(
                chapter,
                f"فصل {index}",
            )
        )
        text_lines.append(
            f"{index}. 📘 {title}"
        )
    text_lines.extend(
        [
            "━━━━━━━━━━━━━━━━━━",
            "فصل موردنظر را انتخاب کنید:",
        ]
    )
    await query.edit_message_text(
        "\n".join(text_lines),
        parse_mode="HTML",
        reply_markup=chapters_keyboard(
            chapters
        ),
    )
# ==========================================================
# Chapter
# ==========================================================
async def show_international_trade_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show lessons inside a chapter."""
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
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    try:
        lessons = get_lessons(
            chapter_id
        )
    except Exception:
        logger.exception(
            "Failed to load lessons for chapter %s.",
            chapter_id,
        )
        await query.edit_message_text(
            "❌ خطا در دریافت درس‌های فصل.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 فصل‌ها",
                            callback_data="trade_chapters",
                        )
                    ]
                ]
            ),
        )
        return
    if not lessons:
        await query.edit_message_text(
            (
                "📘 <b>فصل تجارت بین‌الملل</b>\n"
                f"شناسه فصل: <code>{_safe_text(chapter_id)}</code>\n\n"
                "هنوز درسی برای این فصل ثبت نشده است."
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 فصل‌ها",
                            callback_data="trade_chapters",
                        )
                    ]
                ]
            ),
        )
        return
    text_lines = [
        (
            "📘 <b>درس‌های فصل</b>\n"
            f"فصل: <code>{_safe_text(chapter_id)}</code>"
        ),
        "━━━━━━━━━━━━━━━━━━",
    ]
    for index, lesson in enumerate(
        lessons,
        start=1,
    ):
        title = _safe_text(
            _get_title(
                lesson,
                f"درس {index}",
            )
        )
        text_lines.append(
            f"{index}. 📖 {title}"
        )
    text_lines.extend(
        [
            "━━━━━━━━━━━━━━━━━━",
            "درس موردنظر را انتخاب کنید:",
        ]
    )
    await query.edit_message_text(
        "\n".join(text_lines),
        parse_mode="HTML",
        reply_markup=lessons_keyboard(
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
    """Show lesson content and register lesson start."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, chapter_id, lesson_id = data.split(
            ":",
            2,
        )
    except ValueError:
        await query.edit_message_text(
            "❌ اطلاعات درس نامعتبر است.",
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
        lesson = get_lesson(
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
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 درس‌ها",
                            callback_data=(
                                f"trade_chapter:"
                                f"{chapter_id}"
                            ),
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
                            "🔙 درس‌ها",
                            callback_data=(
                                f"trade_chapter:"
                                f"{chapter_id}"
                            ),
                        )
                    ]
                ]
            ),
        )
        return
    user = update.effective_user
    if user is not None:
        try:
            mark_lesson_started(
                telegram_id=user.id,
                module_id=MODULE_ID,
                chapter_id=chapter_id,
                lesson_id=lesson_id,
            )
        except Exception:
            logger.exception(
                (
                    "Failed to mark International "
                    "Trade lesson started: %s/%s"
                ),
                chapter_id,
                lesson_id,
            )
    title = _safe_text(
        _get_title(
            lesson,
            lesson_id,
        )
    )
    content = (
        lesson.get("content")
        or lesson.get("text")
        or lesson.get("lesson")
        or ""
    )
    content = _safe_text(
        content,
        "محتوای این درس هنوز ثبت نشده است.",
    )
    has_quiz = bool(
        lesson.get("quiz")
        or lesson.get("questions")
    )
    text = (
        f"🌍 <b>{title}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{content}\n\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=lesson_keyboard(
            chapter_id,
            lesson_id,
            has_quiz=has_quiz,
        ),
    )
# ==========================================================
# Complete lesson
# ==========================================================
async def complete_international_trade_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Mark lesson as completed."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    data = query.data or ""
    try:
        _, chapter_id, lesson_id = data.split(
            ":",
            2,
        )
    except ValueError:
        await query.edit_message_text(
            "❌ اطلاعات درس نامعتبر است.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    user = update.effective_user
    if user is None:
        return
    try:
        mark_lesson_completed(
            telegram_id=user.id,
            module_id=MODULE_ID,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
        )
    except Exception:
        logger.exception(
            (
                "Failed to mark International "
                "Trade lesson completed: %s/%s"
            ),
            chapter_id,
            lesson_id,
        )
        await query.edit_message_text(
            "❌ ثبت تکمیل درس انجام نشد.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 منوی تجارت بین‌الملل",
                            callback_data=(
                                "menu_international_trade"
                            ),
                        )
                    ]
                ]
            ),
        )
        return
    await query.edit_message_text(
        (
            "✅ <b>درس با موفقیت تکمیل شد</b>\n\n"
            f"🌍 ماژول: {_safe_text(MODULE_TITLE)}\n"
            f"📘 فصل: <code>{_safe_text(chapter_id)}</code>\n"
            f"📖 درس: <code>{_safe_text(lesson_id)}</code>\n\n"
            "پیشرفت شما در سیستم ثبت شد."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 بازگشت به درس",
                        callback_data=(
                            f"trade_lesson:"
                            f"{chapter_id}:"
                            f"{lesson_id}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 درس‌ها",
                        callback_data=(
                            f"trade_chapter:"
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
# ==========================================================
# Quiz helpers
# ==========================================================
def _extract_questions(
    lesson: dict[str, Any],
) -> list[dict[str, Any]]:
    """Extract quiz questions from lesson data."""
    questions = (
        lesson.get("quiz")
        or lesson.get("questions")
        or []
    )
    if isinstance(questions, dict):
        questions = questions.get(
            "questions",
            [],
        )
    if not isinstance(
        questions,
        list,
    ):
        return []
    return [
        item
        for item in questions
        if isinstance(item, dict)
    ]
def _question_text(
    question: dict[str, Any],
) -> str:
    """Extract question text."""
    return str(
        question.get("question")
        or question.get("text")
        or question.get("title")
        or "سوال"
    )
def _question_options(
    question: dict[str, Any],
) -> list[str]:
    """Extract question options."""
    options = (
        question.get("options")
        or question.get("choices")
        or []
    )
    if not isinstance(
        options,
        list,
    ):
        return []
    return [
        str(option)
        for option in options
    ]
def _correct_option(
    question: dict[str, Any],
) -> int | None:
    """Extract correct option index."""
    value = (
        question.get("correct")
        if "correct" in question
        else question.get("answer")
    )
    if value is None:
        value = question.get(
            "correct_index"
        )
    if isinstance(
        value,
        int,
    ):
        return value
    if isinstance(
        value,
        str,
    ):
        value = value.strip()
        if value.upper() in {
            "A",
            "B",
            "C",
            "D",
        }:
            return ord(
                value.upper()
            ) - ord("A")
        try:
            return int(value)
        except ValueError:
            return None
    return None
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
    try:
        _, chapter_id, lesson_id = data.split(
            ":",
            2,
        )
    except ValueError:
        await query.edit_message_text(
            "❌ اطلاعات آزمون نامعتبر است.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    try:
        lesson = get_lesson(
            chapter_id,
            lesson_id,
        )
    except Exception:
        logger.exception(
            "Failed to load quiz lesson."
        )
        await query.edit_message_text(
            "❌ خطا در دریافت آزمون.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    if not lesson:
        await query.edit_message_text(
            "❌ درس موردنظر پیدا نشد.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    questions = _extract_questions(
        lesson
    )
    if not questions:
        await query.edit_message_text(
            (
                "📝 برای این درس هنوز آزمونی "
                "ثبت نشده است."
            ),
            reply_markup=lesson_keyboard(
                chapter_id,
                lesson_id,
                has_quiz=False,
            ),
        )
        return
    context.user_data[
        "international_trade_quiz"
    ] = {
        "module_id": MODULE_ID,
        "chapter_id": chapter_id,
        "lesson_id": lesson_id,
        "questions": questions,
        "current": 0,
        "correct": 0,
    }
    await _show_trade_quiz_question(
        update,
        context,
    )
# ==========================================================
# Show quiz question
# ==========================================================
async def _show_trade_quiz_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Display current quiz question."""
    query = update.callback_query
    if query is None:
        return
    state = context.user_data.get(
        "international_trade_quiz"
    )
    if not state:
        await query.edit_message_text(
            "❌ آزمون فعال نیست.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    current = int(
        state.get(
            "current",
            0,
        )
    )
    questions = state.get(
        "questions",
        [],
    )
    if current >= len(questions):
        await finish_international_trade_quiz(
            update,
            context,
        )
        return
    question = questions[current]
    text = (
        f"📝 <b>آزمون تجارت بین‌الملل</b>\n"
        f"سوال {current + 1} از {len(questions)}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{_safe_text(_question_text(question))}"
    )
    options = _question_options(
        question
    )
    if not options:
        await query.edit_message_text(
            (
                "❌ این سوال گزینه معتبری ندارد."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "❌ لغو آزمون",
                            callback_data=(
                                f"trade_quiz_cancel:"
                                f"{state['chapter_id']}:"
                                f"{state['lesson_id']}"
                            ),
                        )
                    ]
                ]
            ),
        )
        return
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=quiz_keyboard(
            state["chapter_id"],
            state["lesson_id"],
            current,
            options,
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
    state = context.user_data.get(
        "international_trade_quiz"
    )
    if not state:
        await query.edit_message_text(
            "❌ آزمون فعال نیست.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    data = query.data or ""
    try:
        parts = data.split(":")
        question_index = int(
            parts[3]
        )
        selected_index = int(
            parts[4]
        )
    except (
        ValueError,
        IndexError,
    ):
        await query.edit_message_text(
            "❌ پاسخ آزمون نامعتبر است.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    current = int(
        state.get(
            "current",
            0,
        )
    )
    if question_index != current:
        await _show_trade_quiz_question(
            update,
            context,
        )
        return
    questions = state.get(
        "questions",
        [],
    )
    if current >= len(questions):
        await finish_international_trade_quiz(
            update,
            context,
        )
        return
    question = questions[current]
    correct_index = _correct_option(
        question
    )
    if (
        correct_index is not None
        and selected_index == correct_index
    ):
        state["correct"] = int(
            state.get(
                "correct",
                0,
            )
        ) + 1
    state["current"] = current + 1
    if state["current"] >= len(
        questions
    ):
        await finish_international_trade_quiz(
            update,
            context,
        )
        return
    await _show_trade_quiz_question(
        update,
        context,
    )
# ==========================================================
# Finish quiz
# ==========================================================
async def finish_international_trade_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Finish quiz and save statistics."""
    query = update.callback_query
    if query is None:
        return
    state = context.user_data.get(
        "international_trade_quiz"
    )
    if not state:
        await query.edit_message_text(
            "❌ آزمون فعال نیست.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    user = update.effective_user
    questions = state.get(
        "questions",
        [],
    )
    total = len(questions)
    correct = int(
        state.get(
            "correct",
            0,
        )
    )
    wrong = max(
        total - correct,
        0,
    )
    score = (
        (correct / total) * 100
        if total
        else 0
    )
    if user is not None:
        try:
            record_quiz_result(
                telegram_id=user.id,
                module_id=MODULE_ID,
                chapter_id=state[
                    "chapter_id"
                ],
                lesson_id=state[
                    "lesson_id"
                ],
                total_questions=total,
                correct_answers=correct,
                score=score,
            )
        except Exception:
            logger.exception(
                "Failed to record International Trade quiz statistics."
            )
    context.user_data.pop(
        "international_trade_quiz",
        None,
    )
    await query.edit_message_text(
        (
            "🏁 <b>آزمون به پایان رسید</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"📚 تعداد سوالات: <b>{total}</b>\n"
            f"✅ پاسخ صحیح: <b>{correct}</b>\n"
            f"❌ پاسخ غلط: <b>{wrong}</b>\n"
            f"📊 نمره: <b>{score:.2f}%</b>\n\n"
            "نتیجه آزمون در Statistics ثبت شد."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 بازگشت به درس",
                        callback_data=(
                            f"trade_lesson:"
                            f"{state['chapter_id']}:"
                            f"{state['lesson_id']}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 فصل‌ها",
                        callback_data="trade_chapters",
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
    """Cancel current quiz."""
    query = update.callback_query
    if query is None:
        return
    await query.answer(
        "آزمون لغو شد.",
        show_alert=False,
    )
    data = query.data or ""
    try:
        _, chapter_id, lesson_id = data.split(
            ":",
            2,
        )
    except ValueError:
        context.user_data.pop(
            "international_trade_quiz",
            None,
        )
        await query.edit_message_text(
            "❌ آزمون لغو شد.",
            reply_markup=international_trade_menu_keyboard(),
        )
        return
    context.user_data.pop(
        "international_trade_quiz",
        None,
    )
    await query.edit_message_text(
        (
            "❌ <b>آزمون لغو شد</b>\n\n"
            "نتیجه‌ای برای این آزمون ثبت نشد."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 بازگشت به درس",
                        callback_data=(
                            f"trade_lesson:"
                            f"{chapter_id}:"
                            f"{lesson_id}"
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
# ==========================================================
# Callback router
# ==========================================================
async def route_international_trade_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Route International Trade callbacks."""
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    if data == "menu_international_trade":
        await show_international_trade_menu(
            update,
            context,
        )
        return
    if data == "trade_chapters":
        await show_international_trade_chapters(
            update,
            context,
        )
        return
    if data.startswith(
        "trade_chapter:"
    ):
        await show_international_trade_chapter(
            update,
            context,
        )
        return
    if data.startswith(
        "trade_lesson:"
    ):
        await show_international_trade_lesson(
            update,
            context,
        )
        return
    if data.startswith(
        "trade_complete:"
    ):
        await complete_international_trade_lesson(
            update,
            context,
        )
        return
    if data.startswith(
        "trade_quiz:"
    ):
        await start_international_trade_quiz(
            update,
            context,
        )
        return
    if data.startswith(
        "trade_quiz_answer:"
    ):
        await answer_international_trade_quiz(
            update,
            context,
        )
        return
    if data.startswith(
        "trade_quiz_cancel:"
    ):
        await cancel_international_trade_quiz(
            update,
            context,
        )
        return
# ==========================================================
# Health check
# ==========================================================
def international_trade_handlers_health_check() -> bool:
    """Basic handler-layer health check."""
    try:
        return bool(
            MODULE_ID
            and MODULE_TITLE
        )
    except Exception:
        return False
