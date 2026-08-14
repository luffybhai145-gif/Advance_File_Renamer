import os


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

# Optional
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://newsudo:786780@cluster0.pbiae8a.mongodb.net/?appName=Cluster0")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7653921320"))
