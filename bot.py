import os
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread
import re

API_ID = int(os.getenv("22134923"))
API_HASH = os.getenv("d3e9d2f01d3291e87ea65298317f86b8")
BOT_TOKEN = os.getenv("8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw")
OWNER_ID = int(os.getenv("7383046042"))

app = Flask(__name__)
bot = Client("TeraBoxBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

SHORTLINK_DOMAIN = "https://teraboxshortlink.hstn.me/redirect.php?go="

@app.route('/')
def home():
    return "✅ TeraBox Shortlink Bot is Running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def shortlink_handler(client, message: Message):
    text = message.text.strip()

    # Match terabox link
    match = re.search(r'(https?://teraboxapp\.com/s/[\w\d]+)', text)
    if not match:
        await message.reply("❌ Invalid link. Please send a valid TeraBox link like:\n`https://teraboxapp.com/s/xxxx`")
        return

    file_code = match.group(1).split("/")[-1]
    short_url = f"{SHORTLINK_DOMAIN}{file_code}"
    
    await message.reply(f"🔗 **Your Shortlink:**\n{short_url}")

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply("👋 Welcome to TeraBox Shortlink Bot!\n\nJust send me a TeraBox link, and I’ll give you a shortlink.")

keep_alive()
bot.run()
