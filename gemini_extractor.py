import json
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]


def extract_speakers(page_text):

    page_text = page_text[:120000]

    prompt = f"""
Extract all conference speakers.

Return ONLY valid JSON.

[
  {{
    "full_name": "",
    "affiliation": ""
  }}
]

Do not include:
- organizers
- committee members
- sponsors

TEXT:

{page_text}
"""

    last_error = None

    for model in MODELS:

        print(f"Trying model: {model}")

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            return json.loads(text)

        except Exception as e:

            print(f"{model} failed")

            last_error = e

            time.sleep(3)

    raise last_error
