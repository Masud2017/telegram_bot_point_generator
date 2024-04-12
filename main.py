from dotenv import load_dotenv
import os
from src.Application import Application
from logging import basicConfig, getLogger, INFO

basicConfig(level=INFO)
log = getLogger()

load_dotenv()


if __name__ == "__main__":
    application = Application(os.environ["TELEGRAM_TOKEN"])
    application.start_application()
