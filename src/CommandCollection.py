from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update,User
from src.Util import *
from src.SessionHandler import SessionHandler
from src.SessionCommandHandler import SessionedCommandHandler

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
                await update.message.reply_text(f"{amount} 원이 성공적으로 {recipient_user_id} 으로 전송 되었습니다.")
            else:
                await update.message.reply_text("잔액이 부족합니다.")
        else:
            await update.message.reply_text("양식에 맞게 수취인의 아이디와 금액을 기재해주세요. 예) /transfer <텔레그램 ID> <송금할 금액>")


    @staticmethod
    async def inventory(update:Update, context: ContextTypes.DEFAULT_TYPE):
        admin_user_id = await get_admin_user_id(update,context)
        current_user_id = current_user_id = update.message.from_user["id"]

        if admin_user_id == current_user_id: # if the user is admin
            splitted_message = update.message.text.split(" ")
            if (len(splitted_message) > 1):
                if (splitted_message[1].isnumeric() == False):
                    await update.message.reply_text("유효한 사용자 ID를 다음 형식으로 제공하십시오:\n /inventory <user_id>")

                user_id = splitted_message[1]
                msg = db.get_inventory_of_a_user(user_id)
                await update.message.reply_text(msg)
            else:
                await update.message.reply_text("유효한 사용자 ID를 다음 형식으로 제공하십시오:\n /inventory <user_id>")

        else: #if the user is regular user
            msg = "👜회원님의 보유아이템👜:\n"
            inventory = db.get_inventory(str(current_user_id))
            
            if (db.is_inventory_available_for_user(str(current_user_id))):
                for i, item in enumerate(inventory):
                    msg += f"{i+1}: {item} - 수량: {inventory[item]}\n"
                await update.message.reply_text(msg)
            else:
                await update.message.reply_text("인벤토리가 비어있습니다.")


    
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
    async def addbox(update:Update,context:ContextTypes.DEFAULT_TYPE):
        admin_user_id = await get_admin_user_id(update,context)
        session_handler = SessionHandler()
        current_user_id = update.message.from_user["id"]

        if (admin_user_id == current_user_id):
            session_handler.init_user_session(str(current_user_id),"addbox")
            await update.message.reply_text("고유 ID를 입력하세요.")
        


    @staticmethod
    async def showboxes(update:Update,context:ContextTypes.DEFAULT_TYPE):
        admin_user_id = await get_admin_user_id(update,context)
        current_user_id = update.message.from_user["id"]

        if (admin_user_id == current_user_id):
            msg = db.get_boxes_info_as_msg()
            await update.message.reply_text(msg)    


    @staticmethod
    async def additem(update:Update,context:ContextTypes.DEFAULT_TYPE):
        # Logic for the /additem command
        pass

    @staticmethod
    async def showitems(update:Update,context:ContextTypes.DEFAULT_TYPE):
        # Logic for the /showitems command
        pass

    @staticmethod
    async def unlistitem(update:Update,context:ContextTypes.DEFAULT_TYPE):
        # Logic for the /unlistitem command
        pass

    @staticmethod
    async def withdrawitem(update:Update,context:ContextTypes.DEFAULT_TYPE):
        # Logic for the /withdrawitem command
        pass

    @staticmethod
    async def editprobability(update:Update,context:ContextTypes.DEFAULT_TYPE):
        # Logic for the /editprobability command
        pass

    @staticmethod
    async def editbox(update:Update,context:ContextTypes.DEFAULT_TYPE):
        # Logic for the /editbox command
        pass

    @staticmethod
    async def deletebox(update:Update,context:ContextTypes.DEFAULT_TYPE):
        admin_user_id = await get_admin_user_id(update,context)
        current_user_id = update.message.from_user["id"]

        if (admin_user_id == current_user_id):
            splitted_msg = update.message.text.split(" ")
            if (len(splitted_msg) == 1):
                await update.message.reply_text("Box id is missing. Please try again")
            if (len(splitted_msg) == 2):
                if not splitted_msg[1].isnumeric():
                    await update.message.reply_text("유효하지 않은 박스 ID입니다.")
                else:
                    # here need to write code
                    
                    if db.is_box_exists(splitted_msg[1]):
                        db.delete_box(splitted_msg[1])
                        await update.message.reply_text(f"Successfully deleted box {splitted_msg[1]}")
                    else:
                        await update.message.reply_text("The box has no existence. Please try with a valid box id.")

            if (len(splitted_msg) > 2):
                await update.message.reply_text("Please provide a valid box ID in the following format:\n /deletebox <box_id>")
            # db.is_box_exists(box_id)

    @staticmethod
    async def regular_message(update:Update,context : ContextTypes.DEFAULT_TYPE):
        session_handler = SessionHandler()
        session_command_handler = SessionedCommandHandler()
        current_user_id = update.message.from_user["id"]

        if session_handler.is_user_using_sessioned_command(str(current_user_id)):
            # message = update.message.text
            # if (message.isnumeric()):
            #     session_handler.update_session(str(current_user_id),int(message),True)
            await session_command_handler.start_handling(update,context,str(current_user_id))
            # else:
            #     await update.message.reply_text("While you are using a sessioned command you are not allowed to use any other commands.")
        else:
            pass
        

# list of command handlers with their subsequent commands
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
message_handler = MessageHandler(filters.ALL,CommandCollection.regular_message)
