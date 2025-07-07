# cre_posts/news.py
import datetime as dt
import feedparser
from newspaper import Article
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

# Find news within the week
cutoff = dt.datetime.utcnow() - dt.timedelta(days=7)

RSS_FEEDS = [
    "https://www.bisnow.com/rss/commercial-real-estate-los-angeles",
    "https://www.bisnow.com/rss/national",
    "https://www.globest.com/feeds/rss/?id=42757",   # LA news
    "https://www.globest.com/feeds/rss/?id=65256",   # national news
]

def fetch_weekly_articles():
    print(f"\nFetching articles since {cutoff.isoformat()} UTC\n")
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = dt.datetime(*entry.published_parsed[:6])
            if published >= cutoff:
                art = Article(entry.link)
                art.download(); art.parse()
                print(f"- {entry.title} ({published.date()})\n  {entry.link}\n")

# Schedule once a week (Monday at 09:00 for now)
schedule.every().monday.at("09:00").do(fetch_weekly_articles)

if __name__ == "__main__":
    # Run immediately once, then enter schedule
    fetch_weekly_articles()
    while True:
        schedule.run_pending()
        time.sleep(60)
