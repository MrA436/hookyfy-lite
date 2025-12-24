import os
import time
import random
import requests
import re
from dotenv import load_dotenv

load_dotenv()

# ---------- Secret Loader ----------
def get_secret(key):
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key)

# ---------- Secrets ----------
MISTRAL_API_KEY = get_secret("OPENAI_API_KEY")
DEEPSEEK_API_KEY = get_secret("OPENAI_API_KEY_2")

# ---------- Config ----------
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
    "HTTP-Referer": "https://hookyfy-lite.streamlit.app/",
    "X-Title": "HookyFY Lite",
}

# ---------- Output Validation ----------
def is_valid_output(text: str) -> bool:
    if not text:
        return False

    blocks = [b.strip() for b in text.split("---") if b.strip()]
    valid = 0

    for block in blocks:
        if (
            "Hook:" in block
            and "Conclusion:" in block
            and "Caption:" in block
        ):
            valid += 1

    return valid >= 1


# ---------- Core API Call (network + rate-limit safe) ----------
def call_openrouter(topic, api_key, model):
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = f"Bearer {api_key}"

    data = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": (
                f"Topic: {topic}\n\n"

                "You write short Instagram Reels.\n"
                "Your task is to surface a thought the viewer already has but avoids admitting.\n\n"

                "Produce EXACTLY 3 sets.\n"
                "Each set must feel like one complete realization that can hold attention.\n\n"

                "Sections:\n"
                "For each set, choose a DIFFERENT section at random from:\n"
                "Power, Curiosity, Shock, Relatable, Motivation\n"
                "Do not repeat a section in the same response.\n\n"

                "CRITICAL FORMAT RULE:\n"
                "The section name MUST be written in parentheses immediately after the word 'Hook'.\n"
                "Do NOT write the section anywhere else.\n\n"

                "Structure (FOLLOW EXACTLY):\n"
                "Hook(<Section Name>): <text>\n"
                "Conclusion: <text>\n"
                "Caption: <text>\n"
                "CTA: <text>\n\n"

                "Length guidelines:\n"
                "- Hook text: 5–9 words (do not exceed 9)\n"
                "- Conclusion: 4–7 words\n"
                "- Caption: 2–3 short sentences\n"
                "- CTA: very short\n\n"

                "Hook rules:\n"
                "- Sounds like inner dialogue\n"
                "- Describes a real behavior or state\n"
                "- Recognition first, not accusation\n"
                "- Includes slight friction or edge\n"
                "- Includes progression or contrast\n"
                "- Calm and composed, not reactive\n"
                "- Simple, everyday language\n"
                "- One clear idea only\n\n"

                "Conclusion rules:\n"
                "- Direct continuation of the hook\n"
                "- States a clear cost, outcome, or loss\n"
                "- Feels final and inevitable\n"
                "- Calm, detached, settled in tone\n"
                "- No analysis or explanation\n"
                "- No commands or advice\n\n"

                "Caption rules:\n"
                "- Plain description of the situation\n"
                "- Include the topic phrase exactly once\n"
                "- No motivation, coaching, or hype\n"
                "- Do not repeat hook or conclusion wording\n"
                "- Leave the loop open\n\n"

                "CTA rules:\n"
                "- Minimal and neutral\n"
                "- Not urgent\n"
                "- Not instructional\n\n"

                "Writing constraints:\n"
                "- Use only common, human language\n"
                "- No metaphors or poetic abstraction\n"
                "- No shouting or dramatic language\n\n"

                "Output EXACTLY 3 sets in this format:\n"
                "---\n"
                "Hook(<Section Name>): ...\n"
                "Conclusion: ...\n"
                "Caption: ...\n"
                "CTA: ...\n"
                "---\n"
                "Hook(<Section Name>): ...\n"
                "Conclusion: ...\n"
                "Caption: ...\n"
                "CTA: ...\n"
                "---\n"
                "Hook(<Section Name>): ...\n"
                "Conclusion: ...\n"
                "Caption: ...\n"
                "CTA: ...\n"
                "---\n"
            ),
        }
    ],
    "temperature": 1.0,
    "top_p": 0.92,
    "frequency_penalty": 0.35,
    "presence_penalty": 0.55,
    "max_tokens": 900,
}


    MAX_NETWORK_RETRIES = 3

    for attempt in range(MAX_NETWORK_RETRIES):
        try:
            response = requests.post(
                ENDPOINT,
                headers=headers,
                json=data,
                timeout=25,
            )

            if response.status_code == 429:
                txt = response.text.lower()

                # upstream overload → abandon this model
                if "temporarily rate-limited upstream" in txt:
                    print(f"⚠️ {model} overloaded. Switching model.")
                    return None

                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ 429 rate limit ({model}). Retrying in {wait:.1f}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            json_resp = response.json()

            return json_resp["choices"][0]["message"]["content"].strip()

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error ({model}) attempt {attempt + 1}: {e}")
            time.sleep(1)

    return None


# ---------- Multi-Model Retry (STRUCTURAL) ----------
def generate_hooks(topic):
    models = []

    if MISTRAL_API_KEY:
        models.append(
            ("mistralai/devstral-2512:free", MISTRAL_API_KEY)
        )

    if DEEPSEEK_API_KEY:
        models.append(
            ("deepseek/deepseek-r1-0528:free", DEEPSEEK_API_KEY)
        )

    MAX_RETRIES_PER_MODEL = 2

    for model, api_key in models:
        for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
            print(f"🔁 {model} | attempt {attempt}")

            result = call_openrouter(topic, api_key, model)

            # ✅ HARD GUARD — fixes Pylance + logic
            if result is not None and is_valid_output(result):
                return result, False

            time.sleep(0.4)

    return (
        "⚠️ HookyFY Lite is currently under heavy load.\n"
        "Please try again shortly — your viral hooks are worth the wait.",
        False,
    )


print(
    "🔍 API Keys Status →",
    "Mistral: READY" if MISTRAL_API_KEY else "Mistral: MISSING",
    "|",
    "DeepSeek: READY" if DEEPSEEK_API_KEY else "DeepSeek: MISSING",
)
