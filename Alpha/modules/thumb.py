from telegram import Update
from telegram.ext import ContextTypes
from Alpha import db  # your db.py

async def save_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return
    photo = update.message.photo[-1].file_id
    await db.save_thumb(update.effective_user.id, photo)
    await update.message.reply_text("Thumbnail Saved Successfully ✅")


async def delete_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await db.del_thumb(update.effective_user.id)
    await update.message.reply_text("Thumbnail Deleted Successfully 🗑️")


async def view_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thumb_id = await db.get_thumb(update.effective_user.id)
    if not thumb_id:
        await update.message.reply_text("You Don't Have Any Thumbnail ❌")
    else:
        await update.message.reply_photo(photo=thumb_id, caption="Your Thumbnail 📸")