# hook_generator.py
# This file contains the function to call DeepSeek API to generate hooks + captions

import os
import streamlit as st
from openai import OpenAI
from openai.types.chat import ChatCompletion  # For proper type hinting

# Try to load local .env in dev environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Load API key from environment or Streamlit secrets
API_KEY: str | None = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# Raise error if key is missing
if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is missing in .env or secrets.toml")

# Initialize OpenAI-compatible client for DeepSeek via OpenRouter
client: OpenAI = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def generate_hooks(topic: str) -> str:
    """
    Generate 3 hook + caption + CTA + reward pairs using Mistral-compatible prompt.

    Args:
        topic (str): Topic to generate content for.

    Returns:
        str: The full raw text response from the model or a warning message.
    """
    prompt: str = (
        f"You are a viral content strategist. Generate 3 Instagram content pairs for the topic: '{topic}'.\n\n"
        "Each pair must follow this exact format:\n"
        "Hook:\n<Strong, emotional, scroll-stopping line>\n\n"
        "Caption:\n<2–3 lines explaining the hook in a relatable way>\n\n"
        "CTA:\n<A strong call to action like 'Save this now' or 'Follow for more'>\n\n"
        "Reward:\n<One-line emotional or practical benefit they’ll get if they follow this advice>\n\n"
        "Only return exactly 3 such pairs.\n"
        "Separate each pair with this: ---"
    )

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",  # You can change model name if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating content: {str(e)}"


    try:
        response: ChatCompletion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=700
        )

        result: str = response.choices[0].message.content.strip()

        if not result or "Hook:" not in result or "Caption:" not in result:
            return "⚠️ Model returned an invalid response. Try rephrasing your topic."

        return result

    except Exception as e:
        return f"❌ Error generating content: {str(e)}"
