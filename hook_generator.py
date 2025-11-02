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
                "Write **exactly 3 viral Instagram post frameworks** that sound like they were written in the aftermath of a breakdown or a breakthrough — raw, visual, and unfiltered.\n"
                "Think: a voice message sent at 3AM that turned into poetry.\n"
                "Every line should sting, seduce, or scar. No motivational tone. No advice. Just cinematic confession and emotional dominance.\n\n"

                "🔥 HOOK RULES (STRICT):\n"
                "- 5–8 words ONLY.\n"
                "- Write like it’s a sin being confessed or a victory being whispered through clenched teeth.\n"
                "- Hooks must evoke **visceral emotion** — regret, lust, revenge, guilt, power, emptiness, or rebirth.\n"
                "- Use physical or visual imagery (blood, silence, mirror, ashes, breath, scars, hunger, fire, eyes, hands, etc.).\n"
                "- Every hook should sound like a *scene* not a *quote*.\n"
                "- Example tone: “I watched myself beg for love.” or “She made me her ghost.”\n"
                "- Ban the following words: success, goals, motivation, mindset, hustle, dream, growth, journey.\n"
                "- No emojis. No hashtags. No fake inspiration.\n\n"

                "💡 CONCLUSION RULES (STRICT):\n"
                "- 3–5 words ONLY.\n"
                "- Must hit like a closing scene or emotional reversal — from chaos to control, from pain to peace, from victim to villain.\n"
                "- Example tones: brutal acceptance, cold peace, power reclaimed, ego reborn.\n"
                "- Examples: “Now I don’t chase.” / “Silence tastes better.” / “She taught me rage.”\n\n"

                "📝 CAPTION RULES (STRICT):\n"
                "- 2–3 short sentences.\n"
                "- Must sound like something you'd write after the storm — calm voice, sharp truth.\n"
                "- Focus on sensory memory: what it felt like, smelled like, sounded like when it all fell apart.\n"
                "- Must end with a **natural CTA** (save/share/comment) woven into emotion, not as a command.\n"
                "- Example: “I kept apologizing for existing until it broke me. If you’ve been there, save this.”\n"
                "- Avoid explanations. Avoid moral lessons. Just pure emotion in motion.\n\n"

                "✅ EXAMPLE OUTPUT (Correct Style):\n"
                "Framework 1:\n"
                "Hook: I begged love to stay sober\n"
                "Conclusion: It chose the bottle\n"
                "Caption: I kept waiting for someone to save me from myself. Turns out, they were drowning too. Save this if you’ve ever mistaken pain for connection.\n\n"
                
                "Framework 2:\n"
                "Hook: She kissed me like a goodbye\n"
                "Conclusion: I still taste it\n"
                "Caption: Some ghosts don’t haunt—they linger in your pulse. Share this if you’ve ever loved a memory that refused to die.\n\n"
                
                "Framework 3:\n"
                "Hook: I became everything I feared\n"
                "Conclusion: And felt alive again\n"
                "Caption: Maybe healing isn’t soft. Maybe it’s burning the version they loved until only you remain. Comment if you understand.\n\n"

                "⚠️ OUTPUT FORMAT (STRICT):\n"
                "Framework 1:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                "Framework 2:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                "Framework 3:\nHook: ...\nConclusion: ...\nCaption: ...\n\n"
                "---\n"
                "**Important:**\n"
                "- Hooks = emotional violence or rebirth moments.\n"
                "- Conclusions = calm after the war.\n"
                "- Captions = human, sensory, cinematic — no fluff, no lessons.\n"
                "- Avoid generic words and positivity — lean into heartbreak, ego death, silence, power.\n"
                "- Make it feel like a confession that went viral."
            )
        }
    ],
    "temperature": 1.15,
    "max_tokens": 1800,
    "top_p": 0.92,
    "frequency_penalty": 0.2,
    "presence_penalty": 0.4
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
