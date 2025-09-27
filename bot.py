from pyrogram import Client
import os

# 🔹 Main Bot Config
TOKEN1 = os.environ.get("TOKEN1", "8302777365:AAGoG2wE6fujqDyMe2oI8eC-wzfwtOIq1e8")
API_ID = int(os.environ.get("API_ID", "21218274"))
API_HASH = os.environ.get("API_HASH", "3474a18b61897c672d315fb330edb213")

# 🔹 Second Bot Config (modules ke liye)
TOKEN2 = os.environ.get("TOKEN2", "1234567890:ABCDEF-your-second-token")

if __name__ == "__main__":
    # ✅ Main Bot (sirf plugins load karega)
    plugins = dict(root="plugins")
    app1 = Client(
        "renamer_bot",
        bot_token=TOKEN1,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )

    # ✅ Second Bot (sirf modules load karega)
    modules = dict(root="modules")
    app2 = Client(
        "modules_bot",
        bot_token=TOKEN2,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=modules
    )

    # Dono bots ko parallel run karne ke liye
    app1.start()
    app2.start()
    print("✅ Both bots started successfully!")
    app1.idle()
    app2.stop()
    app1.stop()