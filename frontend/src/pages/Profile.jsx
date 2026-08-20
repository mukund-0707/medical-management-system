import { useAuth } from '../context/AuthContext';
import { User, Mail, Shield, Clock, Edit2, Save, Key } from 'lucide-react';

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h2 className="text-white text-xl font-bold">My Profile</h2>
        <p className="text-slate-400 text-sm mt-0.5">Manage your account information and security</p>
      </div>

      {/* Profile card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-start gap-5">
          <div className="relative flex-shrink-0">
            <div className="w-20 h-20 rounded-2xl bg-blue-600 flex items-center justify-center text-white text-3xl font-bold shadow-lg shadow-blue-600/30">
              A
            </div>
            <button className="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition">
              <Edit2 size={12} />
            </button>
          </div>
          <div className="flex-1">
            <h3 className="text-white text-lg font-bold">{user?.name || 'Admin User'}</h3>
            <p className="text-blue-400 text-sm font-medium">{user?.role || 'Administrator'}</p>
            <div className="flex items-center gap-4 mt-3">
              <span className="flex items-center gap-1.5 text-slate-400 text-xs">
                <Clock size={12} /> Last login: Today, 11:06 AM
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400 text-xs">
                <Shield size={12} /> Active session
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Account info */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-800">
          <User size={16} className="text-slate-400" />
          <h3 className="text-white font-semibold text-sm">Account Information</h3>
        </div>
        <div className="p-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-400 text-xs mb-1.5 font-medium">Full Name</label>
              <input
                type="text"
                defaultValue="Admin User"
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-xs mb-1.5 font-medium">Username</label>
              <input
                type="text"
                defaultValue="admin"
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-xs mb-1.5 font-medium">Email Address</label>
              <input
                type="email"
                defaultValue="admin@msms.local"
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-xs mb-1.5 font-medium">Role</label>
              <input
                type="text"
                defaultValue="Administrator"
                readOnly
                className="w-full bg-slate-800/50 border border-slate-700 text-slate-400 rounded-xl px-4 py-2.5 text-sm cursor-not-allowed"
              />
            </div>
          </div>
          <div className="flex justify-end pt-2">
            <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-5 py-2.5 text-sm font-medium transition shadow-lg shadow-blue-600/20">
              <Save size={14} /> Save Changes
            </button>
          </div>
        </div>
      </div>

      {/* Change password */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-800">
          <Key size={16} className="text-slate-400" />
          <h3 className="text-white font-semibold text-sm">Change Password</h3>
        </div>
        <div className="p-6 space-y-4">
          {['Current Password', 'New Password', 'Confirm New Password'].map(label => (
            <div key={label}>
              <label className="block text-slate-400 text-xs mb-1.5 font-medium">{label}</label>
              <input
                type="password"
                placeholder="••••••••"
                className="w-full bg-slate-800 border border-slate-700 text-white placeholder-slate-600 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}
          <div className="flex justify-end pt-2">
            <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-5 py-2.5 text-sm font-medium transition">
              <Key size={14} /> Update Password
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
