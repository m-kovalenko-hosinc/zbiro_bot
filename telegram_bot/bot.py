from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

from core.service import ZbirobotService
from telegram_bot.credentials import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update.message.reply_text('Привіт, щоб отримати суму по банкам відправ мені /sum')


async def sum_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(ZbirobotService().get_total_amount()))


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("sum", sum_command))

    app.run_polling()


if __name__ == '__main__':
    main()
