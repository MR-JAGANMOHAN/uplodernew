


import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.types import Message 
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from Uploader.config import Config
from Uploader.script import Translation
from pyrogram import Client, filters
from Uploader.database.add import AddUser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Uploader.database.database import db
from Uploader.functions.forcesub import handle_force_subscribe
from Uploader.settings.settings import OpenSettings
from Uploader.config import *
from pyrogram import types, errors

@Client.on_message(
    filters.command("start") & filters.private,
)
async def start_bot(_, m: Message):
    await AddUser(_, m)
    return await m.reply_text(
        Translation.START_TEXT.format(m.from_user.first_name),
        reply_markup=Translation.START_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(
    filters.command("help") & filters.private,
)
async def help_bot(_, m: Message):
    await AddUser(_, m)

    return await m.reply_text(
        Translation.HELP_TEXT,
        reply_markup=Translation.HELP_BUTTONS,
        disable_web_page_preview=True,
    )

@Client.on_message(
    filters.command("about") & filters.private,
)
async def aboutme(_, m: Message):
    await AddUser(_, m)

    return await m.reply_text(
        Translation.ABOUT_TEXT,
        reply_markup=Translation.ABOUT_BUTTONS,
        disable_web_page_preview=True,
    )

@Client.on_message(
    filters.private & filters.reply & filters.text
)
async def edit_caption(bot, update):
    await AddUser(bot, update)

    try:
        await bot.send_cached_media(
            chat_id=update.chat.id,
            file_id=update.reply_to_message.video.file_id,
            reply_to_message_id=update.id,
            caption=update.text
        )
    except:
        try:
            await bot.send_cached_media(
                chat_id=update.chat.id,
                file_id=update.reply_to_message.document.file_id,
                reply_to_message_id=update.id,
                caption=update.text
            )
        except:
            pass


@Client.on_message(
    filters.private & filters.command(["caption"])
)

async def add_caption_help(bot, update):
    await AddUser(bot, update)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ADD_CAPTION_HELP,
        reply_markup=Translation.BUTTONS,
        reply_to_message_id=update.id
    )


@Client.on_message(
    filters.private & filters.command("me")
)
async def info_handler(bot, update):


    if update.from_user.last_name:
        last_name = update.from_user.last_name
    else:
        last_name = "None"

  
    await update.reply_text(  
        text=Translation.INFO_TEXT.format(update.from_user.first_name, last_name, update.from_user.username, update.from_user.id, update.from_user.mention, update.from_user.dc_id, update.from_user.language_code, update.from_user.status), 
        reply_markup=Translation.BUTTONS,           
        disable_web_page_preview=True
    )

@Client.on_message(
    filters.command("plans") & filters.private,
)
async def myplans(_, m: Message):
    await AddUser(_, m)

    return await m.reply_text(
        Translation.PLANS,
        reply_markup=Translation.BUTTONS,
        disable_web_page_preview=True,
    )
