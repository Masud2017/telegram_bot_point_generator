from src.SessionHandler import SessionHandler
from telegram.ext import ContextTypes
from telegram import Update
from src import db
from src.Util import get_random_item

class SessionedCommandHandler:
    def __init__(self):
        self.session_handler = SessionHandler()
    
    # add box section started
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
    # add box section ended



    # edit box section started
    async def handle_edit_box_phase_name(self,update:Update, context : ContextTypes.DEFAULT_TYPE,box,session,user_id:str):
        box_id = session["item_id"]  
        box[box_id] = {
                        "name": update.message.text,
                        "description": None,
                        "price": None,
                        "items": []
        }  

        self.session_handler.update_session(user_id,box_id,update_item_id=True)

        await update.message.reply_text("박스 오픈 금액을 적어주세요.")


    async def handle_edit_box_phase_price(self, update:Update, context : ContextTypes.DEFAULT_TYPE,box,session,user_id:str):
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

    async def handle_edit_box_phase_description(self, update:Update, context : ContextTypes.DEFAULT_TYPE,box,session,user_id:str):
        box_id = session["item_id"]
        box[box_id]["description"] = update.message.text
        db.update_box_item_to_db(box_id,box)
        
        await update.message.reply_text("상자가 성공적으로 업데이트되었습니다.")
        self.session_handler.remove_user_session(user_id)

    async def handle_edit_box(self,user_id:str,update:Update,context:ContextTypes.DEFAULT_TYPE):
        session = self.session_handler.get_user_session_obj(user_id)
        if "box" not in session:
            session["box"] = {}

        if len(session) > 0:
            if (session["phase"] == 1):
                # box_id = update.message.text
                box_id = db.get_box_id_by_sequence_no(update.message.text)
                if str(box_id).isnumeric():
                    if not db.is_box_exists(box_id):
                       await update.message.reply_text("해당 상자의 ID가 존재하지 않습니다. 기존 상자 ID를 입력하세요.")
                       self.session_handler.remove_user_session(user_id)
                       return

                    self.session_handler.update_session(user_id,int(box_id),True)
                    await update.message.reply_text("편집할 상자 이름을 적어주세요.")
                else:
                    await update.message.reply_text("You need to provide a valid existing box id to edit.")
            elif(session["phase"] == 2):
                await self.handle_edit_box_phase_name(update,context,session["box"],session,user_id)
            elif(session["phase"] == 3):
                await self.handle_edit_box_phase_price(update,context,session["box"],session,user_id)
            elif(session["phase"] == 4):
                await self.handle_edit_box_phase_description(update,context,session["box"],session,user_id)
 
    # edit box section ended
                

    # add item section started
    async def handle_add_item_phase_name(self,update:Update, context : ContextTypes.DEFAULT_TYPE,item,session,user_id:str):
        box_id = session["item_id"]  

        item.update({
            "name":update.message.text,
            "probability":None
        })

        self.session_handler.update_session(user_id,box_id,update_item_id=True)

        await update.message.reply_text("아이템의 확률을 적어주세요.")


    async def handle_add_item_phase_probability(self, update:Update, context : ContextTypes.DEFAULT_TYPE,item,session,user_id:str):
        box_id = session["item_id"]  
        try: 
            probability  = int(update.message.text)
            print("Probability : " ,session["item"])

            item["probability"] = probability
        except:
            import traceback
            traceback.print_exc()
            await update.message.reply_text("올바른 확률 값을 입력하세요.")
            return
        self.session_handler.update_session(user_id,box_id,update_item_id=True)
        await update.message.reply_text("박스 이미지를 보내주세요.")

    async def handle_add_item_phase_image(self, update:Update, context : ContextTypes.DEFAULT_TYPE,item,session,user_id:str):
        box_id = session["item_id"]
        
        
        if update.message.photo:
        
            # file_id = update.message.document.file_id
            
            
            file_id = update.message.photo[0].file_id
            session["item"]["image"] = file_id
        # box[box_id]["description"] = update.message.text
            db.add_item_item_to_db(box_id,item)
        
            await update.message.reply_text("항목이 성공적으로 저장되었습니다.")
            self.session_handler.remove_user_session(user_id)
        else:
            await update.message.reply_text("유효한 이미지를 보내주세요.")

    async def handle_add_item(self,user_id:str,update:Update,context:ContextTypes.DEFAULT_TYPE):
        session = self.session_handler.get_user_session_obj(user_id)
        if "item" not in session:
            session["item"] = {}

        if len(session) > 0:
            if (session["phase"] == 1):
                box_id = update.message.text
                box_id = db.get_box_id_by_sequence_no(box_id)
                if box_id.isnumeric():
                    if not db.is_box_exists(box_id):
                       await update.message.reply_text("해당 상자의 ID가 존재하지 않습니다. 기존 상자 ID를 입력하세요.")
                       self.session_handler.remove_user_session(user_id)
                       return

                    self.session_handler.update_session(user_id,int(box_id),True)
                    await update.message.reply_text("아이템의 이름을 적어주세요.")
                else:
                    await update.message.reply_text("You need to provide a valid existing box id to edit.")
            elif(session["phase"] == 2):
                await self.handle_add_item_phase_name(update,context,session["item"],session,user_id)
            elif(session["phase"] == 3):
                await self.handle_add_item_phase_probability(update,context,session["item"],session,user_id)
            elif(session["phase"] == 4):
                await self.handle_add_item_phase_image(update,context,session["item"],session,user_id)
 

    # add item section ended
                 

    #open box section started
                
    async def handle_open_box(self,user_id:str,update:Update,context:ContextTypes.DEFAULT_TYPE):
        session = self.session_handler.get_user_session_obj(user_id)
        if "item" not in session:
            session["item"] = {}

        if len(session) > 0:
            if (session["phase"] == 1):
                box_id = update.message.text
                if box_id.isnumeric():
                    if not db.is_box_exists(box_id):
                       await update.message.reply_text("해당 상자의 ID가 존재하지 않습니다. 기존 상자 ID를 입력하세요.")
                       self.session_handler.remove_user_session(user_id)
                       return

                    boxes = db.get_all_boxes()
                    box_id = db.get_box_id_by_sequence_no(box_id)
                    box = boxes[box_id]
                    if len(box["items"]) == 0:
                        await update.message.reply_text("This box does not have any item. Please enter a box that contains at least one item.")
                        self.session_handler.remove_user_session(user_id)
                        return
                    
                    if not db.deduct_balance(box_id,user_id):
                        await update.message.reply_text("잔액이 부족합니다.")
                        self.session_handler.remove_user_session(user_id)
                        return
                    
                    random_item = get_random_item(box)

                    if not db.add_random_item_to_user_inventory(user_id,random_item):
                            await update.message.reply_text("Something went wrong while trying to save the random item to user's inventory.")
                            self.session_handler.remove_user_session(user_id)
                            return
                    await update.message.reply_text(f"🎇 축하드립니다 !! 상자에서 {random_item['name']}이 나왔습니다 🎇")

                    await update.message.reply_photo(photo=random_item["image"],caption = random_item["name"])
                    self.session_handler.remove_user_session(user_id)
                
    #open box section ended        


    async def start_handling(self,update:Update,context:ContextTypes.DEFAULT_TYPE,user_id:str):
        user_session = self.session_handler.get_user_session_obj(user_id)

        if (user_session["command_name"] == "addbox"):
            await self.handle_add_box(user_id,update,context)
        elif(user_session["command_name"] == "editbox"):
            await self.handle_edit_box(user_id,update,context)
        elif(user_session["command_name"] == "additem"):
            await self.handle_add_item(user_id,update,context)

        
        elif(user_session["command_name"] == "openbox"):
            await self.handle_open_box(user_id,update,context)
