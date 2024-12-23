import requests
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("bin", prefixes=["/", "."]))
async def bin_lookup(client, message):
    try:
        input_text = message.text.split()
        if len(input_text) < 2 or len(input_text[1]) < 6:
            return await message.reply("<i>❌ Invalid format. Use: <code>/bin 456789</code></i>")

        bin_code = input_text[1][:6]
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_code}").json()

        if 'bin' not in response:
            await message.reply_text(f"<i>❌ Error: BIN not found <code>{bin_code}</code></i>")
        else:
            brand = response.get('brand', 'N/A')
            country_name = response.get('country_name', 'N/A')
            country_flag = response.get('country_flag', '')
            country_currency = response.get('country_currencies', 'N/A')
            bank = response.get('bank', 'N/A')
            level = response.get('level', 'N/A')
            type_card = response.get('type', 'N/A')
            username = message.from_user.username or "Unknown User"

            await message.reply_text(f"""
<b>[ϟ] BIN Lookup</b>
━━━━━━━━━━━━━━━
<b>[Ϟ] BIN:</b> <code>{bin_code}</code>
<b>[Ϟ] Info:</b> {brand} - {type_card} - {level}
<b>[Ϟ] Bank:</b> {bank}
<b>[Ϟ] Country:</b> {country_name} {country_flag} - {country_currency}
━━━━━━━━━━━━━━━
<b>Checked By:</b> @{username}
""")

    except Exception as e:
        await message.reply("<i>❌ An error occurred while processing your request.</i>")
        print(f"Error: {e}")
