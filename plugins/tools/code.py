import aiohttp
import asyncio
import uuid
import random
import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Predefined list of available themes for the code image.
AVAILABLE_THEMES = [
    "3024-night", "a11y-dark", "blackboard", "base16-dark", "base16-light", 
    "cobalt", "dracula", "duotone-dark", "duotone-light", "hopscotch",
    "lucario", "material", "monokai", "night-owl", "nord", "oceanic-next",
    "one-light", "one-dark", "panda-syntax", "paraiso-dark", "seti",
    "shades-of-purple", "solarized", "solarized-light", "synthwave-84",
    "twilight", "verminal", "yeti", "zenburn"
]

# Constants for the external API endpoint and header.
CARBONARA_API_URL = "https://carbonara.solopov.dev/api/cook"
CONTENT_TYPE_HEADER = {'Content-Type': 'application/json'}

async def generate_code_image(code: str) -> str:
    """Generate a code image from the provided code using an external API."""
    unique_id = str(uuid.uuid4())
    random_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    random_theme = random.choice(AVAILABLE_THEMES)

    payload = {
        'code': code,
        'backgroundColor': random_color,
        'theme': random_theme,
        'watermark': False,
        'name': f'carbon_{unique_id}.png'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CARBONARA_API_URL, json=payload) as response:
            if response.status != 200:
                raise Exception("Failed to generate code image.")

            content = await response.read()
            filename = f'carbon_{unique_id}.png'
            with open(filename, 'wb') as file:
                file.write(content)

    return filename, unique_id

async def send_code_image(client, message: Message, filename: str, unique_id: str):
    """Send the generated code image to the user."""
    try:
        sent_message = await message.reply_document(filename)
        await message.reply_text(f"Your code image is ready: {sent_message.document.file_name}")
    finally:
        os.remove(filename)

        # Cleanup: delete any previous identical images to avoid clutter.
        async for media in client.search_messages(chat_id=message.chat.id, query=f'carbon_{unique_id}.png'):
            if media.document and media.document.file_name == filename:
                await client.delete_messages(chat_id=message.chat.id, message_ids=media.message_id)

async def handle_code_image_request(client, message: Message):
    """Handle the command to convert code into an image."""
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply_text("<b>It must be used on text.</b>\nExample:\n<code>/code</code> (replying to a message containing code)")

    code = message.reply_to_message.text
    try:
        loading_message = await message.reply_text("<b>Loading image...</b>")
        filename, unique_id = await generate_code_image(code)
        await send_code_image(client, message, filename, unique_id)
    except Exception as error:
        await message.reply_text(f"Error: {str(error)}")
    finally:
        await loading_message.delete()

@Client.on_message(filters.command('code') & (filters.reply | filters.text))
async def code_to_image(client: Client, message: Message):
    """Command handler to convert code into an image."""
    await handle_code_image_request(client, message)
