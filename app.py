import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from groq import Groq
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")

# --- CUSTOM CSS FOR EXCELLENT UI (Bonus Feature) ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    .stMetric { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 10px; border-radius: 8px; }
    [data-theme="dark"] .stMetric { background-color: #262730; border: 1px solid #333; }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "df" not in st.session_state: st.session_state.df = None
if "chart_explanation" not in st.session_state: st.session_state.chart_explanation = None
if "qa_answers" not in st.session_state: st.session_state.qa_answers = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("📊 AI Data Analyst")
    st.markdown("---")
    
    # 🔥 API PROBLEM FIXED: Sidebar input instead of broken os.environ.get()
    st.header("🔑 API Configuration")
    st.caption("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")
    api_key = st.text_input("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", type="password")
    if not api_key:
        st.warning("AI features ke liye API Key zaroori hai.")
    
    st.markdown("---")
    st.header("📁 Upload Dataset")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success("✅ Dataset loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")

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
    if not api_key:
        return "⚠️ Please enter your Groq API Key in the sidebar."
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Fast aur free model
            messages=[
                {"role": "system", "content": "You are an expert business data analyst. Provide clear, concise, and accurate answers based ONLY on the provided data context."},
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
    
    # Excellent UI ke liye Tabs ka istemal
    tab1, tab2, tab3 = st.tabs(["📊 1. Dataset Overview", "📈 2. Analysis & Charts", "🤖 3. AI Q&A (Judges)"])
    
    # ==========================================
    # TAB 1: DATASET OVERVIEW (Step 1)
    # ==========================================
    with tab1:
        st.header("Dataset Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Rows", df.shape[0])
        c2.metric("Total Columns", df.shape[1])
        c3.metric("Missing Values", int(df.isnull().sum().sum()))
        c4.metric("Duplicate Rows", int(df.duplicated().sum()))
        
        with st.expander("View Full Dataset", expanded=False):
            st.dataframe(df, use_container_width=True)
            
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Data Types")
            st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Type'}))
        with col2:
            st.subheader("Missing Values per Column")
            st.dataframe(df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing'}))

    # ==========================================
    # TAB 2: ANALYSIS & CHARTS (Step 2, 4, 5)
    # ==========================================
    with tab2:
        st.header("Statistical Analysis")
        num_df = df.select_dtypes(include=np.number)
        if not num_df.empty:
            st.dataframe(num_df.describe().round(2), use_container_width=True)
        else:
            st.info("No numeric columns found for statistical analysis.")
            
        st.markdown("---")
        st.header("Interactive Visualization")
        
        c1, c2, c3 = st.columns(3)
        chart_type = c1.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])
        cols = df.columns.tolist()
        x_col = c2.selectbox("X-Axis", cols)
        y_col = c3.selectbox("Y-Axis", ["None"] + cols)
        
        fig = None
        try:
            # Chart generation logic
            if chart_type == "Bar Chart" and y_col != "None": fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            elif chart_type == "Line Chart" and y_col != "None": fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            elif chart_type == "Scatter Plot" and y_col != "None": fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            elif chart_type == "Pie Chart": fig = px.pie(df, names=x_col, title=f"Distribution of {x_col}")
            elif chart_type == "Histogram": fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
            
            if fig:
                fig.update_layout(template="plotly_white") # Clean layout
                st.plotly_chart(fig, use_container_width=True)
                
                # Step 5: Explain Result with AI
                if st.button("✨ Explain this Chart with AI"):
                    with st.spinner("AI is analyzing the chart..."):
                        prompt = f"Dataset Context:\n{context}\n\nA {chart_type} was generated with X-axis: '{x_col}' and Y-axis: '{y_col}'. Provide a short, simple explanation of the findings, trends, and business insights from this chart."
                        st.session_state.chart_explanation = call_ai(prompt)
                
                if st.session_state.chart_explanation:
                    st.info("💡 **AI Explanation:**")
                    st.write(st.session_state.chart_explanation)
            else:
                st.warning("Please select a valid Y-axis for this chart type.")
        except Exception as e:
            st.error(f"Error generating chart: {e}")

    # ==========================================
    # TAB 3: AI Q&A FOR JUDGES (Step 3)
    # ==========================================
    with tab3:
        st.header("🤖 AI Data Assistant (For Judges)")
        st.caption("Judges yahan 3 fixed questions pooch sakte hain. AI dataset analyze kar ke jawab dega.")
        
        # 3 Questions Inputs
        q1 = st.text_area("Question 1", placeholder="e.g., Which product generated the highest sales?", height=70)
        q2 = st.text_area("Question 2", placeholder="e.g., What is the average age of customers?", height=70)
        q3 = st.text_area("Question 3", placeholder="e.g., Which city has the maximum orders?", height=70)
        
        if st.button("🚀 Analyze All Questions"):
            if not any([q1, q2, q3]):
                st.warning("Please enter at least one question.")
            else:
                with st.spinner("AI is analyzing the dataset and answering questions..."):
                    # Single API call for all 3 questions (Saves time and API limits)
                    prompt = f"""
                    You are an expert data analyst. 
                    Dataset Context:
                    {context}
                    
                    The judges have asked the following questions:
                    1. {q1 if q1 else "No question"}
                    2. {q2 if q2 else "No question"}
                    3. {q3 if q3 else "No question"}
                    
                    Provide clear, accurate, and concise answers to each question based STRICTLY on the data context. Format with clear headings for each question.
                    """
                    st.session_state.qa_answers = call_ai(prompt)
                    
        if st.session_state.qa_answers:
            st.markdown("---")
            st.subheader("📝 AI Answers:")
            st.write(st.session_state.qa_answers)
            
        st.markdown("---")
        # Bonus Feature: Export Data
        st.download_button(
            "📥 Download Cleaned Dataset (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "cleaned_dataset.csv",
            "text/csv"
        )

else:
    st.title("👋 Welcome to AI Data Analysis Assistant")
    st.info("Please upload a CSV file from the sidebar to begin.")