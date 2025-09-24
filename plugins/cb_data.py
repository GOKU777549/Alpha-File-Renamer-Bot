import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
from helper.progress import progress_for_pyrogram

DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

# Temporary in-memory storage to track pending renames
PENDING_RENAME = {}  # user_id -> file_message_id

# -------------------- Handle incoming files -------------------- #
@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def handle_file(client, message):
    file = message.document or message.audio or message.video
    filename = file.file_name
    filesize = humanbytes(file.file_size)
    dcid = getattr(file, "dc_id", "N/A")

    await message.reply_text(
        f"📥 **New File Received** 📥\n\n"
        f"**File Name**: {filename}\n"
        f"**File Size**: {filesize}\n"
        f"**DC ID**: {dcid}",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📝 Rename", callback_data="rename"),
                InlineKeyboardButton("✖️ Cancel", callback_data="cancel")
            ]
        ])
    )

    # Store original file message ID
    PENDING_RENAME[message.from_user.id] = message.id

# -------------------- Ask for new filename -------------------- #
@Client.on_callback_query(filters.regex("rename"))
async def ask_rename(client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_RENAME:
        return await query.answer("❌ No file found to rename.", show_alert=True)

    await query.message.delete()
    await query.message.reply_text(
        "✏️ Please Enter New Filename...\n\nOld File Name :- {}".format(
            (await client.get_messages(query.message.chat.id, PENDING_RENAME[user_id])).document.file_name
            if (await client.get_messages(query.message.chat.id, PENDING_RENAME[user_id])).document
            else "Unknown"
        ),
        reply_markup=ForceReply(True)
    )

# -------------------- Handle new filename -------------------- #
@Client.on_message(filters.private & filters.reply)
async def rename_file(client, message):
    user_id = message.from_user.id
    if user_id not in PENDING_RENAME:
        return

    new_name = message.text.strip()
    await message.delete()

    file_msg_id = PENDING_RENAME.pop(user_id)
    orig_msg = await client.get_messages(message.chat.id, file_msg_id)

    file = orig_msg.document or orig_msg.audio or orig_msg.video
    if not file:
        return await message.reply_text("❌ Original file not found.")

    old_name = file.file_name
    ext = os.path.splitext(old_name)[1]
    out_filename = new_name if "." in new_name else new_name + ext
    file_path = os.path.join(DOWNLOADS, out_filename)

    status = await message.reply_text("⏳ Trying To Downloading ...")
    start_time = time.time()
    downloaded_path = await client.download_media(
        file, file_path, progress=progress_for_pyrogram,
        progress_args=("📥 Downloading...", status, start_time)
    )

    thumb = find(user_id)
    ph_path = None
    if thumb:
        ph_path = await client.download_media(thumb)

    await status.edit("⏳ Trying To Uploading ...")
    try:
        if orig_msg.video:
            duration = 0
            try:
                metadata = extractMetadata(createParser(file_path))
                if metadata and metadata.has("duration"):
                    duration = metadata.get("duration").seconds
            except:
                duration = 0

            await client.send_video(
                message.chat.id, video=file_path, thumb=ph_path,
                duration=duration,
                caption=f"File Name :- {out_filename}",
                progress=progress_for_pyrogram, progress_args=("📤 Uploading...", status, start_time)
            )

        elif orig_msg.audio:
            await client.send_audio(
                message.chat.id, audio=file_path, thumb=ph_path,
                caption=f"File Name :- {out_filename}",
                progress=progress_for_pyrogram, progress_args=("📤 Uploading...", status, start_time)
            )
        else:
            await client.send_document(
                message.chat.id, document=file_path, thumb=ph_path,
                caption=f"File Name :- {out_filename}",
                progress=progress_for_pyrogram, progress_args=("📤 Uploading...", status, start_time)
            )

        await status.delete()
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)


# -------------------- Utility -------------------- #
def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size,2)} {Dic_powerN[n]}B"