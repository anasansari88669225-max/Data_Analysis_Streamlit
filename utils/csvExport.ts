import { AttendanceRecord } from '../types';

export function generateAttendanceCsv(records: AttendanceRecord[]): string {
  const rows = [
    ['Record ID', 'Employee ID', 'Employee Name', 'Department', 'Date', 'Check-in Time', 'Method', 'Confidence', 'Status', 'Notes'],
    ...records.map((record) => [
      record.id,
      record.employeeId,
      record.employeeName,
      record.department,
      record.attendanceDate,
      record.checkInTimeFormatted,
      record.captureMethod,
      String(record.confidenceScore),
      record.reviewStatus,
      record.notes ?? '',
    ]),
  ];
  return rows
    .map((row) => row.map((value) => `"${value.replaceAll('"', '""')}"`).join(','))
    .join('\r\n');
}

export function downloadCsvFile(csv: string, fileName: string): void {
  const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = fileName;
  anchor.click();
  URL.revokeObjectURL(url);
}
