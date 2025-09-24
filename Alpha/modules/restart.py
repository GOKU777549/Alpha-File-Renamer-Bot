import os
import sys
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Restart the bot"""
    await update.message.reply_text("♻️ Bot Restarting... Please wait!")

    # Restart process
    os.execv(sys.executable, ['python'] + sys.argv)


def register(application):
    application.add_handler(CommandHandler("restart", restart))