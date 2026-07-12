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

# --- 🎨 PROFESSIONAL DARK THEME ---
st.markdown("""
    <style>
    /* === COLOR VARIABLES === */
    :root {
        --bg-main: #0F172A;
        --bg-sidebar: #1E293B;
        --bg-card: #111827;
        --primary: #7C3AED;
        --primary-hover: #8B5CF6;
        --secondary: #06B6D4;
        --success: #22C55E;
        --warning: #F59E0B;
        --error: #EF4444;
        --text-main: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --border: #1E293B;
        --chart-grid: #374151;
    }
    
    /* === ANIMATIONS === */
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
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* === MAIN CONTAINER === */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* === MAIN BACKGROUND === */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #374151;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #F8FAFC !important;
    }
    
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #94A3B8 !important;
    }
    
    /* === GLASS CARD === */
    .glass-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #7C3AED, #06B6D4, #7C3AED);
        background-size: 200% 100%;
        animation: gradientShift 3s ease infinite;
    }
    
    .glass-card:hover {
        border-color: #7C3AED;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.2);
        transform: translateY(-2px);
    }
    
    /* === METRICS === */
    .stMetric {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #7C3AED, #06B6D4);
    }
    
    .stMetric:hover {
        border-color: #7C3AED;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.3);
        transform: translateY(-3px);
    }
    
    .stMetric label {
        color: #CBD5E1 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* === HEADERS === */
    h1 {
        background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    h2 {
        color: #F8FAFC !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        padding-left: 16px;
        animation: slideInLeft 0.6s ease-out;
    }
    
    h2::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 80%;
        background: linear-gradient(180deg, #7C3AED, #06B6D4);
        border-radius: 2px;
    }
    
    h3 {
        color: #CBD5E1 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        animation: slideInRight 0.6s ease-out;
    }
    
    p, span, div {
        color: #F8FAFC;
    }
    
    /* === BUTTONS === */
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
        color: #F8FAFC !important;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.3px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #22D3EE 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1E293B;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        color: #94A3B8 !important;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #1E293B;
        color: #F8FAFC !important;
        border-color: #374151;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid transparent !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
    }
    
    /* === CHATBOT STYLES === */
    .chat-container {
        background: #111827;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #1E293B;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 16px;
    }
    
    .user-message {
        background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
        color: #F8FAFC;
        padding: 14px 18px;
        border-radius: 16px 16px 4px 16px;
        margin: 12px 0;
        margin-left: 15%;
        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.3);
        animation: slideInRight 0.4s ease-out;
        font-size: 0.95rem;
        line-height: 1.6;
        position: relative;
    }
    
    .user-message::after {
        content: '';
        position: absolute;
        top: 12px;
        right: -8px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-left-color: #8B5CF6;
        border-right: 0;
    }
    
    .ai-message {
        background: #1E293B;
        color: #F8FAFC;
        padding: 14px 18px;
        border-radius: 16px 16px 16px 4px;
        margin: 12px 0;
        margin-right: 15%;
        border: 1px solid #374151;
        border-left: 3px solid #06B6D4;
        box-shadow: 0 2px 10px rgba(6, 182, 212, 0.1);
        animation: slideInLeft 0.4s ease-out;
        font-size: 0.95rem;
        line-height: 1.6;
        position: relative;
    }
    
    .ai-message::after {
        content: '';
        position: absolute;
        top: 12px;
        left: -8px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-right-color: #06B6D4;
        border-left: 0;
    }
    
    .typing-indicator {
        display: inline-flex;
        gap: 4px;
        padding: 12px 16px;
        background: #1E293B;
        border-radius: 16px;
        border: 1px solid #374151;
        margin: 8px 0;
    }
    
    .typing-indicator span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #06B6D4;
        animation: typing 1.4s ease-in-out infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    /* === DATAFRAME === */
    .stDataFrame {
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* === ALERTS === */
    .stAlert {
        border-radius: 12px;
        border: 1px solid;
        background: #111827 !important;
    }
    
    .stSuccess {
        border-color: #22C55E !important;
        color: #22C55E !important;
        background: rgba(34, 197, 94, 0.1) !important;
    }
    
    .stWarning {
        border-color: #F59E0B !important;
        color: #F59E0B !important;
        background: rgba(245, 158, 11, 0.1) !important;
    }
    
    .stError {
        border-color: #EF4444 !important;
        color: #EF4444 !important;
        background: rgba(239, 68, 68, 0.1) !important;
    }
    
    .stInfo {
        border-color: #06B6D4 !important;
        color: #06B6D4 !important;
        background: rgba(6, 182, 212, 0.1) !important;
    }
    
    /* === SELECTBOX === */
    .stSelectbox > div > div {
        background: #111827 !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #7C3AED !important;
    }
    
    .stSelectbox label {
        color: #CBD5E1 !important;
    }
    
    /* === TEXT INPUT === */
    .stTextInput input,
    .stTextArea textarea {
        background: #111827 !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
        outline: none !important;
    }
    
    .stTextInput label,
    .stTextArea label {
        color: #CBD5E1 !important;
    }
    
    /* === FILE UPLOADER === */
    .stFileUploader {
        background: #111827;
        border: 2px dashed #374151;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #7C3AED;
        background: rgba(124, 58, 237, 0.05);
    }
    
    .stFileUploader label {
        color: #CBD5E1 !important;
    }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0F172A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #374151;
        border-radius: 5px;
        border: 2px solid #0F172A;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #7C3AED;
    }
    
    /* === WELCOME SCREEN === */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .welcome-emoji {
        font-size: 5rem;
        animation: float 3s ease-in-out infinite;
        display: inline-block;
        filter: drop-shadow(0 0 20px rgba(124, 58, 237, 0.5));
    }
    
    .welcome-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 24px 0;
    }
    
    .welcome-subtitle {
        font-size: 1.25rem;
        color: #94A3B8;
        margin-bottom: 32px;
    }
    
    /* === FEATURE CARDS === */
    .feature-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 32px 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #7C3AED, #06B6D4);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        border-color: #7C3AED;
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.2);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 16px;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 15px rgba(124, 58, 237, 0.4));
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 12px;
    }
    
    .feature-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* === DIVIDERS === */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #374151, transparent);
        margin: 24px 0;
    }
    
    /* === API STATUS BADGE === */
    .api-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #22C55E;
        color: #22C55E;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .api-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #22C55E;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    /* === DATA QUALITY SCORE === */
    .quality-score {
        background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 16px 0;
    }
    
    .quality-score h3 {
        color: white !important;
        margin: 0 0 10px 0;
    }
    
    .quality-score .score {
        font-size: 3rem;
        font-weight: 800;
        color: white;
    }
    
    /* === CORRELATION HEATMAP === */
    .heatmap-container {
        background: #111827;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #1E293B;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background: #111827 !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #1E293B !important;
        border-color: #7C3AED !important;
    }
    
    /* === DOWNLOAD BUTTON === */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #22C55E 0%, #06B6D4 100%) !important;
        color: #F8FAFC !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #16A34A 0%, #0891B2 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "df" not in st.session_state: 
    st.session_state.df = None
if "chart_explanation" not in st.session_state: 
    st.session_state.chart_explanation = None
if "chat_messages" not in st.session_state: 
    st.session_state.chat_messages = [
        {"role": "ai", "content": "👋 Assalam o Alaikum! Main aapka AI Data Analyst hoon. Dataset upload karein aur koi bhi sawaal poochein! 🚀"}
    ]

# --- HELPER FUNCTIONS ---
def get_context(df):
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

def calculate_data_quality(df):
    """Data quality score calculate karta hai"""
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    missing_pct = (missing_cells / total_cells) * 100 if total_cells > 0 else 0
    duplicate_pct = (duplicate_rows / df.shape[0]) * 100 if df.shape[0] > 0 else 0
    
    # Quality score calculation
    quality_score = 100 - (missing_pct * 0.5) - (duplicate_pct * 0.3)
    return max(0, min(100, quality_score))

def call_ai(prompt):
    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert business data analyst. Provide clear, concise, and accurate answers based ONLY on the provided data context. Be friendly and helpful. Respond in the same language as the user."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 style="text-align: center; font-size: 2rem;">🧠 AI Data Pro</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="api-badge">API Active</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📁 Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file:
        try:
            with st.spinner("🔄 Loading..."):
                time.sleep(0.5)
                st.session_state.df = pd.read_csv(uploaded_file)
                st.success("✅ Dataset loaded!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- MAIN APP ---
if st.session_state.df is not None:
    df = st.session_state.df
    context = get_context(df)
    
    st.markdown('<h1>🧠 AI Data Analyst Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;">Your Intelligent Data Analysis Companion</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analysis", "🔗 Correlations", "💬 AI Chat"])
    
    # === TAB 1: DATASET OVERVIEW ===
    with tab1:
        # Data Quality Score
        quality_score = calculate_data_quality(df)
        st.markdown(f'<div class="quality-score"><h3>📊 Data Quality Score</h3><div class="score">{quality_score:.1f}%</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("📊 Dataset Summary")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Rows", f"{df.shape[0]:,}")
        with c2:
            st.metric("Total Columns", f"{df.shape[1]:,}")
        with c3:
            st.metric("Missing Values", f"{int(df.isnull().sum().sum()):,}")
        with c4:
            st.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.expander("🔍 View Full Dataset"):
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
            st.subheader("📉 Missing Values")
            st.dataframe(df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing'}))
            st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 2: ANALYSIS & CHARTS ===
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("📈 Statistical Analysis")
        num_df = df.select_dtypes(include=np.number)
        if not num_df.empty:
            st.dataframe(num_df.describe().round(2), use_container_width=True)
        else:
            st.info("ℹ️ No numeric columns found.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🎨 Interactive Visualization")
        
        c1, c2, c3 = st.columns(3)
        chart_type = c1.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"])
        cols = df.columns.tolist()
        x_col = c2.selectbox("X-Axis", cols)
        y_col = c3.selectbox("Y-Axis", ["None"] + cols)
        
        fig = None
        try:
            if chart_type == "Bar Chart" and y_col != "None": 
                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            elif chart_type == "Line Chart" and y_col != "None": 
                fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            elif chart_type == "Scatter Plot" and y_col != "None": 
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            elif chart_type == "Pie Chart": 
                fig = px.pie(df, names=x_col, title=f"Distribution of {x_col}")
            elif chart_type == "Histogram": 
                fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
            elif chart_type == "Box Plot" and y_col != "None":
                fig = px.box(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            
            if fig:
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='#111827',
                    paper_bgcolor='#111827',
                    font=dict(color='#F8FAFC', size=13),
                    title_font=dict(size=18, color='#F8FAFC'),
                    xaxis=dict(gridcolor='#374151'),
                    yaxis=dict(gridcolor='#374151'),
                    legend=dict(bgcolor='rgba(0,0,0,0)')
                )
                fig.update_traces(marker=dict(color='#7C3AED', line=dict(color='#06B6D4', width=1)))
                st.plotly_chart(fig, use_container_width=True)
                
                if st.button("✨ Explain with AI"):
                    with st.spinner("🤖 AI analyzing..."):
                        prompt = f"Dataset Context:\n{context}\n\nA {chart_type} was generated with X: '{x_col}' and Y: '{y_col}'. Provide key insights and business implications."
                        st.session_state.chart_explanation = call_ai(prompt)
                
                if st.session_state.chart_explanation:
                    st.markdown('<div class="ai-message">', unsafe_allow_html=True)
                    st.markdown("💡 **AI Insights:**")
                    st.write(st.session_state.chart_explanation)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please select a valid Y-axis.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 3: CORRELATIONS ===
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🔗 Correlation Analysis")
        
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 1:
            st.markdown("### Correlation Heatmap")
            corr_matrix = df[num_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="Feature Correlations"
            )
            fig_corr.update_layout(
                plot_bgcolor='#111827',
                paper_bgcolor='#111827',
                font=dict(color='#F8FAFC')
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.markdown("### 🤖 AI Correlation Insights")
            if st.button("🔍 Analyze Correlations"):
                with st.spinner("Analyzing..."):
                    prompt = f"Dataset Context:\n{context}\n\nCorrelation Matrix:\n{corr_matrix.to_string()}\n\nAnalyze the strongest positive and negative correlations. What do they mean for the business?"
                    st.info(call_ai(prompt))
        else:
            st.info("ℹ️ Need at least 2 numeric columns for correlation analysis.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 4: AI CHATBOT ===
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("💬 AI Data Chatbot")
        st.caption("🤖 Ask anything about your data!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat Display
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat Input
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        user_input = st.text_input("Ask a question", placeholder="💭 Type your question here...", label_visibility="collapsed", key="chat_input")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            send_button = st.button("🚀 Send", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process Message
        if send_button and user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            with st.spinner(""):
                time.sleep(0.3)
                prompt = f"""Dataset Context:
{context}

User Question: {user_input}

Provide a clear, accurate answer based on the dataset. Be conversational and helpful."""
                ai_response = call_ai(prompt)
                st.session_state.chat_messages.append({"role": "ai", "content": ai_response})
            
            st.rerun()
    
    # Download Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            "📥 Download Dataset",
            df.to_csv(index=False).encode("utf-8"),
            "dataset.csv",
            "text/csv",
            use_container_width=True
        )

else:
    # Welcome Screen
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-emoji">🧠✨</div>
        <div class="welcome-title">AI Data Analyst Pro</div>
        <div class="welcome-subtitle">Your Intelligent Data Analysis Companion</div>
    </div>
    """, unsafe_allow_html=True)
    
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
            <div class="feature-icon">🔗</div>
            <div class="feature-title">Correlations</div>
            <div class="feature-desc">Discover hidden patterns and relationships in data</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Please upload a CSV file from the sidebar to begin!")