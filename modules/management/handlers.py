"""
Telegram handlers for the Management education module.
Supported:
- Chapter 1: Lessons 01-12
- Chapter 2: Lessons 13-19
- Chapter 3: Lessons 20-26
- Chapter 4: Lessons 27-36
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
# ==========================================================
# Chapter 1 imports
# ==========================================================
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
# ==========================================================
# Chapter 2 imports
# ==========================================================
from modules.management.lessons.lesson_13 import LESSON_13
from modules.management.lessons.lesson_14 import LESSON_14
from modules.management.lessons.lesson_15 import LESSON_15
from modules.management.lessons.lesson_16 import LESSON_16
from modules.management.lessons.lesson_17 import LESSON_17
from modules.management.lessons.lesson_18 import LESSON_18
from modules.management.lessons.lesson_19 import LESSON_19
# ==========================================================
# Chapter 3 imports
# ==========================================================
from modules.management.lessons.lesson_20 import LESSON_20
from modules.management.lessons.lesson_21 import LESSON_21
from modules.management.lessons.lesson_22 import LESSON_22
from modules.management.lessons.lesson_23 import LESSON_23
from modules.management.lessons.lesson_24 import LESSON_24
from modules.management.lessons.lesson_25 import LESSON_25
from modules.management.lessons.lesson_26 import LESSON_26
# ==========================================================
# Chapter 4 imports
# ==========================================================
from modules.management.lessons.lesson_27 import LESSON_27
from modules.management.lessons.lesson_28 import LESSON_28
from modules.management.lessons.lesson_29 import LESSON_29
from modules.management.lessons.lesson_30 import LESSON_30
from modules.management.lessons.lesson_31 import LESSON_31
from modules.management.lessons.lesson_32 import LESSON_32
from modules.management.lessons.lesson_33 import LESSON_33
from modules.management.lessons.lesson_34 import LESSON_34
from modules.management.lessons.lesson_35 import LESSON_35
from modules.management.lessons.lesson_36 import LESSON_36
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
    LESSON_20["id"]: LESSON_20,
    LESSON_21["id"]: LESSON_21,
    LESSON_22["id"]: LESSON_22,
    LESSON_23["id"]: LESSON_23,
    LESSON_24["id"]: LESSON_24,
    LESSON_25["id"]: LESSON_25,
    LESSON_26["id"]: LESSON_26,
    LESSON_27["id"]: LESSON_27,
    LESSON_28["id"]: LESSON_28,
    LESSON_29["id"]: LESSON_29,
    LESSON_30["id"]: LESSON_30,
    LESSON_31["id"]: LESSON_31,
    LESSON_32["id"]: LESSON_32,
    LESSON_33["id"]: LESSON_33,
    LESSON_34["id"]: LESSON_34,
    LESSON_35["id"]: LESSON_35,
    LESSON_36["id"]: LESSON_36,
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
MANAGEMENT_CHAPTER_03_LESSONS = [
    LESSON_20,
    LESSON_21,
    LESSON_22,
    LESSON_23,
    LESSON_24,
    LESSON_25,
    LESSON_26,
]
MANAGEMENT_CHAPTER_04_LESSONS = [
    LESSON_27,
    LESSON_28,
    LESSON_29,
    LESSON_30,
    LESSON_31,
    LESSON_32,
    LESSON_33,
    LESSON_34,
    LESSON_35,
    LESSON_36,
]
MANAGEMENT_CHAPTER_LESSONS = {
    "management_basics": MANAGEMENT_CHAPTER_01_LESSONS,
    "planning": MANAGEMENT_CHAPTER_02_LESSONS,
    "organizing": MANAGEMENT_CHAPTER_03_LESSONS,
    "leadership": MANAGEMENT_CHAPTER_04_LESSONS,
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
    display_lessons = detailed_lessons
    if not display_lessons:
        display_lessons = [
            {
                "id": f"{chapter_id}_{index}",
                "title": title,
            }
            for index, title in enumerate(
                chapter.get("lessons", [])
            )
        ]
    for index, lesson in enumerate(
        display_lessons
    ):
        prefix = (
            "📖"
            if index < len(detailed_lessons)
            else "🔒"
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    (
                        f"{prefix} درس "
                        f"{index + 1}: "
                        f"{lesson['title']}"
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
    lesson_count = max(
        len(chapter.get("lessons", [])),
        detailed_count,
    )
    text = f"""
<b>{chapter["title"]}</b>
📚 تعداد درس‌ها: {lesson_count}
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
{lesson.get("lesson", "")}
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
{lesson.get("practical_example", "")}
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
    lessons = get_chapter_lessons(
        chapter_id
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
    if lesson_index + 1 < len(
        lessons
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
                "📚 فهرست فصل‌ها",
                callback_data="menu_management",
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
    _, chapter_id, lesson_index_raw = parts
    try:
        lesson_index = int(
            lesson_index_raw
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
    lesson = get_management_lesson(
        chapter_id,
        lesson_index,
    )
    if lesson is None:
        await query.edit_message_text(
            "درس موردنظر هنوز محتوای کامل ندارد.",
            reply_markup=InlineKeyboardMarkup(
                [
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
            ),
        )
        return
    text = format_lesson_text(
        lesson
    )
    keyboard = lesson_navigation_keyboard(
        chapter_id,
        lesson_index,
        lesson,
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
    """Create answer buttons for current question."""
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
    """Format the current quiz question."""
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
    """Start the quiz for any supported management lesson."""
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
                            "📚 فهرست فصل‌ها",
                            callback_data="menu_management",
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
        chapter_id = (
            location[0]
            if location is not None
            else "management_basics"
        )
        await query.edit_message_text(
            "برای این درس هنوز سوال آزمون ثبت نشده است.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت به درس‌ها",
                            callback_data=(
                                f"management_chapter:"
                                f"{chapter_id}"
                            ),
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
# Answer quiz question
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
    if (
        selected_option < 0
        or selected_option >= len(
            question.options
        )
    ):
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
        quiz_context = QUIZ_LESSON_CONTEXT.get(
            user.id,
            {},
        )
        chapter_id = quiz_context.get(
            "chapter_id",
            "management_basics",
        )
        lesson_index = quiz_context.get(
            "lesson_index",
            0,
        )
        lesson_id = quiz_context.get(
            "lesson_id"
        )
        final_text = f"""
<b>{feedback}</b>
{explanation}
━━━━━━━━━━━━━━
{result_text}
"""
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔄 مرور دوباره درس",
                    callback_data=(
                        f"management_lesson:"
                        f"{chapter_id}:"
                        f"{lesson_index}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "📝 آزمون دوباره",
                    callback_data=(
                        f"management_quiz:"
                        f"{lesson_id}"
                        if lesson_id
                        else "menu_management"
                    ),
                )
            ],
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
    """Cancel an active quiz."""
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    user = update.effective_user
    chapter_id = "management_basics"
    if user is not None:
        quiz_context = QUIZ_LESSON_CONTEXT.get(
            user.id,
            {},
        )
        chapter_id = quiz_context.get(
            "chapter_id",
            "management_basics",
        )
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
                        callback_data=(
                            f"management_chapter:"
                            f"{chapter_id}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 فهرست فصل‌ها",
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
