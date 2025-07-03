from flask import Flask
import os, requests

app = Flask(__name__)

BOT  = os.getenv("BOT_TOKEN")
CHAT = os.getenv("CHAT_ID")

def send(text):
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT, "text": text})
    return r.status_code

@app.route("/")
def ok():       return "✅ 서버 정상 작동 중!"

@app.route("/test")
def test():     return f"telegram → {send('📢 TEST OK')}"

# Railway: gunicorn main:app  →  app 객체만 필요
