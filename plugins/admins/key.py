import asyncio
import json
import requests
import re
from pyrogram import Client, filters
from pyrogram.types import Message
import random
import string
from datetime import datetime, timedelta
import mysql.connector
from db import cursor, db

def random_string(length):
    characters = string.digits + string.ascii_lowercase
    return ''.join(random.choice(characters) for _ in range(length))

async def generate_key():
    key_exists = True
    generated_key = ''

    while key_exists:
        two = random_string(4)
        three = random_string(4)
        four = random_string(4)
        generated_key = f'SkullGuard-{two}{three}{four}'

        cursor = db.cursor()
        select_query = "SELECT * FROM keyuser WHERE clave = %s"
        cursor.execute(select_query, (generated_key,))
        result = cursor.fetchone()
        cursor.close()  # Close the cursor manually

        if not result:
            key_exists = False

    return generated_key

@Client.on_message(filters.command('key', prefixes='/'))
async def generate_and_store_key(client: Client, message: Message):
    query = "SELECT * FROM admins WHERE user_id = %s"
    user_id = message.from_user.id

    cursor = db.cursor()
    cursor.execute(query, (user_id,))
    cursor.fetchall()
    cursor.close()  # Close the cursor manually

    if cursor.rowcount == 0:
        await message.reply_text("<i>❌ Sorry, you don't have permission to execute this command.</i>")
        return

    # Check if the command contains a valid argument
    arguments = message.text.split(' ', 1)
    if len(arguments) < 2:
        await message.reply('<i>❌ Incorrect format. Usage: /key [days]</i>')
        return

    days = arguments[1].strip()

    # Check if the argument is a valid number
    if not days.isdigit():
        await message.reply('<i>❌ Incorrect format. The number of days must be a valid numerical value.</i>')
        return

    days = int(days)
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=days)

    generated_key = await generate_key()

    # Insert the generated key into the database
    cursor = db.cursor()
    insert_query = "INSERT INTO keyuser (clave, status, planexpiry) VALUES (%s, %s, %s)"
    insert_data = (generated_key, 'Premium', expiration_date)
    cursor.execute(insert_query, insert_data)
    db.commit()
    cursor.close()  # Close the cursor manually

    # Send response message with the generated key information
    await message.reply(f'<b>♻️ Key created successfully</b>\n'
                        f'━━━━━━━━━━━━━━━━━━\n'
                        f'<i>⚜️ Key:</i> <code>{generated_key}</code>\n'
                        f'<i>➤ Rank:</i> <code>Premium</code>\n'
                        f'<i>📛 Expiration Date:</i> <code>{expiration_date.strftime("%Y-%m-%d")}</code>\n'
                        f'━━━━━━━━━━━━━━━━━━')
