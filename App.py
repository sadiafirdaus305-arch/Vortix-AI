import streamlit as st
import datetime
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os

st.set_page_config(
    page_title="VortixAI - Next-Gen Global AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "daily_quota" not in st.session_state:
    st.session_state.daily_quota = 0

if "monthly_quota" not in st.session_state:
    st.session_state.monthly_quota = 0

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

    anti_fluff = st.toggle("Anti-Fluff Semantic Filter (Active)", value=True)

    st.divider()
    st.subheader("🖼️ Global Image Quota")
    st.write(f"**Daily Quota:** {st.session_state.daily_quota} / 15")
    st.write(f"**Monthly Quota:** {st.session_state.monthly_quota} / 500")

    st.divider()
    if st.button("Clear Session Memory"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1>⚡ VortixAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888888;'>Enterprise-Grade Global AI Intelligence Platform</p>", unsafe_allow_html=True)

if not api_key_input:
    st.warning("⚠️ Please configure your Gemini API Key to initialize VortixAI.")
    st.stop()

uploaded_file = st.file_uploader("Upload image or file:", type=["png", "jpg", "jpeg", "pdf", "txt"])
img_data = None

if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        img_data = PILImage.open(uploaded_file)
        st.image(img_data, caption="Uploaded Image Preview", use_container_width=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask VortixAI...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing prompt..."):
            try:
                client = genai.Client(api_key=api_key_input)
                
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
                    prompt_text += " (Note: Provide a direct and concise response.)"

                content_payload.append(prompt_text)

                response = client.models.generate_content(
                    model=target_model,
                    contents=content_payload
                )

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"System Exception: {str(e)}")
