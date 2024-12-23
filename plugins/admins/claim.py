from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
import mysql.connector
from db import cursor, db

@Client.on_message(filters.command('claim', prefixes='/'))
async def claim_key(client: Client, message: Message):
    user_id = message.from_user.id
    command, *arguments = message.text.split(' ', 1)

    if not arguments:
        await message.reply('<i>❌ Incorrect format. Usage: /claim key</i>')
        return

    arguments = arguments[0]

    command, key = message.text.split(' ', 1)
    key = key.strip()

    select_query = "SELECT * FROM users WHERE user_id = %s"
    select_data = (user_id,)
    cursor.execute(select_query, select_data)
    user_data = cursor.fetchone()

    if user_data:
        warns = user_data[6] if user_data[6] is not None else 0

        if warns is None:
            warns = 0

        if int(warns) >= 4:
            await message.reply('<b>❌ You are temporarily banned. You cannot use this command for the next 12 hours.</b>')
            return

        select_query = "SELECT * FROM keyuser WHERE `clave` = %s AND `status` = 'Premium'"
        select_data = (key,)
        cursor.execute(select_query, select_data)
        result = cursor.fetchone()

        if result:
            key_data = result
            expiration_date = key_data[3]

            # Update users table with the claimed key, credits, and expiration_date
            update_query_users = "UPDATE users SET `key` = %s, `creditos` = `creditos` + 20, `expiration_date` = %s WHERE user_id = %s"
            update_data_users = (key, expiration_date, user_id)
            cursor.execute(update_query_users, update_data_users)
            db.commit()

            # Mark the claimed key as 'Active' in keyuser table
            update_query_keyuser = "UPDATE keyuser SET `status` = 'Active' WHERE `clave` = %s"
            update_data_keyuser = (key,)
            cursor.execute(update_query_keyuser, update_data_keyuser)
            db.commit()

            await message.reply(f'<b>✅ Key successfully claimed. 20 credits have been added to your account. Expires on: {expiration_date}</b>')
        else:
            warns += 1

            if int(warns) >= 4:
                update_query = "UPDATE users SET `warns` = %s, `status` = 'Banned', `ban_expiration` = %s WHERE user_id = %s"
                ban_expiration = datetime.now() + timedelta(hours=12)
                update_data = (warns, ban_expiration, user_id)
                cursor.execute(update_query, update_data)
                db.commit()

                await message.reply('<b>❌ You are temporarily banned. You cannot use this command for the next 12 hours.</b>')
            else:
                await message.reply('<b>❌ The key is not valid or not available with \'Premium\' status.</b>')
    else:
        return
