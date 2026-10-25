import { useState, useEffect } from 'react';
import { Sidebar, NavigationTab } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardView } from './components/DashboardView';
import { MarkAttendanceView } from './components/MarkAttendanceView';
import { RegisterEmployeeView } from './components/RegisterEmployeeView';
import { EmployeeManagementView } from './components/EmployeeManagementView';
import { AttendanceHistoryView } from './components/AttendanceHistoryView';
import { ReportsView } from './components/ReportsView';
import { SettingsView } from './components/SettingsView';
import {
  INITIAL_SETTINGS,
  INITIAL_EMPLOYEES,
  getInitialAttendanceRecords,
} from './data/seedData';
import { Employee, AttendanceRecord, SystemSettings } from './types';

const STORAGE_KEY_EMPLOYEES = 'faceattendance_employees_v1';
const STORAGE_KEY_RECORDS = 'faceattendance_records_v1';
const STORAGE_KEY_SETTINGS = 'faceattendance_settings_v1';

export default function App() {
  const [activeTab, setActiveTab] = useState<NavigationTab>('dashboard');

  // Load state from localStorage or seed data
  const [employees, setEmployees] = useState<Employee[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY_EMPLOYEES);
      if (saved) return JSON.parse(saved);
    } catch {
      // fallback
    }
    return INITIAL_EMPLOYEES;
  });

  const [records, setRecords] = useState<AttendanceRecord[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY_RECORDS);
      if (saved) return JSON.parse(saved);
    } catch {
      // fallback
    }
    return getInitialAttendanceRecords();
  });

  const [settings, setSettings] = useState<SystemSettings>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY_SETTINGS);
      if (saved) return JSON.parse(saved);
    } catch {
      // fallback
    }
    return INITIAL_SETTINGS;
  });

  // Sync to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY_EMPLOYEES, JSON.stringify(employees));
    } catch (e) {
      console.warn('Storage sync error:', e);
    }
  }, [employees]);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY_RECORDS, JSON.stringify(records));
    } catch (e) {
      console.warn('Storage sync error:', e);
    }
  }, [records]);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(settings));
    } catch (e) {
      console.warn('Storage sync error:', e);
    }
  }, [settings]);

  // Handlers
  const handleRecordAdded = (record: AttendanceRecord) => {
    setRecords((prev) => [record, ...prev]);
  };

  const handleEmployeeRegistered = (employee: Employee) => {
    setEmployees((prev) => [employee, ...prev]);
  };

  const handleToggleEmployeeActive = (employeeId: string) => {
    setEmployees((prev) =>
      prev.map((emp) =>
        emp.employeeId === employeeId ? { ...emp, isActive: !emp.isActive } : emp
      )
    );
  };

  const handleDeleteEmployee = (employeeId: string) => {
    // Purge employee and biometric data
    setEmployees((prev) => prev.filter((emp) => emp.employeeId !== employeeId));
  };

  const handleUpdateEmployee = (updated: Employee) => {
    setEmployees((prev) =>
      prev.map((emp) => (emp.employeeId === updated.employeeId ? updated : emp))
    );
  };

  const handleApproveRecord = (recordId: string) => {
    setRecords((prev) =>
      prev.map((rec) =>
        rec.id === recordId ? { ...rec, reviewStatus: 'manually_approved' } : rec
      )
    );
  };

  const handleUpdateSettings = (newSettings: SystemSettings) => {
    setSettings(newSettings);
  };

  const handleResetData = () => {
    setEmployees(INITIAL_EMPLOYEES);
    setRecords(getInitialAttendanceRecords());
    setSettings(INITIAL_SETTINGS);
    localStorage.removeItem(STORAGE_KEY_EMPLOYEES);
    localStorage.removeItem(STORAGE_KEY_RECORDS);
    localStorage.removeItem(STORAGE_KEY_SETTINGS);
  };

  const sectionTitles: Record<NavigationTab, string> = {
    dashboard: 'Dashboard',
    'mark-attendance': 'Mark Attendance',
    'register-employee': 'Register Employee',
    'employee-management': 'Employee Directory',
    'attendance-history': 'Attendance History',
    reports: 'Reports & Analytics',
    settings: 'System Settings',
  };

  return (
    <div className="min-h-screen bg-[#E8EEF5] flex flex-col md:flex-row text-slate-800">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        organizationName={settings.organizationName}
      />

      {/* Main Viewport Content */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen">
        <Header currentSection={sectionTitles[activeTab]} settings={settings} />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && (
            <DashboardView
              employees={employees}
              records={records}
              settings={settings}
              onNavigate={setActiveTab}
            />
          )}

          {activeTab === 'mark-attendance' && (
            <MarkAttendanceView
              employees={employees}
              records={records}
              settings={settings}
              onRecordAdded={handleRecordAdded}
            />
          )}

          {activeTab === 'register-employee' && (
            <RegisterEmployeeView
              existingEmployees={employees}
              onEmployeeRegistered={handleEmployeeRegistered}
              onNavigateToDirectory={() => setActiveTab('employee-management')}
            />
          )}

          {activeTab === 'employee-management' && (
            <EmployeeManagementView
              employees={employees}
              onToggleActive={handleToggleEmployeeActive}
              onDeleteEmployee={handleDeleteEmployee}
              onUpdateEmployee={handleUpdateEmployee}
            />
          )}

          {activeTab === 'attendance-history' && (
            <AttendanceHistoryView
              records={records}
              settings={settings}
              onApproveRecord={handleApproveRecord}
            />
          )}

          {activeTab === 'reports' && (
            <ReportsView records={records} settings={settings} />
          )}

          {activeTab === 'settings' && (
            <SettingsView
              settings={settings}
              onUpdateSettings={handleUpdateSettings}
              onResetData={handleResetData}
            />
          )}
        </main>
      </div>
    </div>
  );
}
