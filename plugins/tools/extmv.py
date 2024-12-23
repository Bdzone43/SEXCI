from pyrogram import Client, filters

@Client.on_message(filters.command(["extmv"], prefixes=["/", "."]))
async def material_inverter_method(client, message):
    text = message.text[len("/extmv "):]

    # Check if the message format is correct
    if '-' not in text or len(text.split("-")) != 2:
        await message.reply_text(
            "❌ *Incorrect format!* ❌\n\n"
            "Please ensure you are using the correct format:\n"
            "/extmv 4879176315980274-4879170021981999\n\n"
            "Both card numbers should be *16 digits* long, separated by a hyphen (-)."
        )
        return

    t1, t2 = text.split("-")
    
    # Ensure both parts of the card are exactly 16 digits
    if len(t1) != 16 or len(t2) != 16:
        await message.reply_text(
            "❌ *Incorrect format!* ❌\n\n"
            "Each card number must be exactly *16 digits* long.\n"
            "Example: `/extmv 4879176315980274-4879170021981999`"
        )
        return

    # Split the card numbers into groups
    t1_group1, t1_group2 = t1[:8], t1[8:]
    t2_group1, t2_group2 = t2[:8], t2[8:]
    
    # Generate the result based on the material inverter method
    result = ''.join(str(int(t2_group1[idx]) * int(t2_group2[idx])) for idx in range(8))
    similarity = ''.join([t1_group2[idx] if t1_group2[idx] == t2_group2[idx] else 'x' for idx in range(8)])
    extrapolated_card = f"{t1_group1}{result}{similarity}"

    # Adjust the last digit to '1' if needed
    if extrapolated_card[-1] == 'x':
        extrapolated_card = extrapolated_card[:-1] + '1'

    # Send a clean, clear result message with proper HTML formatting
    message_text = f"""
<b>🛠 MaTerialDInVerter Method - Extrapolated Card</b>

<b>Generated Card:</b> 
<code>{extrapolated_card}</code>
"""

    await message.reply_text(message_text, parse_mode="HTML")
