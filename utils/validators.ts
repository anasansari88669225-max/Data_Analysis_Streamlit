import { Employee } from '../types';

interface EmployeeRegistrationInput {
  employeeId: string;
  fullName: string;
  department: string;
  jobTitle: string;
  email: string;
  consentGiven: boolean;
  hasFaceImage: boolean;
}

export function validateEmployeeRegistration(
  input: EmployeeRegistrationInput,
  employees: Employee[],
): { isValid: boolean; errors: Record<string, string> } {
  const errors: Record<string, string> = {};
  const employeeId = input.employeeId.trim();

  if (!employeeId) {
    errors.employeeId = 'Employee ID is required.';
  } else if (employees.some((employee) => employee.employeeId.toLowerCase() === employeeId.toLowerCase())) {
    errors.employeeId = 'This employee ID is already registered.';
  }
  if (!input.fullName.trim()) errors.fullName = 'Full name is required.';
  if (!input.department.trim()) errors.department = 'Department is required.';
  if (!input.jobTitle.trim()) errors.jobTitle = 'Job title is required.';
  if (input.email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.email.trim())) {
    errors.email = 'Enter a valid email address.';
  }
  if (!input.consentGiven) errors.consent = 'Biometric consent is required.';
  if (!input.hasFaceImage) errors.face = 'A profile image is required for this demo.';

  return { isValid: Object.keys(errors).length === 0, errors };
}

export function validateImageUpload(file: File): { valid: boolean; error?: string } {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: 'Choose a JPG, PNG, or WebP image.' };
  }
  if (file.size > 5 * 1024 * 1024) {
    return { valid: false, error: 'Image must be 5 MB or smaller.' };
  }
  return { valid: true };
}
