import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from groq import Groq
import io
import time
import json

# --- 🔥 PERMANENT API KEY ---
API_KEY = "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"

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Data Analyst Pro", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# --- 🎨 PROFESSIONAL DARK THEME (Same as before) ---
st.markdown("""
    <style>
    :root {
        --bg-main: #0F172A; --bg-sidebar: #1E293B; --bg-card: #111827;
        --primary: #7C3AED; --primary-hover: #8B5CF6; --secondary: #06B6D4;
        --success: #22C55E; --warning: #F59E0B; --error: #EF4444;
        --text-main: #F8FAFC; --text-secondary: #CBD5E1; --text-muted: #94A3B8;
        --border: #1E293B; --chart-grid: #374151;
    }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideInLeft { from { opacity: 0; transform: translateX(-50px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes slideInRight { from { opacity: 0; transform: translateX(50px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.9; } }
    @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    @keyframes typing { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-10px); } }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; animation: fadeInUp 0.8s ease-out; }
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #374151; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #F8FAFC !important; }
    [data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #94A3B8 !important; }
    .glass-card { background: #111827; border: 1px solid #1E293B; border-radius: 16px; padding: 24px; margin: 16px 0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); animation: fadeInUp 0.6s ease-out; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; }
    .glass-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #7C3AED, #06B6D4, #7C3AED); background-size: 200% 100%; animation: gradientShift 3s ease infinite; }
    .glass-card:hover { border-color: #7C3AED; box-shadow: 0 8px 30px rgba(124, 58, 237, 0.2); transform: translateY(-2px); }
    .stMetric { background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 16px; transition: all 0.3s ease; position: relative; overflow: hidden; }
    .stMetric::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #7C3AED, #06B6D4); }
    .stMetric:hover { border-color: #7C3AED; box-shadow: 0 0 20px rgba(124, 58, 237, 0.3); transform: translateY(-3px); }
    .stMetric label { color: #CBD5E1 !important; font-size: 0.9rem !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    .stMetric [data-testid="stMetricValue"] { color: #F8FAFC !important; font-size: 2rem !important; font-weight: 700 !important; background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    h1 { background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 3rem !important; font-weight: 800 !important; margin-bottom: 1.5rem; animation: fadeInUp 0.8s ease-out; }
    h2 { color: #F8FAFC !important; font-size: 2rem !important; font-weight: 700 !important; margin-top: 1.5rem; margin-bottom: 1rem; position: relative; padding-left: 16px; animation: slideInLeft 0.6s ease-out; }
    h2::before { content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 4px; height: 80%; background: linear-gradient(180deg, #7C3AED, #06B6D4); border-radius: 2px; }
    h3 { color: #CBD5E1 !important; font-size: 1.5rem !important; font-weight: 600 !important; animation: slideInRight 0.6s ease-out; }
    p, span, div { color: #F8FAFC; }
    .stButton > button { background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); color: #F8FAFC !important; border: none; border-radius: 10px; padding: 10px 24px; font-weight: 600; font-size: 0.95rem; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; letter-spacing: 0.3px; }
    .stButton > button:hover { background: linear-gradient(135deg, #8B5CF6 0%, #22D3EE 100%); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4); }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: #111827; padding: 8px; border-radius: 12px; border: 1px solid #1E293B; margin-bottom: 24px; }
    .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; padding: 10px 20px; color: #94A3B8 !important; font-weight: 600; font-size: 0.95rem; transition: all 0.3s ease; border: 1px solid transparent; }
    .stTabs [data-baseweb="tab"]:hover { background: #1E293B; color: #F8FAFC !important; border-color: #374151; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%) !important; color: #F8FAFC !important; border: 1px solid transparent !important; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4); }
    .user-message { background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%); color: #F8FAFC; padding: 14px 18px; border-radius: 16px 16px 4px 16px; margin: 12px 0; margin-left: 15%; box-shadow: 0 2px 10px rgba(124, 58, 237, 0.3); animation: slideInRight 0.4s ease-out; font-size: 0.95rem; line-height: 1.6; position: relative; }
    .ai-message { background: #1E293B; color: #F8FAFC; padding: 14px 18px; border-radius: 16px 16px 16px 4px; margin: 12px 0; margin-right: 15%; border: 1px solid #374151; border-left: 3px solid #06B6D4; box-shadow: 0 2px 10px rgba(6, 182, 212, 0.1); animation: slideInLeft 0.4s ease-out; font-size: 0.95rem; line-height: 1.6; position: relative; }
    .stDataFrame { border: 1px solid #1E293B !important; border-radius: 12px !important; overflow: hidden; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); }
    .stAlert { border-radius: 12px; border: 1px solid; background: #111827 !important; }
    .stSuccess { border-color: #22C55E !important; color: #22C55E !important; background: rgba(34, 197, 94, 0.1) !important; }
    .stWarning { border-color: #F59E0B !important; color: #F59E0B !important; background: rgba(245, 158, 11, 0.1) !important; }
    .stError { border-color: #EF4444 !important; color: #EF4444 !important; background: rgba(239, 68, 68, 0.1) !important; }
    .stInfo { border-color: #06B6D4 !important; color: #06B6D4 !important; background: rgba(6, 182, 212, 0.1) !important; }
    .stSelectbox > div > div { background: #111827 !important; border: 1px solid #1E293B !important; border-radius: 8px !important; color: #F8FAFC !important; }
    .stTextInput input, .stTextArea textarea { background: #111827 !important; border: 1px solid #1E293B !important; border-radius: 8px !important; color: #F8FAFC !important; transition: all 0.3s ease; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #7C3AED !important; box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important; outline: none !important; }
    .stFileUploader { background: #111827; border: 2px dashed #374151; border-radius: 12px; padding: 24px; transition: all 0.3s ease; }
    .stFileUploader:hover { border-color: #7C3AED; background: rgba(124, 58, 237, 0.05); }
    ::-webkit-scrollbar { width: 10px; height: 10px; } ::-webkit-scrollbar-track { background: #0F172A; } ::-webkit-scrollbar-thumb { background: #374151; border-radius: 5px; border: 2px solid #0F172A; } ::-webkit-scrollbar-thumb:hover { background: #7C3AED; }
    .welcome-container { text-align: center; padding: 60px 20px; animation: fadeInUp 0.8s ease-out; }
    .welcome-emoji { font-size: 5rem; animation: float 3s ease-in-out infinite; display: inline-block; filter: drop-shadow(0 0 20px rgba(124, 58, 237, 0.5)); }
    .welcome-title { font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 24px 0; }
    .welcome-subtitle { font-size: 1.25rem; color: #94A3B8; margin-bottom: 32px; }
    .feature-card { background: #111827; border: 1px solid #1E293B; border-radius: 16px; padding: 32px 24px; text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); animation: fadeInUp 0.6s ease-out; position: relative; overflow: hidden; }
    .feature-card:hover { border-color: #7C3AED; transform: translateY(-8px); box-shadow: 0 20px 40px rgba(124, 58, 237, 0.2); }
    .feature-icon { font-size: 3.5rem; margin-bottom: 16px; animation: float 3s ease-in-out infinite; filter: drop-shadow(0 0 15px rgba(124, 58, 237, 0.4)); }
    .feature-title { font-size: 1.25rem; font-weight: 700; color: #F8FAFC; margin-bottom: 12px; }
    .feature-desc { color: #94A3B8; font-size: 0.95rem; line-height: 1.6; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, #374151, transparent); margin: 24px 0; }
    .api-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 197, 94, 0.1); border: 1px solid #22C55E; color: #22C55E; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; }
    .api-badge::before { content: ''; width: 8px; height: 8px; background: #22C55E; border-radius: 50%; animation: pulse 2s infinite; }
    .quality-score { background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%); border-radius: 12px; padding: 20px; text-align: center; margin: 16px 0; }
    .quality-score h3 { color: white !important; margin: 0 0 10px 0; }
    .quality-score .score { font-size: 3rem; font-weight: 800; color: white; }
    .stDownloadButton > button { background: linear-gradient(135deg, #22C55E 0%, #06B6D4 100%) !important; color: #F8FAFC !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; padding: 12px 28px !important; font-size: 1rem !important; }
    .stDownloadButton > button:hover { background: linear-gradient(135deg, #16A34A 0%, #0891B2 100%) !important; transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3) !important; }
    .chart-download-section { background: #1E293B; border-radius: 12px; padding: 16px; margin-top: 16px; border: 1px solid #374151; }
    .streamlit-expanderHeader { background: #111827 !important; border: 1px solid #1E293B !important; border-radius: 8px !important; color: #F8FAFC !important; font-weight: 600 !important; }
    .executive-report { background: linear-gradient(135deg, #1E293B 0%, #111827 100%); border-left: 4px solid #F59E0B; padding: 20px; border-radius: 8px; font-size: 1rem; line-height: 1.8; color: #CBD5E1; margin: 20px 0; animation: fadeInUp 1s ease-out; }
    .magic-card { background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); border: 1px dashed #7C3AED; border-radius: 12px; padding: 20px; margin: 15px 0; animation: pulse 3s infinite; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "df" not in st.session_state: st.session_state.df = None
if "smart_profile" not in st.session_state: st.session_state.smart_profile = None
if "exec_summary" not in st.session_state: st.session_state.exec_summary = None
if "magic_insights" not in st.session_state: st.session_state.magic_insights = None
if "chat_messages" not in st.session_state: 
    st.session_state.chat_messages = [{"role": "ai", "content": "👋 Assalam o Alaikum! Main ek Senior AI Data Scientist hoon. Dataset upload karein, main khud uska post-mortem karunga! 🧠✨"}]

# --- 🧠 NEXT-GEN BACKEND FUNCTIONS ---

def generate_smart_profile(df):
    """AI ko raw text nahi, structured JSON DNA bhejte hain. Yeh 10x zyada accurate hai."""
    profile = {
        "dataset_shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "column_types": df.dtypes.astype(str).to_dict(),
        "missing_data_percentage": ((df.isnull().sum() / len(df)) * 100).round(2).to_dict(),
        "duplicate_rows_count": int(df.duplicated().sum()),
    }
    
    # Numeric Stats (Only top 5 metrics to save tokens)
    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) > 0:
        profile["numeric_distributions"] = df[num_cols].describe().loc[['mean', 'min', 'max', 'std']].round(2).to_dict()
        
    # Categorical Dominance (What is the most common thing?)
    cat_cols = df.select_dtypes(exclude=np.number).columns
    cat_dom = {}
    for col in cat_cols:
        top_val = df[col].value_counts(normalize=True).head(1)
        if not top_val.empty:
            cat_dom[col] = {str(top_val.index[0]): f"{top_val.values[0]*100:.1f}%"}
    profile["categorical_dominance"] = cat_dom
    
    return json.dumps(profile, indent=2)

def call_ai(prompt, system_role="You are a Senior Data Scientist at McKinsey & Company. You provide deep, actionable business insights, not just basic summaries. Use professional formatting (bolding, bullet points)."):
    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 style="text-align: center; font-size: 2rem;">🧠 AI Data Pro</h1>', unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.markdown('<div class="api-badge">Agentic AI</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📁 Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file:
        try:
            with st.spinner("🧬 Extracting Data DNA..."):
                time.sleep(0.5)
                st.session_state.df = pd.read_csv(uploaded_file)
                # Generate Smart Profile automatically
                st.session_state.smart_profile = generate_smart_profile(st.session_state.df)
                st.success("✅ DNA Extracted!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- MAIN APP ---
if st.session_state.df is not None:
    df = st.session_state.df
    profile_json = st.session_state.smart_profile
    
    st.markdown('<h1>🧠 AI Data Analyst Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;">Agentic AI Data Science Platform</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive AI Report", "📈 Deep Analysis", "🔗 Correlations", "💬 AI Consultant Chat"])
    
    # === TAB 1: EXECUTIVE AI REPORT (The "Wow" Factor) ===
    with tab1:
        # Data Quality Score
        total_cells = df.shape[0] * df.shape[1]
        missing_pct = (df.isnull().sum().sum() / total_cells) * 100 if total_cells > 0 else 0
        dup_pct = (df.duplicated().sum() / df.shape[0]) * 100 if df.shape[0] > 0 else 0
        quality_score = max(0, min(100, 100 - (missing_pct * 0.5) - (dup_pct * 0.3)))
        
        st.markdown(f'<div class="quality-score"><h3>📊 Data Health Index</h3><div class="score">{quality_score:.1f}%</div></div>', unsafe_allow_html=True)
        
        # Auto-Generate Executive Summary
        if st.session_state.exec_summary is None:
            with st.spinner("🧠 AI is reading the dataset and writing an Executive Business Report..."):
                prompt = f"""Here is the JSON profile of a new dataset:
                {profile_json}
                
                Write a high-level Executive Summary for the CEO. Include:
                1. **Data Health:** Is the data reliable? Mention missing/duplicate issues.
                2. **Key Metrics:** Highlight the most impressive numbers from the numeric distributions.
                3. **Dominant Factors:** What are the most common categories (from categorical dominance)?
                4. **Strategic Warning:** Point out any red flags (e.g., high standard deviation, missing critical data).
                Keep it professional, concise, and impactful."""
                st.session_state.exec_summary = call_ai(prompt)
        
        st.markdown("### 📑 Auto-Generated Executive Report")
        st.markdown(f'<div class="executive-report">{st.session_state.exec_summary}</div>', unsafe_allow_html=True)
        
        # 🪄 AI MAGIC INSIGHTS (Anomaly Detection)
        st.markdown("### 🪄 AI Magic: Hidden Pattern Detection")
        if st.button("🔮 Scan for Hidden Anomalies & Patterns"):
            with st.spinner("🕵️ AI Detective is scanning for outliers and frauds..."):
                magic_prompt = f"""Analyze this dataset DNA: {profile_json}.
                Act as a Data Detective. Find 3 HIDDEN patterns, potential anomalies, or surprising facts that a normal human analyst would miss just by looking at basic stats.
                Format your answer exactly like this:
                🚨 **Red Flag / Anomaly**: [Insight]
                💡 **Hidden Opportunity**: [Insight]
                🔍 **Surprising Correlation/Fact**: [Insight]"""
                st.session_state.magic_insights = call_ai(magic_prompt)
        
        if st.session_state.magic_insights:
            st.markdown(f'<div class="magic-card">{st.session_state.magic_insights}</div>', unsafe_allow_html=True)
            
        # Basic Stats below the magic
        with st.expander("🔍 View Raw Data & Basic Stats"):
            c1, c2 = st.columns(2)
            c1.metric("Rows", f"{df.shape[0]:,}")
            c2.metric("Columns", f"{df.shape[1]:,}")
            st.dataframe(df.head(10), use_container_width=True)

    # === TAB 2: DEEP ANALYSIS ===
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🎨 Interactive Visualization Engine")
        
        c1, c2, c3 = st.columns(3)
        chart_type = c1.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"])
        cols = df.columns.tolist()
        x_col = c2.selectbox("X-Axis", cols)
        y_col = c3.selectbox("Y-Axis", ["None"] + cols)
        
        fig = None
        try:
            if chart_type == "Bar Chart" and y_col != "None": fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            elif chart_type == "Line Chart" and y_col != "None": fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            elif chart_type == "Scatter Plot" and y_col != "None": fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            elif chart_type == "Pie Chart": fig = px.pie(df, names=x_col, title=f"Distribution of {x_col}")
            elif chart_type == "Histogram": fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
            elif chart_type == "Box Plot" and y_col != "None": fig = px.box(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            
            if fig:
                fig.update_layout(template="plotly_dark", plot_bgcolor='#111827', paper_bgcolor='#111827', font=dict(color='#F8FAFC', size=13), title_font=dict(size=18, color='#F8FAFC'), xaxis=dict(gridcolor='#374151'), yaxis=dict(gridcolor='#374151'))
                fig.update_traces(marker=dict(color='#7C3AED', line=dict(color='#06B6D4', width=1)))
                st.plotly_chart(fig, use_container_width=True)
                
                # Download Section
                st.markdown('<div class="chart-download-section">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    try:
                        img_bytes = fig.to_image(format="png", width=1200, height=800, scale=2)
                        st.download_button("🖼️ Export PNG", img_bytes, f"{chart_type}.png", "image/png", use_container_width=True)
                    except: st.warning("Install kaleido for PNG")
                with col2:
                    st.download_button("🌐 Export Interactive HTML", fig.to_html(include_plotlyjs='cdn').encode('utf-8'), f"{chart_type}.html", "text/html", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            else: st.warning("⚠️ Select valid axes.")
        except Exception as e: st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 3: CORRELATIONS ===
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🔗 Neural Correlation Matrix")
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 1:
            corr_matrix = df[num_cols].corr()
            fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", title="Feature Heatmap")
            fig_corr.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827', font=dict(color='#F8FAFC'))
            st.plotly_chart(fig_corr, use_container_width=True)
        else: st.info("Need 2+ numeric columns.")
        st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 4: AI CONSULTANT CHAT ===
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("💬 Senior AI Consultant")
        st.caption("Yeh normal chatbot nahi hai. Yeh tumhe business strategy batayega.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        user_input = st.text_input("Ask for strategic advice...", placeholder="e.g., How can we increase revenue based on this data?", label_visibility="collapsed", key="chat_input")
        if st.button("🚀 Consult AI", use_container_width=True):
            if user_input:
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                with st.spinner("🧠 Formulating strategy..."):
                    prompt = f"""Dataset DNA: {profile_json}\n\nUser Query: {user_input}\n\nProvide a strategic, McKinsey-style answer. Use bullet points and bold text."""
                    ai_response = call_ai(prompt)
                    st.session_state.chat_messages.append({"role": "ai", "content": ai_response})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome Screen
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-emoji">🧠✨</div>
        <div class="welcome-title">AI Data Pro</div>
        <div class="welcome-subtitle">Next-Generation Agentic Data Science Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><div class="feature-icon">🧬</div><div class="feature-title">DNA Profiling</div><div class="feature-desc">AI reads the JSON structure of your data, not just raw text</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><div class="feature-icon">📑</div><div class="feature-title">Auto-Reports</div><div class="feature-desc">Generates CEO-level Executive Summaries automatically</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><div class="feature-icon">🕵️</div><div class="feature-title">Anomaly Detection</div><div class="feature-desc">Finds hidden frauds and outliers humans miss</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Upload a CSV to unleash the AI.")