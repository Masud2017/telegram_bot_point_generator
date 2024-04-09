from telegram.ext import CommandHandler, ContextTypes
from telegram import Update,User


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
        await update.message.reply_text(help_content_for_regular_user)

    @staticmethod
    async def myid(update:Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user["id"]
        await update.message.reply_text(f"회원님의 텔레그램 아이디는 {user_id} 입니다.")


    @staticmethod
    async def balance(self):
        pass

    @staticmethod
    async def transfer(self, telegram_id, amount):
        pass

    @staticmethod
    async def inventory(self):
        pass
    
    @staticmethod
    async def openbox(self):
        pass

    # Admin specific command section started
    @staticmethod
    async def addbalance(user_id, amount):
        # Logic for the /addbalance command
        pass

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
