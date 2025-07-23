import os
import re
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

SHORTLINK_API_TOKEN = "04e8ee10b5f123456a640c8f33195abc"
SHORTLINK_DOMAIN = "teraboxshortlink.hstn.me"

app = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def create_shortlink(original_url):
    api_url = f"https://{SHORTLINK_DOMAIN}/api"
    params = {
        "api": SHORTLINK_API_TOKEN,
        "url": original_url
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if "shortenedUrl" in data:
            return data["shortenedUrl"]
        elif "shortened" in data:
            return data["shortened"]
        else:
            return data.get("message", "❌ Unknown error occurred while shortening.")
    except Exception as e:
        return f"⚠️ Error: {e}"


@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        "**🧿 Terabox ShortLink Generator Bot 🧿**\n\n"
        "✅ Just send me any Terabox link and I will return the shortlink instantly!\n\n"
        "__Powered by @YourVideoss_bot__"
    )


@app.on_message(filters.command("short") & filters.user(OWNER_ID))
async def short_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: `/short <terabox_link>`", quote=True)
    
    link = message.text.split(None, 1)[1]
    if not re.match(r'https?://', link):
        return await message.reply_text("❗ Please provide a valid URL starting with http:// or https://")

    await message.reply_text("⏳ Generating shortlink, please wait...")
    short_url = create_shortlink(link)
    await message.reply_text(f"🔗 Shortlink: `{short_url}`", disable_web_page_preview=True)


@app.on_message(filters.regex(r"https?://.*terabox\.com") & filters.user(OWNER_ID))
async def auto_shortlink_handler(client, message: Message):
    links = re.findall(r"https?://[^\s]+", message.text)
    response = ""
    for link in links:
        short = create_shortlink(link)
        response += f"\n🔗 `{short}`"
    
    if response:
        await message.reply_text(f"✅ Shortened Links:\n{response}", quote=True)
    else:
        await message.reply_text("⚠️ No valid Terabox link found.", quote=True)


app.run()
