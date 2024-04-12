from random import SystemRandom
from telegram import Update
from telegram.ext import ContextTypes
from telegram import constants
import re

async def get_admin_user_id(update:Update,context:ContextTypes) -> None:
    data = await context.bot.getChatAdministrators(update.message.chat.id)
    current_user_id = update.message.from_user["id"]

    # print("printing the chat data  ",data)
    admin_user_id = 0
    for x in data:
        
        if x.status == constants.ChatMemberStatus.OWNER or x.status == constants.ChatMemberStatus.ADMINISTRATOR:
            if x.user.id == current_user_id:
                admin_user_id = x.user.id
                break
        
    return admin_user_id


def get_random_item(box):
    items = box["items"]
    probabilities = [int(x_item["probability"]) for x_item in box["items"]]

    random_item = SystemRandom().choices(population=items,weights=probabilities,k=1)[0]

    return random_item


def extract_message(message,reason):
    command_len = len(message.split(" ")[0])
    message = message[command_len+1:]

    if reason == "unlistitem":
        pattern = r'(\d+)\s+(.+)$'
        result = re.match(pattern, message)
        if result:
            box_id = result.group(1)
            name = result.group(2)
            return (int(box_id),name)

    elif reason == "withdrawitem" or reason == "editprobability":
        print("Printing the value of message : ",message)
        pattern = r"(\d+)\s+(.+)\s+([\d.]+)$"    
        result = re.match(pattern, message)

        if result:
            box_id = result.group(1)
            name = result.group(2)
            qty = result.group(3)
            return (int(box_id),name,int(qty))
        
    