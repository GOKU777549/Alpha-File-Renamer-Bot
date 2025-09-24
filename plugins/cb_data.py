from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
from PIL import Image
import os, time

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    await update.message.delete()
    await update.message.reply_text(
        "__Please enter the new filename...__",
        reply_to_message_id=update.message.reply_to_message.message_id,
        reply_markup=ForceReply(True)
    )

@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):
    # Get new filename from replied ForceReply message
    if not update.message.reply_to_message or not update.message.reply_to_message.text:
        return await update.message.edit("❌ Failed to get the new filename.")
    
    new_name = update.message.reply_to_message.text
    try:
        new_filename = new_name.split(":-")[1]
    except IndexError:
        return await update.message.edit("❌ Invalid format. Use 'Name:-newfilename'")
    
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message.reply_to_message  # original file message
    ms = await update.message.edit("```Trying to download...```")
    start_time = time.time()
    
    try:
        path = await bot.download_media(
            file, progress=progress_for_pyrogram, 
            progress_args=("```Trying to download...```", ms, start_time)
        )
    except Exception as e:
        return await ms.edit(f"❌ Download failed:\n{str(e)}")
    
    # Rename the file
    os.rename(path, file_path)
    
    # Get thumbnail if exists
    user_id = update.message.chat.id
    thumb = find(user_id)
    
    if thumb:
        ph_path = await bot.download_media(thumb)
        img = Image.open(ph_path).convert("RGB")
        img = img.resize((320, 320))
        img.save(ph_path, "JPEG")
    
    await ms.edit("```Uploading...```")
    
    try:
        if thumb:
            await bot.send_document(
                update.message.chat.id, document=file_path, thumb=ph_path,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram, progress_args=("```Uploading...```", ms, start_time)
            )
            os.remove(ph_path)
        else:
            await bot.send_document(
                update.message.chat.id, document=file_path,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram, progress_args=("```Uploading...```", ms, start_time)
            )
        await ms.delete()
        os.remove(file_path)
    except Exception as e:
        await ms.edit(f"❌ Upload failed:\n{str(e)}")
        os.remove(file_path)