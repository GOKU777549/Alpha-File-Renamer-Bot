import psutil
import platform
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from Alpha import db

start_time = datetime.now()


def get_readable_time(seconds: int) -> str:
    """Convert seconds to human-readable uptime"""
    periods = [
        ('d', 60 * 60 * 24),
        ('h', 60 * 60),
        ('m', 60),
        ('s', 1)
    ]
    strings = []
    for name, count in periods:
        value = seconds // count
        if value:
            seconds -= value * count
            strings.append(f"{value}{name}")
    return " ".join(strings)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot status info"""
    uptime = get_readable_time((datetime.now() - start_time).seconds)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    total_users = await db.users_col.count_documents({})

    text = f"""
📊 **Bot Status**

⏱ Uptime: `{uptime}`
💾 RAM Usage: `{ram_usage}%`
🖥 CPU Usage: `{cpu_usage}%`
👥 Total Users: `{total_users}`
"""

    await update.message.reply_text(text, parse_mode="Markdown")


def register(application):
    application.add_handler(CommandHandler("status", status))