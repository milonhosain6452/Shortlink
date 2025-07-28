import os
import json
import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))  # optional: only allow you to generate

DATA_FILE = "data.json"
SHORTLINK_DOMAIN = "https://teraboxlink.free.nf"  # your domain here

app = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"links": [], "generated_count": 0}, f)
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply("👋 Send me a link and I will give you a short link!")


@app.on_message(filters.text & ~filters.command(["start"]))
async def shortlink(_, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Invalid link.")
        return

    data = load_data()
    existing = next((link for link in data["links"] if link["original_url"] == url), None)
    if existing:
        short = f"{SHORTLINK_DOMAIN}/{existing['code']}"
        await message.reply(f"✅ Already shortened:\n{short}")
        return

    code = generate_code()
    data["links"].append({"original_url": url, "code": code, "clicks": 0})
    data["generated_count"] += 1
    save_data(data)

    short_url = f"{SHORTLINK_DOMAIN}/{code}"
    await message.reply(f"✅ Shortlink:\n{short_url}")


app.run()
