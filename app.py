import os
import sqlite3
from flask import Flask, request, redirect, render_template, jsonify
import secrets
from urllib.parse import urlparse

app = Flask(__name__)

# ডাটাবেস পাথ (Render-ফ্রেন্ডলি)
db_path = '/tmp/database.db'

# টেলিগ্রাম বটের ক্রেডেনশিয়াল (আপনার দেওয়া)
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8303642695:AAGs0HhQo2fGNTRRVIX4APFcHq7AbpstmlI"
OWNER_ID = 7383046042

# Adsterra AD URL (আপনার দেওয়া)
AD_URL = "https://www.profitableratecpm.com/wdwn7wjiy?key=f8f5344e7390639ff8c5563ee357acf8"

# ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            short_code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# র্যান্ডম শর্টকোড জেনারেটর
def generate_short_code(length=6):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(secrets.choice(chars) for _ in range(length))

# হোমপেজ
@app.route('/')
def index():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(clicks) FROM links")
        total_links, total_clicks = cursor.fetchone()
        total_clicks = total_clicks or 0
        
        cursor.execute("SELECT * FROM links")
        links = cursor.fetchall()
        conn.close()
        
        return render_template('index.html', 
                            total_links=total_links,
                            total_clicks=total_clicks,
                            links=links)
    except Exception as e:
        return f"Error: {str(e)}", 500

# শর্ট লিঙ্ক জেনারেটর
@app.route('/generate', methods=['POST'])
def generate_short_link():
    try:
        original_url = request.form.get('original_url', '').strip()
        
        if not original_url:
            return "Error: URL is empty!", 400
        
        parsed = urlparse(original_url)
        if not parsed.scheme or not parsed.netloc:
            return "Error: Invalid URL!", 400
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT short_code FROM links WHERE original_url = ?", (original_url,))
        existing = cursor.fetchone()
        
        if existing:
            short_code = existing[0]
        else:
            short_code = generate_short_code()
            cursor.execute("INSERT INTO links (short_code, original_url) VALUES (?, ?)", 
                         (short_code, original_url))
            conn.commit()
        
        conn.close()
        
        short_url = f"{request.host_url}{short_code}"
        return jsonify({
            "original_url": original_url,
            "short_url": short_url
        })
    except Exception as e:
        return f"Error: {str(e)}", 500

# রিডাইরেক্ট
@app.route('/<short_code>')
def redirect_to_original(short_code):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT original_url FROM links WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()
        
        if not result:
            return "Invalid or expired link!", 404
        
        original_url = result[0]
        
        cursor.execute("UPDATE links SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
        conn.commit()
        conn.close()
        
        return render_template('redirect.html', 
                            final_url=original_url,
                            ad_url=AD_URL)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
