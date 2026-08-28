import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  Activity, LayoutDashboard, Pill, Truck, ShoppingCart,
  Package, Receipt, BarChart2, FileText, Settings,
  LogOut, ChevronLeft, ChevronRight, User, X
} from 'lucide-react';

const NAV_ITEMS = [
  { label: 'Dashboard',  path: '/dashboard', icon: LayoutDashboard },
  { label: 'Medicine',   path: '/medicine',  icon: Pill },
  { label: 'Supplier',   path: '/supplier',  icon: Truck },
  { label: 'Purchase',   path: '/purchase',  icon: ShoppingCart },
  { label: 'Inventory',  path: '/inventory', icon: Package },
  { label: 'Billing',    path: '/billing',   icon: Receipt },
  { label: 'Sales',      path: '/sales',     icon: BarChart2 },
  { label: 'Reports',    path: '/reports',   icon: FileText },
];

const BOTTOM_ITEMS = [
  { label: 'Profile',  path: '/profile',  icon: User },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export default function Sidebar({ open, onToggle, isMobile, onClose }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  // Mobile mein hamesha full width drawer, desktop mein collapsible
  const sidebarWidth = isMobile ? 'w-64' : (open ? 'w-60' : 'w-16');

  return (
    <aside
      className={`
        relative flex flex-col h-full bg-slate-900 border-r border-slate-800
        transition-all duration-300 ease-in-out
        ${sidebarWidth}
      `}
    >
      {/* Logo + Mobile close button */}
      <div className="flex items-center h-16 px-4 border-b border-slate-800 gap-3 overflow-hidden flex-shrink-0">
        <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow shadow-blue-600/40">
          <Activity size={16} className="text-white" />
        </div>
        {(open || isMobile) && (
          <div className="min-w-0 flex-1">
            <span className="text-white font-bold text-sm tracking-tight block">MSMS</span>
            <span className="text-slate-500 text-[10px] block leading-tight">Medical Store Mgmt.</span>
          </div>
        )}
        {/* Mobile close button */}
        {isMobile && (
          <button
            onClick={onClose}
            className="flex-shrink-0 p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition"
          >
            <X size={16} />
          </button>
        )}
      </div>

      {/* Desktop toggle button */}
      {!isMobile && (
        <button
          onClick={onToggle}
          className="absolute -right-3 top-[4.5rem] z-10 w-6 h-6 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400 hover:text-white hover:bg-slate-700 transition shadow-md"
        >
          {open ? <ChevronLeft size={12} /> : <ChevronRight size={12} />}
        </button>
      )}

      {/* Main nav */}
      <nav className="flex-1 py-4 px-2 space-y-0.5 overflow-y-auto overflow-x-hidden">
        {(open || isMobile) && (
          <p className="text-slate-600 text-[10px] font-semibold uppercase tracking-widest px-3 mb-2">
            Main Menu
          </p>
        )}
        {NAV_ITEMS.map(({ label, path, icon: Icon }) => (
          <NavLink
            key={path}
            to={path}
            title={(!open && !isMobile) ? label : undefined}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all group
               ${isActive
                ? 'bg-blue-600/15 text-blue-400 border border-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-800 border border-transparent'}`
            }
          >
            {({ isActive }) => (
              <>
                <Icon
                  size={isMobile ? 18 : 17}
                  className={`flex-shrink-0 ${isActive ? 'text-blue-400' : 'text-slate-500 group-hover:text-slate-300'}`}
                />
                {(open || isMobile) && <span className="truncate">{label}</span>}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Bottom nav */}
      <div className="px-2 pb-2 space-y-0.5 border-t border-slate-800 pt-2 flex-shrink-0">
        {BOTTOM_ITEMS.map(({ label, path, icon: Icon }) => (
          <NavLink
            key={path}
            to={path}
            title={(!open && !isMobile) ? label : undefined}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all group
               ${isActive
                ? 'bg-blue-600/15 text-blue-400 border border-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-800 border border-transparent'}`
            }
          >
            {({ isActive }) => (
              <>
                <Icon size={17} className={`flex-shrink-0 ${isActive ? 'text-blue-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
                {(open || isMobile) && <span className="truncate">{label}</span>}
              </>
            )}
          </NavLink>
        ))}

        {/* User + logout */}
        <div className="flex items-center gap-3 px-3 py-2 mt-1 rounded-lg bg-slate-800/50 border border-slate-700/50 overflow-hidden">
          <div className="flex-shrink-0 w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold">
            {(user?.username || user?.name || 'A')[0].toUpperCase()}
          </div>
          {(open || isMobile) && (
            <>
              <div className="flex-1 min-w-0">
                <p className="text-white text-xs font-semibold truncate">
                  {user?.username || user?.name || 'Admin'}
                </p>
                <p className="text-slate-500 text-[10px] truncate">
                  {user?.is_staff ? 'Administrator' : 'Staff'}
                </p>
              </div>
              <button
                onClick={handleLogout}
                title="Logout"
                className="text-slate-500 hover:text-red-400 transition flex-shrink-0 p-1"
              >
                <LogOut size={15} />
              </button>
            </>
          )}
          {/* Collapsed state logout — desktop only */}
          {!open && !isMobile && (
            <button
              onClick={handleLogout}
              title="Logout"
              className="text-slate-500 hover:text-red-400 transition"
            >
              <LogOut size={15} />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
