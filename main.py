from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
KEYWORDS = os.environ.get("KEYWORDS", "").split(",")
RSS_FEED_URLS = os.environ.get("RSS_FEED_URLS", "").split(",")

@app.route("/")
def home():
    return "RWA Watcher is running!"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "📢 새로운 알림이 도착했습니다.")
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(telegram_url, json=payload)
    return {"status": "ok"}
