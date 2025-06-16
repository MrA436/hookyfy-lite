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
    Generate 3 Instagram content pairs with short, scroll-stopping hooks and punchy payoff rewards.

    Args:
        topic (str): Topic to generate content for.

    Returns:
        str: Raw model response or error message.
    """
    prompt = (
        f"You are a viral content strategist. Generate 3 Instagram content pairs on '{topic}'.\n\n"
        "Each pair must follow this exact format with clear separation by a blank line:\n\n"
        "Hook:\n<A very short, strong, emotional, scroll-stopping line (max 5 words) that grabs attention immediately>\n\n"
        "Caption:\n<2–3 lines explaining the hook in a relatable way>\n\n"
        "CTA:\n<A clear call to action like 'Save this now'>\n\n"
        "Reward:\n<The punchline or payoff — the surprising or satisfying answer viewers want after the hook (max 5 words)>\n\n"
        "Return exactly 3 pairs, each separated by TWO blank lines."
    )

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating content: {str(e)}"





   