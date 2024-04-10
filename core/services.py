from asyncio import gather

import aiohttp
from telegram import User as TelegramUser

from core.constants import JAR_BALANCE_URL_PREFIX
from core.db import Session
from core.models import Jar, User, Project
from core.repositories import JarsRepository, UsersRepository, ProjectsRepository


class JarsService:
    @staticmethod
    async def get_jar_balance_and_state(jar: Jar) -> (float, bool):
        url = JAR_BALANCE_URL_PREFIX + jar.long_jar_id
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.json()

        return response["amount"], response["closed"] is False

    @classmethod
    async def get_jars_total_amount(cls, jars: list[Jar]) -> float:
        jars_info = await gather(*[cls.get_jar_balance_and_state(jar) for jar in jars])
        amount_in_kopeks = sum([jar_balance for jar_balance, _ in jars_info])
        return float(amount_in_kopeks) / 100

    @staticmethod
    def parse_jar_id(jar_widget_url: str) -> str:
        return jar_widget_url.split("longJarId=")[1].split("&")[0]

    @staticmethod
    def add_jar(*, widget_url: str, project: Project, title: str | None) -> Jar:
        long_jar_id = JarsService.parse_jar_id(widget_url)
        jar = Jar(long_jar_id=long_jar_id, title=title, project=project)
        return JarsRepository.add_jar(jar)

    @staticmethod
    def get_jars() -> list[Jar]:
        return JarsRepository.get_all_jars()


class UsersService:
    @staticmethod
    def get_or_create_user(telegram_user: TelegramUser) -> User:
        user = UsersRepository.get_user(str(telegram_user.id))
        if user is None:
            user = UsersRepository.add_user(
                User(telegram_id=str(telegram_user.id), nickname=telegram_user.username,
                     first_name=telegram_user.first_name, last_name=telegram_user.last_name)
            )

        return user


class ProjectsService:
    @staticmethod
    def add_project(owner: TelegramUser, title: str, description: str | None) -> Project:
        user = UsersService().get_or_create_user(owner)
        project = Project(title=title, description=description, owner=user)
        ProjectsRepository.create_project(project)

        return project

    @staticmethod
    def get_user_projects(owner: TelegramUser) -> list[Project]:
        user = UsersRepository.get_user(str(owner.id))
        return ProjectsRepository.get_user_active_projects(user)

    @staticmethod
    async def project_sum(project: Project) -> float:
        with Session() as session:
            session.add(project)
            return await JarsService.get_jars_total_amount(project.jars)

    @staticmethod
    def get_project_by_title(title: str) -> Project:
        return ProjectsRepository.get_project_by_title(title)

    @staticmethod
    def get_all_jars_by_user_projects(user: TelegramUser) -> dict[str, list[Jar]]:
        projects = ProjectsService().get_user_projects(user)
        with Session() as session:
            for project in projects:
                session.add(project)
            return {project.title: project.jars for project in projects}

    @staticmethod
    def follow_project(user: TelegramUser, project_title: str) -> None:
        user = UsersService().get_or_create_user(user)
        project = ProjectsService().get_project_by_title(project_title)
        ProjectsRepository.follow_project(user, project)

    @staticmethod
    def unfollow_all(user: TelegramUser) -> None:
        user = UsersService().get_or_create_user(user)
        ProjectsRepository.remove_all_follows(user)

    @staticmethod
    def deactivate_project(project: Project) -> None:
        ProjectsRepository.deactivate_project(project)

    @staticmethod
    def deactivate_by_title(project_title: str) -> None:
        project = ProjectsService().get_project_by_title(project_title)
        if project is None:
            raise ValueError("Project not found")
        ProjectsRepository.deactivate_project(project)

    @staticmethod
    def get_followed_projects(user: TelegramUser) -> list[Project]:
        return ProjectsRepository.get_user_followed_projects(str(user.id))
