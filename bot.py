# bot.py
import json
import requests
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

# Token save file
TOKEN_FILE = "tokens.json"

# Website API Endpoint
API_ENDPOINT = "https://www.teraboxlink.free.nf/wp-content/plugins/api-tools-plugin/includes/api.php"

# Function: Load all tokens
def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function: Save tokens
def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /gen <terabox_link> to shorten your link.\n\n"
        "🔐 Only owner can update API token using /settoken"
    )

# Command: /settoken (owner only)
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

# Command: /gen <link>
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

# Run the bot
if __name__ == "__main__":
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settoken", settoken))
    app.add_handler(CommandHandler("gen", gen))

    print("🤖 Bot is running...")
    app.run_polling()
