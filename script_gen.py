# script_gen.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in your .env")

client = OpenAI(api_key=OPENAI_KEY)

# Market‐update prompt
def make_market_update(articles: list[dict]) -> str:
    """
    Given a list of filtered articles, returns a ~200–300 word
    market update script (1–2 min).
    """
    bullets = []
    for art in articles:
        first_sent = art["text"].split(".")[0]
        bullets.append(f"- {art['title']}: {first_sent}.")
    bullets_text = "\n".join(bullets)

    prompt = f"""
You are a commercial-real-estate market analyst. 
Here are recent headlines (Los Angeles + national), excluding specific deals:
{bullets_text}

Write a 300-400 word spoken update (about 2-3 minutes) that:
• Summarizes overall market trends and data (rents, vacancy, investment sentiment)
• Speaks in a warm, professional tone
• Ends with a call-to-action, e.g. “If you’d like deeper insights, DM me!”
Do NOT mention individual transactions or deal details. Ensure that this post will flow naturally for spoken language. Do not include any hashtags or emojis as this is just a script to be read aloud.
""".strip()

    resp = client.chat.completions.create(
        # gpt parameters, adjust as needed
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


if __name__ == "__main__":
    # Quick test of consolidated update
    from news import get_weekly_articles
    articles = get_weekly_articles()
    print(make_market_update(articles))
