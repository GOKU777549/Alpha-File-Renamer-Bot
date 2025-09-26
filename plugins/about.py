import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import total_users
from config import ADMIN_ID

START_TIME = time.time()


def get_uptime():
    seconds = int(time.time() - START_TIME)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        return f"{d}d {h}h {m}m {s}s"
    elif h:
        return f"{h}h {m}m {s}s"
    elif m:
        return f"{m}m {s}s"
    else:
        return f"{s}s"


@Client.on_message(filters.command("status"))
async def bot_status(client: Client, message: Message):
    # Only admins can use
    if message.from_user.id not in ADMIN_ID:
        return await message.reply_text("❌ You are not authorized to use this command.")

    users = total_users()  # total users count

    # System stats
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage("/").percent
    uptime = get_uptime()

    text = f"""
✦───────────────✦
🚀 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀 🚀
✦───────────────✦

👥 𝗨𝘀𝗲𝗿𝘀        » {users}
💾 𝗥𝗔𝗠          » {ram}%
🖥️ 𝗖𝗣𝗨          » {cpu}%
📂 𝗦𝘁𝗼𝗿𝗮𝗴𝗲     » {disk}%
⏳ 𝗨𝗽𝘁𝗶𝗺𝗲       » {uptime}
"""
    await message.reply_text(text)