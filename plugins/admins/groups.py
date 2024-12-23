import mysql.connector
import requests
import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from db import *
from unidecode import unidecode

@Client.on_message(filters.command(["addgp"], ["/", "."]))
async def add_group_to_database(_, message: Message):
    user_id = message.from_user.id
    query = "SELECT * FROM admins WHERE user_id = %s"
    cursor = db.cursor()
    cursor.execute(query, (user_id,))
    cursor.fetchall()
    if cursor.rowcount == 0:
        await message.reply_text("<i>❌ Sorry, you don't have permission to execute this command.</i>")
        return

    args = message.text.split("|")
    if len(args) != 2:
        await message.reply_text("<i>Incorrect format.</i> The /addgp command should be followed by the group ID and expiration days separated by '|'. Example: /addgp -1001610482690|30")
        return

    group_id = args[0].strip().replace("/addgp ", "")
    expiry_days = args[1].strip()

    if not group_id.startswith("-") or not group_id[1:].isdigit() or not expiry_days.isdigit():
        await message.reply_text("The group ID and/or expiration days are not valid. Make sure to enter numbers and a valid group ID with the '-' sign.")
        return

    group_id = int(group_id)
    expiry_days = int(expiry_days)
    url = f"https://api.telegram.org/bot5632332899:AAGa6LwI9EP9nOhJ40Z24Pt2Smkf1eODyWM/getChat?chat_id={group_id}"
    response = requests.get(url).json()

    if not response['ok'] or 'result' not in response or 'title' not in response['result']:
        await message.reply_text(f"Unable to retrieve group information. Make sure to provide a valid group ID: {group_id}")
        return

    group_title = response['result']['title']
    group_username = response['result'].get('username', unidecode(group_title.lower()))

    query = "SELECT * FROM `groups` WHERE id = %s"
    cursor.execute(query, (group_id,))
    if cursor.fetchone() is not None:
        await message.reply_text(f"<i>❌ Oh no!!, The group \"{group_title}\" is already registered as premium and cannot be premium again.</i>")
        return

    expiry_date = (datetime.datetime.now() + datetime.timedelta(days=expiry_days)).date()

    query = "INSERT INTO `groups` (id, name, expiration_date, status) VALUES (%s, %s, %s, 'premium')"
    cursor.execute(query, (group_id, group_username, expiry_date))
    db.commit()

    cursor.nextset()

    await message.reply_text(f"<i>The group \"{group_title}\" has been registered as premium with the expiration date.</i>")
