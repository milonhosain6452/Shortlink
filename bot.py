from pyrogram import Client, filters
from pyrogram.types import Message
import re
import os

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

# Storage for user settings
user_data = {}

# Regex to find terabox links
TERABOX_REGEX = r"(https:\/\/(?:1024terabox\.com|terafileshare\.com)\/s\/[a-zA-Z0-9\-_]+)"

# Start bot
app = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text(
        "🤖 Bot is **alive** and working!\n\nSend a message containing Terabox links to convert them."
    )


@app.on_message(filters.command("features") & filters.user(OWNER_ID))
async def features(client, message: Message):
    await message.reply_text(
        "**📌 Available Commands:**\n\n"
        "`/api <shortlink>` - Set your shortlink API\n"
        "`/unlink` - Remove your API\n"
        "`/add_channel <channel link>` - Set your channel link\n"
        "`/remove_channel` - Remove channel link\n"
        "`/footer <text>` - Set footer text\n"
        "`/remove_footer` - Remove footer\n"
        "`/link` - Show your current API\n"
        "`/help` - How to use this bot\n"
    )


@app.on_message(filters.command("api") & filters.user(OWNER_ID))
async def set_api(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Send: `/api http://yourshortener.com/xxxxx`")
    user_data["api"] = message.command[1]
    await message.reply_text("✅ API saved successfully!")


@app.on_message(filters.command("unlink") & filters.user(OWNER_ID))
async def unlink_api(client, message: Message):
    user_data.pop("api", None)
    await message.reply_text("✅ API removed!")


@app.on_message(filters.command("add_channel") & filters.user(OWNER_ID))
async def add_channel(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Send: `/add_channel https://t.me/yourchannel`")
    user_data["channel"] = message.command[1]
    await message.reply_text("✅ Channel saved!")


@app.on_message(filters.command("remove_channel") & filters.user(OWNER_ID))
async def remove_channel(client, message: Message):
    user_data.pop("channel", None)
    await message.reply_text("✅ Channel removed!")


@app.on_message(filters.command("footer") & filters.user(OWNER_ID))
async def set_footer(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Send: `/footer your footer text here`")
    user_data["footer"] = " ".join(message.command[1:])
    await message.reply_text("✅ Footer saved!")


@app.on_message(filters.command("remove_footer") & filters.user(OWNER_ID))
async def remove_footer(client, message: Message):
    user_data.pop("footer", None)
    await message.reply_text("✅ Footer removed!")


@app.on_message(filters.command("link") & filters.user(OWNER_ID))
async def show_api(client, message: Message):
    if "api" in user_data:
        await message.reply_text(f"🔗 Current API: `{user_data['api']}`")
    else:
        await message.reply_text("❌ No API set.")


@app.on_message(filters.command("help") & filters.user(OWNER_ID))
async def help_msg(client, message: Message):
    await message.reply_text("📩 Just send me any post with terabox links, I will replace those with your shortlinks!")


@app.on_message(filters.private & ~filters.command(["start", "api", "unlink", "footer", "remove_footer", "add_channel", "remove_channel", "features", "link", "help"]))
async def handle_post(client, message: Message):
    if "api" not in user_data:
        return await message.reply_text("❗ Please set your API first using `/api` command.")

    matches = re.findall(TERABOX_REGEX, message.text or "")
    if not matches:
        return

    new_text = message.text
    for link in matches:
        short = f"{user_data['api']}/{os.urandom(6).hex()}"
        new_text = new_text.replace(link, short)

    # Add footer if exists
    if "footer" in user_data:
        new_text += f"\n\n{user_data['footer']}"

    # Send updated post
    await message.reply_text(new_text, disable_web_page_preview=True)

app.run()
