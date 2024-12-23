from pyrogram import Client, filters
from db import *
import random
import requests
import time

@Client.on_message(filters.command("extra", ["/", "."]))
async def generate_extra(client, message):
    start_time = time.perf_counter()

    user_id = message.from_user.id
    cursor.execute(f"SELECT status FROM users WHERE user_id='{user_id}'")
    result = cursor.fetchone()

    if result is None:
        await message.reply_text("You are not registered. Please use /register to sign up.")
        return

    rank = result[0]
    input_message = message.text.split(None, 1)

    if len(input_message) != 2 or not input_message[1]:
        await message.reply_text("<b>⚠️ Incorrect usage. Use /extra followed by the first 6 digits of the BIN.</b>")
        return

    BIN = input_message[1][:6]
    req = requests.get(f"https://bins.antipublic.cc/bins/{BIN}").json()

    try:
        brand, country, country_name, country_flag, country_currencies, bank, level, typea = (
            req['brand'], req['country'], req['country_name'], req['country_flag'],
            req['country_currencies'], req['bank'], req['level'], req['type']
        )
    except KeyError:
        await message.reply_text("Sorry, the BIN is not in my database.")
        return

    extrapolated_results = [
        f"<code>{BIN}{''.join(random.choice('0123456789') for _ in range(6))}xxxx|{random.randint(1, 12):02d}|{random.randint(2024, 2030)}</code>"
        for _ in range(28)
    ]

    similar_bins = [f"<code>{BIN}{''.join(random.choice('0123456789') for _ in range(4))}</code>" for _ in range(2)]

    end_time = time.perf_counter()

    message_text = f"""
<b>✅ Extrap Generated Successfully</b>
Bin Info: <code>{level} - {typea} [{country_flag}]</code>
Bank: <code>{bank}</code>
Country: <code>{country_name} - {country}</code>
🔢 Extra Digits: 333

━━━━━━━━━━━━━━━━━━
""" + "\n".join(extrapolated_results) + f"""
━━━━━━━━━━━━━━━━━━

Similar Extras Available:
↳ » {' '.join(similar_bins)} «

Generated by ~ {message.from_user.username}
Execution Time: {end_time - start_time:.2f} seconds
"""

    await message.reply_text(text=message_text)