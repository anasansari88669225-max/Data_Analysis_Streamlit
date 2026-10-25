import React, { useState } from 'react';
import {
  FileSpreadsheet,
  Download,
  Calendar,
  Filter,
  Users,
  CheckCircle2,
  Printer,
} from 'lucide-react';
import { AttendanceRecord, SystemSettings } from '../types';
import { generateAttendanceCsv, downloadCsvFile } from '../utils/csvExport';
import { getLocalCalendarDate } from '../utils/attendanceRules';

interface ReportsViewProps {
  records: AttendanceRecord[];
  settings: SystemSettings;
}

export const ReportsView: React.FC<ReportsViewProps> = ({ records, settings }) => {
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [dateRange, setDateRange] = useState<'ALL' | 'TODAY' | 'WEEK' | 'MONTH'>('ALL');
  const [searchEmployee, setSearchEmployee] = useState('');

  const today = getLocalCalendarDate(new Date(), settings.timezone);

  const departments = ['ALL', ...Array.from(new Set(records.map((r) => r.department)))];

  const filteredRecords = records.filter((rec) => {
    // Dept
    const matchDept = selectedDept === 'ALL' || rec.department === selectedDept;

    // Search
    const matchSearch =
      rec.employeeName.toLowerCase().includes(searchEmployee.toLowerCase()) ||
      rec.employeeId.toLowerCase().includes(searchEmployee.toLowerCase());

    // Date
    let matchDate = true;
    if (dateRange === 'TODAY') {
      matchDate = rec.attendanceDate === today;
    } else if (dateRange === 'WEEK') {
      const recDate = new Date(rec.attendanceDate);
      const diffDays = (Date.now() - recDate.getTime()) / (1000 * 3600 * 24);
      matchDate = diffDays <= 7;
    } else if (dateRange === 'MONTH') {
      const recDate = new Date(rec.attendanceDate);
      const diffDays = (Date.now() - recDate.getTime()) / (1000 * 3600 * 24);
      matchDate = diffDays <= 30;
    }

    return matchDept && matchSearch && matchDate;
  });

  // Calculate Summary Metrics
  const totalEntries = filteredRecords.length;
  const uniqueEmployees = new Set(filteredRecords.map((r) => r.employeeId)).size;
  const webcamCount = filteredRecords.filter((r) => r.captureMethod === 'webcam').length;
  const photoUploadCount = filteredRecords.filter((r) => r.captureMethod === 'photo_upload').length;
  const manualCount = filteredRecords.filter((r) => r.captureMethod === 'manual_override').length;

  const handleExportCsv = () => {
    const csvData = generateAttendanceCsv(filteredRecords);
    const fileName = `attendance_report_${today}.csv`;
    downloadCsvFile(csvData, fileName);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6">
      {/* Header and Export Actions */}
      <div className="neu-surface p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">Attendance Reports & Exports</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Generate audit-ready records, compute workforce compliance, and export RFC-4180 CSV sheets
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <button
            onClick={handlePrint}
            className="neu-btn px-3.5 py-2 text-xs font-semibold text-slate-700 flex items-center gap-1.5"
            title="Print Summary Sheet"
          >
            <Printer className="w-4 h-4" />
            <span>Print Report</span>
          </button>

          <button
            onClick={handleExportCsv}
            disabled={filteredRecords.length === 0}
            className="neu-btn-primary px-4 py-2 text-xs font-bold flex items-center gap-2 disabled:opacity-50"
          >
            <Download className="w-4 h-4" />
            <span>Download CSV ({filteredRecords.length})</span>
          </button>
        </div>
      </div>

      {/* Filter Ribbon */}
      <div className="neu-surface p-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Date Filter */}
        <div>
          <label className="block text-[11px] font-bold text-slate-500 mb-1 uppercase tracking-wider">
            Date Window
          </label>
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value as 'ALL' | 'TODAY' | 'WEEK' | 'MONTH')}
            className="w-full px-3 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
          >
            <option value="ALL">Complete History (All Dates)</option>
            <option value="TODAY">Today Only ({today})</option>
            <option value="WEEK">Past 7 Days</option>
            <option value="MONTH">Past 30 Days</option>
          </select>
        </div>

        {/* Department Filter */}
        <div>
          <label className="block text-[11px] font-bold text-slate-500 mb-1 uppercase tracking-wider">
            Department
          </label>
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="w-full px-3 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
          >
            {departments.map((dept) => (
              <option key={dept} value={dept}>
                {dept === 'ALL' ? 'All Departments' : dept}
              </option>
            ))}
          </select>
        </div>

        {/* Employee Search */}
        <div>
          <label className="block text-[11px] font-bold text-slate-500 mb-1 uppercase tracking-wider">
            Employee Filter
          </label>
          <input
            type="text"
            value={searchEmployee}
            onChange={(e) => setSearchEmployee(e.target.value)}
            placeholder="Search by ID or name..."
            className="w-full px-3 py-2 text-xs neu-inset-field"
          />
        </div>
      </div>

      {/* KPI Overview for Filtered Window */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="neu-surface p-4 text-center">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Total Records</span>
          <div className="text-2xl font-extrabold text-slate-900 tabular-nums mt-1">{totalEntries}</div>
        </div>
        <div className="neu-surface p-4 text-center">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Unique Staff</span>
          <div className="text-2xl font-extrabold text-blue-600 tabular-nums mt-1">{uniqueEmployees}</div>
        </div>
        <div className="neu-surface p-4 text-center">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Live Webcam</span>
          <div className="text-2xl font-extrabold text-emerald-600 tabular-nums mt-1">{webcamCount}</div>
        </div>
        <div className="neu-surface p-4 text-center">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Upload / Manual</span>
          <div className="text-2xl font-extrabold text-amber-600 tabular-nums mt-1">
            {photoUploadCount + manualCount}
          </div>
        </div>
      </div>

      {/* Detailed Tabular Report */}
      <div className="neu-surface overflow-hidden">
        <div className="p-4 border-b border-[#D6E0EC]/70 flex items-center justify-between">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-600">
            Filtered Report Table
          </h3>
          <span className="text-[11px] text-slate-500">
            Timezone: <strong>{settings.timezone}</strong>
          </span>
        </div>

        {filteredRecords.length === 0 ? (
          <div className="p-10 text-center text-xs text-slate-500">
            No attendance data found for the selected report filters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-[11px] font-bold text-slate-500 border-b border-[#D6E0EC]/70 uppercase tracking-wider bg-[#E8EEF5]">
                  <th className="py-2.5 px-4">Record ID</th>
                  <th className="py-2.5 px-4">Employee</th>
                  <th className="py-2.5 px-4">Department</th>
                  <th className="py-2.5 px-4">Date</th>
                  <th className="py-2.5 px-4">Time</th>
                  <th className="py-2.5 px-4">Source</th>
                  <th className="py-2.5 px-4 text-right">Confidence</th>
                  <th className="py-2.5 px-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#D6E0EC]/50 text-xs text-slate-700">
                {filteredRecords.map((rec) => (
                  <tr key={rec.id} className="hover:bg-[#E2E8F1]/40 transition-colors">
                    <td className="py-3 px-4 font-mono text-[10px] text-slate-500">{rec.id}</td>
                    <td className="py-3 px-4 font-semibold text-slate-900">
                      {rec.employeeName}{' '}
                      <span className="text-[10px] text-blue-700 font-mono font-normal">
                        ({rec.employeeId})
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-600">{rec.department}</td>
                    <td className="py-3 px-4 tabular-nums">{rec.attendanceDate}</td>
                    <td className="py-3 px-4 tabular-nums font-semibold">{rec.checkInTimeFormatted}</td>
                    <td className="py-3 px-4 capitalize text-slate-600">
                      {rec.captureMethod.replace('_', ' ')}
                    </td>
                    <td className="py-3 px-4 text-right tabular-nums font-semibold text-blue-700">
                      {rec.confidenceScore}%
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-md text-[10px] font-bold uppercase ${
                          rec.reviewStatus === 'verified'
                            ? 'bg-emerald-100 text-emerald-800'
                            : rec.reviewStatus === 'under_review'
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {rec.reviewStatus.replace('_', ' ')}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
