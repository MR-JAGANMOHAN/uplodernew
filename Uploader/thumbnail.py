# Copyright @Tellybots | @ShriMadhavUk | @PlanetBots

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import random
import numpy
import os
from PIL import Image
import time

# the Strings used for this "thing"
from Uploader.script import Translation
from pyrogram import Client
from Uploader.database.add import AddUser
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
from Uploader.functions.help_Nekmo_ffmpeg import take_screen_shot
import psutil
import shutil
import string
import asyncio
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from Uploader.functions.forcesub import handle_force_subscribe
from Uploader.database.database import db
from Uploader.config import Config
from Uploader.database.database import db
from Uploader.settings.settings import *

f = filters.command(["delthumb"])
s = filters.command("showthumb")

@Client.on_message(filters.photo)
async def save_photo(bot, update):
    await AddUser(bot, update)
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    # received single photo
    download_location = os.path.join(
        Config.DOWNLOAD_LOCATION,
        str(update.from_user.id) + ".jpg"
    )
    await bot.download_media(
        message=update,
        file_name=download_location
    )
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.id
    )
    await db.set_thumbnail(update.from_user.id, thumbnail=update.photo.file_id)


@Client.on_message(f)
async def delete_thumbnail(bot, update):

    await AddUser(bot, update)
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return

    download_location = os.path.join(
        Config.DOWNLOAD_LOCATION,
        str(update.from_user.id)
    )
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.id
    )
    await db.set_thumbnail(update.from_user.id, thumbnail=None)

@Client.on_message(s)
async def viewthumbnail(bot, update):

    await AddUser(bot, update)

    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return   
    thumbnail = await db.get_thumbnail(update.from_user.id)
    if thumbnail is not None:
        await bot.send_photo(
        chat_id=update.chat.id,
        photo=thumbnail,
        caption=f"ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ 🦠",
        reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="deleteThumbnail")]]
                ),
        reply_to_message_id=update.id)
    else:
        await update.reply_text(text=f"ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ғᴏᴜɴᴅ 🤒")


async def Gthumb01(bot, update):
    thumb_image_path = f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}.jpg"
    db_thumbnail = await db.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}.jpg"
    db_thumbnail = await db.get_thumbnail(update.from_user.id)
    return (
        await bot.download_media(
            message=db_thumbnail, file_name=thumb_image_path
        )
        if db_thumbnail is not None
        else await take_screen_shot(
            download_directory,
            os.path.dirname(download_directory),
            random.randint(0, duration - 1),
        )
    )

async def Mdata01(download_directory):

          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")

          return width, height, duration

async def Mdata02(download_directory):

          width = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")

          return width, duration

async def Mdata03(download_directory):

    metadata = extractMetadata(createParser(download_directory))
    return (
        metadata.get('duration').seconds
        if metadata is not None and metadata.has("duration")
        else 0
    )

