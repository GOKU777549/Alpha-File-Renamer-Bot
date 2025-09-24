from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from Alpha import db
from config import ADMIN_ID
import asyncio


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_ID:
        return await update.message.reply_text("❌ You are not authorized to use this command!")

    if not context.args:
        return await update.message.reply_text(
            "⚠ Please provide a message to broadcast.\n\nUsage: `/broadcast Hello Users!`",
            parse_mode="Markdown"
        )

    msg = " ".join(context.args)
    users = db.get_all_users()

    sent, failed = 0, 0
    for user in users:   # db se list return hoti hai, isliye async for ki jagah normal loop
        try:
            await context.bot.send_message(user["user_id"], msg)
            sent += 1
            await asyncio.sleep(0.1)  # flood control
        except Exception:
            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast Completed!\n\n📨 Sent: `{sent}`\n⚠ Failed: `{failed}`",
        parse_mode="Markdown"
    )


def register(application):
    application.add_handler(CommandHandler("broadcast", broadcast))