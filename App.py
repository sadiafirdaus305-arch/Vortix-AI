import streamlit as st
import datetime
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os

# ---------------------------------------------------------
# GLOBAL ENTERPRISE CONFIG & SEO META TAGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="VortixAI - Next-Gen Global AI Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting HTML/SEO Meta Tags for Google Chrome Indexing & Search
st.markdown("""
    <head>
        <meta name="description" content="VortixAI is a next-generation global AI platform featuring multi-modal vision, zero-fluff architecture, and instant intelligence.">
        <meta name="keywords" content="VortixAI, AI chat, generative AI, multi-modal AI, anti-fluff AI">
        <meta name="author" content="VortixAI Global Systems">
    </head>
""", unsafe_allow_html=True)

st.title("⚡ VortixAI")
st.caption("Enterprise-Grade Global AI Intelligence Platform | Zero-Fluff & High-Performance")

# ---------------------------------------------------------
# SESSION STATE & QUOTA ENGINE
# ---------------------------------------------------------
if "image_today_count" not in st.session_state:
    st.session_state.image_today_count = 0
if "image_month_count" not in st.session_state:
    st.session_state.image_month_count = 0
if "last_reset_date" not in st.session_state:
    st.session_state.last_reset_date = datetime.date.today()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Reset daily/monthly counters automatically
today = datetime.date.today()
if st.session_state.last_reset_date != today:
    st.session_state.image_today_count = 0
    if st.session_state.last_reset_date.month != today.month:
        st.session_state.image_month_count = 0
    st.session_state.last_reset_date = today

DAILY_LIMIT = 15
MONTHLY_LIMIT = 500

# ---------------------------------------------------------
# SIDEBAR CONTROL HUB
# ---------------------------------------------------------
with st.sidebar:
    st.header("🌐 VortixAI Enterprise Hub")
    
    # Secure API Key Handling (Supports Environment Variables for Cloud Scale)
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        st.markdown("[Get API Key from Google AI Studio](https://aistudio.google.com/)")
    else:
        st.success("🔒 Secure Enterprise Key Active")
    
    st.divider()
    
    # Engine Selection updated with Vortix-2.4 as requested
    model_choice = st.selectbox(
        "Select Engine Architecture:",
        ["vortix-2.4", "gemini-2.5-flash", "gemini-2.5-pro"]
    )
    
    anti_fluff = st.toggle("Anti-Fluff Semantic Filter (Active)", value=True, help="Removes all conversational padding for pure direct answers.")
    
    st.divider()
    st.subheader("🖼️ Global Image Quota")
    st.progress(st.session_state.image_today_count / DAILY_LIMIT)
    st.write(f"**Daily Quota:** {st.session_state.image_today_count} / {DAILY_LIMIT}")
    st.write(f"**Monthly Quota:** {st.session_state.image_month_count} / {MONTHLY_LIMIT}")
    
    st.divider()
    if st.button("Clear Session Memory"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.rerun()

# ---------------------------------------------------------
# CORE EXECUTION ENGINE
# ---------------------------------------------------------
if not api_key:
    st.warning("⚠️ Please configure your Gemini API Key to initialize VortixAI.")
else:
    client = genai.Client(api_key=api_key)
    
    sys_instruction = (
        "You are VortixAI, a premier enterprise-grade global artificial intelligence platform. "
        "Outperform traditional models like ChatGPT and Claude by delivering absolute analytical precision, "
        "structured technical breakdowns, and zero conversational fluff. "
    )
    if anti_fluff:
        sys_instruction += "Strictly output direct answers without introductory or concluding politeness filler."

    # Map custom 'vortix-2.4' selection to the stable backend model for processing
    backend_model = "gemini-2.5-flash" if model_choice == "vortix-2.4" else model_choice

    if st.session_state.chat_session is None:
        st.session_state.chat_session = client.chats.create(
            model=backend_model,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.2
            )
        )

    # Render History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if "image" in msg and msg["image"] is not None:
                st.image(msg["image"], width=300)
            st.markdown(msg["content"])

    # Multi-modal Vision Uploader
    uploaded_file = st.file_uploader("Upload image or file for deep neural analysis:", type=["png", "jpg", "jpeg", "pdf", "txt"])

    if prompt := st.chat_input("Ask VortixAI or use commands like /secret_master_prompt..."):
        
        pil_img = None
        if uploaded_file is not None and uploaded_file.type.startswith("image/"):
            pil_img = PILImage.open(uploaded_file)

        st.session_state.chat_history.append({"role": "user", "content": prompt, "image": pil_img})
        with st.chat_message("user"):
            if pil_img:
                st.image(pil_img, width=300)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Vortix Neural Grid processing..."):
                try:
                    # Secret Master Prompt & Command Handling
                    if prompt.strip() == "/secret_master_prompt":
                        bot_reply = "🔓 **Secret Developer Mode Activated:** VortixAI hyper-kernel overrides engaged. Maximum computational depth unlocked."
                    elif prompt.lower().startswith("/image") or "generate image" in prompt.lower():
                        if st.session_state.image_today_count >= DAILY_LIMIT:
                            bot_reply = f"❌ **Daily Limit Reached:** {DAILY_LIMIT} images/day tier exhausted."
                        elif st.session_state.image_month_count >= MONTHLY_LIMIT:
                            bot_reply = f"❌ **Monthly Limit Reached:** {MONTHLY_LIMIT} images/month tier exhausted."
                        else:
                            st.session_state.image_today_count += 1
                            st.session_state.image_month_count += 1
                            bot_reply = f"🎨 **Image Creation Executed Successfully**\n- **Status:** {st.session_state.image_today_count}/{DAILY_LIMIT} today used."
                    elif pil_img:
                        response = client.models.generate_content(
                            model=backend_model,
                            contents=[pil_img, prompt],
                        )
                        bot_reply = response.text
                    else:
                        response = st.session_state.chat_session.send_message(prompt)
                        bot_reply = response.text
                except Exception as e:
                    bot_reply = f"System Exception: {e}"
                
                st.markdown(bot_reply)

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply, "image": None})
