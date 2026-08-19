import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence, useInView, useScroll, useSpring } from 'framer-motion';
import { Truck, PackageCheck, ScanLine, Receipt, BarChart2 } from 'lucide-react';
import SectionHeading from './SectionHeading';

const steps = [
  {
    icon: Truck,
    title: 'Record the purchase',
    desc: 'Enter the supplier invoice once. Batch, expiry, cost and MRP are captured together and stock rises automatically.',
    meta: 'Supplier → Store',
  },
  {
    icon: PackageCheck,
    title: 'Inventory writes a ledger row',
    desc: 'Nothing is edited by hand. Every movement — in, out, adjusted — becomes a permanent, traceable entry.',
    meta: 'Auto ledger',
  },
  {
    icon: ScanLine,
    title: 'Cashier scans the barcode',
    desc: 'Name, batch, rate and available quantity appear instantly. No lookup, no typing, no guesswork at the counter.',
    meta: '< 1 second',
  },
  {
    icon: Receipt,
    title: 'GST invoice prints itself',
    desc: 'Tax splits, rounding and totals are computed on the fly, and the sold quantity leaves inventory in the same action.',
    meta: 'Compliant by default',
  },
  {
    icon: BarChart2,
    title: 'Reports stay current',
    desc: 'Sales trends, low-stock and expiry alerts update the moment a bill closes — the dashboard is never stale.',
    meta: 'Real time',
  },
];

function StepRow({ step, index, active, onEnter }) {
  const ref = useRef(null);
  const inView = useInView(ref, { margin: '-45% 0px -45% 0px' });

  useEffect(() => {
    if (inView) onEnter(index);
  }, [inView, index, onEnter]);

  const Icon = step.icon;

  return (
    <div ref={ref} className="relative pl-12 sm:pl-16">
      {/* Node on the rail */}
      <span
        className={`absolute left-[13px] top-7 h-3 w-3 -translate-x-1/2 rounded-full border-2 transition-all duration-500 sm:left-[17px] ${
          active
            ? 'scale-125 border-gold-400 bg-gold-400 shadow-[0_0_18px_rgba(245,194,76,0.7)]'
            : 'border-white/20 bg-ink-950'
        }`}
      />

      <motion.div
        initial={{ opacity: 0, y: 22 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-80px' }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className={`surface mb-4 rounded-3xl p-6 transition-all duration-500 sm:p-7 ${
          active ? 'border-gold-400/25 bg-white/[0.05]' : 'opacity-70'
        }`}
      >
        <div className="mb-3 flex items-center gap-3">
          <span
            className={`inline-flex h-10 w-10 items-center justify-center rounded-2xl transition-colors duration-500 ${
              active ? 'bg-gold-400/15 text-gold-300' : 'bg-white/[0.05] text-white/45'
            }`}
          >
            <Icon size={18} strokeWidth={1.7} />
          </span>
          <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-white/30">
            Step {String(index + 1).padStart(2, '0')} · {step.meta}
          </span>
        </div>

        <h3 className="font-display mb-2 text-[19px] font-bold tracking-tight text-white">
          {step.title}
        </h3>
        <p className="text-[14px] leading-relaxed text-white/45">{step.desc}</p>
      </motion.div>
    </div>
  );
}

export default function HowItWorks() {
  const sectionRef = useRef(null);
  const railRef    = useRef(null);
  const headInView = useInView(sectionRef, { once: true, margin: '-90px' });
  const [active, setActive] = useState(0);

  const { scrollYProgress } = useScroll({
    target: railRef,
    offset: ['start 60%', 'end 60%'],
  });
  const railScale = useSpring(scrollYProgress, { stiffness: 90, damping: 22, restDelta: 0.001 });

  return (
    <section id="workflow" ref={sectionRef} className="relative border-t border-white/[0.06] py-24 sm:py-32">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[420px] opacity-60"
        style={{ background: 'radial-gradient(ellipse 50% 100% at 50% 0%, rgba(224,165,38,0.10), transparent 70%)' }}
      />

      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="How it works"
          title={<>One flow, <span className="accent-serif text-gold-gradient">zero</span> confusion</>}
          sub="From the supplier's invoice to the customer's receipt — five steps, fully automated and fully auditable."
          inView={headInView}
        />

        <div className="mt-16 grid gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:gap-14">
          {/* Sticky live panel */}
          <div className="hidden lg:block">
            <div className="sticky top-28">
              <div className="glass relative overflow-hidden rounded-3xl p-8">
                <div
                  className="pointer-events-none absolute -right-16 -top-16 h-52 w-52 rounded-full blur-3xl"
                  style={{ background: 'radial-gradient(circle, rgba(224,165,38,0.28), transparent 65%)' }}
                />
                <AnimatePresence mode="wait">
                  <motion.div
                    key={active}
                    initial={{ opacity: 0, y: 16, filter: 'blur(6px)' }}
                    animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
                    exit={{ opacity: 0, y: -16, filter: 'blur(6px)' }}
                    transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                    className="relative"
                  >
                    <span className="font-display block text-[76px] font-extrabold leading-none tracking-tighter text-white/[0.08]">
                      {String(active + 1).padStart(2, '0')}
                    </span>
                    <h4 className="font-display mt-4 text-2xl font-bold leading-tight tracking-tight text-white">
                      {steps[active].title}
                    </h4>
                    <p className="mt-3 text-[14px] leading-relaxed text-white/45">
                      {steps[active].desc}
                    </p>
                  </motion.div>
                </AnimatePresence>

                <div className="mt-8 flex gap-1.5">
                  {steps.map((s, i) => (
                    <span
                      key={s.title}
                      className={`h-1 flex-1 rounded-full transition-all duration-500 ${
                        i <= active ? 'bg-gold-400' : 'bg-white/10'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Steps with scroll-linked rail */}
          <div ref={railRef} className="relative">
            <span className="absolute left-[13px] top-0 h-full w-px bg-white/[0.08] sm:left-[17px]" />
            <motion.span
              style={{ scaleY: railScale }}
              className="absolute left-[13px] top-0 h-full w-px origin-top bg-gradient-to-b from-gold-300 to-gold-600 sm:left-[17px]"
            />

            {steps.map((step, i) => (
              <StepRow key={step.title} step={step} index={i} active={active === i} onEnter={setActive} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
