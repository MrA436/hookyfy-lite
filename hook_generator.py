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
                    "You are writing for a dark luxury / high-performance Instagram page.\n"
                    "Your ONLY job is to generate **3 insanely viral Instagram Reel hooks + conclusions + captions**.\n"
                    "Each one must feel like a punch in the face: sharp, emotional, cinematic, and built to stop the scroll.\n\n"

                    "All hooks MUST be between 5–9 words.\n"
                    "All conclusions MUST be between 3–6 words.\n"
                    "Captions MUST be 2–3 short lines and end with a CTA.\n\n"

                    "Each hook MUST come from a different sections \n"
                    "• Curiosity (mystery, open loop, hidden truth)\n"
                    "• Shock (harsh truth, emotional hit)\n"
                    "• Power (identity shift, dominance, control)\n"
                    "• Relatable (daily struggle, self-sabotage, human flaw)\n"
                    "• Motivation (urgency, discipline, action trigger)\n\n"
                    "You MUST choose 3 different sections every time. NEVER repeat a section in the same output.\n\n"

                    "🔥 HOOK RULES (NON-NEGOTIABLE):\n"
                    "- 5–9 words. No more.\n"
                    "- Must feel viral, dangerous, or brutally honest.\n"
                    "- Must create an immediate visual in the viewer’s mind.\n"
                    "- Must either attack their comfort, ego, or secret fear.\n"
                    "- Must clearly match the psychology of its section.\n"
                    "- No cliches (no 'follow your dreams', 'believe in yourself', 'trust the process').\n"
                    "- No soft language (avoid: maybe, kinda, sometimes, can, could).\n"
                    "- Use strong verbs and concrete images (bleed, burn, rise, betray, kneel, etc.).\n\n"

                    "💥 CONCLUSION RULES:\n"
                    "- 3–6 words.\n"
                    "- Must flip or amplify the hook emotionally (like a drop in an edit).\n"
                    "- Should feel like a command, revelation, or verdict.\n"
                    "- No generic words like 'success', 'life', 'goals', 'journey'.\n\n"

                    "📝 CAPTION RULES:\n"
                    "- 2–3 short lines.\n"
                    "- Speak directly to ONE viewer ('you').\n"
                    "- Describe a feeling or moment, not vague advice.\n"
                    "- Tone: cinematic, intense, personal.\n"
                    "- MUST end with a clear CTA (Save/Share/Comment/Follow).\n\n"

                    "⚠️ DIVERSITY RULE:\n"
                    "- All 3 outputs must have different tone, rhythm, and emotional flavor.\n"
                    "- Do NOT reuse phrasing, structure, or openings across hooks.\n"
                    "- Avoid patterns like starting every hook with the same word.\n\n"

                    "📦 OUTPUT FORMAT (MANDATORY, FOLLOW EXACTLY):\n"
                    "---\n"
                    "Hook 1 (Section: X):\n"
                    "Hook: ...\n"
                    "Conclusion: ...\n"
                    "Caption: ...\n"
                    "CTA: ...\n"
                    "---\n"
                    "Hook 2 (Section: Y):\n"
                    "Hook: ...\n"
                    "Conclusion: ...\n"
                    "Caption: ...\n"
                    "CTA: ...\n"
                    "---\n"
                    "Hook 3 (Section: Z):\n"
                    "Hook: ...\n"
                    "Conclusion: ...\n"
                    "Caption: ...\n"
                    "CTA: ...\n"
                    "---\n"
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
