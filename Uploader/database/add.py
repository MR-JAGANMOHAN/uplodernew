from pyrogram import Client
from Uploader.database.database import db
from pyrogram.types import Message


async def AddUser(bot: Client, update: Message):
    if not await db.is_user_exist(update.from_user.id):
           await db.add_user(update.from_user.id)
