# Kanged From @TroJanZheX
import asyncio
import re
import ast
import math
import random
import os
lock = asyncio.Lock()
import pytz
from datetime import datetime, timedelta, date, time
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink, check_verification, get_token, stream_site, get_tutorial
from database.users_chats_db import db, get_referal_users_count
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
TIMEZONE = "Asia/Kolkata"
from database.gfilters_mdb import (
    find_gfilter,
    get_gfilters,
    del_allg
)
import logging
from urllib.parse import quote_plus
from SAFARI.utils.file_properties import get_name, get_hash, get_media_file_size

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
CAP = {}

@Client.on_callback_query(filters.regex(r"^streaming"))
async def stream_download(bot, query):
    file_id = query.data.split('#', 1)[1] 
    user_id = query.from_user.id
    username =  query.from_user.mention 
    msg = await bot.send_cached_media(
        chat_id=BIN_CHANNEL,
        file_id=file_id)
        
    online = f"{URL}watch/{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
    download = f"{URL}{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
    non_online = await stream_site(online)
    non_download = await stream_site(download)
    if not await db.has_premium_access(user_id) and STREAM_LINK_MODE == True:  
        await msg.reply_text(text=f"tg://openmessage?user_id={user_id}\n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} LINK MODE ON",
            reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=non_download),
                    InlineKeyboardButton("🖥️ ꜱᴛʀᴇᴇᴍ 🖥️", url=non_online)]]))
        await query.answer("𝐍𝐨𝐭𝐞:\n𝐓𝐡𝐞 𝐀𝐝𝐬-𝐅𝐫𝐞𝐞 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬 𝐎𝐧𝐥𝐲 𝐅𝐨𝐫 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐔𝐬𝐞𝐫𝐬\n\n‼️Tᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ, ᴄʜᴇᴀᴋ ʙᴇʟᴏᴡ..!!!", show_alert=True)
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=non_download),
                    InlineKeyboardButton("🖥️ ꜱᴛʀᴇᴇᴍ 🖥️", url=non_online)
                ],[
                    InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=STREAMHTO)]]))
    else:
        await msg.reply_text(text=f"tg://openmessage?user_id={user_id}\n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} SHORT MODE OFF",
            reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download),
                    InlineKeyboardButton("🖥️ ꜱᴛʀᴇᴇᴍ 🖥️", url=online)]]))
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download),
                    InlineKeyboardButton("🖥️ ꜱᴛʀᴇᴇᴍ 🖥️", url=online)
                ],[
                    InlineKeyboardButton('⁉️ ᴄʟᴏsᴇ ⁉️', callback_data='close_data')]]))
                        
@Client.on_message(filters.private & filters.command("stream"))
async def reply_stream(client, message):
    reply_message = message.reply_to_message
    user_id = message.from_user.id
    user_name =  message.from_user.mention 
    if not reply_message or not (reply_message.document or reply_message.video):
        return await message.reply_text("**Reply to a video or document file.**")

    file_id = reply_message.document or reply_message.video

    try:
        msg = await reply_message.forward(chat_id=BIN_CHANNEL)
        await client.send_message(text=f"<b>Streaming Link Gernated By </b>:{message.from_user.mention}  <code>{message.from_user.id}</code> 👁️✅",
                  chat_id=BIN_CHANNEL,
                  disable_web_page_preview=True)
    except Exception as e:
        return await message.reply_text(f"Error: {str(e)}")

    online = f"{URL}watch/{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
    download = f"{URL}{str(msg.id)}/{quote_plus(get_name(msg))}?hash={get_hash(msg)}"
    non_online = await stream_site(online)
    non_download = await stream_site(download)

    file_name = file_id.file_name.replace("_", " ").replace(".mp4", "").replace(".mkv", "").replace(".", " ")
    if not await db.has_premium_access(user_id) and STREAM_LINK_MODE == True:  
        await message.reply_text(
            text=f"<b>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <a href={CHNL_LNK}>{file_name}</a>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ : {non_download}\n\n🖥WATCH  : {non_online}\n\n⚠️ Tʜᴇ ʟɪɴᴋ ᴡɪʟʟ ɴᴏᴛ ᴇxᴘɪʀᴇ ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ'ꜱ ꜱᴇʀᴠᴇʀ ɪꜱ ᴄʜᴀɴɢᴇᴅ. 🔋\n\n𝐍𝐨𝐭𝐞:\n𝐓𝐡𝐞 𝐀𝐝𝐬-𝐅𝐫𝐞𝐞 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬 𝐎𝐧𝐥𝐲 𝐅𝐨𝐫 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐔𝐬𝐞𝐫𝐬\n\n‼️Tᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ, ᴄʜᴇᴀᴋ ʙᴇʟᴏᴡ..!!!</b>",
            reply_markup=InlineKeyboardMarkup(
                [[
                  InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=non_download),
                  InlineKeyboardButton("🖥️ ꜱᴛʀᴇᴇᴍ 🖥️", url=non_online)
                  ],[
                  InlineKeyboardButton('🔒 Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ 🔒', url=STREAMHTO)
                ],[
                 InlineKeyboardButton('✨ ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅꜱ ✨', callback_data="seeplans")
                ]]),
                disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=f"<b>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <a href={CHNL_LNK}>{file_name}</a>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ : {download}\n\n🖥WATCH  : {online}\n\n⚠️ Tʜᴇ ʟɪɴᴋ ᴡɪʟʟ ɴᴏᴛ ᴇxᴘɪʀᴇ ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ'ꜱ ꜱᴇʀᴠᴇʀ ɪꜱ ᴄʜᴀɴɢᴇᴅ. 🔋</b>",
            reply_markup=InlineKeyboardMarkup(
                [[
                  InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download),
                  InlineKeyboardButton("🖥️ ꜱᴛʀᴇᴇᴍ 🖥️", url=online)
                ]]),
                disable_web_page_preview=True
        )

@Client.on_message(filters.group & filters.text & filters.incoming)
async def force_sub(client, message):
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        btn = [[
                InlineKeyboardButton("❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆", url=invite_link.invite_link)
              ]]
        await message.reply(
            text="**Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ᴏᴜʀ Bᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ sᴏ ʏᴏᴜ ᴅᴏɴ'ᴛ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇ...\n\nIғ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴀɴᴅ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '↻ Tʀʏ Aɢᴀɪɴ' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ...\n\nTʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇs...**",
            reply_markup=InlineKeyboardMarkup(btn),
        )
        return
    else:
        await auto_filter(client, message)


@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    if message.chat.id != SUPPORT_CHAT_ID:
        manual = await manual_filters(client, message)
        if manual == False:
            settings = await get_settings(message.chat.id)
            try:
                if settings['auto_ffilter']:
                    await auto_filter(client, message)
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_ffilter', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_ffilter']:
                    await auto_filter(client, message) 
    else: #a better logic to avoid repeated lines of code in auto_filter function
        search = message.text
        temp_files, temp_offset, total_results = await get_search_results(chat_id=message.chat.id, query=search.lower(), offset=0, filter=True)
        if total_results == 0:
            return
        else:
            return await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ ✅\n\n📂 ꜰɪʟᴇꜱ ꜰᴏᴜɴᴅ : {str(total_results)}\n🔍 ꜱᴇᴀʀᴄʜ :</b> <code>{search}</code>\n\n<b>‼️ ᴛʜɪs ɪs ᴀ <u>sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</u> sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\n📝 ꜱᴇᴀʀᴄʜ ʜᴇʀᴇ : 👇</b>",   
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔍 ᴊᴏɪɴ ᴀɴᴅ ꜱᴇᴀʀᴄʜ ʜᴇʀᴇ 🔎", url=f"https://t.me/Finding_Movies")]]))

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    if PM_FILTER == True:  
        await auto_filter(bot, message) 
    else:
        content = message.text
    user = message.from_user.mention
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    if user_id in ADMINS: return # ignore admins
    await message.reply_text(
         text=f"<b>ʜᴇʏ {user} 😍 ,\n\nʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ᴍᴏᴠɪᴇs ꜰʀᴏᴍ ʜᴇʀᴇ. ʀᴇǫᴜᴇsᴛ ɪᴛ ɪɴ ᴏᴜʀ ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ @Mix_Cinema_Box 👇</b>",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 ʀᴇǫᴜᴇsᴛ ʜᴇʀᴇ ", url=f"https://t.me/Finding_Movies")]])
    )
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#𝐏𝐌_𝐌𝐒𝐆\n\nNᴀᴍᴇ : {user}\n\nID : {user_id}\n\nMᴇssᴀɢᴇ : {content}</b>"
    )
    

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
#    if not search:
#        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
#        return

    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    temp.SHORT[query.from_user.id] = query.message.chat.id
    temp.GETALL[key] = files
    files_link = ''
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(query=search, title=imdb['title'], votes=imdb['votes'], seasons=imdb["seasons"], imdb_id=imdb["imdb_id"], cast=imdb["cast"], runtime=imdb["runtime"], countries=imdb["countries"], certificates=imdb["certificates"], languages=imdb["languages"], director=imdb["director"], release_date=imdb['release_date'], year=imdb['year'], genres=imdb['genres'], poster=imdb['poster'], plot=imdb['plot'], rating=imdb['rating'], url=imdb['url'])
    else:
        cap = f"<b> I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {search}.</b>"
    if settings['button']:
        btn = []
        for file in files:
            files_link += f"""<b>\n\n❤️ <a href=https://t.me/{temp.U_NAME}?start=files_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Linkz') and not x.startswith('boxoffice') and not x.startswith('{') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}</a></b>"""
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('boxoffice') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    try:
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                        InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    except KeyError:
        await save_group_settings(query.message.chat.id, 'max_btn', True)
        if 0 < offset <= 10:
            off_set = 0
        elif offset == 0:
            off_set = None
        else:
            off_set = offset - 10
        if n_offset == 0:
            btn.append(
                [InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
            )
        elif off_set is None:
            btn.append([InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")])
        else:
            btn.append(
                [
                    InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"),
                    InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                    InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")
                ],
            )
    btn.insert(0, [
        InlineKeyboardButton("Lᴀɴɢᴜᴀɢᴇ", callback_data=f"select_lang#{req}"),
        InlineKeyboardButton("Qᴜᴀʟɪᴛʏꜱ", callback_data=f"lusi_films#{req}"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴꜱ", callback_data=f"jk_dev#{req}")
    ])
    btn.insert(0, [
        InlineKeyboardButton("", callback_data=f""),  
    ])
    try:
        await query.message.edit_text(text=cap + files_link, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^lang"))
async def language_check(bot, query):
    _, userid, language = query.data.split("#")
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if language == "unknown":
        return await query.answer("Sᴇʟᴇᴄᴛ ᴀɴʏ ʟᴀɴɢᴜᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs !", show_alert=True)
    movie = temp.KEYWORD.get(query.from_user.id)
    cap = CAP.get(movie)
#    if not movie:
#        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if language != "home":
        movie = f"{movie} {language}"
    files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
    if files:
        key = f"{query.message.chat.id}-{query.message.id}"
        settings = await get_settings(query.message.chat.id)
        temp.SHORT[query.from_user.id] = query.message.chat.id
        temp.GETALL[key] = files
        files_link = ''
        pre = 'filep' if settings['file_secure'] else 'file'
        if settings['button']:
            btn = []
            for file in files:
                files_link += f"""<b>\n\n❤️ <a href=https://t.me/{temp.U_NAME}?start=files_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('boxoffice') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}</a></b>"""
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('@') and not x.startswith('boxoffice') and not x.startswith('www'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                    ),
                ]
                for file in files
            ]
        btn.insert(0, [
            InlineKeyboardButton("! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !", callback_data=f"select_lang#{userid}"),
            InlineKeyboardButton("Qᴜᴀʟɪᴛʏꜱ", callback_data=f"lusi_films#{userid}"),
            InlineKeyboardButton("Sᴇᴀꜱᴏɴꜱ", callback_data=f"jk_dev#{userid}")
        ])

        btn.insert(0, [
            InlineKeyboardButton("", callback_data=f"")
        ])

        if offset != "":
            key = f"{query.message.chat.id}-{query.message.id}"
            BUTTONS[key] = movie
            CAP[key] = movie
            req = userid
            try:
                if settings['max_btn']:
                    btn.append(
                        [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                    )

                else:
                    btn.append(
                        [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                    )
            except KeyError:
                await save_group_settings(query.message.chat.id, 'max_btn', True)
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )
        else:
            btn.append(
                [InlineKeyboardButton(text="𝐍𝐎 𝐌𝐎𝐑𝐄 𝐏𝐀𝐆𝐄𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄",callback_data="pages")]
            )
        try:
            await query.message.edit_text(text=cap + files_link, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
        await query.answer()
    else:
        return await query.answer(f"Sᴏʀʀʏ, Nᴏ ғɪʟᴇs ғᴏᴜɴᴅ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {movie}.", show_alert=True)
    
@Client.on_callback_query(filters.regex(r"^select_lang"))
async def select_language(bot, query):
    _, userid = query.data.split("#")
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    btn = [[
        InlineKeyboardButton("Sᴇʟᴇᴄᴛ Yᴏᴜʀ Dᴇꜱɪʀᴇᴅ Lᴀɴɢᴜᴀɢᴇ ↓", callback_data=f"lang#{userid}#unknown")
    ],[
        InlineKeyboardButton("Eɴɢʟɪꜱʜ", callback_data=f"lang#{userid}#eng"),
        InlineKeyboardButton("Tᴀᴍɪʟ", callback_data=f"lang#{userid}#tam"),
        InlineKeyboardButton("Hɪɴᴅɪ", callback_data=f"lang#{userid}#hin")
    ],[
        InlineKeyboardButton("Kᴀɴɴᴀᴅᴀ", callback_data=f"lang#{userid}#kan"),
        InlineKeyboardButton("Tᴇʟᴜɢᴜ", callback_data=f"lang#{userid}#tel")
    ],[
        InlineKeyboardButton("Mᴀʟᴀʏᴀʟᴀᴍ", callback_data=f"lang#{userid}#mal")
    ],[
        InlineKeyboardButton("Gᴜᴊᴀʀᴀᴛɪ", callback_data=f"lang#{userid}#guj"),
        InlineKeyboardButton("Mᴀʀᴀᴛʜɪ", callback_data=f"lang#{userid}#mar"),
        InlineKeyboardButton("Pᴜɴᴊᴀʙɪ", callback_data=f"lang#{userid}#pun")
    ],[
        InlineKeyboardButton("Mᴜʟᴛɪ Aᴜᴅɪᴏ", callback_data=f"lang#{userid}#multi"),
        InlineKeyboardButton("Dᴜᴀʟ Aᴜᴅɪᴏ", callback_data=f"lang#{userid}#dual")
    ],[
        InlineKeyboardButton("Gᴏ Bᴀᴄᴋ", callback_data=f"lang#{userid}#home")
    ]]
    try:
       await query.edit_message_reply_markup(
           reply_markup=InlineKeyboardMarkup(btn)
       )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^lusifilms"))
async def quality_check(bot, query):
    _, userid, quality = query.data.split("#")
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if quality == "unknown":
        return await query.answer("Sᴇʟᴇᴄᴛ ᴀɴʏ Qᴜᴀʟɪᴛʏꜱ ғʀᴏᴍ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs !", show_alert=True)
    movie = temp.KEYWORD.get(query.from_user.id)
    cap = CAP.get(movie)
#    if not movie:
#        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if quality != "home":
        movie = f"{movie} {quality}"
    files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
    if files:
        key = f"{query.message.chat.id}-{query.message.id}"
        settings = await get_settings(query.message.chat.id)
        temp.SHORT[query.from_user.id] = query.message.chat.id
        temp.GETALL[key] = files
        files_link = ''
        pre = 'filep' if settings['file_secure'] else 'file'
        if settings['button']:
            btn = []
            for file in files:
                files_link += f"""<b>\n\n❤️ <a href=https://t.me/{temp.U_NAME}?start=files_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('boxoffice') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}</a></b>"""
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('boxoffice') and not x.startswith('@') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('www'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                    ),
                ]
                for file in files
            ]
        btn.insert(0, [
            InlineKeyboardButton("Lᴀɴɢᴜᴀɢᴇ", callback_data=f"select_lang#{userid}"),
            InlineKeyboardButton("Sᴇʟᴇᴄᴛ Aɢᴀɪɴ", callback_data=f"lusi_films#{userid}"),
            InlineKeyboardButton("Sᴇᴀꜱᴏɴꜱ", callback_data=f"jk_dev#{userid}")
        ])

        btn.insert(0, [
            InlineKeyboardButton("", callback_data=f"")
        ])

        if offset != "":
            key = f"{query.message.chat.id}-{query.message.id}"
            BUTTONS[key] = movie
            CAP[key] = movie
            req = userid
            try:
                if settings['max_btn']:
                    btn.append(
                        [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                    )

                else:
                    btn.append(
                        [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                    )
            except KeyError:
                await save_group_settings(query.message.chat.id, 'max_btn', True)
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )
        else:
            btn.append(
                [InlineKeyboardButton(text="𝐍𝐎 𝐌𝐎𝐑𝐄 𝐏𝐀𝐆𝐄𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄",callback_data="pages")]
            )
        try:
            await query.message.edit_text(text=cap + files_link, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
        await query.answer()
    else:
        return await query.answer(f"Sᴏʀʀʏ, Nᴏ ғɪʟᴇs ғᴏᴜɴᴅ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {movie}.", show_alert=True)

@Client.on_callback_query(filters.regex(r"^lusi_films"))
async def select_quality(bot, query):
    _, userid = query.data.split("#")
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    btn = [[
        InlineKeyboardButton("Sᴇʟᴇᴄᴛ Yᴏᴜʀ Dᴇꜱɪʀᴇᴅ Qᴜᴀʟɪᴛʏꜱ ↓", callback_data=f"lusifilms#{userid}#unknown")
    ],[
        InlineKeyboardButton("480p", callback_data=f"lusifilms#{userid}#480p"),
        InlineKeyboardButton("720p", callback_data=f"lusifilms#{userid}#720p")
    ],[
        InlineKeyboardButton("1080p", callback_data=f"lusifilms#{userid}#1080p"),
        InlineKeyboardButton("1080p HQ", callback_data=f"lusifilms#{userid}#1080p HQ")
    ],[
        InlineKeyboardButton("1440p", callback_data=f"lusifilms#{userid}#1440p"),
        InlineKeyboardButton("2160p", callback_data=f"lusifilms#{userid}#2160p")
    ],[
        InlineKeyboardButton("Gᴏ Bᴀᴄᴋ", callback_data=f"lusifilms#{userid}#home")
    ]]
    try:
       await query.edit_message_reply_markup(
           reply_markup=InlineKeyboardMarkup(btn)
       )
    except MessageNotModified:
        pass
    await query.answer()
    
@Client.on_callback_query(filters.regex(r"^seasons"))
async def seasons_check(bot, query):
    _, userid, seasons = query.data.split("#")
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if seasons == "unknown":
        return await query.answer("Sᴇʟᴇᴄᴛ ᴀɴʏ Sᴇᴀꜱᴏɴꜱ ғʀᴏᴍ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs !", show_alert=True)
    movie = temp.KEYWORD.get(query.from_user.id)
    cap = CAP.get(movie)
#    if not movie:
#        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if seasons != "home":
        movie = f"{movie} {seasons}"
    files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
    if files:
        key = f"{query.message.chat.id}-{query.message.id}"
        settings = await get_settings(query.message.chat.id)
        temp.SHORT[query.from_user.id] = query.message.chat.id
        temp.GETALL[key] = files
        files_link = ''
        pre = 'filep' if settings['file_secure'] else 'file'
        if settings['button']:
            btn = []
            for file in files:
                files_link += f"""<b>\n\n❤️ <a href=https://t.me/{temp.U_NAME}?start=files_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('boxoffice') and not x.startswith('Linkz') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}</a></b>"""
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('boxoffice') and not x.startswith('@') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('www'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                    ),
                ]
                for file in files
            ]
        btn.insert(0, [
            InlineKeyboardButton("Lᴀɴɢᴜᴀɢᴇ", callback_data=f"select_lang#{userid}"),
            InlineKeyboardButton("Qᴜᴀʟɪᴛʏꜱ", callback_data=f"lusi_films#{userid}"),
            InlineKeyboardButton("Sᴇʟᴇᴄᴛ Aɢᴀɪɴ", callback_data=f"jk_dev#{userid}")
        ])

        btn.insert(0, [
            InlineKeyboardButton("", callback_data=f"")
        ])

        if offset != "":
            key = f"{query.message.chat.id}-{query.message.id}"
            BUTTONS[key] = movie
            CAP[key] = movie
            req = userid
            try:
                if settings['max_btn']:
                    btn.append(
                        [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                    )

                else:
                    btn.append(
                        [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                    )
            except KeyError:
                await save_group_settings(query.message.chat.id, 'max_btn', True)
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )
        else:
            btn.append(
                [InlineKeyboardButton(text="𝐍𝐎 𝐌𝐎𝐑𝐄 𝐏𝐀𝐆𝐄𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄",callback_data="pages")]
            )
        try:
            await query.message.edit_text(text=cap + files_link, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
        await query.answer()
    else:
        return await query.answer(f"Sᴏʀʀʏ, Nᴏ ғɪʟᴇs ғᴏᴜɴᴅ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {movie}.", show_alert=True)

@Client.on_callback_query(filters.regex(r"^jk_dev"))
async def select_seasons(bot, query):
    _, userid = query.data.split("#")
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    btn = [[
        InlineKeyboardButton("Sᴇʟᴇᴄᴛ Yᴏᴜʀ Dᴇꜱɪʀᴇᴅ Sᴇᴀꜱᴏɴꜱ ↓", callback_data=f"seasons#{userid}#unknown")
    ],[
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟷", callback_data=f"seasons#{userid}#s01"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟸", callback_data=f"seasons#{userid}#s02")
    ],[
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟹", callback_data=f"seasons#{userid}#s03"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟺", callback_data=f"seasons#{userid}#s04")
    ],[
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟻", callback_data=f"seasons#{userid}#s05"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟼", callback_data=f"seasons#{userid}#s06")
    ],[
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟽", callback_data=f"seasons#{userid}#s07"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟾", callback_data=f"seasons#{userid}#s08")
    ],[
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟿", callback_data=f"seasons#{userid}#s09"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴ 𝟷𝟶", callback_data=f"seasons#{userid}#s10")
    ],[
        InlineKeyboardButton("Gᴏ Bᴀᴄᴋ", callback_data=f"seasons#{userid}#home")
    ]]
    try:
       await query.edit_message_reply_markup(
           reply_markup=InlineKeyboardMarkup(btn)
       )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return #await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movie = movies[(int(movie_))]
    movie = re.sub(r"[:\-]", " ", movie)
    movie = re.sub(r"\s+", " ", movie).strip()
    await query.answer(script.TOP_ALRT_MSG)
    gl = await global_filters(bot, query.message, text=movie)
    if gl == False:
        k = await manual_filters(bot, query.message, text=movie)
        if k == False:
            files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
            if files:
                k = (movie, files, offset, total_results)
                await auto_filter(bot, query, k)
            else:
                reqstr1 = query.from_user.id if query.from_user else 0
                reqstr = await bot.get_users(reqstr1)
                if NO_RESULTS_MSG:
                    safari = [[
                        InlineKeyboardButton('Not Release 📅', callback_data=f"not_release:{reqstr1}:{movie}"),
                    ],[
                        InlineKeyboardButton('Already Available🕵️', callback_data=f"already_available:{reqstr1}:{movie}"),
                        InlineKeyboardButton('Not Available🙅', callback_data=f"not_available:{reqstr1}:{movie}")
                    ],[
                        InlineKeyboardButton('Uploaded Done✅', callback_data=f"uploaded:{reqstr1}:{movie}")
                    ],[
                        InlineKeyboardButton('Series Error🙅', callback_data=f"series:{reqstr1}:{movie}"),
                        InlineKeyboardButton('Spell Error✍️', callback_data=f"spelling_error:{reqstr1}:{movie}")
                    ],[
                        InlineKeyboardButton('⁉️ Close ⁉️', callback_data=f"close_data")
                    ]]
                    reply_markup = InlineKeyboardMarkup(safari)
                    total=await bot.get_chat_members_count(query.message.chat.id)
                    await bot.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(query.message.chat.title, query.message.chat.id, total, temp.B_NAME, reqstr.mention, movie)), reply_markup=InlineKeyboardMarkup(safari))
                k = await query.message.edit(script.MVE_NT_FND)
                await asyncio.sleep(60)
                await k.delete()

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "gfiltersdeleteallconfirm":
        await del_allg(query.message, 'gfilters')
        await query.answer("Dᴏɴᴇ !")
        return
    elif query.data == "gfiltersdeleteallcancel": 
        await query.message.reply_to_message.delete()
        await query.message.delete()
        await query.answer("Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ !")
        return
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Mᴀᴋᴇ sᴜʀᴇ I'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ!!", quote=True)
                    return await query.answer(MSG_ALRT)
            else:
                await query.message.edit_text(
                    "I'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs!\nCʜᴇᴄᴋ /connections ᴏʀ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs",
                    quote=True
                )
                return await query.answer(MSG_ALRT)

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer(MSG_ALRT)

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ Gʀᴏᴜᴘ Oᴡɴᴇʀ ᴏʀ ᴀɴ Aᴜᴛʜ Usᴇʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Tʜᴀᴛ's ɴᴏᴛ ғᴏʀ ʏᴏᴜ!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Gʀᴏᴜᴘ Nᴀᴍᴇ : **{title}**\nGʀᴏᴜᴘ ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer(MSG_ALRT)
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Cᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer(MSG_ALRT)
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ !"
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "Tʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ ᴛᴏ sᴏᴍᴇ ɢʀᴏᴜᴘs ғɪʀsᴛ.",
            )
            return await query.answer(MSG_ALRT)
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Yᴏᴜʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ ᴅᴇᴛᴀɪʟs ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "gfilteralert" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_gfilter('gfilters', keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
            
            
    if query.data.startswith("file"):
        clicked = query.from_user.id
        try:
            typed = query.message.reply_to_message.from_user.id
        except:
            typed = query.from_user.id
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), files.file_name.split()))},"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            elif settings['botpm'] and settings['is_shortlink'] and not await db.has_premium_access(query.from_user.id):
                if clicked == typed:
                    temp.SHORT[clicked] = query.message.chat.id
                    await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=short_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            elif settings['is_shortlink'] and not settings['botpm'] and not await db.has_premium_access(query.from_user.id):
                if clicked == typed:
                    temp.SHORT[clicked] = query.message.chat.id
                    await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=short_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            elif settings['botpm']:
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            else:
                if clicked == typed:
                    if IS_VERIFY and not await check_verification(client, query.from_user.id) and not await db.has_premium_access(query.from_user.id):
                        btn = [[
                            InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, query.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
                            InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                            ],[
                            InlineKeyboardButton("💸 𝐑𝐞𝐦𝐨𝐯𝐞 𝐕𝐞𝐫𝐢𝐟𝐲 💸", callback_data='seeplans')
                        ]]
                        await client.send_message(
                            chat_id=query.from_user.id,
                            text=(script.VERIFY_TEXT),
                            protect_content=True if ident == 'checksubp' else False,
                            disable_web_page_preview=True,
                            parse_mode=enums.ParseMode.HTML,
                            reply_markup=InlineKeyboardMarkup(btn)
                        )
                        return await query.answer("Hᴇʏ, Yᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴅᴀʏ. Yᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ. Cʜᴇᴄᴋ ᴍʏ PM ᴛᴏ ᴠᴇʀɪғʏ ᴀɴᴅ ɢᴇᴛ ғɪʟᴇs !", show_alert=True)
                    else:
                        await client.send_cached_media(
                            chat_id=query.from_user.id,
                            file_id=file_id,
                            caption=f_caption,
                            protect_content=True if ident == "filep" else False,
                            reply_markup=InlineKeyboardMarkup(
                                [
                                [
                                InlineKeyboardButton("🖥️ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ 📥", callback_data=f"streaming#{file_id}")
                            ],[
                                InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                                InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                                ]
                                ]
                            )
                        )
                        return await query.answer('Cʜᴇᴄᴋ PM, I ʜᴀᴠᴇ sᴇɴᴛ ғɪʟᴇs ɪɴ PM', show_alert=True)
                else:
                    return await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
        except UserIsBlocked:
            await query.answer('Uɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴍᴀʜɴ !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
            
            
    elif query.data.startswith("sendfiles"):
        clicked = query.from_user.id
        ident, key = query.data.split("#")
        settings = await get_settings(query.message.chat.id)
        try:
            if settings['botpm'] and settings['is_shortlink']:
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles1_{key}")
                return
            elif settings['is_shortlink'] and not settings['botpm'] and not await db.has_premium_access(query.from_user.id):
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles2_{key}")
                return
            else:
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=allfiles_{key}")
                return
        except UserIsBlocked:
            await query.answer('Uɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴍᴀʜɴ !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles3_{key}")
        except Exception as e:
            logger.exception(e)
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles4_{key}")
            
            
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("Jᴏɪɴ ᴏᴜʀ Bᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ ᴍᴀʜɴ! 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        if IS_VERIFY and not await check_verification(client, query.from_user.id) and not await db.has_premium_access(query.from_user.id):
            btn = [[
                InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, query.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
                InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                ],[
                InlineKeyboardButton("💸 𝐑𝐞𝐦𝐨𝐯𝐞 𝐕𝐞𝐫𝐢𝐟𝐲 💸", callback_data='seeplans')
            ]]
            await client.send_message(
                chat_id=query.from_user.id,
                text=(script.VERIFY_TEXT),
                protect_content=True if ident == 'checksubp' else False,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            return
        else:
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_id,
                caption=f_caption,
                protect_content=True if ident == 'checksubp' else False,
                reply_markup=InlineKeyboardMarkup(
                [
                 [
                  InlineKeyboardButton("🖥️ Wᴀᴛᴄʜ & Dᴏᴡɴʟᴏᴀᴅ 📥", callback_data=f"streaming#{file_id}")
               ],[
                  InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                  InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                 ]
                ]
            ))
    elif query.data == "pages":
        await query.answer()

    elif query.data.startswith("killfilesdq"):
        ident, keyword = query.data.split("#")
        await query.message.edit_text(f"<b>Fᴇᴛᴄʜɪɴɢ Fɪʟᴇs ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword} ᴏɴ DB... Pʟᴇᴀsᴇ ᴡᴀɪᴛ...</b>")
        files, total = await get_bad_files(keyword)
        await query.message.edit_text(f"<b>Fᴏᴜɴᴅ {total} Fɪʟᴇs ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword} !\n\nFɪʟᴇ ᴅᴇʟᴇᴛɪᴏɴ ᴘʀᴏᴄᴇss ᴡɪʟʟ sᴛᴀʀᴛ ɪɴ 5 sᴇᴄᴏɴᴅs!</b>")
        await asyncio.sleep(5)
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if result.deleted_count:
                        logger.info(f'Fɪʟᴇ Fᴏᴜɴᴅ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword}! Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {file_name} ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>Pʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ ғᴏʀ ᴅᴇʟᴇᴛɪɴɢ ғɪʟᴇs ғʀᴏᴍ DB. Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {str(deleted)} ғɪʟᴇs ғʀᴏᴍ DB ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword} !\n\nPʟᴇᴀsᴇ ᴡᴀɪᴛ...</b>")
            except Exception as e:
                logger.exception(e)
                await query.message.edit_text(f'Eʀʀᴏʀ: {e}')
            else:
                await query.message.edit_text(f"<b>Pʀᴏᴄᴇss Cᴏᴍᴘʟᴇᴛᴇᴅ ғᴏʀ ғɪʟᴇ ᴅᴇʟᴇᴛɪᴏɴ !\n\nSᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {str(deleted)} ғɪʟᴇs ғʀᴏᴍ DB ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword}.</b>")

    elif query.data.startswith("opnsetgrp"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Tʜᴇ Rɪɢʜᴛs Tᴏ Dᴏ Tʜɪs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Rᴇꜱᴜʟᴛ Pᴀɢᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Tᴇxᴛ' if settings["button"] else 'Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('SʜᴏʀᴛLɪɴᴋ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["is_shortlink"] else '✘ Oғғ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_reply_markup(reply_markup)
        
    elif query.data.startswith("opnsetpm"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Tʜᴇ Rɪɢʜᴛs Tᴏ Dᴏ Tʜɪs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        btn2 = [[
                 InlineKeyboardButton("Cʜᴇᴄᴋ PM", url=f"t.me/{temp.U_NAME}")
               ]]
        reply_markup = InlineKeyboardMarkup(btn2)
        await query.message.edit_text(f"<b>Yᴏᴜʀ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ ғᴏʀ {title} ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ PM</b>")
        await query.message.edit_reply_markup(reply_markup)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Rᴇꜱᴜʟᴛ Pᴀɢᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Tᴇxᴛ' if settings["button"] else 'Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('SʜᴏʀᴛLɪɴᴋ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["is_shortlink"] else '✘ Oғғ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await client.send_message(
                chat_id=userid,
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=query.message.id
            )
    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton('☆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ☆', url=f'http://telegram.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('💸 ᴇᴀʀɴ ᴍᴏɴᴇʏ 💸', callback_data="shortlink_info"),
                    InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇꜱ •', callback_data='channels')
                ],[
                    InlineKeyboardButton('• ᴄᴏᴍᴍᴀɴᴅꜱ •', callback_data='help'),
                    InlineKeyboardButton('• ᴀʙᴏᴜᴛ •', callback_data='about'), 
                 ]]
        if IS_VERIFY or IS_SHORTLINK is True:
            buttons.append([
                InlineKeyboardButton('ʀᴇғғᴇʀ 💖', callback_data='subscription')
            ])
            buttons.append([
                InlineKeyboardButton('✨ ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅꜱ ✨', callback_data="premium_info")
            ]) 
        reply_markup = InlineKeyboardMarkup(buttons)
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 👋" 
        elif curr_time < 17:
            gtxt = "ɢᴏᴏᴅ ᴀғᴛᴇʀɴᴏᴏɴ 👋" 
        elif curr_time < 21:
            gtxt = "ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ 👋"
        else:
            gtxt = "ɢᴏᴏᴅ ɴɪɢʜᴛ 👋"
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)
        
    elif query.data == "show_reff":
        user_id = query.from_user.id
        total_referrals = await get_referal_users_count(user_id)
        await query.answer(text=f'You Have: {total_referrals} Refferal Points', show_alert=True)
        
    elif query.data == "subscription":
        user_id = query.from_user.id
        total_referrals = await get_referal_users_count(user_id)
        buttons = [[
            InlineKeyboardButton('Invite 🔗', url=f'https://telegram.me/share/url?url=https://t.me/{temp.U_NAME}?start=reff-{user_id}&text=E1%B4%84%CA%9F%C9%AA%E1%B4%84%E1%B4%8B%20%E1%B4%8F%C9%B4%20%E1%B4%9B%CA%9C%E1%B4%87%20%CA%9F%C9%AA%C9%B4%E1%B4%8B%20%E1%B4%80%C9%B4%E1%B4%85%20%E1%B4%87%C9%B4%E1%B4%8A%E1%B4%8F%CA%8F%20%C9%B4%E1%B4%87%E1%B4%A1%20%E1%B4%80%C9%B4%E1%B4%85%20%E1%B4%9B%CA%80%E1%B4%87%C9%B4%E1%B4%85%C9%AA%C9%B4%C9%A2%20%E1%B4%8D%E1%B4%8F%E1%B4%A0%C9%AA%E1%B4%87s/s%E1%B4%87%CA%80%C9%AA%E1%B4%87s'), 
            InlineKeyboardButton(text=f'⏳{total_referrals}', callback_data=f"show_reff"), 
            InlineKeyboardButton('⇚Back', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.SUBSCRIPTION_TXT.format(temp.U_NAME, query.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data.startswith("not_available"):
        _, user_id, movie = data.split(":")
        try:
            safari = [[
                    InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                    ]]
            reply_markup = InlineKeyboardMarkup(safari)
            await client.send_message(int(user_id), f"माफ़ करें आपने जो <b>{movie}</b> नाम की फिल्म मांगी थीं वो हमे नहीं मिली 😟ं, हो सकता है आगे चल कर मिल जाएं")
            msg=await query.edit_message_text(text=f"Mᴇꜱꜱᴀɢᴇ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n⏳ꜱᴛᴀᴛᴜꜱ : Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ 😒.\n🪪ᴜꜱᴇʀɪᴅ : `{user_id}`\n🎞ᴄᴏɴᴛᴇɴᴛ : `{movie}`", reply_markup=InlineKeyboardMarkup(safari))
            await asyncio.sleep(10)
            await msg.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return
    elif data.startswith("already_available"):
        _, user_id, movie = data.split(":")
        try:
            safari = [[
                    InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                    ]]
            reply_markup = InlineKeyboardMarkup(safari)
            await client.send_message(int(user_id), f"आपने जो <b>{movie}</b> फिल्म मांगी थी वो पहले से ही ग्रुप में अवेलबल हैं\n\n📌 कृपया नाम सही से लिखें |\सिर्फ फिल्म का नाम और वर्ष लिखें उसके आगे आगे कुछ ना लिखें\n\nजैसे  👉 <code>Shaitaan 2024</code>\n\nसीरीज फॉर्मेट 👉 <code>Money Heist S01E01</code> | <code>S01 E01</code>\n\nग्रुप 👉 <a href={GRP_LNK}>Rᴇǫ Gʀᴏᴜᴘ</a>")
            msg=await query.edit_message_text(text=f"Mᴇꜱꜱᴀɢᴇ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n⏳ꜱᴛᴀᴛᴜꜱ : Already Aᴠᴀɪʟᴀʙʟᴇ 🤩.\n🪪ᴜꜱᴇʀɪᴅ : `{user_id}`\n🎞ᴄᴏɴᴛᴇɴᴛ : `{movie}`", reply_markup=InlineKeyboardMarkup(safari))
            await asyncio.sleep(10)
            await msg.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return
    elif data.startswith("uploaded"):
        _, user_id, movie = data.split(":")
        try:
            safari = [[
                    InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                    ]]
            reply_markup = InlineKeyboardMarkup(safari)
            await client.send_message(int(user_id), f"आपने जो <b><code>{movie}</code></b> फिल्म मांगी थी वो अपलोड कर दी गईं हैं\n\nअब आपको ग्रुप में फिल्म मिल जायेगी 👉 <a href={GRP_LNK}>Rᴇǫ Gʀᴏᴜᴘ</a>")
            msg=await query.edit_message_text(text=f"Mᴇꜱꜱᴀɢᴇ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n⏳ꜱᴛᴀᴛᴜꜱ : Uᴘʟᴏᴀᴅᴇᴅ 🎊.\n🪪ᴜꜱᴇʀɪᴅ : `{user_id}`\n🎞ᴄᴏɴᴛᴇɴᴛ : `{movie}`", reply_markup=InlineKeyboardMarkup(safari))
            await asyncio.sleep(10)
            await msg.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return
    elif data.startswith("not_release"):
        _, user_id, movie = data.split(":")
        try:
            safari = [[
                    InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                    ]]
            reply_markup = InlineKeyboardMarkup(safari)
            await client.send_message(int(user_id), f"आपने जो <b>{movie}</b> फिल्म मांगी है वो अभी 📅 रिलीज नही हुई हैं\nजिस दिन फिल्म रिलीज होगी उस दिन, साम तक मिल जायेगी\n\n📌 कृपया रिलीज डेट 📅 से पहले ना मांगें")
            msg=await query.edit_message_text(text=f"Mᴇꜱꜱᴀɢᴇ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n⏳ꜱᴛᴀᴛᴜꜱ : Not Release 🙅.\n🪪ᴜꜱᴇʀɪᴅ : `{user_id}`\n🎞ᴄᴏɴᴛᴇɴᴛ : `{movie}`", reply_markup=InlineKeyboardMarkup(safari))
            await asyncio.sleep(10)
            await msg.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return
    elif data.startswith("spelling_error"):
        _, user_id, movie = data.split(":")
        try:
            safari = [[
                    InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                    ]]
            reply_markup = InlineKeyboardMarkup(safari)
            await client.send_message(int(user_id), f"<b>{movie}</b> ये नाम गलत है\nआपको सिर्फ मूवी/सीरीज का नाम और वर्ष लिखना है\n\nकुछ इस इस तरह से 👉 Sʜᴀɪᴛᴀᴀɴ 𝟸𝟶𝟸𝟺\n\nसीरीज फॉर्मेट 👉 Mᴏɴᴇʏ Hᴇɪꜱᴛ ꜱ𝟶𝟺ᴇ𝟶𝟷 | ꜱ𝟶𝟺 ᴇ𝟶𝟷\n\nग्रुप 👉 <a href={GRP_LNK}>Rᴇǫ Gʀᴏᴜᴘ</a>")
            msg=await query.edit_message_text(text=f"Mᴇꜱꜱᴀɢᴇ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n⏳ꜱᴛᴀᴛᴜꜱ : Sᴘᴇʟʟɪɴɢ Eʀʀᴏʀ 🕵️.\n🪪ᴜꜱᴇʀɪᴅ : `{user_id}`\n🎞ᴄᴏɴᴛᴇɴᴛ : `{movie}`", reply_markup=InlineKeyboardMarkup(safari))
            await asyncio.sleep(10)
            await msg.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return
    elif data.startswith("series"):
        _, user_id, movie = data.split(":")
        try:
            safari = [[
                    InlineKeyboardButton(text=f"🗑 Delete Log ❌", callback_data = "close_data")
                    ]]
            reply_markup = InlineKeyboardMarkup(safari)
            await client.send_message(int(user_id), f"आपने सीरीज का नाम गलत तरीके से लिखीं हैं\n{movie}\n\nआपको सीरीज का नाम इस तरह से नहीं लिखनी है\n\nआपको सीरीज का नाम इस तरह से लिखनी है\n<code>Money Heist S01E03</code> 👈\n<code>Money Heist S01 E03</code> 👈\n\nग्रुप 👉 <a href={GRP_LNK}>Rᴇǫ Gʀᴏᴜᴘ</a>")
            msg=await query.edit_message_text(text=f"Mᴇꜱꜱᴀɢᴇ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n⏳ꜱᴛᴀᴛᴜꜱ : Series Eʀʀᴏʀ 🕵️.\n🪪ᴜꜱᴇʀɪᴅ : `{user_id}`\n🎞ᴄᴏɴᴛᴇɴᴛ : `{movie}`", reply_markup=InlineKeyboardMarkup(safari))
            await asyncio.sleep(10)
            await msg.delete()
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return
    elif query.data == "purchase":
        buttons = [[
            InlineKeyboardButton('💵 ᴘᴀʏ ᴠɪᴀ ᴜᴘɪ ɪᴅ 💵', callback_data='upi_info')
        ],[
            InlineKeyboardButton('📸 ꜱᴄᴀɴ ǫʀ ᴄᴏᴅᴇ 📸', callback_data='qr_info')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PURCHASE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "upi_info":
        buttons = [[
            InlineKeyboardButton('📲 ꜱᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʜᴇʀᴇ', url=f"https://t.me/Monster_cave")
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='purchase')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.UPI_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "qr_info":
        buttons = [[
            InlineKeyboardButton('📲 ꜱᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʜᴇʀᴇ', url=f"https://t.me/Monster_cave")
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='purchase')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(CODE)
            )
        await query.message.edit_text(
            text=script.QR_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )       
    
    elif query.data == "seeplans":
        if await db.has_premium_access(query.from_user.id):
            await query.answer("ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀ ᴘʟᴀɴ ғʀɪᴇɴᴅ 🙂\n\nᴡᴀɪᴛ ғᴏʀ ʏᴏᴜʀ  ᴘʟᴀɴ ᴛᴏ ᴇɴᴅ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ʙᴜʏ ᴀ ɴᴇᴡ ᴘʟᴀɴ", show_alert=True)      
            return 
        else:
            buttons = [[
                InlineKeyboardButton('• ꜰʀᴇᴇ ᴛʀɪᴀʟ •', callback_data='free')
            ],[
                InlineKeyboardButton('• ʙʀᴏɴᴢᴇ •', callback_data='broze'),
                InlineKeyboardButton('• ꜱɪʟᴠᴇʀ •', callback_data='silver')
            ],[
                InlineKeyboardButton('• ɢᴏʟᴅ •', callback_data='gold'),
                InlineKeyboardButton('• ᴘʟᴀᴛɪɴᴜᴍ •', callback_data='platinum')
            ],[
                InlineKeyboardButton('• ᴅɪᴀᴍᴏɴᴅ •', callback_data='diamond'),
                InlineKeyboardButton('• ᴏᴛʜᴇʀ •', callback_data='other')
            ],[
                InlineKeyboardButton('❌ ᴄʟᴏꜱᴇ ❌', callback_data='close_data')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.reply_photo(
                photo=(SUBSCRIPTION),
                caption=script.PREPLANS_TXT.format(query.from_user.mention),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
 
    elif query.data == "give_trial":
        user_id = query.from_user.id
        has_free_trial = await db.check_trial_status(user_id)
        if await db.has_premium_access(query.from_user.id):
            await query.answer("ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀ ᴘʟᴀɴ ғʀɪᴇɴᴅ 🙂", show_alert=True)      
            return
        elif has_free_trial:
            await query.answer("🚸 ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ᴏɴᴄᴇ !\n\n📌 ᴄʜᴇᴄᴋᴏᴜᴛ ᴏᴜʀ ᴘʟᴀɴꜱ ʙʏ : /plans", show_alert=True) 
            return
        else:            
            await db.give_free_trial(user_id)
            await query.message.reply_text(
                text="<b>🥳 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ\n\n🎉 ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ꜰʀᴇᴇ ᴛʀᴀɪʟ ꜰᴏʀ <u>5 ᴍɪɴᴜᴛᴇs</u> ꜰʀᴏᴍ ɴᴏᴡ !</b>",
                quote=False,
                disable_web_page_preview=True,                  
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", callback_data='seeplans')]]))
            return    

    elif query.data == "premium_info":
        if await db.has_premium_access(query.from_user.id):
            await query.answer("ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀ ᴘʟᴀɴ ғʀɪᴇɴᴅ 🙂\n\nᴡᴀɪᴛ ғᴏʀ ʏᴏᴜʀ  ᴘʟᴀɴ ᴛᴏ ᴇɴᴅ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ʙᴜʏ ᴀ ɴᴇᴡ ᴘʟᴀɴ", show_alert=True)      
            return 
        else:
            buttons = [[
                InlineKeyboardButton('• ꜰʀᴇᴇ ᴛʀɪᴀʟ •', callback_data='free')
            ],[
                InlineKeyboardButton('• ʙʀᴏɴᴢᴇ •', callback_data='broze'),
                InlineKeyboardButton('• ꜱɪʟᴠᴇʀ •', callback_data='silver')
            ],[
                InlineKeyboardButton('• ɢᴏʟᴅ •', callback_data='gold'),
                InlineKeyboardButton('• ᴘʟᴀᴛɪɴᴜᴍ •', callback_data='platinum')
            ],[
                InlineKeyboardButton('• ᴅɪᴀᴍᴏɴᴅ •', callback_data='diamond'),
                InlineKeyboardButton('• ᴏᴛʜᴇʀ •', callback_data='other')
            ],[            
                InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(SUBSCRIPTION)
            )
            await query.message.edit_text(
                text=script.PLAN_TXT.format(query.from_user.mention),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "free":
        buttons = [[
            InlineKeyboardButton('⚜️ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ꜰʀᴇᴇ ᴛʀɪᴀʟ', callback_data="give_trial")
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='other'),
            InlineKeyboardButton('1 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='broze')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FREE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "broze":
        buttons = [[
            InlineKeyboardButton('🔐 ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='free'),
            InlineKeyboardButton('2 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='silver')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BRONZE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "silver":
        buttons = [[
            InlineKeyboardButton('🔐 ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='broze'),
            InlineKeyboardButton('3 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='gold')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SILVER_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "gold":
        buttons = [[
            InlineKeyboardButton('🔐 ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='silver'),
            InlineKeyboardButton('4 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='platinum')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GOLD_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "platinum":
        buttons = [[
            InlineKeyboardButton('🔐 ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='gold'),
            InlineKeyboardButton('5 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='diamond')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PLATINUM_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    
    elif query.data == "diamond":
        buttons = [[
            InlineKeyboardButton('🔐 ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='platinum'),
            InlineKeyboardButton('6 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='other')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DIAMOND_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "other":
        buttons = [[
            InlineKeyboardButton('☎️ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ', url=f"https://t.me/Monster_cave")
        ],[
            InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='diamond'),
            InlineKeyboardButton('7 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('ɴᴇxᴛ ⋟', callback_data='free')
        ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.OTHER_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
  
    elif query.data == "channels":
        buttons = [[
            InlineKeyboardButton('⚜️ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ⚜️', url=CHNL_LNK)
        ],[
            InlineKeyboardButton('✉️ ʀᴇǫᴜᴇꜱᴛ ɢʀᴏᴜᴘ ✉️', url=GRP_LNK)
        ],[
            InlineKeyboardButton('⇇ ʙᴀᴄᴋ', callback_data='start'),
            InlineKeyboardButton('ꜱᴜᴘᴘᴏʀᴛ 👮', url=CHNL_LNK)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CHANNELS.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "users":
        buttons = [[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.USERS_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "group":
        buttons = [[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GROUP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "admic":
        if query.from_user.id not in ADMINS:
            return await query.answer("⚠️ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀ ʙᴏᴛ ᴀᴅᴍɪɴ !", show_alert=True)        
        buttons = [[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIC_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    

    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('• ʙᴏᴛ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ •', callback_data='admic')
        ], [
            InlineKeyboardButton('• ᴜꜱᴇʀ •', callback_data='users'),
            InlineKeyboardButton('• ɢʀᴏᴜᴘ •', callback_data='group')
        ], [
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('‼️ ᴅɪꜱᴄʟᴀɪᴍᴇʀ ‼️', callback_data='disclaimer'),
        ], [
            InlineKeyboardButton('• ᴏᴡɴᴇʀ •', url=f"https://t.me/Monster_cave"),
            InlineKeyboardButton('• ꜱᴛᴀᴛꜱ •', callback_data='stats')
        ], [
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "shortlink_info":
            btn = [[
            InlineKeyboardButton("1 / 3", callback_data="pagesn1"),
            InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data="shortlink_info2")
            ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )   
    elif query.data == "shortlink_info2":
            btn = [[
            InlineKeyboardButton("⋞ ʙᴀᴄᴋ", callback_data="shortlink_info"),
            InlineKeyboardButton("2 / 3", callback_data="pagesn1"),
            InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data="shortlink_info3")
            ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO2),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "shortlink_info3":
            btn = [[
            InlineKeyboardButton("⋞ ʙᴀᴄᴋ", callback_data="shortlink_info2"),
            InlineKeyboardButton("3 / 3", callback_data="pagesn1")
            ],[
            InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO3),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )   
    
    elif query.data == "disclaimer":
            btn = [[
                    InlineKeyboardButton("⇋ ʙᴀᴄᴋ ⇋", callback_data="about")
                  ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.DISCLAIMER_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML 
            )
               
    elif query.data == "filters":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴀʟ FIʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ FIʟᴛᴇʀ', callback_data='autofilter')
        ],[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs', callback_data='global_filters')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ALL_FILTERS.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "global_filters":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters'),
            InlineKeyboardButton('Bᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )    
    elif query.data == "stats":
        if query.from_user.id not in ADMINS:
            return await query.answer("⚠️ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀ ʙᴏᴛ ᴀᴅᴍɪɴ !", show_alert=True) 
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='start'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "owner_info":
            btn = [[
                    InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="start"),
                    InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ", url="t.me/Monster_cave")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.OWNER_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )

    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if set_type == 'is_shortlink' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hᴇʏ {query.from_user.first_name}, Yᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ !\n\nIᴛ's ᴀɴ ᴀᴅᴍɪɴ ᴏɴʟʏ sᴇᴛᴛɪɴɢ !", show_alert=True)

        if str(grp_id) != str(grpid) and query.from_user.id not in ADMINS:
            await query.message.edit("Yᴏᴜʀ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴ Hᴀs Bᴇᴇɴ Cʜᴀɴɢᴇᴅ. Gᴏ Tᴏ /connections ᴀɴᴅ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.")
            return await query.answer(MSG_ALRT)

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Rᴇꜱᴜʟᴛ Pᴀɢᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Tᴇxᴛ' if settings["button"] else 'Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('SʜᴏʀᴛLɪɴᴋ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["is_shortlink"] else '✘ Oғғ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer(MSG_ALRT)

    
async def auto_filter(client, msg, spoll=False):
    #reqstr1 = msg.from_user.id
    #reqstr = await client.get_users(reqstr1)
    if not spoll:
        message = msg
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if len(message.text) < 100:
            search = message.text
            m=await message.reply_sticker(sticker="CAACAgIAAxkBAAEVugJljpdfkszexOUZu8hPjuPKty8ZmAACdxgAAqPjKEmMVSFmXGLogR4E",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🅿︎🅻︎🅴︎🅰︎🆂︎🅴︎  🆆︎🅰︎🅸︎🆃︎", url=CHNL_LNK)]]))
            search = search.lower()
            find = search.split(" ")
            search = ""
            removes = ["in","upload", "series", "full", "horror", "thriller", "mystery", "print", "file", "send", "chahiye", "chiye", "movi", "movie", "bhejo", "dijiye", "jaldi", "hd", "bollywood", "hollywood", "south", "karo"]
            for x in find:
                if x in removes:
                    continue
                else:
                    search = search + x + " "
            search = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)", "", search, flags=re.IGNORECASE)
            search = re.sub(r"\s+", " ", search).strip()
            search = search.replace("-", " ")
            search = search.replace(":","")
            files, offset, total_results = await get_search_results(message.chat.id ,search, offset=0, filter=True)
            settings = await get_settings(message.chat.id)
            if not files:
                await m.delete()
                if settings["spell_check"]:
                    return await advantage_spell_chok(client, msg)
                else:
                    if NO_RESULTS_MSG:
                        total=await client.get_chat_members_count(message.chat.id)
                        await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(message.chat.title, message.chat.id, total, temp.B_NAME, reqstr.mention, search)))
                    return
        else:
            return
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
        m=await message.reply_sticker(sticker="CAACAgIAAxkBAAEVugJljpdfkszexOUZu8hPjuPKty8ZmAACdxgAAqPjKEmMVSFmXGLogR4E",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🅿︎🅻︎🅴︎🅰︎🆂︎🅴︎  🆆︎🅰︎🅸︎🆃︎", url=CHNL_LNK)]]))
        settings = await get_settings(message.chat.id)
    key = f"{message.chat.id}-{message.id}"
    temp.GETALL[key] = files
    temp.KEYWORD[message.from_user.id] = search
    temp.SHORT[message.from_user.id] = message.chat.id
    files_link = ''
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = []
        for file in files:
            files_link += f"""<b>\n\n❤️ <a href=https://t.me/{temp.U_NAME}?start=files_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('boxoffice') and not x.startswith('Linkz') and not x.startswith('{') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}</a></b>"""
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('Original') and not x.startswith('Villa') and not x.startswith('Linkz') and not x.startswith('boxoffice') and not x.startswith('{') and not x.startswith('Links') and not x.startswith('@') and not x.startswith('www'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        
    btn.insert(0, [
        InlineKeyboardButton("Lᴀɴɢᴜᴀɢᴇs", callback_data=f"select_lang#{message.from_user.id}"),
        InlineKeyboardButton("Qᴜᴀʟɪᴛʏꜱ", callback_data=f"lusi_films#{message.from_user.id}"),
        InlineKeyboardButton("Sᴇᴀꜱᴏɴꜱ", callback_data=f"jk_dev#{message.from_user.id}")
    ])

    btn.insert(0, [
        InlineKeyboardButton("! Sᴇɴᴅ Aʟʟ Tᴏ PM !", callback_data=f"sendfiles#{key}"),
    ])

    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        CAP[key] = search
        req = message.from_user.id if message.from_user else 0
        try:
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(message.chat.id, 'max_btn', True)
            btn.append(
                [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
            )
    else:
        btn.append(
            [InlineKeyboardButton(text="𝐍𝐎 𝐌𝐎𝐑𝐄 𝐏𝐀𝐆𝐄𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄",callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>Hᴇʏ {message.from_user.mention}, Hᴇʀᴇ ɪs Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {search}.</b>"
    CAP[search] = cap
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024] + files_link, reply_markup=InlineKeyboardMarkup(btn))
            await message.delete()
            await m.delete()
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await hehe.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(600)
                await hehe.delete()
                await message.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo=poster, caption=cap[:1024] + files_link, reply_markup=InlineKeyboardMarkup(btn))
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await hmm.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(600)
                await hmm.delete()
                await message.delete()
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_photo(photo=NOR_IMG, caption=cap + files_link, reply_markup=InlineKeyboardMarkup(btn))
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await fek.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(600)
                await fek.delete()
                await message.delete()
    else:
        fuk = await message.reply_photo(photo=NOR_IMG, caption=cap + files_link, reply_markup=InlineKeyboardMarkup(btn))
        await message.delete()
        await m.delete()
        try:
            if settings['auto_delete']:
                await asyncio.sleep(600)
                await fuk.delete()
                await message.delete()
        except KeyError:
            await save_group_settings(message.chat.id, 'auto_delete', True)
            await asyncio.sleep(600)
            await fuk.delete()
            await message.delete()
    if spoll:
        await msg.message.delete()


async def advantage_spell_chok(client, msg):
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    find = mv_rqst.split(" ")
    query = ""
    removes = ["in","upload", "series", "full", "horror", "thriller", "mystery", "print", "file", "send", "chahiye", "chiye", "movi", "movie", "bhejo", "dijiye", "jaldi", "hd", "bollywood", "hollywood", "south", "karo"]
    for x in find:
        if x in removes:
            continue
        else:
            query = query + x + " "
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)", "", query, flags=re.IGNORECASE)
    query = re.sub(r"\s+", " ", query).strip() + "movie"
    try:
        g_s = await search_gagala(query)
        g_s += await search_gagala(msg.text)
        gs_parsed = []
        if not g_s:
            reqst_gle = query.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                total=await client.get_chat_members_count(message.chat.id)
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(message.chat.title, message.chat.id, total, temp.B_NAME, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
        gs = list(filter(regex.match, g_s))
        gs_parsed = [re.sub(
            r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
            '', i, flags=re.IGNORECASE) for i in gs]
        if not gs_parsed:
            reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                             re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
            for mv in g_s:
                match = reg.match(mv)
                if match:
                    gs_parsed.append(match.group(1))
        movielist = []
        gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
        if len(gs_parsed) > 3:
            gs_parsed = gs_parsed[:3]
        if gs_parsed:
            for mov in gs_parsed:
                imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
                if imdb_s:
                    movielist += [movie.get('title') for movie in imdb_s]
        movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
        movielist = list(dict.fromkeys(movielist))  # removing duplicates
        if not movielist:
            reqst_gle = query.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                total=await client.get_chat_members_count(message.chat.id)
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(message.chat.title, message.chat.id, total, temp.B_NAME, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        SPELL_CHECK[mv_id] = movielist
        btn = [[
            InlineKeyboardButton(
                text=movie.strip(),
                callback_data=f"spolling#{reqstr1}#{k}",
            )
        ] for k, movie in enumerate(movielist)]
        btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
        spell_check_del = await msg.reply_photo(
            photo=(SPELL_IMG),
            caption=(script.CUDNT_FND.format(mv_rqst)),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        try:
            if settings['auto_delete']:
                await asyncio.sleep(60)
                await spell_check_del.delete()
        except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(60)
                    await spell_check_del.delete()
    except:
        try:
            movies = await get_poster(mv_rqst, bulk=True)
        except Exception as e:
            logger.exception(e)
            reqst_gle = mv_rqst.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                total=await client.get_chat_members_count(message.chat.id)
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(message.chat.title, message.chat.id, total, temp.B_NAME, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        movielist = []
        if not movies:
            reqst_gle = mv_rqst.replace(" ", "+")
            button = [[
                       InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
            ]]
            if NO_RESULTS_MSG:
                total=await client.get_chat_members_count(message.chat.id)
                await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(message.chat.title, message.chat.id, total, temp.B_NAME, reqstr.mention, mv_rqst)))
            k = await msg.reply_photo(
                photo=SPELL_IMG, 
                caption=script.I_CUDNT.format(mv_rqst),
                reply_markup=InlineKeyboardMarkup(button)
            )
            await asyncio.sleep(30)
            await k.delete()
            return
        movielist += [movie.get('title') for movie in movies]
        movielist += [f"{movie.get('title')} {movie.get('year')}" for movie in movies]
        SPELL_CHECK[mv_id] = movielist
        btn = [
            [
                InlineKeyboardButton(
                    text=movie_name.strip(),
                    callback_data=f"spol#{reqstr1}#{k}",
                )
            ]
            for k, movie_name in enumerate(movielist)
        ]
        btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
        spell_check_del = await msg.reply_photo(
            photo=(SPELL_IMG),
            caption=(script.CUDNT_FND.format(mv_rqst)),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        try:
            if settings['auto_delete']:
                await asyncio.sleep(600)
                await spell_check_del.delete()
        except KeyError:
                grpid = await active_connection(str(msg.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(msg.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(600)
                    await spell_check_del.delete()


async def manual_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)

                        else:
                            button = eval(btn)
                            joelkb = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)

                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            protect_content=True if settings["file_secure"] else False,
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)

                    else:
                        button = eval(btn)
                        joelkb = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await asyncio.sleep(600)
                                        await joelkb.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def global_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            manual = await manual_filters(client, message)
                            if manual == False:
                                settings = await get_settings(message.chat.id)
                                try:
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message)
                                        try:
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                    else:
                                        try:
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_ffilter', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message) 
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            
                        else:
                            button = eval(btn)
                            joelkb = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            manual = await manual_filters(client, message)
                            if manual == False:
                                settings = await get_settings(message.chat.id)
                                try:
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message)
                                        try:
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                    else:
                                        try:
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await asyncio.sleep(600)
                                                await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_ffilter', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message) 
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()

                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        manual = await manual_filters(client, message)
                        if manual == False:
                            settings = await get_settings(message.chat.id)
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message) 
                        else:
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                    else:
                        button = eval(btn)
                        joelkb = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        manual = await manual_filters(client, message)
                        if manual == False:
                            settings = await get_settings(message.chat.id)
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(600)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message) 
                        else:
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
