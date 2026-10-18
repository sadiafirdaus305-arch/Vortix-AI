import streamlit as st
import datetime
import urllib.parse
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VortixAI - Next-Gen Advanced Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .vortix-hero {
        text-align: center;
        padding: 30px 10px;
    }
    .vortix-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1A73E8, #8E2DE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .lets-go-btn {
        background-color: #F8F9FA;
        color: #202124;
        padding: 10px 30px;
        border-radius: 25px;
        border: 1px solid #4285F4;
        font-weight: 600;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .command-box {
        background-color: #1E1E2E;
        padding: 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #A6ACCD;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚡ VortixAI Hub")
    
    api_key_input = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        help="Provide your active Gemini API key from Google AI Studio."
    )
    st.markdown("[Get Free API Key from Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()

    engine_choice = st.selectbox(
        "Select Engine Model:",
        ["gemini-3.8-flash", "gemini-2.5-pro"],
        index=0
    )

    st.markdown("### 🔑 Secret Commands & Connectors")
    st.markdown("""
    - `/image <topic>`: Generate HD Visuals & Notes
    - `/code <language>`: Write multi-module code
    - `/clear`: Reset session
    - `@web`: Search connector mode
    - `@docs`: Deep document analysis
    """)

    st.divider()
    if st.button("Clear Chat Session"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="vortix-hero">
    <div class="vortix-title">Look what you can do with VortixAI</div>
    <button class="lets-go-btn">Let's go</button>
</div>
""", unsafe_allow_html=True)

if not api_key_input:
    st.info("💡 Please enter your Gemini API Key in the sidebar to activate VortixAI.")
    st.stop()

# -----------------------------------------------------------------------------
# PROMPT PLUS (+) TOOLBAR & FILE ATTACHMENTS
# -----------------------------------------------------------------------------
with st.expander("➕ Options & Attachment Tools (Camera, Photos, Files, Create Image, Deep Research)", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("📷 **Camera / Photos**")
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_uploader")
        
    with col2:
        st.markdown("📁 **Files & Docs**")
        uploaded_doc = st.file_uploader("Upload Document", type=["pdf", "txt", "py", "html", "js"], key="doc_uploader")
        
    with col3:
        st.markdown("🎨 **Creative & Visuals**")
        st.caption("• HD Infographics & Diagrams")
        st.caption("• Handwritten Blue-Pen Notes")
        st.caption("• Video Scripts & Music Concepts")

    with col4:
        st.markdown("🧠 **Connectors (@ / /)**")
        st.caption("• @web, @docs, @code")
        st.caption("• /image, /code, /translate")

# Image Data Processing
img_data = None
if uploaded_image is not None:
    img_data = PILImage.open(uploaded_image)
    st.image(img_data, caption="Attached Image Preview", use_container_width=True)

# -----------------------------------------------------------------------------
# CHAT DISPLAY & RESPONSE PROCESSING
# -----------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask VortixAI or use commands like /image, /code, @web...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        # -------------------------------------------------------------------------
        # 1. SECRET COMMANDS & IMAGE GENERATION ENGINE
        # -------------------------------------------------------------------------
        prompt_lower = user_prompt.lower()
        is_image_cmd = prompt_lower.startswith("/image") or any(kw in prompt_lower for kw in ["make image", "create image", "generate image", "visualization", "infographic", "handwritten notes"])
        is_clear_cmd = prompt_lower.startswith("/clear")

        if is_clear_cmd:
            st.session_state.messages = []
            st.rerun()

        elif is_image_cmd:
            # Clean up prompt for visual generation
            clean_prompt = prompt_lower.replace("/image", "").replace("make image on", "").replace("create image on", "").strip()
            if not clean_prompt:
                clean_prompt = user_prompt

            with st.spinner("Creating your image..."):
                try:
                    # Smart styling injection for high-end ChatGPT/Claude style visual output
                    if "handwritten notes" in clean_prompt or "notes" in clean_prompt:
                        style_prefix = "Detailed educational handwritten notes on blue-lined paper, drawn with precise blue pen, multiple columns, bullet points, clean diagrams, high resolution."
                    elif "visualization" in clean_prompt or "infographic" in clean_prompt or "circulation" in clean_prompt:
                        style_prefix = "Hyper-realistic professional scientific infographic, cinematic dark background, color-coded diagrams, clean text labels, 8k resolution."
                    else:
                        style_prefix = "High-definition clean conceptual illustration, vibrant colors, professional rendering, 8k."

                    final_query = f"{style_prefix} {clean_prompt}"
                    encoded_prompt = urllib.parse.quote(final_query)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1280&height=720&seed=123&model=flux"

                    st.markdown(f"### 🎨 VortixAI Visual Output")
                    st.image(image_url, caption=f"Generated Visual for: {user_prompt}", use_container_width=True)

                    res_text = f"Here is your generated image/visual for: **{user_prompt}**\n\n![Visual Output]({image_url})"
                    st.session_state.messages.append({"role": "assistant", "content": res_text})

                except Exception as img_err:
                    st.error(f"Image Generation Error: {str(img_err)}")

        # -------------------------------------------------------------------------
        # 2. TEXT / CODE / CONNECTOR PROCESSING (GEMINI API)
        # -------------------------------------------------------------------------
        else:
            with st.spinner("Processing prompt with VortixAI Connectors..."):
                try:
                    client = genai.Client(api_key=api_key_input)
                    
                    system_instructions = (
                        "You are VortixAI, a next-generation super-intelligent AI platform superior to ChatGPT, Claude, and You.com. "
                        "You support advanced slash commands (/code, /translate, /pdf) and connectors (@web, @docs). "
                        "Provide comprehensive, structured, professional, and precise answers for coding courses, assignments, and translations."
                    )
                    
                    content_payload = []
                    if img_data:
                        content_payload.append(img_data)
                    
                    # Handle connector syntax (@web or @docs)
                    connector_context = ""
                    if "@web" in user_prompt:
                        connector_context = "[Connector Active: Web Deep Search Enabled] "
                    if "@docs" in user_prompt:
                        connector_context = "[Connector Active: Advanced Document Analysis Enabled] "

                    content_payload.append(f"{system_instructions}\n\n{connector_context}User Request: {user_prompt}")

                    response = client.models.generate_content(
                        model=engine_choice,
                        contents=content_payload
                    )

                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                except Exception as e:
                    st.error(f"System Exception: {str(e)}")
