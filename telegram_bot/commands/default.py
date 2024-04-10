from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт, щоб отримати суму по банкам відправ мені /sum')


async def help(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Доступні команди:\n'
                                    '/add_jar - додати банку\n'
                                    '/all_jars - показати всі банки\n'
                                    '/add_project - додати збір\n'
                                    '/follow_project - підписатись на збір\n'
                                    '/deactivate_project - закрити збір\n'
                                    '/sum - показати суму по збору')
