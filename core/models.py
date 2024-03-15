import requests

from core.constants import JAR_BALANCE_URL_PREFIX


class Jar:
    def __init__(self, long_jar_id: str):
        self.long_jar_id = long_jar_id

    def get_current_balance(self):
        url = JAR_BALANCE_URL_PREFIX + self.long_jar_id
        response = requests.get(url).json()

        return response["amount"]
