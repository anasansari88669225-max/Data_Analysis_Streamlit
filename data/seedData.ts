import { Employee, AttendanceRecord, SystemSettings } from '../types';
import { getLocalCalendarDate, getLocalFormattedTime } from '../utils/attendanceRules';
import { generateDeterministicEmbedding } from '../utils/faceMath';

export const INITIAL_SETTINGS: SystemSettings = {
  organizationName: 'Demo Organization',
  timezone: 'Asia/Karachi',
  faceThreshold: 0.45,
  adminPin: '1234',
  lateThresholdTime: '09:00',
};

const createdAt = new Date().toISOString();

export const INITIAL_EMPLOYEES: Employee[] = [
  {
    id: 'emp-demo-001',
    employeeId: 'EMP-001',
    fullName: 'Alex Morgan',
    department: 'Engineering',
    jobTitle: 'Software Engineer',
    email: 'alex.morgan@example.com',
    faceEmbedding: generateDeterministicEmbedding('demo-employee-001'),
    isActive: true,
    biometricConsentGiven: true,
    consentTimestamp: createdAt,
    createdAt,
    updatedAt: createdAt,
  },
  {
    id: 'emp-demo-002',
    employeeId: 'EMP-002',
    fullName: 'Jordan Lee',
    department: 'Operations',
    jobTitle: 'Operations Coordinator',
    email: 'jordan.lee@example.com',
    faceEmbedding: generateDeterministicEmbedding('demo-employee-002'),
    isActive: true,
    biometricConsentGiven: true,
    consentTimestamp: createdAt,
    createdAt,
    updatedAt: createdAt,
  },
  {
    id: 'emp-demo-003',
    employeeId: 'EMP-003',
    fullName: 'Taylor Kim',
    department: 'People',
    jobTitle: 'People Partner',
    email: 'taylor.kim@example.com',
    faceEmbedding: generateDeterministicEmbedding('demo-employee-003'),
    isActive: true,
    biometricConsentGiven: true,
    consentTimestamp: createdAt,
    createdAt,
    updatedAt: createdAt,
  },
];

export function getInitialAttendanceRecords(): AttendanceRecord[] {
  const now = new Date();
  const today = getLocalCalendarDate(now, INITIAL_SETTINGS.timezone);
  const checkInTime = new Date(now);
  checkInTime.setHours(9, 15, 0, 0);

  return [
    {
      id: 'att-demo-001',
      employeeId: 'EMP-001',
      employeeName: 'Alex Morgan',
      department: 'Engineering',
      attendanceDate: today,
      checkInTime: checkInTime.toISOString(),
      checkInTimeFormatted: getLocalFormattedTime(checkInTime, INITIAL_SETTINGS.timezone),
      distance: 0.018,
      captureMethod: 'webcam',
      confidenceScore: 98,
      reviewStatus: 'verified',
    },
    {
      id: 'att-demo-002',
      employeeId: 'EMP-002',
      employeeName: 'Jordan Lee',
      department: 'Operations',
      attendanceDate: today,
      checkInTime: new Date(checkInTime.getTime() + 12 * 60 * 1000).toISOString(),
      checkInTimeFormatted: getLocalFormattedTime(
        new Date(checkInTime.getTime() + 12 * 60 * 1000),
        INITIAL_SETTINGS.timezone,
      ),
      distance: 0.026,
      captureMethod: 'photo_upload',
      confidenceScore: 96,
      reviewStatus: 'verified',
    },
  ];
}
