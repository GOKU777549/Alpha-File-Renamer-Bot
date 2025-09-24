import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    """Handle user input after ForceReply to rename files"""
    
    # Make sure the replied message had ForceReply
    reply_markup = getattr(message.reply_to_message, "reply_markup", None)
    if not reply_markup or not isinstance(reply_markup, ForceReply):
        return

    new_name = message.text
    await message.delete()

    # Get the original file message
    orig_msg = getattr(message.reply_to_message, "reply_to_message", None)
    if not orig_msg:
        return await message.reply_text("❌ Cannot find the original file message.")

    file = orig_msg.document or orig_msg.video or orig_msg.audio
    if not file:
        return await message.reply_text("❌ No valid file found in the replied message.")

    filename = getattr(file, "file_name", None)
    if not filename:
        return await message.reply_text("❌ The file has no filename.")

    mime = file.mime_type.split("/")[0] if file.mime_type else "file"

    # Safe filename extraction
    base, ext = os.path.splitext(filename)
    if not ext:
        return await message.reply_text("❌ Error: No file extension found. Cannot rename.")

    # Determine output filename
    out_filename = new_name if "." in new_name else new_name + ext

    # Prepare inline buttons
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

    # Delete the ForceReply message to keep chat clean
    await message.reply_to_message.delete()

    # Send selection message (safe with Pyrogram v2+)
    await message.reply_text(
        f"**Select the output file type**\n**Output FileName** :- ```{out_filename}```",
        reply_markup=markup
    )