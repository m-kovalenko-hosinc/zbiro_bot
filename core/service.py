import requests

from core.constants import JAR_BALANCE_URL_PREFIX
from core.models import Jar
from core.repositories import JarsRepository


class ZbirobotService:
    @staticmethod
    def get_jar_balance(jar: Jar) -> float:
        url = JAR_BALANCE_URL_PREFIX + jar.long_jar_id
        response = requests.get(url).json()

        return response["amount"]

    @classmethod
    def get_total_amount(cls) -> float:
        jars = JarsRepository.get_all_jars()
        amount_in_kopeks = sum([cls.get_jar_balance(jar) for jar in jars])
        return float(amount_in_kopeks) / 100

    @staticmethod
    def parse_jar_id(jar_widget_url: str) -> str:
        return jar_widget_url.split("longJarId=")[1].split("&")[0]

    @staticmethod
    def add_jar(jar_widget_url: str, title: str | None) -> Jar:
        long_jar_id = ZbirobotService.parse_jar_id(jar_widget_url)
        jar = Jar(long_jar_id=long_jar_id, title=title)
        return JarsRepository.add_jar(jar)

    @staticmethod
    def get_jars() -> list[Jar]:
        return JarsRepository.get_all_jars()


if __name__ == '__main__':
    service = ZbirobotService()
    print(service.get_total_amount())
