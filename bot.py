import json
import requests
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from keep_alive import keep_alive

# Bot credentials
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

# Render will auto-provide this environment variable
WEBHOOK_HOST = os.environ.get("RENDER_EXTERNAL_URL", "https://your-backup-url.com").strip("/")

# Token save file
TOKEN_FILE = "tokens.json"

# API Endpoint
API_ENDPOINT = "https://www.teraboxlink.free.nf/wp-content/plugins/api-tools-plugin/includes/api.php"

# Token loader/saver
def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /gen <terabox_link> to shorten your link.\n\n"
        "🔐 Only owner can update API token using /settoken"
    )

async def settoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /settoken <your_token>")
        return

    token = context.args[0]
    tokens = load_tokens()
    tokens[str(OWNER_ID)] = token
    save_tokens(tokens)
    await update.message.reply_text("✅ Token saved successfully.")

async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tokens = load_tokens()

    if user_id not in tokens:
        await update.message.reply_text("⚠️ No API token found. Only the owner can set it using /settoken.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /gen <terabox_link>")
        return

    url = context.args[0]
    token = tokens[user_id]
    api_url = f"{API_ENDPOINT}?token={token}&url={url}"

    try:
        response = requests.get(api_url)
        result = response.text

        if "http" in result:
            await update.message.reply_text(f"✅ Generated Link:\n{result}")
        else:
            await update.message.reply_text(f"❌ Error: {result}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to fetch shortlink.\nError: {e}")

# MAIN run
if __name__ == "__main__":
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settoken", settoken))
    app.add_handler(CommandHandler("gen", gen))

    webhook_url = f"{WEBHOOK_HOST}/webhook/{BOT_TOKEN}"
    print(f"Setting webhook to: {webhook_url}")
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=webhook_url
    )
