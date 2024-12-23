import requests
import re
from pyrogram import Client, filters

@Client.on_message(filters.command("ibam"))
async def ibam_check(client, message):
    try:
        # Extract the IBAN from the message
        data = message.text[len('/ibam '):].strip()

        if not data:
            await message.reply("<b>⎚ Invalid or Empty Input</b> ❌\n<b>Format:</b> <code>/ibam IBAN_NUMBER</code>")
            return

        # Regular expression to match a valid IBAN
        iban_regex = r"([A-Z]{2}[ \'\+\-]?[0-9]{2})(?=(?:[ \'\+\-]?[A-Z0-9]){9,30}$)((?:[ \'\+\-]?[A-Z0-9]{3,5}){2,7})([ \'\+\-]?[A-Z0-9]{1,3})?"

        # Match the IBAN against the regex
        if not re.match(iban_regex, data):
            await message.reply("<b>❌ Error</b> → <i>Please enter a valid IBAN.</i>")
            return

        # Call the external IBAN validation API
        api_url = f'https://openiban.com/validate/{data}?getBIC=true&validateBankCode=true'
        response = requests.get(api_url)

        if response.status_code != 200:
            await message.reply("<b>❌ Error</b> → <i>Server error occurred while validating the IBAN.</i>")
            return

        # Parse the API response
        api_json = response.json()

        if not api_json.get("valid"):
            error_msg = api_json.get("messages", ["This IBAN isn't valid"])
            await message.reply(f"<b>❌ Error</b> → <i>{', '.join(error_msg)}</i>")
            return

        # Extract bank information
        bank = api_json.get("bankData", {})
        bank_name = bank.get("name", "N/A")
        bank_code = bank.get("bankCode", "N/A")
        bank_bic = bank.get("bic", "N/A")

        # Construct the success message with clean formatting
        msg = f"""
<b>📟 IBAN Validation Result</b>
─────────────────────────
<b>IBAN:</b> <code>{data}</code>

<b>Messages:</b> <i>{', '.join(api_json.get('messages', []))}</i>

<b>🏦 Bank Information:</b>
  • <b>Name:</b> <i>{bank_name}</i>
  • <b>Code:</b> <i>{bank_code}</i>
  • <b>BIC:</b> <i>{bank_bic}</i>

─────────────────────────
<b>Checked by:</b> @{message.from_user.username}
<b>Bot created by:</b> [ꜱʜɪɴ々cʜᴀɴ]
"""
        await message.reply(msg)
    
    except Exception as e:
        # Handle unexpected errors
        await message.reply("<b>❌ Error</b> → <i>Something went wrong. Please try again later.</i>")
        print(f"Error: {e}")
