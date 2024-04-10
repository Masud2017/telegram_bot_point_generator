from telegram import Update
from telegram.ext import ContextTypes

async def get_admin_user_id(update:Update,context:ContextTypes) -> None:
    data = await context.bot.getChatAdministrators(update.message.chat.id)
    admin_user_id = 0
    for x in data:
        if x.status == "creator":
            admin_user_id = x.user.id
            break

    return admin_user_id
