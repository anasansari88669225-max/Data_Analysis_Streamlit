"""
Register Employee Page: Enroll new staff and generate biometric embedding.
"""
import streamlit as st
from employee_attendance.database.repository import AttendanceRepository
from employee_attendance.services.employee_service import EmployeeService

st.title("👤 Register New Employee")
st.markdown(
    "This demo creates a synthetic vector from the employee ID and name; it does not analyze "
    "the uploaded face image. Facial recognition is not configured."
)

repo = AttendanceRepository()
emp_service = EmployeeService(repo)

with st.form("employee_registration_form"):
    col1, col2 = st.columns(2)
    with col1:
        emp_id = st.text_input("Employee ID (Unique)*", placeholder="e.g. EMP-108")
        full_name = st.text_input("Full Name*", placeholder="e.g. Liam Foster")
        email = st.text_input("Corporate Email (Optional)", placeholder="e.g. liam.f@aerosync.io")
    with col2:
        dept = st.selectbox("Department*", ["Engineering", "Product", "Operations", "Finance", "Human Resources", "Security"])
        job_title = st.text_input("Job Title*", placeholder="e.g. Senior Security Specialist")
        uploaded_face = st.file_uploader("Face Photo*", type=["jpg", "jpeg", "png"])

    consent = st.checkbox(
        "I explicitly confirm that the employee has received the biometric notice and consented to biometric processing in accordance with privacy regulations."
    )

    submitted = st.form_submit_button("Register & Generate Vector")

    if submitted:
        success, msg, _ = emp_service.register_employee(
            employee_id=emp_id,
            full_name=full_name,
            department=dept,
            job_title=job_title,
            consent_given=consent,
            has_image=uploaded_face is not None,
            email=email
        )
        if success:
            st.success(msg)
        else:
            st.error(msg)
