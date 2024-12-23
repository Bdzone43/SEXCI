import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("ip"))
async def cmds(client, message):
    try:
        # Extract IP from message
        zipcode = message.text[len('/ip '):]
        
        # Check if the IP was provided
        if not zipcode:
            await message.reply("<b>⎚ Please use the command in this format: <code>/ip 1.1.1.1</code></b>")
            return

        # Request headers to mimic browser behavior
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        # Request to ipwho.is API
        response = requests.get(f'http://ipwho.is/{zipcode}', headers=headers, verify=False).json()
        
        # Extract relevant data from response
        ip = response.get('ip', '')
        flag = response.get('flag', {}).get('emoji', '')
        connection = response.get('connection', {})
        timezone = response.get('timezone', {})

        # Check for missing information and handle gracefully
        if not ip:
            await message.reply("<b>❌ Invalid IP address or unable to fetch details. Please try again.</b>")
            return

        # Prepare the response message
        response_text = f"""<b>
IP Information:
━━━━━━━━━━━━━━
IP: <code>{ip}</code> ✅
Country/Region: <code>{timezone.get('id', 'N/A')} {flag}</code>
ISP: <code>{connection.get('isp', 'N/A')}</code>
Organization: <code>{connection.get('org', 'N/A')}</code>
Domain: <code>{connection.get('domain', 'N/A')}</code>
Timezone: <code>{timezone.get('abbr', 'N/A')} ({timezone.get('utc', 'N/A')})</code>
Current Time: <code>{timezone.get('current_time', 'N/A')}</code>

Checked by: @{message.from_user.username}
━━━━━━━━━━━━━━
</b>"""
        await message.reply(response_text, parse_mode="HTML")
    
    except Exception as e:
        await message.reply("<b>❌ An error occurred while processing the request. Please try again later.</b>")
        print(f"Error: {str(e)}")
