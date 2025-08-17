import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# ---------- Secrets ----------
def get_secret(key_name, fallback=""):
    value = os.getenv(key_name, fallback)
    if not value:
        print(f"⚠️ Warning: {key_name} not found in environment.")
    return value

# ✅ Load API keys safely
DEESEEK_API_KEY = get_secret("OPENAI_API_KEY_2")  # DeepSeek via OpenRouter
MISTRAL_API_KEY = get_secret("OPENAI_API_KEY")    # Mistral via OpenRouter

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
                    "You are an elite Instagram content strategist for luxury, wealth, and high-performance niches.\n"
                    "Generate 3 viral post frameworks that feel like a top creator saying 'I’m not here to compete, I’m here to dominate.'\n\n"

                    "🔥 HOOK + REWARD RULES:\n"
                    "🎯 Hook: Bold, commanding, scroll-stopping. Max 7 words. Can be declarative or a proclamation of dominance.\n"
                    "🎁 Reward: Tangible outcome or power statement. Max 5 words. Reinforces dominance and status.\n"
                    "⚡ Hook + Reward combined under 10 words.\n"
                    "⚡ Avoid vague/soft language: no 'maybe', 'try', 'sometimes'.\n"
                    "✅ Use swagger, authority, elite mindset, and cinematic language.\n\n"

                    "📝 Caption RULES:\n"
                    "- 2–3 short, punchy sentences.\n"
                    "- Tone: Dominant, commanding, swagger-filled. No fluff.\n"
                    "- Emphasize status, power, execution, or market dominance.\n"
                    "- Use power verbs (obliterate, dominate, command, annihilate, redefine) and cinematic flair.\n\n"

                    "📢 CTA RULES:\n"
                    "- Must be commanding: 'Save this now', 'Share with your team', 'Comment X to claim'.\n"
                    "- Avoid weak or optional phrasing.\n\n"

                    "⚠️ OUTPUT FORMAT (strict):\n"
                    "🎯 Hook: ...\n"
                    "🎁 Reward: ...\n"
                    "📝 Caption: ...\n"
                    "📢 CTA: ...\n"
                    "---"
                )
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }



    response = requests.post(ENDPOINT, headers=headers, json=data, timeout=15)
    response.raise_for_status()

    json_resp = response.json()
    # ✅ Some models return "message", some "messages"
    if "choices" in json_resp and json_resp["choices"]:
        result = (
            json_resp["choices"][0]
            .get("message", json_resp["choices"][0].get("messages", {}))
            .get("content", "")
            .strip()
        )
    else:
        raise ValueError("⚠️ Unexpected API response format")

    # ✅ Cutoff-safe idea parsing
    ideas = [x for x in result.split("---") if "🎯 Hook:" in x and "🎁 Reward:" in x]
    is_incomplete = len(ideas) < 3

    return result, is_incomplete


# ---------- Multi-Model Retry ----------
def generate_hooks(topic):
    apis = [
        ("DeepSeek", lambda t: call_openrouter(t, DEESEEK_API_KEY, "deepseek/deepseek-r1-0528:free")),
        ("Mistral",  lambda t: call_openrouter(t, MISTRAL_API_KEY, "mistralai/mistral-7b-instruct:free"))
    ]

    for name, api_call in apis:
        for attempt in range(2):
            try:
                result, is_incomplete = api_call(topic)
                if result and len(result.strip()) > 10:
                    return result, is_incomplete
            except Exception as e:
                print(f"❌ {name} failed on attempt {attempt + 1}: {e}")
            time.sleep(1)

    return (
        "⚠️ HookyFY Lite is currently under heavy load.\n\n"
        "Please try again shortly — your viral hooks are worth the wait. 💡",
        False
    )


# ---------- Debug ----------
print("Mistral Key starts with:", (MISTRAL_API_KEY or "❌None")[:10])
print("DeepSeek Key starts with:", (DEESEEK_API_KEY or "❌None")[:10])
