import math
import time
from datetime import datetime
from telegram import Message

async def progress_for_ptb(
    current: int,
    total: int,
    ud_type: str,
    message: Message,
    start_time: float = None,
    markdown: bool = True
):
    """
    Progress bar for python-telegram-bot uploads/downloads

    Parameters:
    - current: bytes transferred
    - total: total bytes
    - ud_type: string, "Uploading"/"Downloading"
    - message: telegram.Message object
    - start_time: timestamp when started (optional)
    - markdown: whether to use Markdown formatting
    """
    now = time.time()
    if start_time is None:
        # fallback: message.date.timestamp() might not be accurate, use now - 1s
        start_time = now - 1

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

    # Sizes in MB
    current_mb = round(current / 1024 / 1024, 2)
    total_mb = round(total / 1024 / 1024, 2)
    speed_mb = round(speed / 1024 / 1024, 2)

    text = f"*{ud_type}*\n" \
           f"Progress: {progress_str}\n" \
           f"{current_mb} MB / {total_mb} MB\n" \
           f"⚡ Speed: {speed_mb} MB/s\n" \
           f"⏳ ETA: {time.strftime('%H:%M:%S', time.gmtime(eta))}"

    try:
        await message.edit_text(text, parse_mode="Markdown")
    except Exception:
        # fallback without markdown
        try:
            await message.edit_text(text)
        except:
            pass