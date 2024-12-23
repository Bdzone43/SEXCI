from pyrogram import Client, filters

@Client.on_message(filters.command(["extb"], ["/", "."]))
async def basic_method(client, message):
    text = message.text[len("/extb "):]
    
    # Check if the text is a valid 16-digit card number
    if not text.isdigit() or len(text) != 16:
        await message.reply_text(
            "🚨 *Incorrect format!* 🚨\n\n"
            "❗️ Please make sure to use the correct format:\n\n"
            "🔑 /extb 4115680117164577\n\n"
            "⚠️ Ensure the number is exactly *16 digits* long.\n\n"
            "If you're still having trouble, check if the number is missing any digits or contains non-numeric characters."
        )
        return

    # Extrapolate the card number
    extrapolated_card = f"{text[:10]}xx xxxx"
    
    # Send the extrapolated result
    await message.reply_text(
        f"🔍 *Result of the basic method*:\n\n"
        f"🔢 Extrapolated Card: `{extrapolated_card}`\n\n"
        "🔒 This is a *masked* version of the card number for security purposes. Only a portion of the card is visible."
    )
