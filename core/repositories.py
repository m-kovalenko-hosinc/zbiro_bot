from core.db import Session
from core.models import Jar


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
            session.add(jar)
            session.commit()
            return jar

    @staticmethod
    def delete_jar(jar: Jar):
        with Session() as session:
            session.delete(jar)
            session.commit()
