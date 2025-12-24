import streamlit as st
import streamlit.components.v1 as components
from hook_generator import generate_hooks
import html
import re

# Page config
st.set_page_config(page_title="HookyFY", layout="centered")

# ======================== CUSTOM THEME ========================
st.markdown(
"""
<style>

    /* ===================== Background ===================== */
    body {
        background: linear-gradient(135deg, #0a0014 0%, #0f0f18 40%, #000000 100%);
        color: white;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0014 0%, #0f0f18 40%, #000000 100%);
    }

    /* ===================== Header Cleanup ===================== */
    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    /* ===================== Text Input ===================== */
    input[type="text"] {
        background-color: rgba(255, 255, 255, 0.06);
        color: white;
        border: 1px solid rgba(123,47,247,0.4);
        border-radius: 6px;
        padding: 0.55em 0.7em;
        box-shadow: inset 0 0 6px rgba(0,0,0,0.6);
    }

    input[type="text"]:focus {
        outline: none;
        border-color: #7b2ff7;
        box-shadow:
            inset 0 0 8px rgba(0,0,0,0.7),
            0 0 8px rgba(123,47,247,0.4);
    }

    /* ===================== Buttons (Streamlit + HTML) ===================== */
    div.stButton > button,
    button {
        background: linear-gradient(135deg, #7b2ff7 30%, #000000 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 600 !important;

        padding: 0.55em 1.3em !important;
        min-height: 38px !important;
        line-height: 1.1 !important;

        box-shadow: 0 6px 16px rgba(123,47,247,0.3) !important;
        transition: transform 0.15s ease, box-shadow 0.25s ease !important;
    }

    div.stButton > button:hover,
    button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(123,47,247,0.45) !important;
    }

    /* ===================== Expander ===================== */
    details {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(123,47,247,0.25);
        border-radius: 6px;
    }

    /* THIS is what actually controls height */
    details > summary {
        padding: 0.35em 0.6em !important;
        font-size: 0.9rem;
    }

    /* ===================== Headings ===================== */
    h1, h2, h3, h4, h5 {
        color: #e3d5ff;
        text-shadow: 0 0 6px rgba(123, 47, 247, 0.18);
        letter-spacing: 0.3px;
    }

    /* ===================== Output Cards (FINAL, STABLE) ===================== */

    /* Style ONLY markdown blocks that contain strong labels */
    [data-testid="stMarkdownContainer"]:has(strong) {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 3px solid rgba(123,47,247,0.55);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1.6rem;
    }

    /* Text rhythm inside cards */
    [data-testid="stMarkdownContainer"]:has(strong) p {
        line-height: 1.65;
        margin-bottom: 0.6rem;
    }

    /* ===================== Output Card Hover (Soft Lift) ===================== */
    [data-testid="stMarkdownContainer"]:has(strong) {
        transition: transform 0.15s ease, box-shadow 0.25s ease;
    }

    [data-testid="stMarkdownContainer"]:has(strong):hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 22px rgba(0,0,0,0.45);
    }


    /* ===================== Section Separators (CORRECT) ===================== */

    /* Style label paragraphs (Hook / Conclusion / Caption) */
    [data-testid="stMarkdownContainer"]:has(strong) p:has(strong) {
        margin-top: 0.9rem;
        padding-top: 0.6rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }

    /* Remove separator above first label */
    [data-testid="stMarkdownContainer"]:has(strong) p:has(strong):first-of-type {
        border-top: none;
        padding-top: 0;
        margin-top: 0;
    }

        


</style>
""",
unsafe_allow_html=True
)






# ======================== MAIN UI ========================

# ---- Hero ----
st.markdown(
    """
    <div class="hero">
        <h1>HookyFY Lite</h1>
        <p class="subtitle">Create viral hooks in seconds. Powered by AI.</p>
        <div class="divider"></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### Generate 3 short-form hooks")

# ---- State init ----

if "output_blocks" not in st.session_state:
    st.session_state.output_blocks = []



# ---- Form (ENTER-safe, duplicate-safe, failure-safe) ----
with st.form(key="generate_form", clear_on_submit=False):

    topic = st.text_input(
        "Topic",
        placeholder="discipline, money, lifestyle",
        key="topic"
    )

    submitted = st.form_submit_button(
        "Generate",
    )

    if submitted:   
        with st.spinner("Generating…"):
            try:
                result, _ = generate_hooks(topic)

                # Handle hard failure
                if not result or isinstance(result, str) and result.startswith(("❌", "⚠️")):
                    st.warning(result or "Generation failed. Try again.")
                    st.session_state.output_blocks = []
                else:
                    def strip_html(text: str) -> str:
                        return re.sub(r"<[^>]+>", "", text)

                    clean_blocks = []

                    for raw in result.split("---"):
                        lines = []

                        for line in raw.splitlines():
                            line = html.unescape(line)
                            line = re.sub(r"<[^>]+>", "", line).strip()


                            if (
                                line.startswith("Hook:")
                                or line.startswith("Conclusion:")
                                or line.startswith("Caption:")
                            ):
                                lines.append(line)

                        if any(l.startswith("Hook:") for l in lines) and any(l.startswith("Conclusion:") for l in lines):
                            clean_blocks.append("\n".join(lines))

                    st.session_state.output_blocks = clean_blocks[:3]



            except Exception as e:
                st.session_state.output_blocks = []
                st.error("Unexpected error during generation.")
                st.exception(e)




# ---- Optional explainer ----
with st.expander("What does this generate"):
    st.markdown(
        """
        **Hook**  
        The opening line that stops the scroll.

        **Conclusion**  
        A cold correction or consequence.

        **Caption**  
        A short expansion with a clean call to action.
        """
    )

# ---- Render Output ----

def extract_field(label, text):
    patterns = {
        "Hook": r"Hook:\s*(.*?)\s*(Conclusion:|Caption:|$)",
        "Conclusion": r"Conclusion:\s*(.*?)\s*(Caption:|$)",
        "Caption": r"Caption:\s*(.*)$",
    }
    match = re.search(patterns[label], text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

if st.session_state.output_blocks:
    st.markdown("#### Output")

    for raw in st.session_state.output_blocks:
        clean = html.unescape(raw)
        clean = re.sub(r"<[^>]+>", "", clean)

        hook = extract_field("Hook", clean)
        conclusion = extract_field("Conclusion", clean)
        caption = extract_field("Caption", clean)

        with st.container():
            st.markdown(
                f"""
                **Hook**  
                {hook}

                **Conclusion**  
                {conclusion}

                **Caption**  
                {caption}
                """
            )









# ------------ Footer -------------
components.html(
    """
    <style>
        .footer-btn {
            background: linear-gradient(135deg, #7b2ff7 30%, #000000 100%);
            color: white;
            border: none;
            padding: 0.55em 1.3em;
            border-radius: 7px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 6px 16px rgba(123, 47, 247, 0.3);
            transition: transform 0.15s ease, box-shadow 0.25s ease;
        }

        .footer-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 22px rgba(123, 47, 247, 0.45);
        }

        .footer-btn:active {
            transform: translateY(0);
            box-shadow: 0 4px 12px rgba(123, 47, 247, 0.25);
        }
    </style>

    <div style="
        text-align:center;
        margin-top:3rem;
        margin-bottom:2rem;
        opacity:0.85;
        font-family:Segoe UI, sans-serif;
    ">
        <p style="font-size:0.9rem; color:#9a9a9a; margin-bottom:0.6rem;">
            Built for creators who take attention seriously.
        </p>

        <p style="font-size:1rem; font-weight:500; color:#aaa; margin-bottom:0.8rem;">
            Access the full HookyFY system
        </p>

        <a href="https://forms.gle/861FsezQHnHFVSLF7" target="_blank">
            <button class="footer-btn">Join the waitlist</button>
        </a>
    </div>
    """,
    height=200,
)
