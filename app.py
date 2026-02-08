__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="COREP Assistant", 
    layout="wide", 
    page_icon="🏦", 
    initial_sidebar_state="auto" 
)

# --- CLOUD FILES ---
CLOUD_FILES = {
    "ps1225app2.pdf": "https://drive.google.com/file/d/1hXqRq1d9nclU2Cfzuk-YVJ4lQ1wsN5-1/view?usp=drive_link",
    "annex-ii-reporting-instructions.pdf": "https://drive.google.com/file/d/1Ks0FMoyNYFoQq_1iE1jypayi8cNc5aVs/view?usp=sharing"
}

# --- PREMIUM GEMINI CSS (FIXED) ---
st.markdown("""
<style>
/* ===== IMPORTS ===== */
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');

/* ===== ROOT VARIABLES ===== */
:root {
    --bg-primary: #131314;
    --bg-secondary: #1e1f20;
    --bg-tertiary: #282a2c;
    --bg-elevated: #303134;
    --accent-blue: #8ab4f8;
    --accent-purple: #c58af9;
    --text-primary: #e3e3e3;
    --text-secondary: #9aa0a6;
    --text-muted: #5f6368;
    --border-subtle: rgba(255,255,255,0.1);
    --glass-bg: rgba(30,31,32,0.9);
    --glass-border: rgba(255,255,255,0.1);
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ===== GLOBAL RESET ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit branding but keep functional elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stStatusWidget"] {display: none;}

/* Keep the native sidebar toggle visible and styled */
section[data-testid="stSidebar"] > div:first-child > button {
    display: block !important;
    visibility: visible !important;
}

.main .block-container {
    padding: 2rem 3rem 10rem 3rem !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* ===== SIDEBAR STYLING ===== */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: var(--bg-secondary) !important;
    padding-top: 2rem !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 12px !important;
    transition: var(--transition-smooth) !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-elevated) !important;
    border-color: var(--accent-blue) !important;
}

/* Style the native Streamlit collapse button */
section[data-testid="stSidebar"] > div:first-child > button {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    margin: 0.5rem !important;
}

section[data-testid="stSidebar"] > div:first-child > button:hover {
    background: var(--bg-elevated) !important;
    border-color: var(--accent-blue) !important;
}

/* ===== CUSTOM MENU TOGGLE BUTTON ===== */
.menu-toggle-btn {
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 999;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    font-size: 1.25rem;
    color: var(--text-primary);
    transition: var(--transition-smooth);
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.menu-toggle-btn:hover {
    background: var(--bg-elevated);
    border-color: var(--accent-blue);
    box-shadow: 0 4px 12px rgba(138,180,248,0.2);
}

/* ===== ANIMATED GREETING ===== */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.greeting-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 45vh;
    text-align: center;
    padding: 2rem;
}

.greeting-title {
    font-size: 3rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4285f4 0%, #ea4335 40%, #fbbc04 70%, #34a853 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeInUp 0.8s ease-out, gradientShift 8s ease infinite;
    margin-bottom: 0.5rem;
}

.greeting-subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    animation: fadeInUp 1s ease-out 0.3s both;
    font-weight: 300;
}

/* ===== OMNIBAR - FIXED CENTERING (Floating Pill) ===== */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 1.5rem !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 4rem) !important;
    max-width: 48rem !important;
    z-index: 100 !important;
}

[data-testid="stChatInput"] > div {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 28px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05) !important;
    padding: 0.5rem 1rem !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: none !important;
    color: var(--text-primary) !important;
    font-size: 1rem !important;
    padding: 0.75rem 0 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

[data-testid="stChatInput"] button {
    background: var(--accent-blue) !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
}

[data-testid="stChatInput"] button svg {
    fill: var(--bg-primary) !important;
}

/* ===== TOOLS CONTAINER ===== */
.context-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.75rem;
    background: rgba(138,180,248,0.15);
    border: 1px solid var(--accent-blue);
    border-radius: 16px;
    color: var(--accent-blue);
    font-size: 0.8rem;
    margin-right: 0.5rem;
}

/* ===== CHAT MESSAGES ===== */
[data-testid="stChatMessage"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin-bottom: 1rem !important;
    max-width: 100% !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] code {
    color: var(--text-primary) !important;
}

/* ===== STATUS BADGE ===== */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(138,180,248,0.1);
    border: 1px solid rgba(138,180,248,0.3);
    border-radius: 20px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    color: var(--accent-blue);
}

/* ===== UPLOAD AREA ===== */
[data-testid="stFileUploader"] {
    background: var(--bg-secondary) !important;
    border: 2px dashed var(--border-subtle) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-blue) !important;
}

[data-testid="stFileUploader"] label {
    color: var(--text-primary) !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.25rem !important;
    font-weight: 500 !important;
    transition: var(--transition-smooth) !important;
}

.stButton > button:hover {
    background: var(--bg-elevated) !important;
    border-color: var(--accent-blue) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4285f4, #8ab4f8) !important;
    border: none !important;
    color: #131314 !important;
    font-weight: 600 !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 12px rgba(66,133,244,0.4) !important;
}

/* ===== EXPANDER ===== */
[data-testid="stExpander"] {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    color: var(--accent-blue) !important;
    font-weight: 500 !important;
}

[data-testid="stExpander"] svg {
    fill: var(--accent-blue) !important;
}

/* ===== SELECTBOX ===== */
[data-testid="stSelectbox"] {
    color: var(--text-primary) !important;
}

[data-testid="stSelectbox"] > div {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
}

/* ===== TEXT INPUT ===== */
[data-testid="stTextInput"] input {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}

/* ===== RADIO BUTTONS ===== */
[data-testid="stRadio"] label {
    color: var(--text-primary) !important;
}

/* ===== DIVIDER ===== */
hr {
    border-color: var(--border-subtle) !important;
    opacity: 0.5 !important;
}

/* ===== SPINNER ===== */
[data-testid="stSpinner"] > div {
    border-top-color: var(--accent-blue) !important;
}

/* ===== SUCCESS/WARNING/ERROR ===== */
[data-testid="stSuccess"],
[data-testid="stWarning"],
[data-testid="stError"] {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# --- IMPORTS ---
import os
import tempfile
import json
import requests
import io
import concurrent.futures
from dotenv import load_dotenv
import torch 
import re 
import chat_db 

# Initialize DB
if "db_initialized" not in st.session_state:
    try:
        chat_db.init_db()
        st.session_state.db_initialized = True
    except Exception as e:
        st.error(f"Failed to initialize database. Ensure chat_db.py exists. Error: {e}")

# Initialize states
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = None
if "tools_open" not in st.session_state:
    st.session_state.tools_open = False

load_dotenv()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.divider()
    
    mode = st.radio("AI Backend:", ("🔒 Local (Llama 3.1 8B)", "🚀 Cloud (Gemini)"))
    
    env_key = os.getenv("GOOGLE_API_KEY")
    gemini_key = None
    
    if mode == "🚀 Cloud (Gemini)":
        manual_key = st.text_input("API Key:", type="password")
        if manual_key:
            gemini_key = manual_key.strip().replace('"', '').replace("'", "")
            st.success("✅ Key Set")
        elif env_key:
            gemini_key = env_key.strip().replace('"', '').replace("'", "")
            st.success("✅ Key Loaded")
        else:
            st.warning("⚠️ No Key")
    else:
        if torch.cuda.is_available():
            st.success(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        else:
            st.warning("⚠️ CPU Mode")
    
    st.divider()
    st.markdown("### 💬 Recent Chats")
    
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = None
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.current_session_id = chat_db.create_session()
        st.session_state.selected_tool = None
        st.rerun()
    
    try:
        sessions = chat_db.get_sessions()
        for session in sessions:
            sid, title, _ = session
            col1, col2 = st.columns([5, 1])
            with col1:
                display_title = title[:18] + "..." if len(title) > 18 else title
                if st.button(f"💬 {display_title}", key=f"s_{sid}", use_container_width=True):
                    st.session_state.current_session_id = sid
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"d_{sid}"):
                    chat_db.delete_session(sid)
                    if st.session_state.current_session_id == sid:
                        st.session_state.current_session_id = None
                    st.rerun()
        
        if st.session_state.current_session_id is None:
            if sessions:
                st.session_state.current_session_id = sessions[0][0]
            else:
                st.session_state.current_session_id = chat_db.create_session()
    except Exception as e:
        st.error(f"DB Error: {e}")

# --- BACKEND FUNCTIONS ---
def format_drive_url(url):
    if "drive.google.com" in url and "/view" in url:
        try:
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except:
            return url
    return url

@st.cache_data(show_spinner=False)
def fetch_pdf_content(url):
    download_url = format_drive_url(url)
    response = requests.get(download_url)
    response.raise_for_status()
    return response.content

@st.cache_resource
def load_embedding_model():
    from langchain_huggingface import HuggingFaceEmbeddings
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

@st.cache_resource(show_spinner=False)
def process_pdfs(_files_data):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    
    my_bar = st.progress(0, text="Processing...")
    all_docs = []
    
    # Calculate step to prevent >100 progress
    step = 40.0 / len(_files_data) if _files_data else 0
    
    for i, file_data in enumerate(_files_data):
        # Progress calculation
        progress_val = min(10 + int(i * step), 50)
        my_bar.progress(progress_val, text=f"Reading {getattr(file_data, 'name', 'document')}...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_data.read())
            tmp_file_path = tmp_file.name
        loader = PyPDFLoader(tmp_file_path)
        all_docs.extend(loader.load())
    
    my_bar.progress(50, text="Splitting...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(all_docs)
    
    my_bar.progress(75, text="Embedding...")
    embeddings_model = load_embedding_model()
    VECTOR_DB_PATH = "./chroma_db_cache"
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings_model, persist_directory=VECTOR_DB_PATH)
    
    my_bar.progress(100, text="Done!")
    my_bar.empty()
    return vectorstore

def get_llm(mode):
    if mode == "🚀 Cloud (Gemini)":
        from langchain_google_genai import ChatGoogleGenerativeAI
        if not gemini_key:
            st.error("⚠️ API Key missing")
            st.stop()
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_key, temperature=0)
    else:
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model="llama3.1", temperature=0, keep_alive="1h")

def load_from_drive():
    files_to_process = []
    with st.status("Loading from Drive...", expanded=True) as status:
        st.write("🚀 Downloading...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_name = {
                executor.submit(fetch_pdf_content, url): name 
                for name, url in CLOUD_FILES.items()
            }
            for future in concurrent.futures.as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    content = future.result()
                    file_obj = io.BytesIO(content)
                    file_obj.name = name
                    files_to_process.append(file_obj)
                    st.write(f"✅ {name}")
                except Exception as e:
                    st.error(f"❌ {name}: {e}")
        
        if len(files_to_process) == len(CLOUD_FILES):
            st.write("⚙️ Processing...")
            st.session_state.vectorstore = process_pdfs(files_to_process)
            status.update(label="✅ Ready!", state="complete")
            st.rerun()
        else:
            status.update(label="❌ Failed", state="error")

# --- MAIN INTERFACE ---
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None

# Auto-Load Logic
VECTOR_DB_PATH = "./chroma_db_cache"
if st.session_state.vectorstore is None and os.path.exists(VECTOR_DB_PATH) and os.path.isdir(VECTOR_DB_PATH):
    try:
        from langchain_community.vectorstores import Chroma
        embeddings_model = load_embedding_model()
        st.session_state.vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings_model)
        st.toast("⚡ Engine Ready (Loaded from Local Cache)", icon="🚀")
    except Exception:
        pass

# === HAMBURGER MENU BUTTON (Always Visible) ===
st.markdown("""
<button class="menu-toggle-btn" onclick="
    const sidebar = window.parent.document.querySelector('[data-testid=stSidebar]');
    const btn = window.parent.document.querySelector('button[kind=header]');
    if (btn) btn.click();
    else if (sidebar) sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
" title="Toggle Menu">☰</button>
""", unsafe_allow_html=True)

# === LANDING PAGE ===
if st.session_state.vectorstore is None:
    st.markdown("""
    <div class="greeting-container">
        <div class="greeting-title">Hi Arthur</div>
        <div class="greeting-subtitle">Where should we start?</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        uploaded_files = st.file_uploader(
            "📂 Drop your PDFs here",
            type="pdf",
            accept_multiple_files=True
        )
        if uploaded_files:
            with st.spinner("Processing..."):
                st.session_state.vectorstore = process_pdfs(uploaded_files)
            st.rerun()
        
        st.write("")
        if st.button("☁️ Load from Google Drive", use_container_width=True, type="primary"):
            load_from_drive()
        st.caption("Pre-configured: PRA Rulebook + COREP Instructions")

# === CHAT INTERFACE ===
else:
    # Status + Tools Row
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
        <div class="status-badge">✨ Ready to assist</div>
    </div>
    """, unsafe_allow_html=True)
    
    tools = {
        "📊 Risk Analysis": "Risk Analysis",
        "🏦 Own Funds (CA1)": "Own Funds (CA1)",
        "📋 Regulatory Compliance": "Regulatory Compliance",
        "💰 Capital Adequacy": "Capital Adequacy"
    }
    
    with st.expander("🛠️ Select Analysis Tool", expanded=False):
        cols = st.columns(4)
        for i, (label, value) in enumerate(tools.items()):
            with cols[i]:
                is_selected = st.session_state.selected_tool == value
                btn_type = "primary" if is_selected else "secondary"
                if st.button(label, key=f"tool_{i}", use_container_width=True, type=btn_type):
                    st.session_state.selected_tool = value
                    st.rerun()
    
    if st.session_state.selected_tool:
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0;">
            <span class="context-badge">🎯 Context: {st.session_state.selected_tool}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Chat History
    messages = chat_db.get_messages(st.session_state.current_session_id)
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat Input (styled via CSS as floating pill)
    placeholder = f"Ask about {st.session_state.selected_tool or 'COREP reporting'}..."
    if query := st.chat_input(placeholder):
        with st.chat_message("user"):
            st.markdown(query)
        
        chat_db.save_message(st.session_state.current_session_id, "user", query)
        
        llm = get_llm(mode)
        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        with st.spinner("Thinking..."):
            try:
                docs = retriever.invoke(query)
                context = "\n\n".join([doc.page_content for doc in docs])
                
                recent_history = messages[-5:]
                history_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in recent_history])
                
                tool_context = st.session_state.selected_tool or "general COREP reporting"
                
                # ========================================
                # DYNAMIC CONTEXT SWITCHING
                # ========================================
                
                # Check if Liquidity or Own Funds context
                is_liquidity_context = tool_context in ["Own Funds (CA1)", "Regulatory Compliance"] or "liquidity" in query.lower() or "lcr" in query.lower() or "hqla" in query.lower()
                
                if is_liquidity_context:
                    # ===== LIQUIDITY / LCR RULES =====
                    rules_block = """===== LCR / LIQUIDITY RULES =====

RULE 1 - HQLA CLASSIFICATION:
• Level 1 (0% haircut): Cash, Central Bank Reserves, Govt Bonds (0% RW sovereigns)
• Level 2A (15% haircut): Covered Bonds (AA-), Corporate Bonds (AA-), Govt Bonds (20% RW)
• Level 2B (50% haircut): Corporate Bonds (A+ to BBB-), **EQUITIES (Major Index)**, RMBS

RULE 2 - EQUITIES ARE LEVEL 2B:
• Equities listed on major index (FTSE, S&P, etc.) = Level 2B = 50% haircut
• Equities are NEVER Level 1 or Level 2A
• Max 15% of total HQLA can be Level 2B

RULE 3 - TEMPLATES:
• LCR Calculation → C 72.00, C 73.00, C 74.00
• NSFR → C 80.00, C 81.00
• Own Funds → C 01.00, C 02.00, C 03.00"""

                    example_block = """===== EXAMPLE =====

USER: How should a bank classify FTSE 100 equities for LCR purposes?

### REASONING
Step 1: Asset type = Equities (listed on major index FTSE 100)
Step 2: Equities → Level 2B (NOT Level 1, NOT Level 2A)
Step 3: Level 2B haircut = 50%

### ANSWER
| Field | Value |
|-------|-------|
| **Template** | C 72.00 (LCR) |
| **Classification** | Level 2B HQLA |
| **Haircut** | 50% |
| **Reasoning** | Major index equities qualify as Level 2B per CRR Art. 12; subject to 50% haircut and 15% cap |"""

                else:
                    # ===== CREDIT RISK RULES (Default) =====
                    rules_block = """===== CREDIT RISK RULES (STANDARDISED) =====

RULE 1 - APPROACH GATE:
• Standardised Approach → C 07.00 ONLY → REJECT all IRB templates (C 08.xx)
• IRB Approach → C 08.01, C 08.02 → REJECT C 07.00

RULE 2 - EXPOSURE CLASSIFICATION:
• SME with exposure < €1 million → Retail Exposure Class → 75% RW
• SME with exposure ≥ €1 million → Corporate Exposure Class → 100% RW
• Residential Mortgage LTV ≤ 80% → Secured by Real Estate → 35% RW
• Residential Mortgage LTV > 80% → Higher RW applies

RULE 3 - DEFAULT THRESHOLD:
• Days Past Due < 90 → Non-Defaulted → Column 0010
• Days Past Due ≥ 90 → Defaulted → Column 0020 → 100-150% RW

RULE 4 - RISK WEIGHTS:
• Sovereigns (EU/UK, 0% RW): 0%
• Institutions (rated): 20-50%
• Corporates (unrated): 100%
• Retail/SME (<€1m): 75%
• Mortgages (LTV≤80%): 35%"""

                    example_block = """===== EXAMPLE =====

USER: A Standardised Approach bank has a €500,000 loan to an SME. Which template and risk weight?

### REASONING
Step 1: Approach = Standardised → Use C 07.00 → Reject IRB templates
Step 2: Exposure = €500,000 < €1 million → Classify as Retail
Step 3: Retail exposure → Risk Weight 75%

### ANSWER
| Field | Value |
|-------|-------|
| **Template** | C 07.00 |
| **Classification** | Retail (SME < €1m) |
| **Risk Weight** | 75% |
| **Reasoning** | SME exposure below €1m threshold qualifies as Retail per CRR Art. 123; 75% RW applies |"""

                full_prompt = f"""You are a COREP Compliance Validator. Output ONLY structured data. NO conversational text.

{rules_block}

{example_block}

===== YOUR TASK =====

Active Context: {tool_context}

REGULATORY DOCUMENTS:
{context}

CONVERSATION HISTORY:
{history_str}

USER QUESTION: {query}

INSTRUCTIONS:
1. Show brief ### REASONING (3 steps max)
2. Output ### ANSWER as a table with these fields:
   - Template: [Code]
   - Classification: [Class/Level]
   - Risk Weight/Haircut: [%]
   - Reasoning: [1-sentence justification with CRR Article]
3. Do NOT write conversational paragraphs
4. If data is missing, output "INSUFFICIENT DATA" and list what's needed"""
                
                response = llm.invoke(full_prompt)
                content = response.content if hasattr(response, 'content') else str(response)
                
                with st.chat_message("assistant"):
                    st.markdown(content)
                    
                    with st.expander("📚 Sources"):
                        for i, doc in enumerate(docs):
                            st.caption(f"**Source {i+1}** (Page {doc.metadata.get('page','?')})")
                            st.text(doc.page_content[:200] + "...")
                
                chat_db.save_message(st.session_state.current_session_id, "assistant", content)
                
                # Auto-Rename if first message
                if len(messages) == 0:
                    try:
                        title_prompt = f"Summarize this question into a 3-4 word title: '{query}'"
                        title_resp = llm.invoke(title_prompt)
                        new_title = (title_resp.content if hasattr(title_resp, 'content') else str(title_resp)).strip().replace('"', '')
                        chat_db.update_session_title(st.session_state.current_session_id, new_title)
                        st.rerun()
                    except:
                        pass
                        
            except Exception as e:
                st.error(f"Error: {e}")
