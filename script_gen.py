import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in your .env")

# Initialize client
client = OpenAI(api_key=OPENAI_KEY)

# Prompt template
TEMPLATE = """
You are a real estate expert. You are creating a script for a spoken social media post that will be read outloud.
Write a 1-2 minute long social-media update script in a warm, upbeat tone that:
• explains general CRE market news to everyday investors and professionals. Explain both the LA and National Markets.
• ends with a call-to-action similar to “Reach out with any questions!!”.
Do NOT mention sources or uncertain numbers. Ensure that this post will flow naturally for spoken language. Do not include any hashtags or emojis as this is just a script to be read aloud.
Headline: {headline}
Excerpt: {excerpt}
""".strip()

def make_script(headline: str, excerpt: str) -> str:
    prompt = TEMPLATE.format(headline=headline, excerpt=excerpt[:1500])
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",       # pick gpt version
        messages=[{"role":"user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

if __name__ == "__main__":
    # Quick smoke-test
    sample_head = "LA Office Market Sees 5% Rent Uptick"
    sample_excerpt = (
        "New leasing activity in the Los Angeles office sector rose by 5% last "
        "quarter, driven by tech and creative tenants returning to hybrid workspaces."
    )
    print(make_script(sample_head, sample_excerpt))
