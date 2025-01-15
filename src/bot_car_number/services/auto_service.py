import re


# TODO: fix
class AutoService:
    @classmethod
    def validate_number(cls, number: str) -> bool:
        pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
        if pattern.match(number):
            return True
        return False
