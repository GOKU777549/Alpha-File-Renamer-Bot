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
PENDING_RENAME = {}  # user_id -> original message id
PENDING_NEWNAME = {}  # user_id -> dict: {"reply_msg_id": ..., "new_name": ...}

# ------------------ Handle incoming files ----------------
@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def handle_file(client, message):
    file = message.document or message.audio or message.video
    PENDING_RENAME[message.from_user.id] = message.id

    reply = await message.reply_text(
        f"✏️ Pʟᴇᴀsᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...\n\nOʟᴅ Fɪʟᴇɴᴀᴍᴇ :- {file.file_name}",
        reply_markup=ForceReply(True)
    )

    # Store reply message id so we can delete later
    PENDING_NEWNAME[message.from_user.id] = {"reply_msg_id": reply.id}

# ------------------ Handle new filename ----------------
@Client.on_message(filters.private & filters.reply)
async def rename_file(client, message):
    user_id = message.from_user.id
    if user_id not in PENDING_RENAME or user_id not in PENDING_NEWNAME:
        return

    new_name = message.text.strip()
    await message.delete()  # delete user reply

    # delete bot's force reply message
    try:
        await client.delete_messages(message.chat.id, PENDING_NEWNAME[user_id]["reply_msg_id"])
    except:
        pass

    PENDING_NEWNAME[user_id]["new_name"] = new_name

    # Get original message
    orig_msg = await client.get_messages(message.chat.id, PENDING_RENAME[user_id])
    file = orig_msg.document or orig_msg.audio or orig_msg.video
    if not file:
        return await message.reply_text("❌ Original file not found.")

    old_name = file.file_name
    ext = os.path.splitext(old_name)[1]
    out_filename = new_name if "." in new_name else new_name + ext
    PENDING_NEWNAME[user_id]["final_name"] = out_filename

    # Ask output type
    await orig_msg.reply_text(
        f"Select The Output File Type\n\nFile Name :- {out_filename}",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Dᴏᴄᴜᴍᴇɴᴛ", callback_data="as_document"),
                InlineKeyboardButton("Vɪᴅᴇᴏ", callback_data="as_video")
            ]
        ])
    )

# ------------------ Callback for output type ----------------
@Client.on_callback_query(filters.regex("as_"))
async def handle_output_type(client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_RENAME or user_id not in PENDING_NEWNAME:
        return await query.answer("❌ No file pending.", show_alert=True)

    orig_msg = await client.get_messages(query.message.chat.id, PENDING_RENAME[user_id])
    file = orig_msg.document or orig_msg.audio or orig_msg.video

    out_filename = PENDING_NEWNAME.pop(user_id)["final_name"]
    file_path = os.path.join(DOWNLOADS, out_filename)

    # delete the type selection message
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
        if query.data == "as_video":
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