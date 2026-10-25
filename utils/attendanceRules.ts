import { AttendanceRecord, CaptureMethod, MatchResult } from '../types';

export function getLocalCalendarDate(date: Date, timezone: string): string {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(date);
  const values = Object.fromEntries(parts.map(({ type, value }) => [type, value]));
  return `${values.year}-${values.month}-${values.day}`;
}

export function getLocalFormattedTime(date: Date, timezone: string): string {
  return new Intl.DateTimeFormat('en-US', {
    timeZone: timezone,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  }).format(date);
}

export function createAttendanceRecord(
  match: MatchResult,
  captureMethod: CaptureMethod,
  records: AttendanceRecord[],
  timezone: string,
  notes?: string,
): { success: boolean; record?: AttendanceRecord; error?: string } {
  if (!match.matched || !match.employee) {
    return { success: false, error: 'A verified employee is required to record attendance.' };
  }

  const now = new Date();
  const attendanceDate = getLocalCalendarDate(now, timezone);
  const alreadyRecorded = records.some(
    (record) => record.employeeId === match.employee?.employeeId && record.attendanceDate === attendanceDate,
  );
  if (alreadyRecorded) {
    return {
      success: false,
      error: `Attendance for ${match.employee.fullName} is already recorded for ${attendanceDate}.`,
    };
  }

  return {
    success: true,
    record: {
      id: `att-${now.getTime()}-${Math.random().toString(36).slice(2, 8)}`,
      employeeId: match.employee.employeeId,
      employeeName: match.employee.fullName,
      department: match.employee.department,
      attendanceDate,
      checkInTime: now.toISOString(),
      checkInTimeFormatted: getLocalFormattedTime(now, timezone),
      distance: match.distance,
      captureMethod,
      confidenceScore: Math.round(match.confidence),
      reviewStatus: captureMethod === 'manual_override' ? 'under_review' : 'verified',
      notes,
    },
  };
}
