import { useEffect, useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';
import { Quote } from 'lucide-react';
import SectionHeading from './SectionHeading';

const stats = [
  { value: 100, suffix: '%', label: 'Automated stock',   desc: 'Every purchase and sale moves inventory on its own — no manual entry, ever.' },
  { value: 0,   suffix: '',  label: 'Manual maths',      desc: 'GST splits, rounding and ledger balances are all computed by the system.' },
  { value: 3,   prefix: '<', suffix: 's', label: 'Per bill',  desc: 'Barcode scan to printed invoice, even on a busy counter.' },
  { value: null, display: '∞', label: 'Ledger history',  desc: 'Every stock movement is kept forever — a complete audit trail.' },
];

/* Count-up that runs once, when the block scrolls into view */
function useCountUp(target, start, duration = 1400) {
  const [n, setN] = useState(0);

  useEffect(() => {
    if (!start || target === null) return undefined;
    if (target === 0) { setN(0); return undefined; }

    let raf;
    const t0 = performance.now();
    const tick = (now) => {
      const p = Math.min((now - t0) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      setN(Math.round(target * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, start, duration]);

  return n;
}

function StatCell({ stat, index, inView }) {
  const n = useCountUp(stat.value, inView);

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.1, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
      className="group relative px-2 py-8 sm:px-6"
    >
      <div className="font-display flex items-baseline gap-0.5 text-[52px] font-extrabold leading-none tracking-[-0.04em] sm:text-[64px]">
        <span className="text-gold-gradient">
          {stat.display ?? `${stat.prefix ?? ''}${n}${stat.suffix ?? ''}`}
        </span>
      </div>
      <p className="font-display mt-4 text-[15px] font-semibold tracking-tight text-white">{stat.label}</p>
      <p className="mt-2 max-w-[240px] text-[13px] leading-relaxed text-white/40">{stat.desc}</p>
    </motion.div>
  );
}

export default function Stats() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-90px' });

  return (
    <section id="stats" ref={ref} className="relative border-t border-white/[0.06] py-24 sm:py-32">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="By the numbers"
          title={<>Built for speed <span className="accent-serif text-gold-gradient">&amp;</span> accuracy</>}
          sub="The metrics that decide whether a counter runs smoothly on a Monday morning rush."
          inView={inView}
        />

        <div className="mt-14 grid grid-cols-1 divide-y divide-white/[0.07] sm:grid-cols-2 sm:divide-y-0 lg:grid-cols-4 lg:divide-x">
          {stats.map((s, i) => (
            <StatCell key={s.label} stat={s} index={i} inView={inView} />
          ))}
        </div>

        {/* Editorial band */}
        <motion.figure
          initial={{ opacity: 0, y: 26 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.45, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          className="glass relative mt-16 overflow-hidden rounded-4xl p-8 sm:p-12"
        >
          <div
            className="pointer-events-none absolute -left-20 -top-24 h-72 w-72 rounded-full blur-3xl"
            style={{ background: 'radial-gradient(circle, rgba(224,165,38,0.22), transparent 65%)' }}
          />
          <Quote size={26} className="relative mb-5 text-gold-400/70" />
          <blockquote className="font-display relative max-w-3xl text-[22px] font-semibold leading-snug tracking-tight text-white/90 sm:text-[30px]">
            A medical store doesn&apos;t need more software. It needs one system where the stock, the bill
            and the report can never disagree with each other.
          </blockquote>
          <figcaption className="relative mt-6 flex items-center gap-3 text-[13px] text-white/40">
            <span className="h-px w-8 bg-gold-500/60" />
            Aai Bhavani Group — Trusted Values. Future Vision.
          </figcaption>
        </motion.figure>
      </div>
    </section>
  );
}
