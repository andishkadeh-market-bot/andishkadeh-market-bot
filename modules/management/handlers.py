"""
Telegram handlers for the Management education module.

Supported:
- Chapter 1: Lessons 01-12
- Chapter 2: Lessons 13-19
- Lesson navigation
- Lesson display
- Lesson quizzes
- Quiz result
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from core.quiz import (
    QuizSession,
    build_questions,
    format_quiz_result,
)
from core.utils import send_long_text

from modules.management.curriculum import (
    MANAGEMENT_CURRICULUM,
)

from modules.management.lessons.lesson_01 import LESSON_01
from modules.management.lessons.lesson_02 import LESSON_02
from modules.management.lessons.lesson_03 import LESSON_03
from modules.management.lessons.lesson_04 import LESSON_04
from modules.management.lessons.lesson_05 import LESSON_05
from modules.management.lessons.lesson_06 import LESSON_06
from modules.management.lessons.lesson_07 import LESSON_07
from modules.management.lessons.lesson_08 import LESSON_08
from modules.management.lessons.lesson_09 import LESSON_09
from modules.management.lessons.lesson_10 import LESSON_10
from modules.management.lessons.lesson_11 import LESSON_11
from modules.management.lessons.lesson_12 import LESSON_12

from modules.management.lessons.lesson_13 import LESSON_13
from modules.management.lessons.lesson_14 import LESSON_14
from modules.management.lessons.lesson_15 import LESSON_15
from modules.management.lessons.lesson_16 import LESSON_16
from modules.management.lessons.lesson_17 import LESSON_17
from modules.management.lessons.lesson_18 import LESSON_18
from modules.management.lessons.lesson_19 import LESSON_19


# ==========================================================
# Quiz session storage
# ==========================================================

QUIZ_SESSIONS: dict[int, QuizSession] = {}

QUIZ_LESSON_CONTEXT: dict[int, dict] = {}


# ==========================================================
# Available lessons
# ==========================================================

MANAGEMENT_LESSONS = {
    LESSON_01["id"]: LESSON_01,
    LESSON_02["id"]: LESSON_02,
    LESSON_03["id"]: LESSON_03,
    LESSON_04["id"]: LESSON_04,
    LESSON_05["id"]: LESSON_05,
    LESSON_06["id"]: LESSON_06,
    LESSON_07["id"]: LESSON_07,
    LESSON_08["id"]: LESSON_08,
    LESSON_09["id"]: LESSON_09,
    LESSON_10["id"]: LESSON_10,
    LESSON_11["id"]: LESSON_11,
    LESSON_12["id"]: LESSON_12,

    LESSON_13["id"]: LESSON_13,
    LESSON_14["id"]: LESSON_14,
    LESSON_15["id"]: LESSON_15,
    LESSON_16["id"]: LESSON_16,
    LESSON_17["id"]: LESSON_17,
    LESSON_18["id"]: LESSON_18,
    LESSON_19["id"]: LESSON_19,
}


# ==========================================================
# Lesson order
# ==========================================================

MANAGEMENT_CHAPTER_01_LESSONS = [
    LESSON_01,
    LESSON_02,
    LESSON_03,
    LESSON_04,
    LESSON_05,
    LESSON_06,
    LESSON_07,
    LESSON_08,
    LESSON_09,
    LESSON_10,
    LESSON_11,
    LESSON_12,
]


MANAGEMENT_CHAPTER_02_LESSONS = [
    LESSON_13,
    LESSON_14,
    LESSON_15,
    LESSON_16,
    LESSON_17,
    LESSON_18,
    LESSON_19,
]


MANAGEMENT_CHAPTER_LESSONS = {
    "management_basics": MANAGEMENT_CHAPTER_01_LESSONS,
    "planning": MANAGEMENT_CHAPTER_02_LESSONS,
}


# ==========================================================
# Helpers
# ==========================================================

def get_chapter(
    chapter_id: str,
) -> dict | None:
    """Return a management chapter by ID."""

    return next(
        (
            chapter
            for chapter in MANAGEMENT_CURRICULUM
            if chapter["id"] == chapter_id
        ),
        None,
    )


def get_chapter_lessons(
    chapter_id: str,
) -> list[dict]:
    """Return detailed lessons for a chapter."""

    return MANAGEMENT_CHAPTER_LESSONS.get(
        chapter_id,
        [],
    )


def get_management_lesson(
    chapter_id: str,
    lesson_index: int,
) -> dict | None:
    """Return detailed lesson content."""

    if lesson_index < 0:
        return None

    lessons = get_chapter_lessons(
        chapter_id
    )

    if lesson_index >= len(lessons):
        return None

    lesson = lessons[lesson_index]

    return MANAGEMENT_LESSONS.get(
        lesson["id"]
    )


def get_lesson_location(
    lesson_id: str,
) -> tuple[str, int] | None:
    """Return chapter ID and lesson index."""

    for chapter_id, lessons in (
        MANAGEMENT_CHAPTER_LESSONS.items()
    ):
        for index, lesson in enumerate(lessons):
            if lesson["id"] == lesson_id:
                return chapter_id, index

    return None


def get_lesson_index(
    lesson_id: str,
) -> int | None:
    """Return lesson index inside its chapter."""

    location = get_lesson_location(
        lesson_id
    )

    if location is None:
        return None

    return location[1]


# ==========================================================
# Management menu
# ==========================================================

def management_menu_keyboard() -> InlineKeyboardMarkup:
    """Create management chapter menu."""

    keyboard = []

    for chapter in MANAGEMENT_CURRICULUM:
        keyboard.append(
            [
                InlineKeyboardButton(
                    chapter["title"],
                    callback_data=(
                        f"management_chapter:"
                        f"{chapter['id']}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="menu_main",
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================================
# Chapter menu
# ==========================================================

def management_chapter_keyboard(
    chapter_id: str,
) -> InlineKeyboardMarkup:
    """Create lesson menu for a chapter."""

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data="menu_management",
                    )
                ]
            ]
        )

    keyboard = []

    detailed_lessons = get_chapter_lessons(
        chapter_id
    )

    for index, lesson_title in enumerate(
        chapter["lessons"]
    ):
        if index < len(detailed_lessons):
            prefix = "📖"
        else:
            prefix = "🔒"

        keyboard.append(
            [
                InlineKeyboardButton(
                    (
                        f"{prefix} درس "
                        f"{index + 1}: "
                        f"{lesson_title}"
                    ),
                    callback_data=(
                        f"management_lesson:"
                        f"{chapter_id}:"
                        f"{index}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به فصل‌ها",
                callback_data="menu_management",
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================================
# Management main menu
# ==========================================================

async def show_management_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show management chapters."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    text = """
<b>📚 آموزش مدیریت</b>

یک مسیر آموزشی مرحله‌ای برای یادگیری مدیریت،
از مفاهیم پایه تا مباحث تخصصی.

📖 درسنامه جامع
🎯 اهداف یادگیری
🔍 مفاهیم کلیدی
💡 نکات تخصصی
📝 نکات آزمونی
📌 مثال کاربردی
❓ آزمون
📊 تحلیل نتیجه
🔄 مرور

<b>فصل موردنظر را انتخاب کنید:</b>
"""

    await query.edit_message_text(
        text,
        reply_markup=management_menu_keyboard(),
        parse_mode="HTML",
    )


# ==========================================================
# Chapter lessons
# ==========================================================

async def show_management_chapter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show lessons inside a management chapter."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    if ":" not in data:
        return

    _, chapter_id = data.split(
        ":",
        1,
    )

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        await query.edit_message_text(
            "فصل موردنظر پیدا نشد.",
            reply_markup=management_menu_keyboard(),
        )
        return

    detailed_count = len(
        get_chapter_lessons(
            chapter_id
        )
    )

    text = f"""
<b>{chapter["title"]}</b>

📚 تعداد درس‌ها: {len(chapter["lessons"])}

🟢 درس‌های آماده: {detailed_count}

هر درس شامل:

📖 درسنامه
🎯 اهداف یادگیری
🔍 مفاهیم کلیدی
💡 نکات تخصصی
📝 نکات آزمونی
📌 مثال کاربردی
📝 آزمون
🔄 مرور و جمع‌بندی

<b>درس موردنظر را انتخاب کنید:</b>
"""

    await query.edit_message_text(
        text,
        reply_markup=management_chapter_keyboard(
            chapter_id
        ),
        parse_mode="HTML",
    )


# ==========================================================
# Lesson formatting
# ==========================================================

def format_lesson_text(
    lesson: dict,
) -> str:
    """Build a complete lesson message."""

    objectives = "\n".join(
        f"• {item}"
        for item in lesson.get(
            "objectives",
            [],
        )
    )

    concepts = "\n\n".join(
        (
            f"<b>{item['title']}</b>\n"
            f"{item['description']}"
        )
        for item in lesson.get(
            "key_concepts",
            [],
        )
    )

    specialized = "\n".join(
        f"• {item}"
        for item in lesson.get(
            "specialized_points",
            [],
        )
    )

    exam_points = "\n".join(
        f"• {item}"
        for item in lesson.get(
            "exam_points",
            [],
        )
    )

    review = "\n".join(
        f"• {item}"
        for item in lesson.get(
            "review",
            [],
        )
    )

    return f"""
<b>{lesson["title"]}</b>

━━━━━━━━━━━━━━

🎯 <b>اهداف یادگیری</b>

{objectives}

━━━━━━━━━━━━━━

📖 <b>درسنامه</b>

{lesson["lesson"]}

━━━━━━━━━━━━━━

🔍 <b>مفاهیم کلیدی</b>

{concepts}

━━━━━━━━━━━━━━

💡 <b>نکات تخصصی</b>

{specialized}

━━━━━━━━━━━━━━

📝 <b>نکات آزمونی</b>

{exam_points}

━━━━━━━━━━━━━━

📌 <b>مثال کاربردی</b>

{lesson["practical_example"]}

━━━━━━━━━━━━━━

🔄 <b>مرور و جمع‌بندی</b>

{review}
"""


# ==========================================================
# Lesson navigation
# ==========================================================

def lesson_navigation_keyboard(
    chapter_id: str,
    lesson_index: int,
    lesson: dict,
) -> InlineKeyboardMarkup:
    """Create lesson navigation keyboard."""

    keyboard = []

    if lesson.get("quiz"):
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📝 شروع آزمون درس",
                    callback_data=(
                        f"management_quiz:"
                        f"{lesson['id']}"
                    ),
                )
            ]
        )

    navigation_row = []

    if lesson_index > 0:
        navigation_row.append(
            InlineKeyboardButton(
                "⬅️ درس قبلی",
                callback_data=(
                    f"management_lesson:"
                    f"{chapter_id}:"
                    f"{lesson_index - 1}"
                ),
            )
        )

    chapter = get_chapter(
        chapter_id
    )

    if (
        chapter is not None
        and lesson_index + 1
        < len(chapter["lessons"])
    ):
        navigation_row.append(
            InlineKeyboardButton(
                "درس بعدی ➡️",
                callback_data=(
                    f"management_lesson:"
                    f"{chapter_id}:"
                    f"{lesson_index + 1}"
                ),
            )
        )

    if navigation_row:
        keyboard.append(
            navigation_row
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت به درس‌ها",
                callback_data=(
                    f"management_chapter:"
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


# ==========================================================
# Lesson handler
# ==========================================================

async def show_management_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show a management lesson safely."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    parts = data.split(":")

    if len(parts) != 3:
        return

    _, chapter_id, lesson_index_text = parts

    try:
        lesson_index = int(
            lesson_index_text
        )
    except ValueError:
        return

    chapter = get_chapter(
        chapter_id
    )

    if chapter is None:
        await query.edit_message_text(
            "فصل موردنظر پیدا نشد.",
            reply_markup=management_menu_keyboard(),
        )
        return

    if (
        lesson_index < 0
        or lesson_index >= len(
            chapter["lessons"]
        )
    ):
        return

    lesson = get_management_lesson(
        chapter_id,
        lesson_index,
    )

    if lesson is None:
        lesson_title = chapter[
            "lessons"
        ][lesson_index]

        text = f"""
<b>📖 {lesson_title}</b>

این درس در برنامه آموزشی فصل قرار دارد.

محتوای کامل آن هنوز به سیستم اضافه نشده است.
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به درس‌ها",
                    callback_data=(
                        f"management_chapter:"
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

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
            parse_mode="HTML",
        )

        return

    text = format_lesson_text(
        lesson
    )

    keyboard = lesson_navigation_keyboard(
        chapter_id=chapter_id,
        lesson_index=lesson_index,
        lesson=lesson,
    )

    await send_long_text(
        update=update,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# ==========================================================
# Quiz keyboard
# ==========================================================

def quiz_keyboard(
    session: QuizSession,
) -> InlineKeyboardMarkup:
    """Create answer buttons."""

    question = session.current_question

    if question is None:
        return InlineKeyboardMarkup([])

    keyboard = []

    for index, option in enumerate(
        question.options
    ):
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{index + 1}. {option}",
                    callback_data=(
                        f"quiz_answer:{index}"
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ خروج از آزمون",
                callback_data="quiz_cancel",
            )
        ]
    )

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================================
# Quiz question formatter
# ==========================================================

def format_quiz_question(
    session: QuizSession,
) -> str:
    """Format current quiz question."""

    question = session.current_question

    if question is None:
        return "آزمون به پایان رسیده است."

    number = session.current_index + 1
    total = session.total_questions

    return f"""
<b>📝 آزمون درس</b>

سوال {number} از {total}

━━━━━━━━━━━━━━

<b>{question.question}</b>

یک گزینه را انتخاب کنید:
"""


# ==========================================================
# Start quiz
# ==========================================================

async def start_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Start quiz for any supported management lesson."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    if ":" not in data:
        return

    _, lesson_id = data.split(
        ":",
        1,
    )

    lesson = MANAGEMENT_LESSONS.get(
        lesson_id
    )

    if lesson is None:
        await query.edit_message_text(
            "آزمون این درس هنوز فعال نشده است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به درس‌ها",
                            callback_data=(
                                "menu_management"
                            ),
                        )
                    ]
                ]
            ),
        )
        return

    user = update.effective_user

    if user is None:
        return

    questions = build_questions(
        lesson.get(
            "quiz",
            [],
        )
    )

    if not questions:
        location = get_lesson_location(
            lesson_id
        )

        if location is None:
            callback = "menu_management"
        else:
            chapter_id, lesson_index = location
            callback = (
                f"management_lesson:"
                f"{chapter_id}:"
                f"{lesson_index}"
            )

        await query.edit_message_text(
            "برای این درس هنوز سوال آزمون ثبت نشده است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به درس",
                            callback_data=callback,
                        )
                    ]
                ]
            ),
        )
        return

    session = QuizSession(
        questions
    )

    QUIZ_SESSIONS[user.id] = session

    location = get_lesson_location(
        lesson_id
    )

    if location is not None:
        chapter_id, lesson_index = location

        QUIZ_LESSON_CONTEXT[user.id] = {
            "lesson_id": lesson_id,
            "chapter_id": chapter_id,
            "lesson_index": lesson_index,
        }

    await query.edit_message_text(
        format_quiz_question(
            session
        ),
        reply_markup=quiz_keyboard(
            session
        ),
        parse_mode="HTML",
    )


# ==========================================================
# Answer quiz
# ==========================================================

async def answer_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Process a quiz answer."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    user = update.effective_user

    if user is None:
        return

    session = QUIZ_SESSIONS.get(
        user.id
    )

    if session is None:
        await query.edit_message_text(
            "آزمون فعالی برای شما پیدا نشد.",
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

    data = query.data or ""

    if ":" not in data:
        return

    _, answer_index = data.split(
        ":",
        1,
    )

    try:
        selected_option = int(
            answer_index
        )
    except ValueError:
        return

    question = session.current_question

    if question is None:
        return

    correct_option = question.answer

    is_correct = session.answer(
        selected_option
    )

    if is_correct:
        feedback = "✅ پاسخ شما درست است."
    else:
        feedback = (
            "❌ پاسخ شما نادرست است.\n\n"
            f"پاسخ صحیح: "
            f"{correct_option + 1}. "
            f"{question.options[correct_option]}"
        )

    explanation = question.explanation

    if session.is_finished:
        result = session.result()

        result_text = format_quiz_result(
            result
        )

        context_data = QUIZ_LESSON_CONTEXT.get(
            user.id
        )

        keyboard = []

        if context_data is not None:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "🔄 مرور دوباره درس",
                        callback_data=(
                            "management_lesson:"
                            f"{context_data['chapter_id']}:"
                            f"{context_data['lesson_index']}"
                        ),
                    )
                ]
            )

            keyboard.append(
                [
                    InlineKeyboardButton(
                        "📚 بازگشت به فصل",
                        callback_data=(
                            "management_chapter:"
                            f"{context_data['chapter_id']}"
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

        final_text = f"""
<b>{feedback}</b>

{explanation}

━━━━━━━━━━━━━━

{result_text}
"""

        await query.edit_message_text(
            final_text,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
            parse_mode="HTML",
        )

        QUIZ_SESSIONS.pop(
            user.id,
            None,
        )

        QUIZ_LESSON_CONTEXT.pop(
            user.id,
            None,
        )

        return

    next_question_text = format_quiz_question(
        session
    )

    text = f"""
<b>{feedback}</b>

{explanation}

━━━━━━━━━━━━━━

{next_question_text}
"""

    await query.edit_message_text(
        text,
        reply_markup=quiz_keyboard(
            session
        ),
        parse_mode="HTML",
    )


# ==========================================================
# Cancel quiz
# ==========================================================

async def cancel_management_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Cancel active quiz."""

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    user = update.effective_user

    if user is not None:
        QUIZ_SESSIONS.pop(
            user.id,
            None,
        )

        QUIZ_LESSON_CONTEXT.pop(
            user.id,
            None,
        )

    await query.edit_message_text(
        "آزمون متوقف شد.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت به درس‌ها",
                        callback_data="menu_management",
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
