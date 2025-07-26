import requests
from pyrogram import Client, filters

API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8164105880:AAEwU1JkpAVr2PVFbmoyvkt2csKinfsChFw"
OWNER_ID = 7383046042
API_URL = "https://www.teraboxlink.free.nf/wp-content/plugins/api-tools-plugin/includes/api.php"
API_TOKEN = "wee8waHqPfONKWLACr18j4B99nk6Y2jz"

app = Client("shortlink_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("👋 Welcome! Send me a Terabox link to shorten.")

@app.on_message(filters.text & filters.private)
async def shorten_link(client, message):
    if not message.text.startswith("https://terabox.com/s/"):
        await message.reply("❌ Please send a valid Terabox link.")
        return

    url = message.text.strip()
    params = {
        "token": API_TOKEN,
        "url": url
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()

        if "short_url" in data:
            await message.reply(f"✅ Shortened Link:\n{data['short_url']}")
        else:
            await message.reply(f"❌ Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        await message.reply(f"❌ Failed to shorten link.\nError: {str(e)}")

app.run()
