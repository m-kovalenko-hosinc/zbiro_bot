from psycopg2 import errors

from core.db import Session
from core.exceptions import JarAlreadyExists
from core.models import Jar, User, Project


class JarsRepository:
    @staticmethod
    def get_all_jars() -> list[Jar]:
        with Session() as session:
            return session.query(Jar).all()

    @staticmethod
    def get_jar(jar_id: int):
        with Session() as session:
            return session.get(Jar, jar_id)

    @staticmethod
    def add_jar(jar: Jar):
        with Session() as session:
            try:
                session.add(jar)
                session.commit()
                return jar
            except errors.UniqueViolation:
                raise JarAlreadyExists()

    @staticmethod
    def delete_jar(jar: Jar):
        with Session() as session:
            session.delete(jar)
            session.commit()


class UsersRepository:
    @staticmethod
    def get_user(telegram_id: str) -> User | None:
        with Session() as session:
            return session.query(User).filter(User.telegram_id == telegram_id).first()

    @staticmethod
    def add_user(user: User) -> User:
        with Session() as session:
            session.add(user)
            session.commit()
            return user


class ProjectsRepository:
    @staticmethod
    def create_project(project: Project) -> Project:
        with Session() as session:
            session.add(project)
            session.commit()
            return project

    @staticmethod
    def get_user_active_projects(user: User) -> list[Project]:
        with Session() as session:
            return session.query(Project).filter(Project.owner == user, Project.active == True).all()

    @staticmethod
    def get_project_by_title(title: str) -> Project | None:
        with Session() as session:
            return session.query(Project).filter(Project.title == title).first()

    @staticmethod
    def follow_project(user: User, project: Project):
        with Session() as session:
            session.add(user)
            session.add(project)
            user.followed_projects.append(project)
            session.commit()

    @staticmethod
    def get_user_followed_projects(user_telegram_id: str) -> list[Project]:
        with Session() as session:
            user = UsersRepository.get_user(user_telegram_id)
            session.add(user)
            return user.followed_projects

    @staticmethod
    def remove_all_follows(user: User):
        with Session() as session:
            session.add(user)
            user.followed_projects = []
            session.commit()

    @staticmethod
    def deactivate_project(project: Project):
        with Session() as session:
            session.add(project)
            project.active = False
            session.commit()
