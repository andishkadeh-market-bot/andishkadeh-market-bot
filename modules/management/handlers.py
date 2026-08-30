"""
Telegram handlers for the Management education module.
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from core.utils import send_long_text

from modules.management.curriculum import MANAGEMENT_CURRICULUM
from modules.management.lessons.lesson_01 import LESSON_01


def management_menu_keyboard() -> InlineKeyboardMarkup:
    """Create management chapter menu."""

    keyboard = []

    for chapter in MANAGEMENT_CURRICULUM:
        keyboard.append(
            [
                InlineKeyboardButton(
                    chapter["title"],
                    callback_data=(
                        f"management_chapter:{chapter['id']}"
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

    return InlineKeyboardMarkup(keyboard)


def management_chapter_keyboard(
    chapter_id: str,
) -> InlineKeyboardMarkup:
    """Create lesson menu for a chapter."""

    chapter = next(
        (
            item
            for item in MANAGEMENT_CURRICULUM
            if item["id"] == chapter_id
        ),
        None,
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

    for index, lesson in enumerate(
        chapter["lessons"],
        start=1,
    ):
        callback_data = (
            f"management_lesson:"
            f"{chapter_id}:"
            f"{index - 1}"
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📖 درس {index}: {lesson}",
                    callback_data=callback_data,
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

    return InlineKeyboardMarkup(keyboard)


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

    chapter = next(
        (
            item
            for item in MANAGEMENT_CURRICULUM
            if item["id"] == chapter_id
        ),
        None,
    )

    if chapter is None:
        await query.edit_message_text(
            "فصل موردنظر پیدا نشد.",
            reply_markup=management_menu_keyboard(),
        )
        return

    text = f"""
<b>{chapter["title"]}</b>

📚 تعداد درس‌ها: {len(chapter["lessons"])}

هر درس شامل درسنامه، نکات تخصصی،
مثال کاربردی، سوالات آزمونی و مرور است.

<b>درس موردنظر را انتخاب کنید:</b>
"""

    await query.edit_message_text(
        text,
        reply_markup=management_chapter_keyboard(
            chapter_id
        ),
        parse_mode="HTML",
    )


def format_lesson_text(
    lesson: dict,
) -> str:
    """Build a complete lesson message."""

    objectives = "\n".join(
        f"• {item}"
        for item in lesson["objectives"]
    )

    concepts = "\n\n".join(
        f"<b>{item['title']}</b>\n"
        f"{item['description']}"
        for item in lesson["key_concepts"]
    )

    specialized = "\n".join(
        f"• {item}"
        for item in lesson["specialized_points"]
    )

    exam_points = "\n".join(
        f"• {item}"
        for item in lesson["exam_points"]
    )

    review = "\n".join(
        f"• {item}"
        for item in lesson["review"]
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

    _, chapter_id, lesson_index = parts

    try:
        lesson_index = int(lesson_index)
    except ValueError:
        return

    chapter = next(
        (
            item
            for item in MANAGEMENT_CURRICULUM
            if item["id"] == chapter_id
        ),
        None,
    )

    if chapter is None:
        return

    if lesson_index < 0:
        return

    if lesson_index >= len(
        chapter["lessons"]
    ):
        return

    if (
        chapter_id == "management_chapter_01"
        and lesson_index == 0
    ):
        text = format_lesson_text(
            LESSON_01
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "📝 شروع آزمون درس",
                    callback_data=(
                        "management_quiz:"
                        "management_01_01"
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

        await send_long_text(
            update=update,
            text=text,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
            parse_mode="HTML",
        )

        return

    lesson_title = chapter["lessons"][lesson_index]

    text = f"""
<b>📖 {lesson_title}</b>

این درس در برنامه آموزشی فصل قرار دارد.

محتوای کامل آن در مرحله تولید محتوای تخصصی
به سیستم اضافه خواهد شد.
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
