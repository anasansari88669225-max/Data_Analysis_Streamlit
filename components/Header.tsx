import React from 'react';
import { Clock, ShieldCheck, MapPin } from 'lucide-react';
import { getLocalFormattedTime, getLocalCalendarDate } from '../utils/attendanceRules';
import { SystemSettings } from '../types';

interface HeaderProps {
  currentSection: string;
  settings: SystemSettings;
}

export const Header: React.FC<HeaderProps> = ({ currentSection, settings }) => {
  const [timeStr, setTimeStr] = React.useState('');
  const [dateStr, setDateStr] = React.useState('');

  React.useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(getLocalFormattedTime(now, settings.timezone));
      setDateStr(getLocalCalendarDate(now, settings.timezone));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, [settings.timezone]);

  return (
    <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 px-6 py-4 border-b border-[#D6E0EC]/60 bg-[#E8EEF5]">
      {/* Zone 1: Section Breadcrumb & Title */}
      <div>
        <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
          <span>FaceAttendance Pro</span>
          <span aria-hidden="true">/</span>
          <span className="text-slate-700">{currentSection}</span>
        </div>
        <h1 className="text-xl font-bold tracking-tight text-slate-900 mt-0.5">
          {currentSection}
        </h1>
      </div>

      {/* Zone 2: Timezone Clock & Security Badge */}
      <div className="flex flex-wrap items-center gap-3 shrink-0">
        <div className="flex items-center gap-2 px-3 py-1.5 neu-inset text-xs text-slate-600">
          <MapPin className="w-3.5 h-3.5 text-blue-600 shrink-0" />
          <span className="font-medium">{settings.timezone}</span>
          <span aria-hidden="true" className="text-slate-400">·</span>
          <Clock className="w-3.5 h-3.5 text-slate-500 shrink-0" />
          <span className="tabular-nums font-semibold text-slate-800">{timeStr || '09:00:00 AM'}</span>
          <span aria-hidden="true" className="text-slate-400">·</span>
          <span className="tabular-nums text-slate-600">{dateStr}</span>
        </div>

        <div className="flex items-center gap-1.5 px-3 py-1.5 neu-surface-sm text-xs font-semibold text-emerald-800">
          <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>Demo Mode · No Face Recognition</span>
        </div>
      </div>
    </header>
  );
};
