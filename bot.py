import os
import json
import string
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

# টেলিগ্রাম বট Config
API_ID = int(os.getenv("API_ID", "22134923"))
API_HASH = os.getenv("API_HASH", "d3e9d2f01d3291e87ea65298317f86b8")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8303642695:AAGs0HhQo2fGNTRRVIX4APFcHq7AbpstmlI")

# শর্টলিংক Config
BASE_URL = os.getenv("BASE_URL", "https://teraboxlink.free.nf")  # ex: https://short.example.com
DATA_FILE = "data.json"

# Pyrogram Bot Setup
bot = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask Web App
app = Flask(__name__)

# ডেটা লোড/সেভ ফাংশন
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"links": [], "generated_count": 0}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# শর্টকোড জেনারেটর
def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# /start command
@bot.on_message(filters.command("start"))
async def start_command(_, message: Message):
    await message.reply("👋 Send me any link, and I'll give you a shortlink.")

# মূল শর্টলিংক ফাংশন
@bot.on_message(filters.text & ~filters.command("start"))
async def handle_link(_, message: Message):
    original_link = message.text.strip()
    if not original_link.startswith("http"):
        await message.reply("❌ Please send a valid URL starting with http/https.")
        return

    data = load_data()
    shortcode = generate_shortcode()

    data["links"].append({
        "code": shortcode,
        "url": original_link,
        "clicks": 0
    })
    data["generated_count"] += 1
    save_data(data)

    short_url = f"{BASE_URL}/?r={shortcode}"
    await message.reply(f"✅ Shortlink: {short_url}")

# Flask root route for UptimeRobot
@app.route('/')
def home():
    return "Bot is Alive!"

# Flask background thread
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Start everything
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run()
