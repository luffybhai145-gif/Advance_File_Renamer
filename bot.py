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
    api_id=15055049,
    api_hash=abe3f66fcd80c91e53009ba52c7b3a83,
    bot_token=8784253318:AAGkOy2f650Jzlr-x8XvcuaMVQmd-BBHumA,
)

db = Database("mongodb+srv://newsudo:786780@cluster0.pbiae8a.mongodb.net/?appName=Cluster0")

register_start(app, db)
register_rename(app, db)


if __name__ == "__main__":
    logger.info("===================================")
    logger.info("Advanced File Renamer Starting...")
    logger.info("===================================")

    app.run()
