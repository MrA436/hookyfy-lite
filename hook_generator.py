import os
import time
import requests
import random
from dotenv import load_dotenv

load_dotenv()

# ---------- Secrets ----------
DEESEEK_API_KEY = os.environ.get("OPENAI_API_KEY_2")
MISTRAL_API_KEY = os.environ.get("OPENAI_API_KEY")

# ---------- Config ----------
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
    "HTTP-Referer": "https://hookyfy-lite.streamlit.app/",  # Playground always sets this
    "X-Title": "HookyFY Lite"
}

# ---------- Core Function ----------
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
                    "Generate **exactly 3 viral Instagram post frameworks** in this style:\n"
                    "\"I’m not here to compete; I’m here to dominate.\"\n\n"
                    "🔥 HOOK RULES:\n"
                    "- Provocative, thought-provoking question or statement (5–12 words).\n"
                    "- Dramatic, reflective, slightly rebellious.\n\n"
                    "💡 CONCLUSION RULES:\n"
                    "- 3–8 words, mindset-shifting answer.\n\n"
                    "📝 CAPTION RULES:\n"
                    "- 2–3 short sentences, cinematic, first-person.\n"
                    "- Use power verbs: dominate, annihilate, conquer, ignite, redefine.\n\n"
                    "📢 CTA RULES:\n"
                    "- Short, commanding, actionable.\n\n"
                    "⚠️ OUTPUT FORMAT (strict, numbered):\n"
                    "Framework 1:\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "Framework 2:\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "Framework 3:\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "---"
                )
            }
        ],
        "temperature": 0.75,
        "max_tokens": 2500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    for attempt in range(3):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=data, timeout=20)

            # --- Handle rate limiting ---
            if response.status_code == 429:
                txt = response.text
                if "temporarily rate-limited upstream" in txt:
                    print("⚠️ One source is overloaded. Switching...")
                    return None, False  # skip this model immediately
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ Too many requests. Retrying in {wait:.1f}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            json_resp = response.json()

            result = json_resp["choices"][0]["message"]["content"].strip()

            # Extract ideas safely
            ideas = [x for x in result.split("---") if "Hook:" in x and "Caption:" in x]
            is_incomplete = len(ideas) < 3

            return result, is_incomplete

        except requests.exceptions.RequestException as e:
            print(f"❌ Network hiccup. Retry {attempt + 1}: {e}")
            time.sleep(1)

    return None, False


# ---------- Multi-Model Retry ----------
def generate_hooks(topic):
    apis = []
    if DEESEEK_API_KEY:
        apis.append(lambda t: call_openrouter(t, DEESEEK_API_KEY, "deepseek/deepseek-r1-0528:free"))
    if MISTRAL_API_KEY:
        apis.append(lambda t: call_openrouter(t, MISTRAL_API_KEY, "mistralai/mistral-7b-instruct:free"))

    for api_call in apis:
        result, is_incomplete = api_call(topic)
        if result and len(result.strip()) > 10:
            return result, is_incomplete

    return (
        "⚠️ HookyFY Lite is currently under heavy load.\nPlease try again shortly — your viral hooks are worth the wait. 💡",
        False
    )


# ---------- Debug ----------
print("🔍 Keys loaded:",
      "Primary ✅" if MISTRAL_API_KEY else "Primary ❌",
      "| Secondary ✅" if DEESEEK_API_KEY else "| Secondary ❌")
