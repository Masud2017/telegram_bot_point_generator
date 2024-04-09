from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()

class Application:
    def __init__(self,telegram_token):
        self.telegram_token = telegram_token

    def start_application(self):
        pass