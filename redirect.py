from flask import Flask, redirect
import json

app = Flask(__name__)
DATA_FILE = "data.json"

@app.route("/<code>")
def shortlink(code):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    links = data.get("links", {})
    info = links.get(code)

    if not info:
        return "Invalid or expired link.", 404

    url = info.get("original")
    if not url:
        return "Invalid or expired link.", 404

    # Update click count
    info["clicks"] = info.get("clicks", 0) + 1
    data["links"][code] = info

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return redirect(url)

@app.route("/")
def home():
    return "🔗 Terabox Shortlink Bot is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
