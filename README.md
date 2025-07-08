# Real Estate Market Update Bot

A Python-based tool to automate weekly commercial real estate (CRE) market updates for social media. On each run, the program:

1. **Fetches** the last 7 days of CRE headlines (default: Los Angeles + national markets) from RSS feeds, filtering out articles about specific deals (sales, leases, acquisitions, etc.) to ensure the post is about general market status.
2. **Generates** a 200–300 word market summary script in a warm, professional tone (1–2 minute spoken update) using an OpenAI ChatGPT model (default: GPT-3.5-turbo).
3. **Produces** a voiceover WAV using a cloned voice via ElevenLabs TTS.
4. **Saves** paired files with timestamps in `ready_to_post/`:
   - `market_update_<YYYYMMDD_HHMMSS>.txt` (the script)
   - `market_update_<YYYYMMDD_HHMMSS>.wav` (the audio)
5. **Runs** either on-demand or on a weekly schedule (default: Monday at 09:00).

---

## Prerequisites

- **macOS or Linux** (Windows supported with minor tweaks)
- **Python 3.10+**
- **Git**
- **Homebrew** *(macOS only)* to install system libraries:
  ```bash
  brew install libxml2 libxslt ffmpeg
  ```
- **API keys** in a `.env` file at project root:
  ```env
  OPENAI_API_KEY=sk-xxx
  ELEVENLABS_API_KEY=elevenlabs_sk-xxx
  ELEVENLABS_VOICE_ID=<your-elevenlabs-voice-uuid>
  ```

---

## Installation

```bash
# 1. Clone the repo
git clone git@github.com:<your-user>/real-estate-news.git
cd real-estate-news

# 2. Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate    # Windows PowerShell: .\.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install --upgrade pip
pip install \
  feedparser newspaper3k python-dotenv schedule \
  openai tiktoken requests \
  lxml_html_clean beautifulsoup4 html5lib
```

---

## Configuration

1. Create a `.env` file in the project root with your API keys (see Prerequisites).
2. Verify your keys are loading correctly:

```bash
python3 - <<EOF
import os
from dotenv import load_dotenv
load_dotenv()
print(
  os.getenv('OPENAI_API_KEY'),
  os.getenv('ELEVENLABS_API_KEY'),
  os.getenv('ELEVENLABS_VOICE_ID')
)
EOF
```

---

## Usage

### Manual Run

```bash
python3 audio_pipeline.py
```

- Fetches & filters last week’s headlines.
- Generates a consolidated market-summary script.
- Saves files like:
  ```
  ready_to_post/market_update_<YYYYMMDD_HHMMSS>.txt
  ready_to_post/market_update_<YYYYMMDD_HHMMSS>.wav
  ```

### Schedule Weekly

Default (Monday at 09:00):

```bash
python3 audio_pipeline.py --schedule
```

Custom day/time (e.g., Tuesday at 10:30):

```bash
python3 audio_pipeline.py --schedule tuesday 10:30
```

Press **Ctrl+C** to stop the scheduler.

---

## Directory Structure

```
real-estate-news/
├── news.py            # Fetch & filter RSS articles
├── script_gen.py      # OpenAI script generation
├── tts_gen.py         # ElevenLabs TTS module
├── audio_pipeline.py  # Orchestrator (manual & scheduled)
├── ready_to_post/     # Output: timestamped .txt & .wav files
├── .env               # API keys (gitignored)
└── README.md          # This documentation
```

---

## User Adjustment Guide

All details of the program can be adjusted depending on the user's needs:

**News Feed** can be swapped under `news.py` in the RSS\_FEEDS section. This allows one to change news sources depending on preferences such as market location.\
**Avoided Keywords** can be removed/changed in `news.py` under DEAL\_KEYWORDS. This allows for news about specific recent deals or to narrow/broaden the topics that will be reported on.\
**Models Used** are easily changed. The ElevenLabs speech generation model can be changed in `tts_gen.py` under `model_id`. The GPT text generation model can be changed in `script_gen.py` under `model`.\
**Model Parameters** may be tweaked for both the speech and text generation models. All text-to-speech parameters and adjustments can be found in `tts_gen.py`, and all text generation parameters can be edited in `script_gen.py`.

---

## Next Steps

- **Video**: integrate D-ID or SadTalker for talking-head clips.
- **Posting**: automate uploads via APIs or an n8n workflow.

