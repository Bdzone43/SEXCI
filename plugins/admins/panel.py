from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
import random
from db import *

@Client.on_message(filters.command(["panel"], ["/", ".", ","]))
async def panel_command(client, message):
    user_id = message.from_user.id

    query = "SELECT * FROM admins WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    cursor.fetchall()

    if cursor.rowcount == 0:
        await message.reply_text("<i>❌ Sorry, you don't have permission to execute this command.</i>")
        return

    video_urls = [
        "https://graph.org/file/9ee7720ecacd44284c13a.gif",
        "https://graph.org/file/7f9436694f82aa6907e97.gif",
        "https://graph.org/file/67ace25a998c1885b6245.gif"
    ]

    sent_videos = getattr(client, "sent_videos", [])

    if len(sent_videos) == len(video_urls):
        sent_videos = []

    video_path = None
    while not video_path:
        random_video = random.choice(video_urls)
        if random_video not in sent_videos:
            video_path = random_video

    sent_videos.append(video_path)
    setattr(client, "sent_videos", sent_videos)

    caption = """
<b>Welcome, Admin! Below are the commands you can use:</b>
<i>
/addgp <id and plan days>
/key |days
/ban id|reason
/unapremium id
/deldb
/unban
</i>"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📿 Profile", callback_data="me"),
            ]
        ]
    )

    await client.send_video(message.chat.id, video_path, caption=caption, reply_markup=keyboard)
