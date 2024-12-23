from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import cursor

@Client.on_message(filters.command(["cmds", "start"], ["/", "."]))
async def cmds_command(client, message):
    user_id = message.from_user.id
    query = f"SELECT username, status, expiration_date, creditos FROM users WHERE user_id='{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        await client.send_message(message.chat.id, "You are not registered. Please use /register to register.")
        return

    video_path = "https://tenor.com/view/steff-hello-there-skull-smoke-art-gif-17940128"
    caption = """
<b>Hello, my name is Skull Chk. It is a pleasure to meet you. Press the buttons below to know more about me.</b>"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📿 Tools", callback_data="tools"),
                InlineKeyboardButton("📿 Gateways", callback_data="gates"),
            ],
            [
                InlineKeyboardButton("📿 Profile", callback_data="me"),
            ]
        ]
    )

    await client.send_video(message.chat.id, video_path, caption=caption, reply_markup=keyboard, reply_to_message_id=message.id)

@Client.on_callback_query()
async def handle_buttons(client, callback_query):
    data = callback_query.data
    message = callback_query.message
    chat_id = message.chat.id
    user_id = callback_query.from_user.id

    query = f"SELECT username, status, expiration_date, creditos FROM users WHERE user_id='{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        await client.send_message(message.chat.id, "You are not registered. Please use /register to register.")
        return

    if result:
        rank, expiration, creditos = result[1], result[2], result[3]
    else:
        rank, expiration, creditos = None, None, None

    if data == "tools":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                    InlineKeyboardButton("Close", callback_data="cerrar"),
                    InlineKeyboardButton("→", callback_data="siguiente"),
                ],
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
🔍 **Command**: `/bin`
   🌐 *Example* : `/bin 531260`
   📌 Retrieve detailed insights for a BIN.

🛠️ **Command**: `/gen`
   🌐 *Example* : `/gen 531260`
   📌 Generate custom data from a BIN.

🎲 **Command**: `/rand`
   🌐 *Example* : `/rand US`
   📌 Get location-specific random data.

🔒 **Command**: `/ip`
   🌐 *Example*: `/ip`
   📌 Explore details of an IP address.

🌐 **Command**: `/site`
   🌐 *Example* : `/site Google.com`
   📌 Fetch insights on a website.

🔍 **Command**: `/extra`
   🌐 *Example* : `/extra bin`
   📌 Deeper into BIN functionalities.

📜 **Command**: `/code`
   🌐 *Example* : `/code reply to some text`
   📌 Transform text into a unique code.
""", reply_markup=keyboard)

    if data == "siguiente":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="tools"),
                    InlineKeyboardButton("Close", callback_data="cerrar"),
                ],
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""

📛 **Command**: `/exta`
   🌐 *Example*: `/exta 4115680117164577-4178490024082621`
   📌 Extrapolate Advance.

📛 **Command**: `/extb`
   🌐 *Example*: `/extb 4115680117164577`
   📌 Extrapolate Basic.

📛 **Command**: `/exti`
   🌐 *Example*: `/exti 4115680117164577`
   📌 View individual card information.

📛 **Command**: `/exts`
   🌐 *Example*: `/exts 4115680117164577-4178490024082621`
   📌 Get summarized data for multiple cards.

📛 **Command**: `/extmv`
 🌐 *Example*: `/extmv 4879176315980274-4879170021981999`
 📌 Extrapolate multiple cards .
 
📛 **Command**: `/sk`
   🌐 *Example*: `/sk sk_live_xxxx`
   📌 Search Status of Stripe Keys.
""", reply_markup=keyboard)

    elif data == "cerrar":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📿 Open Back", callback_data="back"),
                ],
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="", reply_markup=keyboard)

    elif data == "principio":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📿 Tools", callback_data="tools"),
                    InlineKeyboardButton("📿 Gateways", callback_data="gates"),
                ],
                [
                    InlineKeyboardButton("📿 Profile", callback_data="me"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
<b>Hello, my name is Skull Chk. It is a pleasure to meet you. Press the buttons below to know more about me.</b>""", reply_markup=keyboard)

    elif data == "back":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📿 Tools", callback_data="tools"),
                    InlineKeyboardButton("📿 Gateways", callback_data="gates"),
                ],
                [
                    InlineKeyboardButton("📿 Profile", callback_data="me"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
<b>Hello, My Name is Skull Chk. It is a pleasure to meet you. Press the buttons below to know more about me.</b>""", reply_markup=keyboard)

    elif data == "gates":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Auth", callback_data="auth"),
                    InlineKeyboardButton("Charged", callback_data="charged"),
                ],
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""


🔹 **Available Gates**:
   • Auth: 3
   • Charger: 3

⏳ More gates will be added soon...
""", reply_markup=keyboard)

    elif data == "back1":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Auth", callback_data="auth"),
                    InlineKeyboardButton("Charged", callback_data="charged"),
                ],
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
🔵 Available Gates:
- Auth: 3
- Charger: 3
""", reply_markup=keyboard)

    elif data == "auth":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back1"),
                    InlineKeyboardButton("Close", callback_data="cerrar"),
                ],
                [
                    InlineKeyboardButton("Home", callback_data="principio"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
🔹 **Gateway Elucidator** [Free]:
   • Format: `/el cc|mm|yyyy|cvv`
   • Gateway: Braintree
   • Status: ✅ ON

🔹 **Gateway Skull** [Free]:
   • Format: `/azu cc|mm|yyyy|cvv`
   • Gateway: Stripe CCN
   • Status: ✅ ON

🔹 **Gateway Ki** [Free]:
   • Format: `/ki cc|mm|yyyy|cvv`
   • Gateway: Stripe auth
   • Status: ❌ OFF""", reply_markup=keyboard)

    elif data == "charged":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back1"),
                    InlineKeyboardButton("Close", callback_data="cerrar"),
                ],
                [
                    InlineKeyboardButton("Home", callback_data="principio"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
🔹 **Gateway Angie** [Premium]
- Format: `/an cc|mm|yyyy|cvv`
- Gateway: Stripe charged
- Status: ✅ ON

🔹 **Gateway Lopus** [Free]
- Format: `/lo cc|mm|yyyy|cvv`
- Gateway: Stripe charged
- Status: ✅ ON

🔹 **Gateway Paypal** [Free]
- Format: `/pp cc|mm|yyyy|cvv`
- Gateway: Paypal charged 0.1$
- Status: ✅ ON

🔹 **Gateway Ayleen** [Free]
- Format: `/ay cc|mm|yyyy|cvv`
- Gateway: Shopify
- Status: ❌ OFF
""", reply_markup=keyboard)

    elif data == "me":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption=f"""
♻️ **Profile Information**

⚜️ **User Details**:
   • ID: `<code>{user_id}</code>`
   • Rank: `<code>{rank}</code>`

📛 **Expiration Information**:
   • Expiry Date: `<code>{expiration}</code>`

🔑 **Credits**:
   • Available: `<code>{creditos}</code>`
""", reply_markup=keyboard)

    elif data == "sk":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ]
            ]
        )

        await client.edit_message_caption(chat_id, message.id, caption="""
🔍 **Command**: `/sk`
   🌐 *Example*: `/sk keyword`
   📌 Search for information related to the provided keyword.
""", reply_markup=keyboard)
