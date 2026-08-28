import { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const location = useLocation();

  // Detect mobile vs desktop
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      // Desktop pe default open, mobile pe default closed
      if (!mobile) setSidebarOpen(true);
      else setSidebarOpen(false);
    };
    handleResize(); // initial run
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Mobile pe route change hone par drawer band karo
  useEffect(() => {
    if (isMobile) setSidebarOpen(false);
  }, [location.pathname, isMobile]);

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden">

      {/* Mobile overlay — sidebar ke peeche dark background */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/60 backdrop-blur-sm"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
          ${isMobile
            ? `fixed inset-y-0 left-0 z-30 transition-transform duration-300 ease-in-out
               ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`
            : 'relative flex-shrink-0'
          }
        `}
      >
        <Sidebar
          open={isMobile ? true : sidebarOpen}
          onToggle={() => setSidebarOpen(o => !o)}
          isMobile={isMobile}
          onClose={() => setSidebarOpen(false)}
        />
      </div>

      {/* Main content area */}
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        <Topbar onMenuClick={() => setSidebarOpen(o => !o)} />
        <main className="flex-1 overflow-y-auto bg-slate-950 p-3 sm:p-4 md:p-6">
          <Outlet />
        </main>
      </div>

    </div>
  );
}
