from pyrogram import Client, filters
import socket
import requests

class SiteSecurityChecker:
    def __init__(self, domain):
        self.domain = domain

    async def check_ip_range(self):
        try:
            ip_addresses = socket.gethostbyname_ex(self.domain)[-1]
            return any(ip.startswith("104.") for ip in ip_addresses)
        except socket.gaierror:
            return False

    async def check_dns(self):
        try:
            resolved_ips = socket.gethostbyname_ex(self.domain)[-1]
            return any(ip.startswith(("172.", "198.", "199.")) for ip in resolved_ips)
        except socket.gaierror:
            return False

    async def is_using_cloudflare(self):
        return await self.check_ip_range() or await self.check_dns()

    async def has_captcha_protection(self):
        try:
            response = requests.get(f"http://{self.domain}")
            if "captcha" in response.text.lower():
                return "Google reCAPTCHA" if "recaptcha" in response.text.lower() else \
                    "hCaptcha" if "hcaptcha" in response.text.lower() else "Unknown CAPTCHA type"
            return "No CAPTCHA protection found on the page."
        except requests.exceptions.RequestException:
            return "Error making the request."

    async def get_server_type(self):
        try:
            response = requests.head(f"http://{self.domain}")
            server_header = response.headers.get("Server")
            return server_header if server_header else "No server information found."
        except requests.exceptions.RequestException:
            return "Error making the request."

# Initialize the bot with your API_ID and API_HASH

# Command /site
@Client.on_message(filters.command("site", prefixes="/"))
async def check_site_info(client, message):
    if len(message.command) != 2:
        await message.reply("You must provide a website after the command.")
        return

    domain = message.command[1]
    checker = SiteSecurityChecker(domain)

    cloudflare_result = "YES" if await checker.is_using_cloudflare() else "NO"
    captcha_type = await checker.has_captcha_protection()
    server_type = await checker.get_server_type()

    reply_message = f"""
    <i>Site:</i> <b>{domain}</b>
    <i>Cloudflare:</i> <b>{cloudflare_result}</b>
    <i>Captcha:</i> <b>{captcha_type}</b>
    <i>Web Server:</i> <b>{server_type}</b>"""

    await message.reply_text(reply_message)
