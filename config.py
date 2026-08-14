import os


# ==============================
# TEMP DIRECTORY
# ==============================

TEMP_DIR = os.getenv(
    "TEMP_DIR",
    "/tmp"
)


# ==============================
# REQUIRED ENVIRONMENT VARIABLES
# ==============================

def required(name):
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


API_ID = int(
    required("API_ID")
)

API_HASH = required(
    "API_HASH"
)

BOT_TOKEN = required(
    "BOT_TOKEN"
)


# ==============================
# ADMIN IDS
# ==============================

_admin_ids = os.getenv(
    "ADMIN_IDS",
    ""
)

ADMIN_IDS = {
    int(x.strip())
    for x in _admin_ids.split(",")
    if x.strip().isdigit()
}


# ==============================
# FFMPEG CONCURRENCY
# ==============================

MAX_CONCURRENT_FFMPEG = int(
    os.getenv(
        "MAX_CONCURRENT_FFMPEG",
        "1"
    )
)
