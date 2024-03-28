from typing import Optional, List

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Jar(Base):
    __tablename__ = "jars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    long_jar_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    title: Mapped[Optional[str]]

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="jars")

    def __repr__(self):
        return f"Jar(id={self.id}, long_jar_id={self.long_jar_id}, title={self.title})"


association_table = Table(
    "followers",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("project_id", ForeignKey("projects.id")),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[Optional[str]]

    projects: Mapped[List["Project"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    followed_projects: Mapped[List["Project"]] = relationship(secondary=association_table)

    def __repr__(self):
        return f"User(id={self.id}, telegram_id={self.telegram_id}, nickname={self.nickname}, " \
               f"first_name={self.first_name}, last_name={self.last_name})"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]]
    active: Mapped[bool] = mapped_column(default=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="projects")

    jars: Mapped[List["Jar"]] = relationship(back_populates="project", cascade="all, delete-orphan")

    followers: Mapped[List["User"]] = relationship(secondary=association_table)

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title}, description={self.description})"
