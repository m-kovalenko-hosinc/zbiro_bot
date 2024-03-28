from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт, щоб отримати суму по банкам відправ мені /sum')
