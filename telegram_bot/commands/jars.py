import logging

from telegram import Update
from telegram.ext import ContextTypes

from core.services import JarsService, ProjectsService

logger = logging.getLogger(__name__)


async def add_jar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 1:
        await update.message.reply_text(
            "Для додавання банки вкажіть посилання на сторінку створення віджету для стрімів з банки"
            " після команди /add_jar \n"
            "(Отримати посилання можна зайшовни на сторінку банки з версії для комп'ютера, "
            "та натиснувши кнопку 'Віджет для стрімів'. Адреса сторінки є потрібним Вам посиланням)"
        )
        return

    projects = ProjectsService().get_user_projects(update.effective_user)
    if len(projects) == 0:
        await update.message.reply_text(
            "У вас немає активних зборів. "
            "Для додавання банки спочатку створіть збір за допомогою команди /add_project."
        )
        return

    if len(projects) > 1:
        await update.message.reply_text(
            "Ви маєте більше ніж один активний збір."
            "Наразі підтримується наявність лише одного активного збору, "
            "для додавання банки закрийте всі збори окрім одного і спробуйте ще раз.\n"
            "У разі якщо Вам потрібно мати більше ніж один активний збір напишіть розробнику @maks_kovalenko"
        )
        return

    project = projects[0]
    jar_widget_url = args[0]
    title = ' '.join(args[1:]) if args[1:] else None
    try:
        jar = JarsService().add_jar(widget_url=jar_widget_url, title=title, project=project)
        await update.message.reply_text(f"Банка{' ' + jar.title} успішно додана до збору {project.title}")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Не вдалося додати банку")


async def get_all_jars(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    jars_by_project = ProjectsService().get_all_jars_by_user_projects(update.effective_user)

    if not jars_by_project:
        await update.message.reply_text("У вас немає активних зборів")
        return

    reply = ""
    for project_title, jars in jars_by_project.items():
        reply += f"{project_title}:\n"
        for jar in jars:
            jar_sum, jar_open = await JarsService().get_jar_balance_and_state(jar)
            reply += f"\t{jar.title}: {float(jar_sum) / 100:.2f} {'🟢' if jar_open else '🔴'}\n"
        reply += "\n"

    await update.message.reply_text(reply)
