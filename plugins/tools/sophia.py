from pyrogram import Client, filters
import re

@Client.on_message(filters.command(["extm"], ["/", "."]))
async def extrapolate(client, message):
    try:
        # Extract input after command
        input_text = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""

        # Check if the argument is empty
        if not input_text:
            await message.reply_text("❌ The argument is empty. It should be: <code>/extm num1-num2</code>")
            return

        # Validate the format of input (must match num1-num2 where both are numbers)
        if re.match(r'^\d+-\d+$', input_text):
            num1, num2 = map(int, input_text.split("-"))

            # Ensure that num1 has at least 6 digits and num2 has at least one digit
            first_number = str(num1)[:6]
            last_digit = str(num2)[-1]

            # Create the extrapolated result
            result = f"{first_number}xxxxxx{last_digit}"

            # Send the result back to the user
            await message.reply_text(f"<b>The extrapolation result is:</b>\n<code>{result}</code>")
        else:
            await message.reply_text("❌ Incorrect format. It should be: <code>/extm num1-num2</code>")

    except IndexError:
        await message.reply_text("❌ Missing argument. It should be: <code>/extm num1-num2</code>")

    except Exception as e:
        # Handle unexpected errors and provide feedback
        await message.reply_text(f"❌ An error occurred: {str(e)}")
