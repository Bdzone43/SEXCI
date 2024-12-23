from pyrogram import Client, filters

# Command /ID
@Client.on_message(filters.command("id"))
async def get_id(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the message is a reply to another message
    if message.reply_to_message:
        replied_user_id = message.reply_to_message.from_user.id
        replied_chat_id = message.reply_to_message.chat.id
        await message.reply_text(
            f"👤 User ID: <code>{replied_user_id}</code>\n"
            f"📌 Chat ID: <code>{replied_chat_id}</code>"
        )
    else:
        await message.reply_text(
            f"👤 Your ID: <code>{user_id}</code>\n"
            f"📌 Chat ID: <code>{chat_id}</code>"
        )
