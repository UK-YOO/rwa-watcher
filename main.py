from flask import Flask
import requests, os, threading, time
import feedparser

app = Flask(__name__)
sent_links = set()

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ BOT_TOKEN 또는 CHAT_ID 누락")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        res = requests.post(url, data=data)
        print("✅ 텔레그램 응답 코드:", res.status_code)
    except Exception as e:
        print("❌ 텔레그램 전송 오류:", e)

def check_feed():
    print("📡 피드 모니터링 시작")
    feed_url = os.environ.get("RSS_FEED_URL")
    keywords = os.environ.get("KEYWORDS", "").split(",")
    if not feed_url or not keywords:
        print("❌ RSS_FEED_URL 또는 KEYWORDS 누락")
        return

    while True:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                if link in sent_links:
                    continue
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    send_telegram(f"📰 새 기사 발견!\n\n📌 제목: {title}\n🔗 링크: {link}")
                    sent_links.add(link)
        except Exception as e:
            print("❌ 루프 내부 오류:", e)
        time.sleep(600)

@app.route("/")
def index():
    return "✅ 서버 정상 작동 중!"

@app.route("/test")
def test():
    send_telegram("📢 테스트 알림입니다.")
    return "✅ 테스트 메시지 전송 성공!"

# 🚨 이건 app 만들고 나서 별도로 Railway에서 실행될 때만 돌도록 분리
def start_background_thread():
    thread = threading.Thread(target=check_feed, daemon=True)
    thread.start()

# gunicorn은 여기까지만 로딩
if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=5000)
