import React from 'react';
import {
  LayoutDashboard,
  Camera,
  UserPlus,
  Users,
  CalendarCheck,
  FileSpreadsheet,
  Settings,
  Shield,
  Menu,
  X,
} from 'lucide-react';

export type NavigationTab =
  | 'dashboard'
  | 'mark-attendance'
  | 'register-employee'
  | 'employee-management'
  | 'attendance-history'
  | 'reports'
  | 'settings';

interface SidebarProps {
  activeTab: NavigationTab;
  onTabChange: (tab: NavigationTab) => void;
  organizationName: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  organizationName,
}) => {
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const navItems: { id: NavigationTab; label: string; icon: React.ReactNode }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { id: 'mark-attendance', label: 'Mark Attendance', icon: <Camera className="w-4 h-4" /> },
    { id: 'register-employee', label: 'Register Employee', icon: <UserPlus className="w-4 h-4" /> },
    { id: 'employee-management', label: 'Employee Directory', icon: <Users className="w-4 h-4" /> },
    { id: 'attendance-history', label: 'Attendance History', icon: <CalendarCheck className="w-4 h-4" /> },
    { id: 'reports', label: 'Reports & Analytics', icon: <FileSpreadsheet className="w-4 h-4" /> },
    { id: 'settings', label: 'System Settings', icon: <Settings className="w-4 h-4" /> },
  ];

  return (
    <>
      {/* Mobile Menu Trigger */}
      <div className="md:hidden flex items-center justify-between p-4 bg-[#E8EEF5] border-b border-[#CAD4E2]">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg neu-surface-sm flex items-center justify-center text-blue-600 font-bold">
            <Shield className="w-4 h-4" />
          </div>
          <span className="font-bold text-sm tracking-tight text-slate-800">FaceAttendance Pro</span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-2 neu-btn text-slate-700"
          aria-label="Toggle navigation menu"
        >
          {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Sidebar Container */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 w-64 bg-[#E8EEF5] border-r border-[#D6E0EC]/70 flex flex-col justify-between p-5 transition-transform duration-200 ease-in-out md:translate-x-0 ${
          mobileOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full'
        }`}
      >
        <div>
          {/* Brand Wordmark */}
          <div className="flex items-center gap-3 px-2 py-3 mb-6">
            <div className="w-10 h-10 rounded-xl neu-surface flex items-center justify-center text-blue-600 font-extrabold shadow-md">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <div className="font-bold text-base tracking-tight text-slate-900 leading-none">
                FaceAttendance
              </div>
              <div className="text-[11px] font-medium text-slate-500 mt-1 truncate max-w-[140px]">
                {organizationName}
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-2" aria-label="Main Navigation">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onTabChange(item.id);
                    setMobileOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 text-xs font-semibold rounded-xl text-left transition-all ${
                    isActive
                      ? 'neu-tab-active text-blue-700'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-[#E1E8F2]/60'
                  }`}
                >
                  <span className={isActive ? 'text-blue-600' : 'text-slate-500'}>{item.icon}</span>
                  <span className="truncate">{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* System Privacy & Version Indicator */}
        <div className="pt-4 border-t border-[#D6E0EC]/70">
          <div className="px-3 py-2.5 neu-surface-sm text-[11px] text-slate-500">
            <div className="font-medium text-slate-700">Enterprise Biometrics</div>
            <div className="text-[10px] text-slate-500 mt-0.5">GDPR & Privacy Compliant</div>
          </div>
        </div>
      </aside>

      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          onClick={() => setMobileOpen(false)}
          className="fixed inset-0 bg-slate-900/30 backdrop-blur-xs z-30 md:hidden"
        />
      )}
    </>
  );
};
