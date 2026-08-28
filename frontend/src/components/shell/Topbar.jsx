import { useLocation } from 'react-router-dom';
import { Menu, Bell, Search } from 'lucide-react';

const PAGE_TITLES = {
  '/dashboard': 'Dashboard',
  '/medicine':  'Medicine',
  '/supplier':  'Supplier',
  '/purchase':  'Purchase Orders',
  '/inventory': 'Inventory',
  '/billing':   'Billing',
  '/sales':     'Sales',
  '/reports':   'Reports',
  '/settings':  'Settings',
  '/profile':   'My Profile',
};

export default function Topbar({ onMenuClick }) {
  const { pathname } = useLocation();
  const title = PAGE_TITLES[pathname] || 'MSMS';

  return (
    <header className="h-14 md:h-16 flex items-center gap-2 md:gap-4 px-3 md:px-6 bg-slate-900 border-b border-slate-800 flex-shrink-0">

      {/* Hamburger menu */}
      <button
        onClick={onMenuClick}
        className="text-slate-400 hover:text-white transition p-1.5 rounded-lg hover:bg-slate-800 flex-shrink-0"
        aria-label="Toggle menu"
      >
        <Menu size={20} />
      </button>

      {/* Page title */}
      <h1 className="text-white font-semibold text-sm md:text-base flex-1 truncate">{title}</h1>

      {/* Right side */}
      <div className="flex items-center gap-1 md:gap-2 flex-shrink-0">

        {/* Search button — text/kbd hidden on mobile */}
        <button className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg px-2 md:px-3 py-1.5 text-slate-400 hover:text-white text-sm transition">
          <Search size={14} />
          <span className="hidden md:inline text-xs">Search…</span>
          <kbd className="hidden lg:inline text-[10px] bg-slate-700 border border-slate-600 rounded px-1 py-0.5 text-slate-500 ml-1">⌘K</kbd>
        </button>

        {/* Notifications */}
        <button className="relative p-2 text-slate-400 hover:text-white transition rounded-lg hover:bg-slate-800">
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-blue-500" />
        </button>

        {/* Avatar */}
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold cursor-pointer hover:ring-2 hover:ring-blue-500 transition flex-shrink-0">
          A
        </div>
      </div>
    </header>
  );
}
