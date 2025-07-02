from flask import Flask
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def index():
    return "봇이 실행 중입니다."

@app.route("/send")
def send_message():
    message = "✅ 텔레그램 봇이 정상적으로 메시지를 전송합니다."
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    return response.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)