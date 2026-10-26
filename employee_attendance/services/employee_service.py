"""Employee enrollment and lifecycle operations."""

import re
import sqlite3

from ..database.repository import AttendanceRepository
from ..utils.face_math import generate_deterministic_embedding


class EmployeeService:
    def __init__(self, repository: AttendanceRepository) -> None:
        self.repository = repository

    def register_employee(
        self,
        *,
        employee_id: str,
        full_name: str,
        department: str,
        job_title: str,
        consent_given: bool,
        has_image: bool,
        email: str = "",
    ) -> tuple[bool, str, dict | None]:
        normalized_id = employee_id.strip().upper()
        if not normalized_id:
            return False, "Employee ID is required.", None
        if not re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{1,49}", normalized_id):
            return False, "Employee ID must be 2–50 letters, numbers, hyphens, or underscores.", None
        if not full_name.strip():
            return False, "Full name is required.", None
        if not department.strip() or not job_title.strip():
            return False, "Department and job title are required.", None
        if email.strip() and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()):
            return False, "Enter a valid email address.", None
        if not consent_given:
            return False, "Explicit employee consent is required.", None
        if not has_image:
            return False, "A profile image is required for this demo.", None

        # This app generates a synthetic demo vector; it does not analyze the image.
        embedding = generate_deterministic_embedding(
            f"{normalized_id}-{full_name.strip()}"
        )
        try:
            employee = self.repository.register_employee(
                employee_id=normalized_id,
                full_name=full_name,
                department=department,
                job_title=job_title,
                email=email,
                face_embedding=embedding,
                consent_given=consent_given,
            )
        except sqlite3.IntegrityError:
            return False, f"Employee ID {normalized_id} is already registered.", None
        return (
            True,
            f"Employee {employee['full_name']} registered with a synthetic demo vector (not derived from the photo).",
            employee,
        )

    def toggle_status(self, employee_id: str) -> bool:
        employee = next(
            (
                item
                for item in self.repository.get_all_employees()
                if item["employee_id"] == employee_id
            ),
            None,
        )
        if employee is None:
            return False
        return self.repository.set_employee_active(
            employee_id, active=not employee["is_active"]
        )

    def delete_employee(self, employee_id: str) -> bool:
        return self.repository.delete_employee(employee_id)
