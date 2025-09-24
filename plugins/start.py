import os
import time
import datetime
import humanize
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.file_id import FileId
from helper.database import insert, find_one

CHANNEL = os.environ.get("CHANNEL", "Alpha_X_Updates")
LIMIT = 240  # Flood control in seconds

def get_wish():
    current_time = datetime.datetime.now().hour
    if current_time < 12:
        return "Good morning"
    elif 12 <= current_time < 18:
        return "Good afternoon"
    else:
        return "Good evening"

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    insert(int(message.chat.id))  # Make sure insert handles duplicates
    wish = get_wish()
    
    await message.reply_text(
        f"Hello {wish} {message.from_user.first_name}!\n"
        "__I am a file renamer bot. Please send any Telegram__\n"
        "**Document, Video, or Audio** and then enter a new filename to rename it.",
        reply_to_message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Support 🇮🇳", url="https://t.me/Alpha_X_Waifu")],
            [InlineKeyboardButton("Subscribe 🧐", url="https://t.me/Alpha_X_Updates")]
        ])
    )

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    user_id = message.from_user.id

    # Channel subscription check
    if CHANNEL:
        try:
            await client.get_chat_member(CHANNEL, user_id)
        except UserNotParticipant:
            return await message.reply_text(
                "**__You are not subscribed to my channel__**",
                reply_to_message_id=message.message_id,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Support 🇮🇳", url=f"https://t.me/{CHANNEL}")]
                ])
            )

    # Flood control
    user_data = find_one(user_id)
    used_date = user_data.get("date", 0)
    now_time = time.time()
    wait_time = (used_date + LIMIT) - now_time
    if wait_time > 0:
        ltime = str(datetime.timedelta(seconds=round(wait_time)))
        await client.send_chat_action(message.chat.id, "typing")
        return await message.reply_text(
            f"```Sorry! Flood control is active. Please wait {ltime}```",
            reply_to_message_id=message.message_id
        )

    # Fetch media info
    media = await client.get_messages(message.chat.id, message.message_id)
    file = media.document or media.video or media.audio
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    dcid = FileId.decode(file.file_id).dc_id

    # Reply with options
    await message.reply_text(
        f"__What do you want me to do with this file?__\n"
        f"**File Name**: {filename}\n"
        f"**File Size**: {filesize}\n"
        f"**DC ID**: {dcid}",
        reply_to_message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📝 Rename", callback_data="rename"),
                InlineKeyboardButton("✖️ Cancel", callback_data="cancel")
            ]
        ])
    )