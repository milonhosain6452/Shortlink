import os
import json
import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

# Credentials
API_ID = 18088290
API_HASH = "1b06cbb45d19188307f10bcf275341c5"
BOT_TOKEN = "7628770960:AAHKgUwOAtrolkpN4hU58ISbsZDWyIP6324"

# Shortlink Webserver Domain
WEB_DOMAIN = "https://yourdomain.com"  # ✅ Change this to your domain

# Data file
DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"links": {}, "generated_count": 0}, f)

# Initialize Bot
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command Handler: /genlink <t.me/c/...> 
@app.on_message(filters.command("genlink") & filters.private)
async def genlink_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 দয়া করে একটি ভিডিও লিংক দিন:\n`/genlink <t.me/c/...>`")

    original_url = message.command[1]
    short_key = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    short_url = f"{WEB_DOMAIN}/redirect.php?go={short_key}"

    # Save to data.json
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    data['links'][short_key] = {
        "original": original_url,
        "clicks": 0
    }
    data['generated_count'] += 1
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    await message.reply(f"✅ Shortlink Generated:\n🔗 `{short_url}`", quote=True)

# Flask for Replit/Render uptime ping
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

# Start everything
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    app.run()
