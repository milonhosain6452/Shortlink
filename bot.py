import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042
SHORTLINK_DOMAIN = "teraboxshortlink.hstn.me"

app = Flask(__name__)
bot = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def generate_shortlink(original_url):
    try:
        url = f"https://{SHORTLINK_DOMAIN}/api.php?url={original_url}"
        response = requests.get(url)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"


@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("👋 Welcome! Just send me a long URL and I’ll give you a shortlink.")


@bot.on_message(filters.private & filters.text)
async def shortlink_handler(_, message: Message):
    original_url = message.text.strip()
    if original_url.startswith("http"):
        await message.reply_text("🔗 Generating shortlink...")
        shortlink = generate_shortlink(original_url)
        await message.reply_text(f"✅ Your shortlink:\n{shortlink}")
    else:
        await message.reply_text("❌ Please send a valid URL starting with http or https.")


@app.route('/')
def home():
    return "Shortlink Bot is Running!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    Thread(target=run).start()


if __name__ == "__main__":
    keep_alive()
    bot.run()
