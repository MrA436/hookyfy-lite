import os
import time
import requests
import random
from dotenv import load_dotenv

load_dotenv()

# ---------- Secrets ----------
MISTRAL_API_KEY = os.environ.get("OPENAI_API_KEY")
DEESEEK_API_KEY = os.environ.get("OPENAI_API_KEY_2")

# ---------- Config ----------
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
    "HTTP-Referer": "https://hookyfy-lite.streamlit.app/",
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

                    "Your ONLY priority is to generate **3 insanely viral Instagram Reel hooks + conclusions + captions**, "
                    "each one short, cinematic, emotionally sharp, and guaranteed to stop the scroll.\n\n"

                    "All hooks MUST be between **5–9 words**.\n"
                    "All conclusions MUST be between **3–6 words**.\n"
                    "Captions MUST be 2–3 lines and end with a CTA.\n\n"

                    "Each hook MUST come from a **different section** \n"
                    "• Curiosity (mystery, open loop, hidden truth)\n"
                    "• Shock (harsh truth, emotional hit)\n"
                    "• Power (identity shift, dominance)\n"
                    "• Relatable (human flaw, everyday struggle)\n"
                    "• Motivation (urgency, discipline)\n\n"

                    "You MUST choose **3 different sections** every time. NEVER repeat a section.\n\n"

                    "🔥 HOOK RULES (EXTREMELY IMPORTANT):\n"
                    "- MUST stop the scroll instantly.\n"
                    "- MUST feel viral, dangerous, or emotionally intense.\n"
                    "- MUST feel visually cinematic for Reels.\n"
                    "- MUST hit like a punch, revelation, or confrontation.\n"
                    "- MUST match the psychology of its assigned section.\n"
                    "- NO vague, soft, or generic lines.\n"
                    "- NO filler words.\n\n"

                    "💥 CONCLUSION RULES:\n"
                    "- 3–6 words.\n"
                    "- Must emotionally flip or amplify the hook.\n"
                    "- Should feel like the 'drop' in a cinematic edit.\n"
                    "- No generic words like 'success', 'life', 'goals'.\n\n"

                    "📝 CAPTION RULES:\n"
                    "- 2–3 short lines.\n"
                    "- Speak directly to the viewer.\n"
                    "- Emotional, personal, or cinematic tone.\n"
                    "- MUST add a CTA (Save/Share/Comment).\n\n"

                    "⚠️ DIVERSITY RULE:\n"
                    "- All 3 must have different tone, rhythm, and emotional type.\n"
                    "- No repetition of structure.\n"
                    "- Avoid predictable patterns.\n\n"

                    "📦 OUTPUT FORMAT (MANDATORY):\n"
                    "---\n"
                    "Hook 1 (Section: X):\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "---\n"
                    "Hook 2 (Section: Y):\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "---\n"
                    "Hook 3 (Section: Z):\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "---"
                )
            }
        ],
        "temperature": 0.92,
        "max_tokens": 1800,
        "top_p": 0.92,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.6
    }


    for attempt in range(3):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=data, timeout=25)

            if response.status_code == 429:
                txt = response.text
                if "temporarily rate-limited upstream" in txt:
                    print("⚠️ One source overloaded. Switching...")
                    return None, False
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ Too many requests. Retrying in {wait:.1f}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            json_resp = response.json()

            result = json_resp["choices"][0]["message"]["content"].strip()
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
        apis.append(lambda t: call_openrouter(t, DEESEEK_API_KEY, "deepseek/deepseek-chat"))
    if MISTRAL_API_KEY:
        apis.append(lambda t: call_openrouter(t, MISTRAL_API_KEY, "mistralai/mistral-7b-instruct"))

    for api_call in apis:
        result, is_incomplete = api_call(topic)
        if result and len(result.strip()) > 10:
            return result, is_incomplete

    return (
        "⚠️ HookyFY Lite is currently under heavy load.\nPlease try again shortly — your viral hooks are worth the wait. 💡",
        False
    )

print("🔍 Keys loaded:",
      "Primary ✅" if MISTRAL_API_KEY else "Primary ❌",
      "| Secondary ✅" if DEESEEK_API_KEY else "| Secondary ❌")
