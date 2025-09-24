from pyrogram import Client, filters

@Client.on_message(filters.private & filters.command("about"))
async def about(client, message):
    text = (
        "🤖 Bot: @rename_urbot\n"
        "👤 Creator: @mrlokaman\n"
        "💻 Language: Python 3\n"
        "📚 Library: Pyrogram 1.4.16\n"
        "🖥️ Server: Heroku"
    )
    await message.reply_text(text)