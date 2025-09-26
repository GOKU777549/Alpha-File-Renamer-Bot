import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find, get_caption
from helper.progress import progress_for_pyrogram

DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

# ---------------- In-memory storage ----------------
# user_id -> { orig_msg_id: { "reply_msg_id": ..., "new_name": ..., "final_name": ... } }
PENDING_TASKS = {}


# ------------------ Handle incoming files ----------------
@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def handle_file(client, message):
    user_id = message.from_user.id
    file = message.document or message.audio or message.video

    if user_id not in PENDING_TASKS:
        PENDING_TASKS[user_id] = {}

    PENDING_TASKS[user_id][message.id] = {}

    reply = await message.reply_text(
        f"✏️ Pʟᴇᴀsᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...\n\nOʟᴅ Fɪʟᴇɴᴀᴍᴇ :- {file.file_name}",
        reply_markup=ForceReply(True)
    )

    PENDING_TASKS[user_id][message.id]["reply_msg_id"] = reply.id


# ------------------ Handle new filename ----------------
@Client.on_message(filters.private & filters.reply)
async def rename_file(client, message):
    user_id = message.from_user.id
    if user_id not in PENDING_TASKS:
        return

    # Find which original file this reply belongs to
    orig_msg_id = None
    for msg_id, data in PENDING_TASKS[user_id].items():
        if "reply_msg_id" in data and data["reply_msg_id"] == message.reply_to_message.id:
            orig_msg_id = msg_id
            break

    if not orig_msg_id:
        return

    new_name = message.text.strip()
    await message.delete()

    try:
        await client.delete_messages(message.chat.id, PENDING_TASKS[user_id][orig_msg_id]["reply_msg_id"])
    except:
        pass

    orig_msg = await client.get_messages(message.chat.id, orig_msg_id)
    file = orig_msg.document or orig_msg.audio or orig_msg.video
    if not file:
        return await message.reply_text("❌ Original file not found.")

    old_name = file.file_name
    ext = os.path.splitext(old_name)[1]
    out_filename = new_name if "." in new_name else new_name + ext

    PENDING_TASKS[user_id][orig_msg_id]["new_name"] = new_name
    PENDING_TASKS[user_id][orig_msg_id]["final_name"] = out_filename

    await orig_msg.reply_text(
        f"Select The Output File Type\n\nFile Name :- {out_filename}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Dᴏᴄᴜᴍᴇɴᴛ", callback_data=f"as_document:{orig_msg_id}")],
            [InlineKeyboardButton("Vɪᴅᴇᴏ", callback_data=f"as_video:{orig_msg_id}")]
        ])
    )


# ------------------ Callback for output type ----------------
@Client.on_callback_query(filters.regex("as_"))
async def handle_output_type(client, query):
    user_id = query.from_user.id
    parts = query.data.split(":")
    action = parts[0]      # as_document / as_video
    orig_msg_id = int(parts[1]) if len(parts) > 1 else None

    if not orig_msg_id or user_id not in PENDING_TASKS or orig_msg_id not in PENDING_TASKS[user_id]:
        return await query.answer("❌ No file pending.", show_alert=True)

    orig_msg = await client.get_messages(query.message.chat.id, orig_msg_id)
    file = orig_msg.document or orig_msg.audio or orig_msg.video

    out_filename = PENDING_TASKS[user_id][orig_msg_id]["final_name"]
    file_path = os.path.join(DOWNLOADS, out_filename)

    await query.message.delete()

    # ---------------- Download ----------------
    status = await orig_msg.reply_text("Tʀʏɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ ...")
    start_time = time.time()

    downloaded_path = await client.download_media(
        file,
        file_path,
        progress=progress_for_pyrogram,
        progress_args=("Downloading", status, start_time)
    )

    # ---------------- Thumbnail ----------------
    thumb = find(user_id)
    ph_path = None
    if thumb:
        ph_path = await client.download_media(thumb)

    # ---------------- Upload ----------------
    await status.edit("Tʀʏɪɴɢ Tᴏ Uᴘʟᴏᴀᴅɪɴɢ ...")
    caption_text = get_caption(user_id) or f"File Name :- {out_filename}"

    try:
        if action == "as_video":
            duration = 0
            try:
                metadata = extractMetadata(createParser(file_path))
                if metadata and metadata.has("duration"):
                    duration = metadata.get("duration").seconds
            except:
                duration = 0

            await client.send_video(
                query.message.chat.id,
                video=file_path,
                thumb=ph_path,
                duration=duration,
                caption=caption_text,
                progress=progress_for_pyrogram,
                progress_args=("Uploading", status, start_time)
            )
        else:
            await client.send_document(
                query.message.chat.id,
                document=file_path,
                thumb=ph_path,
                caption=caption_text,
                progress=progress_for_pyrogram,
                progress_args=("Uploading", status, start_time)
            )

        await status.delete()
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)

    # Cleanup task
    del PENDING_TASKS[user_id][orig_msg_id]
    if not PENDING_TASKS[user_id]:
        del PENDING_TASKS[user_id]