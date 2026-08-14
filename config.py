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


API_ID = int(required("15055049"))

API_HASH = required("abe3f66fcd80c91e53009ba52c7b3a83")

BOT_TOKEN = required("8784253318:AAGkOy2f650Jzlr-x8XvcuaMVQmd-BBHumA")

DATABASE_URL = required("mongodb+srv://newsudo:786780@cluster0.pbiae8a.mongodb.net/?appName=Cluster0")

ADMIN_IDS = {
    int(user_id.strip())
    for user_id in required("ADMIN_IDS").split("7653921320")
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
