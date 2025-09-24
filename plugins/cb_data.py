import os
import time
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
from helper.progress import progress_for_pyrogram

DOWNLOADS = "downloads"

if not os.path.exists(DOWNLOADS):
    os.makedirs(DOWNLOADS)

# ---------------- Rename callback ---------------- #
@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    """Ask user to input new filename"""
    await update.message.delete()
    await update.message.reply_text(
        "__Please enter the new filename in format 'Name:-newfilename'__",
        reply_markup=ForceReply(True)
    )

# ---------------- Document Handler ---------------- #
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):
    msg = update.message
    # Get the original file message (the one replied to in ForceReply)
    if not msg.reply_to_message or not msg.reply_to_message.reply_to_message:
        return await msg.edit("❌ Failed to get the original file message.")
    
    file_msg = msg.reply_to_message.reply_to_message
    new_name_text = msg.reply_to_message.text
    
    # Parse new filename
    try:
        new_filename = new_name_text.split(":-")[1]
    except IndexError:
        return await msg.edit("❌ Invalid format. Use 'Name:-newfilename'")
    
    # Prepare paths
    file_path = os.path.join(DOWNLOADS, new_filename)
    
    # Download original file
    ms = await msg.edit("```Trying to download...```")
    start_time = time.time()
    try:
        downloaded_path = await bot.download_media(
            file_msg, progress=progress_for_pyrogram,
            progress_args=("```Downloading...```", ms, start_time)
        )
    except Exception as e:
        return await ms.edit(f"❌ Download failed:\n{str(e)}")
    
    os.rename(downloaded_path, file_path)
    
    # Check for thumbnail
    user_id = msg.chat.id
    thumb = find(user_id)
    ph_path = None
    if thumb:
        ph_path = await bot.download_media(thumb)
        img = Image.open(ph_path).convert("RGB")
        img = img.resize((320, 320))
        img.save(ph_path, "JPEG")
    
    # Upload file
    await ms.edit("```Uploading...```")
    try:
        if ph_path:
            await bot.send_document(
                msg.chat.id, document=file_path, thumb=ph_path,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,
                progress_args=("```Uploading...```", ms, start_time)
            )
            os.remove(ph_path)
        else:
            await bot.send_document(
                msg.chat.id, document=file_path,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,
                progress_args=("```Uploading...```", ms, start_time)
            )
        await ms.delete()
        os.remove(file_path)
    except Exception as e:
        await ms.edit(f"❌ Upload failed:\n{str(e)}")
        os.remove(file_path)

# ---------------- Video Handler ---------------- #
@Client.on_callback_query(filters.regex("vid"))
async def vid(bot, update):
    msg = update.message
    if not msg.reply_to_message or not msg.reply_to_message.reply_to_message:
        return await msg.edit("❌ Failed to get the original file message.")

    file_msg = msg.reply_to_message.reply_to_message
    new_name_text = msg.reply_to_message.text
    try:
        new_filename = new_name_text.split(":-")[1]
    except IndexError:
        return await msg.edit("❌ Invalid format. Use 'Name:-newfilename'")

    file_path = os.path.join(DOWNLOADS, new_filename)
    ms = await msg.edit("```Trying to download...```")
    start_time = time.time()
    
    try:
        downloaded_path = await bot.download_media(
            file_msg, progress=progress_for_pyrogram,
            progress_args=("```Downloading...```", ms, start_time)
        )
    except Exception as e:
        return await ms.edit(f"❌ Download failed:\n{str(e)}")

    os.rename(downloaded_path, file_path)
    
    # Get duration
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get("duration").seconds
    
    # Check thumbnail
    user_id = msg.chat.id
    thumb = find(user_id)
    ph_path = None
    if thumb:
        ph_path = await bot.download_media(thumb)
        img = Image.open(ph_path).convert("RGB")
        img = img.resize((320, 320))
        img.save(ph_path, "JPEG")
    
    await ms.edit("```Uploading...```")
    try:
        if ph_path:
            await bot.send_video(
                msg.chat.id, video=file_path, thumb=ph_path, duration=duration,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,
                progress_args=("```Uploading...```", ms, start_time)
            )
            os.remove(ph_path)
        else:
            await bot.send_video(
                msg.chat.id, video=file_path, duration=duration,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,
                progress_args=("```Uploading...```", ms, start_time)
            )
        await ms.delete()
        os.remove(file_path)
    except Exception as e:
        await ms.edit(f"❌ Upload failed:\n{str(e)}")
        os.remove(file_path)

# ---------------- Audio Handler ---------------- #
@Client.on_callback_query(filters.regex("aud"))
async def aud(bot, update):
    msg = update.message
    if not msg.reply_to_message or not msg.reply_to_message.reply_to_message:
        return await msg.edit("❌ Failed to get the original file message.")

    file_msg = msg.reply_to_message.reply_to_message
    new_name_text = msg.reply_to_message.text
    try:
        new_filename = new_name_text.split(":-")[1]
    except IndexError:
        return await msg.edit("❌ Invalid format. Use 'Name:-newfilename'")

    file_path = os.path.join(DOWNLOADS, new_filename)
    ms = await msg.edit("```Trying to download...```")
    start_time = time.time()
    
    try:
        downloaded_path = await bot.download_media(
            file_msg, progress=progress_for_pyrogram,
            progress_args=("```Downloading...```", ms, start_time)
        )
    except Exception as e:
        return await ms.edit(f"❌ Download failed:\n{str(e)}")

    os.rename(downloaded_path, file_path)
    
    # Get duration
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get("duration").seconds
    
    # Check thumbnail
    user_id = msg.chat.id
    thumb = find(user_id)
    ph_path = None
    if thumb:
        ph_path = await bot.download_media(thumb)
        img = Image.open(ph_path).convert("RGB")
        img = img.resize((320, 320))
        img.save(ph_path, "JPEG")
    
    await ms.edit("```Uploading...```")
    try:
        if ph_path:
            await bot.send_audio(
                msg.chat.id, audio=file_path, thumb=ph_path, duration=duration,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,
                progress_args=("```Uploading...```", ms, start_time)
            )
            os.remove(ph_path)
        else:
            await bot.send_audio(
                msg.chat.id, audio=file_path, duration=duration,
                caption=f"**{new_filename}**",
                progress=progress_for_pyrogram,
                progress_args=("```Uploading...```", ms, start_time)
            )
        await ms.delete()
        os.remove(file_path)
    except Exception as e:
        await ms.edit(f"❌ Upload failed:\n{str(e)}")
        os.remove(file_path)