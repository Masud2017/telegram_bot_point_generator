from dotenv import load_dotenv
import os
from src.Application import Application
from logging import basicConfig, getLogger, INFO

basicConfig(level=INFO)
log = getLogger()

load_dotenv()
# print(os.environ["TELEGRAM_TOKEN"])

application = Application(os.environ["TELEGRAM_TOKEN"])
application.start_application()
