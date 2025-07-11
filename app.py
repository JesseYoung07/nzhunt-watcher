import requests
from bs4 import BeautifulSoup
import time
import os

# === CONFIG ===
URL = "https://www.nzhuntingandshooting.co.nz/f13/"
KEYWORDS = ["leupold", "vx1", "vx2", "vx3", "FS:", "scope", "lefthand", "left hand", "lh"]
CHECK_INTERVAL = 300  # 5 minutes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(telegram_url, data=payload)

def check_site(seen_posts):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    threads = soup.select("a.title")

    new_seen_posts = seen_posts.copy()

    for thread in threads:
        title = thread.text.strip()
        link = thread.get("href")
        if not link.startswith("http"):
            link = "https://www.nzhuntingandshooting.co.nz/" + link

        if link not in seen_posts and any(k in title.lower() for k in KEYWORDS):
            message = f"🔔 <b>{title}</b>\n{link}"
            send_telegram_message(message)
            print(f"Sent alert: {title}")
            new_seen_posts.add(link)

    return new_seen_posts

print("🔄 NZHunting watcher started...")
seen_posts = set()

while True:
    seen_posts = check_site(seen_posts)
    time.sleep(CHECK_INTERVAL)
