“””
Telegram handlers for the Management education module.

Chapter 1:
Fundamentals and Concepts of Management

Lessons 01-12 are supported.
“””

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

from modules.management.lessons.lesson_01 import (
LESSON_01,
)
from modules.management.lessons.lesson_02 import (
LESSON_02,
)
from modules.management.lessons.lesson_03 import (
LESSON_03,
)
from modules.management.lessons.lesson_04 import (
LESSON_04,
)
from modules.management.lessons.lesson_05 import (
LESSON_05,
)
from modules.management.lessons.lesson_06 import (
LESSON_06,
)
from modules.management.lessons.lesson_07 import (
LESSON_07,
)
from modules.management.lessons.lesson_08 import (
LESSON_08,
)
from modules.management.lessons.lesson_09 import (
LESSON_09,
)
from modules.management.lessons.lesson_10 import (
LESSON_10,
)
from modules.management.lessons.lesson_11 import (
LESSON_11,
)
from modules.management.lessons.lesson_12 import (
LESSON_12,
)

==========================================================

Quiz session storage

==========================================================

QUIZ_SESSIONS: dict[int, QuizSession] = {}

==========================================================

Available lesson content

==========================================================

MANAGEMENT_LESSONS = {
LESSON_01[“id”]: LESSON_01,
LESSON_02[“id”]: LESSON_02,
LESSON_03[“id”]: LESSON_03,
LESSON_04[“id”]: LESSON_04,
LESSON_05[“id”]: LESSON_05,
LESSON_06[“id”]: LESSON_06,
LESSON_07[“id”]: LESSON_07,
LESSON_08[“id”]: LESSON_08,
LESSON_09[“id”]: LESSON_09,
LESSON_10[“id”]: LESSON_10,
LESSON_11[“id”]: LESSON_11,
LESSON_12[“id”]: LESSON_12,
}

==========================================================

Chapter 1 lesson order

==========================================================

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

==========================================================

Helpers

==========================================================

def get_chapter(
chapter_id: str,
) -> dict | None:
“”“Return a management chapter by ID.”””

return next(
    (
        chapter
        for chapter in MANAGEMENT_CURRICULUM
        if chapter["id"] == chapter_id
    ),
    None,
)

def get_management_lesson(
chapter_id: str,
lesson_index: int,
) -> dict | None:
“””
Return detailed lesson content when available.

Currently Chapter 1 supports Lessons 01-12.
"""
if chapter_id != "management_basics":
    return None
if lesson_index < 0:
    return None
if lesson_index >= len(
    MANAGEMENT_CHAPTER_01_LESSONS
):
    return None
lesson = MANAGEMENT_CHAPTER_01_LESSONS[
    lesson_index
]
return MANAGEMENT_LESSONS.get(
    lesson["id"]
)

def get_lesson_index(
lesson_id: str,
) -> int | None:
“”“Return the chapter index of a lesson.”””

for index, lesson in enumerate(
    MANAGEMENT_CHAPTER_01_LESSONS
):
    if lesson["id"] == lesson_id:
        return index
return None

def lesson_navigation_keyboard(
chapter_id: str,
lesson_index: int,
lesson: dict,
) -> InlineKeyboardMarkup:
“”“Create navigation buttons for a lesson.”””

keyboard = []
# Quiz
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
# Previous / next lesson
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
chapter = get_chapter(chapter_id)
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
# Back to chapter
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
# Main menu
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

==========================================================

Management menu

==========================================================

def management_menu_keyboard() -> InlineKeyboardMarkup:
“”“Create management chapter menu.”””

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

==========================================================

Chapter menu

==========================================================

def management_chapter_keyboard(
chapter_id: str,
) -> InlineKeyboardMarkup:
“”“Create lesson menu for a chapter.”””

chapter = get_chapter(
    chapter_id
)
if chapter is None:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data=(
                        "menu_management"
                    ),
                )
            ]
        ]
    )
keyboard = []
for index, lesson in enumerate(
    chapter["lessons"]
):
    lesson_content = get_management_lesson(
        chapter_id,
        index,
    )
    if lesson_content is not None:
        prefix = "📖"
    else:
        prefix = "🔒"
    keyboard.append(
        [
            InlineKeyboardButton(
                (
                    f"{prefix} درس "
                    f"{index + 1}: "
                    f"{lesson}"
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
            callback_data=(
                "menu_management"
            ),
        )
    ]
)
return InlineKeyboardMarkup(
    keyboard
)

==========================================================

Management main menu

==========================================================

async def show_management_menu(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show management chapters.”””

query = update.callback_query
if query is None:
    return
await query.answer()
text = """

📚 آموزش مدیریت

یک مسیر آموزشی مرحله‌ای برای یادگیری مدیریت،
از مفاهیم پایه تا مباحث تخصصی.

📖 درسنامه جامع
💡 نکات تخصصی
📝 نکات آزمونی
📌 مثال کاربردی
❓ آزمون
📊 تحلیل نتیجه
🔄 مرور

فصل موردنظر را انتخاب کنید:
“””

await query.edit_message_text(
    text,
    reply_markup=management_menu_keyboard(),
    parse_mode="HTML",
)

==========================================================

Chapter lessons

==========================================================

async def show_management_chapter(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show lessons inside a management chapter.”””

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
text = f"""

{chapter[“title”]}

📚 تعداد درس‌ها: {len(chapter[“lessons”])}

هر درس شامل:

📖 درسنامه
🎯 اهداف یادگیری
🔍 مفاهیم کلیدی
💡 نکات تخصصی
📝 نکات آزمونی
📌 مثال کاربردی
📝 آزمون
🔄 مرور و جمع‌بندی

درس موردنظر را انتخاب کنید:
“””

await query.edit_message_text(
    text,
    reply_markup=management_chapter_keyboard(
        chapter_id
    ),
    parse_mode="HTML",
)

==========================================================

Lesson formatting

==========================================================

def format_lesson_text(
lesson: dict,
) -> str:
“”“Build a complete lesson message.”””

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

{lesson[“title”]}

━━━━━━━━━━━━━━

🎯 اهداف یادگیری

{objectives}

━━━━━━━━━━━━━━

📖 درسنامه

{lesson[“lesson”]}

━━━━━━━━━━━━━━

🔍 مفاهیم کلیدی

{concepts}

━━━━━━━━━━━━━━

💡 نکات تخصصی

{specialized}

━━━━━━━━━━━━━━

📝 نکات آزمونی

{exam_points}

━━━━━━━━━━━━━━

📌 مثال کاربردی

{lesson[“practical_example”]}

━━━━━━━━━━━━━━

🔄 مرور و جمع‌بندی

{review}
“””

==========================================================

Lesson handler

==========================================================

async def show_management_lesson(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Show a management lesson safely.”””

query = update.callback_query
if query is None:
    return
await query.answer()
data = query.data or ""
parts = data.split(":")
if len(parts) != 3:
    return
_, chapter_id, lesson_index = parts
try:
    lesson_index = int(
        lesson_index
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
if lesson_index < 0:
    return
if lesson_index >= len(
    chapter["lessons"]
):
    return
lesson = get_management_lesson(
    chapter_id,
    lesson_index,
)
# ------------------------------------------------------
# Detailed lesson
# ------------------------------------------------------
if lesson is not None:
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
    return
# ------------------------------------------------------
# Lesson not available
# ------------------------------------------------------
lesson_title = chapter[
    "lessons"
][lesson_index]
text = f"""

📖 {lesson_title}

این درس در برنامه آموزشی فصل قرار دارد.

محتوای کامل آن هنوز به سیستم اضافه نشده است.
“””

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

==========================================================

Quiz keyboard

==========================================================

def quiz_keyboard(
session: QuizSession,
) -> InlineKeyboardMarkup:
“”“Create answer buttons for current question.”””

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

==========================================================

Quiz question formatter

==========================================================

def format_quiz_question(
session: QuizSession,
) -> str:
“”“Format the current quiz question.”””

question = session.current_question
if question is None:
    return "آزمون به پایان رسیده است."
number = session.current_index + 1
total = session.total_questions
return f"""

📝 آزمون درس

سوال {number} از {total}

━━━━━━━━━━━━━━

{question.question}

یک گزینه را انتخاب کنید:
“””

==========================================================

Start quiz

==========================================================

async def start_management_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Start the quiz for a supported management lesson.”””

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
                        "🔙 بازگشت به فصل",
                        callback_data=(
                            "management_chapter:"
                            "management_basics"
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
quiz_data = lesson.get(
    "quiz",
    [],
)
questions = build_questions(
    quiz_data
)
if not questions:
    lesson_index = get_lesson_index(
        lesson_id
    )
    if lesson_index is None:
        lesson_index = 0
    await query.edit_message_text(
        "برای این درس هنوز سوال آزمون ثبت نشده است.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت به درس",
                        callback_data=(
                            "management_lesson:"
                            "management_basics:"
                            f"{lesson_index}"
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
await query.edit_message_text(
    format_quiz_question(
        session
    ),
    reply_markup=quiz_keyboard(
        session
    ),
    parse_mode="HTML",
)

==========================================================

Answer quiz question

==========================================================

async def answer_management_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Process a quiz answer.”””

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
    or selected_option
    >= len(question.options)
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
    final_text = f"""

{feedback}

{explanation}

━━━━━━━━━━━━━━

{result_text}
“””

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 مرور دوباره درس",
                callback_data=(
                    "management_chapter:"
                    "management_basics"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                "📚 بازگشت به فصل",
                callback_data=(
                    "management_chapter:"
                    "management_basics"
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
    return
next_question_text = format_quiz_question(
    session
)
text = f"""

{feedback}

{explanation}

━━━━━━━━━━━━━━

{next_question_text}
“””

await query.edit_message_text(
    text,
    reply_markup=quiz_keyboard(
        session
    ),
    parse_mode="HTML",
)

==========================================================

Cancel quiz

==========================================================

async def cancel_management_quiz(
update: Update,
context: ContextTypes.DEFAULT_TYPE,
) -> None:
“”“Cancel an active quiz.”””

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
await query.edit_message_text(
    "آزمون متوقف شد.",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به درس‌ها",
                    callback_data=(
                        "management_chapter:"
                        "management_basics"
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
