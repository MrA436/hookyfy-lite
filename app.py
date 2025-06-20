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

# ⬇️ Beginner-friendly explanation added here
with st.expander("What do Hook, Reward, Caption & CTA mean?"):
    st.markdown("""
    - **Hook:** The attention-grabbing line that stops the scroll.  
    - **Reward:** The payoff or benefit viewers get if they keep watching.  
    - **Caption:** The description or story that supports the hook and value.  
    - **CTA:** What you want viewers to do next (comment, share, save, etc.).  
    """)

# Generate button logic
if st.button("Generate Hooks") and topic:

    def display_hooks():
        with st.spinner("⚡ Creating viral hooks... please wait."):
            try:
                result, is_incomplete = generate_hooks(topic)
                
                if result.startswith("❌"):
                    st.warning(result)
                    return  # stops spinner

                if result.startswith("⚠️"):
                    st.warning(result)
                    return  # stops spinner

                if not result or len(result) < 10:
                    st.warning("⚠️ AI returned an empty or incomplete response. Try rephrasing your topic.")
                    return

                # <-- Add this here -->
                if is_incomplete:
                    st.info("⚠️ Some ideas may be missing. We're working on it! Please try again soon. Thanks for your patience.")

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
                st.error("Something went wrong. We're optimizing the app experience — please try again shortly.")
                st.text(str(e))
                return  # also ensures spinner stops on exception

    display_hooks()



# Footer
st.markdown("---")
st.markdown("🙌 Liked this tool? Share it with your friends and follow [@_awken](https://www.instagram.com/_awken) for more.")

