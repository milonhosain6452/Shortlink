import os
import json
import string
import random
from pyrogram import Client, filters
from pyrogram.types import Message

# API credentials directly used here (as per your request)
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8303642695:AAGs0HhQo2fGNTRRVIX4APFcHq7AbpstmlI"
OWNER_ID = 7383046042

# Set your custom domain
DOMAIN = "https://teraboxlink.free.nf"

# Data file to store short links
DATA_FILE = "data.json"

# Ensure data file exists and is correctly initialized
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"links": [], "generated_count": 0}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

app = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text("👋 Send me any link, and I'll give you a shortlink.")

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_link(client, message: Message):
    link = message.text.strip()
    if not (link.startswith("http://") or link.startswith("https://")):
        await message.reply_text("❌ Please send a valid link.")
        return

    data = load_data()

    # Make sure links list exists
    if "links" not in data or not isinstance(data["links"], list):
        data["links"] = []

    # Generate short code
    code = generate_short_code()
    short_url = f"{DOMAIN}/{code}"

    # Save link
    data["links"].append({
        "original": link,
        "short": code,
        "clicks": 0
    })

    data["generated_count"] += 1
    save_data(data)

    await message.reply_text(f"✅ Your shortlink:\n{short_url}")

app.run()
