# Real Estate Market Update Bot

A Python-based tool to automate weekly commercial real estate (CRE) market updates for social media. On each run, the program:

1. **Fetches** the last 7 days of CRE headlines (default is Los Angeles + national markets) from RSS feeds, filtering out articles about specific deals (sales, leases, acquisitions, etc.) to ensure the post is about general market status.
2. **Generates** a 200–300 word market summary script in a warm, professional tone (1–2 minute spoken update) using an OpenAI ChatGPT model (default is GPT 3.5 turbo).
3. **Produces** a voiceover WAV using a cloned voice via ElevenLabs TTS.
4. **Saves** audio (`.wav`) in a file under a folder named `ready_to_post/`.
5. **Runs** either on-demand or on a weekly schedule (default: Monday at 09:00).

---

## Prerequisites

- **macOS or Linux** (Windows will work with minor path adjustments)
- **Python 3.10 or later+**
- **Git**
- **Homebrew** (for macOS) to install system libs:
  ```bash
  brew install libxml2 libxslt ffmpeg
  ```
- **API keys** saved in a `.env` file:
  ```env
  OPENAI_API_KEY=sk-xxx
  ELEVENLABS_API_KEY=elevenlabs_sk-xxx
  ELEVENLABS_VOICE_ID=<your-elevenlabs-voice-uuid>
  ```

## Installation

```bash
# 1. Clone the repo
git clone git@github.com:<your-user>/real-estate-news.git
cd real-estate-news

# 2. Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# 3. Install Python dependencies
pip install --upgrade pip
pip install \
  feedparser newspaper3k python-dotenv schedule \
  openai tiktoken requests \
  lxml_html_clean beautifulsoup4 html5lib
```

## Configuration

1. Create a `.env` file in the project root with your keys (example above).
2. Verify your `.env` is loaded by running:
   ```bash
   python3 - <<EOF
   ```

import os; from dotenv import load\_dotenv load\_dotenv(); print(os.getenv('OPENAI\_API\_KEY'), os.getenv('ELEVENLABS\_API\_KEY')) EOF

````

## Usage

### Manual Run

```bash
python3 audio_pipeline.py
````

- Fetches and filters headlines.
- Builds consolidated market summary.
- Saves `ready_to_post/market_update.wav`.

### Schedule Weekly

Default (Monday 09:00):

```bash
python3 audio_pipeline.py --schedule
```

Custom day/time (e.g., Tuesday 10:30):

```bash
python3 audio_pipeline.py --schedule tuesday 10:30
```

Press **Ctrl+C** to stop the scheduler.

## Directory Structure

```
real-estate-news/
├── news.py            # RSS fetch & filter
├── script_gen.py      # OpenAI script functions
├── tts_gen.py         # ElevenLabs TTS module
├── audio_pipeline.py  # Runs pipeline on-demand or scheduled
├── ready_to_post/     # Outputs: timestamped .txt & .wav files
├── .env               # API keys (gitignored)
└── README.md          # This documentation
```
## User Adjustment Guide

All details of the program can be adjusted depending on the user's needs:

**News Feed** can be swapped under `news.py` in the RSS_FEEDS section. This allows one to change news sources depending on preferences such as market location.
**Avoided Keywords** can be removed/changed in `news.py` under DEAL_KEYWORDS. This allows for news about specific recentl deals or to narrow/broaden the topics that will be reported on.
**Models Used** are easily changed. The Elevenlabs speech generation model can be changed in `tts_gen.py` under `model_id`. The GPT text generation model can be changed in `script_gen.py` under `model`. 
**Model Parameters** may be tweaked for both the speech and text generation models. All text-to-speech parameters and adjustments can be found in `tts_gen.py`, and all text generation parameters can be editted in `script_gen.py`.

## Next Steps

- **Video**: integrate D-ID or SadTalker for talking-head clips.
- **Posting**: automate uploads via APIs or an n8n workflow.


