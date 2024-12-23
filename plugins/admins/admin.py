import json
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import mysql.connector
from db import cursor, db

@Client.on_message(filters.command("admin"))
async def process_admin_command(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.id

    # Ensure only the owner of the bot can execute this command
    if user_id != 5850715014:
        return

    # Only process the command if it starts with '/admin'
    if not message.text.startswith('/admin'):
        return

    # Split the message into parts to extract the user_id
    parts = message.text.split(' ')
    if len(parts) < 2:
        await client.send_message(chat_id, "El formato es: /admin [ID]", reply_to_message_id=message_id)
        return

    user_id_str = parts[1].strip()

    # Check if the user ID is numeric
    if not user_id_str.isnumeric():
        await client.send_message(chat_id, "El ID de usuario debe ser un número", reply_to_message_id=message_id)
        return

    user_id = int(user_id_str)

    # Ensure the database is connected
    if not db.is_connected():
        await client.send_message(chat_id, "No se pudo conectar a la base de datos", reply_to_message_id=message_id)
        return

    # Query to check if the user is already an admin
    query = "SELECT username FROM admins WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    result = cursor.fetchone()

    if result:
        username = result[0]
        await client.send_message(chat_id, f"El usuario @{username} ya es un admin", reply_to_message_id=message_id)
    else:
        # If user is not already an admin, try to fetch username from Telegram API
        try:
            api_url = f"https://api.telegram.org/bot5632332899:AAGa6LwI9EP9nOhJ40Z24Pt2Smkf1eODyWM/getChat?chat_id={user_id}"
            api_response = requests.get(api_url).json()

            # Check if the API response is successful
            if not api_response["ok"]:
                await client.send_message(chat_id, "No se pudo obtener información del usuario", reply_to_message_id=message_id)
                return

            username = api_response["result"].get("username")
            if not username:
                await client.send_message(chat_id, "El usuario no tiene un nombre de usuario", reply_to_message_id=message_id)
                return
        except Exception as e:
            await client.send_message(chat_id, f"No se pudo obtener el nombre de usuario del ID {user_id}", reply_to_message_id=message_id)
            print(f"Error fetching user info: {e}")
            return

        # Insert the user as admin into the database
        query = "INSERT INTO admins (user_id, username) VALUES (%s, %s)"
        cursor.execute(query, (user_id, username))
        db.commit()

        # Send confirmation message
        await client.send_message(chat_id, f"El usuario @{username} ahora es un admin", reply_to_message_id=message_id)
