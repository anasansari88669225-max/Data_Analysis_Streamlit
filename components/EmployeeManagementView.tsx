import React, { useState } from 'react';
import {
  Search,
  Filter,
  UserCheck,
  UserX,
  Trash2,
  Edit,
  ShieldAlert,
  X,
  CheckCircle,
} from 'lucide-react';
import { Employee } from '../types';

interface EmployeeManagementViewProps {
  employees: Employee[];
  onToggleActive: (employeeId: string) => void;
  onDeleteEmployee: (employeeId: string) => void;
  onUpdateEmployee: (updated: Employee) => void;
}

export const EmployeeManagementView: React.FC<EmployeeManagementViewProps> = ({
  employees,
  onToggleActive,
  onDeleteEmployee,
  onUpdateEmployee,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState<'ALL' | 'ACTIVE' | 'INACTIVE'>('ALL');

  // Deletion Confirmation Modal State
  const [deleteTarget, setDeleteTarget] = useState<Employee | null>(null);

  // Edit Modal State
  const [editTarget, setEditTarget] = useState<Employee | null>(null);
  const [editFullName, setEditFullName] = useState('');
  const [editDept, setEditDept] = useState('');
  const [editJobTitle, setEditJobTitle] = useState('');
  const [editEmail, setEditEmail] = useState('');

  const departments = ['ALL', ...Array.from(new Set(employees.map((e) => e.department)))];

  const filtered = employees.filter((emp) => {
    const matchesSearch =
      emp.fullName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      emp.employeeId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      emp.jobTitle.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesDept = selectedDept === 'ALL' || emp.department === selectedDept;
    const matchesStatus =
      selectedStatus === 'ALL' ||
      (selectedStatus === 'ACTIVE' && emp.isActive) ||
      (selectedStatus === 'INACTIVE' && !emp.isActive);

    return matchesSearch && matchesDept && matchesStatus;
  });

  const openEditModal = (emp: Employee) => {
    setEditTarget(emp);
    setEditFullName(emp.fullName);
    setEditDept(emp.department);
    setEditJobTitle(emp.jobTitle);
    setEditEmail(emp.email || '');
  };

  const handleSaveEdit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!editTarget) return;

    const updated: Employee = {
      ...editTarget,
      fullName: editFullName.trim(),
      department: editDept,
      jobTitle: editJobTitle.trim(),
      email: editEmail.trim() || undefined,
      updatedAt: new Date().toISOString(),
    };

    onUpdateEmployee(updated);
    setEditTarget(null);
  };

  const handleConfirmDelete = () => {
    if (deleteTarget) {
      onDeleteEmployee(deleteTarget.employeeId);
      setDeleteTarget(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header and Filter Toolbar */}
      <div className="neu-surface p-5 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-900">Employee Directory</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Manage registered staff, biometric profiles, and access authorization status
            </p>
          </div>
          <div className="text-xs text-slate-500">
            Showing <strong className="text-slate-800">{filtered.length}</strong> of{' '}
            <strong className="text-slate-800">{employees.length}</strong> enrolled records
          </div>
        </div>

        {/* Filter Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* Search Box */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by ID, name, or title..."
              className="w-full pl-9 pr-4 py-2 text-xs neu-inset-field"
            />
          </div>

          {/* Department Filter */}
          <div className="relative">
            <Filter className="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
            <select
              value={selectedDept}
              onChange={(e) => setSelectedDept(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
            >
              {departments.map((dept) => (
                <option key={dept} value={dept}>
                  {dept === 'ALL' ? 'All Departments' : dept}
                </option>
              ))}
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value as 'ALL' | 'ACTIVE' | 'INACTIVE')}
              className="w-full px-4 py-2 text-xs neu-inset-field bg-[#E4EAF3] cursor-pointer"
            >
              <option value="ALL">All Statuses</option>
              <option value="ACTIVE">Active Only</option>
              <option value="INACTIVE">Deactivated Only</option>
            </select>
          </div>
        </div>
      </div>

      {/* Employee List Table */}
      <div className="neu-surface overflow-hidden">
        {filtered.length === 0 ? (
          <div className="p-10 text-center text-xs text-slate-500">
            No employees found matching the specified filters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-[11px] font-bold text-slate-500 border-b border-[#D6E0EC]/70 uppercase tracking-wider bg-[#E8EEF5]">
                  <th className="py-3 px-4">Employee</th>
                  <th className="py-3 px-4">Role & Unit</th>
                  <th className="py-3 px-4">Biometric Consent</th>
                  <th className="py-3 px-4">Registered Date</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#D6E0EC]/50 text-xs text-slate-700">
                {filtered.map((emp) => (
                  <tr key={emp.id} className="hover:bg-[#E2E8F1]/40 transition-colors">
                    {/* Employee Profile */}
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-3">
                        {emp.avatarUrl ? (
                          <img
                            src={emp.avatarUrl}
                            alt={emp.fullName}
                            referrerPolicy="no-referrer"
                            className="w-10 h-10 rounded-full object-cover neu-inset shrink-0"
                          />
                        ) : (
                          <div className="w-10 h-10 rounded-full neu-surface flex items-center justify-center font-bold text-blue-600 text-sm shrink-0">
                            {emp.fullName.charAt(0)}
                          </div>
                        )}
                        <div>
                          <div className="font-bold text-slate-900">{emp.fullName}</div>
                          <div className="text-[11px] text-blue-700 font-semibold tabular-nums">
                            {emp.employeeId}
                          </div>
                        </div>
                      </div>
                    </td>

                    {/* Department & Title */}
                    <td className="py-3.5 px-4">
                      <div className="font-medium text-slate-800">{emp.jobTitle}</div>
                      <div className="text-[11px] text-slate-500">{emp.department}</div>
                    </td>

                    {/* Biometric Consent */}
                    <td className="py-3.5 px-4">
                      <span className="inline-flex items-center gap-1 text-[11px] text-emerald-800 font-semibold">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Consented</span>
                      </span>
                    </td>

                    {/* Registration Date */}
                    <td className="py-3.5 px-4 tabular-nums text-slate-600">
                      {emp.createdAt ? emp.createdAt.split('T')[0] : '2026-01-15'}
                    </td>

                    {/* Status Badge */}
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-md text-[10px] font-bold uppercase ${
                          emp.isActive
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-rose-100 text-rose-800'
                        }`}
                      >
                        {emp.isActive ? 'Active' : 'Deactivated'}
                      </span>
                    </td>

                    {/* Actions */}
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        {/* Edit Button */}
                        <button
                          onClick={() => openEditModal(emp)}
                          className="p-1.5 neu-btn text-slate-600 hover:text-blue-600"
                          title="Edit Details"
                          aria-label={`Edit ${emp.fullName}`}
                        >
                          <Edit className="w-3.5 h-3.5" />
                        </button>

                        {/* Deactivate/Activate Toggle */}
                        <button
                          onClick={() => onToggleActive(emp.employeeId)}
                          className={`p-1.5 neu-btn ${
                            emp.isActive
                              ? 'text-amber-600 hover:text-amber-700'
                              : 'text-emerald-600 hover:text-emerald-700'
                          }`}
                          title={emp.isActive ? 'Deactivate Employee' : 'Activate Employee'}
                          aria-label={emp.isActive ? `Deactivate ${emp.fullName}` : `Activate ${emp.fullName}`}
                        >
                          {emp.isActive ? (
                            <UserX className="w-3.5 h-3.5" />
                          ) : (
                            <UserCheck className="w-3.5 h-3.5" />
                          )}
                        </button>

                        {/* Delete Button */}
                        <button
                          onClick={() => setDeleteTarget(emp)}
                          className="p-1.5 neu-btn text-slate-500 hover:text-rose-600"
                          title="Delete with Biometric Purge"
                          aria-label={`Delete ${emp.fullName}`}
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Edit Employee Modal */}
      {editTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="w-full max-w-md neu-surface p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-[#D6E0EC]/70 pb-3">
              <h3 className="text-sm font-bold text-slate-900">
                Edit Employee ({editTarget.employeeId})
              </h3>
              <button
                onClick={() => setEditTarget(null)}
                className="p-1 text-slate-400 hover:text-slate-700"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveEdit} className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                <input
                  type="text"
                  value={editFullName}
                  onChange={(e) => setEditFullName(e.target.value)}
                  className="w-full px-3 py-2 text-xs neu-inset-field"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Department</label>
                <select
                  value={editDept}
                  onChange={(e) => setEditDept(e.target.value)}
                  className="w-full px-3 py-2 text-xs neu-inset-field bg-[#E4EAF3]"
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

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Job Title</label>
                <input
                  type="text"
                  value={editJobTitle}
                  onChange={(e) => setEditJobTitle(e.target.value)}
                  className="w-full px-3 py-2 text-xs neu-inset-field"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Email</label>
                <input
                  type="email"
                  value={editEmail}
                  onChange={(e) => setEditEmail(e.target.value)}
                  className="w-full px-3 py-2 text-xs neu-inset-field"
                />
              </div>

              <div className="pt-3 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setEditTarget(null)}
                  className="neu-btn px-4 py-2 text-xs font-semibold text-slate-600"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="neu-btn-primary px-5 py-2 text-xs font-bold"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete / Biometric Purge Confirmation Modal */}
      {deleteTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="w-full max-w-md neu-surface p-6 space-y-4">
            <div className="flex items-center gap-3 text-rose-600">
              <ShieldAlert className="w-6 h-6 shrink-0" />
              <h3 className="text-sm font-bold text-slate-900">
                Confirm Biometric Data Purge
              </h3>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              Are you sure you want to permanently delete{' '}
              <strong>{deleteTarget.fullName}</strong> ({deleteTarget.employeeId})?
            </p>

            <div className="p-3 neu-inset text-[11px] text-slate-600 rounded-lg space-y-1">
              <div className="font-bold text-slate-800">Biometric Regulation Notice:</div>
              <div>
                This action irreversibly destroys all stored facial recognition vectors, embeddings, and enrollment photographs from the system in compliance with GDPR Article 17 (Right to Erasure).
              </div>
            </div>

            <div className="pt-3 flex items-center justify-end gap-2">
              <button
                onClick={() => setDeleteTarget(null)}
                className="neu-btn px-4 py-2 text-xs font-semibold text-slate-600"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                className="neu-btn px-5 py-2 text-xs font-bold text-white bg-rose-600 hover:bg-rose-700 rounded-lg shadow-md"
              >
                Permanently Delete & Purge Vectors
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
