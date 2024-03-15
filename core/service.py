from core.models import Jar


class ZbirobotService:
    def get_total_amount(self) -> float:
        from core.jars_creds import JARS
        amount_in_kopeks = sum([Jar(jar_id).get_current_balance() for jar_id, _ in JARS])
        return float(amount_in_kopeks) / 100


if __name__ == '__main__':
    service = ZbirobotService()
    print(service.get_total_amount())
