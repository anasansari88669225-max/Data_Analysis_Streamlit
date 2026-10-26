"""SQLite repository for the Streamlit attendance application."""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from ..utils.timezone_utils import get_current_date_str, get_current_time

DEFAULT_SETTINGS: dict[str, Any] = {
    "organization_name": "AeroSync Global Technologies",
    "timezone": "Asia/Karachi",
    "face_threshold": 0.5,
    "strict_anti_spoofing": True,
    "allow_photo_upload": True,
    "late_threshold_time": "09:30",
    "admin_pin": "1234",
}


class AttendanceRepository:
    """Read and write attendance data in a local SQLite database."""

    def __init__(self, database_path: str | Path | None = None) -> None:
        configured_path = database_path or os.environ.get("ATTENDANCE_DB_PATH")
        self.database_path = (
            Path(configured_path).expanduser()
            if configured_path
            else Path(__file__).resolve().parents[2] / "attendance.db"
        )
        if str(self.database_path) != ":memory:":
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(str(self.database_path), timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    id TEXT PRIMARY KEY,
                    employee_id TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    email TEXT,
                    face_embedding TEXT NOT NULL,
                    avatar_url TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    biometric_consent_given INTEGER NOT NULL DEFAULT 1,
                    consent_timestamp TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS attendance (
                    id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    employee_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    attendance_date TEXT NOT NULL,
                    check_in_timestamp TEXT NOT NULL,
                    check_in_time_formatted TEXT NOT NULL,
                    capture_method TEXT NOT NULL CHECK (
                        capture_method IN ('webcam', 'photo_upload', 'manual_override')
                    ),
                    confidence_score REAL NOT NULL,
                    distance REAL NOT NULL,
                    review_status TEXT NOT NULL DEFAULT 'verified' CHECK (
                        review_status IN ('verified', 'under_review', 'manually_approved')
                    ),
                    notes TEXT,
                    UNIQUE(employee_id, attendance_date)
                );
                CREATE INDEX IF NOT EXISTS idx_attendance_date
                    ON attendance(attendance_date);
                CREATE TABLE IF NOT EXISTS system_settings (
                    id TEXT PRIMARY KEY,
                    organization_name TEXT NOT NULL,
                    timezone TEXT NOT NULL,
                    face_threshold REAL NOT NULL,
                    strict_anti_spoofing INTEGER NOT NULL,
                    allow_photo_upload INTEGER NOT NULL,
                    late_threshold_time TEXT NOT NULL,
                    admin_pin TEXT NOT NULL
                );
                """
            )
            existing = connection.execute(
                "SELECT id FROM system_settings WHERE id = 'default'"
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO system_settings (
                        id, organization_name, timezone, face_threshold,
                        strict_anti_spoofing, allow_photo_upload,
                        late_threshold_time, admin_pin
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "default",
                        DEFAULT_SETTINGS["organization_name"],
                        DEFAULT_SETTINGS["timezone"],
                        DEFAULT_SETTINGS["face_threshold"],
                        int(DEFAULT_SETTINGS["strict_anti_spoofing"]),
                        int(DEFAULT_SETTINGS["allow_photo_upload"]),
                        DEFAULT_SETTINGS["late_threshold_time"],
                        DEFAULT_SETTINGS["admin_pin"],
                    ),
                )

    @staticmethod
    def _employee_from_row(row: sqlite3.Row) -> dict[str, Any]:
        employee = dict(row)
        employee["face_embedding"] = json.loads(employee["face_embedding"])
        employee["is_active"] = bool(employee["is_active"])
        employee["biometric_consent_given"] = bool(
            employee["biometric_consent_given"]
        )
        return employee

    @staticmethod
    def _attendance_from_row(row: sqlite3.Row) -> dict[str, Any]:
        return dict(row)

    def get_all_employees(self) -> list[dict[str, Any]]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT * FROM employees ORDER BY full_name, employee_id"
            ).fetchall()
        return [self._employee_from_row(row) for row in rows]

    def get_active_employees(self) -> list[dict[str, Any]]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT * FROM employees WHERE is_active = 1 ORDER BY full_name"
            ).fetchall()
        return [self._employee_from_row(row) for row in rows]

    def get_attendance_records(
        self, attendance_date: str | None = None
    ) -> list[dict[str, Any]]:
        with self._connection() as connection:
            if attendance_date is None:
                rows = connection.execute(
                    "SELECT * FROM attendance ORDER BY check_in_timestamp DESC"
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT * FROM attendance
                    WHERE attendance_date = ?
                    ORDER BY check_in_timestamp DESC
                    """,
                    (attendance_date,),
                ).fetchall()
        return [self._attendance_from_row(row) for row in rows]

    def get_settings(self) -> dict[str, Any]:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM system_settings WHERE id = 'default'"
            ).fetchone()
        if row is None:
            return DEFAULT_SETTINGS.copy()
        settings = dict(row)
        settings["strict_anti_spoofing"] = bool(settings["strict_anti_spoofing"])
        settings["allow_photo_upload"] = bool(settings["allow_photo_upload"])
        return settings

    def register_employee(
        self,
        *,
        employee_id: str,
        full_name: str,
        department: str,
        job_title: str,
        email: str = "",
        face_embedding: list[float],
        consent_given: bool,
    ) -> dict[str, Any]:
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        normalized_id = employee_id.strip().upper()
        employee = {
            "id": str(uuid.uuid4()),
            "employee_id": normalized_id,
            "full_name": full_name.strip(),
            "department": department.strip(),
            "job_title": job_title.strip(),
            "email": email.strip() or None,
            "face_embedding": json.dumps(face_embedding),
            "avatar_url": None,
            "is_active": 1,
            "biometric_consent_given": int(consent_given),
            "consent_timestamp": now,
            "created_at": now,
            "updated_at": now,
        }
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO employees (
                    id, employee_id, full_name, department, job_title, email,
                    face_embedding, avatar_url, is_active,
                    biometric_consent_given, consent_timestamp, created_at,
                    updated_at
                ) VALUES (
                    :id, :employee_id, :full_name, :department, :job_title,
                    :email, :face_embedding, :avatar_url, :is_active,
                    :biometric_consent_given, :consent_timestamp, :created_at,
                    :updated_at
                )
                """,
                employee,
            )
        employee["face_embedding"] = json.loads(employee["face_embedding"])
        employee["is_active"] = bool(employee["is_active"])
        employee["biometric_consent_given"] = bool(
            employee["biometric_consent_given"]
        )
        return employee

    def set_employee_active(self, employee_id: str, active: bool) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                """
                UPDATE employees SET is_active = ?, updated_at = ?
                WHERE employee_id = ?
                """,
                (
                    int(active),
                    datetime.now().astimezone().isoformat(timespec="seconds"),
                    employee_id,
                ),
            )
        return cursor.rowcount > 0

    def delete_employee(self, employee_id: str) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM employees WHERE employee_id = ?", (employee_id,)
            )
        return cursor.rowcount > 0

    def add_attendance_record(
        self,
        employee: dict[str, Any],
        *,
        capture_method: str,
        confidence_score: float,
        distance: float,
        notes: str | None = None,
        timezone: str | None = None,
    ) -> dict[str, Any]:
        settings = self.get_settings()
        timezone = timezone or settings["timezone"]
        attendance_date = get_current_date_str(timezone)
        now = get_current_time(timezone)
        record = {
            "id": str(uuid.uuid4()),
            "employee_id": employee["employee_id"],
            "employee_name": employee["full_name"],
            "department": employee["department"],
            "attendance_date": attendance_date,
            "check_in_timestamp": now.isoformat(timespec="seconds"),
            "check_in_time_formatted": now.strftime("%I:%M %p"),
            "capture_method": capture_method,
            "confidence_score": round(confidence_score, 2),
            "distance": round(distance, 6),
            "review_status": (
                "under_review" if capture_method == "manual_override" else "verified"
            ),
            "notes": notes,
        }
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO attendance (
                    id, employee_id, employee_name, department, attendance_date,
                    check_in_timestamp, check_in_time_formatted, capture_method,
                    confidence_score, distance, review_status, notes
                ) VALUES (
                    :id, :employee_id, :employee_name, :department,
                    :attendance_date, :check_in_timestamp,
                    :check_in_time_formatted, :capture_method,
                    :confidence_score, :distance, :review_status, :notes
                )
                """,
                record,
            )
        return record
