from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

CHANNEL_USERNAME = "@andishkadeh_marketing"
CHANNEL_URL = "https://t.me/andishkadeh_marketing"


def membership_keyboard() -> InlineKeyboardMarkup:
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


async def is_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
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
        return False


async def show_membership_required(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    text = (
        "📢 برای استفاده از ربات اندیشکده مدیریت و بازار، "
        "ابتدا باید عضو کانال ما شوید.\n\n"
        "بعد از عضویت روی «✅ بررسی عضویت» بزنید."
    )

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=membership_keyboard(),
        )
    elif update.message:
        await update.message.reply_text(
            text=text,
            reply_markup=membership_keyboard(),
        )


async def check_membership_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    if await is_member(update, context):
        await query.edit_message_text(
            "✅ عضویت شما تأیید شد.\n\n"
            "اکنون می‌توانید از امکانات ربات استفاده کنید."
        )

        # فعلاً فقط تأیید عضویت انجام می‌شود.
        # اتصال به منوی اصلی را در مرحله بعد انجام می‌دهیم.

    else:
        await query.edit_message_text(
            "❌ هنوز عضویت شما در کانال تأیید نشده است.\n\n"
            "ابتدا عضو کانال شوید و سپس دوباره روی "
            "«✅ بررسی عضویت» بزنید.",
            reply_markup=membership_keyboard(),
        )


membership_handlers = [
    CallbackQueryHandler(
        check_membership_callback,
        pattern=r"^check_membership$",
    )
]
