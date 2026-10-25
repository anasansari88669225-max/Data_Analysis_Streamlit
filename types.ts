export interface Employee {
  id: string;
  employeeId: string;
  fullName: string;
  department: string;
  jobTitle: string;
  email?: string;
  faceEmbedding?: number[];
  avatarUrl?: string;
  isActive: boolean;
  biometricConsentGiven: boolean;
  consentTimestamp?: string;
  createdAt: string;
  updatedAt: string;
}

export type CaptureMethod = 'webcam' | 'photo_upload' | 'manual_override';

export type ReviewStatus = 'verified' | 'under_review' | 'manually_approved';

export interface AttendanceRecord {
  id: string;
  employeeId: string;
  employeeName: string;
  department: string;
  attendanceDate: string;
  checkInTime: string;
  checkInTimeFormatted: string;
  distance: number;
  captureMethod: CaptureMethod;
  confidenceScore: number;
  reviewStatus: ReviewStatus;
  notes?: string;
}

export interface SystemSettings {
  organizationName: string;
  timezone: string;
  faceThreshold: number;
  adminPin: string;
  lateThresholdTime: string;
}

export interface MatchResult {
  matched: boolean;
  employee: Employee | null;
  distance: number;
  confidence: number;
  threshold: number;
  message: string;
}
