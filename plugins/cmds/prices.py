from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *

@Client.on_message(filters.command("price"))
async def cmds_command2(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    query = f"SELECT username, status, expiration_date, creditos FROM users WHERE user_id='{user_id}'"
    cursor.execute(query)

    result = cursor.fetchone()
    if result is None:
        await client.send_message(message.chat.id, "You are not registered. Please use /register to sign up.")
        return

    video_path = "https://telegra.ph/file/713a63a369be49accbb0a.jpg"

    if result:
        rank = result[1]
        expiration = result[2]
        credits = result[3]
    else:
        rank = None

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📿 References", url="https://t.me/AzunaReferencias"),
                InlineKeyboardButton("📿 Info and Updates", url="https://t.me/AzunaInfo"),
            ]
        ]
    )

    await client.send_video(message.chat.id, video_path, caption=f"""
<i>
📛 PERSONAL PRICES

💸 15 days: $2.60
💸 30 days: $4.60 

━━━━━━━━━━━━━

🔰 GROUP PRICES 

💸 15 Days: $1.60
💸 30 Days: $3.60

━━━━━━━━━━━━━

[🝂] | Payment Methods

✅ Paypal
</i>
""", reply_markup=keyboard, reply_to_message_id=message.id)
