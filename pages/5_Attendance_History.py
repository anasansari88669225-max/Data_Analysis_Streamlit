"""
Attendance History Page: Complete historical logs and filters.
"""
import streamlit as st
import pandas as pd
from employee_attendance.database.repository import AttendanceRepository

st.title("📅 Attendance History Logs")

repo = AttendanceRepository()
records = repo.get_attendance_records()

if records:
    df = pd.DataFrame(records)
    st.dataframe(df, width="stretch")
else:
    st.info("No attendance records logged in the database.")
