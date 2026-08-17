import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { TrendingUp, ClipboardCheck, Timer, ShieldCheck } from 'lucide-react';

const stats = [
  {
    icon: TrendingUp,
    value: '100%',
    label: 'Auto Inventory',
    desc: 'Stock updates automatically on every purchase and sale — no manual entry ever',
  },
  {
    icon: ClipboardCheck,
    value: '0',
    label: 'Manual Calculations',
    desc: 'The system handles every calculation — from GST to stock ledger entries',
  },
  {
    icon: Timer,
    value: '< 3s',
    label: 'Billing Speed',
    desc: 'Barcode scan to printed invoice — the fastest billing experience for your cashier',
  },
  {
    icon: ShieldCheck,
    value: '∞',
    label: 'Ledger History',
    desc: 'Every stock movement is recorded forever — full audit trail, zero blind spots',
  },
];

export default function Stats() {
  const ref    = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section id="stats" className="relative py-24 sm:py-32 overflow-hidden" style={{ background: '#0a0902' }}>
      <div className="divider-gold absolute top-0 inset-x-0" />

      {/* Center glow */}
      <div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
      >
        <div
          className="w-[600px] h-[400px] rounded-full"
          style={{ background: 'radial-gradient(ellipse, rgba(212,160,23,0.07) 0%, transparent 70%)', filter: 'blur(60px)' }}
        />
      </div>

      <div className="relative max-w-7xl mx-auto px-5 sm:px-8">

        {/* Header */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="text-center mb-16 sm:mb-20"
        >
          <div
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-widest uppercase mb-5"
            style={{ border: '1px solid rgba(212,160,23,0.25)', background: 'rgba(212,160,23,0.07)', color: '#d4a017' }}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-gold-500" />
            By The Numbers
          </div>
          <h2 className="text-3xl sm:text-5xl md:text-[52px] font-extrabold tracking-tight text-white leading-[1.1] mb-5">
            Built for{' '}
            <span className="shimmer-text">Speed & Accuracy</span>
          </h2>
          <p className="text-white/45 text-base sm:text-lg max-w-xl mx-auto">
            Every metric that matters for running a smooth, profitable medical store.
          </p>
        </motion.div>

        {/* Stats grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 30 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.1 + i * 0.1, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
              whileHover={{ y: -6, boxShadow: '0 20px 50px rgba(0,0,0,0.4), 0 0 30px rgba(212,160,23,0.1)' }}
              className="rounded-2xl p-7 text-center transition-all duration-300 cursor-default"
              style={{
                background: 'rgba(255,255,255,0.025)',
                border: '1px solid rgba(212,160,23,0.12)',
              }}
            >
              {/* Icon */}
              <div
                className="inline-flex items-center justify-center w-12 h-12 rounded-xl mb-5"
                style={{
                  background: 'rgba(212,160,23,0.1)',
                  border: '1px solid rgba(212,160,23,0.2)',
                }}
              >
                <s.icon size={22} className="text-gold-500" />
              </div>

              {/* Value */}
              <div className="text-4xl sm:text-5xl font-black mb-2 shimmer-text tracking-tight">
                {s.value}
              </div>

              {/* Label */}
              <div className="text-sm font-bold text-white mb-3 tracking-tight">
                {s.label}
              </div>

              {/* Desc */}
              <p className="text-xs text-white/35 leading-relaxed">
                {s.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="divider-gold absolute bottom-0 inset-x-0" />
    </section>
  );
}
