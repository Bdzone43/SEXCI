from pyrogram import Client, filters

@Client.on_message(filters.command(["exti"], prefixes=["/", "."]))
async def logical_indentation_method(client, message):
    text = message.text[len("/exti "):]
    
    # Check if the input follows the correct format
    if not text.isdigit() or len(text) != 16:
        await message.reply_text(
            "🚨 *Incorrect format!* 🚨\n\n"
            "Please ensure you are using the correct format:\n"
            "/exti 4915110176928790\n\n"
            "The card number should be exactly *16 digits* long and consist of only numeric characters."
        )
        return

    # Split the card number into different parts
    bin, rest = text[:6], text[6:]
    group1, group2, group3 = rest[:3], rest[3:7], rest[7:]

    # Apply logical indentation to the second group
    group2 = f"{group2[0]}xx{group2[3]}"

    # Construct the extrapolated card
    extrapolated_card = f"{bin}{group1}{group2}{group3}"

    # Send the result
    await message.reply_text(
        f"🔍 *Logical Indentation Method Result:* 🔍\n\n"
        f"🔢 Extrapolated Card: `{extrapolated_card}`\n\n"
        "🔒 This is a *masked* version of the card number for security purposes."
    )
