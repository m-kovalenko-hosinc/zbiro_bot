import logging

from telegram.ext import ApplicationBuilder, CommandHandler

from telegram_bot.commands.default import start
from telegram_bot.commands.jars import add_jar, get_all_jars
from telegram_bot.commands.projects import add_project, projects_sum
from telegram_bot.credentials import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_jar", add_jar))
    app.add_handler(CommandHandler("all_jars", get_all_jars))
    app.add_handler(CommandHandler("add_project", add_project))
    app.add_handler(CommandHandler("sum", projects_sum))

    app.run_polling()


if __name__ == '__main__':
    main()
