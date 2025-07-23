import logging
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, API_TOKEN, BASE_URL

logging.basicConfig(level=logging.INFO)

app = Client("shortlink-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "👋 Welcome! Just send me a **long link** and I will return a **shortened link** using your custom shortlink site."
    )

@app.on_message(filters.text & ~filters.command(["start"]))
async def shorten_link(client, message: Message):
    long_url = message.text.strip()

    try:
        response = requests.post(
            f"{BASE_URL}/api",
            params={"api": API_TOKEN, "url": long_url}
        )
        data = response.json()

        if data.get("status") == "success":
            short_link = data.get("shortenedUrl") or data.get("short")
            await message.reply_text(f"🔗 Shortened Link:\n{short_link}")
        else:
            await message.reply_text(f"❌ Error: {data.get('message')}")
    except Exception as e:
        await message.reply_text("⚠️ Something went wrong. Please try again later.")
        logging.error(e)

app.run()
