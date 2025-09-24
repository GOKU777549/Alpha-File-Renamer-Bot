from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler
from Alpha import db


START_TEXT = """
👋 Hi {},

I am a simple yet powerful **File Renamer Bot** ✨
I can:

📌 Rename Files  
📌 Save Custom Thumbnail  
📌 Save Custom Caption  

Use me in PM for smooth experience 🚀
"""

HELP_TEXT = """
**Available Commands 🛠**

/start - Show Welcome Message  
/help - Show This Message  
/view_thumb - View Your Thumbnail  
/del_thumb - Delete Your Thumbnail  
/set_caption - Save Custom Caption  
/view_caption - View Your Caption  
/del_caption - Delete Your Caption  

Just send me any file to start renaming process 🔥
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await db.add_user(user.id)

    buttons = [
        [InlineKeyboardButton("⚙ Help", callback_data="help")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/yourchannel")]
    ]

    await update.message.reply_text(
        START_TEXT.format(user.first_name),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode="Markdown"
    )


def register(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))