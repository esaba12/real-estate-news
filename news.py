# news.py

import datetime as dt
import feedparser
from newspaper import Article
from dotenv import load_dotenv

load_dotenv()  #for api keys

# Look at past week
cutoff = dt.datetime.utcnow() - dt.timedelta(days=7)

# RSS feeds for LA & national commercial real estate
# CHANGE THESE LINKS TO CHANGE DEMOGRAPHIC
RSS_FEEDS = [
    "https://www.bisnow.com/rss/commercial-real-estate-los-angeles",
    "https://www.bisnow.com/rss/national",
    "https://www.globest.com/feeds/rss/?id=42757",   # LA
    "https://www.globest.com/feeds/rss/?id=65256",   # National
]

# Keywords to identify specific-deal stories -- ensuring market-based summary rather than deal based
DEAL_KEYWORDS = {
    "sale", "acquisition", "leased", "deal", "transaction",
    "funding", "closed", "brokered"
}

def get_weekly_articles():
    """
    Fetches all articles published in the past 7 days from the defined RSS feeds,
    excluding deal-specific stories. Returns a list of dicts:
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
                title_lower = entry.title.lower()
                if any(kw in title_lower for kw in DEAL_KEYWORDS):
                    continue
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
