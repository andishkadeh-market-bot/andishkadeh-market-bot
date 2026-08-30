"""
Telegram handlers for the management education module.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from modules.management.curriculum import MANAGEMENT_CURRICULUM


def management_menu_keyboard() -> InlineKeyboardMarkup:
    """Create management chapter menu."""

    keyboard = []

    for chapter in MANAGEMENT_CURRICULUM:
        keyboard.append(
            [
                InlineKeyboardButton(
                    chapter["title"],
                    callback_data=f"management_chapter:{chapter['id']}",
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
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📖 درس {index}: {lesson}",
                    callback_data=(
                        f"management_lesson:"
                        f"{chapter_id}:"
                        f"{index - 1}"
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

مسیر آموزشی مدیریت از مفاهیم پایه تا مباحث پیشرفته طراحی شده است.

هر فصل شامل مجموعه‌ای از درس‌های تخصصی است که در مراحل بعدی با درسنامه کامل، مثال‌های کاربردی، نکات آزمونی و آزمون‌های پایان فصل تکمیل می‌شود.

<b>یک فصل را انتخاب کنید:</b>
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

تعداد درس‌ها: {len(chapter["lessons"])}

هر درس در مرحله تولید محتوا شامل موارد زیر خواهد بود:

📖 درسنامه مفصل
🎯 اهداف یادگیری
💡 نکات تخصصی
📝 نکات آزمونی
📌 مثال کاربردی
❓ سوالات
🔄 مرور

<b>درس موردنظر را انتخاب کنید:</b>
"""

    await query.edit_message_text(
        text,
        reply_markup=management_chapter_keyboard(
            chapter_id
        ),
        parse_mode="HTML",
    )


async def show_management_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show a management lesson placeholder."""

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

    lessons = chapter["lessons"]

    if lesson_index < 0 or lesson_index >= len(lessons):
        return

    lesson_title = lessons[lesson_index]

    text = f"""
<b>📖 {lesson_title}</b>

این درس در حال آماده‌سازی محتوای تخصصی است.

نسخه نهایی درس شامل:

━━━━━━━━━━━━━━

🎯 <b>اهداف یادگیری</b>

📖 <b>درسنامه جامع و مفصل</b>

💡 <b>نکات تخصصی</b>

📝 <b>نکات مهم آزمونی</b>

📌 <b>مثال‌های کاربردی</b>

❓ <b>آزمون و سوالات چهارگزینه‌ای</b>

📊 <b>نتیجه و تحلیل آزمون</b>

🔄 <b>مرور و جمع‌بندی</b>

━━━━━━━━━━━━━━

محتوای کامل این درس در مرحله تولید محتوای تخصصی اضافه خواهد شد.
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 بازگشت به درس‌ها",
                callback_data=(
                    f"management_chapter:{chapter_id}"
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
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )
