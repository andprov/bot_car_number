from dataclasses import dataclass


@dataclass
class AppError(Exception):
    message: str = "ERROR: App error"


@dataclass
class UserNotFoundError(AppError):
    message: str = "ERROR: User not found"


@dataclass
class AutoAlreadyExistsError(AppError):
    message: str = "ERROR: Auto already exists"


@dataclass
class AutoNotFoundError(AppError):
    message: str = "ERROR: Auto not found"


@dataclass
class AutoOwnerError(AppError):
    message: str = "ERROR: Attempt to modify an auto by non-owner"
