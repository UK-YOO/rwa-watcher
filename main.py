
from flask import Flask
import os
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        res = requests.post(url, data=data)
        print(f"[텔레그램 전송 결과] {res.status_code} / {res.text}")
    except Exception as e:
        print(f"[전송 오류] {e}")

@app.route("/")
def index():
    send_telegram_message("✅ 봇이 Railway에서 실행되었습니다.")
    return "봇 실행 중!"

@app.route("/test")
def test():
    send_telegram_message("✅ 테스트 호출 - 메시지 전송됨!")
    return "테스트 메시지 전송 완료!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
