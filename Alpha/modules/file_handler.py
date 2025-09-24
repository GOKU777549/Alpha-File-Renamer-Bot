import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
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
from Alpha.utils.progress import progress_for_pyrogram

# States
ASK_FILENAME, ASK_TYPE = range(2)

# Step 1: Detect file and ask for new name
async def detect_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = None

    if message.document:
        file = message.document
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio

    if not file:
        return ConversationHandler.END

    context.user_data["file"] = file
    await message.reply_text(
        f"Please Enter New Filename...\n\nOld File Name :- `{file.file_name}`",
        parse_mode="Markdown"
    )
    return ASK_FILENAME

# Step 2: Get new filename
async def ask_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_name = update.message.text
    context.user_data["new_name"] = new_name

    buttons = [
        [InlineKeyboardButton("📄 Document", callback_data="document"),
         InlineKeyboardButton("🎬 Video", callback_data="video")]
    ]
    await update.message.reply_text(
        f"Select The Output File Type\n\nFile Name :- `{new_name}`",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return ASK_TYPE

# Step 3: Process file with type
async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file = context.user_data["file"]
    new_name = context.user_data["new_name"]
    file_type = query.data

    msg = await query.edit_message_text("Trying To Downloading....")

    os.makedirs("downloads", exist_ok=True)
    file_path = os.path.join("downloads", new_name)

    tfile = await file.get_file()
    await tfile.download_to_drive(
        custom_path=file_path,
        progress=progress_for_pyrogram,
        progress_args=("Downloading", msg, file.file_size)
    )

    caption = await db.get_caption(update.effective_user.id) or ""
    thumb = await db.get_thumb(update.effective_user.id)

    await msg.edit_text("Trying To Uploading....")

    if file_type == "document":
        await query.message.reply_document(
            document=open(file_path, "rb"),
            caption=caption,
            thumb=thumb
        )
    else:
        await query.message.reply_video(
            video=open(file_path, "rb"),
            caption=caption,
            thumb=thumb,
            supports_streaming=True
        )

    os.remove(file_path)
    return ConversationHandler.END

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Process Cancelled")
    return ConversationHandler.END

# Register handlers
def register(application: Application):
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Document.ALL, detect_file),
            MessageHandler(filters.VIDEO, detect_file),
            MessageHandler(filters.AUDIO, detect_file)
        ],
        states={
            ASK_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_filename)],
            ASK_TYPE: [CallbackQueryHandler(ask_type)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    application.add_handler(conv)