from flask import Flask
import os, threading, time, requests
import feedparser

app = Flask(__name__)
sent_links = set()

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ BOT_TOKEN 또는 CHAT_ID 누락")
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(url, data={"chat_id": chat_id, "text": message})
        print("✅ 텔레그램 응답:", res.status_code)
    except Exception as e:
        print("❌ 전송 오류:", e)

def check_feed():
    feed_url = os.environ.get("RSS_FEED_URL")
    keywords = os.environ.get("KEYWORDS", "").split(",")
    if not feed_url or not keywords:
        print("❌ 환경변수 누락")
        return
    while True:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                if link in sent_links:
                    continue
                if any(k.lower() in title.lower() for k in keywords):
                    send_telegram(f"📰 새 기사 발견!\n📌 {title}\n🔗 {link}")
                    sent_links.add(link)
        except Exception as e:
            print("❌ 피드 파싱 오류:", e)
        time.sleep(600)

@app.route("/")
def index():
    return "✅ 서버 정상 작동 중!"

@app.route("/test")
def test():
    send_telegram("📢 테스트 알림입니다.")
    return "✅ 테스트 메시지 전송 성공!"

def start_background():
    thread = threading.Thread(target=check_feed)
    thread.daemon = True
    thread.start()

def create_app():
    start_background()
    return app

app = create_app()
