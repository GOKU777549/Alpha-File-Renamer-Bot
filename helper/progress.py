import math
import time

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 1.00) == 0 or current == total:  # update frequently
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time_ms = int(diff * 1000)
        remaining_time_ms = int((total - current) / speed * 1000 if speed else 0)
        eta_ms = elapsed_time_ms + remaining_time_ms

        elapsed_time = TimeFormatter(elapsed_time_ms)
        eta = TimeFormatter(remaining_time_ms)

        # Progress bar
        done_blocks = math.floor(percentage / 5)
        progress_bar = "Progress: [{}{}] {:.1f}%".format(
            "■" * done_blocks,
            "□" * (20 - done_blocks),
            percentage
        )

        text = (
            f"{progress_bar}\n"
            f"📥 {ud_type}: {humanbytes(current)} | {humanbytes(total)}\n"
            f"⚡️ Speed: {humanbytes(speed)}/s\n"
            f"⌛ ETA: {eta}\n"
            f"⏱️ Time elapsed: {elapsed_time}"
        )

        try:
            await message.edit(text=text)
        except:
            pass


def humanbytes(size):
    if not size:
        return "0B"
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
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