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

# async def show_inventory(update:Update,message):
#         users = json.loads(self.db.get("users"))
#         inventory = {}
#         for item in users[str(message.from_user.id)]["inventory"]:
#             name = item["name"]
#             if name in inventory:
#                 inventory[name] += 1
#             else:
#                 inventory[name] = 1
#         # msg = "👜회원님의 보유아이템👜:\n"

#         # for i, item in enumerate(inventory):
#         #     msg += f"{i+1}: {item} - 수량: {inventory[item]}\n"
#         # await update.message_update_text(msg)
#         return True