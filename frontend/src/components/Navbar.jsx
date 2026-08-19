import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, ArrowUpRight } from 'lucide-react';
import Logo, { ABMark } from './Logo';

const navLinks = [
  { label: 'Features', id: 'features' },
  { label: 'Workflow', id: 'workflow' },
  { label: 'Numbers',  id: 'stats'    },
  { label: 'Contact',  id: 'contact'  },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled]     = useState(false);
  const [active, setActive]         = useState('hero');

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Highlight the section currently filling the viewport
  useEffect(() => {
    const ids = ['hero', ...navLinks.map((l) => l.id)];
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: '-45% 0px -50% 0px', threshold: 0 },
    );
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [mobileOpen]);

  const scrollTo = (id) => {
    setMobileOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      <motion.header
        initial={{ y: -24, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="fixed inset-x-0 top-0 z-50 px-4 pt-4 sm:px-6 sm:pt-5"
      >
        <nav
          className={`mx-auto flex items-center justify-between rounded-full transition-all duration-500 ${
            scrolled
              ? 'glass max-w-4xl px-3 py-2 shadow-[0_18px_50px_-20px_rgba(0,0,0,0.9)]'
              : 'max-w-6xl border border-transparent px-4 py-2.5'
          }`}
        >
          <Logo size={scrolled ? 30 : 34} />

          {/* Desktop links with a sliding active pill */}
          <ul className="hidden items-center gap-1 md:flex">
            {navLinks.map((link) => (
              <li key={link.id} className="relative">
                <button
                  onClick={() => scrollTo(link.id)}
                  className={`relative z-10 rounded-full px-4 py-2 text-[13px] font-medium transition-colors duration-300 ${
                    active === link.id ? 'text-white' : 'text-white/50 hover:text-white/85'
                  }`}
                >
                  {link.label}
                </button>
                {active === link.id && (
                  <motion.span
                    layoutId="nav-pill"
                    transition={{ type: 'spring', stiffness: 380, damping: 32 }}
                    className="absolute inset-0 rounded-full bg-white/[0.08] ring-1 ring-inset ring-white/10"
                  />
                )}
              </li>
            ))}
          </ul>

          <div className="hidden items-center gap-2 md:flex">
            <button className="rounded-full px-4 py-2 text-[13px] font-medium text-white/55 transition-colors hover:text-white">
              Sign In
            </button>
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => scrollTo('contact')}
              className="btn-gold group inline-flex items-center gap-1.5 rounded-full px-5 py-2.5 text-[13px] font-semibold"
            >
              Book a Demo
              <ArrowUpRight size={15} className="transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
            </motion.button>
          </div>

          <motion.button
            onClick={() => setMobileOpen((v) => !v)}
            whileTap={{ scale: 0.9 }}
            className="z-50 flex h-10 w-10 items-center justify-center rounded-full text-gold-400 transition-colors hover:bg-white/5 md:hidden"
            aria-label="Toggle menu"
            aria-expanded={mobileOpen}
          >
            <AnimatePresence mode="wait" initial={false}>
              <motion.span
                key={mobileOpen ? 'close' : 'menu'}
                initial={{ rotate: -90, opacity: 0, scale: 0.8 }}
                animate={{ rotate: 0, opacity: 1, scale: 1 }}
                exit={{ rotate: 90, opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.2 }}
              >
                {mobileOpen ? <X size={22} /> : <Menu size={22} />}
              </motion.span>
            </AnimatePresence>
          </motion.button>
        </nav>
      </motion.header>

      {/* ── Mobile sheet ── */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            key="sheet"
            initial={{ opacity: 0, y: -14 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -14 }}
            transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
            className="fixed inset-0 z-40 flex flex-col bg-ink-950/95 px-6 pb-10 pt-28 backdrop-blur-2xl md:hidden"
          >
            <div className="flex flex-1 flex-col justify-center">
              {navLinks.map((link, i) => (
                <motion.button
                  key={link.id}
                  initial={{ opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.06 + i * 0.06, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                  onClick={() => scrollTo(link.id)}
                  className="group flex items-center justify-between border-b border-white/[0.07] py-5 text-left"
                >
                  <span className="font-display text-3xl font-semibold tracking-tight text-white/85 group-hover:text-gold-400">
                    {link.label}
                  </span>
                  <span className="font-mono text-[11px] text-white/25">
                    0{i + 1}
                  </span>
                </motion.button>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.4 }}
              className="flex flex-col gap-3"
            >
              <button className="btn-ghost w-full rounded-2xl py-3.5 text-sm font-medium">
                Sign In
              </button>
              <button
                onClick={() => scrollTo('contact')}
                className="btn-gold w-full rounded-2xl py-3.5 text-sm font-bold"
              >
                Book a Demo
              </button>
              <div className="mt-4 flex items-center justify-center gap-2 opacity-40">
                <ABMark size={20} />
                <span className="text-[10px] uppercase tracking-[0.3em]">Trusted Values</span>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
