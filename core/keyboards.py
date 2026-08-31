"""
Telegram keyboards for Andishkadeh Management & Market.
Connected modules:
- Management
- General Exam
- Banking
- Accounting
- Finance
- International Trade
- Marketing & Sales
- Economics & Market
- Psychology & Social Work
- Random Quiz
- Resources
- Social Networks
- Profile
- About
"""
from __future__ import annotations
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
# ==========================================================
# Main Menu
# ==========================================================
def main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Return the main bot menu.
    Every callback_data value must match the central
    menu router or the dedicated module router.
    """
    keyboard = [
        # --------------------------------------------------
        # Management / Exam
        # --------------------------------------------------
        [
            InlineKeyboardButton(
                "📚 آموزش مدیریت",
                callback_data="menu_management",
            ),
            InlineKeyboardButton(
                "📝 آزمون استخدامی",
                callback_data="menu_exam",
            ),
        ],
        # --------------------------------------------------
        # Banking / Accounting
        # --------------------------------------------------
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
        # --------------------------------------------------
        # Finance / International Trade
        # --------------------------------------------------
        [
            InlineKeyboardButton(
                "💳 مدیریت مالی",
                callback_data="menu_finance",
            ),
            InlineKeyboardButton(
                "🌍 تجارت بین‌الملل",
                callback_data="menu_international_trade",
            ),
        ],
        # --------------------------------------------------
        # Marketing / Economics
        # --------------------------------------------------
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
        # --------------------------------------------------
        # Psychology / Random Quiz
        # --------------------------------------------------
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
        # --------------------------------------------------
        # Resources / Social
        # --------------------------------------------------
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
        # --------------------------------------------------
        # Profile / About
        # --------------------------------------------------
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
# ==========================================================
# Back Button
# ==========================================================
def back_button() -> InlineKeyboardMarkup:
    """
    Return a simple back button to the main menu.
    """
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
# ==========================================================
# Health Check
# ==========================================================
def keyboards_health_check() -> bool:
    """
    Basic health check for keyboard configuration.
    """
    try:
        keyboard = main_menu_keyboard()
        if keyboard is None:
            return False
        if not keyboard.inline_keyboard:
            return False
        # Verify that International Trade is exposed
        # through the expected callback.
        trade_found = False
        for row in keyboard.inline_keyboard:
            for button in row:
                if (
                    button.callback_data
                    == "menu_international_trade"
                ):
                    trade_found = True
                    break
            if trade_found:
                break
        if not trade_found:
            return False
        return True
    except Exception:
        return False
