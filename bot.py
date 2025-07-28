import os
import json
import string
import random
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------------- CONFIG ----------------
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8303642695:AAGs0HhQo2fGNTRRVIX4APFcHq7AbpstmlI"
OWNER_ID = 7383046042
BASE_URL = "https://teraboxlink.free.nf"
DATA_FILE = "data.json"

# ---------------- FLASK SERVER (for Render) ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# ---------------- PYROGRAM BOT ----------------
bot = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize data.json if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"links": []}, f)

# Load data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Generate unique short code
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# /start command
@bot.on_message(filters.command("start") & filters.private)
async def start(_, msg: Message):
    await msg.reply("👋 Send me any link, and I'll give you a shortlink.")

# Link handler
@bot.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_link(_, msg: Message):
    user_id = msg.from_user.id
    if user_id != OWNER_ID:
        await msg.reply("🚫 Only the owner can generate links.")
        return

    url = msg.text.strip()
    if not url.startswith("http"):
        await msg.reply("❌ Please send a valid link.")
        return

    short_code = generate_code()
    data = load_data()
    data["links"].append({
        "code": short_code,
        "url": url,
        "clicks": 0
    })
    save_data(data)

    short_link = f"{BASE_URL}/?id={short_code}"
    await msg.reply(f"✅ Shortlink generated:\n{short_link}")

# ---------------- START BOTH FLASK + BOT ----------------
if __name__ == "__main__":
    import threading
    def run_flask():
        app.run(host="0.0.0.0", port=10000)  # Port can be 10000 for Render

    threading.Thread(target=run_flask).start()
    bot.run()
