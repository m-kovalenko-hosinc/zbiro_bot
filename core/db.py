from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("postgresql://postgres:0613@localhost:5433/zbirobot", echo=True)
# engine = create_engine("postgresql+psycopg2://postgres:0613@localhost/zbirobot", echo=True)
Session = sessionmaker(engine, expire_on_commit=False)
