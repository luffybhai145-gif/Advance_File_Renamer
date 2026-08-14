import os


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

# Optional
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
