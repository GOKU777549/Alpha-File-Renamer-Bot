import os

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your-bot-token-here")
    API_ID = int(os.getenv("API_ID", 12345))
    API_HASH = os.getenv("API_HASH", "your-api-hash-here")

    # Database (MongoDB)
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "FileRenamerBot")

    # Admins (for broadcast/restart)
    ADMINS = [int(x) for x in os.getenv("ADMINS", "123456789").split()]

    # Others
    DOWNLOAD_DIR = "./downloads"
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 2 * 1024 * 1024 * 1024))  # 2GB default