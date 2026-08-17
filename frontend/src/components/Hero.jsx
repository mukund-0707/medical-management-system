import { motion } from 'framer-motion';
import { ArrowRight, ShieldCheck, Zap, BarChart3 } from 'lucide-react';

const fadeUp = {
  hidden:  { opacity: 0, y: 28 },
  visible: (delay = 0) => ({
    opacity: 1, y: 0,
    transition: { delay, duration: 0.75, ease: [0.22, 1, 0.36, 1] },
  }),
};

const badges = [
  { icon: ShieldCheck, label: 'Secure & Reliable' },
  { icon: Zap,         label: 'Real-time Sync'    },
  { icon: BarChart3,   label: 'Smart Analytics'   },
];

export default function Hero() {
  return (
    <section
      id="hero"
      className="relative min-h-screen w-full flex flex-col items-center justify-center overflow-hidden animated-bg"
    >
      {/* Gold orbs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full orb pointer-events-none"
        style={{ background: 'rgba(212,160,23,0.08)' }} />
      <div className="absolute bottom-1/4 right-1/4 w-[380px] h-[380px] rounded-full orb-2 pointer-events-none"
        style={{ background: 'rgba(180,130,10,0.06)' }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] rounded-full pointer-events-none"
        style={{ background: 'radial-gradient(circle, rgba(212,160,23,0.07) 0%, transparent 70%)', filter: 'blur(60px)' }} />

      {/* Grid */}
      <div className="absolute inset-0 grid-overlay opacity-100 pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 pt-32 pb-20 flex flex-col items-center text-center">

        {/* Group label */}
        <motion.div
          custom={0} variants={fadeUp} initial="hidden" animate="visible"
          className="mb-4 inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold tracking-widest uppercase"
          style={{ border: '1px solid rgba(212,160,23,0.3)', background: 'rgba(212,160,23,0.07)', color: '#d4a017' }}
        >
          <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
          Aai Bhavani Group — Trusted Values. Future Vision.
        </motion.div>

        {/* Main heading */}
        <motion.h1
          custom={0.15} variants={fadeUp} initial="hidden" animate="visible"
          className="text-4xl sm:text-6xl md:text-7xl lg:text-[80px] font-black leading-[1.05] tracking-tight text-white mb-6 max-w-5xl"
        >
          Smarter Medical
          <br />
          <span className="shimmer-text">Store Management</span>
          <br />
          <span className="text-white/80 text-3xl sm:text-4xl md:text-5xl font-bold">
            by AB Groups
          </span>
        </motion.h1>

        {/* Subheading */}
        <motion.p
          custom={0.3} variants={fadeUp} initial="hidden" animate="visible"
          className="text-base sm:text-lg md:text-xl text-white/50 max-w-2xl leading-relaxed mb-10"
        >
          AB Groups presents a complete Medical Store Management System — automating inventory,
          barcode billing, purchase tracking, and reports for modern Indian pharmacies.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          custom={0.45} variants={fadeUp} initial="hidden" animate="visible"
          className="flex flex-col sm:flex-row items-center gap-4 mb-16"
        >
          <motion.button
            whileHover={{ scale: 1.04, boxShadow: '0 8px 40px rgba(212,160,23,0.45)' }}
            whileTap={{ scale: 0.96 }}
            className="inline-flex items-center gap-2.5 font-bold text-sm sm:text-base rounded-full px-7 py-3.5"
            style={{
              background: 'linear-gradient(135deg, #f4c040, #d4a017, #b8860b)',
              color: '#0a0902',
              boxShadow: '0 4px 24px rgba(212,160,23,0.35)',
            }}
            onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
          >
            Explore Features
            <ArrowRight size={18} />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.04, borderColor: 'rgba(212,160,23,0.5)' }}
            whileTap={{ scale: 0.96 }}
            className="inline-flex items-center gap-2.5 text-sm sm:text-base font-medium rounded-full px-7 py-3.5 transition-all"
            style={{ border: '1px solid rgba(212,160,23,0.2)', color: 'rgba(212,160,23,0.8)' }}
            onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })}
          >
            Request Demo
          </motion.button>
        </motion.div>

        {/* Feature badges */}
        <motion.div
          custom={0.6} variants={fadeUp} initial="hidden" animate="visible"
          className="flex flex-wrap items-center justify-center gap-3"
        >
          {badges.map(({ icon: Icon, label }) => (
            <div
              key={label}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs sm:text-sm font-medium text-white/50"
              style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(212,160,23,0.1)' }}
            >
              <Icon size={14} className="text-gold-500" />
              {label}
            </div>
          ))}
        </motion.div>

        {/* Dashboard mockup */}
        <motion.div
          initial={{ opacity: 0, y: 60, scale: 0.96 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ delay: 0.75, duration: 1, ease: [0.22, 1, 0.36, 1] }}
          className="mt-20 w-full max-w-5xl"
        >
          <div
            className="relative rounded-2xl overflow-hidden p-1"
            style={{
              background: 'rgba(255,255,255,0.02)',
              border: '1px solid rgba(212,160,23,0.18)',
              boxShadow: '0 0 60px rgba(212,160,23,0.12), 0 40px 80px rgba(0,0,0,0.5)',
            }}
          >
            {/* Top bar */}
            <div
              className="flex items-center gap-2 px-4 py-3"
              style={{ borderBottom: '1px solid rgba(212,160,23,0.1)' }}
            >
              <span className="w-3 h-3 rounded-full" style={{ background: 'rgba(244,76,76,0.5)' }} />
              <span className="w-3 h-3 rounded-full" style={{ background: 'rgba(244,196,64,0.5)' }} />
              <span className="w-3 h-3 rounded-full" style={{ background: 'rgba(52,211,153,0.5)' }} />
              <span className="ml-4 text-xs font-mono" style={{ color: 'rgba(212,160,23,0.35)' }}>
                AB Groups — Medical Management Dashboard
              </span>
            </div>

            {/* Dashboard content */}
            <div className="p-5 sm:p-8">
              {/* Stat cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
                {[
                  { label: 'Total Medicines', value: '2,847', color: '#d4a017',   change: '+12 this week' },
                  { label: 'Today\'s Sales',   value: '₹48,320', color: '#34d399', change: '+8.2%' },
                  { label: 'Low Stock',        value: '23',      color: '#fbbf24', change: '-5 items' },
                  { label: 'Pending Orders',   value: '7',       color: '#a78bfa', change: '-2 pending' },
                ].map((stat) => (
                  <div
                    key={stat.label}
                    className="rounded-xl p-3 sm:p-4"
                    style={{ background: 'rgba(255,255,255,0.025)', border: '1px solid rgba(212,160,23,0.08)' }}
                  >
                    <p className="text-[10px] sm:text-xs mb-1" style={{ color: 'rgba(255,255,255,0.35)' }}>
                      {stat.label}
                    </p>
                    <p className="text-lg sm:text-2xl font-black" style={{ color: stat.color }}>
                      {stat.value}
                    </p>
                    <p className="text-[10px] mt-1" style={{ color: 'rgba(255,255,255,0.25)' }}>
                      {stat.change}
                    </p>
                  </div>
                ))}
              </div>

              {/* Charts row */}
              <div className="grid grid-cols-3 gap-3">
                <div
                  className="col-span-2 rounded-xl p-4 h-32 sm:h-40 flex flex-col justify-between"
                  style={{ background: 'rgba(255,255,255,0.015)', border: '1px solid rgba(212,160,23,0.07)' }}
                >
                  <p className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>
                    Sales Overview — Last 7 Days
                  </p>
                  <div className="flex items-end gap-2 h-20">
                    {[55, 72, 48, 90, 65, 88, 95].map((h, i) => (
                      <div
                        key={i}
                        className="flex-1 rounded-t-sm"
                        style={{
                          height: `${h}%`,
                          background: `linear-gradient(to top, #9a6f08, #d4a017)`,
                          opacity: 0.75,
                        }}
                      />
                    ))}
                  </div>
                </div>
                <div
                  className="rounded-xl p-4 h-32 sm:h-40 flex flex-col justify-between"
                  style={{ background: 'rgba(255,255,255,0.015)', border: '1px solid rgba(212,160,23,0.07)' }}
                >
                  <p className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>Stock Status</p>
                  <div className="flex flex-col gap-2">
                    {[
                      { label: 'In Stock',  pct: 78, color: '#34d399' },
                      { label: 'Low Stock', pct: 15, color: '#fbbf24' },
                      { label: 'Out Stock', pct: 7,  color: '#f87171' },
                    ].map((item) => (
                      <div key={item.label} className="flex items-center gap-2">
                        <span className="text-[10px] w-14 shrink-0" style={{ color: 'rgba(255,255,255,0.35)' }}>
                          {item.label}
                        </span>
                        <div className="flex-1 h-1.5 rounded-full" style={{ background: 'rgba(255,255,255,0.06)' }}>
                          <div className="h-full rounded-full" style={{ width: `${item.pct}%`, background: item.color }} />
                        </div>
                        <span className="text-[10px]" style={{ color: 'rgba(255,255,255,0.3)' }}>{item.pct}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 inset-x-0 h-24 pointer-events-none"
        style={{ background: 'linear-gradient(to top, #0a0902, transparent)' }} />
    </section>
  );
}
