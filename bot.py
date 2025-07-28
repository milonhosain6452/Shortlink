import json
import string
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

# --- Bot Credentials ---
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8303642695:AAGs0HhQo2fGNTRRVIX4APFcHq7AbpstmlI"
OWNER_ID = "7383046042"

# --- Shortlink settings ---
SHORTLINK_DOMAIN = "https://yourdomain.com"  # change to your domain
DATA_FILE = "shortlinks/data.json"

# --- Load data.json ---
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Generate random shortcode ---
def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# --- Bot setup ---
app = Flask(__name__)
bot = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/")
def home():
    return "✅ Bot is running!"

@bot.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("👋 Send me any link, and I'll give you a shortlink.")

@bot.on_message(filters.text & ~filters.command(["start"]))
def shortlink_handler(client, message: Message):
    original_url = message.text.strip()
    if not original_url.startswith("http"):
        message.reply("❌ Invalid URL")
        return

    data = load_data()

    # Check if already shortened
    for shortcode, info in data["links"].items():
        if info["url"] == original_url:
            shortlink = f"{SHORTLINK_DOMAIN}/{shortcode}"
            message.reply(f"🔗 Shortlink: {shortlink}")
            return

    # Generate new shortlink
    shortcode = generate_shortcode()
    data["links"][shortcode] = {
        "url": original_url,
        "clicks": 0
    }
    data["generated_count"] += 1
    save_data(data)

    shortlink = f"{SHORTLINK_DOMAIN}/{shortcode}"
    message.reply(f"✅ Shortlink generated:\n{shortlink}")

# --- Flask runner ---
def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

# --- Start bot ---
bot.run()
