import React, { useState } from 'react';
import {
  Settings,
  Sliders,
  Globe,
  Lock,
  Database,
  RotateCcw,
  CheckCircle2,
  Shield,
  FileText,
  X,
} from 'lucide-react';
import { SystemSettings } from '../types';

interface SettingsViewProps {
  settings: SystemSettings;
  onUpdateSettings: (newSettings: SystemSettings) => void;
  onResetData: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({
  settings,
  onUpdateSettings,
  onResetData,
}) => {
  const [currentSettings, setCurrentSettings] = useState<SystemSettings>(settings);
  const [savedNotice, setSavedNotice] = useState(false);
  const [showPrivacyPolicy, setShowPrivacyPolicy] = useState(false);

  const timezones = [
    { value: 'Asia/Karachi', label: 'Asia/Karachi (PKT, UTC+5) - Default' },
    { value: 'UTC', label: 'UTC (Coordinated Universal Time)' },
    { value: 'Asia/Dubai', label: 'Asia/Dubai (GST, UTC+4)' },
    { value: 'Asia/Dhaka', label: 'Asia/Dhaka (BST, UTC+6)' },
    { value: 'Asia/Kolkata', label: 'Asia/Kolkata (IST, UTC+5:30)' },
    { value: 'Asia/Tokyo', label: 'Asia/Tokyo (JST, UTC+9)' },
    { value: 'Europe/London', label: 'Europe/London (GMT/BST)' },
    { value: 'America/New_York', label: 'America/New_York (EST/EDT, UTC-5)' },
    { value: 'America/Los_Angeles', label: 'America/Los_Angeles (PST/PDT, UTC-8)' },
  ];

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdateSettings(currentSettings);
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 2500);
  };

  const handleReset = () => {
    if (
      window.confirm(
        'Are you sure you want to restore the default sample employees and attendance records? Any newly added data will be overwritten.'
      )
    ) {
      onResetData();
      alert('Default demonstration data and settings successfully restored.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="neu-surface p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">System Configuration & Policies</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Configure organization timezones, facial recognition similarity thresholds, and compliance policies
          </p>
        </div>

        <button
          onClick={() => setShowPrivacyPolicy(true)}
          className="neu-btn px-4 py-2 text-xs font-semibold text-blue-700 flex items-center gap-1.5 shrink-0"
        >
          <FileText className="w-4 h-4" />
          <span>Biometric Privacy Policy</span>
        </button>
      </div>

      {savedNotice && (
        <div className="neu-surface p-4 border-l-4 border-l-emerald-500 flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
          <span className="text-xs font-semibold text-emerald-900">
            Settings updated and stored in persistent state!
          </span>
        </div>
      )}

      {/* Main Settings Form */}
      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Timezone & Organization */}
        <div className="neu-surface p-6 space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-[#D6E0EC]/70">
            <Globe className="w-4 h-4 text-blue-600" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Organization & Timezone Boundary
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Organization Display Name
              </label>
              <input
                type="text"
                value={currentSettings.organizationName}
                onChange={(e) =>
                  setCurrentSettings({ ...currentSettings, organizationName: e.target.value })
                }
                className="w-full px-4 py-2.5 text-xs neu-inset-field"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Official Timezone (Calendar Day Calculation)
              </label>
              <select
                value={currentSettings.timezone}
                onChange={(e) =>
                  setCurrentSettings({ ...currentSettings, timezone: e.target.value })
                }
                className="w-full px-4 py-2.5 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
              >
                {timezones.map((tz) => (
                  <option key={tz.value} value={tz.value}>
                    {tz.label}
                  </option>
                ))}
              </select>
              <p className="text-[11px] text-slate-500 mt-1">
                Determines midnight resets and strictly prevents duplicate check-ins on the same calendar day.
              </p>
            </div>
          </div>
        </div>

        {/* Section 2: Biometric Model & Thresholds */}
        <div className="neu-surface p-6 space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-[#D6E0EC]/70">
            <Sliders className="w-4 h-4 text-blue-600" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Biometric Matching Thresholds
            </h3>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-800">
                Cosine Distance Threshold: <strong className="text-blue-700 tabular-nums">{currentSettings.faceThreshold.toFixed(2)}</strong>
              </span>
              <span className="text-slate-500 text-[11px]">
                {currentSettings.faceThreshold <= 0.40
                  ? 'Strict / High Security'
                  : currentSettings.faceThreshold <= 0.55
                  ? 'Balanced (Recommended)'
                  : 'Lenient / High Tolerance'}
              </span>
            </div>

            <input
              type="range"
              min="0.30"
              max="0.70"
              step="0.05"
              value={currentSettings.faceThreshold}
              onChange={(e) =>
                setCurrentSettings({
                  ...currentSettings,
                  faceThreshold: parseFloat(e.target.value),
                })
              }
              className="w-full accent-blue-600 cursor-pointer"
            />

            <div className="flex justify-between text-[10px] text-slate-500 font-medium">
              <span>0.30 (Lower FAR, potential false reject)</span>
              <span>0.50 (Standard)</span>
              <span>0.70 (Higher tolerance for lighting)</span>
            </div>

            <div className="p-3 neu-inset rounded-lg text-[11px] text-slate-600 leading-relaxed">
              <strong>Security Guidance:</strong> Lower threshold values require tighter facial alignment and higher cosine similarity, minimizing False Acceptance Rates (FAR). Higher values accommodate varied office lighting and minor camera angles at the cost of slightly looser matching margins.
            </div>
          </div>
        </div>

        {/* Section 3: Security & Supervisor Override PIN */}
        <div className="neu-surface p-6 space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-[#D6E0EC]/70">
            <Lock className="w-4 h-4 text-blue-600" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Supervisor Security & Access Controls
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Supervisor Override PIN
              </label>
              <input
                type="password"
                maxLength={6}
                value={currentSettings.adminPin}
                onChange={(e) =>
                  setCurrentSettings({ ...currentSettings, adminPin: e.target.value })
                }
                className="w-full px-4 py-2.5 text-xs neu-inset-field"
                required
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Required to authorize manual non-biometric attendance overrides.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Standard Workday Late Threshold
              </label>
              <input
                type="time"
                value={currentSettings.lateThresholdTime}
                onChange={(e) =>
                  setCurrentSettings({ ...currentSettings, lateThresholdTime: e.target.value })
                }
                className="w-full px-4 py-2.5 text-xs neu-inset-field"
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Check-ins recorded after this time are marked as late arrival.
              </p>
            </div>
          </div>
        </div>

        {/* Section 4: Database & Demo Data Restoration */}
        <div className="neu-surface p-6 space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-[#D6E0EC]/70">
            <Database className="w-4 h-4 text-blue-600" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Storage Engine & Reset Controls
            </h3>
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 neu-surface-sm">
            <div>
              <div className="text-xs font-bold text-slate-800">
                Storage Status: Persistent Client State & Supabase Ready
              </div>
              <div className="text-[11px] text-slate-500 mt-0.5">
                All employee biometrics and attendance records are securely persisted locally.
              </div>
            </div>

            <button
              type="button"
              onClick={handleReset}
              className="neu-btn px-4 py-2 text-xs font-semibold text-rose-700 hover:text-rose-800 flex items-center gap-1.5 shrink-0"
            >
              <RotateCcw className="w-4 h-4 text-rose-600" />
              <span>Reset Default Demo Data</span>
            </button>
          </div>
        </div>

        {/* Save Changes Button */}
        <div className="flex items-center justify-end">
          <button
            type="submit"
            className="neu-btn-primary px-8 py-3 text-xs font-bold flex items-center gap-2"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Apply & Save Configuration</span>
          </button>
        </div>
      </form>

      {/* Biometric Privacy Policy Modal */}
      {showPrivacyPolicy && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="w-full max-w-2xl max-h-[85vh] overflow-y-auto neu-surface p-6 sm:p-8 space-y-4">
            <div className="flex items-center justify-between border-b border-[#D6E0EC]/70 pb-3">
              <div className="flex items-center gap-2 text-blue-600 font-bold text-sm">
                <Shield className="w-5 h-5" />
                <span>Biometric Data Processing & Privacy Notice</span>
              </div>
              <button
                onClick={() => setShowPrivacyPolicy(false)}
                className="p-1 text-slate-400 hover:text-slate-700"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs text-slate-600 leading-relaxed">
              <h4 className="font-bold text-slate-900">1. Purpose of Collection</h4>
              <p>
                Facial recognition vectors are processed solely to authenticate employee identity for time, attendance, and physical access verification. Biometric data is never shared with unauthorized third parties or used for commercial marketing.
              </p>

              <h4 className="font-bold text-slate-900">2. Storage & Encryption</h4>
              <p>
                Raw facial imagery is transformed into mathematical 128-dimensional embedding vectors. Raw photos are not perpetually retained unless explicitly chosen during enrollment, and vectors cannot be reverse-engineered into photographic representations.
              </p>

              <h4 className="font-bold text-slate-900">3. Employee Rights & Right to Erasure</h4>
              <p>
                Under GDPR Article 17 and global biometric privacy standards, employees retain the right to withdraw biometric consent at any time and request immediate, irreversible purging of all biometric templates through the administrator dashboard.
              </p>

              <h4 className="font-bold text-slate-900">4. Non-Biometric Alternative</h4>
              <p>
                A non-biometric manual authorization path is maintained for any employees with temporary injuries or privacy exemptions. Biometric matching is never used as the sole automated basis for adverse employment or disciplinary decisions.
              </p>
            </div>

            <div className="pt-3 border-t border-[#D6E0EC]/70 flex justify-end">
              <button
                onClick={() => setShowPrivacyPolicy(false)}
                className="neu-btn-primary px-5 py-2 text-xs font-bold"
              >
                Understood & Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
