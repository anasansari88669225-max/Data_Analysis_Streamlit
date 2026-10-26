import React, { useState } from 'react';
import {
  Search,
  Filter,
  CheckCircle,
  Clock,
  Camera,
  Upload,
  KeyRound,
  Check,
} from 'lucide-react';
import { AttendanceRecord, SystemSettings } from '../types';
import { getLocalCalendarDate } from '../utils/attendanceRules';

interface AttendanceHistoryViewProps {
  records: AttendanceRecord[];
  settings: SystemSettings;
  onApproveRecord: (recordId: string) => void;
}

export const AttendanceHistoryView: React.FC<AttendanceHistoryViewProps> = ({
  records,
  settings,
  onApproveRecord,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [dateFilter, setDateFilter] = useState<'ALL' | 'TODAY' | 'YESTERDAY' | 'LAST7'>('ALL');
  const [methodFilter, setMethodFilter] = useState<'ALL' | 'webcam' | 'photo_upload' | 'manual_override' | 'demo_simulation'>('ALL');
  const [deptFilter, setDeptFilter] = useState('ALL');

  const todayStr = getLocalCalendarDate(new Date(), settings.timezone);

  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = getLocalCalendarDate(yesterday, settings.timezone);

  const departments = ['ALL', ...Array.from(new Set(records.map((r) => r.department)))];

  const filtered = records.filter((rec) => {
    // Search
    const matchesSearch =
      rec.employeeName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      rec.employeeId.toLowerCase().includes(searchQuery.toLowerCase());

    // Date
    let matchesDate = true;
    if (dateFilter === 'TODAY') {
      matchesDate = rec.attendanceDate === todayStr;
    } else if (dateFilter === 'YESTERDAY') {
      matchesDate = rec.attendanceDate === yesterdayStr;
    } else if (dateFilter === 'LAST7') {
      const recDate = new Date(rec.attendanceDate);
      const diffDays = (Date.now() - recDate.getTime()) / (1000 * 3600 * 24);
      matchesDate = diffDays <= 7;
    }

    // Method
    const matchesMethod = methodFilter === 'ALL' || rec.captureMethod === methodFilter;

    // Dept
    const matchesDept = deptFilter === 'ALL' || rec.department === deptFilter;

    return matchesSearch && matchesDate && matchesMethod && matchesDept;
  });

  return (
    <div className="space-y-6">
      {/* Filter and Search Bar */}
      <div className="neu-surface p-5 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-900">Attendance Log History</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Auditable timestamp records with capture method and biometric confidence metrics
            </p>
          </div>
          <div className="text-xs text-slate-500">
            Showing <strong className="text-slate-800">{filtered.length}</strong> of{' '}
            <strong className="text-slate-800">{records.length}</strong> logged entries
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by ID or name..."
              className="w-full pl-9 pr-4 py-2 text-xs neu-inset-field"
            />
          </div>

          {/* Date Range Selector */}
          <div>
            <select
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value as 'ALL' | 'TODAY' | 'YESTERDAY' | 'LAST7')}
              className="w-full px-3 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
            >
              <option value="ALL">All Recorded Dates</option>
              <option value="TODAY">Today ({todayStr})</option>
              <option value="YESTERDAY">Yesterday</option>
              <option value="LAST7">Past 7 Days</option>
            </select>
          </div>

          {/* Capture Method */}
          <div>
            <select
              value={methodFilter}
              onChange={(e) => setMethodFilter(e.target.value as 'ALL' | 'webcam' | 'photo_upload' | 'manual_override' | 'demo_simulation')}
              className="w-full px-3 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
            >
              <option value="ALL">All Capture Methods</option>
              <option value="webcam">Live Webcam</option>
              <option value="photo_upload">Photo Upload</option>
              <option value="manual_override">Manual Override</option>
              <option value="demo_simulation">Synthetic Demo</option>
            </select>
          </div>

          {/* Department */}
          <div>
            <select
              value={deptFilter}
              onChange={(e) => setDeptFilter(e.target.value)}
              className="w-full px-3 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
            >
              {departments.map((dept) => (
                <option key={dept} value={dept}>
                  {dept === 'ALL' ? 'All Departments' : dept}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Attendance Table */}
      <div className="neu-surface overflow-hidden">
        {filtered.length === 0 ? (
          <div className="p-10 text-center text-xs text-slate-500">
            No attendance records match the selected filters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-[11px] font-bold text-slate-500 border-b border-[#D6E0EC]/70 uppercase tracking-wider bg-[#E8EEF5]">
                  <th className="py-3 px-4">Employee</th>
                  <th className="py-3 px-4">Department</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Check-in Time</th>
                  <th className="py-3 px-4">Method</th>
                  <th className="py-3 px-4 text-right">Confidence</th>
                  <th className="py-3 px-4 text-right">Review Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#D6E0EC]/50 text-xs text-slate-700">
                {filtered.map((rec) => (
                  <tr key={rec.id} className="hover:bg-[#E2E8F1]/40 transition-colors">
                    {/* Employee */}
                    <td className="py-3 px-4 font-semibold text-slate-900">
                      <div>{rec.employeeName}</div>
                      <div className="text-[10px] text-blue-700 tabular-nums">{rec.employeeId}</div>
                    </td>

                    {/* Department */}
                    <td className="py-3 px-4 text-slate-600">{rec.department}</td>

                    {/* Date */}
                    <td className="py-3 px-4 tabular-nums text-slate-700 font-medium">
                      {rec.attendanceDate}
                    </td>

                    {/* Time */}
                    <td className="py-3 px-4 tabular-nums font-bold text-slate-900">
                      {rec.checkInTimeFormatted}
                    </td>

                    {/* Method */}
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center gap-1.5 text-xs text-slate-600">
                        {rec.captureMethod === 'webcam' ? (
                          <Camera className="w-3.5 h-3.5 text-blue-600" />
                        ) : rec.captureMethod === 'photo_upload' ? (
                          <Upload className="w-3.5 h-3.5 text-amber-600" />
                        ) : rec.captureMethod === 'demo_simulation' ? (
                          <Check className="w-3.5 h-3.5 text-blue-600" />
                        ) : (
                          <KeyRound className="w-3.5 h-3.5 text-slate-500" />
                        )}
                        <span className="capitalize">{rec.captureMethod.replace('_', ' ')}</span>
                      </span>
                    </td>

                    {/* Confidence */}
                    <td className="py-3 px-4 text-right tabular-nums font-semibold text-blue-700">
                      {rec.confidenceScore}%
                      <div className="text-[10px] text-slate-400 font-normal">
                        dist: {rec.distance.toFixed(3)}
                      </div>
                    </td>

                    {/* Review Status */}
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

                    {/* Action */}
                    <td className="py-3 px-4 text-right">
                      {rec.reviewStatus === 'under_review' ? (
                        <button
                          onClick={() => onApproveRecord(rec.id)}
                          className="neu-btn px-2.5 py-1 text-[11px] font-semibold text-emerald-700 hover:text-emerald-800 inline-flex items-center gap-1"
                          title="Manually verify this attendance record"
                        >
                          <Check className="w-3 h-3" />
                          <span>Approve</span>
                        </button>
                      ) : (
                        <span className="text-[11px] text-slate-400">Locked</span>
                      )}
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
