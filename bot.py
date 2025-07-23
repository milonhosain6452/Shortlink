import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread

# --- API Config ---
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042
SHORTLINK_DOMAIN = "teraboxshortlink.hstn.me"

# --- Flask Web Server for Render.com keepalive ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Pyrogram Bot Setup ---
bot = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    await message.reply_text("👋 Welcome! Send me a Terabox link and I will generate a shortlink.")

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def shortlink_handler(client, message: Message):
    url = message.text.strip()

    if "terabox" not in url:
        await message.reply_text("❌ Please send a valid Terabox link.")
        return

    await message.reply_text("🔗 Generating shortlink...")

    try:
        res = requests.get(f"https://{SHORTLINK_DOMAIN}/api.php?url={url}")
        shortlink = res.text.strip()

        if "http" in shortlink:
            await message.reply_text(f"✅ Your shortlink:\n{shortlink}")
        else:
            await message.reply_text(f"⚠️ Error: {shortlink}")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

# --- Start ---
keep_alive()
bot.run()
