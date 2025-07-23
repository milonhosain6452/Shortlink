import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

SHORTLINK_API_TOKEN = os.getenv("SHORTLINK_API_TOKEN")
SHORTLINK_DOMAIN = os.getenv("SHORTLINK_DOMAIN")

bot = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    await message.reply_text("👋 Welcome! Send /short <link> to generate a shortlink.")

@bot.on_message(filters.command("short") & filters.private)
async def generate_shortlink(_, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ You are not authorized to use this bot.")

    if len(message.command) < 2:
        return await message.reply_text("❗️Please provide a URL.\n\nUsage: /short <link>")

    original_url = message.text.split(None, 1)[1]

    try:
        api_url = f"https://{SHORTLINK_DOMAIN}/api"
        response = requests.post(api_url, json={
            "api": SHORTLINK_API_TOKEN,
            "url": original_url
        })

        result = response.json()
        if result["status"] == "success":
            short_url = result["data"]["shortenedUrl"] if "shortenedUrl" in result["data"] else result["data"]["url"]
            await message.reply_text(f"✅ Shortlink created:\n{short_url}")
        else:
            await message.reply_text(f"❌ Failed: {result['message']}")

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {str(e)}")

bot.run()
