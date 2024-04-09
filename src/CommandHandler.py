from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

command_for_regular_user = dict(
    [
        {"help","""
                    안녕하세요! 각종 도움이 되는 도움말을 제공합니다!
                    /help - 명령어 도움말을 실행합니다.
                    /myid - 유저의 텔레그램 아이디를 제공 받을 수 있습니다.
                    /balance - 유저의 포인트 잔액을 확인할 수 있습니다.
                    /transfer <텔레그램 아이디> <금액> - 포인트를 회원에게 송금합니다.
                    /inventory - 유저의 인벤토리 현황을 볼 수 있습니다.
                    /openbox - 랜덤상자를 열 수 있습니다.
                """
         },
        
    ]
)

command_for_admin_user = dict(
    [
        {"help","""
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
         },
        
    ]
)