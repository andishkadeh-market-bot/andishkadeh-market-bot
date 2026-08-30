"""
Telegram keyboards for Andishkadeh Management & Market.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Return the main bot menu."""

    keyboard = [
        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="menu_education",
            ),
            InlineKeyboardButton(
                "📝 آزمون استخدامی",
                callback_data="menu_exam",
            ),
        ],
        [
            InlineKeyboardButton(
                "🏦 بانکداری تخصصی",
                callback_data="menu_banking",
            ),
            InlineKeyboardButton(
                "🧾 حسابداری",
                callback_data="menu_accounting",
            ),
        ],
        [
            InlineKeyboardButton(
                "💳 مدیریت مالی",
                callback_data="menu_finance",
            ),
            InlineKeyboardButton(
                "🌍 تجارت بین‌الملل",
                callback_data="menu_trade",
            ),
        ],
        [
            InlineKeyboardButton(
                "📈 بازاریابی و فروش",
                callback_data="menu_marketing",
            ),
            InlineKeyboardButton(
                "💰 اقتصاد و بازار",
                callback_data="menu_economics",
            ),
        ],
        [
            InlineKeyboardButton(
                "🧠 روانشناسی و مددکاری",
                callback_data="menu_psychology",
            ),
            InlineKeyboardButton(
                "🎲 سوالات تصادفی",
                callback_data="menu_random",
            ),
        ],
        [
            InlineKeyboardButton(
                "📂 فایل و منابع آموزشی",
                callback_data="menu_resources",
            ),
            InlineKeyboardButton(
                "📱 شبکه‌های اجتماعی",
                callback_data="menu_social",
            ),
        ],
        [
            InlineKeyboardButton(
                "👤 پروفایل من",
                callback_data="menu_profile",
            ),
            InlineKeyboardButton(
                "ℹ️ درباره اندیشکده",
                callback_data="menu_about",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_button() -> InlineKeyboardMarkup:
    """Return a simple back button."""

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="menu_main",
                )
            ]
        ]
    )
