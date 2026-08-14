import os

from dotenv import load_dotenv


load_dotenv()


def required(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


API_ID = int(required("API_ID"))

API_HASH = required("API_HASH")

BOT_TOKEN = required("BOT_TOKEN")

DATABASE_URL = required("DB_URL")

ADMIN_IDS = {
    int(user_id.strip())
    for user_id in required("ADMIN_IDS").split(",")
    if user_id.strip()
}


MAX_CONCURRENT_FFMPEG = int(
    os.getenv("MAX_CONCURRENT_FFMPEG", "1")
)


TEMP_DIR = os.getenv(
    "TEMP_DIR",
    "/tmp/advanced-file-renamer"
)


os.makedirs(TEMP_DIR, exist_ok=True)
