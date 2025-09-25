from pyrogram import Client, filters
from helper.database import save_caption, get_caption, del_caption

# -------------------- Set Caption -------------------- #
@Client.on_message(filters.private & filters.command("set_caption"))
async def set_caption_cmd(client, message):
    user_id = message.from_user.id
    args = message.text.split(" ", 1)

    if len(args) == 1:
        return await message.reply_text(
            "⚡️ Gɪᴠᴇ Tʜᴇ Cᴀᴘᴛɪᴏɴ\n\n"
            "Exᴀᴍᴩʟᴇ:\n"
            "`/set_caption {filename}\n\n💾 Size: {filesize}\n⏰ Duration: {duration}`",
            quote=True
        )

    caption_text = args[1].strip()
    save_caption(user_id, caption_text)

    await message.reply_text("✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ", quote=True)


# -------------------- See Caption -------------------- #
@Client.on_message(filters.private & filters.command("see_caption"))
async def see_caption_cmd(client, message):
    user_id = message.from_user.id
    caption_text = get_caption(user_id)

    if not caption_text:
        return await message.reply_text("😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ", quote=True)

    await message.reply_text(f"📝 Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ:\n\n{caption_text}", quote=True)


# -------------------- Delete Caption -------------------- #
@Client.on_message(filters.private & filters.command("del_caption"))
async def del_caption_cmd(client, message):
    user_id = message.from_user.id
    if get_caption(user_id):
        del_caption(user_id)
        return await message.reply_text("❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ", quote=True)
    else:
        return await message.reply_text("😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ", quote=True)


# -------------------- Helper for Renamer Bot -------------------- #
def get_caption_for_user(user_id: int, default: str = None) -> str:
    """
    Return user's saved caption from DB.
    If not found, return fallback default.
    """
    caption = get_caption(user_id)
    return caption if caption else default