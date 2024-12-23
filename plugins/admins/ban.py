from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
import mysql.connector
from db import cursor, db

async def ban_user(client, user_id, reason="No reason provided"):
    try:
        delete_query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        db.commit()

        with open('banned.txt', 'a') as file:
            file.write(str(user_id) + '\n')

        broadcast_msg = (
            f"<b>User ID:</b> {user_id}\n"
            f"<b>Status:</b> Banned\n"
            f"<b>Reason:</b> {reason}"
        )
        await client.send_message(user_id, broadcast_msg)

        return True
    except Exception as e:
        print(f"Error banning user {user_id}: {e}")
        return False

# Admin verification logic
async def verify_admin(client, message):
    user_id = message.from_user.id

    query = "SELECT * FROM admins WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    cursor.fetchall()

    if cursor.rowcount == 0:
        await message.reply_text("<i>❌ Sorry, you don't have permission to execute this command.</i>")
        return False

    return True

@Client.on_message(filters.command('ban', prefixes='/'))
async def ban_user_command(client: Client, message: Message):
    # Verify if the user executing the command is an admin
    if not await verify_admin(client, message):
        return

    # Extract the user ID and reason to be banned from the command
    argumentos = message.text.split(' ', 2)

    # Check if there are at least 2 arguments (user_id and reason)
    if len(argumentos) < 2:
        await message.reply('<i>❌ Incorrect format. Usage: /ban [user_id] [reason]</i>')
        return

    user_id = argumentos[1].strip()

    if user_id.isdigit():
        user_to_ban = int(user_id)

        # Perform the banning logic
        reason = argumentos[2].strip() if len(argumentos) > 2 else "No reason provided"
        if await ban_user(client, user_to_ban, reason):
            await message.reply(f'<b>✅ User {user_to_ban} has been banned successfully</b>')
        else:
            await message.reply(f'<b>❌ Failed to ban user {user_to_ban}. Please check the logs for details.</b>')
    else:
        await message.reply('<i>❌ Invalid user ID.</i>')
