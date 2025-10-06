import streamlit as st
from hook_generator import generate_hooks

# Page config
st.set_page_config(page_title="HookyFY", layout="centered")

# ======================== CUSTOM THEME ========================
st.markdown(
    """
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #0a0014 0%, #0f0f18 40%, #000000 100%);
        color: white;
    }

    /* App container */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0014 0%, #0f0f18 40%, #000000 100%);
        color: white;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    /* Text input */
    input[type="text"] {
        background-color: rgba(255, 255, 255, 0.08);
        color: white;
        border: 1px solid #7b2ff7;
        border-radius: 6px;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #7b2ff7 30%, #000000 100%);
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 0 12px rgba(123, 47, 247, 0.3);
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(123, 47, 247, 0.6);
    }

    /* Expander style */
    details {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(123,47,247,0.3);
        border-radius: 8px;
        padding: 0.5em;
        color: white;
    }

    /* Headings */
    h1, h2, h3, h4, h5 {
        color: #e3d5ff;
        text-shadow: 0 0 10px rgba(123, 47, 247, 0.3);
    }

    /* Divider line */
    hr {
        border-top: 1px solid rgba(255,255,255,0.1);
    }

    /* Code box (results) */
    pre, code {
        background: rgba(255,255,255,0.07) !important;
        color: #e6e6e6 !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ======================== MAIN UI ========================
st.markdown("""
    <div style='text-align: center; font-family: "Segoe UI", sans-serif;'>
        <h1 style='font-size: 3em; margin-bottom: 0.2em;'>🚀 HookyFY Lite</h1>
        <h3 style='margin-top: 0;'>💡 Create Viral Hooks in Seconds — Powered by AI.</h3>
        <hr style='border-top: 1px solid #bbb; width: 60%; margin: 1em auto;'/>
    </div>
""", unsafe_allow_html=True)

st.markdown("#### 🎯 Generate 3 viral Instagram hooks + captions instantly")

# Topic input
topic = st.text_input("Enter a topic (e.g., Gym motivation, Wealth, Discipline):")

# Explanation expander
with st.expander("What do Hook, Reward, Caption & CTA mean?"):
    st.markdown("""
    - **Hook:** The attention-grabbing line that stops the scroll.  
    - **Reward:** The payoff or benefit viewers get if they keep watching.  
    - **Caption:** The description or story that supports the hook and value.  
    - **CTA:** What you want viewers to do next (comment, share, save, etc.).  
    """)

# ======================== HOOK GENERATION ========================
if st.button("Generate Hooks") and topic:

    def display_hooks():
        with st.spinner("⚡ Creating viral hooks... please wait."):
            try:
                result, is_incomplete = generate_hooks(topic)
                
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.warning(result)
                    return

                if not result or len(result) < 10:
                    st.warning("⚠️ AI returned an empty or incomplete response. Try rephrasing your topic.")
                    return

                if is_incomplete:
                    st.info("⚠️ Some ideas may be missing. We're working on it! Please try again soon.")

                st.success("🔥 Here's your content:")
                st.markdown("### 📌 Generated Hooks + Captions")

                pairs = [block.strip() for block in result.split("---") if "Hook:" in block and ("Caption:" in block or "CTA:" in block)]
                if not pairs:
                    st.warning("⚠️ No valid pairs found. Try again or rephrase your topic.")
                    return

                for idx, pair in enumerate(pairs[:3], start=1):
                    lines = pair.strip().splitlines()
                    formatted = []
                    has_cta = False

                    for line in lines:
                        if "Hook:" in line:
                            formatted.append(f"🎯 Hook: {line.split('Hook:')[-1].strip()}")
                        elif "Caption:" in line:
                            formatted.append(f"📝 Caption: {line.split('Caption:')[-1].strip()}")
                        elif "CTA:" in line:
                            formatted.append(f"📢 CTA: {line.split('CTA:')[-1].strip()}")
                            has_cta = True
                        elif "Reward:" in line:
                            formatted.append(f"🎁 Reward: {line.split('Reward:')[-1].strip()}")
                        else:
                            formatted.append(line.strip())

                    if not has_cta:
                        formatted.append("📢 CTA: 🔁 Save this. Follow for more.")

                    display_text = "\n\n".join(formatted)
                    st.markdown(f"#### 🔹 Pair {idx}")
                    st.code(display_text, language="markdown")
                    st.markdown("---")

            except Exception as e:
                st.error("Something went wrong. Please try again shortly.")
                st.text(str(e))

    display_hooks()

# ======================== FOOTER ========================
st.markdown("---")
st.markdown("<div style='text-align: center; color: #bbb;'>🙌 Liked this tool? Share it with your friends</div>", unsafe_allow_html=True)

# Waitlist button
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; font-family: "Segoe UI", sans-serif;'>
        <h4 style='font-weight: 500; color: #aaa;'>🚀 Be the first to try the full HookyFY experience</h4>
        <a href='https://your-waitlist-link.com' target='_blank'>
            <button class="generate-btn">
                🔔 Join Waitlist
            </button>
        </a>
    </div>

    <style>
    .generate-btn {
        background: linear-gradient(135deg, #7b2ff7 30%, #000000 100%);
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 0 12px rgba(123, 47, 247, 0.3);
    }
    .generate-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(123, 47, 247, 0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

