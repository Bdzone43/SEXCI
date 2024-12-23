import requests
from pyrogram import Client, filters
import re

def extract_credit_card_info(text):
    pattern = r'\b(\d{16})\|(\d{1,2}\|\d{4})\|(\d{3})\b'
    matches = re.findall(pattern, text)
    
    if not matches:
        return "No valid credit card information found in the message."

    return "\n".join(f"{card}|{expiry}|{cvv}" for card, expiry, cvv in matches)

@Client.on_message(filters.command("clean") & filters.reply)
async def handle_clean_command(_, message):
    replied_message = message.reply_to_message

    if not replied_message.text:
        await message.reply_text("The replied-to message does not contain text.")
        return

    cleaned_info = extract_credit_card_info(replied_message.text)
    await message.reply_text(cleaned_info)
