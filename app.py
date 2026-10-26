"""
FaceAttendance Pro - Streamlit Entry Point
"""
import streamlit as st
import os

st.set_page_config(
    page_title="FaceAttendance Pro - Biometric Attendance System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Neumorphic theme CSS
css_path = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🛡️ FaceAttendance Pro")
st.subheader("Employee Attendance Management Demo")

st.markdown("""
Welcome to **FaceAttendance Pro**, a prototype for employee enrollment, attendance records, and workforce reporting.
It does **not** perform facial recognition: the enrollment and matching flows use synthetic demo vectors, and
camera and photo uploads are previews only. Do not use the demo as a biometric security or payroll system.

### 🧭 Navigation & Workflow Sections
Use the sidebar navigation to access:
1. **Dashboard:** Real-time workforce presence KPIs, attendance rates, and 7-day trend analytics.
2. **Mark Attendance:** Camera preview, photo upload preview, and synthetic demo-vector tester.
3. **Register Employee:** Enroll demo staff with explicit consent and a synthetic 128-dimensional vector.
4. **Employee Management:** Directory of registered staff, active/inactive toggles, and demo-vector deletion.
5. **Attendance History:** Searchable audit trail with confidence scores and supervisor approval actions.
6. **Reports & Analytics:** Filterable workforce reports with one-click RFC-4180 CSV export.
7. **Settings:** Timezone boundary configuration, cosine distance threshold slider, and privacy notice.

---
*Built with Python and Streamlit. Attendance records are stored in a local SQLite database.*
""")
