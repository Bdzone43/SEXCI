import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("rand"))
async def rand_check(client, message):
    try:
        # Fetch random user data from the API
        response = requests.get('https://randomuser.me/api/1.2/?nat=US')

        # Log the raw response text to inspect what we get
        print(f"Raw API Response: {response.text}")

        # Try parsing the response as JSON
        try:
            data = response.json()  # Attempt to parse the JSON response
        except ValueError:
            await message.reply("<b>❌ Failed to parse the API response. It may not be valid JSON.</b>")
            return

        # Ensure the data is structured as expected
        if 'results' not in data or not data['results']:
            await message.reply("<b>❌ Failed to fetch user data or no results found.</b>")
            return

        # Extract information from the response (make sure to index 'results' correctly)
        user = data['results'][0]  # Accessing the first user in the results list

        first = user['name']['first']
        last = user['name']['last']
        email = user['email']
        street = user['location']['street']
        city = user['location']['city']
        state = user['location']['state']
        postcode = user['location']['postcode']
        phone = user['phone']
        cell = user['cell']
        username = user['login']['username']
        password = user['login']['password']
        gender = user['gender']
        dob = user['dob']['date']
        ssn = user.get('id', {}).get('value', 'null')
        country = user['nat']

        # Format the response message
        response_message = f"""<b>Ϟ RAND INFO GENERATOR</b>
        Ϟ FIRST NAME: <code>{first}</code>
        Ϟ LAST NAME: <code>{last}</code>
        Ϟ EMAIL: <code>{email}</code>
        Ϟ ADDRESS: <code>{street}</code>
        Ϟ CITY: <code>{city}</code>
        Ϟ STATE: <code>{state}</code>
        Ϟ POSTCODE: <code>{postcode}</code>
        Ϟ PHONE: <code>{phone}</code>
        Ϟ CELL: <code>{cell}</code>
        Ϟ USERNAME: <code>{username}</code>
        Ϟ PASSWORD: <code>{password}</code>
        Ϟ GENDER: <code>{gender}</code>
        Ϟ DOB: <code>{dob}</code>
        Ϟ SSN: <code>{ssn}</code>
        Ϟ COUNTRY: <code>{country}</code>"""

        # Send the response message to the user
        await message.reply(response_message)

        # Log the response (optional)
        log_msg = f"RAND INFO:\nFirst Name: {first}\nLast Name: {last}\nChecked by: @{message.from_user.username}"
        log_chat_id = "1190070178"  # Log chat ID (replace with actual)
        log_data = {
            "chat_id": log_chat_id,
            "text": log_msg
        }
        requests.get(f"https://api.telegram.org/botYOUR_BOT_API_TOKEN/sendMessage", params=log_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        await message.reply("<b>❌ An error occurred while processing the request.</b>")
