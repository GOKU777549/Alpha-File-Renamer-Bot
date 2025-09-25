from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

# View custom thumbnail
@Client.on_message(filters.private & filters.command('viewthumb'))
async def viewthumb(client, message):
    thumb = find(int(message.chat.id))
    if thumb:
        await client.send_photo(message.chat.id, photo=thumb)
    else:
        await message.reply_text("😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ")

# Delete custom thumbnail
@Client.on_message(filters.private & filters.command('delthumb'))
async def removethumb(client, message):
    delthumb(int(message.chat.id))
    await message.reply_text("❌️ Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ")

# Add / update custom thumbnail
@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    if not message.photo:
        return await message.reply_text("❌ No photo found in the message.")
    
    file_id = message.photo.file_id
    addthumb(int(message.chat.id), file_id)
    await message.reply_text("✅️ Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ")