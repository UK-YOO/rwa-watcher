
import os
import requests
import feedparser
from flask import Flask

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
RSS_FEED_URL = os.environ.get("RSS_FEED_URL")
KEYWORDS = [k.strip().lower() for k in os.environ.get("KEYWORDS", "").split(",") if k.strip()]


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.status_code, response.text


@app.route("/")
def home():
    return "✅ 서버 정상 작동 중!"


@app.route("/test")
def test():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return "❌ 환경변수 누락!"
    code, resp = send_telegram_message("📢 테스트 알림입니다.")
    return f"📨 텔레그램 응답 코드: {code}\n응답 내용: {resp}"


@app.route("/rss-check")
def check_rss():
    if not RSS_FEED_URL or not KEYWORDS:
        return "❌ RSS 피드 URL 또는 키워드가 설정되지 않았습니다."

    feed = feedparser.parse(RSS_FEED_URL)
    matched = []

    for entry in feed.entries[:10]:  # 최신 10개만 검사
        title = entry.get("title", "").lower()
        summary = entry.get("summary", "").lower()
        link = entry.get("link", "")

        for kw in KEYWORDS:
            if kw in title or kw in summary:
                msg = f"<b>📌 키워드 감지됨:</b> {kw}\n🔗 <a href='{link}'>{entry.get('title')}</a>"
                send_telegram_message(msg)
                matched.append(kw)
                break

    if matched:
        return f"✅ {len(matched)}개 항목 전송됨."
    else:
        return "ℹ️ 키워드에 매칭되는 항목이 없습니다."


import os
port = int(os.environ.get("PORT", 8000))  # 환경변수 없을 땐 8000 fallback
app.run(host="0.0.0.0", port=port)
