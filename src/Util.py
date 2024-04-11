from random import SystemRandom
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


def get_random_item(box):
    items = box["items"]
    probabilities = [int(x_item["probability"]) for x_item in box["items"]]

    random_item = SystemRandom().choices(population=items,weights=probabilities,k=1)[0]

    return random_item