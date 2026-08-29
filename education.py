# =========================================================
# education.py
# 📚 آموزش تخصصی
# 🏛️ اندیشکده مدیریت و بازار
# =========================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


# =========================================================
# EDUCATION INTRO
# =========================================================

def education_intro_text():

    return """
📚 آموزش تخصصی

━━━━━━━━━━━━━━━━━━

🎓 مرکز آموزش تخصصی اندیشکده

در این بخش می‌توانید مفاهیم کاربردی
مدیریت، بازرگانی و مهارت‌های حرفه‌ای
را به‌صورت مرحله‌ای یاد بگیرید.

━━━━━━━━━━━━━━━━━━

📚 حوزه‌های آموزشی:

🏢 مدیریت و سازمان
🌍 تجارت بین‌الملل
📈 بازاریابی و فروش
🏦 بانکداری
💰 اقتصاد و بازار
🧾 حسابداری
💼 مهارت‌های شغلی

━━━━━━━━━━━━━━━━━━

🎯 روش یادگیری:

📖 آموزش مفهومی
+
💡 مثال‌های کاربردی
+
📝 تمرین
+
🎯 آزمون
+
📊 ارزیابی

━━━━━━━━━━━━━━━━━━

👇 حوزه موردنظر خود را انتخاب کنید.
"""


# =========================================================
# EDUCATION MENU
# =========================================================

def education_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🏢 مدیریت و سازمان",
                callback_data="education_management"
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 تجارت بین‌الملل",
                callback_data="international_trade"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 بازاریابی و فروش",
                callback_data="marketing"
            )
        ],

        [
            InlineKeyboardButton(
                "🏦 بانکداری",
                callback_data="banking"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 اقتصاد و بازار",
                callback_data="economics"
            )
        ],

        [
            InlineKeyboardButton(
                "🧾 حسابداری",
                callback_data="accounting"
            )
        ],

        [
            InlineKeyboardButton(
                "💼 مهارت‌های شغلی",
                callback_data="education_career"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ])


# =========================================================
# MANAGEMENT
# =========================================================

def education_management_text():

    return """
🏢 مدیریت و سازمان

━━━━━━━━━━━━━━━━━━

📚 آموزش تخصصی مدیریت

موضوعات اصلی:

👔 اصول مدیریت
🏢 رفتار سازمانی
📊 برنامه‌ریزی و تصمیم‌گیری
🎯 مدیریت استراتژیک
👥 مدیریت منابع انسانی
💼 مدیریت کسب‌وکار
📈 کنترل و ارزیابی عملکرد
💡 کارآفرینی

━━━━━━━━━━━━━━━━━━

🎯 هدف:

تقویت دانش مدیریتی و تبدیل
مفاهیم دانشگاهی به مهارت‌های
قابل استفاده در محیط کار.

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
"""


# =========================================================
# CAREER
# =========================================================

def education_career_text():

    return """
💼 مهارت‌های شغلی

━━━━━━━━━━━━━━━━━━

🎯 مهارت‌هایی برای ورود و پیشرفت
در بازار کار

━━━━━━━━━━━━━━━━━━

📄 رزومه‌نویسی
🎤 مهارت مصاحبه
💬 ارتباط حرفه‌ای
🤝 مذاکره
📊 حل مسئله
⏱️ مدیریت زمان
👥 کار تیمی
💼 رفتار حرفه‌ای
📈 توسعه مسیر شغلی

━━━━━━━━━━━━━━━━━━

💡 هدف:

افزایش آمادگی برای ورود به بازار کار
و موفقیت در محیط‌های حرفه‌ای.

━━━━━━━━━━━━━━━━━━

🏛️ اندیشکده مدیریت و بازار
"""


# =========================================================
# EDUCATION CALLBACK
# =========================================================

async def education_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        education_intro_text(),
        reply_markup=education_menu()
    )


# =========================================================
# EDUCATION SECTION CALLBACK
# =========================================================

async def education_section_callback(
    update,
    context
):

    query = update.callback_query

    await query.answer()

    data = query.data

    texts = {

        "education_management":
            education_management_text(),

        "education_career":
            education_career_text(),

    }

    text = texts.get(
        data,
        "❌ این بخش آموزشی وجود ندارد."
    )

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="education"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home"
            )
        ],

    ])

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )
