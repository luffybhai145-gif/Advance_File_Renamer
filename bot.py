import logging

from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN
from database import Database

from handlers.start import register as register_start
from handlers.rename import register as register_rename


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("AdvancedFileRenamer")


app = Client(
    "advanced_file_renamer",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

db = Database("bot.db")

register_start(app, db)
register_rename(app, db)


if __name__ == "__main__":
    logger.info("===================================")
    logger.info("Advanced File Renamer Starting...")
    logger.info("===================================")

    app.run()
