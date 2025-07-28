import os
import json
import string
import random
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

DATA_FILE = "data.json"
DOMAIN = "https://teraboxlink.free.nf/"  # শর্টলিংক ডোমেইন শেষ / দিয়ে শেষ করতে হবে

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"links": {}, "generated_count": 0}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

bot = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start(_, msg: Message):
    await msg.reply("👋 Send me a link and I will give you a short link!")

@bot.on_message(filters.private & filters.text)
async def shorten(_, msg: Message):
    url = msg.text.strip()
    if not url.startswith("http"):
        await msg.reply("❌ Invalid URL!")
        return

    data = load_data()

    # Check if link already exists
    for code, info in data["links"].items():
        if info.get("original") == url:
            short_url = f"{DOMAIN}{code}"
            await msg.reply(f"🔗 Short Link: {short_url}")
            return

    # New code
    code = generate_code()
    while code in data["links"]:
        code = generate_code()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["links"][code] = {
        "original": url,
        "clicks": 0,
        "created": now
    }
    data["generated_count"] = data.get("generated_count", 0) + 1

    save_data(data)
    short_url = f"{DOMAIN}{code}"
    await msg.reply(f"✅ Short Link Created:\n\n🔗 {short_url}")

# --- Flask Server for Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Shortlink Bot is Running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run()
