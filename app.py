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
st.subheader("Enterprise Facial Recognition Attendance System")

st.markdown("""
Welcome to **FaceAttendance Pro**, a modern biometric attendance application engineered for 
sub-second verification, calendar-day duplicate prevention, and strict privacy regulation compliance.

### 🧭 Navigation & Workflow Sections
Use the sidebar navigation to access:
1. **Dashboard:** Real-time workforce presence KPIs, attendance rates, and 7-day trend analytics.
2. **Mark Attendance:** Live camera facial recognition and photo upload verification terminal.
3. **Register Employee:** Enroll new staff with explicit biometric consent and 128-d vector generation.
4. **Employee Management:** Directory of registered staff, active/inactive toggles, and GDPR-compliant vector purge.
5. **Attendance History:** Searchable audit trail with confidence scores and supervisor approval actions.
6. **Reports & Analytics:** Filterable workforce reports with one-click RFC-4180 CSV export.
7. **Settings:** Timezone boundary configuration, cosine distance threshold slider, and privacy notice.

---
*Built with Python, Streamlit, and modern Computer Vision principles.*
""")
