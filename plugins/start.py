import os
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import insert

CHANNEL = os.environ.get("CHANNEL", "Alpha_X_Updates")
BOT_IMAGE = "https://telegra.ph/file/1234567890abcdef12345.jpg"  # Yaha bot ka welcome image daal

def get_wish():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

# -------------------- /start handler --------------------
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    insert(int(message.chat.id))  # Save user in DB if not exists
    wish = get_wish()

    text = (
        f"ʜᴇʏ {user.mention}!✨\n\n"
        "🫧 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʀᴇɴᴀᴍᴇ ʙᴏᴛ!\n"
        "ᴡʜɪᴄʜ ᴄᴀɴ ᴍᴀɴᴜᴀʟʟʏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ғɪʟᴇs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴀɴᴅ ᴀʟsᴏ ᴄᴀɴ sᴇᴛ ᴘʀᴇғɪx ᴀɴᴅ sᴜғғɪx ᴏɴ ʏᴏᴜʀ ғɪʟᴇs.⚡️\n\n"
        f"✨ ᴛʜɪs ʙᴏᴛ ɪs ᴄʀᴇᴀᴛᴇᴅ ʙʏ ⏤͟͟͞͞𝗔𝗫𝗕 • ɴᴀʀυᴛo | ࿐{user.mention}\n"
        "──────────────────\n"
        "๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs."
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("HOW TO USE", callback_data="how_to_use")],
            [InlineKeyboardButton("UPDATE", url=f"https://t.me/{CHANNEL}"), 
             InlineKeyboardButton("SUPPORT", url="https://t.me/Alpha_X_Waifu")],
            [InlineKeyboardButton("ABOUT", callback_data="about"),
             InlineKeyboardButton("DONATE", callback_data="donate")]
        ]
    )

    await message.reply_photo(
        photo=BOT_IMAGE,
        caption=text,
        reply_markup=buttons
    )

# -------------------- Callback handler --------------------
@Client.on_callback_query()
async def cb_handler(client, query):
    user = query.from_user
    data = query.data

    if data == "how_to_use":
        text = (
            "ᴇᴅɢᴇ ʀᴇɴᴀᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs🫧\n\n"
            f"{user.bot.mention} ɪꜱ ᴀ ᴠᴇʀʏ ʜᴀɴᴅʏ ᴀɴᴅ ʜᴇʟᴘғᴜʟ ʙᴏᴛ  ᴛʜᴀᴛ ʜᴇʟᴘꜱ ʏᴏᴜ ʀᴇɴᴀᴍᴇ ᴀɴᴅ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ꜰɪʟᴇꜱ ᴇꜰꜰᴏʀᴛʟᴇꜱꜱʟʏ.\n\n"
            "ɪᴍᴘᴏʀᴛᴀɴᴛ ғᴇᴀᴛᴜʀᴇs:\n"
            "➲ ᴄᴀɴ ʀᴇɴᴀᴍᴇ ᴀɴʏ ғɪʟᴇs.\n"
            "➲ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ᴍᴇᴛᴀᴅᴀᴛᴀ.\n"
            "➲ ᴜᴘʟᴏᴀᴅ ɪɴ ᴅᴇsɪʀᴇ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.\n"
            "➲ ᴄᴀɴ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴘʀᴇғɪx & sᴜғғɪx.\n"
            "➲ ʀᴇɴᴀᴍᴇ ғɪʟᴇs ᴠᴇʀʏ ǫᴜɪᴄᴋʟʏ."
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="back")]])
        await query.message.edit_caption(text=text, reply_markup=buttons)

    elif data == "about":
        text = (
            "» ᴅᴇᴠᴇʟᴏᴩᴇʀ : ⏤͟͟͞͞𝗔𝗫𝗕 • ɴᴀʀυᴛo | ࿐\n"
            "» ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ\n"
            "» ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ\n"
            f"» ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ : {CHANNEL}\n"
            "» ᴍᴀɪɴ ɢʀᴏᴜᴘ : 𝗔𝗟𝗣𝗛𝗔 𝗕𝗢𝗧 [𝕊𝕌ℙℙ𝕆ℝ𝕋]"
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="back")]])
        await query.message.edit_caption(text=text, reply_markup=buttons)

    elif data == "donate":
        text = (
            f"👋 ʜᴇʏ ᴛʜᴇʀᴇ {user.mention},\n\n"
            "Jᴜsᴛ ᴡᴀɴᴛᴇᴅ ᴛᴏ ᴅʀᴏᴘ ᴀ ǫᴜɪᴄᴋ ᴛʜᴀɴᴋs ʏᴏᴜʀ ᴡᴀʏ! 🌟\n"
            "Nᴏ ɴᴇᴇᴅ ᴛᴏ sᴛʀᴇss ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴs – ʏᴏᴜʀ ʟɪᴛᴛʟᴇ sᴜᴘᴘᴏʀᴛ ᴀɴᴅ ᴄʟɪᴄᴋs ᴍᴇᴀɴ ᴛʜᴇ ᴡᴏʀʟᴅ ᴛᴏ ᴜs."
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("BACK", callback_data="back")]])
        await query.message.edit_caption(text=text, reply_markup=buttons)

    elif data == "back":
        # Go back to main start
        wish = get_wish()
        text = (
            f"ʜᴇʏ {user.mention}!✨\n\n"
            "🫧 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʀᴇɴᴀᴍᴇ ʙᴏᴛ!\n"
            "ᴡʜɪᴄʜ ᴄᴀɴ ᴍᴀɴᴜᴀʟʟʏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ғɪʟᴇs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴀɴᴅ ᴀʟsᴏ ᴄᴀɴ sᴇᴛ ᴘʀᴇғɪx ᴀɴᴅ sᴜғғɪx ᴏɴ ʏᴏᴜʀ ғɪʟᴇs.⚡️\n\n"
            f"✨ ᴛʜɪs ʙᴏᴛ ɪs ᴄʀᴇᴀᴛᴇᴅ ʙʏ ⏤͟͟͞͞𝗔𝗫𝗕 • ɴᴀʀυᴛo | ࿐{user.mention}\n"
            "──────────────────\n"
            "๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs."
        )
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("HOW TO USE", callback_data="how_to_use")],
                [InlineKeyboardButton("UPDATE", url=f"https://t.me/{CHANNEL}"),
                 InlineKeyboardButton("SUPPORT", url="https://t.me/Alpha_X_Waifu")],
                [InlineKeyboardButton("ABOUT", callback_data="about"),
                 InlineKeyboardButton("DONATE", callback_data="donate")]
            ]
        )
        await query.message.edit_caption(text=text, reply_markup=buttons)