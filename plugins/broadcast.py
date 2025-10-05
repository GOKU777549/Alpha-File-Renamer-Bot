import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from bot import Client
from config import ADMIN_ID
from helper.database import getid


@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_(_, message: Message):
    """Broadcast a message to all users and groups, with automatic pinning in groups."""

    reply = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not reply and not text:
        return await message.reply_text("❖ Reply to a message or provide text to broadcast.")

    progress_msg = await message.reply_text("❖ Broadcasting message Please wait...")

    sent_groups, sent_users, failed, pinned = 0, 0, 0, 0

    # Fetch all chat IDs from MongoDB
    recipients = getid()

    for chat_id in recipients:
        try:
            if reply:
                msg = await reply.copy(chat_id)
            else:
                msg = await client.send_message(chat_id, text=text)

            if chat_id < 0:  # Group chat
                try:
                    await msg.pin(disable_notification=True)
                    pinned += 1
                except:
                    pass
                sent_groups += 1
            else:
                sent_users += 1

            await asyncio.sleep(0.2)  # Prevent rate limits

        except FloodWait as fw:
            await asyncio.sleep(fw.value + 1)
        except:
            failed += 1

    await progress_msg.edit_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"👥 **Groups Sent:** {sent_groups}\n"
        f"🧑‍💻 **Users Sent:** {sent_users}\n"
        f"📌 **Pinned in:** {pinned}\n"
        f"❌ **Failed:** {failed}"
    )