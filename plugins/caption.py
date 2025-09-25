from pyrogram import Client, filters
from helper.database import save_caption, get_caption, del_caption

# -------------------- Set Caption -------------------- #
@Client.on_message(filters.private & filters.command("set_caption"))
async def set_caption_cmd(client, message):
    user_id = message.from_user.id
    text = message.text
    args = text.split(" ", 1)

    if len(args) == 1:
        return await message.reply_text(
            "Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ

Exᴀᴍᴩʟᴇ:- /set_caption {filename}

💾 Sɪᴢᴇ: {filesize}

⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}"
        )

    caption_text = args[1].strip()
    save_caption(user_id, caption_text)

    await message.reply_text(
        f"✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ"
    )


# -------------------- See Caption -------------------- #
@Client.on_message(filters.private & filters.command("see_caption"))
async def see_caption_cmd(client, message):
    user_id = message.from_user.id
    caption_text = get_caption(user_id)

    if not caption_text:
        return await message.reply_text("😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ")

    await message.reply_text(f"📝 Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-\n\n{caption_text}")


# -------------------- Delete Caption -------------------- #
@Client.on_message(filters.private & filters.command("del_caption"))
async def del_caption_cmd(client, message):
    user_id = message.from_user.id
    if get_caption(user_id):
        del_caption(user_id)
        return await message.reply_text("❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ")
    else:
        return await message.reply_text("😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ")


# -------------------- Helper for Renamer Bot -------------------- #
def get_caption_for_user(user_id, default=None):
    """
    Return user's default caption from DB
    If not found, return fallback default
    """
    caption = get_caption(user_id)
    if caption:
        return caption
    return default