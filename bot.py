import os
import json
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from flask import Flask, request

# Bot credentials
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042

# Website API Endpoint
API_ENDPOINT = "https://www.teraboxlink.free.nf/wp-content/plugins/api-tools-plugin/includes/api.php"
TOKEN_FILE = "tokens.json"

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()


def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /gen <terabox_link> to shorten your link.\n\n"
        "🔐 Only owner can update API token using /settoken"
    )

# /settoken command
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

# /gen command
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


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("settoken", settoken))
telegram_app.add_handler(CommandHandler("gen", gen))


# Flask route for Telegram Webhook
@app.route("/")
def home():
    return "🤖 Bot is alive!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "OK"


if __name__ == "__main__":
    import asyncio

    # Set webhook URL
    WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"

    async def run():
        await telegram_app.bot.delete_webhook(drop_pending_updates=True)
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        await telegram_app.initialize()
        await telegram_app.start()

    asyncio.run(run())
    app.run(host="0.0.0.0", port=8080)
