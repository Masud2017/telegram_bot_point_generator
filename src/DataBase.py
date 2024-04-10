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
        if user_id in users:
            users[user_id]["balance"] += balance
        else:
            users[str(user_id)] = {
                "first_name": "Unknown",
                "last_name": "Unknown",
                "username": "Unknown",
                "balance": balance,
                "inventory": []
            }
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