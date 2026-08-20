import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Landing page components
import { useScroll, useSpring, motion } from 'framer-motion';
import Navbar      from './components/Navbar';
import Hero        from './components/Hero';
import Marquee     from './components/Marquee';
import Features    from './components/Features';
import HowItWorks  from './components/HowItWorks';
import Stats       from './components/Stats';
import CtaFooter   from './components/CtaFooter';

// MSMS App
import LoginPage from './pages/LoginPage';
import AppShell  from './components/shell/AppShell';
import Dashboard from './pages/Dashboard';
import Medicine  from './pages/Medicine';
import Supplier  from './pages/Supplier';
import Purchase  from './pages/Purchase';
import Inventory from './pages/Inventory';
import Billing   from './pages/Billing';
import Sales     from './pages/Sales';
import Reports   from './pages/Reports';
import Settings  from './pages/Settings';
import Profile   from './pages/Profile';

function LandingPage() {
  const { scrollYProgress } = useScroll();
  const progress = useSpring(scrollYProgress, { stiffness: 120, damping: 26, restDelta: 0.001 });

  return (
    <div className="relative min-h-screen bg-ink-950 font-inter text-white">
      <motion.div
        style={{ scaleX: progress }}
        className="fixed inset-x-0 top-0 z-[70] h-[2px] origin-left bg-gradient-to-r from-gold-300 via-gold-400 to-gold-600"
      />
      <div className="grain" aria-hidden="true" />
      <Navbar />
      <main>
        <Hero />
        <Marquee />
        <Features />
        <HowItWorks />
        <Stats />
        <CtaFooter />
      </main>
    </div>
  );
}

function PrivateRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

function PublicOnlyRoute({ children }) {
  const { user } = useAuth();
  return user ? <Navigate to="/dashboard" replace /> : children;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Landing page — always accessible */}
          <Route path="/" element={<LandingPage />} />

          {/* Login — only if not logged in */}
          <Route path="/login" element={<PublicOnlyRoute><LoginPage /></PublicOnlyRoute>} />

          {/* MSMS App — protected */}
          <Route
            path="/"
            element={<PrivateRoute><AppShell /></PrivateRoute>}
          >
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="medicine"  element={<Medicine />} />
            <Route path="supplier"  element={<Supplier />} />
            <Route path="purchase"  element={<Purchase />} />
            <Route path="inventory" element={<Inventory />} />
            <Route path="billing"   element={<Billing />} />
            <Route path="sales"     element={<Sales />} />
            <Route path="reports"   element={<Reports />} />
            <Route path="settings"  element={<Settings />} />
            <Route path="profile"   element={<Profile />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
