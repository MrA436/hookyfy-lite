import streamlit as st
from hook_generator import generate_hooks

# Page config
st.set_page_config(page_title="HookyFY Lite", layout="centered")

# Title and description
st.markdown("""
    <div style='text-align: center; font-family: "Segoe UI", sans-serif;'>
        <h1 style='font-size: 3em; margin-bottom: 0.2em;'>🚀 HookyFY Lite</h1>
        <h3 style='margin-top: 0;'>💡 Create Viral Hooks in Seconds — Powered by AI.</h3>
        <p><strong>🔥 First 20 users get lifetime access free — DM ‘HOOKY’ to claim.</strong></p>
        <hr style='border-top: 1px solid #bbb; width: 60%; margin: 1em auto;'/>
        <p style='font-size: 0.95em;'>👥 Want custom features or faster outputs?<br>
        DM me on Instagram <a href='https://www.instagram.com/_awken/' target='_blank' style='text-decoration: none; color: #FF4B4B;'>@_awken</a></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("#### 🎯 Generate 3 viral Instagram hooks + captions instantly")

# Topic input
topic = st.text_input("Enter a topic (e.g., Gym motivation, Wealth, Discipline):")

# Generate button logic
if st.button("Generate Hooks") and topic:
    with st.spinner("Thinking..."):
        try:
            result = generate_hooks(topic)

            if result.startswith("❌") or result.startswith("⚠️"):
                st.warning(result)
                st.stop()

            if not result or len(result) < 10:
                st.warning("⚠️ AI returned an empty or incomplete response. Try rephrasing your topic.")
                st.stop()

            st.success("🔥 Here's your content:")
            st.markdown("### 📌 Generated Hooks + Captions")

            # Split by "---" and filter valid pairs
            pairs = [block.strip() for block in result.split("---") if "Hook:" in block and ("Caption:" in block or "CTA:" in block)]

            if not pairs:
                st.warning("⚠️ No valid pairs found. Try again or rephrase your topic.")
                st.stop()

            for idx, pair in enumerate(pairs[:3], start=1):
                lines = pair.splitlines()
                formatted = []
                has_cta = False

                for line in lines:
                    if "Hook:" in line:
                        formatted.append(f"**🎯 Hook:** {line.split('Hook:')[-1].strip()}")
                    elif "Caption:" in line:
                        formatted.append(f"**📝 Caption:** {line.split('Caption:')[-1].strip()}")
                    elif "CTA:" in line:
                        formatted.append(f"**📢 CTA:** {line.split('CTA:')[-1].strip()}")
                        has_cta = True
                    elif "Reward:" in line:
                        formatted.append(f"**🎁 Reward:** {line.split('Reward:')[-1].strip()}")
                    else:
                        formatted.append(line.strip())

                # Add fallback CTA if missing
                if not has_cta:
                    formatted.append("**📢 CTA:** 🔁 Save this. Follow for more.")

                display_text = "\n".join(formatted)
                st.markdown(f"#### 🔹 Pair {idx}")
                st.markdown(display_text, unsafe_allow_html=True)
                st.text_area(f"📋 Copy Pair {idx}", display_text, height=300, key=f"copy_{idx}")
                st.markdown("---")

        except Exception as e:
            st.error("Something went wrong. Please check your API key or retry.")
            st.text(str(e))

# Footer
st.markdown("---")
st.markdown("🙌 Liked this tool? Share it with your friends and follow [@_awken](https://www.instagram.com/_awken) for more.")
