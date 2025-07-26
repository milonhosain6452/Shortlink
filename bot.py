import json
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from fastapi import FastAPI, Request
import uvicorn
import asyncio
import os

# Bot credentials
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042
WEBHOOK_URL = "https://your-render-app-name.onrender.com"  # Render app URL দিয়ে দাও

# Token save file
TOKEN_FILE = "tokens.json"
API_ENDPOINT = "https://www.teraboxlink.free.nf/wp-content/plugins/api-tools-plugin/includes/api.php"

# FastAPI app
app = FastAPI()

# Load and Save token
def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

# Bot commands
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

# Telegram bot init
@app.on_event("startup")
async def startup_event():
    global application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settoken", settoken))
    application.add_handler(CommandHandler("gen", gen))
    
    # Set webhook
    await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

# FastAPI route to receive Telegram updates
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# Run the app
if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
