from pyrogram import Client, filters
from db import *

@Client.on_message(filters.command(["delkey"], ["/", "."]))
async def process_command(client, message):
    sender_id = message.from_user.id
    query = "SELECT * FROM admins WHERE user_id = %s"
    cursor = db.cursor()
    cursor.execute(query, (sender_id,))
    cursor.fetchall()
    if cursor.rowcount == 0:
        await message.reply_text("<i>❌ Sorry, you don't have permission to execute this command.</i>")
        return

    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply_text("<i>❌ Incorrect format. You should use: /delkey key</i>")
        return

    key_to_delete = command_parts[1]

    query_key = "SELECT * FROM users WHERE `key` = %s"
    cursor.execute(query_key, (key_to_delete,))
    key_data = cursor.fetchone()
    if not key_data:
        await message.reply_text("<i>❌ The key does not exist in the database.</i>")
        return

    user_id = key_data[0]
    update_query = "UPDATE users SET status = 'free user', credits = credits - 20, `key` = NULL, expiration_date = NULL WHERE user_id = %s"
    cursor.execute(update_query, (user_id,))
    db.commit()

    await message.reply_text("The key has been deleted, and 20 credits have been deducted from the user with ID {}. The key and expiration date have been set to NULL.".format(user_id))
