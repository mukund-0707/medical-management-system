import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Pill, Truck, PackageCheck, ReceiptText, ShoppingCart, BarChart2 } from 'lucide-react';

const features = [
  {
    icon: Pill,
    title: 'Medicine Master',
    desc: 'Centralized medicine database with barcode, batch, expiry, and category management. Never lose track of a single medicine.',
    tag: 'Core',
  },
  {
    icon: Truck,
    title: 'Supplier Management',
    desc: 'Manage supplier profiles, track purchase history, monitor outstanding payments, and maintain reliable vendor relationships.',
    tag: 'Operations',
  },
  {
    icon: PackageCheck,
    title: 'Smart Inventory',
    desc: 'Inventory-driven architecture. Every stock change is recorded through business operations — not manual edits. Full ledger history.',
    tag: 'Inventory',
  },
  {
    icon: ShoppingCart,
    title: 'Purchase Tracking',
    desc: 'Log supplier purchases, auto-update stock levels on receipt, and maintain complete purchase history with invoice records.',
    tag: 'Purchase',
  },
  {
    icon: ReceiptText,
    title: 'Barcode Billing',
    desc: 'Lightning-fast barcode-based billing. Scan medicine, auto-fetch price & stock, generate GST invoice in seconds.',
    tag: 'Billing',
  },
  {
    icon: BarChart2,
    title: 'Dashboard & Reports',
    desc: 'Real-time analytics, sales trends, low stock alerts, expiry warnings, and detailed reports — all on one screen.',
    tag: 'Analytics',
  },
];

const containerVariants = {
  hidden:   {},
  visible:  { transition: { staggerChildren: 0.1 } },
};

const cardVariants = {
  hidden:   { opacity: 0, y: 30 },
  visible:  { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] } },
};

export default function Features() {
  const ref    = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section id="features" className="relative py-24 sm:py-32" style={{ background: '#0a0902' }}>
      <div className="divider-gold absolute top-0 inset-x-0" />

      <div className="max-w-7xl mx-auto px-5 sm:px-8">

        {/* Section header */}
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
            All-in-One Platform
          </div>
          <h2 className="text-3xl sm:text-5xl md:text-[52px] font-extrabold tracking-tight text-white leading-[1.1] mb-5">
            Everything Your{' '}
            <span className="shimmer-text">Medical Store</span>
            <br className="hidden sm:block" />
            {' '}Needs
          </h2>
          <p className="text-white/45 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
            From medicine management to final reports — every module is tightly integrated
            so your store runs on autopilot.
          </p>
        </motion.div>

        {/* Cards grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5"
        >
          {features.map((f, idx) => (
            <motion.div
              key={f.title}
              variants={cardVariants}
              className="group feature-card relative rounded-2xl p-6 sm:p-7 cursor-default overflow-hidden"
              style={{
                background: 'rgba(255,255,255,0.025)',
                border: '1px solid rgba(212,160,23,0.1)',
              }}
            >
              {/* Hover glow bg */}
              <div
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none rounded-2xl"
                style={{ background: 'radial-gradient(ellipse at top left, rgba(212,160,23,0.05), transparent 70%)' }}
              />

              {/* Icon */}
              <div
                className="inline-flex items-center justify-center w-11 h-11 rounded-xl mb-5"
                style={{
                  background: 'linear-gradient(135deg, rgba(212,160,23,0.2), rgba(212,160,23,0.08))',
                  border: '1px solid rgba(212,160,23,0.25)',
                }}
              >
                <f.icon size={20} className="text-gold-400" strokeWidth={1.8} />
              </div>

              {/* Tag */}
              <span
                className="absolute top-6 right-6 text-[10px] font-bold tracking-wider uppercase"
                style={{ color: 'rgba(212,160,23,0.35)' }}
              >
                {f.tag}
              </span>

              {/* Content */}
              <h3 className="text-base sm:text-lg font-bold text-white mb-2.5 tracking-tight">
                {f.title}
              </h3>
              <p className="text-sm text-white/45 leading-relaxed">{f.desc}</p>

              {/* Bottom gold line */}
              <div
                className="absolute bottom-0 left-6 right-6 h-[1.5px] rounded-full scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"
                style={{ background: 'linear-gradient(90deg, #d4a017, #f4c040, #d4a017)' }}
              />
            </motion.div>
          ))}
        </motion.div>
      </div>

      <div className="divider-gold absolute bottom-0 inset-x-0" />
    </section>
  );
}
