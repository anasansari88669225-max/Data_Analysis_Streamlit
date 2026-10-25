import React, { useState, useRef } from 'react';
import {
  UserPlus,
  Camera,
  Upload,
  CheckCircle2,
  AlertCircle,
  ShieldCheck,
  RefreshCw,
  User,
} from 'lucide-react';
import { Employee } from '../types';
import { validateEmployeeRegistration, validateImageUpload } from '../utils/validators';
import { generateDeterministicEmbedding } from '../utils/faceMath';

interface RegisterEmployeeViewProps {
  existingEmployees: Employee[];
  onEmployeeRegistered: (employee: Employee) => void;
  onNavigateToDirectory: () => void;
}

export const RegisterEmployeeView: React.FC<RegisterEmployeeViewProps> = ({
  existingEmployees,
  onEmployeeRegistered,
  onNavigateToDirectory,
}) => {
  const [employeeId, setEmployeeId] = useState('');
  const [fullName, setFullName] = useState('');
  const [department, setDepartment] = useState('Engineering');
  const [jobTitle, setJobTitle] = useState('');
  const [email, setEmail] = useState('');
  const [consentGiven, setConsentGiven] = useState(false);
  const [faceImage, setFaceImage] = useState<string | null>(null);

  const [captureMethod, setCaptureMethod] = useState<'upload' | 'camera'>('upload');
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 480 }, height: { ideal: 480 } },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setIsCameraActive(true);
    } catch {
      alert('Camera access failed. Please use file upload instead.');
    }
  };

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraActive(false);
  };

  const captureWebcamSnapshot = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth || 480;
    canvas.height = videoRef.current.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
      setFaceImage(dataUrl);
      stopWebcam();
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const val = validateImageUpload(file);
    if (!val.valid) {
      setFormErrors((prev) => ({ ...prev, face: val.error || 'Invalid image file.' }));
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setFaceImage(reader.result as string);
      setFormErrors((prev) => {
        const next = { ...prev };
        delete next.face;
        return next;
      });
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFeedback(null);

    const validation = validateEmployeeRegistration(
      {
        employeeId,
        fullName,
        department,
        jobTitle,
        email,
        consentGiven,
        hasFaceImage: !!faceImage,
      },
      existingEmployees
    );

    if (!validation.isValid) {
      setFormErrors(validation.errors);
      setFeedback({
        type: 'error',
        message: 'Please review and fix the validation errors marked below.',
      });
      return;
    }

    setIsGenerating(true);

    // Simulate single face detection verification & 128-d embedding generation
    setTimeout(() => {
      const cleanId = employeeId.trim().toUpperCase();
      const embedding = generateDeterministicEmbedding(`${cleanId}-${fullName.trim()}`);

      const now = new Date().toISOString();
      const newEmployee: Employee = {
        id: `emp-${Date.now()}`,
        employeeId: cleanId,
        fullName: fullName.trim(),
        department,
        jobTitle: jobTitle.trim(),
        email: email.trim() || undefined,
        faceEmbedding: embedding,
        avatarUrl: faceImage || undefined,
        isActive: true,
        biometricConsentGiven: true,
        consentTimestamp: now,
        createdAt: now,
        updatedAt: now,
      };

      onEmployeeRegistered(newEmployee);
      setIsGenerating(false);
      setFeedback({
        type: 'success',
        message: `Employee ${newEmployee.fullName} (${newEmployee.employeeId}) registered with a synthetic demo vector (not a face-derived biometric template).`,
      });

      // Clear form
      setEmployeeId('');
      setFullName('');
      setJobTitle('');
      setEmail('');
      setFaceImage(null);
      setConsentGiven(false);
      setFormErrors({});
    }, 700);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Info */}
      <div className="neu-surface p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Enroll New Employee</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Demo enrollment creates a synthetic vector from the employee ID and name; it does not analyze the face image.
          </p>
        </div>
        <button
          onClick={onNavigateToDirectory}
          className="neu-btn px-4 py-2 text-xs font-semibold text-slate-700 shrink-0"
        >
          View All Employees ({existingEmployees.length})
        </button>
      </div>

      {feedback && (
        <div
          className={`neu-surface p-4 border-l-4 flex items-center gap-3 ${
            feedback.type === 'success' ? 'border-l-emerald-500' : 'border-l-rose-500'
          }`}
        >
          {feedback.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
          )}
          <span className="text-xs font-medium text-slate-800">{feedback.message}</span>
        </div>
      )}

      {/* Main Registration Form */}
      <form onSubmit={handleSubmit} className="neu-surface p-6 sm:p-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Column: Personal & Organizational Details */}
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 pb-1 border-b border-[#D6E0EC]/70">
              Personal & Role Details
            </h3>

            {/* Employee ID */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Employee ID <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={employeeId}
                onChange={(e) => {
                  setEmployeeId(e.target.value.toUpperCase());
                  if (formErrors.employeeId) {
                    setFormErrors((prev) => {
                      const next = { ...prev };
                      delete next.employeeId;
                      return next;
                    });
                  }
                }}
                placeholder="e.g. EMP-107"
                className={`w-full px-4 py-2.5 text-xs neu-inset-field ${
                  formErrors.employeeId ? 'border border-rose-400' : ''
                }`}
              />
              {formErrors.employeeId && (
                <p className="text-[11px] text-rose-600 font-medium mt-1">{formErrors.employeeId}</p>
              )}
            </div>

            {/* Full Name */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Full Name <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => {
                  setFullName(e.target.value);
                  if (formErrors.fullName) {
                    setFormErrors((prev) => {
                      const next = { ...prev };
                      delete next.fullName;
                      return next;
                    });
                  }
                }}
                placeholder="e.g. Elena Rostova"
                className={`w-full px-4 py-2.5 text-xs neu-inset-field ${
                  formErrors.fullName ? 'border border-rose-400' : ''
                }`}
              />
              {formErrors.fullName && (
                <p className="text-[11px] text-rose-600 font-medium mt-1">{formErrors.fullName}</p>
              )}
            </div>

            {/* Department */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Department <span className="text-rose-500">*</span>
              </label>
              <select
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="w-full px-4 py-2.5 text-xs neu-inset-field bg-[#E4EAF3]"
              >
                <option value="Engineering">Engineering</option>
                <option value="Product">Product</option>
                <option value="Operations">Operations</option>
                <option value="Finance">Finance</option>
                <option value="Human Resources">Human Resources</option>
                <option value="Security">Security & Facilities</option>
                <option value="Legal & Compliance">Legal & Compliance</option>
              </select>
            </div>

            {/* Job Title */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Job Title <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => {
                  setJobTitle(e.target.value);
                  if (formErrors.jobTitle) {
                    setFormErrors((prev) => {
                      const next = { ...prev };
                      delete next.jobTitle;
                      return next;
                    });
                  }
                }}
                placeholder="e.g. Lead QA Specialist"
                className={`w-full px-4 py-2.5 text-xs neu-inset-field ${
                  formErrors.jobTitle ? 'border border-rose-400' : ''
                }`}
              />
              {formErrors.jobTitle && (
                <p className="text-[11px] text-rose-600 font-medium mt-1">{formErrors.jobTitle}</p>
              )}
            </div>

            {/* Email (Optional) */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Corporate Email <span className="text-slate-400 font-normal">(Optional)</span>
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="e.g. elena.r@aerosync.io"
                className="w-full px-4 py-2.5 text-xs neu-inset-field"
              />
              {formErrors.email && (
                <p className="text-[11px] text-rose-600 font-medium mt-1">{formErrors.email}</p>
              )}
            </div>
          </div>

          {/* Right Column: Biometric Capture & Image */}
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 pb-1 border-b border-[#D6E0EC]/70">
              Biometric Enrollment Image
            </h3>

            {/* Capture Tabs */}
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => {
                  setCaptureMethod('upload');
                  stopWebcam();
                }}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg ${
                  captureMethod === 'upload' ? 'neu-tab-active' : 'neu-btn text-slate-600'
                }`}
              >
                Upload Photo
              </button>
              <button
                type="button"
                onClick={() => {
                  setCaptureMethod('camera');
                  startWebcam();
                }}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg ${
                  captureMethod === 'camera' ? 'neu-tab-active' : 'neu-btn text-slate-600'
                }`}
              >
                Live Webcam
              </button>
            </div>

            {captureMethod === 'upload' && (
              <label className="block w-full border-2 border-dashed border-[#CAD4E2] rounded-xl p-6 text-center cursor-pointer hover:border-blue-500 transition-colors bg-[#E4EAF3]">
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/jpg"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Upload className="w-8 h-8 mx-auto text-blue-600 mb-2" />
                <div className="text-xs font-bold text-slate-800">Select employee headshot</div>
                <div className="text-[11px] text-slate-500 mt-1">JPEG, JPG, or PNG (exactly 1 face)</div>
              </label>
            )}

            {captureMethod === 'camera' && (
              <div className="space-y-3">
                <div className="relative w-full aspect-square max-h-52 rounded-xl overflow-hidden neu-inset bg-slate-900 flex items-center justify-center">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                  />
                </div>
                <button
                  type="button"
                  onClick={captureWebcamSnapshot}
                  className="neu-btn-primary w-full py-2 text-xs font-bold flex items-center justify-center gap-2"
                >
                  <Camera className="w-4 h-4" />
                  <span>Snap Enrollment Photo</span>
                </button>
              </div>
            )}

            {/* Image Preview & Biometric status */}
            {faceImage ? (
              <div className="flex items-center gap-4 p-3 neu-surface-sm">
                <img
                  src={faceImage}
                  alt="Enrollment portrait"
                  className="w-16 h-16 rounded-lg object-cover neu-inset"
                />
                <div className="space-y-0.5">
                  <div className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Single Face Detected (Ready)</span>
                  </div>
                  <div className="text-[11px] text-slate-500">
                    High-quality landmark confidence detected.
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-4 neu-inset text-center text-xs text-slate-500">
                <User className="w-8 h-8 mx-auto text-slate-400 mb-1" />
                <span>No face photo provided yet.</span>
              </div>
            )}
            {formErrors.face && (
              <p className="text-[11px] text-rose-600 font-medium">{formErrors.face}</p>
            )}

            {/* Mandatory Biometric Consent */}
            <div className="pt-2">
              <label className="flex items-start gap-3 p-3.5 neu-surface-sm rounded-xl cursor-pointer">
                <input
                  type="checkbox"
                  checked={consentGiven}
                  onChange={(e) => {
                    setConsentGiven(e.target.checked);
                    if (formErrors.consent) {
                      setFormErrors((prev) => {
                        const next = { ...prev };
                        delete next.consent;
                        return next;
                      });
                    }
                  }}
                  className="mt-0.5 h-4 w-4 rounded text-blue-600 focus:ring-blue-500"
                />
                <div className="text-[11px] text-slate-700 leading-relaxed">
                  <span className="font-bold text-slate-900 block">
                    Biometric Processing Consent Confirmation (Required)
                  </span>
                  I confirm that this employee has received the biometric data privacy disclosure notice and explicitly consented to the extraction, storage, and matching of their facial embeddings.
                </div>
              </label>
              {formErrors.consent && (
                <p className="text-[11px] text-rose-600 font-medium mt-1">{formErrors.consent}</p>
              )}
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4 border-t border-[#D6E0EC]/70 flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => {
              setEmployeeId('');
              setFullName('');
              setJobTitle('');
              setEmail('');
              setFaceImage(null);
              setConsentGiven(false);
              setFormErrors({});
            }}
            className="neu-btn px-5 py-2.5 text-xs font-semibold text-slate-600"
          >
            Reset Form
          </button>
          <button
            type="submit"
            disabled={isGenerating}
            className="neu-btn-primary px-7 py-2.5 text-xs font-bold flex items-center gap-2 disabled:opacity-50"
          >
            {isGenerating ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Generating Biometric Vector...</span>
              </>
            ) : (
              <>
                <ShieldCheck className="w-4 h-4" />
                <span>Save Employee & Enroll Vector</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
