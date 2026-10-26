"""Attendance verification for the synthetic demo probe."""

import sqlite3

from ..database.repository import AttendanceRepository
from ..utils.face_math import cosine_distance


class AttendanceService:
    def __init__(self, repository: AttendanceRepository) -> None:
        self.repository = repository

    def verify_and_record(
        self, probe_embedding: list[float], capture_method: str = "webcam"
    ) -> tuple[bool, str, dict | None]:
        if capture_method not in {"webcam", "photo_upload", "manual_override"}:
            return False, "Unsupported attendance capture method.", None
        if not probe_embedding:
            return False, "An embedding is required for the demo probe.", None

        employees = self.repository.get_active_employees()
        candidates = []
        try:
            for employee in employees:
                distance = cosine_distance(probe_embedding, employee["face_embedding"])
                candidates.append((distance, employee))
        except ValueError as error:
            return False, str(error), None
        if not candidates:
            return False, "No active employees with a valid demo embedding were found.", None

        distance, employee = min(candidates, key=lambda candidate: candidate[0])
        settings = self.repository.get_settings()
        threshold = float(settings["face_threshold"])
        if distance > threshold:
            return (
                False,
                f"No employee matched the demo probe (distance {distance:.3f}; threshold {threshold:.3f}).",
                None,
            )

        try:
            record = self.repository.add_attendance_record(
                employee,
                capture_method=capture_method,
                confidence_score=max(0.0, (1.0 - distance) * 100.0),
                distance=distance,
                notes="Matched using a synthetic demo probe; not a real biometric verification.",
            )
        except sqlite3.IntegrityError:
            return (
                False,
                f"Attendance for {employee['full_name']} has already been recorded today.",
                None,
            )
        return (
            True,
            f"Demo probe matched {employee['full_name']}; this is not a real biometric verification.",
            record,
        )
