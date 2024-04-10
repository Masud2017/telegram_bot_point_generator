from src.SessionHandler import SessionHandler
from telegram.ext import ContextTypes
from telegram import Update
from src import db

class SessionedCommandHandler:
    def __init__(self):
        self.session_handler = SessionHandler()
    
    async def handle_add_box_phase_name(self,update:Update, context : ContextTypes.DEFAULT_TYPE,box,session,user_id:str):
        box_id = session["item_id"]  
        box[box_id] = {
                        "name": update.message.text,
                        "description": None,
                        "price": None,
                        "items": []
        }  

        self.session_handler.update_session(user_id,box_id,update_item_id=True)

        await update.message.reply_text("박스 오픈 금액을 적어주세요.")


    async def handle_add_box_phase_price(self, update:Update, context : ContextTypes.DEFAULT_TYPE,box,session,user_id:str):
        box_id = session["item_id"]  
        try: 
            price  = int(update.message.text)
            print("VAelu of box : " ,box)

            box[box_id]["price"] = price
        except:
            import traceback
            traceback.print_exc()
            await update.message.reply_text("유효한 가격을 적어주세요.")
            return
        self.session_handler.update_session(user_id,box_id,update_item_id=True)
        await update.message.reply_text("박스에 대한 설명을 적어주세요.")

    async def handle_add_box_phase_description(self, update:Update, context : ContextTypes.DEFAULT_TYPE,box,session,user_id:str):
        box_id = session["item_id"]
        box[box_id]["description"] = update.message.text
        db.save_box_item_to_db(box_id,box)
        
        await update.message.reply_text("박스 설정이 성공적으로 저장되었습니다.")
        self.session_handler.remove_user_session(user_id)
    

    async def handle_add_box(self,user_id:str,update:Update,context:ContextTypes.DEFAULT_TYPE):
        session = self.session_handler.get_user_session_obj(user_id)
        if "box" not in session:
            session["box"] = {}

        if len(session) > 0:
            if (session["phase"] == 1):
                box_id = update.message.text
                if box_id.isnumeric():
                    if db.is_box_exists(box_id):
                       await update.message.reply_text("해당 박스의 아이디는 이미 존재합니다. 다른 아이디를 입력해주세요.")
                       self.session_handler.remove_user_session(user_id)
                       return

                    self.session_handler.update_session(user_id,int(box_id),True)
                    await update.message.reply_text("박스 이름을 적어주세요.")
                else:
                    await update.message.reply_text("You need to provide an unique box id.")
            elif(session["phase"] == 2):
                await self.handle_add_box_phase_name(update,context,session["box"],session,user_id)
            elif(session["phase"] == 3):
                await self.handle_add_box_phase_price(update,context,session["box"],session,user_id)
            elif(session["phase"] == 4):
                await self.handle_add_box_phase_description(update,context,session["box"],session,user_id)

        pass
    async def start_handling(self,update:Update,context:ContextTypes.DEFAULT_TYPE,user_id:str):
        user_session = self.session_handler.get_user_session_obj(user_id)

        if (user_session["command_name"] == "addbox"):
            await self.handle_add_box(user_id,update,context)