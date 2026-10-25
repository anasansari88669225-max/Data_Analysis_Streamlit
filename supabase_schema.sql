-- ====================================================================
-- FaceAttendance Pro: Supabase / PostgreSQL Database Architecture
-- ====================================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. EMPLOYEES TABLE
CREATE TABLE IF NOT EXISTS employees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    face_embedding JSONB NOT NULL, -- 128-d normalized embedding vector
    avatar_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    biometric_consent_given BOOLEAN NOT NULL DEFAULT TRUE,
    consent_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast lookup on employee_id and active status
CREATE INDEX IF NOT EXISTS idx_employees_lookup ON employees(employee_id, is_active);
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department);

-- 2. ATTENDANCE TABLE
CREATE TABLE IF NOT EXISTS attendance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id VARCHAR(50) NOT NULL,
    employee_name VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    attendance_date DATE NOT NULL, -- Organization-local calendar date
    check_in_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    check_in_time_formatted VARCHAR(20) NOT NULL,
    capture_method VARCHAR(30) NOT NULL CHECK (capture_method IN ('webcam', 'photo_upload', 'manual_override')),
    confidence_score NUMERIC(5, 2) NOT NULL,
    distance NUMERIC(6, 4) NOT NULL,
    review_status VARCHAR(30) NOT NULL DEFAULT 'verified' CHECK (review_status IN ('verified', 'under_review', 'manually_approved')),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Foreign Key Constraint
    CONSTRAINT fk_attendance_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- MANDATORY INVARIANT: Exactly 1 attendance record per employee per calendar date
    CONSTRAINT uq_attendance_employee_date
        UNIQUE (employee_id, attendance_date)
);

-- Indexes for attendance reporting and daily checks
CREATE INDEX IF NOT EXISTS idx_attendance_date_dept ON attendance(attendance_date, department);
CREATE INDEX IF NOT EXISTS idx_attendance_emp_date ON attendance(employee_id, attendance_date);

-- 3. SYSTEM SETTINGS TABLE
CREATE TABLE IF NOT EXISTS system_settings (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'default',
    organization_name VARCHAR(150) NOT NULL DEFAULT 'AeroSync Global Technologies',
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Karachi',
    face_threshold NUMERIC(4, 2) NOT NULL DEFAULT 0.50,
    strict_anti_spoofing BOOLEAN NOT NULL DEFAULT TRUE,
    allow_photo_upload BOOLEAN NOT NULL DEFAULT TRUE,
    late_threshold_time VARCHAR(10) NOT NULL DEFAULT '09:30',
    admin_pin VARCHAR(20) NOT NULL DEFAULT '1234',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_settings ENABLE ROW LEVEL SECURITY;

-- Allow authenticated application service role full access
CREATE POLICY "Allow service role full access to employees"
    ON employees FOR ALL
    USING (true);

CREATE POLICY "Allow service role full access to attendance"
    ON attendance FOR ALL
    USING (true);

CREATE POLICY "Allow service role full access to system_settings"
    ON system_settings FOR ALL
    USING (true);
