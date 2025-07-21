import os
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import re
import requests

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

app = Flask(__name__)

bot = Client(
    "TeraBoxShortLinkBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

TERABOX_PATTERN = r"https?://(?:1024terabox\.com|terafileshare\.com)/s/[a-zA-Z0-9\-_]+"
SHORT_API = "http://teraboxshortlink.com/9dDtqLnTx?url={}"

user_data = {}

# ---------- Start Command ----------
@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply_text(
        "✅ Bot is running.\n\nUse /help to see available commands."
    )

# ---------- Help & Feature ----------
@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message: Message):
    await message.reply_text(
        "/start - Check if bot is alive\n"
        "/api <your_api_link>\n"
        "/add_channel <channel_link>\n"
        "/footer <your footer>\n"
        "/unlink\n/remove_channel\n/remove_footer\n"
        "/features - Show all features\n"
        "/link - How to link API"
    )

@bot.on_message(filters.command("features") & filters.private)
async def features_cmd(client, message: Message):
    await message.reply_text("🔗 Converts terabox links\n📝 Keeps original text\n👤 Owner-only")

@bot.on_message(filters.command("link") & filters.private)
async def link_cmd(client, message: Message):
    await message.reply_text("Send: /api <API link>\nExample:\n/api http://teraboxshortlink.com/9dDtqLnTx")

# ---------- Settings ----------
@bot.on_message(filters.command("api") & filters.user(OWNER_ID))
async def set_api(client, message: Message):
    try:
        user_data["api"] = message.text.split(None, 1)[1]
        await message.reply_text("✅ API saved.")
    except:
        await message.reply_text("⚠️ Usage:\n/api <your_api_link>")

@bot.on_message(filters.command("add_channel") & filters.user(OWNER_ID))
async def set_channel(client, message: Message):
    try:
        user_data["channel"] = message.text.split(None, 1)[1]
        await message.reply_text("✅ Channel link saved.")
    except:
        await message.reply_text("⚠️ Usage:\n/add_channel <channel_link>")

@bot.on_message(filters.command("footer") & filters.user(OWNER_ID))
async def set_footer(client, message: Message):
    try:
        user_data["footer"] = message.text.split(None, 1)[1]
        await message.reply_text("✅ Footer saved.")
    except:
        await message.reply_text("⚠️ Usage:\n/footer <your_footer>")

# ---------- Unlink Commands ----------
@bot.on_message(filters.command("unlink") & filters.user(OWNER_ID))
async def unlink_api(client, message: Message):
    user_data.pop("api", None)
    await message.reply_text("❌ API removed.")

@bot.on_message(filters.command("remove_channel") & filters.user(OWNER_ID))
async def remove_channel(client, message: Message):
    user_data.pop("channel", None)
    await message.reply_text("❌ Channel link removed.")

@bot.on_message(filters.command("remove_footer") & filters.user(OWNER_ID))
async def remove_footer(client, message: Message):
    user_data.pop("footer", None)
    await message.reply_text("❌ Footer removed.")

# ---------- Message Handler ----------
@bot.on_message(filters.private & filters.user(OWNER_ID))
async def replace_links(client, message: Message):
    if "api" not in user_data:
        await message.reply_text("⚠️ First, set your API using /api")
        return

    matches = re.findall(TERABOX_PATTERN, message.text or "")
    if not matches:
        await message.reply_text("❌ No valid terabox links found.")
        return

    updated_text = message.text
    for link in matches:
        short_link = requests.get(user_data["api"] + f"?url={link}").text
        updated_text = updated_text.replace(link, short_link.strip())

    if "footer" in user_data:
        updated_text += f"\n\n{user_data['footer']}"

    await message.reply_text(updated_text)

# ---------- Flask Dummy Server ----------
@app.route('/')
def home():
    return "TeraBox ShortLink Bot is running!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: bot.run()).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
