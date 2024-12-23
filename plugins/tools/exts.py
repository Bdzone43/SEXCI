from pyrogram import Client, filters

@Client.on_message(filters.command(["exts"], prefixes=["/", "."]))
async def similarity_method(client, message):
    text = message.text[len("/exts "):]

    # Ensure the format is correct
    if '-' not in text:
        await message.reply_text(
            "❌ *Incorrect format!* ❌\n\n"
            "Please use the following format:\n"
            "/exts 4115680117164577-4178490024082621\n\n"
            "Ensure both card numbers are separated by a hyphen (-)."
        )
        return

    # Split the two card numbers
    t1, t2 = text.split("-")

    bin_t1, rest_t1 = t1[:6], t1[6:]
    bin_t2, rest_t2 = t2[:6], t2[6:]

    # Calculate the similarity part
    similarity = ''.join([digit if digit == rest_t1[idx] else 'x' for idx, digit in enumerate(rest_t2)])

    # Extrapolated card based on similarity
    extrapolated_card = f"{bin_t1}{similarity}"

    # Send the result with enhanced formatting
    await message.reply_text(
        f"🔍 *Similarity Method Result:* 🔍\n\n"
        f"🔢 Extrapolated Card: `{extrapolated_card}`\n\n"
        "🔒 This is a *masked* version of the card number for security purposes."
    )
