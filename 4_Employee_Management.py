"""
Employee Management Page: Search, filter, status toggling, and biometric purge.
"""
import streamlit as st
import pandas as pd
from employee_attendance.database.repository import AttendanceRepository
from employee_attendance.services.employee_service import EmployeeService

st.title("👥 Employee Management Directory")

repo = AttendanceRepository()
emp_service = EmployeeService(repo)
employees = repo.get_all_employees()

st.write(f"Total Enrolled Employees: **{len(employees)}**")

if employees:
    # Search
    search = st.text_input("Filter by Name or ID", "")
    filtered = [
        e for e in employees
        if search.lower() in e["full_name"].lower() or search.lower() in e["employee_id"].lower()
    ]

    for emp in filtered:
        with st.expander(f"{emp['full_name']} ({emp['employee_id']}) - {'Active' if emp['is_active'] else 'Deactivated'}"):
            st.write(f"**Department:** {emp['department']} | **Role:** {emp['job_title']}")
            st.write(f"**Email:** {emp.get('email') or 'N/A'}")
            st.write(f"**Consent Verified:** {'Yes' if emp['biometric_consent_given'] else 'No'}")

            col1, col2 = st.columns(2)
            with col1:
                btn_label = "Deactivate Employee" if emp["is_active"] else "Activate Employee"
                if st.button(btn_label, key=f"toggle_{emp['employee_id']}"):
                    emp_service.toggle_status(emp["employee_id"])
                    st.rerun()

            with col2:
                if st.button("Permanently Purge Biometrics & Delete", key=f"del_{emp['employee_id']}"):
                    emp_service.delete_employee(emp["employee_id"])
                    st.success(f"Purged biometrics for {emp['full_name']}.")
                    st.rerun()
else:
    st.info("No employees registered in the system.")
