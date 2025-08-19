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
                    "Generate **exactly 3 viral Instagram post frameworks** in this style:\n"
                    "\"I’m not here to compete; I’m here to dominate.\"\n\n"

                    "🔥 HOOK RULES:\n"
                    "- Provocative, thought-provoking question or statement (5–12 words).\n"
                    "- Dramatic, reflective, slightly rebellious.\n"
                    "- Examples: 'Why were you born into mediocrity?', 'What if your fear is the final obstacle?'\n\n"

                    "💡 CONCLUSION RULES:\n"
                    "- 3–8 words, mindset-shifting answer.\n"
                    "- Emotionally magnetic, aspirational, or surprising.\n"
                    "- Examples: 'To rewrite your destiny.', 'Own your legacy.'\n\n"

                    "📝 CAPTION RULES:\n"
                    "- 2–3 short sentences, cinematic, first-person.\n"
                    "- Expand on hook + conclusion.\n"
                    "- Use power verbs: dominate, annihilate, conquer, ignite, redefine.\n\n"

                    "📢 CTA RULES:\n"
                    "- Short, commanding, actionable.\n"
                    "- Examples: 'Comment X if this hits', 'Save this to own your day', 'Share to inspire.'\n\n"

                    "⚠️ OUTPUT FORMAT (strict, numbered):\n"
                    "Framework 1:\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "Framework 2:\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "Framework 3:\nHook: ...\nConclusion: ...\nCaption: ...\nCTA: ...\n"
                    "---"
                )
            }
        ],
        "temperature": 0.75,
        "max_tokens": 2500
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
