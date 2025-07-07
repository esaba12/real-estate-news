# audio_pipeline.py
import os
from datetime import datetime
from news import get_weekly_articles
from script_gen import make_script
from tts_gen import gen_audio

OUTPUT_DIR = "ready_to_post"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(s: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in s)[:50]

def run_audio_pipeline():
    
    articles = get_weekly_articles() #pull articles
    print(f"Found {len(articles)} articles to process.\n")
    for art in articles: #parse articles
        title = art["title"]
        date = art["published"][:10]  # formatted as YYYY-MM-DD
        excerpt = art["text"][:300]
        script = make_script(title, excerpt)

        slug = sanitize_filename(title)
        filename = f"{date}__{slug}.wav"
        out_path = os.path.join(OUTPUT_DIR, filename)

        print(f"→ Generating audio for '{title}'")
        gen_audio(script, out_path=out_path) #generate tts 
        print(f"   saved: {out_path}\n")

if __name__ == "__main__":
    run_audio_pipeline()
