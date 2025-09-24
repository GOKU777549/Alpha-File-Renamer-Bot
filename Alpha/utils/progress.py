import math, time
from telegram import Message


async def progress_for_pyrogram(current, total, ud_type, message: Message, total_size):
    now = time.time()
    diff = now - message.date.timestamp()
    if diff == 0:
        diff = 1

    percentage = current * 100 / total
    speed = current / diff
    eta = (total - current) / speed if speed != 0 else 0

    progress_str = "[{0}{1}] {2}%".format(
        ''.join(["■" for i in range(math.floor(percentage / 5))]),
        ''.join(["□" for i in range(20 - math.floor(percentage / 5))]),
        round(percentage, 2)
    )

    text = f"""
**{ud_type}**
Progress: {progress_str}
{round(current / 1024 / 1024, 2)} MB / {round(total_size / 1024 / 1024, 2)} MB
⚡ Speed: {round(speed / 1024 / 1024, 2)} MB/s
⏳ ETA: {time.strftime("%H:%M:%S", time.gmtime(eta))}
"""
    try:
        await message.edit_text(text, parse_mode="Markdown")
    except:
        pass