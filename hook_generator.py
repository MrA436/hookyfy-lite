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
                    "Generate exactly 3 viral Instagram post frameworks that hit **raw, high-stakes emotion**:\n\n"
                    "🔥 HOOK RULES (STRICT):\n"
                    "- Must grab attention instantly; trigger strong emotions: fear, envy, guilt, pride, shock, FOMO, anger, joy.\n"
                    "- 5–8 words only.\n"
                    "- Use simple, everyday language anyone scrolling can understand.\n"
                    "- Hooks must present **conflict, tension, or high stakes**.\n"
                    "- Hooks must make the user **stop scrolling immediately and feel something personal**.\n\n"
                    "💡 CONCLUSION RULES (STRICT):\n"
                    "- 3–5 words.\n"
                    "- Must resolve the tension emotionally, or twist it to shock or inspire.\n\n"
                    "📝 CAPTION RULES (STRICT):\n"
                    "- 2–3 short sentences, first-person storytelling.\n"
                    "- Must **embed a natural CTA at the end** ('like', 'save', 'share').\n"
                    "- NO separate CTA field under any circumstance.\n"
                    "- Language must feel raw, urgent, relatable, and real.\n"
                    "- Example correct framework:\n"
                    "Hook: I watched my dreams burn\n"
                    "Conclusion: Then I rebuilt\n"
                    "Caption: Everything I worked for went up in smoke, but I refused to quit. Save this if you’re not giving up.\n\n"
                    "⚠️ OUTPUT FORMAT (STRICT, numbered, all hooks & captions must feel intense and real):\n"
                    "Framework 1:\nHook: ...\nConclusion: ...\nCaption: ...\n"
                    "Framework 2:\nHook: ...\nConclusion: ...\nCaption: ...\n"
                    "Framework 3:\nHook: ...\nConclusion: ...\nCaption: ...\n"
                    "---\n"
                    "**Important:** Only 3 fields per framework. Hooks must feel raw, high-stakes, and emotionally gripping. Captions must tell a story, be relatable, and **include CTA naturally at the end**. Do NOT add extra lines, separate CTA fields, or vague/soft hooks."
                )
            }
        ],
        "temperature": 0.95,
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
