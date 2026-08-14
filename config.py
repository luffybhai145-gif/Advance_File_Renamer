import os

TEMP_DIR = os.getenv("TEMP_DIR", "/tmp")
# ✅ CORRECT (casting to int)
FFMPEG_SEMAPHORE = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENT_TRANSCODES", 1)))


def required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


API_ID = int(required("API_ID"))
API_HASH = required("API_HASH")
BOT_TOKEN = required("BOT_TOKEN")

# Comma-separated Telegram user IDs
_admin_ids = os.getenv("ADMIN_IDS", "")

ADMIN_IDS = {
    int(x.strip())
    for x in _admin_ids.split(",")
    if x.strip().isdigit()
}
