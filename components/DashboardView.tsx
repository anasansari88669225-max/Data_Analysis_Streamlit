import React from 'react';
import {
  Users,
  UserCheck,
  UserX,
  TrendingUp,
  Camera,
  UserPlus,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import { Employee, AttendanceRecord, SystemSettings } from '../types';
import { getLocalCalendarDate } from '../utils/attendanceRules';
import { NavigationTab } from './Sidebar';

interface DashboardViewProps {
  employees: Employee[];
  records: AttendanceRecord[];
  settings: SystemSettings;
  onNavigate: (tab: NavigationTab) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  employees,
  records,
  settings,
  onNavigate,
}) => {
  const todayStr = getLocalCalendarDate(new Date(), settings.timezone);

  const activeEmployees = employees.filter((e) => e.isActive);
  const totalActive = activeEmployees.length;

  const todayRecords = records.filter((r) => r.attendanceDate === todayStr);
  const presentTodayCount = todayRecords.length;
  const pendingCount = Math.max(0, totalActive - presentTodayCount);
  const attendanceRate = totalActive > 0 ? Math.round((presentTodayCount / totalActive) * 1000) / 10 : 0;

  // Calculate 7-Day Trend
  const last7Days: { dateStr: string; label: string; count: number }[] = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateFormatted = getLocalCalendarDate(d, settings.timezone);
    const dayLabel = d.toLocaleDateString('en-US', { weekday: 'short', month: 'numeric', day: 'numeric' });
    const count = records.filter((r) => r.attendanceDate === dateFormatted).length;
    last7Days.push({ dateStr: dateFormatted, label: dayLabel, count });
  }

  const maxDailyCount = Math.max(1, ...last7Days.map((d) => d.count), totalActive);

  // Department Summary
  const departments = Array.from(new Set(activeEmployees.map((e) => e.department)));
  const deptStats = departments.map((dept) => {
    const totalInDept = activeEmployees.filter((e) => e.department === dept).length;
    const presentInDept = todayRecords.filter((r) => r.department === dept).length;
    const pct = totalInDept > 0 ? Math.round((presentInDept / totalInDept) * 100) : 0;
    return { dept, total: totalInDept, present: presentInDept, pct };
  });

  // Recent 5 attendances
  const recentRecords = records.slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Hero Banner with Executive Access Terminal */}
      <div className="neu-surface overflow-hidden p-6 sm:p-8 flex flex-col lg:flex-row items-center gap-8 justify-between relative">
        <div className="max-w-xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 neu-surface-sm text-xs font-semibold text-blue-700">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <span>Attendance System Prototype</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight text-balance">
            Attendance Management & Verification Demo
          </h2>
          <p className="text-sm text-slate-600 leading-relaxed">
            This prototype uses synthetic test vectors, not face-derived biometric templates. Webcam and photo capture are previews only; use supervisor-authorized manual check-in for attendance.
          </p>
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => onNavigate('mark-attendance')}
              className="neu-btn-primary px-5 py-2.5 text-xs font-semibold flex items-center gap-2"
            >
              <Camera className="w-4 h-4" />
              <span>Launch Camera Terminal</span>
            </button>
            <button
              onClick={() => onNavigate('register-employee')}
              className="neu-btn px-5 py-2.5 text-xs font-semibold text-slate-700 flex items-center gap-2"
            >
              <UserPlus className="w-4 h-4 text-blue-600" />
              <span>Enroll New Employee</span>
            </button>
          </div>
        </div>

        <div
          role="img"
          aria-label="Attendance verification terminal illustration"
          className="w-full lg:w-96 h-48 sm:h-52 shrink-0 rounded-xl overflow-hidden neu-surface-sm flex items-center justify-center bg-gradient-to-br from-blue-100 via-slate-100 to-indigo-100"
        >
          <div className="relative flex h-32 w-32 items-center justify-center rounded-full border border-blue-200 bg-white/70 shadow-inner">
            <div className="absolute inset-3 rounded-full border border-dashed border-blue-300" />
            <ShieldCheck className="h-14 w-14 text-blue-600" aria-hidden="true" />
          </div>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Metric 1 */}
        <div className="neu-surface p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Staff</span>
            <div className="w-9 h-9 rounded-xl neu-surface-sm flex items-center justify-center text-blue-600">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-extrabold text-slate-900 tabular-nums">
            {totalActive}
          </div>
          <div className="mt-1 text-xs text-slate-500">
            Registered employees
          </div>
        </div>

        {/* Metric 2 */}
        <div className="neu-surface p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Present Today</span>
            <div className="w-9 h-9 rounded-xl neu-surface-sm flex items-center justify-center text-emerald-600">
              <UserCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-extrabold text-emerald-600 tabular-nums">
            {presentTodayCount}
          </div>
          <div className="mt-1 text-xs text-slate-500">
            Verified today ({todayStr})
          </div>
        </div>

        {/* Metric 3 */}
        <div className="neu-surface p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Pending Check-in</span>
            <div className="w-9 h-9 rounded-xl neu-surface-sm flex items-center justify-center text-amber-600">
              <UserX className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-extrabold text-amber-600 tabular-nums">
            {pendingCount}
          </div>
          <div className="mt-1 text-xs text-slate-500">
            Not yet checked in today
          </div>
        </div>

        {/* Metric 4 */}
        <div className="neu-surface p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Attendance Rate</span>
            <div className="w-9 h-9 rounded-xl neu-surface-sm flex items-center justify-center text-blue-600">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 text-3xl font-extrabold text-slate-900 tabular-nums">
            {attendanceRate}%
          </div>
          <div className="mt-1 text-xs text-slate-500">
            Organization target: 90%
          </div>
        </div>
      </div>

      {/* Main Charts & Feeds Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 7-Day Trend Bar Chart */}
        <div className="lg:col-span-2 neu-surface p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-[#D6E0EC]/60 pb-3">
            <div>
              <h3 className="text-sm font-bold text-slate-900">7-Day Attendance Activity</h3>
              <p className="text-xs text-slate-500 mt-0.5">Daily biometric check-in volume</p>
            </div>
            <button
              onClick={() => onNavigate('attendance-history')}
              className="text-xs text-blue-600 font-semibold hover:underline inline-flex items-center gap-1"
            >
              <span>View Logs</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Neumorphic SVG/HTML Bar Chart */}
          <div className="pt-4">
            <div className="grid grid-cols-7 gap-2 sm:gap-4 items-end h-48 pb-2">
              {last7Days.map((day, idx) => {
                const heightPct = Math.round((day.count / maxDailyCount) * 100);
                const isToday = day.dateStr === todayStr;
                return (
                  <div key={idx} className="flex flex-col items-center gap-2 h-full justify-end group">
                    <span className="text-[11px] font-bold text-slate-700 tabular-nums group-hover:text-blue-600">
                      {day.count}
                    </span>
                    <div className="w-full max-w-[42px] bg-[#DFE6F0] rounded-lg neu-inset p-1 flex items-end h-36">
                      <div
                        style={{ height: `${Math.max(8, heightPct)}%` }}
                        className={`w-full rounded-md transition-all duration-300 ${
                          isToday ? 'bg-blue-600 shadow-sm' : 'bg-slate-400 group-hover:bg-slate-500'
                        }`}
                      />
                    </div>
                    <span className="text-[10px] font-medium text-slate-500 truncate max-w-full text-center">
                      {day.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Department Attendance Distribution */}
        <div className="neu-surface p-6 space-y-4">
          <div className="border-b border-[#D6E0EC]/60 pb-3">
            <h3 className="text-sm font-bold text-slate-900">Department Overview</h3>
            <p className="text-xs text-slate-500 mt-0.5">Today's presence by unit</p>
          </div>

          <div className="space-y-3.5">
            {deptStats.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">No department data available.</p>
            ) : (
              deptStats.map((item, idx) => (
                <div key={idx} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-700">{item.dept}</span>
                    <span className="tabular-nums font-semibold text-slate-900">
                      {item.present} / {item.total}{' '}
                      <span className="text-slate-500 text-[11px]">({item.pct}%)</span>
                    </span>
                  </div>
                  <div className="w-full h-2 rounded-full neu-inset overflow-hidden">
                    <div
                      style={{ width: `${item.pct}%` }}
                      className="h-full bg-blue-600 rounded-full transition-all duration-300"
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Live Recent Activity Table */}
      <div className="neu-surface p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-[#D6E0EC]/60 pb-3">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Recent Attendance Records</h3>
            <p className="text-xs text-slate-500 mt-0.5">Live log of verified employee check-ins</p>
          </div>
          <button
            onClick={() => onNavigate('reports')}
            className="neu-btn px-3 py-1.5 text-xs font-semibold text-slate-700"
          >
            Export CSV
          </button>
        </div>

        {recentRecords.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">
            No attendance records logged yet today.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-[11px] font-bold text-slate-500 border-b border-[#D6E0EC]/70 uppercase tracking-wider">
                  <th className="py-2.5 px-3">Employee</th>
                  <th className="py-2.5 px-3">Department</th>
                  <th className="py-2.5 px-3">Date</th>
                  <th className="py-2.5 px-3">Check-In Time</th>
                  <th className="py-2.5 px-3">Method</th>
                  <th className="py-2.5 px-3 text-right">Confidence</th>
                  <th className="py-2.5 px-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#D6E0EC]/50 text-xs text-slate-700">
                {recentRecords.map((rec) => (
                  <tr key={rec.id} className="hover:bg-[#E2E8F1]/40 transition-colors">
                    <td className="py-3 px-3 font-semibold text-slate-900">
                      <div>{rec.employeeName}</div>
                      <div className="text-[10px] text-slate-500 tabular-nums">{rec.employeeId}</div>
                    </td>
                    <td className="py-3 px-3">{rec.department}</td>
                    <td className="py-3 px-3 tabular-nums">{rec.attendanceDate}</td>
                    <td className="py-3 px-3 tabular-nums font-semibold">{rec.checkInTimeFormatted}</td>
                    <td className="py-3 px-3">
                      <span className="capitalize text-slate-600">
                        {rec.captureMethod.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right tabular-nums font-semibold text-blue-700">
                      {rec.confidenceScore}%
                    </td>
                    <td className="py-3 px-3 text-right">
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
