from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *

@Client.on_message(filters.command("profile"))
async def cmds_command2(client, message):
    if message.reply_to_message:
        reply_msg = message.reply_to_message

        if not reply_msg.from_user:
            await message.reply_text("❌ Failed to retrieve user information.")
            return

        user_id = reply_msg.from_user.id
        query = f"SELECT username, status, expiration_date, credits FROM users WHERE user_id='{user_id}'"
        cursor.execute(query)

        result = cursor.fetchone()
        if result is None:
            await message.reply_text("User is not registered.")
            return

        video_path = "https://graph.org/file/9ee7720ecacd44284c13a.gif"
        rank, expiration, credits = result[1], result[2], result[3]

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ]
            ]
        )

        await client.send_video(
            message.chat.id,
            video_path,
            caption=f"""
♻️ Profile Info 
━━━━━━━━━━━━━━━━━━
⚜️ User: 
➳ User ID: <code>{user_id}</code>
➤ Rank: <code>{rank}</code>
📛 Expiration Date: <code>{expiration}</code>
🔑 Credits: <code>{credits}</code>
━━━━━━━━━━━━━━━━━━""",
            reply_markup=keyboard,
            reply_to_message_id=message.id
        )
    else:
        user_id = message.from_user.id
        query = f"SELECT username, status, expiration_date, credits FROM users WHERE user_id='{user_id}'"
        cursor.execute(query)

        result = cursor.fetchone()
        if result is None:
            await message.reply_text("You are not registered. Please use /register to register.")
            return

        video_path = "https://graph.org/file/9ee7720ecacd44284c13a.gif"
        rank, expiration, credits = result[1], result[2], result[3]

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ]
            ]
        )

        await client.send_video(
            message.chat.id,
            video_path,
            caption=f"""
♻️ Profile Info 
━━━━━━━━━━━━━━━━━━
⚜️ User: 
➳ ID: <code>{user_id}</code>
➤ Rank: <code>{rank}</code>
📛 Expiration Date: <code>{expiration}</code>
🔑 Credits: <code>{credits}</code>
━━━━━━━━━━━━━━━━━━""",
            reply_markup=keyboard,
            reply_to_message_id=message.id
        )
