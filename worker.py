import os, time, requests
import feedparser

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
        print("✅ 응답:", res.status_code)
    except Exception as e:
        print("❌ 오류:", e)

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
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    send_telegram(f"📰 새 기사!\n📌 {title}\n🔗 {link}")
                    sent_links.add(link)
        except Exception as e:
            print("❌ 피드 체크 오류:", e)
        time.sleep(600)

if __name__ == "__main__":
    check_feed()
