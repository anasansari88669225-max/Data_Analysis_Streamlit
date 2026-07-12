import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from groq import Groq
import io
import time

# --- 🔥 PERMANENT API KEY ---
API_KEY = "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"

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Data Analyst Pro", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# --- 🎨 PREMIUM COLORFUL UI WITH ANIMATIONS ---
st.markdown("""
    <style>
    /* === GLOBAL ANIMATIONS === */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(138, 43, 226, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 20, 147, 0.8); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes blink {
        50% { border-color: transparent; }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
    
    @keyframes ripple {
        0% { transform: scale(0); opacity: 1; }
        100% { transform: scale(4); opacity: 0; }
    }

    /* === MAIN CONTAINER === */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        animation: fadeInUp 1s ease-out;
    }
    
    /* === ANIMATED BACKGROUND === */
    .stApp {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #4facfe 75%, 
            #667eea 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    /* === GLASSMORPHISM EFFECT === */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        padding: 25px;
        margin: 15px 0;
        animation: fadeInUp 0.8s ease-out;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* === COLORFUL METRICS === */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 2px solid rgba(255, 255, 255, 0.4);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: bounceIn 0.6s ease-out;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    .stMetric:hover {
        transform: scale(1.05) rotate(1deg);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric .metric-value {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
    }
    
    /* === HEADERS === */
    h1 {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out, float 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    h2 {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        animation: slideInLeft 0.8s ease-out;
    }
    
    h3 {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        animation: slideInRight 0.8s ease-out;
    }
    
    /* === BUTTONS === */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.5);
        border-radius: 50px;
        padding: 12px 35px;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.6);
        border: 2px solid rgba(255, 255, 255, 0.8);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(102, 126, 234, 0.95) 0%, 
            rgba(118, 75, 162, 0.95) 50%, 
            rgba(240, 147, 251, 0.95) 100%);
        backdrop-filter: blur(20px);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stAlert {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 15px;
        animation: glow 2s ease-in-out infinite;
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 12px 25px;
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%) !important;
        animation: pulse 2s ease-in-out infinite;
        border: 2px solid white;
        box-shadow: 0 0 30px rgba(240, 147, 251, 0.8);
    }
    
    /* === CHATBOT STYLES === */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 25px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin: 20px 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 15px 0;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideInRight 0.5s ease-out;
        font-size: 1.05rem;
        line-height: 1.6;
        position: relative;
        overflow: hidden;
    }
    
    .user-message::before {
        content: '👤';
        position: absolute;
        left: -35px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 15px 0;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
        animation: slideInLeft 0.5s ease-out;
        font-size: 1.05rem;
        line-height: 1.6;
        position: relative;
        overflow: hidden;
    }
    
    .ai-message::before {
        content: '🤖';
        position: absolute;
        right: -35px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
    }
    
    .typing-indicator {
        display: inline-block;
        padding: 10px 15px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        margin: 10px 0;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .typing-indicator span {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: white;
        margin: 0 3px;
        animation: float 1.4s ease-in-out infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    /* === DATAFRAME === */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* === ALERTS === */
    .stAlert {
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        animation: fadeInUp 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* === SELECTBOX === */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }
    
    /* === TEXT INPUT === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.4) !important;
    }
    
    /* === FILE UPLOADER === */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.15);
        border: 2px dashed rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
        animation: pulse 3s ease-in-out infinite;
    }
    
    .stFileUploader:hover {
        border: 2px dashed rgba(255, 255, 255, 0.9);
        background: rgba(255, 255, 255, 0.25);
        transform: scale(1.02);
    }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* === WELCOME SCREEN === */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        animation: fadeInUp 1s ease-out;
    }
    
    .welcome-emoji {
        font-size: 6rem;
        animation: float 3s ease-in-out infinite;
        display: inline-block;
    }
    
    .welcome-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 30px 0;
        text-shadow: 0 0 40px rgba(255, 255, 255, 0.5);
    }
    
    .welcome-subtitle {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 40px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* === LOADING SPINNER === */
    .custom-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 30px;
    }
    
    .spinner-ring {
        width: 60px;
        height: 60px;
        border: 5px solid rgba(255, 255, 255, 0.3);
        border-top: 5px solid white;
        border-radius: 50%;
        animation: rotate 1.5s linear infinite;
    }
    
    /* === CHAT INPUT === */
    .chat-input-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* === FEATURE CARDS === */
    .feature-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        text-align: center;
        transition: all 0.4s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.7);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 15px;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* === DIVIDERS === */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.5) 50%, 
            transparent 100%);
        margin: 30px 0;
        animation: shimmer 3s infinite;
    }
    
    /* === PLOTLY CHARTS === */
    .stPlotlyChart {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.8s ease-out;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "df" not in st.session_state: st.session_state.df = None
if "chart_explanation" not in st.session_state: st.session_state.chart_explanation = None
if "chat_messages" not in st.session_state: 
    st.session_state.chat_messages = [
        {"role": "ai", "content": "👋 Assalam o Alaikum! Main aapka AI Data Analyst hoon. Apna dataset upload karein aur mujhse koi bhi sawaal poochein - main aapki puri madad karunga! 🚀"}
    ]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 style="text-align: center; animation: float 3s ease-in-out infinite;">🧠✨ AI Data Pro</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<div class="glass-card"><h3 style="color: white; text-align: center;">🔑 API Status</h3><p style="color: white; text-align: center; font-size: 1.1rem;">✅ Active & Ready</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<h3 style="color: white; text-align: center;">📁 Upload Dataset</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file:
        try:
            with st.spinner("🔄 Loading dataset..."):
                time.sleep(0.5)
                st.session_state.df = pd.read_csv(uploaded_file)
                st.success("✅ Dataset loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

# --- HELPER FUNCTIONS ---
def get_context(df):
    """Dataset ka summary AI ko bhejne ke liye"""
    buffer = io.StringIO()
    buffer.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n")
    buffer.write(f"Columns: {', '.join(df.columns)}\n")
    buffer.write(f"Missing Values:\n{df.isnull().sum().to_string()}\n")
    
    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) > 0:
        buffer.write(f"Numeric Stats:\n{df[num_cols].describe().to_string()}\n")
        
    cat_cols = df.select_dtypes(exclude=np.number).columns
    for col in cat_cols:
        buffer.write(f"Category '{col}' distribution:\n{df[col].value_counts().head(5).to_string()}\n")
        
    buffer.write(f"Sample Data:\n{df.head(3).to_string()}")
    return buffer.getvalue()

def call_ai(prompt):
    """Groq API ko call karne ka safe function"""
    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert business data analyst. Provide clear, concise, and accurate answers based ONLY on the provided data context. Be friendly and helpful."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# --- MAIN APP ---
if st.session_state.df is not None:
    df = st.session_state.df
    context = get_context(df)
    
    # Animated Header
    st.markdown('<h1>🧠✨ AI Data Analyst Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 1.3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 30px;">Your Intelligent Data Analysis Companion 🚀</p>', unsafe_allow_html=True)
    
    # Tabs with Icons
    tab1, tab2, tab3 = st.tabs(["📊 Dataset Overview", "📈 Analysis & Charts", "💬 AI Chatbot"])
    
    # ==========================================
    # TAB 1: DATASET OVERVIEW
    # ==========================================
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("📊 Dataset Summary")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div style="animation: bounceIn 0.6s ease-out;">', unsafe_allow_html=True)
            st.metric("🔢 Total Rows", f"{df.shape[0]:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div style="animation: bounceIn 0.7s ease-out;">', unsafe_allow_html=True)
            st.metric("📋 Total Columns", f"{df.shape[1]:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div style="animation: bounceIn 0.8s ease-out;">', unsafe_allow_html=True)
            st.metric("⚠️ Missing Values", f"{int(df.isnull().sum().sum()):,}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div style="animation: bounceIn 0.9s ease-out;">', unsafe_allow_html=True)
            st.metric("🔄 Duplicate Rows", f"{int(df.duplicated().sum()):,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.expander("🔍 View Full Dataset", expanded=False):
            st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🏷️ Data Types")
            st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Type'}))
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📉 Missing Values per Column")
            st.dataframe(df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing'}))
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # TAB 2: ANALYSIS & CHARTS
    # ==========================================
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("📈 Statistical Analysis")
        num_df = df.select_dtypes(include=np.number)
        if not num_df.empty:
            st.dataframe(num_df.describe().round(2), use_container_width=True)
        else:
            st.info("ℹ️ No numeric columns found for statistical analysis.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🎨 Interactive Visualization")
        
        c1, c2, c3 = st.columns(3)
        chart_type = c1.selectbox("📊 Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])
        cols = df.columns.tolist()
        x_col = c2.selectbox("📍 X-Axis", cols)
        y_col = c3.selectbox("📍 Y-Axis", ["None"] + cols)
        
        fig = None
        try:
            if chart_type == "Bar Chart" and y_col != "None": fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            elif chart_type == "Line Chart" and y_col != "None": fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            elif chart_type == "Scatter Plot" and y_col != "None": fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            elif chart_type == "Pie Chart": fig = px.pie(df, names=x_col, title=f"Distribution of {x_col}")
            elif chart_type == "Histogram": fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
            
            if fig:
                fig.update_layout(
                    template="plotly_white",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=14)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                if st.button("✨ Explain this Chart with AI"):
                    with st.spinner("🤖 AI is analyzing the chart..."):
                        prompt = f"Dataset Context:\n{context}\n\nA {chart_type} was generated with X-axis: '{x_col}' and Y-axis: '{y_col}'. Provide a short, simple explanation of the findings, trends, and business insights from this chart."
                        st.session_state.chart_explanation = call_ai(prompt)
                
                if st.session_state.chart_explanation:
                    st.markdown('<div class="ai-message">', unsafe_allow_html=True)
                    st.markdown("💡 **AI Explanation:**")
                    st.write(st.session_state.chart_explanation)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please select a valid Y-axis for this chart type.")
        except Exception as e:
            st.error(f"❌ Error generating chart: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # TAB 3: AI CHATBOT (ChatGPT Style)
    # ==========================================
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("💬 AI Data Chatbot")
        st.caption("🤖 ChatGPT-style AI assistant - Apne dataset ke baare mein kuch bhi poochein!")
        
        # Chat Messages Display
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat Input
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        user_input = st.text_input("", placeholder="💭 Apna sawaal yahan likhein... (e.g., 'Which product has highest sales?')", label_visibility="collapsed")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            send_button = st.button("🚀 Send Message", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Suggestions
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💡 Quick Suggestions")
        sug1, sug2, sug3, sug4 = st.columns(4)
        with sug1:
            if st.button("📊 Top 5 Products", use_container_width=True):
                user_input = "Top 5 products kya hain?"
                send_button = True
        with sug2:
            if st.button("📈 Sales Trend", use_container_width=True):
                user_input = "Sales ka trend kya hai?"
                send_button = True
        with sug3:
            if st.button("🏆 Best Customer", use_container_width=True):
                user_input = "Best customer kaunsa hai?"
                send_button = True
        with sug4:
            if st.button("📉 Missing Data", use_container_width=True):
                user_input = "Missing data ke baare mein batao"
                send_button = True
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process User Input
        if send_button and user_input:
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            # Show typing indicator
            with st.spinner("🤖 AI is thinking..."):
                time.sleep(0.5)
                
                # Get AI response
                prompt = f"""Dataset Context:
{context}

User Question: {user_input}

Provide a clear, accurate, and helpful answer based on the dataset. Be conversational and friendly."""
                
                ai_response = call_ai(prompt)
                
                # Add AI response
                st.session_state.chat_messages.append({"role": "ai", "content": ai_response})
            
            # Rerun to show new messages
            st.rerun()

else:
    # Welcome Screen
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-emoji">🧠✨</div>
        <div class="welcome-title">AI Data Analyst Pro</div>
        <div class="welcome-subtitle">Your Intelligent Data Analysis Companion</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Smart Analysis</div>
            <div class="feature-desc">Advanced statistical analysis with beautiful visualizations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Chatbot</div>
            <div class="feature-desc">ChatGPT-style AI assistant for instant answers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Beautiful UI</div>
            <div class="feature-desc">Stunning colorful interface with smooth animations</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Please upload a CSV file from the sidebar to begin your data analysis journey!")