from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *

@Client.on_message(filters.command("gate"))
async def cmds_command2(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    query = f"SELECT username, status, expiration_date, creditos FROM users WHERE user_id='{user_id}'"
    cursor.execute(query)

    result = cursor.fetchone()
    if result is None:
        await client.send_message(message.chat.id, "You are not registered. Please use /register to register.")
        return

    video_path = "https://telegra.ph/file/8412cb157c94d03b14aa2.gif"

    if result:
        rank = result[1]
        expiration = result[2]
        credits = result[3]
    else:
        rank = None

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("auth", callback_data="auth"),
                InlineKeyboardButton("charged", callback_data="charged"),
            ],
            [
                InlineKeyboardButton("back", callback_data="back"),
            ]
        ]
    )

    await client.send_video(
        message.chat.id,
        video_path,
        caption=f"""

<b>♻️ Available Gates</b> 

<b>➤  Auth  [3]</b>
<b>[🝂] Charger [3]</b>

<b>[↯] New gates will be added soon....</b>━""",
        reply_markup=keyboard,
        reply_to_message_id=message.id  # Corrected here
    )
