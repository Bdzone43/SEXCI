import mysql.connector
from pyrogram import Client, filters
from db import *

@Client.on_message(filters.command(["register", ".register"]))
async def register_command(client, message):
    # Check if the user is already registered in the database
    user_id = message.from_user.id
    cursor = db.cursor()
    username = message.from_user.username
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        # The user is already registered
        await client.send_message(
            chat_id=message.chat.id,
            text="<i>❌You are already registered.</i>"
        )
    else:
        # Register the user as a free user in the database
        insert_query = f"INSERT INTO users (user_id, username, status, expiration_date, creditos, warns) VALUES ('{user_id}', '{username}', 'free user', NULL, 0, NULL)"
        cursor.execute(insert_query)
        db.commit()
        await client.send_message(
            chat_id=message.chat.id,
            text="<i>You have successfully registered!</i>"
        )
