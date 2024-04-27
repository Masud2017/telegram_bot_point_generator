from src.CommandCollection import *
from src.DataBase import DataBase
from telegram.ext import ApplicationBuilder



class Application:
    def __init__(self,telegram_token):
        self.app = ApplicationBuilder().token(telegram_token).build()
        

    def start_application(self):
        self.app.add_handler(help_command)
        self.app.add_handler(myid_command)
        self.app.add_handler(balance_command)
        self.app.add_handler(transfer_command)
        self.app.add_handler(inventory_command)
        self.app.add_handler(openbox_command)
        self.app.add_handler(addbalance_command)
        self.app.add_handler(addbox_command)
        self.app.add_handler(showboxes_command)
        self.app.add_handler(additem_command)
        self.app.add_handler(showitems_command)
        self.app.add_handler(unlistitem_command)
        self.app.add_handler(withdrawitem_command)
        self.app.add_handler(editprobability_command)
        self.app.add_handler(editbox_command)
        self.app.add_handler(deletebox_command)

        self.app.add_handler(promote_user_level_command)
        self.app.add_handler(demote_user_level_command)
        self.app.add_handler(get_user_level_command)
        self.app.add_handler(get_my_level_command)
        
        self.app.add_handler(message_handler)


        self.app.run_polling()