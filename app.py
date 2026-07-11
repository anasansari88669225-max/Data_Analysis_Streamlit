# main.py

import os
from io import StringIO

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Data Analysis Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Data Analysis Assistant")
st.caption("Upload a CSV, explore data, visualize insights, filter records, and chat with AI.")

if "df" not in st.session_state:
    st.session_state.df = None

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = None

if "messages" not in st.session_state:
    st.session_state.messages = []


def get_statistics(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty:
        return pd.DataFrame()

    stats = pd.DataFrame({
        "Mean": numeric_df.mean(),
        "Median": numeric_df.median(),
        "Mode": numeric_df.mode().iloc[0],
        "Std Dev": numeric_df.std(),
        "Minimum": numeric_df.min(),
        "Maximum": numeric_df.max(),
    })

    return stats.round(4)


def apply_filters(df: pd.DataFrame):
    filtered = df.copy()

    st.sidebar.header("Dataset Filters")

    numeric_cols = filtered.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = filtered.select_dtypes(exclude=np.number).columns.tolist()

    for col in numeric_cols:
        min_val = float(filtered[col].min())
        max_val = float(filtered[col].max())

        if min_val != max_val:
            values = st.sidebar.slider(
                col,
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
            )
            filtered = filtered[
                (filtered[col] >= values[0]) &
                (filtered[col] <= values[1])
            ]

    for col in categorical_cols:
        options = filtered[col].dropna().unique().tolist()

        if options:
            selected = st.sidebar.multiselect(
                col,
                options,
                default=options
            )
            filtered = filtered[filtered[col].isin(selected)]

    return filtered


def dataset_context(df):
    stats = get_statistics(df)

    buffer = StringIO()
    buffer.write("Dataset Summary\n")
    buffer.write(f"Rows: {df.shape[0]}\n")
    buffer.write(f"Columns: {df.shape[1]}\n\n")

    buffer.write("Columns:\n")
    buffer.write(", ".join(df.columns.tolist()))
    buffer.write("\n\n")

    buffer.write("Data Types:\n")
    buffer.write(df.dtypes.to_string())
    buffer.write("\n\n")

    buffer.write("Missing Values:\n")
    buffer.write(df.isnull().sum().to_string())
    buffer.write("\n\n")

    buffer.write("Statistics:\n")
    if not stats.empty:
        buffer.write(stats.to_string())
    else:
        buffer.write("No numeric columns.")
    buffer.write("\n\n")

    buffer.write("Sample Rows:\n")
    buffer.write(df.head(10).to_string())

    return buffer.getvalue()


with st.sidebar:
    st.header("Upload Dataset")
    uploaded = st.file_uploader("CSV File", type=["csv"])

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        st.session_state.df = df
        st.success("CSV uploaded successfully.")
    except Exception as e:
        st.error(str(e))

if st.session_state.df is not None:

    df = st.session_state.df
    filtered_df = apply_filters(df)
    st.session_state.filtered_df = filtered_df

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", filtered_df.shape[0])
    c2.metric("Columns", filtered_df.shape[1])
    c3.metric("Missing Values", int(filtered_df.isnull().sum().sum()))
    c4.metric("Duplicate Rows", int(filtered_df.duplicated().sum()))

    with st.expander("Dataset Preview", expanded=True):
        st.dataframe(filtered_df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Column Names")
            st.write(filtered_df.columns.tolist())

        with col2:
            st.subheader("Data Types")
            st.dataframe(filtered_df.dtypes.astype(str).reset_index().rename(
                columns={"index": "Column", 0: "Type"}
            ))

        st.subheader("Missing Values")
        st.dataframe(filtered_df.isnull().sum().reset_index().rename(
            columns={"index": "Column", 0: "Missing"}
        ))

    with st.expander("Statistics", expanded=True):
        stats = get_statistics(filtered_df)

        if stats.empty:
            st.info("No numeric columns found.")
        else:
            st.dataframe(stats, use_container_width=True)

    with st.container():

        st.subheader("Interactive Charts")

        chart = st.selectbox(
            "Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Scatter Plot",
                "Histogram",
                "Pie Chart",
                "Box Plot",
            ],
        )

        cols = filtered_df.columns.tolist()

        x = st.selectbox("X Column", cols)

        y = st.selectbox(
            "Y Column",
            ["None"] + cols
        )

        fig = None

        if chart == "Bar Chart":
            if y != "None":
                fig = px.bar(filtered_df, x=x, y=y)

        elif chart == "Line Chart":
            if y != "None":
                fig = px.line(filtered_df, x=x, y=y)

        elif chart == "Scatter Plot":
            if y != "None":
                fig = px.scatter(filtered_df, x=x, y=y)

        elif chart == "Histogram":
            fig = px.histogram(filtered_df, x=x)

        elif chart == "Pie Chart":
            fig = px.pie(filtered_df, names=x)

        elif chart == "Box Plot":
            if y != "None":
                fig = px.box(filtered_df, x=x, y=y)

        if fig:
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.text_input("Ask about your dataset")

    if st.button("Ask AI"):

        if not question.strip():
            st.error("Please enter a question.")

        else:
            api_key = os.environ.get("GROQ_API_KEY")

            if not api_key:
                st.error("GROQ_API_KEY environment variable not found.")

            else:
                client = Groq(api_key=api_key)

                context = dataset_context(filtered_df)

                prompt = f"""
You are a senior business data analyst.

Dataset Information:

{context}

User Question:
{question}

Provide:
- Clear business insights
- Trends
- Risks
- Opportunities
- Recommendations
"""

                st.session_state.messages.append(
                    {"role": "user", "content": question}
                )

                with st.spinner("Analyzing..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert business data analyst."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                answer = response.choices[0].message.content

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                st.rerun()

    st.subheader("Export")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Cleaned CSV",
        csv,
        "cleaned_dataset.csv",
        "text/csv"
    )