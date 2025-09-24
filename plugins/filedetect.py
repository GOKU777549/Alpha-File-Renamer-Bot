import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    # Check if the replied message had ForceReply
    reply_markup = message.reply_to_message.reply_markup
    if not reply_markup or not isinstance(reply_markup, ForceReply):
        return

    new_name = message.text
    await message.delete()

    media = await client.get_messages(message.chat.id, message.reply_to_message.message_id)
    file = media.reply_to_message.document or media.reply_to_message.video or media.reply_to_message.audio
    if not file:
        return await message.reply_text("❌ No valid file found in the replied message.")

    filename = file.file_name
    mime = file.mime_type.split("/")[0]
    mg_id = media.reply_to_message.message_id

    # Extract extension safely
    base, ext = os.path.splitext(filename)
    if not ext:
        return await message.reply_text(
            "**Error**: No file extension found. Cannot rename.", 
            reply_to_message_id=mg_id
        )

    # Create the output filename
    if "." in new_name:
        out_filename = new_name
    else:
        out_filename = new_name + ext

    # Prepare inline buttons based on file type
    if mime == "video":
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 Document", callback_data="doc"),
             InlineKeyboardButton("🎥 Video", callback_data="vid")]
        ])
    elif mime == "audio":
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 Document", callback_data="doc"),
             InlineKeyboardButton("🎵 Audio", callback_data="aud")]
        ])
    else:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 Document", callback_data="doc")]
        ])

    # Delete original ForceReply message
    await message.reply_to_message.delete()
    
    # Send selection message
    await message.reply_text(
        f"**Select the output file type**\n**Output FileName** :- ```{out_filename}```",
        reply_to_message_id=mg_id,
        reply_markup=markup
    )