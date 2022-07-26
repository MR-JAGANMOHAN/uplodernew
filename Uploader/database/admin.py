import shutil
import psutil
from pyrogram import filters
from pyrogram.types import (
    Message
)
from Uploader.config import Config
from pyrogram import Client, enums
from Uploader.database.database import db
from Uploader.functions.display_progress import humanbytes
from Uploader.database.bcast import broadcast_handler

f = filters.command("status") & filters.user(Config.OWNER_ID)

s = filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply

@Client.on_message(f)
async def edited(_, m: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Disk Space:** {total} \n"
             f"**Used Space:** {used}({disk_usage}%) \n"
             f"**Free Space:** {free} \n"
             f"**CPU Usage:** {cpu_usage}% \n"
             f"**RAM Usage:** {ram_usage}%\n\n"
             f"**Total Users in DB:** `{total_users}`",
        parse_mode=enums.ParseMode.MARKDOWN,
        quote=True
    )
    print("edited")

@Client.on_message(s)
async def edited(_, m: Message):
    await broadcast_handler(m)
    print("edited")
