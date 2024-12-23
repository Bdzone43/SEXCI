from pyrogram import Client, filters
from db import *

@Client.on_message(filters.command(["deldb"], ["/", "."]))
async def process_command(client, message):
    # Extract the user ID provided after the "/deldb" command
    sender_id = message.from_user.id
    query = "SELECT * FROM admins WHERE user_id = %s"
    cursor = db.cursor()
    cursor.execute(query, (sender_id,))
    cursor.fetchall()  # Discard unread results
    if cursor.rowcount == 0:
        await message.reply_text("<i>❌ Sorry, you don't have permission to execute this command.</i>")
        return
    command_parts = message.text.split(" ")
    if len(command_parts) != 2 or not command_parts[1].isdigit():
        await message.reply_text("<i>❌ Incorrect format. You should use: /deldb ID</i>")
        return

    user_id = int(command_parts[1])

    # Delete the user from the database
    delete_query = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(delete_query, (user_id,))
    db.commit()

    # Send a response to the user
    await message.reply_text("The user with ID {} has been deleted from the database.".format(user_id))

# Define and run the event loop
