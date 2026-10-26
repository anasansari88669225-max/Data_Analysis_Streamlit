"""
Mark Attendance Page: Live camera input and photo upload recognition.
"""
import streamlit as st
from employee_attendance.database.repository import AttendanceRepository
from employee_attendance.services.attendance_service import AttendanceService

st.title("📷 Mark Attendance Terminal")
st.markdown("Authenticate using live camera capture or an authorized portrait image.")

repo = AttendanceRepository()
service = AttendanceService(repo)

tab_cam, tab_upload, tab_test = st.tabs(["Webcam Camera", "Photo Upload", "Quick Probe Tester"])

with tab_cam:
    img_file = st.camera_input("Position face in center frame and click capture")
    if img_file is not None:
        st.error(
            "Facial recognition is not configured. The captured image was not matched "
            "to an employee and no attendance was recorded."
        )

with tab_upload:
    st.warning(
        "Facial recognition and anti-spoofing are not configured. Uploaded images "
        "cannot be used to verify or record attendance."
    )
    uploaded = st.file_uploader("Upload headshot photo (JPEG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        if st.button("Process & Verify Photo"):
            st.error(
                "Facial recognition is not configured. The uploaded image was not "
                "matched to an employee and no attendance was recorded."
            )

with tab_test:
    st.markdown(
        "Try a synthetic demo-vector match against active employees. This is not "
        "facial recognition and does not analyze camera or uploaded photos."
    )
    active = repo.get_active_employees()
    if active:
        options = {f"{e['full_name']} ({e['employee_id']})": e for e in active}
        selected = st.selectbox("Select employee to simulate probe for:", list(options.keys()))
        if st.button("Run Simulation Match"):
            emp = options[selected]
            success, msg, rec = service.verify_and_record(emp["face_embedding"], capture_method="webcam")
            if success:
                st.success(f"Biometric Match Success: {rec.get('employee_name')} checked in at {rec.get('check_in_time_formatted')}!")
            else:
                st.warning(msg)
    else:
        st.info("No active employees found to test.")
