import asyncio
import traceback
from configs import Config
from pyrogram import Client

# Callback query handler
@Client.on_callback_query()
async def callback_privates(client, callback_query):
    try:
        # Add specific debugging for callback queries
        print(f"Received callback query: {callback_query.data}")
        # Your callback query handling code here
    except Exception as e:
        print(f"Error in callback query: {e}")
        traceback.print_exc()  # Print the full traceback for debugging

async def main():
    bot = Client(
        "shades",
        api_hash=Config.API_HASH,
        api_id=Config.API_ID,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="plugins"),
    )

    try:
        print("Bot is starting...")

        # Start the client
        await bot.start()
        print("Bot started successfully!")

        # Keep the bot running
        while True:
            print("Bot is running...")
            await asyncio.sleep(60)  # Check every 60 seconds

    except Exception as e:
        print(f"Error in main: {e}")
        # Log the traceback for detailed error information
        traceback.print_exc()

    finally:
        try:
            if bot.is_initialized:
                await bot.stop()
                print("Bot has been stopped successfully.")
            else:
                print("Bot was not initialized properly.")
        except Exception as stop_error:
            print(f"Error while stopping the bot: {stop_error}")
            traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot terminated by user.")
    except Exception as final_error:
        print(f"Unhandled exception in __main__: {final_error}")
        traceback.print_exc()
