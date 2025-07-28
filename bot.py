import json
import string
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading
import os

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8303642695:AAGs0HhQo2fGNTRRVIX4APFcHq7AbpstmlI"
OWNER_ID = 7383046042

DOMAIN = "https://teraboxlink.free.nf"
DATA_FILE = "data.json"

# Ensure data.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"links": []}, f)

# Initialize Bot
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 Send me any link, and I'll give you a shortlink.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def handle_link(client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Invalid link.")
        return

    # Generate random slug
    slug = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    short_url = f"{DOMAIN}/{slug}"

    # Load and update data.json
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if not isinstance(data.get("links"), list):
        data["links"] = []

    data["links"].append({
        "id": slug,
        "url": url,
        "clicks": 0
    })

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    await message.reply(f"✅ Your shortlink:\n{short_url}")

# Flask app to serve redirect
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Shortlink Bot is running!"

@flask_app.route("/<slug>")
def redirect_link(slug):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    for link in data["links"]:
        if link["id"] == slug:
            link["clicks"] += 1
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
            return f"<meta http-equiv='refresh' content='0; url={link['url']}' />"

    return "❌ Invalid link."

# Run Flask in separate thread
def run():
    flask_app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run).start()

# Start the bot
app.run()
