from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading
import os
import random
import string

# ----------------- API CONFIG -----------------
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

# ----------------- BOT INIT -----------------
bot = Client(
    "short_link_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ----------------- SHORT LINK GENERATOR -----------------
def generate_short_link(original_url):
    random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"https://short.link/{random_id}"  # Replace with your own domain if needed

# ----------------- COMMANDS -----------------

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    await message.reply_text(
        "👋 Welcome to the Short Link Bot!\n\n"
        "🔗 Send /short <your_link> to get a short version.\n"
        "ℹ️ Use /api to get API access.\n"
        "❓ Use /help for help."
    )

@bot.on_message(filters.command("help") & filters.private)
async def help(_, message: Message):
    await message.reply_text(
        "🆘 **Help Menu**\n\n"
        "• `/short <link>` - Get a short link.\n"
        "• `/api` - Learn how to use API.\n"
        "• `/start` - Check if bot is running.\n\n"
        "👨‍💻 Developer: @YourUsername"
    )

@bot.on_message(filters.command("api") & filters.private)
async def api(_, message: Message):
    await message.reply_text(
        "🧠 **Short Link API Usage**:\n\n"
        "`https://yourdomain.com/api?url=YOUR_LINK`\n\n"
        "Example:\n`https://yourdomain.com/api?url=https://google.com`\n\n"
        "🔐 Replace `yourdomain.com` with your own domain or IP."
    )

@bot.on_message(filters.command("short") & filters.private)
async def short(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a link!\nUsage: /short https://example.com")
        return
    original_link = message.text.split(None, 1)[1]
    short_link = generate_short_link(original_link)
    await message.reply_text(
        f"✅ Here is your short link:\n\n🔗 {short_link}"
    )

# ----------------- FLASK SERVER FOR RENDER -----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is Alive!"

# ----------------- RUN -----------------
if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))),
        daemon=True
    ).start()

    bot.run()
