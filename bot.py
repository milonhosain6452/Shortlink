import os
import logging
import requests
from pyrogram import Client, filters
from flask import Flask
import threading

# Telegram Bot Credentials
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

# Shortlink API Info
SHORTLINK_API = "04e8ee10b5f123456a640c8f33195abc"
BASE_URL = "https://teraboxshortlink.hstn.me"

# Logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Pyrogram Client
bot = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route('/')
def home():
    return "Bot is running!"

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Welcome! Send me a long URL to generate a shortlink.")

@bot.on_message(filters.private & filters.text)
async def generate_shortlink(client, message):
    try:
        long_url = message.text.strip()
        response = requests.get(f"{BASE_URL}/api", params={"api": SHORTLINK_API, "url": long_url})
        data = response.json()

        if data["status"] == "success":
            short = data["shortenedUrl"]
            await message.reply_text(f"✅ Shortlink created:\n{short}")
        else:
            await message.reply_text(f"❌ Failed: {data.get('message', 'Unknown error')}")
    except Exception as e:
        await message.reply_text(f"⚠️ Error occurred:\n{e}")

# Threaded Flask App
def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run()
