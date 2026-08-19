import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Pill, Truck, PackageCheck, ReceiptText, ShoppingCart, BarChart2 } from 'lucide-react';
import SectionHeading from './SectionHeading';

/* Cursor-following spotlight — the small detail that makes cards feel alive */
function BentoCard({ children, className = '', delay = 0, inView }) {
  const ref = useRef(null);

  const onMove = (e) => {
    const el = ref.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', `${e.clientX - r.left}px`);
    el.style.setProperty('--my', `${e.clientY - r.top}px`);
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={onMove}
      initial={{ opacity: 0, y: 26 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
      className={`group surface card-lift edge-light relative overflow-hidden rounded-3xl p-6 sm:p-7 ${className}`}
    >
      <span
        className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
        style={{
          background:
            'radial-gradient(420px circle at var(--mx, 50%) var(--my, 0%), rgba(245,194,76,0.10), transparent 62%)',
        }}
      />
      <div className="relative">{children}</div>
    </motion.div>
  );
}

function CardHead({ icon: Icon, tag, title }) {
  return (
    <>
      <div className="mb-5 flex items-start justify-between">
        <span
          className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.05] text-gold-300 transition-colors duration-500 group-hover:border-gold-400/40 group-hover:text-gold-200"
        >
          <Icon size={19} strokeWidth={1.7} />
        </span>
        <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-white/25">{tag}</span>
      </div>
      <h3 className="font-display mb-2.5 text-[19px] font-bold tracking-tight text-white">{title}</h3>
    </>
  );
}

export default function Features() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-90px' });

  return (
    <section id="features" ref={ref} className="relative py-24 sm:py-32">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="All-in-one platform"
          title={<>Every module your <span className="accent-serif text-gold-gradient">store</span> needs</>}
          sub="Medicine master to final report — tightly integrated, so nothing has to be typed twice."
          inView={inView}
        />

        <div className="mt-14 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6">
          {/* ── Wide: inventory ── */}
          <BentoCard className="lg:col-span-4" delay={0} inView={inView}>
            <CardHead icon={PackageCheck} tag="Inventory" title="Inventory that updates itself" />
            <p className="max-w-md text-[14px] leading-relaxed text-white/45">
              Stock moves only through real business events — purchase in, sale out, adjustment logged.
              Every change writes a ledger row, so the number on screen is always the number on the shelf.
            </p>

            <div className="mt-6 flex flex-col gap-2.5">
              {[
                { name: 'Pantop 40 mg', pct: 74, tone: '#6ee7b7' },
                { name: 'Amoxyclav 625', pct: 22, tone: '#f5c24c' },
                { name: 'Montek LC', pct: 8, tone: '#f87171' },
              ].map((r, i) => (
                <div key={r.name} className="flex items-center gap-3">
                  <span className="w-28 shrink-0 text-[11px] text-white/55">{r.name}</span>
                  <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/[0.06]">
                    <motion.span
                      initial={{ width: 0 }}
                      animate={inView ? { width: `${r.pct}%` } : {}}
                      transition={{ delay: 0.35 + i * 0.12, duration: 1, ease: [0.22, 1, 0.36, 1] }}
                      className="block h-full rounded-full"
                      style={{ background: r.tone }}
                    />
                  </div>
                  <span className="w-9 shrink-0 text-right font-mono text-[10px] text-white/35">{r.pct}%</span>
                </div>
              ))}
            </div>
          </BentoCard>

          {/* ── Tall: billing ── */}
          <BentoCard className="lg:col-span-2" delay={0.08} inView={inView}>
            <CardHead icon={ReceiptText} tag="Billing" title="Scan. Bill. Print." />
            <p className="text-[14px] leading-relaxed text-white/45">
              Barcode in, price and stock out. GST invoice ready before the customer opens their wallet.
            </p>
            <div className="mt-6 flex h-16 items-end gap-[3px] opacity-70">
              {[3, 1, 2, 4, 1, 2, 1, 3, 2, 1, 4, 2, 1, 3, 1, 2, 3, 1].map((w, i) => (
                <span key={i} className="block h-full rounded-sm bg-white/45" style={{ width: w }} />
              ))}
            </div>
            <p className="mt-3 font-mono text-[10px] tracking-[0.2em] text-white/25">₹ 225.40 · 3 items</p>
          </BentoCard>

          {/* ── Trio ── */}
          <BentoCard className="lg:col-span-2" delay={0.14} inView={inView}>
            <CardHead icon={Pill} tag="Core" title="Medicine master" />
            <p className="text-[14px] leading-relaxed text-white/45">
              One clean database — barcode, batch, expiry, HSN, category and rate, all in a single record.
            </p>
          </BentoCard>

          <BentoCard className="lg:col-span-2" delay={0.2} inView={inView}>
            <CardHead icon={Truck} tag="Operations" title="Supplier ledger" />
            <p className="text-[14px] leading-relaxed text-white/45">
              Vendor profiles, purchase history and outstanding payments — know who you owe, to the rupee.
            </p>
          </BentoCard>

          <BentoCard className="lg:col-span-2" delay={0.26} inView={inView}>
            <CardHead icon={ShoppingCart} tag="Purchase" title="Purchase entry" />
            <p className="text-[14px] leading-relaxed text-white/45">
              Log an invoice once; stock, batch and cost price update on receipt without a second entry.
            </p>
          </BentoCard>

          {/* ── Wide: reports ── */}
          <BentoCard className="lg:col-span-6" delay={0.32} inView={inView}>
            <div className="grid gap-8 lg:grid-cols-2 lg:items-center">
              <div>
                <CardHead icon={BarChart2} tag="Analytics" title="Reports you'll actually open" />
                <p className="max-w-md text-[14px] leading-relaxed text-white/45">
                  Daily sales, fast movers, dead stock, expiry in the next 90 days, GST summary — every
                  report is a click away and always current, because it reads the same ledger the billing
                  counter writes to.
                </p>
                <div className="mt-5 flex flex-wrap gap-2">
                  {['Daily closing', 'GST summary', 'Expiry watch', 'Dead stock'].map((t) => (
                    <span
                      key={t}
                      className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[11px] text-white/50"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex h-36 items-end gap-2 sm:h-40">
                {[38, 52, 44, 67, 58, 82, 71, 90, 63].map((h, i) => (
                  <motion.span
                    key={i}
                    initial={{ height: 0 }}
                    animate={inView ? { height: `${h}%` } : {}}
                    transition={{ delay: 0.5 + i * 0.05, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                    className="block flex-1 rounded-t-lg"
                    style={{
                      background:
                        i === 7
                          ? 'linear-gradient(to top, #a9761a, #f5c24c)'
                          : 'linear-gradient(to top, rgba(255,255,255,0.04), rgba(255,255,255,0.16))',
                    }}
                  />
                ))}
              </div>
            </div>
          </BentoCard>
        </div>
      </div>
    </section>
  );
}
