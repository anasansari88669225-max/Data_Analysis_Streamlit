"""
Settings Page: Timezone boundaries, recognition threshold, and privacy notice.
"""
import streamlit as st

st.title("⚙️ System Configuration & Privacy Policies")

st.subheader("1. Organization Timezone")
timezone = st.selectbox(
    "Active Timezone (Calendar Day Enforcement)",
    ["Asia/Karachi", "UTC", "Asia/Dubai", "Europe/London", "America/New_York"]
)

st.subheader("2. Face Matching Sensitivity")
threshold = st.slider(
    "Cosine Distance Threshold (Lower = Stricter)",
    min_value=0.30,
    max_value=0.70,
    value=0.50,
    step=0.05
)
st.caption("Standard recommended threshold is 0.50. Values below 0.40 enforce high security.")

st.markdown("---")
st.subheader("3. Biometric Notice & GDPR Policy")
st.info("""
**Biometric Processing Standard:**
- Facial templates are transformed into non-reversible 128-d vectors.
- Exactly 1 attendance record is permitted per employee per calendar day.
- Employees have the right to request full biometric data deletion at any time.
""")
