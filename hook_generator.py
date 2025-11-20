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
                "Generate **exactly 3 unique viral Instagram post frameworks** about this topic.\n"
                "Each must feel raw, emotional, and mirror the viewer’s own experiences — like you’re talking directly to their hidden pain or pride.\n\n"

                "🔥 HOOK RULES:\n"
                "- Must directly relate to the topic — use its meaning or emotion, not just its word.\n"
                "- 5–9 words.\n"
                "- Different tone for each: 1) angry/defiant, 2) sad/regretful, 3) empowering/shocking.\n"
                "- Avoid repeating structure or rhythm from previous hooks.\n"
                "- Must make the viewer feel personally attacked, understood, or exposed.\n\n"

                "💥 CONCLUSION RULES:\n"
                "- 3–6 words that emotionally flip the hook.\n"
                "- Must *complete* the emotional arc — if the hook is pain, make the conclusion power or peace.\n"
                "- Avoid generic words like 'success', 'goals', 'life'.\n\n"

                "🩸 CAPTION RULES:\n"
                "- 2–3 short lines max.\n"
                "- Talk to the reader directly ('you'), not about yourself.\n"
                "- Keep tone emotional, cinematic, and personal.\n"
                "- Must include a call to action: 'Save this', 'Comment if it hits', or 'Share if it’s you'.\n"
                "- Avoid vague motivational lines — show a *feeling* or a *moment*.\n\n"

                "⚠️ DIVERSITY ENFORCER:\n"
                "- No two frameworks can share the same emotion, tone, or sentence rhythm.\n"
                "- Each should feel like a different scene from the same emotional universe.\n"
                "- Must include the input topic or its synonym clearly.\n\n"

                "📦 OUTPUT FORMAT:\n"
                "Framework 1:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                "Framework 2:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                "Framework 3:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
            )
        }
    ],
    "temperature": 0.9,
    "max_tokens": 2500,
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
