from asyncio import gather

from telegram import Update
from telegram.ext import ContextTypes

from core.models import Project
from core.services import ProjectsService


async def add_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Не вказано назву збору")
        return

    title = args[0]
    ProjectsService().add_project(update.effective_user, title, ' '.join(args[1:]))
    await update.message.reply_text("Збір успішно додано")


async def _get_project_sum_by_title(project: Project) -> str:
    project_sum = await ProjectsService().project_sum(project)
    return f"{project.title}: {project_sum:.2f}"


async def projects_sum(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    projects = ProjectsService().get_user_projects(update.effective_user)

    match len(projects):
        case 0:
            projects = ProjectsService().get_followed_projects(update.effective_user)
            if not projects:
                await update.message.reply_text("У вас немає активних зборів")
            last_followed_project = sorted(projects, key=lambda p: p.id)[-1]
            project_sum = await ProjectsService().project_sum(last_followed_project)
            await update.message.reply_text(f"{project_sum:.2f}")
        case 1:
            project = projects[0]
            project_sum = await ProjectsService().project_sum(project)
            await update.message.reply_text(f"{project_sum:.2f}")
        case _:
            response = "\n".join(await gather(*[_get_project_sum_by_title(project) for project in projects]))
            await update.message.reply_text(response)


async def follow_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Не вказано назву збору")
        return

    project_title = " ".join(args)
    ProjectsService().follow_project(update.effective_user, project_title)
    await update.message.reply_text(f"Ви підписались на збір {project_title}. "
                                    f"Спробуйте команду /sum для прогресу по збору!")


async def unfollow_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ProjectsService().unfollow_all(update.effective_user)
    await update.message.reply_text("Ви відписались від усіх зборів")


async def deactivate_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    projects = ProjectsService().get_user_projects(update.effective_user)

    match len(projects):
        case 0:
            await update.message.reply_text("У вас немає активних зборів")
        case 1:
            project = projects[0]
            ProjectsService().deactivate_project(project)
            await update.message.reply_text(f"Збір {project.title} деактивовано")
        case _:
            args = context.args
            if len(args) < 1:
                await update.message.reply_text("У вас більше ніж один активний збір. Для деактивації вкажіть назву збору після команди /deactivate_project")
                return

            project_title = " ".join(args)
            try:
                ProjectsService().deactivate_by_title(project_title)
                await update.message.reply_text(f"Збір {project_title} деактивовано")

            except ValueError:
                await update.message.reply_text(f"Збір з назвою {project_title} не знайдено")
