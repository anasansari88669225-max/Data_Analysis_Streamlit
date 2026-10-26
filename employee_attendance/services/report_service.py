"""CSV report generation for attendance records."""

import csv
import io
from collections.abc import Iterable, Mapping


class ReportService:
    COLUMNS = (
        "id",
        "employee_id",
        "employee_name",
        "department",
        "attendance_date",
        "check_in_timestamp",
        "check_in_time_formatted",
        "capture_method",
        "confidence_score",
        "distance",
        "review_status",
        "notes",
    )

    def __init__(self, repository: object) -> None:
        self.repository = repository

    def generate_csv_string(
        self, records: Iterable[Mapping[str, object]]
    ) -> str:
        output = io.StringIO(newline="")
        writer = csv.DictWriter(
            output, fieldnames=self.COLUMNS, extrasaction="ignore", lineterminator="\r\n"
        )
        writer.writeheader()
        writer.writerows(
            {column: record.get(column, "") for column in self.COLUMNS}
            for record in records
        )
        return output.getvalue()
