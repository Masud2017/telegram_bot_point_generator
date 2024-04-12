import redis
import json

class DataBase:
    def __init__(self,url):
        if (url == "rediss://127.0.0.1:6379"):
            self.db = redis.Redis()
        else:
            self.db = redis.from_url(url)
        
        users = {}
        inventories = {}
        boxes = {}

        users_str = self.db.get("users")
        if not users_str:
            self.db.set("users", json.dumps(users))
        else:
            users = json.loads(users_str.decode("utf-8"))

        inventories_str = self.db.get("inventories")
        if not inventories_str:
            self.db.set("inventories", json.dumps(inventories))
        else:
            inventories = json.loads(inventories_str.decode("utf-8"))

        boxes_str = self.db.get("boxes")
        if not boxes_str:
            self.db.set("boxes", json.dumps(boxes))
        else:
            boxes = json.loads(boxes_str.decode("utf-8"))

    def init_users(self,user_id:str, message):
        users = json.loads(self.db.get("users"))
        print(message)

        if (user_id not in users):

            users[str(message.from_user.id)] = {
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "username": message.from_user.username,
                "balance": 0,
                "inventory": []
            }
            # with open("/var/data/users.json", "w") as f:
            #     json.dump(users, f, indent=4)
            self.db.set("users", json.dumps(users))

    def init_inventories(self,user_id:str):
        pass
    def init_boxes(self,user_id:str):
        pass

    def update_record(self,key:str,val):
        self.db.set(key, json.dumps(val))

    def get_balance(self,user_id:str):

        return json.loads(self.db.get("users"))[user_id]["balance"]
        
    def add_balance(self,user_id:str,balance:int):
        users = json.loads(self.db.get("users"))
        user_id = str(user_id).strip()
        if self.is_user_exist(str(user_id)):
            users[user_id]["balance"] += balance
       
        self.update_record("users",users)
    
    async def transfer_currency(self,sender_id:str, receiver_id:str, amount:int):
        users = json.loads(self.db.get("users"))
        if amount < 0: return False
        if users[sender_id]["balance"] >= amount:
            users[sender_id]["balance"] -= amount
            users[receiver_id]["balance"] += amount
            
            self.db.set("users", json.dumps(users))
            return True
        return False
    

    def is_user_exist(self,user_id:str):
        users = json.loads(self.db.get("users"))
        
        if user_id in users:
            return True
        else:
            False


    # def get_inventory(self,user_id:str):
    #     users = json.loads(self.db.get("users"))
    #     inventory = {}
    #     for item in users[user_id]["inventory"]:
    #         name = item["name"]
    #         if name in inventory:
    #             inventory[name] += 1
    #         else:
    #             inventory[name] = 1

    #     return inventory
    
    def is_inventory_available_for_user(self,user_id):
        users = json.loads(self.db.get("users"))

        if len(users[user_id]["inventory"]) == 0:
            return False
        else:
            True

    def get_inventory_of_a_user(self,user_id:str):
        users = json.loads(self.db.get("users"))
        
        inventory = {}
        for item in users[user_id]["inventory"]:
            name = item["name"]
            if name in inventory:
                inventory[name] += 1
            else:
                inventory[name] = 1
        msg = f"{user_id}의 인벤토리:\n"
        for i, item in enumerate(inventory):
            msg += f"{i+1}: {item} - 수량: {inventory[item]}\n"

        return msg
    def is_box_exists(self,box_id:str):
        boxes = json.loads(self.db.get("boxes"))

        if box_id in boxes:
            return True
        else:
            return False
        
    def save_box_item_to_db(self,box_id,box):
        boxes = json.loads(self.db.get("boxes"))

        if box_id not in boxes:
            boxes.update(box)
        self.db.set("boxes", json.dumps(boxes))    

    def get_boxes_info_as_msg(self):
        boxes = json.loads(self.db.get("boxes"))

        msg = "📦오픈 가능한 박스📦\n\n"
        for i, box_id in enumerate(boxes):
            msg += f"{i+1}: {boxes[box_id]['name']} - {boxes[box_id]['price']} 포인트\n{boxes[box_id]['description']}\n\n"

        return msg
    def delete_box(self,box_id:str):
        boxes = json.loads(self.db.get("boxes"))

        if box_id in boxes:
            boxes.pop(box_id)       
            self.db.set("boxes", json.dumps(boxes))

    def update_box_item_to_db(self,box_id,box):
        boxes = json.loads(self.db.get("boxes"))        

        print("Inspecting the box object",boxes)

        # if box_id in boxes:
            
        boxes[str(box_id)]["name"] = box[box_id]["name"]
        boxes[str(box_id)]["price"] = box[box_id]["price"]
        boxes[str(box_id)]["description"] = box[box_id]["description"]
        
        self.db.set("boxes", json.dumps(boxes))

    def add_item_item_to_db(self,box_id,item):
        boxes = json.loads(self.db.get("boxes"))

    
        
        boxes[str(box_id)]["items"].append(item)
        print("boxes : ",boxes[str(box_id)])
        self.db.set("boxes", json.dumps(boxes))

    def get_items_info_as_msg(self,box_id):
        boxes = json.loads(self.db.get("boxes"))
        msg = ""
        if box_id in boxes:
            msg = f"Items in box {box_id}:\n"
            for i, item in enumerate(boxes[box_id]["items"]):
                msg += f"{i+1}: {item['name']} - Probability: {item['probability']}%\n"
        else:
            msg = "The box id does not exists."

        return msg
    
    def update_item_info(self,box_id:str,item_name,probability):
        boxes = json.loads(self.db.get("boxes"))

        print(boxes[box_id]["items"])
        for x_item in boxes[box_id]["items"]:

            if item_name == x_item["name"]:
                x_item["probability"] = probability

        self.db.set("boxes", json.dumps(boxes))

    def get_all_boxes_for_unlistitem(self):
        boxes = json.loads(self.db.get("boxes"))
        msg = ""
        for i, box_id in enumerate(boxes):
            msg += f"{i+1}: {boxes[box_id]['name']} box id : {box_id}\n"
        msg += "\n박스를 선택하기 위해 박스의 아이디를 적어주세요, 전체의 경우 \"all\"을 적어주세요."

        return msg
    
    def is_boxes_empty(self):
        boxes = json.loads(self.db.get("boxes"))

        if (len(boxes) == 0):
            return True
        else:
            return False
        
    def get_all_boxes(self):
        return json.loads(self.db.get("boxes"))

    def deduct_balance(self,box_id:str,user_id:str):
        users = json.loads(self.db.get("users"))
        boxes = json.loads(self.db.get("boxes"))

        if self.is_user_exist(user_id):
            if self.is_box_exists(box_id):
                if users[user_id]["balance"] >= boxes[box_id]["price"]:
                    users[user_id]["balance"] -= boxes[box_id]["price"]

                    self.db.set("users", json.dumps(users))
                    return True
                else:
                    return False

        
    def add_random_item_to_user_inventory(self,user_id,random_item):
        users = json.loads(self.db.get("users"))

        if self.is_user_exist(user_id):
            users[user_id]["inventory"].append(random_item)
            self.db.set("users", json.dumps(users))
            return True
        else:
            return False
        
    def withdraw_item_from_inventory(self,user_id,quantity,item_name):
        users = json.loads(self.db.get("users"))

        if self.is_user_exist(user_id):
            if quantity == None:
                pass
    
            for _ in range(quantity):
                for item in users[user_id]["inventory"]:
                    if item["name"] == item_name:
                        users[user_id]["inventory"].remove(item)
                        break
            self.update_record("users",users)

            return True
        else:
            return False
        
    def remove_item_from_box(self,box_id,item_name):
        boxes = json.loads(self.db.get("boxes"))
        if self.is_box_exists(box_id):
            for x_item in boxes[box_id]["items"]:
                if item_name == x_item["name"]:
                    boxes[box_id]["items"].remove(x_item)
                    break
            self.update_record("boxes",boxes)
            return True

        else:
            False
    def get_box_id_by_sequence_no(self,sequence_no):
        boxes = json.loads(self.db.get("boxes"))
        box_id = int(sequence_no)
        if (box_id <= len(boxes.keys())):
            box_id = list(boxes.keys())[int(box_id)-1]
            return str(box_id)