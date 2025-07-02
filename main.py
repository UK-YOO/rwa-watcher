from flask import Flask
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ 서버 정상 작동 중!"

@app.route("/test")
def test():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    message = "✅ 테스트 알림입니다."

    if not token or not chat_id:
        return "❌ 환경변수 누락!"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    r = requests.post(url, data=data)

    return f"텔레그램 응답 코드: {r.status_code}"