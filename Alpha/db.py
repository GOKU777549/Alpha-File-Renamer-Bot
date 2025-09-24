import motor.motor_asyncio
from config import Config

client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URL)
db = client[Config.DB_NAME]

users_col = db["users"]
thumbs_col = db["thumbnails"]
captions_col = db["captions"]


# ---------------- USERS ---------------- #
async def add_user(user_id: int):
    """Add user to DB if not exists"""
    if not await users_col.find_one({"user_id": user_id}):
        await users_col.insert_one({"user_id": user_id})


async def get_all_users():
    """Return all users for broadcast"""
    return users_col.find()


# ---------------- THUMBNAILS ---------------- #
async def save_thumb(user_id: int, file_id: str):
    """Save or update user thumbnail"""
    await thumbs_col.update_one(
        {"user_id": user_id},
        {"$set": {"file_id": file_id}},
        upsert=True
    )


async def get_thumb(user_id: int):
    """Get user thumbnail"""
    doc = await thumbs_col.find_one({"user_id": user_id})
    return doc["file_id"] if doc else None


async def del_thumb(user_id: int):
    """Delete user thumbnail"""
    await thumbs_col.delete_one({"user_id": user_id})


# ---------------- CAPTIONS ---------------- #
async def save_caption(user_id: int, caption: str):
    """Save or update user caption"""
    await captions_col.update_one(
        {"user_id": user_id},
        {"$set": {"caption": caption}},
        upsert=True
    )


async def get_caption(user_id: int):
    """Get user caption"""
    doc = await captions_col.find_one({"user_id": user_id})
    return doc["caption"] if doc else None


async def del_caption(user_id: int):
    """Delete user caption"""
    await captions_col.delete_one({"user_id": user_id})