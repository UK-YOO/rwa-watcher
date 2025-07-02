import os
import requests
import feedparser
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
KEYWORDS = [kw.strip().lower() for kw in os.getenv("KEYWORDS", "").split(",")]
RSS_FEED_URL = os.getenv("RSS_FEED_URL")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running", 200

@app.route("/notify", methods=["POST"])
def notify():
    try:
        data = request.get_json()
        title = data.get("title", "No title")
        summary = data.get("summary", "")
        link = data.get("link", "")

        message = f"📢 *{title}*\n{summary}\n{link}"
        send_telegram(message)
        return "Message sent", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def check_feed():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        title = entry.title.lower()
        summary = entry.summary.lower()
        if any(keyword in title or keyword in summary for keyword in KEYWORDS):
            message = f"📡 *{entry.title}*\n{entry.link}"
            send_telegram(message)
            break

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
