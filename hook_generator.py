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
                    "Generate **exactly 3 viral Instagram post frameworks** that feel cinematic, primal, and emotionally high-stakes.\n"
                    "Each framework must make the reader *feel punched in the chest*, not just impressed.\n\n"
                    
                    "🔥 HOOK RULES (STRICT):\n"
                    "- 5–8 words ONLY.\n"
                    "- Must create instant emotional impact — make the reader FEEL fear, envy, guilt, power, pride, regret, or awe.\n"
                    "- Must sound like something a human would scream, confess, or whisper at rock-bottom or peak victory.\n"
                    "- Hooks must imply a story, conflict, or transformation.\n"
                    "- Avoid generic words (success, mindset, goals, dreams). Use visceral language that stings or inspires.\n"
                    "- No emojis. No hashtags.\n\n"
                    
                    "💡 CONCLUSION RULES (STRICT):\n"
                    "- 3–5 words.\n"
                    "- Must emotionally resolve or reverse the hook — either redemption, dominance, or awakening.\n"
                    "- Should feel like the climax of a movie scene.\n\n"
                    
                    "📝 CAPTION RULES (STRICT):\n"
                    "- 2–3 short sentences.\n"
                    "- First-person tone: sound real, confessional, and raw.\n"
                    "- Must include a **natural CTA** at the end (like, save, share, comment) — no separate CTA field.\n"
                    "- Use storytelling and contrast: downfall → lesson → power.\n"
                    "- No motivational quotes or clichés.\n"
                    "- Write like you’re talking to one person who’s struggling silently.\n\n"
                    
                    "✅ EXAMPLE OUTPUT (Correct Style):\n"
                    "Hook: I lost everything chasing validation\n"
                    "Conclusion: But found myself instead\n"
                    "Caption: I kept posting for approval until I forgot who I was. Don’t make my mistake — save this for when you need to remember your worth.\n\n"
                    
                    "⚠️ OUTPUT FORMAT (STRICT):\n"
                    "Framework 1:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                    "Framework 2:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                    "Framework 3:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                    "---\n"
                    "**Important:**\n"
                    "- Every hook must hit like a confession or a declaration of war.\n"
                    "- Every caption must sound human, vulnerable, or victorious.\n"
                    "- Do NOT add extra notes, hashtags, emojis, or empty motivation."
                )
            }
        ],
        "temperature": 1.0,
        "max_tokens": 2500,
        "top_p": 1,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.3
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
        apis.append(lambda t: call_openrouter(t, DEESEEK_API_KEY, "deepseek/deepseek-chat-v3.1:free"))
    if MISTRAL_API_KEY:
        apis.append(lambda t: call_openrouter(t, MISTRAL_API_KEY, "mistralai/devstral-small-2505:free"))

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
