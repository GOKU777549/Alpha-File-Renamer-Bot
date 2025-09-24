from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from Alpha import db


# Save thumbnail when user sends a photo
async def save_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return
    photo = update.message.photo[-1].file_id  # best quality
    await db.save_thumb(update.effective_user.id, photo)
    await update.message.reply_text("Thumbnail Saved Successfully ✅")


# Delete thumbnail
async def delete_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await db.del_thumb(update.effective_user.id)
    await update.message.reply_text("Thumbnail Deleted Successfully 🗑️")


# View thumbnail
async def view_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thumb_id = await db.get_thumb(update.effective_user.id)
    if not thumb_id:
        await update.message.reply_text("You Don't Have Any Thumbnail ❌")
    else:
        await update.message.reply_photo(photo=thumb_id, caption="Your Thumbnail 📸")


def register(application: Application):
    application.add_handler(MessageHandler(filters.PHOTO, save_thumbnail))
    application.add_handler(CommandHandler("del_thumb", delete_thumbnail))
    application.add_handler(CommandHandler("view_thumb", view_thumbnail))