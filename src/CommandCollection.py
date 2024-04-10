from telegram.ext import CommandHandler, ContextTypes
from telegram import Update,User
from src.Util import *

from . import db

help_content_for_regular_user ="""
                안녕하세요! 각종 도움이 되는 도움말을 제공합니다!
                /help - 명령어 도움말을 실행합니다.
                /myid - 유저의 텔레그램 아이디를 제공 받을 수 있습니다.
                /balance - 유저의 포인트 잔액을 확인할 수 있습니다.
                /transfer <텔레그램 아이디> <금액> - 포인트를 회원에게 송금합니다.
                /inventory - 유저의 인벤토리 현황을 볼 수 있습니다.
                /openbox - 랜덤상자를 열 수 있습니다.
                """

help_content_for_admin_user ="""
                안녕하세요! 각종 도움이 되는 도움말을 제공합니다!
                /help - 명령어 도움말을 실행합니다.
                /myid - 유저의 텔레그램 아이디를 제공 받을 수 있습니다.
                /balance - 유저의 포인트 잔액을 확인할 수 있습니다.
                /transfer <텔레그램 아이디> <금액> - 포인트를 회원에게 송금합니다.
                /inventory - 유저의 인벤토리 현황을 볼 수 있습니다.
                /openbox - 랜덤상자를 열 수 있습니다.
        
                어드민 명령어 
                /addbalance <user_id> <amount> - Add balance to a user
                /addbox - Add a new box
                /showboxes - Show all available boxes
                /additem - Add item to a box
                /showitems <box_id> - Show all items in a box
                /unlistitem <box_id> <item_name> - Unlist an item from a box
                /withdrawitem <user_id> <item_name> <quantity> - Withdraw an item from a user's inventory
                /editprobability <box_id> <item_name> <probability> - Edit probability of an item in a box
                /editbox - Edit a box
                /deletebox <box_id> - Delete a box
                """


'''
<h1>CommandHandler</h1>
This class provides command functionality based on user type.
It detects whether the user is admin or regular and make particular command active based on that.
If the user is regular then command functions related to admin will have no effect.
'''
class CommandCollection:
    def __init__(self):
        pass

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
        admin_user_id = await get_admin_user_id(update,context)

        current_user_id = update.message.from_user["id"]
        if (current_user_id == admin_user_id):
            await update.message.reply_text(help_content_for_admin_user)
        else:
            await update.message.reply_text(help_content_for_regular_user)

    @staticmethod
    async def myid(update:Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user["id"]
        
        print(update.message)
        await update.message.reply_text(f"회원님의 텔레그램 아이디는 {user_id} 입니다.")


    @staticmethod
    async def balance(update:Update, context: ContextTypes.DEFAULT_TYPE):
        current_user_id = update.message.from_user["id"]

        db.init_users(str(current_user_id),update.message) # this function will only work if the user is new and does not have any record else  it will be ignored

        balance = db.get_balance(str(current_user_id))
        await update.message.reply_text(f"보유 잔액은 {balance} 원입니다")

    @staticmethod
    async def transfer(update:Update, context: ContextTypes.DEFAULT_TYPE):
        splitted_message = update.message.text.split(" ")
        recipient_user_id = splitted_message[1]
        amount = int(splitted_message[2])
        current_user_id = str(update.message.from_user["id"])

        if (db.is_user_exist(recipient_user_id)):
            if await db.transfer_currency(current_user_id,recipient_user_id,amount):
                await update.message_reply_text(f"{amount} 원이 성공적으로 {recipient_user_id} 으로 전송 되었습니다.")
            else:
                await update.message_update_text("잔액이 부족합니다.")
        else:
            await update.message_update_text("양식에 맞게 수취인의 아이디와 금액을 기재해주세요. 예) /transfer <텔레그램 ID> <송금할 금액>")


    @staticmethod
    async def inventory(self):
        pass
    
    @staticmethod
    async def openbox(self):
        pass

    # Admin specific command section started
    @staticmethod
    async def addbalance(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
        admin_user_id = await get_admin_user_id(update,context)
        current_user_id = update.message.from_user["id"]

        db.init_users(str(current_user_id),update.message) # this function will only work if the user is new and does not have any record else  it will be ignored

        if (admin_user_id == current_user_id):
            msg_text_splitted = update.message.text.split(" ")
            recipient_user_id = msg_text_splitted[1]
            balance = msg_text_splitted[2]

            db.add_balance(str(recipient_user_id),int(balance))
            await update.message.reply_text(f"Successfully added {balance} to {recipient_user_id}")

    @staticmethod
    async def addbox():
        # Logic for the /addbox command
        pass

    @staticmethod
    async def showboxes():
        # Logic for the /showboxes command
        pass

    @staticmethod
    async def additem():
        # Logic for the /additem command
        pass

    @staticmethod
    async def showitems(box_id):
        # Logic for the /showitems command
        pass

    @staticmethod
    async def unlistitem(box_id, item_name):
        # Logic for the /unlistitem command
        pass

    @staticmethod
    async def withdrawitem(user_id, item_name, quantity):
        # Logic for the /withdrawitem command
        pass

    @staticmethod
    async def editprobability(box_id, item_name, probability):
        # Logic for the /editprobability command
        pass

    @staticmethod
    async def editbox():
        # Logic for the /editbox command
        pass

    @staticmethod
    async def deletebox(box_id):
        # Logic for the /deletebox command
        pass

help_command = CommandHandler("help", CommandCollection.help)
myid_command = CommandHandler("myid", CommandCollection.myid)
balance_command = CommandHandler("balance", CommandCollection.balance)
transfer_command = CommandHandler("transfer", CommandCollection.transfer)
inventory_command = CommandHandler("inventory", CommandCollection.inventory)
openbox_command = CommandHandler("openbox", CommandCollection.openbox)
addbalance_command = CommandHandler("addbalance", CommandCollection.addbalance)
addbox_command = CommandHandler("addbox", CommandCollection.addbox)
showboxes_command = CommandHandler("showboxes", CommandCollection.showboxes)
additem_command = CommandHandler("additem", CommandCollection.additem)
showitems_command = CommandHandler("showitems", CommandCollection.showitems)
unlistitem_command = CommandHandler("unlistitem", CommandCollection.unlistitem)
withdrawitem_command = CommandHandler("withdrawitem", CommandCollection.withdrawitem)
editprobability_command = CommandHandler("editprobability", CommandCollection.editprobability)
editbox_command = CommandHandler("editbox", CommandCollection.editbox)
deletebox_command = CommandHandler("deletebox", CommandCollection.deletebox)
