import streamlit as st
from hook_generator import generate_hooks

# Page config
st.set_page_config(page_title="HookyFY Lite", layout="centered")

# Title and description
st.markdown("<h1 style='text-align: center;'>🚀 HookyFY Lite</h1>", unsafe_allow_html=True)
st.markdown("### 💡 Write Viral Hooks in 10 Seconds. Powered by AI.")
st.markdown("**🔥 First 20 users get lifetime access free — DM ‘HOOKY’ to claim.**")
st.markdown("---")
st.markdown("👥 Want custom features or faster outputs? DM me on Instagram [@awkenofficial](https://instagram.com/awkenofficial)")

st.markdown("##### Generate 3 viral Instagram hooks + captions instantly")

# Topic input
topic = st.text_input("Enter a topic (e.g., Gym motivation, Wealth, Discipline):")

# Generate button logic
if st.button("Generate Hooks") and topic:
    with st.spinner("Thinking..."):
        try:
            result = generate_hooks(topic).strip()

            st.success("🔥 Here's your content:")
            st.markdown("### 📌 Generated Hooks + Captions")

            # Split by "---" to isolate each hook-caption-cta block
            pairs = [block.strip() for block in result.split("---") if "Hook:" in block and "Caption:" in block]

            if not pairs:
                st.warning("⚠️ No valid pairs found. Try again or rephrase your topic.")

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
