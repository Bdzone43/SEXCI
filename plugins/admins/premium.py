from pyrogram import Client, filters
from db import *
import datetime

@Client.on_message(filters.command(["prem"], ["/", "."]))
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
        await message.reply_text("<i>❌ Incorrect format. You should use: /prem ID|days</i>")
        return

    user_id, expiration_days = command_parts[1].split("|")
    if not user_id.isdigit() or not expiration_days.isdigit():
        await message.reply_text("<i>❌ Incorrect format. You should use: /prem ID|days</i>")
        return

    user_id = int(user_id)
    expiration_days = int(expiration_days)

    expiration_date = datetime.datetime.now() + datetime.timedelta(days=expiration_days)
    expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")

    update_query = "UPDATE users SET status = 'Premium', expiration_date = %s WHERE user_id = %s"
    cursor.execute(update_query, (expiration_date_str, user_id))
    db.commit()

    await message.reply_text("The user with ID {} is now a Premium user until {}.".format(user_id, expiration_date_str))
