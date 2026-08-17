import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { ArrowRight, Mail, Phone, MapPin } from 'lucide-react';

// Reuse the same AB Logo as Navbar
function ABLogo({ size = 30 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="32" cy="32" r="32" fill="#0a0902" />
      <path d="M10 50 L22 18 L28 18 L40 50 H34 L31 42 H19 L16 50 Z M21 36 H29 L25 24 Z"
        fill="url(#goldGradF)" />
      <path d="M42 18 H52 C56 18 59 21 59 25 C59 27.5 57.5 29.5 55.5 30.5 C58 31.5 60 34 60 37 C60 41.5 56.5 45 52 45 H42 Z M47 28 H51 C52.7 28 54 26.7 54 25 C54 23.3 52.7 22 51 22 H47 Z M47 41 H52 C54 41 55.5 39.5 55.5 37.5 C55.5 35.5 54 34 52 34 H47 Z"
        fill="url(#goldGradF)" />
      <defs>
        <linearGradient id="goldGradF" x1="0" y1="0" x2="0" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0%"   stopColor="#f4c040" />
          <stop offset="50%"  stopColor="#d4a017" />
          <stop offset="100%" stopColor="#9a6f08" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function CtaFooter() {
  const ref    = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <>
      {/* ── CTA Section ── */}
      <section id="contact" className="relative py-24 sm:py-32 overflow-hidden" style={{ background: '#111009' }}>
        <div className="divider-gold absolute top-0 inset-x-0" />

        {/* Background glow */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] rounded-full"
            style={{ background: 'radial-gradient(ellipse, rgba(212,160,23,0.08) 0%, transparent 70%)', filter: 'blur(80px)' }}
          />
        </div>

        <div className="relative max-w-4xl mx-auto px-5 sm:px-8 text-center">
          <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 30 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          >
            <div
              className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-widest uppercase mb-7"
              style={{ border: '1px solid rgba(212,160,23,0.25)', background: 'rgba(212,160,23,0.07)', color: '#d4a017' }}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
              Ready to Transform Your Store?
            </div>

            <h2 className="text-3xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white leading-[1.1] mb-6">
              Start Managing Smarter
              <br />
              <span className="shimmer-text">with AB Groups.</span>
            </h2>

            <p className="text-white/45 text-base sm:text-lg max-w-xl mx-auto leading-relaxed mb-10">
              Aai Bhavani Group brings you enterprise-grade medical store management.
              Request a demo and see the complete system live.
            </p>

            {/* Contact form */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.2, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
              className="rounded-2xl p-6 sm:p-8 max-w-lg mx-auto"
              style={{
                background: 'rgba(255,255,255,0.025)',
                border: '1px solid rgba(212,160,23,0.15)',
              }}
            >
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Your Name"
                    className="w-full rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition-all"
                    style={{
                      background: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(212,160,23,0.12)',
                    }}
                    onFocus={(e) => e.target.style.borderColor = 'rgba(212,160,23,0.45)'}
                    onBlur={(e)  => e.target.style.borderColor = 'rgba(212,160,23,0.12)'}
                  />
                  <input
                    type="tel"
                    placeholder="Phone Number"
                    className="w-full rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition-all"
                    style={{
                      background: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(212,160,23,0.12)',
                    }}
                    onFocus={(e) => e.target.style.borderColor = 'rgba(212,160,23,0.45)'}
                    onBlur={(e)  => e.target.style.borderColor = 'rgba(212,160,23,0.12)'}
                  />
                </div>
                <input
                  type="email"
                  placeholder="Email Address"
                  className="w-full rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition-all"
                  style={{
                    background: 'rgba(255,255,255,0.04)',
                    border: '1px solid rgba(212,160,23,0.12)',
                  }}
                  onFocus={(e) => e.target.style.borderColor = 'rgba(212,160,23,0.45)'}
                  onBlur={(e)  => e.target.style.borderColor = 'rgba(212,160,23,0.12)'}
                />
                <input
                  type="text"
                  placeholder="Medical Store Name"
                  className="w-full rounded-xl px-4 py-3 text-sm text-white placeholder-white/30 outline-none transition-all"
                  style={{
                    background: 'rgba(255,255,255,0.04)',
                    border: '1px solid rgba(212,160,23,0.12)',
                  }}
                  onFocus={(e) => e.target.style.borderColor = 'rgba(212,160,23,0.45)'}
                  onBlur={(e)  => e.target.style.borderColor = 'rgba(212,160,23,0.12)'}
                />
                <motion.button
                  whileHover={{ scale: 1.02, boxShadow: '0 8px 40px rgba(212,160,23,0.45)' }}
                  whileTap={{ scale: 0.97 }}
                  className="w-full flex items-center justify-center gap-2.5 font-bold rounded-xl py-3.5 text-sm transition-all"
                  style={{
                    background: 'linear-gradient(135deg, #f4c040, #d4a017, #b8860b)',
                    color: '#0a0902',
                    boxShadow: '0 4px 20px rgba(212,160,23,0.3)',
                  }}
                >
                  Request Free Demo
                  <ArrowRight size={17} />
                </motion.button>
              </div>
              <p className="text-xs mt-4 text-center" style={{ color: 'rgba(212,160,23,0.3)' }}>
                No credit card required. We'll reach out within 24 hours.
              </p>
            </motion.div>

            {/* Contact info */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.5, duration: 0.6 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-5 sm:gap-10 mt-10 text-sm text-white/35"
            >
              <a href="mailto:info@aaibhavanigroup.com" className="flex items-center gap-2 hover:text-gold-400 transition-colors">
                <Mail size={15} className="text-gold-600" />
                info@aaibhavanigroup.com
              </a>
              <a href="tel:+919999999999" className="flex items-center gap-2 hover:text-gold-400 transition-colors">
                <Phone size={15} className="text-gold-600" />
                +91 99999 99999
              </a>
              <span className="flex items-center gap-2">
                <MapPin size={15} className="text-gold-600" />
                India
              </span>
            </motion.div>
          </motion.div>
        </div>

        <div className="divider-gold absolute bottom-0 inset-x-0" />
      </section>

      {/* ── Footer ── */}
      <footer className="relative pt-14 pb-8" style={{ background: '#0a0902' }}>
        <div className="max-w-7xl mx-auto px-5 sm:px-8">

          {/* Top row */}
          <div
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 pb-12"
            style={{ borderBottom: '1px solid rgba(212,160,23,0.1)' }}
          >
            {/* Brand */}
            <div className="col-span-1 sm:col-span-2 lg:col-span-1">
              <div className="flex items-center gap-3 mb-4">
                <ABLogo size={36} />
                <div className="flex flex-col leading-tight">
                  <span className="text-[15px] font-extrabold tracking-wider uppercase text-white">
                    Aai <span className="text-gold-500">Bhavani</span>
                  </span>
                  <span className="text-[9px] tracking-[0.25em] uppercase text-gold-700/60">Group</span>
                </div>
              </div>
              <p className="text-sm text-white/35 leading-relaxed max-w-[220px] mb-2">
                Trusted Values. Future Vision.
              </p>
              <p className="text-xs text-white/25 leading-relaxed max-w-[220px]">
                Modern solutions for Indian businesses — built with quality at the core.
              </p>
            </div>

            {/* Links */}
            {[
              {
                title: 'Product',
                links: ['Features', 'Workflow', 'Dashboard', 'Reports', 'Pricing'],
              },
              {
                title: 'Modules',
                links: ['Medicine Master', 'Inventory', 'Purchase', 'Billing', 'Analytics'],
              },
              {
                title: 'Company',
                links: ['About AB Groups', 'Contact', 'Privacy Policy', 'Terms of Service'],
              },
            ].map((col) => (
              <div key={col.title}>
                <h4
                  className="text-[10px] font-bold tracking-widest uppercase mb-4"
                  style={{ color: 'rgba(212,160,23,0.5)' }}
                >
                  {col.title}
                </h4>
                <ul className="flex flex-col gap-2.5">
                  {col.links.map((link) => (
                    <li key={link}>
                      <a href="#" className="text-sm text-white/35 hover:text-gold-400 transition-colors">
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Bottom row */}
          <div className="pt-7 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-white/20">
              © 2026 Aai Bhavani Group. All rights reserved.
            </p>
            <p className="text-xs" style={{ color: 'rgba(212,160,23,0.3)' }}>
              Trusted Values. Future Vision.
            </p>
          </div>
        </div>
      </footer>
    </>
  );
}
