from flask import Flask
import os
import requests

app = Flask(__name__)

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        return "❌ BOT_TOKEN 또는 CHAT_ID 누락"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        res = requests.post(url, data=data)
        return f"✅ 응답: {res.status_code}"
    except Exception as e:
        return f"❌ 오류: {e}"

@app.route("/")
def index():
    return "✅ 서버 정상 작동 중!"

@app.route("/test")
def test():
    return send_telegram("📢 테스트 메시지입니다.")

if __name__ == "__main__":
    app.run()
