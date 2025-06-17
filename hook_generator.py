import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()


# Get keys
DEESEEK_API_KEY = os.getenv("OPENAI_API_KEY_2")  # DeepSeek via OpenRouter
MISTRAL_API_KEY = os.getenv("OPENAI_API_KEY")    # Mistral via OpenRouter

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
    "HTTP-Referer": "https://hookyfy-lite.streamlit.app/",   
    "X-Title": "HookyFY Lite"
}

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
                    "You're a viral Instagram expert. For this topic, give **exactly 3** viral content ideas.\n\n"
                    "Each idea must include:\n"
                    "🎯 Hook: Scroll-stopping action or trigger (MAX 7 words).\n"
                    "🎁 Reward: Tangible result or win (MAX 5 words).\n"
                    "⚠️ Hook + Reward must be UNDER 10 words total.\n"
                    "⚠️ Hook must directly lead to the Reward.\n"
                    "⚠️ No vague words (e.g., 'potential', 'power', 'greatness').\n"
                    "⚠️ No poetic, fluffy, or rhyming lines.\n\n"
                    "📝 Caption: Keep it short, punchy, and relatable (Instagram tone).\n"
                    "📢 CTA: One strong call to action (Save / Comment / Share).\n\n"
                    "👉 Output Format (repeat 3 times, use --- to separate):\n"
                    "🎯 Hook: ...\n"
                    "🎁 Reward: ...\n"
                    "📝 Caption: ...\n"
                    "📢 CTA: ...\n"
                    "---"
                )
            }
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }



    response = requests.post(ENDPOINT, headers=headers, json=data, timeout=15)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def generate_hooks(topic):
    apis = [
        lambda topic: call_openrouter(topic, DEESEEK_API_KEY, "deepseek/deepseek-r1-0528:free"),
        lambda topic: call_openrouter(topic, MISTRAL_API_KEY, "mistralai/mistral-7b-instruct:free")
    ]

    for api_call in apis:
        for attempt in range(2):
            try:
                result = api_call(topic)
                if result and len(result.strip()) > 10:
                    return result
            except Exception as e:
                print(f"API call failed on attempt {attempt + 1} for {api_call.__name__}: {e}")
            time.sleep(1)

    return (
        "⚠️ HookyFY Lite is currently under heavy load.\n\n"
        "Please try again shortly — your viral hooks are worth the wait. 💡"
    )



print("Mistral Key starts with:", MISTRAL_API_KEY[:10])
print("DeepSeek Key starts with:", DEESEEK_API_KEY[:10])
