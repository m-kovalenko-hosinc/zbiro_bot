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


async def add_jar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Не вказано ID банки")
        return

    jar_widget_url = args[0]
    title = ' '.join(args[1:]) if args[1:] else None
    try:
        jar = ZbirobotService().add_jar(jar_widget_url, title)
        await update.message.reply_text(f"Банка{' ' + jar.title} успішно додана")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Не вдалося додати банку")


async def get_all_jars_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    jars = ZbirobotService().get_jars()
    await update.message.reply_text('\n'.join([f"{jar.title}: {jar.long_jar_id}" for jar in jars]))


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("sum", sum_command))
    app.add_handler(CommandHandler("add_jar", add_jar_command))
    app.add_handler(CommandHandler("all_jars", get_all_jars_command))

    app.run_polling()


if __name__ == '__main__':
    main()
