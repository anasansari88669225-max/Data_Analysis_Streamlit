# FaceAttendance Pro demo

This repository includes two local demos. The Python app requires Python 3.10 or later.

- **React preview:** run `npm install`, then `npm run dev` and open `http://localhost:3000`.
- **Streamlit app:** install Python dependencies with `python -m pip install -r requirements.txt`, then run `streamlit run app.py` and open `http://localhost:8501`.

The Streamlit app stores data in a local SQLite `attendance.db` file. Set `ATTENDANCE_DB_PATH` to use a different database location.

**Prototype notice:** this project does not perform facial recognition. Registration and simulated matching use synthetic vectors; camera and photo uploads do not verify identity. Do not use this demo for biometric security or payroll decisions.
