# hook_generator.py
# This file contains the function to call DeepSeek API to generate hooks + captions

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Get the API key from environment variable
import streamlit as st
api_key = st.secrets["OPENAI_API_KEY"]


# Raise error early if API key is missing
if not API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in environment variables.")

#Initialize OpenAI-compatible client for DeepSeek via OpenRouter
client = OpenAI(
    api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1"
        )

def generate_hooks(topic):
    """
    Generate 3 viral Instagram hook + caption pairs using DeepSeek.

    Args:
        topic (str): Topic to generate content for (e.g., "discipline", "luxury").

    Returns:
        str: Generated text from the DeepSeek model.
    """
    prompt = (
        f"Give me 3 Instagram hook + caption pairs for the topic '{topic}'.\n"
        "Each hook should be bold, emotional, and highly viral.\n"
        "Each caption should explain the hook in 2–3 lines and end with a strong CTA like "
        "'Follow for more', 'Save this now', or 'Tag someone'.\n"
        "Use this format strictly:\n"
        "Hook:\n<your hook>\nCaption:\n<your caption>\nCTA:\n<your CTA>\n---"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating content: {str(e)}"
