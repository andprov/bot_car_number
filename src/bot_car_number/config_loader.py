import os

MAX_AUTO_COUNT = 10
MAX_AUTO_NAME_LEN = 50
MAX_REGISTRATIONS_COUNT = 2
SEARCH_COUNT_LIMIT = 3
TIME_LIMIT = 3


def get_env_value(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is not set")
    return value
