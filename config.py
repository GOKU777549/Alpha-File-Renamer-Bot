import os

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8302777365:AAGoG2wE6fujqDyMe2oI8eC-wzfwtOIq1e8")
    API_ID = int(os.getenv("API_ID", 21218274))
    API_HASH = os.getenv("API_HASH", "3474a18b61897c672d315fb330edb213)

    # Database (MongoDB)
    MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot")
    DB_NAME = os.getenv("DB_NAME", "FileRenamerBot")

    # Admins (for broadcast/restart)
    ADMIN_ID = [int(x) for x in os.getenv("ADMINS", "7576729648").split()]

    # Others
    DOWNLOAD_DIR = "./downloads"
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 2 * 1024 * 1024 * 1024))  # 2GB default