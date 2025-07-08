import os
import sys
import time
import schedule
from news import get_weekly_articles
from script_gen import make_market_update
from tts_gen import gen_audio

OUTPUT_DIR = "ready_to_post"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# makes all calls to find articles and generate final audio

# allows pipeline to run on demand
def run_consolidated_pipeline():
    """
    Fetch weekly articles, generate a consolidated market update script,
    and produce a single WAV audio file.
    """
    articles = get_weekly_articles() # pull articles
    print(f"Using {len(articles)} market-style articles.\n")
    script = make_market_update(articles) # build the script
    print("Generated combined script:\n")
    print(script, "\n")

    out_path = os.path.join(OUTPUT_DIR, "market_update.wav")
    print("Generating audio…")
    gen_audio(script, out_path=out_path) # generate audio
    print(f"✅ Saved audio to {out_path}")

# allows pipeline to run on a schedule
def schedule_weekly(day: str = "monday", time_str: str = "09:00"): # adjust timing here 
    """
    Schedule the pipeline to run weekly on the specified day and time.
    Usage: schedule_weekly('monday', '09:00')
    """
    # Dynamically get schedule.every().<day>()
    job = getattr(schedule.every(), day).at(time_str).do(run_consolidated_pipeline)
    print(f"Scheduled weekly run: every {day.capitalize()} at {time_str}")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Usage:
    #   python3 audio_pipeline.py             # runs immediately
    #   python3 audio_pipeline.py --schedule  # schedules Monday at 09:00
    #   python3 audio_pipeline.py --schedule tuesday 10:30

# if arguments given, set to custom schedule based on arguments
# otherwise, default to every Monday at 9am
    if len(sys.argv) > 1 and sys.argv[1] in ("--schedule", "-s"): 
        day = sys.argv[2].lower() if len(sys.argv) >= 3 else "monday"
        time_str = sys.argv[3] if len(sys.argv) >= 4 else "09:00"
        schedule_weekly(day, time_str)
    else:
        run_consolidated_pipeline()
