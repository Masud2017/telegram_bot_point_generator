from dotenv import load_dotenv
import os
from src.Application import Application

load_dotenv()
# print(os.environ["TELEGRAM_TOKEN"])

application = Application(os.environ["TELEGRAM_TOKEN"])
application.start_application()