from pyrogram import Client
import os

TOKEN = os.environ.get("TOKEN", "8302777365:AAGoG2wE6fujqDyMe2oI8eC-wzfwtOIq1e8")

API_ID = int(os.environ.get("API_ID", "21218274"))

API_HASH = os.environ.get("API_HASH", "3474a18b61897c672d315fb330edb213")

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    app = Client(
        "renamer",
        bot_token=TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()