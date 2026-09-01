"""
Membership handlers for Andishkadeh Management & Market.
Provides:
- Mandatory channel membership check
- Membership required message
- Join channel button
- Membership verification button
- Automatic redirect to main menu after successful verification
- Safe callback handling
"""
from __future__ import annotations
import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)
logger = logging.getLogger(__name__)
# ==========================================================
# Constants
# ==========================================================
CHANNEL_USERNAME = "@andishkadeh_marketing"
CHANNEL_URL = "https://t.me/andishkadeh_marketing"
# ==========================================================
# Membership Keyboard
# ==========================================================
def membership_keyboard() -> InlineKeyboardMarkup:
    """
    Return the mandatory membership keyboard.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 عضویت در کانال",
                    url=CHANNEL_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ بررسی عضویت",
                    callback_data="check_membership",
                )
            ],
        ]
    )
# ==========================================================
# Membership Check
# ==========================================================
async def is_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> bool:
    """
    Check whether the current Telegram user is a member
    of the required channel.
    Allowed statuses:
    - member
    - administrator
    - creator
    Any API error is treated as not a member so that the
    membership gate remains safe.
    """
    user = update.effective_user
    if user is None:
        return False
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user.id,
        )
        return member.status in {
            "member",
            "administrator",
            "creator",
        }
    except Exception:
        logger.exception(
            "Membership check failed for user: %s",
            user.id,
        )
        return False
# ==========================================================
# Membership Required
# ==========================================================
async def show_membership_required(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Show the mandatory channel membership message.
    """
    text = (
        "📢 <b>عضویت در کانال الزامی است</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "برای استفاده از ربات "
        "<b>اندیشکده مدیریت و بازار</b>، "
        "ابتدا باید عضو کانال ما شوید.\n\n"
        "1️⃣ روی «📢 عضویت در کانال» بزنید.\n"
        "2️⃣ عضو کانال شوید.\n"
        "3️⃣ سپس روی «✅ بررسی عضویت» بزنید."
    )
    query = update.callback_query
    if query is not None:
        try:
            await query.answer()
        except Exception:
            logger.exception(
                "Unable to answer membership callback."
            )
        try:
            await query.edit_message_text(
                text=text,
                reply_markup=membership_keyboard(),
                parse_mode="HTML",
            )
        except Exception:
            logger.exception(
                "Unable to edit membership required message."
            )
        return
    message = update.effective_message
    if message is not None:
        try:
            await message.reply_text(
                text=text,
                reply_markup=membership_keyboard(),
                parse_mode="HTML",
            )
        except Exception:
            logger.exception(
                "Unable to send membership required message."
            )
# ==========================================================
# Check Membership Callback
# ==========================================================
async def check_membership_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Verify channel membership.
    If membership is confirmed:
        Redirect user to the main menu.
    If membership is not confirmed:
        Keep the membership keyboard visible.
    """
    query = update.callback_query
    if query is None:
        return
    try:
        await query.answer()
    except Exception:
        logger.exception(
            "Unable to answer check membership callback."
        )
    # ------------------------------------------------------
    # Verify membership
    # ------------------------------------------------------
    if await is_member(
        update,
        context,
    ):
        logger.info(
            "Membership verified for user: %s",
            update.effective_user.id
            if update.effective_user
            else "unknown",
        )
        # --------------------------------------------------
        # Redirect to main menu
        # --------------------------------------------------
        #
        # Imported lazily to avoid circular imports:
        #
        # core.menu
        #     ↓
        # modules.membership.handlers
        #
        # A normal top-level import here could therefore
        # break application startup.
        #
        try:
            from core.menu import show_main_menu
            await show_main_menu(
                update,
                context,
            )
            return
        except Exception:
            logger.exception(
                "Unable to redirect verified user to main menu."
            )
        # --------------------------------------------------
        # Fallback message
        # --------------------------------------------------
        try:
            await query.edit_message_text(
                text=(
                    "✅ <b>عضویت شما تأیید شد.</b>\n\n"
                    "اکنون می‌توانید از امکانات "
                    "اندیشکده مدیریت و بازار استفاده کنید."
                ),
                parse_mode="HTML",
            )
        except Exception:
            logger.exception(
                "Unable to show membership confirmation."
            )
        return
    # ======================================================
    # Membership Not Confirmed
    # ======================================================
    logger.info(
        "Membership not confirmed for user: %s",
        update.effective_user.id
        if update.effective_user
        else "unknown",
    )
    try:
        await query.edit_message_text(
            text=(
                "❌ <b>عضویت شما تأیید نشد.</b>\n\n"
                "هنوز عضویت شما در کانال "
                "اندیشکده مدیریت و بازار تأیید نشده است.\n\n"
                "ابتدا عضو کانال شوید و سپس دوباره "
                "روی «✅ بررسی عضویت» بزنید."
            ),
            reply_markup=membership_keyboard(),
            parse_mode="HTML",
        )
    except Exception:
        logger.exception(
            "Unable to show membership failure message."
        )
# ==========================================================
# Membership Handlers
# ==========================================================
membership_handlers = [
    CallbackQueryHandler(
        check_membership_callback,
        pattern=r"^check_membership$",
    ),
]
# ==========================================================
# Public Exports
# ==========================================================
__all__ = [
    "CHANNEL_USERNAME",
    "CHANNEL_URL",
    "membership_keyboard",
    "is_member",
    "show_membership_required",
    "check_membership_callback",
    "membership_handlers",
]
