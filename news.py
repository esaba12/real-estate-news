# news.py

import datetime as dt
import feedparser
from newspaper import Article
from dotenv import load_dotenv

load_dotenv()  #for api keys

# Look back one week
cutoff = dt.datetime.utcnow() - dt.timedelta(days=7)

# RSS feeds for LA & national commercial real estate
# edit these links to change location feed
RSS_FEEDS = [
    "https://www.bisnow.com/rss/commercial-real-estate-los-angeles",
    "https://www.bisnow.com/rss/national",
    "https://www.globest.com/feeds/rss/?id=42757",   # LA
    "https://www.globest.com/feeds/rss/?id=65256",   # National
]

def get_weekly_articles():
    """
    Fetches all articles published in the past 7 days from the defined RSS feeds.
    Returns a list of dicts:
      [{
         "title": str,
         "text": str,
         "url": str,
         "published": ISO8601 timestamp
       }, ...]
    """
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = dt.datetime(*entry.published_parsed[:6])
            if published >= cutoff:
                art = Article(entry.link)
                art.download()
                art.parse()
                articles.append({
                    "title": entry.title,
                    "text": art.text,
                    "url": entry.link,
                    "published": published.isoformat()
                })
    return articles

if __name__ == "__main__":
    for a in get_weekly_articles():
        date = a["published"][:10]
        print(f"- {a['title']} ({date})\n  {a['url']}\n")
