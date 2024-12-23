from pyrogram import Client, filters

@Client.on_message(filters.command(["exta"], prefixes=["/", "."]))
async def extrapolate_advanced(client, message):
    text = message.text[len("/exta "):]
    
    # Check if the input follows the correct format
    if '-' not in text:
        await message.reply_text(
            "🚨 *Incorrect format!* 🚨\n\n"
            "Please use the following format:\n"
            "/exta 4115680117164577-4178490024082621\n\n"
            "Ensure that both card numbers are 16 digits long, separated by a hyphen (-)."
        )
        return

    t1, t2 = text.split("-")
    
    # Try to perform the calculations
    try:
        t1_group2_sum = int(t1[7]) + int(t1[8])
        t2_group2_sum = int(t2[7]) + int(t2[8])
    except IndexError:
        await message.reply_text(
            "❗️ *Card numbers are too short.*\n\n"
            "Please ensure both card numbers are exactly 16 digits long and formatted correctly."
        )
        return

    # Calculate results
    t1_result = int((t1_group2_sum / 2) * 5)
    t2_result = int((t2_group2_sum / 2) * 5)
    total_result = t1_result + t2_result
    
    # Format the extrapolated card
    extrapolated_card = f"{t1[:7]} {total_result:03d}xx xxxx"

    # Send the result
    await message.reply_text(
        f"🔍 *Advanced Extrapolation Result:* 🔍\n\n"
        f"🔢 Extrapolated Card: `{extrapolated_card}`\n\n"
        "🔒 This is a *masked* version of the card number for security purposes."
    )
