"""
Dashboard Page: Workforce presence KPIs and daily trends.
"""
import streamlit as st
import pandas as pd
from employee_attendance.database.repository import AttendanceRepository
from employee_attendance.utils.timezone_utils import get_current_date_str

st.title("📊 Workforce Attendance Dashboard")

repo = AttendanceRepository()
employees = repo.get_all_employees()
active_employees = [e for e in employees if e.get("is_active", True)]
total_active = len(active_employees)

today_date = get_current_date_str("Asia/Karachi")
today_records = repo.get_attendance_records(today_date)
present_today = len(today_records)
pending_today = max(0, total_active - present_today)
rate = round((present_today / total_active * 100), 1) if total_active > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Active Staff", total_active)
with col2:
    st.metric("Present Today", present_today)
with col3:
    st.metric("Pending Check-in", pending_today)
with col4:
    st.metric("Attendance Rate", f"{rate}%")

st.markdown("---")
st.subheader(f"Today's Attendance Logs ({today_date})")

if today_records:
    df = pd.DataFrame(today_records)
    cols = ["employee_name", "employee_id", "department", "check_in_time_formatted", "capture_method", "confidence_score", "review_status"]
    present_cols = [c for c in cols if c in df.columns]
    st.dataframe(df[present_cols], width="stretch")
else:
    st.info("No attendance records logged yet for today.")
