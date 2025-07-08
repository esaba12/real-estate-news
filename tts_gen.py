# tts_gen.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()  

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

if not API_KEY:
    raise RuntimeError("Set ELEVENLABS_API_KEY in .env")

def gen_audio(text: str, out_path="voice.wav") -> str:
    """
    Generates a WAV file using ElevenLabs TTS API.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/wav",
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5", # change model as desired, v2 is default for quick and cheap english generation
        "voice_settings": {
            "stability": 0.5, #adjust as needed
            "similarity_boost": 0.7 #adjust as needed
        }
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()  # will raise if something went wrong

    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path

if __name__ == "__main__":
    sample = "Testing our new voice clone via direct API call!"
    path = gen_audio(sample, "voice.wav")
    print(f"Saved audio to {path}")
