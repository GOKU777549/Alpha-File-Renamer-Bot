import math
import time
from datetime import datetime
from telegram import Message  # for type hinting

async def progress_for_pyrogram(
    current: int,
    total: int,
    ud_type: str,
    message: Message,
    total_size: int = None,
    start_time: float = None,
    markdown: bool = True
):
    """
    Universal progress function for file upload/download
    Works with Pyrogram & python-telegram-bot messages.
    
    Parameters:
    - current: bytes transferred
    - total: total bytes
    - ud_type: string, "Uploading"/"Downloading"
    - message: Message object
    - total_size: total size in bytes (optional, for better display)
    - start_time: timestamp when started (optional, defaults to message.date)
    - markdown: whether to use Markdown formatting
    """
    now = time.time()
    if start_time is None:
        start_time = message.date.timestamp()  # fallback

    diff = now - start_time
    if diff == 0:
        diff = 1

    percentage = current * 100 / total
    speed = current / diff
    eta = (total - current) / speed if speed != 0 else 0

    # Progress bar
    progress_str = "[{0}{1}] {2:.2f}%".format(
        "■" * int(percentage // 5),
        "□" * (20 - int(percentage // 5)),
        percentage
    )

    # Display sizes
    current_mb = round(current / 1024 / 1024, 2)
    total_mb = round(total_size / 1024 / 1024, 2) if total_size else round(total / 1024 / 1024, 2)
    speed_mb = round(speed / 1024 / 1024, 2)

    text = f"**{ud_type}**\n" \
           f"Progress: {progress_str}\n" \
           f"{current_mb} MB / {total_mb} MB\n" \
           f"⚡ Speed: {speed_mb} MB/s\n" \
           f"⏳ ETA: {time.strftime('%H:%M:%S', time.gmtime(eta))}"

    # Try editing the message
    try:
        if markdown:
            await message.edit_text(text, parse_mode="Markdown")
        else:
            await message.edit_text(text)
    except:
        pass