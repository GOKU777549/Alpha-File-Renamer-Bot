import math
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def progress_for_pyrogram(current, total, ud_type, message, start):
    """
    Fancy progress bar with 10-circle top bar, box info below, and CANCEL button
    """
    now = time.time()
    diff = now - start
    if round(diff % 1.0) == 0 or current == total:
        # Percentage
        percentage = current * 100 / total

        # Speed
        speed = current / diff if diff else 0

        # Time calculations
        elapsed_time_ms = int(diff * 1000)
        remaining_time_ms = int((total - current) / speed * 1000 if speed else 0)

        elapsed_time = TimeFormatter(elapsed_time_ms)
        eta = TimeFormatter(remaining_time_ms)

        # ------------------ Progress bar (max 10 circles) ------------------
        total_circles = 10
        done_circles = math.floor((percentage / 100) * total_circles)
        progress_bar = f"[{'●' * done_circles}{'○' * (total_circles - done_circles)}] {percentage:.1f}%"

        # ------------------ Fancy box style ------------------
        text = (
            f"⚡ {progress_bar}\n\n"
            f"╭━━━━❰ ᴘʀᴏɢʀᴇss ʙᴀʀ ❱━➣\n"
            f"┣⪼ 🗃️ Sɪᴢᴇ   : {humanbytes(current)} | {humanbytes(total)}\n"
            f"┣⪼ 🚀 Sᴩᴇᴇᴅ  : {humanbytes(speed)}/s\n"
            f"┣⪼ ⏳ Eᴛᴀ    : {eta}\n"
            f"┣⪼ ⏱️ Tɪᴍᴇ ᴇʟᴀᴩsᴇᴅ : {elapsed_time}\n"
            f"╰━━━━━━━━━━━━━━━➣"
        )

        # ------------------ Inline CANCEL button ------------------
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cᴀɴᴄᴇʟ ❌", callback_data="cancel_upload")]]
        )

        try:
            await message.edit(text=text, reply_markup=buttons)
        except:
            pass

# ------------------ Helper functions ------------------
def humanbytes(size):
    if not size:
        return "0B"
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power and n < 4:
        size /= power
        n += 1
    return f"{round(size,2)} {Dic_powerN[n]}B"

def TimeFormatter(milliseconds: int) -> str:
    seconds, ms = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ""
    if days:
        tmp += f"{days}d "
    if hours:
        tmp += f"{hours}h "
    if minutes:
        tmp += f"{minutes}m "
    if seconds:
        tmp += f"{seconds}s "
    if ms:
        tmp += f"{ms}ms"
    return tmp.strip()