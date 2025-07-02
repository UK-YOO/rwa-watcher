
from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

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

    response = requests.post(telegram_url, json=payload)
    return {"status": "ok", "telegram_response": response.json()}

@app.route("/", methods=["GET"])
def home():
    return "RWA Watcher is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
