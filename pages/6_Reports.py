"""
Reports and Analytics Page: RFC-4180 CSV export and metric breakdowns.
"""
import streamlit as st
import pandas as pd
from employee_attendance.database.repository import AttendanceRepository
from employee_attendance.services.report_service import ReportService
from employee_attendance.utils.timezone_utils import get_current_date_str

st.title("📈 Reports & Analytics")

repo = AttendanceRepository()
report_service = ReportService(repo)
records = repo.get_attendance_records()

if records:
    csv_data = report_service.generate_csv_string(records)
    today = get_current_date_str("Asia/Karachi")

    st.download_button(
        label=f"📥 Download Full CSV Report ({len(records)} Records)",
        data=csv_data,
        file_name=f"attendance_report_{today}.csv",
        mime="text/csv",
    )

    df = pd.DataFrame(records)
    st.markdown("### Department Breakdown")
    if "department" in df.columns:
        dept_counts = df["department"].value_counts()
        st.bar_chart(dept_counts)
else:
    st.info("No attendance data available to generate reports.")
