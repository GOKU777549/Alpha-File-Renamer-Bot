import pymongo
import os

DB_NAME = os.environ.get("DB_NAME", "File-rename")
DB_URL = os.environ.get("DB_URL", "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot")

mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]

# -------------------- User collection -------------------- #
dbcol = db["user"]
caption_col = db["caption"]

def total_users():
    """Return total users count"""
    return dbcol.count_documents({})

def insert(chat_id):
    user_id = int(chat_id)
    user_det = {"_id": user_id, "file_id": None, "date": 0}
    try:
        dbcol.insert_one(user_det)
    except:
        return 'exists'

def addthumb(chat_id, file_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})

def delthumb(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})

def find(chat_id):
    data = dbcol.find_one({"_id": chat_id})
    if data:
        return data.get("file_id")
    return None

def getid():
    return [key["_id"] for key in dbcol.find()]

def find_one(chat_id):
    return dbcol.find_one({"_id": chat_id})


# -------------------- Caption collection -------------------- #

def save_caption(user_id, caption_text):
    """Save default caption for user"""
    caption_col.update_one(
        {"_id": user_id},
        {"$set": {"caption": caption_text}},
        upsert=True
    )

def get_caption(user_id):
    """Fetch default caption for user"""
    data = caption_col.find_one({"_id": user_id})
    if data and "caption" in data:
        return data["caption"]
    return None

def del_caption(user_id):
    """Delete default caption for user"""
    caption_col.update_one({"_id": user_id}, {"$unset": {"caption": ""}})