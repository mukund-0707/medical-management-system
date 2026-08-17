import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X } from 'lucide-react';

const navLinks = ['Features', 'Workflow', 'Stats', 'Contact'];

// Inline SVG logo matching AB Groups gold+black mark
function ABLogo({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Background circle */}
      <circle cx="32" cy="32" r="32" fill="#0a0902" />
      {/* Gold A */}
      <path d="M10 50 L22 18 L28 18 L40 50 H34 L31 42 H19 L16 50 Z M21 36 H29 L25 24 Z"
        fill="url(#goldGrad)" />
      {/* Gold B */}
      <path d="M42 18 H52 C56 18 59 21 59 25 C59 27.5 57.5 29.5 55.5 30.5 C58 31.5 60 34 60 37 C60 41.5 56.5 45 52 45 H42 Z M47 28 H51 C52.7 28 54 26.7 54 25 C54 23.3 52.7 22 51 22 H47 Z M47 41 H52 C54 41 55.5 39.5 55.5 37.5 C55.5 35.5 54 34 52 34 H47 Z"
        fill="url(#goldGrad)" />
      <defs>
        <linearGradient id="goldGrad" x1="0" y1="0" x2="0" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0%"   stopColor="#f4c040" />
          <stop offset="50%"  stopColor="#d4a017" />
          <stop offset="100%" stopColor="#9a6f08" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled]     = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? 'hidden' : '';
  }, [mobileOpen]);

  const scrollTo = (id) => {
    setMobileOpen(false);
    const el = document.getElementById(id.toLowerCase());
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      {/* ── Navbar ── */}
      <motion.nav
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
          scrolled
            ? 'bg-[#0a0902]/90 backdrop-blur-xl border-b border-gold-600/20 shadow-lg shadow-black/30'
            : 'bg-transparent'
        }`}
      >
        <div className="max-w-7xl mx-auto px-5 sm:px-8 py-4 flex items-center justify-between">

          {/* Logo */}
          <a href="#" className="flex items-center gap-3 group" aria-label="Aai Bhavani Group">
            <div className="group-hover:scale-105 transition-transform duration-200">
              <ABLogo size={36} />
            </div>
            <div className="flex flex-col leading-tight">
              <span className="text-[15px] font-extrabold tracking-wider uppercase text-white">
                Aai <span className="shimmer-text">Bhavani</span>
              </span>
              <span className="text-[9px] tracking-[0.25em] uppercase text-gold-500/70 font-medium">
                Group
              </span>
            </div>
          </a>

          {/* Desktop nav links */}
          <ul className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <li key={link}>
                <button
                  onClick={() => scrollTo(link)}
                  className="text-sm font-medium text-white/60 hover:text-gold-400 transition-colors duration-200 relative after:absolute after:bottom-[-3px] after:left-0 after:h-[1.5px] after:w-0 after:bg-gold-500 after:rounded-full after:transition-all hover:after:w-full"
                >
                  {link}
                </button>
              </li>
            ))}
          </ul>

          {/* Desktop CTAs */}
          <div className="hidden md:flex items-center gap-3">
            <button className="text-sm font-medium text-white/50 hover:text-white transition-colors px-4 py-2">
              Sign In
            </button>
            <motion.button
              whileHover={{ scale: 1.04, boxShadow: '0 6px 28px rgba(212,160,23,0.4)' }}
              whileTap={{ scale: 0.96 }}
              className="text-sm font-semibold rounded-full px-5 py-2.5 transition-all"
              style={{
                background: 'linear-gradient(135deg, #d4a017, #b8860b)',
                color: '#0a0902',
                boxShadow: '0 4px 18px rgba(212,160,23,0.3)',
              }}
            >
              Request Demo
            </motion.button>
          </div>

          {/* Mobile hamburger */}
          <motion.button
            onClick={() => setMobileOpen((v) => !v)}
            whileTap={{ scale: 0.9 }}
            className="md:hidden w-10 h-10 flex items-center justify-center rounded-lg text-gold-400 hover:bg-gold-900/20 transition-colors z-50"
            aria-label="Toggle menu"
          >
            <AnimatePresence mode="wait" initial={false}>
              {mobileOpen ? (
                <motion.span key="close"
                  initial={{ rotate: -90, opacity: 0, scale: 0.8 }}
                  animate={{ rotate: 0,   opacity: 1, scale: 1 }}
                  exit={{   rotate:  90, opacity: 0, scale: 0.8 }}
                  transition={{ duration: 0.2 }}
                >
                  <X size={22} />
                </motion.span>
              ) : (
                <motion.span key="menu"
                  initial={{ rotate:  90, opacity: 0, scale: 0.8 }}
                  animate={{ rotate: 0,   opacity: 1, scale: 1 }}
                  exit={{   rotate: -90, opacity: 0, scale: 0.8 }}
                  transition={{ duration: 0.2 }}
                >
                  <Menu size={22} />
                </motion.span>
              )}
            </AnimatePresence>
          </motion.button>
        </div>
      </motion.nav>

      {/* ── Mobile Menu ── */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              key="backdrop"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm"
              onClick={() => setMobileOpen(false)}
            />
            <motion.div
              key="sheet"
              initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="fixed right-0 top-0 z-40 h-[100dvh] w-[min(85vw,340px)] flex flex-col shadow-2xl"
              style={{ background: '#111009', borderLeft: '1px solid rgba(212,160,23,0.15)' }}
            >
              {/* Sheet header */}
              <div className="flex items-center gap-3 px-6 py-5 border-b border-gold-800/30">
                <ABLogo size={30} />
                <div className="flex flex-col leading-tight">
                  <span className="text-sm font-extrabold tracking-wider uppercase text-white">
                    Aai <span className="text-gold-400">Bhavani</span>
                  </span>
                  <span className="text-[9px] tracking-[0.25em] uppercase text-gold-600/60">Group</span>
                </div>
              </div>

              {/* Sheet links */}
              <div className="flex flex-col justify-center flex-1 px-6 gap-1">
                {navLinks.map((link, i) => (
                  <motion.button
                    key={link}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 + i * 0.06, duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
                    onClick={() => scrollTo(link)}
                    className="text-left text-2xl font-semibold text-white/70 hover:text-gold-400 py-3.5 transition-colors border-b border-gold-900/30 last:border-0"
                  >
                    {link}
                  </motion.button>
                ))}
              </div>

              {/* Sheet CTAs */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35, duration: 0.35 }}
                className="px-6 pb-10 flex flex-col gap-3"
              >
                <button className="w-full py-3 text-sm font-medium text-white/60 border border-gold-800/30 rounded-xl hover:border-gold-600/40 hover:text-white transition-all">
                  Sign In
                </button>
                <button
                  onClick={() => scrollTo('contact')}
                  className="w-full py-3 text-sm font-bold rounded-xl transition-all"
                  style={{ background: 'linear-gradient(135deg, #d4a017, #b8860b)', color: '#0a0902' }}
                >
                  Request Demo
                </button>
              </motion.div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
