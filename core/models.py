from typing import Optional

import requests
from sqlalchemy.orm import Mapped, mapped_column

from core.constants import JAR_BALANCE_URL_PREFIX
from core.db import Base


class Jar(Base):
    __tablename__ = "jars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    long_jar_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    title: Mapped[Optional[str]]

    def __repr__(self):
        return f"Jar(id={self.id}, long_jar_id={self.long_jar_id}, title={self.title})"

    def get_current_balance(self):
        url = JAR_BALANCE_URL_PREFIX + self.long_jar_id
        response = requests.get(url).json()

        return response["amount"]
