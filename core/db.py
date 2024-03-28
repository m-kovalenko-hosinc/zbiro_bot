import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:0613@localhost:5433/zbirobot")
DEBUG = os.environ.get("DEBUG", False)

engine = create_engine(DATABASE_URL, echo=DEBUG)
Session = sessionmaker(engine, expire_on_commit=False)
