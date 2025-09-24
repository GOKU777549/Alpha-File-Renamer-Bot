import logging
from telegram.ext import Application
from config import Config
from Alpha import db

# Import all modules
from Alpha.modules import start, thumb, caption, broadcast, status, restart, file_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Register modules
    start.register(application)
    thumb.register(application)
    caption.register(application)
    broadcast.register(application)
    status.register(application)
    restart.register(application)
    file_handler.register(application)

    logger.info("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()