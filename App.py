import streamlit as st
import datetime
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os

# -----------------------------------------------------------------------------
# GLOBAL ENTERPRISE CONFIG & SEO META TAGS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VortixAI - Next-Gen Global AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting HTML/SEO Meta Tags
st.markdown("""
<head>
    <meta name="description" content="VortixAI Enterprise Platform: High-performance AI processing engine.">
    <meta name="keywords" content="VortixAI, AI Platform, Gemini API, Streamlit AI">
    <meta name="author" content="VortixAI Engineering">
</head>
""", unsafe_allow_dict=True)

# Custom CSS Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #888888;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_dict=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "daily_quota" not in st.session_state:
    st.session_state.daily_quota = 0

if "monthly_quota" not in st.session_state:
    st.session_state.monthly_quota = 0

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🌐 VortixAI Enterprise Hub")
    
    api_key_input = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        help="Provide your active Gemini API key from Google AI Studio."
    )
    
    st.markdown("[Get API Key from Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()

    engine_choice = st.selectbox(
        "Select Engine Architecture:",
        ["vortex-2.4", "vortex-2.5-flash", "vortex-2.5-pro"],
        index=0
    )

    anti_fluff = st.toggle("Anti-Fluff Semantic Filter (Active)", value=True, help="Removes unnecessary introductory filler.")

    st.divider()
    st.subheader("🖼️ Global Image Quota")
    st.write(f"**Daily Quota:** {st.session_state.daily_quota} / 15")
    st.write(f"**Monthly Quota:** {st.session_state.monthly_quota} / 500")

    st.divider()
    if st.button("Clear Session Memory"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN LAYOUT & HEADER
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">⚡ VortixAI</div>', unsafe_allow_dict=True)
st.markdown('<div class="sub-header">Enterprise-Grade Global AI Intelligence Platform | Zero-Fluff & High-Performance</div>', unsafe_allow_dict=True)

if not api_key_input:
    st.warning("⚠️ Please configure your Gemini API Key to initialize VortixAI.")
    st.stop()

# -----------------------------------------------------------------------------
# MULTI-MODAL FILE UPLOAD
# -----------------------------------------------------------------------------
uploaded_file = st.file_uploader("Upload image or file for deep neural analysis:", type=["png", "jpg", "jpeg", "pdf", "txt"])
img_data = None

if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        img_data = PILImage.open(uploaded_file)
        st.image(img_data, caption="Uploaded Image Preview", use_container_width=True)

# -----------------------------------------------------------------------------
# CHAT INTERFACE & HISTORY
# -----------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
user_prompt = st.chat_input("Ask VortixAI or use commands like...")

if user_prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Process response with Gemini API (Fresh Client per Request)
    with st.chat_message("assistant"):
        with st.spinner("Processing prompt..."):
            try:
                # Dynamically initialize client to avoid 'closed client' session drops
                client = genai.Client(api_key=api_key_input)
                
                # Map engine back to real Gemini API models
                target_model = "gemini-2.5-flash"
                if "2.5-pro" in engine_choice:
                    target_model = "gemini-2.5-pro"

                content_payload = []
                if img_data:
                    content_payload.append(img_data)
                    st.session_state.daily_quota += 1
                    st.session_state.monthly_quota += 1
                
                prompt_text = user_prompt
                if anti_fluff:
                    prompt_text += " (Note: Provide a direct, concise, and high-performance response without unnecessary greetings or filler.)"

                content_payload.append(prompt_text)

                response = client.models.generate_content(
                    model=target_model,
                    contents=content_payload
                )

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"System Exception: {str(e)}")
