import os
import re
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042
SHORTLINK_DOMAIN = "teraboxshortlink.hstn.me"

bot = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

TERABOX_REGEX = re.compile(
    r"(https?://)?(www\.)?(terabox(app|links|sharelink)?\.com|teraboxapp\.com)/[^\s]+"
)

@bot.on_message(filters.command("start"))
async def start_handler(_, msg: Message):
    await msg.reply("👋 Send me any Terabox link to get a shortlink.")

@bot.on_message(filters.private & filters.text)
async def link_handler(_, msg: Message):
    text = msg.text.strip()
    match = TERABOX_REGEX.search(text)

    if not match:
        await msg.reply("❌ Please send a valid Terabox link.")
        return

    terabox_link = match.group(0)

    await msg.reply("🔗 Generating shortlink...")

    try:
        response = requests.get(
            f"https://{SHORTLINK_DOMAIN}/redirect.php",
            params={"go": terabox_link},
            timeout=10
        )

        if response.status_code == 200 and "redirect.php?go=" in response.url:
            short_url = response.url
            await msg.reply(f"✅ Your shortlink:\n{short_url}")
        else:
            await msg.reply("⚠️ Error: Failed to get a proper shortlink response.")

    except requests.exceptions.RequestException as e:
        await msg.reply(f"⚠️ Error: {e}")

bot.run()
