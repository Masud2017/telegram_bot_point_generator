import os
from dotenv import load_dotenv
from src.DataBase import DataBase

load_dotenv()

db_url = ""
if (os.environ["PROD"] == "0"):
    
    db_url = os.environ["REDIS_PROD_URL"]
else :
    db_url = os.environ["REDIS_DEV_URL"]
print(db_url)
db = DataBase(db_url)

user_session = dict()