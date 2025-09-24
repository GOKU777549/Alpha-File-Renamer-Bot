import os
import time
import math
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)
from Alpha import db

# States
ASK_FILENAME, ASK_TYPE = range(2)

# Step 1: Detect file
async def detect_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = message.document or message.video or message.audio
    if not file:
        await message.reply_text("❌ No valid file detected!")
        return ConversationHandler.END

    context.user_data["file"] = file
    await message.reply_text(
        f"Please Enter New Filename...\n\nOld File Name: `{file.file_name}`",
        parse_mode="Markdown"
    )
    return ASK_FILENAME

# Step 2: Ask new filename
async def ask_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_name = update.message.text
    context.user_data["new_name"] = new_name

    buttons = [
        [InlineKeyboardButton("📄 Document", callback_data="document"),
         InlineKeyboardButton("🎬 Video", callback_data="video")]
    ]
    await update.message.reply_text(
        f"Select output type for `{new_name}`",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return ASK_TYPE

# Progress updater
async def progress(current, total, message, start_time):
    now = time.time()
    diff = now - start_time
    if diff == 0:
        diff = 1
    percentage = current * 100 / total
    speed = current / diff
    eta = (total - current) / speed if speed != 0 else 0
    progress_str = "[" + "■" * int(percentage // 5) + "□" * (20 - int(percentage // 5)) + "]"
    text = f"Progress: {progress_str} {percentage:.2f}%\n" \
           f"{current/1024/1024:.2f}MB / {total/1024/1024:.2f}MB\n" \
           f"Speed: {speed/1024/1024:.2f}MB/s\n" \
           f"ETA: {time.strftime('%H:%M:%S', time.gmtime(eta))}"
    try:
        await message.edit_text(text)
    except:
        pass

# Step 3: Handle type & download/upload
async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    file = context.user_data["file"]
    new_name = context.user_data["new_name"]
    file_type = query.data

    msg = await query.edit_message_text("📥 Downloading...")

    # Ensure downloads folder
    os.makedirs("downloads", exist_ok=True)
    file_path = os.path.join("downloads", new_name)

    # Download file
    start_time = time.time()
    file_obj = await file.get_file()
    await file_obj.download_to_drive(custom_path=file_path)

    await msg.edit_text("📤 Uploading...")

    # Get caption & thumb
    caption = await db.get_caption(update.effective_user.id) or ""
    thumb_path = await db.get_thumb(update.effective_user.id)
    thumb_file = InputFile(thumb_path) if thumb_path and os.path.exists(thumb_path) else None

    # Send file
    if file_type == "document":
        await query.message.reply_document(
            document=InputFile(file_path),
            caption=caption,
            thumb=thumb_file
        )
    else:
        await query.message.reply_video(
            video=InputFile(file_path),
            caption=caption,
            thumb=thumb_file,
            supports_streaming=True
        )

    os.remove(file_path)
    return ConversationHandler.END

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Process Cancelled")
    return ConversationHandler.END

# Register
def register(application: Application):
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Document.ALL, detect_file),
            MessageHandler(filters.VIDEO, detect_file),
            MessageHandler(filters.AUDIO, detect_file)
        ],
        states={
            ASK_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_filename)],
            ASK_TYPE: [CallbackQueryHandler(ask_type)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    application.add_handler(conv)