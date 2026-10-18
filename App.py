import streamlit as st
import datetime
import urllib.parse
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from fpdf import FPDF
import base64

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VortixAI - Next-Gen Intelligence Platform",
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
        background: linear-gradient(90deg, #4A00E0, #8E2DE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .lets-go-btn {
        background-color: #1E1E2E;
        color: #FFFFFF;
        padding: 8px 24px;
        border-radius: 20px;
        border: 1px solid #444;
        font-weight: 600;
        margin-top: 15px;
    }
    .stChatInputContainer {
        padding-bottom: 10px;
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

    st.subheader("🛠️ Quick Tools")
    pdf_mode = st.checkbox("Generate Downloadable PDF Output", value=False)
    
    st.divider()
    if st.button("Clear Chat Session"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# HERO SECTION (LOOK WHAT YOU CAN DO WITH VORTIXAI)
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
with st.expander("➕ Options & Attachment Tools (Camera, Photos, Create Image, Deep Research...)", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("📷 **Camera / Photos**")
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_uploader")
        
    with col2:
        st.markdown("📁 **Files & Docs**")
        uploaded_doc = st.file_uploader("Upload Document", type=["pdf", "txt", "py", "html", "js"], key="doc_uploader")
        
    with col3:
        st.markdown("🎨 **Creative Suite**")
        st.caption("• HD Image Generation (English, Urdu, etc.)")
        st.caption("• Royalty-Free Video Prompt Scripts")
        st.caption("• Create Music & Audio Concepts")

    with col4:
        st.markdown("🧠 **Deep AI Suite**")
        st.caption("• Canvas Workspace")
        st.caption("• Deep Research Engine")
        st.caption("• Guided Learning & Coding Courses")

# Image Data Processing
img_data = None
if uploaded_image is not None:
    img_data = PILImage.open(uploaded_image)
    st.image(img_data, caption="Attached Image Preview", use_container_width=True)

# -----------------------------------------------------------------------------
# PDF GENERATOR HELPER
# -----------------------------------------------------------------------------
def create_pdf_file(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Basic encoding fix for printable text
    clean_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    filename = "VortixAI_Assignment_Report.pdf"
    pdf.output(filename)
    return filename

# -----------------------------------------------------------------------------
# CHAT DISPLAY & RESPONSE PROCESSING
# -----------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask VortixAI or generate images, code, 70-page PDFs, videos...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("VortixAI Processing..."):
            try:
                # 1. IMAGE GENERATION ENGINE DETECTOR
                is_image_request = any(keyword in user_prompt.lower() for keyword in ["make image", "create image", "generate image", "photo", "handwritten notes", "draw", "picture"])
                
                if is_image_request:
                    encoded_prompt = urllib.parse.quote(user_prompt)
                    # High-definition Pollinations HD rendering URL
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1280&height=720&seed=42&model=flux"
                    
                    st.markdown(f"### 🎨 VortixAI HD Image Output")
                    st.image(image_url, caption=f"Generated Image: {user_prompt}", use_container_width=True)
                    
                    response_text = f"Here is your HD generated image for: **{user_prompt}**\n\n![Generated Image]({image_url})"
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                # 2. TEXT / CODE / DEEP RESEARCH GENERATION ENGINE
                else:
                    client = genai.Client(api_key=api_key_input)
                    
                    system_instructions = (
                        "You are VortixAI, an advanced super-intelligent AI platform superior to ChatGPT, Claude, and You.com. "
                        "You can write long-form 60-70 page comprehensive assignment notes, generate full multi-module coding courses "
                        "(Python, Java, HTML, C++, JS), create copyright-free video script generation prompts, offer Urdu/English translation, "
                        "and produce clear structured notes."
                    )
                    
                    content_payload = []
                    if img_data:
                        content_payload.append(img_data)
                    
                    content_payload.append(f"{system_instructions}\n\nUser Request: {user_prompt}")

                    response = client.models.generate_content(
                        model=engine_choice,
                        contents=content_payload
                    )

                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                    # If PDF Mode is enabled, generate PDF download button
                    if pdf_mode:
                        pdf_path = create_pdf_file(response.text)
                        with open(pdf_path, "rb") as f:
                            st.download_button("📄 Download 60+ Page PDF Assignment/Report", f, file_name="VortixAI_Report.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"System Exception: {str(e)}")
