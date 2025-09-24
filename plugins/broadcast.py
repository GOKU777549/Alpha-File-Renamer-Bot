import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from helper.database import getid

ADMIN = int(os.environ.get("ADMIN", 7576729648))

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command("broadcast"))
async def broadcast(bot, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Please reply to a message to broadcast it.")
    
    ms = await message.reply_text("Getting all IDs from database...")
    ids = getid()
    tot = len(ids)
    success = 0
    failed = 0

    await ms.edit(f"Starting Broadcast...\nSending message to {tot} users")

    for user_id in ids:
        try:
            await asyncio.sleep(1)  # non-blocking sleep
            await message.reply_to_message.copy(user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            success += 1
        except Exception:
            failed += 1
            continue
        
        # Update progress
        try:
            await ms.edit(
                f"Message sent to {success} chat(s). "
                f"{failed} chat(s) failed.\nTotal: {tot}"
            )
        except:
            pass