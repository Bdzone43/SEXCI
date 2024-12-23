from pyrogram import Client, filters
from deep_translator import GoogleTranslator
from langdetect import detect

def translate_message_to_language(text, dest_language):
    source_language = detect(text)
    try:
        translated_text = GoogleTranslator(source=source_language, target=dest_language).translate(text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def get_language_code(language_name):
    return language_name

def get_language_name(language_code):
    return language_code

@Client.on_message(filters.command(["trad"], ["/", "."]))
async def translate_message(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        text_to_translate = message.reply_to_message.text
    else:
        text_to_translate = " ".join(message.command[1:])

    if not text_to_translate:
        await message.reply_text("Please include a message to translate.")
        return

    if detect(text_to_translate) == 'en':
        await message.reply_text("Sorry, the message is already in English, I can't translate it.")
        return

    if len(message.command) >= 3:
        dest_language = get_language_code(message.command[1])
        text_to_translate = " ".join(message.command[2:])
    else:
        dest_language = "en"

    translated_text = translate_message_to_language(text_to_translate, dest_language)

    if translated_text is None:
        await message.reply_text("An error occurred during translation.")
        return

    source_language = detect(text_to_translate)
    source_language_name = get_language_name(source_language)
    dest_language_name = get_language_name(dest_language)

    response_text = f"""
    Translation ({source_language_name} ➜ {dest_language_name}): 
{translated_text}"""
    await message.reply_text(response_text)
