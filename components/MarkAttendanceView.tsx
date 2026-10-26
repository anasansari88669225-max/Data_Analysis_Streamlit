import React, { useRef, useState, useEffect } from 'react';
import {
  Camera,
  Upload,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  RefreshCw,
  KeyRound,
  ShieldAlert,
  Info,
  UserCheck,
} from 'lucide-react';
import { Employee, AttendanceRecord, SystemSettings, MatchResult } from '../types';
import {
  findBestFaceMatch,
  simulateFaceScanVariation,
  generateDeterministicEmbedding,
} from '../utils/faceMath';
import { createAttendanceRecord, getLocalCalendarDate } from '../utils/attendanceRules';
import { validateImageUpload } from '../utils/validators';

interface MarkAttendanceViewProps {
  employees: Employee[];
  records: AttendanceRecord[];
  settings: SystemSettings;
  onRecordAdded: (record: AttendanceRecord) => void;
}

export const MarkAttendanceView: React.FC<MarkAttendanceViewProps> = ({
  employees,
  records,
  settings,
  onRecordAdded,
}) => {
  const [activeMode, setActiveMode] = useState<'camera' | 'upload' | 'manual'>('camera');
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [matchResult, setMatchResult] = useState<MatchResult | null>(null);
  const [attendanceMessage, setAttendanceMessage] = useState<{
    type: 'success' | 'error' | 'duplicate' | 'info';
    title: string;
    description: string;
  } | null>(null);

  // Manual fallback state
  const [manualEmpId, setManualEmpId] = useState('');
  const [manualReason, setManualReason] = useState('Camera hardware unavailable');
  const [manualPin, setManualPin] = useState('');

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Start webcam
  const startCamera = async () => {
    setCameraError(null);
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
        });
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
        setCameraActive(true);
      } else {
        setCameraError('Camera API is not supported by your browser.');
      }
    } catch (err: unknown) {
      console.warn('Camera access error:', err);
      setCameraError(
        'Unable to access local camera device. Please grant browser camera permissions or use the supervisor-authorized manual check-in.'
      );
      setCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setCameraActive(false);
  };

  useEffect(() => {
    if (activeMode === 'camera') {
      startCamera();
    } else {
      stopCamera();
    }
    return () => {
      stopCamera();
    };
  }, [activeMode]);

  // Capture frame from webcam
  const handleCaptureFromCamera = () => {
    if (!videoRef.current || !canvasRef.current) return;
    setIsProcessing(true);
    setAttendanceMessage(null);

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
      setCapturedImage(dataUrl);
      setMatchResult(null);
      setAttendanceMessage({
        type: 'info',
        title: 'Camera Photo Captured',
        description:
          'This demo does not analyze faces. Choose an active employee under Synthetic Demo Check-in below to try the attendance flow; your camera photo will not be used to identify anyone.',
      });
      setIsProcessing(false);
    } else {
      setIsProcessing(false);
    }
  };

  // Upload image handler
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const validation = validateImageUpload(file);
    if (!validation.valid) {
      setAttendanceMessage({
        type: 'error',
        title: 'Invalid Image',
        description: validation.error || 'Please provide a valid image.',
      });
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setCapturedImage(reader.result as string);
      setMatchResult(null);
      setAttendanceMessage({
        type: 'info',
        title: 'Photo Loaded',
        description:
          'This demo does not analyze faces. Choose an active employee under Synthetic Demo Check-in below to try the attendance flow; your photo will not be used to identify anyone.',
      });
    };
    reader.readAsDataURL(file);
  };

  // Execute biometric match & record
  const executeBiometricMatch = (
    forcedEmployeeId: string,
    method: 'webcam' | 'photo_upload' | 'demo_simulation' = 'demo_simulation'
  ) => {
    setIsProcessing(true);

    let probeEmbedding: number[];
    if (forcedEmployeeId !== 'STRANGER-999') {
      const target = employees.find((e) => e.employeeId === forcedEmployeeId);
      if (target && target.faceEmbedding) {
        probeEmbedding = simulateFaceScanVariation(target.faceEmbedding, 0.06);
      } else {
        probeEmbedding = generateDeterministicEmbedding('UNKNOWN-STRANGER');
      }
    } else {
      probeEmbedding = generateDeterministicEmbedding('UNKNOWN-STRANGER');
    }

    const match = findBestFaceMatch(probeEmbedding, employees, settings.faceThreshold);
    setMatchResult(match);

    if (match.matched && match.employee) {
      const saveRes = createAttendanceRecord(match, method, records, settings.timezone);
      if (saveRes.success && saveRes.record) {
        onRecordAdded(saveRes.record);
        setAttendanceMessage({
          type: 'success',
          title: 'Demo Check-in Recorded',
          description: `A synthetic demo check-in was recorded for ${match.employee.fullName} at ${saveRes.record.checkInTimeFormatted} (${settings.timezone}). No face was recognized; this record is flagged for review.`,
        });
      } else {
        setAttendanceMessage({
          type: 'duplicate',
          title: 'Duplicate Check-In Prevented',
          description:
            saveRes.error ||
            `Attendance for ${match.employee.fullName} is already recorded for today in ${settings.timezone}.`,
        });
      }
    } else {
      setAttendanceMessage({
        type: 'error',
        title: 'Biometric Verification Failed',
        description: match.message || 'No registered active employee matched this facial scan.',
      });
    }

    setIsProcessing(false);
  };

  // Manual fallback check-in
  const handleManualCheckIn = (e: React.FormEvent) => {
    e.preventDefault();
    if (!manualEmpId.trim()) return;

    if (manualPin !== settings.adminPin) {
      setAttendanceMessage({
        type: 'error',
        title: 'Supervisor Authorization Required',
        description: 'Incorrect supervisor PIN. Manual attendance override requires authorization.',
      });
      return;
    }

    const emp = employees.find(
      (e) => e.employeeId.toUpperCase() === manualEmpId.trim().toUpperCase()
    );
    if (!emp) {
      setAttendanceMessage({
        type: 'error',
        title: 'Employee Not Found',
        description: `No employee registered with ID "${manualEmpId}".`,
      });
      return;
    }

    if (!emp.isActive) {
      setAttendanceMessage({
        type: 'error',
        title: 'Deactivated Employee',
        description: `Employee ${emp.fullName} (${emp.employeeId}) is currently deactivated.`,
      });
      return;
    }

    const manualMatch: MatchResult = {
      matched: true,
      employee: emp,
      distance: 0,
      confidence: 100,
      threshold: settings.faceThreshold,
      message: 'Supervisor manual override verified',
    };

    const res = createAttendanceRecord(
      manualMatch,
      'manual_override',
      records,
      settings.timezone,
      `Supervisor override: ${manualReason}`
    );

    if (res.success && res.record) {
      onRecordAdded(res.record);
      setAttendanceMessage({
        type: 'success',
        title: 'Manual Attendance Approved',
        description: `Supervisor override logged for ${emp.fullName} (${emp.employeeId}) at ${res.record.checkInTimeFormatted}.`,
      });
      setManualEmpId('');
      setManualPin('');
    } else {
      setAttendanceMessage({
        type: 'duplicate',
        title: 'Duplicate Check-In Prevented',
        description: res.error || 'Attendance already exists for today.',
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Mode Selector Tabs */}
      <div className="neu-surface p-2 flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setActiveMode('camera');
              setAttendanceMessage(null);
            }}
            className={`px-4 py-2 text-xs font-semibold rounded-lg flex items-center gap-2 transition-all ${
              activeMode === 'camera' ? 'neu-tab-active' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Camera className="w-4 h-4" />
            <span>Live Webcam Terminal</span>
          </button>

          <button
            onClick={() => {
              setActiveMode('upload');
              setAttendanceMessage(null);
            }}
            className={`px-4 py-2 text-xs font-semibold rounded-lg flex items-center gap-2 transition-all ${
              activeMode === 'upload' ? 'neu-tab-active' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Upload className="w-4 h-4" />
            <span>Photo Upload</span>
          </button>

          <button
            onClick={() => {
              setActiveMode('manual');
              setAttendanceMessage(null);
            }}
            className={`px-4 py-2 text-xs font-semibold rounded-lg flex items-center gap-2 transition-all ${
              activeMode === 'manual' ? 'neu-tab-active' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <KeyRound className="w-4 h-4" />
            <span>Manual PIN Fallback</span>
          </button>
        </div>

        <div className="text-[11px] text-slate-500 font-medium px-3">
          Daily limit: <span className="font-bold text-slate-700">1 Check-in / Day</span> ({settings.timezone})
        </div>
      </div>

      {/* Main Scanner Card */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Live Video or Upload Zone */}
        <div className="lg:col-span-7 neu-surface p-6 space-y-4">
          {activeMode === 'camera' && (
            <div className="space-y-4">
              <div className="relative w-full aspect-4/3 rounded-xl overflow-hidden neu-inset flex items-center justify-center bg-slate-900">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className={`w-full h-full object-cover ${cameraActive ? 'block' : 'hidden'}`}
                />

                {/* Hidden canvas for capturing video frames */}
                <canvas ref={canvasRef} className="hidden" />

                {/* Camera Inactive / Error Placeholder */}
                {!cameraActive && (
                  <div className="p-6 text-center text-slate-300 space-y-3">
                    <Camera className="w-12 h-12 mx-auto text-slate-500" />
                    <div className="text-sm font-semibold">Webcam Terminal Standby</div>
                    <p className="text-xs text-slate-400 max-w-sm mx-auto">
                      {cameraError || 'Click "Start Camera" to initialize optical biometric stream.'}
                    </p>
                    <button
                      onClick={startCamera}
                      className="neu-btn-primary px-4 py-2 text-xs font-semibold"
                    >
                      Start Camera
                    </button>
                  </div>
                )}

                {/* Biometric Scanning Reticle Overlay */}
                {cameraActive && (
                  <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
                    <div className="w-56 h-64 border-2 border-blue-400/70 rounded-3xl relative">
                      {/* Corner Accents */}
                      <div className="absolute top-0 left-0 w-4 h-4 border-t-4 border-l-4 border-blue-500 -mt-1 -ml-1 rounded-tl-lg" />
                      <div className="absolute top-0 right-0 w-4 h-4 border-t-4 border-r-4 border-blue-500 -mt-1 -mr-1 rounded-tr-lg" />
                      <div className="absolute bottom-0 left-0 w-4 h-4 border-b-4 border-l-4 border-blue-500 -mb-1 -ml-1 rounded-bl-lg" />
                      <div className="absolute bottom-0 right-0 w-4 h-4 border-b-4 border-r-4 border-blue-500 -mb-1 -mr-1 rounded-br-lg" />

                      <div className="absolute top-2 inset-x-0 text-center">
                        <span className="text-[10px] uppercase tracking-wider font-semibold bg-black/60 text-white px-2 py-0.5 rounded-full">
                          Align Face
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3 justify-between">
                <div className="flex items-center gap-2">
                  {cameraActive ? (
                    <button
                      onClick={stopCamera}
                      className="neu-btn px-4 py-2 text-xs font-semibold text-slate-700"
                    >
                      Turn Off Camera
                    </button>
                  ) : (
                    <button
                      onClick={startCamera}
                      className="neu-btn px-4 py-2 text-xs font-semibold text-slate-700"
                    >
                      Start Camera
                    </button>
                  )}
                </div>

                <button
                  onClick={handleCaptureFromCamera}
                  disabled={!cameraActive || isProcessing}
                  className="neu-btn-primary px-6 py-2.5 text-xs font-bold flex items-center gap-2 disabled:opacity-50"
                >
                  {isProcessing ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Scanning Face...</span>
                    </>
                  ) : (
                    <>
                      <Camera className="w-4 h-4" />
                      <span>Capture Image</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {activeMode === 'upload' && (
            <div className="space-y-4">
              <div className="flex items-start gap-3 p-3.5 neu-surface-sm text-xs text-amber-800 bg-[#E8EEF5]">
                <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold">Photo Preview Only</div>
                  <div className="text-[11px] text-slate-600 mt-0.5 leading-relaxed">
                    This demo does not analyze the uploaded image. To try the attendance flow, select a synthetic demo profile below.
                  </div>
                </div>
              </div>

              {/* Upload Dropzone */}
              <label className="block w-full border-2 border-dashed border-[#CAD4E2] rounded-xl p-8 text-center cursor-pointer hover:border-blue-500 transition-colors bg-[#E4EAF3]">
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/jpg"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Upload className="w-10 h-10 mx-auto text-blue-600 mb-2" />
                <div className="text-sm font-bold text-slate-800">
                  Click to browse or drop an employee face photo
                </div>
                <div className="text-xs text-slate-500 mt-1">
                  Supports JPEG, JPG, and PNG (maximum 10MB). Image preview only; no face matching is performed.
                </div>
              </label>

              {capturedImage && (
                <div className="flex items-center gap-4 p-3 neu-surface-sm">
                  <img
                    src={capturedImage}
                    alt="Uploaded preview"
                    className="w-16 h-16 object-cover rounded-lg neu-inset"
                  />
                  <div>
                    <div className="text-xs font-bold text-slate-800">Image Loaded</div>
                    <div className="text-[11px] text-slate-500">Preview only; no biometric embedding was extracted</div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeMode === 'manual' && (
            <form onSubmit={handleManualCheckIn} className="space-y-4">
              <div className="flex items-start gap-3 p-3.5 neu-surface-sm text-xs text-blue-900 bg-[#E8EEF5]">
                <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold">Non-Biometric Accessibility Fallback</div>
                  <div className="text-[11px] text-slate-600 mt-0.5 leading-relaxed">
                    In compliance with labor and privacy laws, employees with temporary facial trauma, camera equipment failures, or religious exemptions may check in via supervisor authorization.
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Employee ID</label>
                  <input
                    type="text"
                    value={manualEmpId}
                    onChange={(e) => setManualEmpId(e.target.value.toUpperCase())}
                    placeholder="e.g. EMP-001"
                    className="w-full px-4 py-2.5 text-xs neu-inset-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Reason for Manual Override</label>
                  <select
                    value={manualReason}
                    onChange={(e) => setManualReason(e.target.value)}
                    className="w-full px-4 py-2.5 text-xs neu-inset-field bg-[#E4EAF3]"
                  >
                    <option value="Camera hardware unavailable">Camera hardware unavailable</option>
                    <option value="Temporary facial bandage or injury">Temporary facial bandage or injury</option>
                    <option value="Biometric exemption policy">Biometric exemption policy</option>
                    <option value="Lighting and glare issue">Lighting and glare issue</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Supervisor PIN (Default: 1234)
                  </label>
                  <input
                    type="password"
                    value={manualPin}
                    onChange={(e) => setManualPin(e.target.value)}
                    placeholder="Enter 4-digit PIN"
                    className="w-full px-4 py-2.5 text-xs neu-inset-field"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="neu-btn-primary w-full py-2.5 text-xs font-bold mt-2"
                >
                  Authorize Manual Check-In
                </button>
              </div>
            </form>
          )}

          {/* Synthetic demo matches do not analyze the captured image. */}
          <div className="pt-4 border-t border-[#D6E0EC]/70 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                Synthetic Demo Check-in
              </span>
              <span className="text-[10px] text-slate-500">Image is not analyzed</span>
            </div>
            <p className="text-[11px] text-slate-500">
              Select an employee to simulate a check-in with their synthetic demo profile. This does not verify the person in the photo.
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {employees.filter((employee) => employee.isActive && employee.faceEmbedding).map((employee) => (
                <button
                  key={employee.employeeId}
                  onClick={() => executeBiometricMatch(employee.employeeId)}
                  disabled={isProcessing}
                  className="neu-btn px-2.5 py-1.5 text-[11px] font-semibold text-slate-700 truncate disabled:opacity-50"
                  title={`Record a synthetic demo check-in for ${employee.fullName} (${employee.employeeId})`}
                >
                  <UserCheck className="inline w-3.5 h-3.5 mr-1" aria-hidden="true" />
                  {employee.fullName} ({employee.employeeId})
                </button>
              ))}
              <button
                onClick={() => executeBiometricMatch('STRANGER-999')}
                disabled={isProcessing}
                className="neu-btn px-2.5 py-1.5 text-[11px] font-semibold text-rose-700 truncate"
                title="Test an unmatched synthetic demo profile"
              >
                Unknown Demo Profile
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Verification Results & Real-Time Feedback */}
        <div className="lg:col-span-5 space-y-5">
          {/* Notification Banner */}
          {attendanceMessage && (
            <div
              className={`neu-surface p-5 border-l-4 transition-all ${
                attendanceMessage.type === 'success'
                  ? 'border-l-emerald-500'
                  : attendanceMessage.type === 'duplicate'
                  ? 'border-l-amber-500'
                  : attendanceMessage.type === 'info'
                  ? 'border-l-blue-500'
                  : 'border-l-rose-500'
              }`}
            >
              <div className="flex items-start gap-3">
                {attendanceMessage.type === 'success' ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                ) : attendanceMessage.type === 'duplicate' ? (
                  <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                ) : attendanceMessage.type === 'info' ? (
                  <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                ) : (
                  <XCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
                )}
                <div className="space-y-1">
                  <h4 className="text-xs font-bold text-slate-900 leading-tight">
                    {attendanceMessage.title}
                  </h4>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {attendanceMessage.description}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Biometric Diagnostic Card */}
          <div className="neu-surface p-6 space-y-4">
            <div className="border-b border-[#D6E0EC]/60 pb-3">
              <h3 className="text-sm font-bold text-slate-900">Synthetic Demo Match</h3>
              <p className="text-xs text-slate-500 mt-0.5">Demo vector metrics only; captured photos are not analyzed</p>
            </div>

            {matchResult ? (
              <div className="space-y-4">
                {/* Matched Employee Profile */}
                {matchResult.matched && matchResult.employee ? (
                  <div className="flex items-center gap-4 p-4 neu-surface-sm">
                    {matchResult.employee.avatarUrl ? (
                      <img
                        src={matchResult.employee.avatarUrl}
                        alt={matchResult.employee.fullName}
                        referrerPolicy="no-referrer"
                        className="w-14 h-14 rounded-full object-cover neu-inset"
                      />
                    ) : (
                      <div className="w-14 h-14 rounded-full neu-surface flex items-center justify-center font-bold text-blue-600 text-lg">
                        {matchResult.employee.fullName.charAt(0)}
                      </div>
                    )}
                    <div>
                      <div className="font-extrabold text-sm text-slate-900">
                        {matchResult.employee.fullName}
                      </div>
                      <div className="text-xs font-semibold text-blue-600 tabular-nums">
                        {matchResult.employee.employeeId}
                      </div>
                      <div className="text-[11px] text-slate-500">
                        {matchResult.employee.jobTitle} · {matchResult.employee.department}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="p-4 neu-inset text-center space-y-2">
                    <XCircle className="w-8 h-8 text-rose-500 mx-auto" />
                    <div className="text-xs font-bold text-slate-800">No Demo Profile Matched</div>
                    <div className="text-[11px] text-slate-500">
                      Calculated distance exceeds acceptable matching threshold.
                    </div>
                  </div>
                )}

                {/* Mathematical Metrics Grid */}
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-3 neu-inset">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Cosine Distance</span>
                    <span className="text-sm font-extrabold text-slate-900 tabular-nums">
                      {matchResult.distance}
                    </span>
                  </div>
                  <div className="p-3 neu-inset">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Confidence</span>
                    <span className="text-sm font-extrabold text-blue-600 tabular-nums">
                      {matchResult.confidence}%
                    </span>
                  </div>
                  <div className="p-3 neu-inset">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Max Threshold</span>
                    <span className="text-sm font-extrabold text-slate-700 tabular-nums">
                      {matchResult.threshold}
                    </span>
                  </div>
                  <div className="p-3 neu-inset">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Outcome</span>
                    <span
                      className={`text-sm font-extrabold uppercase ${
                        matchResult.matched ? 'text-emerald-600' : 'text-rose-600'
                      }`}
                    >
                      {matchResult.matched ? 'Demo Match' : 'No Match'}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-10 text-center text-xs text-slate-500 space-y-2">
                <Camera className="w-8 h-8 mx-auto text-slate-400" />
                <p>Capture a photo, then select a synthetic demo profile to try the check-in flow.</p>
              </div>
            )}
          </div>

          {/* Duplicate Prevention Status Info */}
          <div className="neu-surface p-5 text-xs text-slate-600 space-y-2">
            <div className="font-bold text-slate-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-blue-600" />
              <span>Enforced Business Invariants</span>
            </div>
            <ul className="list-disc list-inside text-[11px] space-y-1 text-slate-600">
              <li>Exactly one check-in per employee per calendar day.</li>
              <li>Calculated in organization timezone: <strong>{settings.timezone}</strong>.</li>
              <li>Only active registered employees are eligible for biometric matching.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
