from dataclasses import dataclass, field


@dataclass(eq=False)
class DomainError(Exception):
    message: str = field(default="Domain Error")


class AutoNumberValidationError(DomainError):
    pass


class AutoModelValidationError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass
