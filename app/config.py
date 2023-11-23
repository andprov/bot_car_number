import os

from dotenv import load_dotenv

load_dotenv()

MAX_AUTO_COUNT = 10
MAX_AUTO_NAME_LEN = 50
MAX_AUTO_NUMBER_LEN = 9

# BOT
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN = os.getenv("ADMIN_ID")
GROUP = os.getenv("GROUP_ID")

# DB
DB_TYPE = os.getenv("DB_TYPE")
DB_CONNECTOR = os.getenv("DB_CONNECTOR")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bot")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

DB_URL = (
    f"{DB_TYPE}+{DB_CONNECTOR}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
)

# LOG
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
