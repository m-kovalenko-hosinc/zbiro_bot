from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///zbirobot.db", echo=True)
Session = sessionmaker(engine, expire_on_commit=False)
