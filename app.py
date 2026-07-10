import streamlit as st
import pandas as pd

# Page Settings
st.set_page_config(
    page_title="My First Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 My First Streamlit Dashboard")

st.write("Assalam-o-Alaikum! Welcome to my first Streamlit App.")
# Metrics
st.header("Quick Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", "$10,000")

with col2:
    st.metric("Customers", "250")

with col3:
    st.metric("Orders", "500")

# Sample Data
st.header("Sample Data")

data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Sales": [1000, 1500, 2000, 1800, 2500]
}

df = pd.DataFrame(data)

st.dataframe(df)

# Chart
st.header("Sales Trend")

st.line_chart(df.set_index("Month"))

# Sidebar
st.sidebar.title("Menu")
st.sidebar.write("This is a sample sidebar.")

# Footer
st.success("App is running successfully!")