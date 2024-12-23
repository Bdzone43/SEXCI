from pyrogram import Client, filters
import time

@Client.on_message(filters.command("ping"))
async def ping(client, message):
    ping = round(time.time() - message.date.timestamp(), 2)
    await message.reply(f"[🏓] <b>Pong</b> ↯ <code>{ping}</code>")
