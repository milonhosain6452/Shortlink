import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
SHORTLINK_DOMAIN = "teraboxshortlink.hstn.me"

bot = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("👋 Send me a Terabox link and I’ll return a shortlink.")

@bot.on_message(filters.private & filters.text)
async def generate_shortlink(client, message: Message):
    original_link = message.text.strip()
    if not original_link.startswith("http") or "terabox" not in original_link:
        await message.reply("❌ Please send a valid Terabox link.")
        return

    await message.reply("🔗 Generating shortlink...")

    try:
        res = requests.get(
            f"https://{SHORTLINK_DOMAIN}/redirect.php",
            params={"go": original_link},
            timeout=10
        )

        if res.status_code == 200 and "redirect.php?go=" in res.url:
            await message.reply(f"✅ Your shortlink:\n{res.url}")
        else:
            await message.reply("⚠️ Failed to generate shortlink. Try again later.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")

bot.run()
