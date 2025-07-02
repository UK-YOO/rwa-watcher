from flask import Flask
import requests, os, threading, time
import feedparser

app = Flask(__name__)

# 중복 전송 방지를 위한 링크 캐시
sent_links = set()

@app.route("/")
def index():
    return "✅ 서버 정상 작동 중!"

@app.route("/test")
def test():
    send_telegram("📢 테스트 알림입니다.")
    return "✅ 테스트 메시지 전송 성공!"

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❌ 텔레그램 전송 오류:", e)

def check_feed():
    try:
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
                    if any(keyword.lower() in title.lower() for keyword in keywords):
                        send_telegram(f"📰 새 기사 발견!\n\n📌 제목: {title}\n🔗 링크: {link}")
                        sent_links.add(link)
            except Exception as e:
                print("❌ 루프 내부 에러:", e)

            time.sleep(600)
    except Exception as e:
        print("❌ check_feed 전체 에러:", e)

        time.sleep(600)  # 10분마다 반복

# 백그라운드 루프 시작
def start_background():
    thread = threading.Thread(target=check_feed)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_background()
    app.run(host="0.0.0.0", port=5000)
