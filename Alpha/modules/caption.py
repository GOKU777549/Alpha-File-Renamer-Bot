from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from Alpha import db


async def set_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save user caption"""
    if not context.args:
        return await update.message.reply_text("⚠ Please provide a caption.\n\nUsage: `/set_caption Your Text Here`", parse_mode="Markdown")

    caption = " ".join(context.args)
    await db.save_caption(update.effective_user.id, caption)
    await update.message.reply_text("✅ Caption Saved Successfully!")


async def view_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View user caption"""
    caption = await db.get_caption(update.effective_user.id)
    if not caption:
        await update.message.reply_text("❌ You Don't Have Any Caption")
    else:
        await update.message.reply_text(f"📝 Your Caption:\n\n`{caption}`", parse_mode="Markdown")


async def del_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete user caption"""
    await db.del_caption(update.effective_user.id)
    await update.message.reply_text("🗑️ Caption Deleted Successfully!")


def register(application):
    application.add_handler(CommandHandler("set_caption", set_caption))
    application.add_handler(CommandHandler("view_caption", view_caption))
    application.add_handler(CommandHandler("del_caption", del_caption))