from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
import asyncio
import random

from db import *

async def get_user_ids():
    query = "SELECT user_id FROM users"
    cursor.execute(query)
    results = cursor.fetchall()
    user_ids = [str(row[0]) for row in results]
    return user_ids

image_urls = [
    "https://tenor.com/view/insomnia-chan-hot-sexy-anime-girl-hot-anime-girl-gif-25339956",
    "https://tenor.com/view/cute-anime-anime-girl-pink-hearts-gif-2859182496452245481",
    "https://tenor.com/view/lewd-anime-gif-18327152"
]

@Client.on_message(filters.command("message", prefixes="/"))
async def send_private_message(client, message):
    sender_id = message.from_user.id

    with open('owner.txt', 'r') as file:
        allowed_ids = file.read().splitlines()

    if str(sender_id) not in allowed_ids:
        no_permission_message = "Sorry, you don't have permission to do this."
        await client.send_message(message.chat.id, no_permission_message)
        return

    # Check if there's at least one element in the list before accessing the second element
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await client.send_message(message.chat.id, "Please provide a message to send.")
        return

    custom_message = command_parts[1]

    confirmation_message = "The message is being sent to all users."
    await client.send_message(message.chat.id, confirmation_message)

    user_ids = await get_user_ids()

    tasks = []
    for user_id in user_ids:
        try:
            image_url = random.choice(image_urls)
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("References", url="https://t.me/stripekeys"),
                    InlineKeyboardButton("Skull Info", url="https://t.me/SkullInfo"),
                ],
            ])
            task = client.send_animation(user_id,
                                     image_url,
                                     caption=f"<b>{custom_message}</b>",
                                     reply_markup=keyboard)
            tasks.append(task)
        except Exception as e:
            error_message = f"Error sending message to {user_id}: {str(e)}"
            await client.send_message(message.chat.id, error_message)

    await asyncio.gather(*tasks)

    message_sent = "The message has been sent to all users."
    await client.send_message(message.chat.id, message_sent)
