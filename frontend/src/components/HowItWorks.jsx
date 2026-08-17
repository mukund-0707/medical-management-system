import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Truck, PackageCheck, ScanLine, Receipt, BarChart2 } from 'lucide-react';

const steps = [
  {
    num: '01',
    icon: Truck,
    title: 'Record Purchase',
    desc: 'Log medicines received from suppliers. System automatically increases inventory — batch-wise, with full traceability.',
  },
  {
    num: '02',
    icon: PackageCheck,
    title: 'Inventory Updates',
    desc: 'Every purchase, sale, or adjustment creates a ledger entry. Stock is always accurate — zero manual calculation needed.',
  },
  {
    num: '03',
    icon: ScanLine,
    title: 'Barcode Billing',
    desc: 'Cashier scans barcode. System instantly fetches medicine name, price, and available stock. Bill in seconds.',
  },
  {
    num: '04',
    icon: Receipt,
    title: 'Invoice Generated',
    desc: 'Automatic GST invoice generation after every sale. Inventory is reduced simultaneously — no double work.',
  },
  {
    num: '05',
    icon: BarChart2,
    title: 'Reports & Insights',
    desc: 'Dashboard shows sales trends, low stock alerts, expiry warnings, and full reports — updated in real time.',
  },
];

export default function HowItWorks() {
  const ref    = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section id="workflow" className="relative py-24 sm:py-32" style={{ background: '#111009' }}>
      <div className="divider-gold absolute top-0 inset-x-0" />

      <div className="max-w-7xl mx-auto px-5 sm:px-8">

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
            How It Works
          </div>
          <h2 className="text-3xl sm:text-5xl md:text-[52px] font-extrabold tracking-tight text-white leading-[1.1] mb-5">
            One Flow,{' '}
            <span className="shimmer-text">Zero Confusion</span>
          </h2>
          <p className="text-white/45 text-base sm:text-lg max-w-xl mx-auto leading-relaxed">
            A seamless workflow from supplier to sale — fully automated, fully auditable.
          </p>
        </motion.div>

        {/* Steps list */}
        <div className="flex flex-col gap-5 max-w-3xl mx-auto">
          {steps.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, x: -24 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ delay: 0.1 + i * 0.1, duration: 0.65, ease: [0.22, 1, 0.36, 1] }}
              className="group flex items-start gap-5 rounded-2xl p-5 sm:p-6 transition-all duration-300"
              style={{
                background: 'rgba(255,255,255,0.02)',
                border: '1px solid rgba(212,160,23,0.1)',
              }}
              whileHover={{
                borderColor: 'rgba(212,160,23,0.3)',
                backgroundColor: 'rgba(212,160,23,0.03)',
              }}
            >
              {/* Step number + icon */}
              <div className="shrink-0 flex flex-col items-center gap-2">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center"
                  style={{
                    background: 'linear-gradient(135deg, rgba(212,160,23,0.18), rgba(212,160,23,0.06))',
                    border: '1px solid rgba(212,160,23,0.25)',
                    boxShadow: '0 4px 16px rgba(212,160,23,0.15)',
                  }}
                >
                  <step.icon size={21} className="text-gold-400" strokeWidth={1.8} />
                </div>
                {/* Connector dot */}
                {i < steps.length - 1 && (
                  <div className="w-px h-6 mt-1" style={{ background: 'rgba(212,160,23,0.15)' }} />
                )}
              </div>

              {/* Text */}
              <div className="pt-1">
                <div className="flex items-center gap-3 mb-1.5">
                  <span
                    className="text-[10px] font-bold tracking-widest uppercase"
                    style={{ color: 'rgba(212,160,23,0.45)' }}
                  >
                    Step {step.num}
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-bold text-white mb-1.5 tracking-tight">
                  {step.title}
                </h3>
                <p className="text-sm text-white/45 leading-relaxed">{step.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="divider-gold absolute bottom-0 inset-x-0" />
    </section>
  );
}
