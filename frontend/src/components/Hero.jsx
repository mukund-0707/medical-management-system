import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowRight, Play, ShieldCheck, Zap, Boxes } from 'lucide-react';
import DemoReel from './DemoReel';

const rise = {
  hidden: { opacity: 0, y: 26, filter: 'blur(8px)' },
  visible: (d = 0) => ({
    opacity: 1,
    y: 0,
    filter: 'blur(0px)',
    transition: { delay: d, duration: 0.85, ease: [0.22, 1, 0.36, 1] },
  }),
};

const proofs = [
  { icon: Zap,         label: 'Bill in under 3 seconds' },
  { icon: Boxes,       label: 'Batch + expiry aware'    },
  { icon: ShieldCheck, label: 'Full audit ledger'       },
];

export default function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] });
  const reelY     = useTransform(scrollYProgress, [0, 1], [0, 110]);
  const reelScale = useTransform(scrollYProgress, [0, 1], [1, 0.94]);
  const copyFade  = useTransform(scrollYProgress, [0, 0.7], [1, 0]);

  return (
    <section
      id="hero"
      ref={ref}
      className="relative w-full overflow-hidden pb-24 pt-32 sm:pb-32 sm:pt-40"
    >
      {/* ── Atmosphere ── */}
      <div className="pointer-events-none absolute inset-0 -z-10">
        <div
          className="aurora-blob animate-drift left-[8%] top-[-12%] h-[520px] w-[520px]"
          style={{ background: 'radial-gradient(circle, rgba(224,165,38,0.28), transparent 62%)' }}
        />
        <div
          className="aurora-blob animate-drift right-[4%] top-[6%] h-[440px] w-[440px]"
          style={{ background: 'radial-gradient(circle, rgba(110,231,183,0.12), transparent 62%)', animationDelay: '-8s' }}
        />
        <div
          className="aurora-blob animate-drift bottom-[6%] left-[34%] h-[560px] w-[560px]"
          style={{ background: 'radial-gradient(circle, rgba(245,194,76,0.14), transparent 65%)', animationDelay: '-15s' }}
        />
        <div className="absolute inset-0 grid-overlay" />
        <div className="vignette absolute inset-0" />
      </div>

      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        {/* ── Copy ── */}
        <motion.div style={{ opacity: copyFade }} className="flex flex-col items-center text-center">
          <motion.a
            href="#features"
            custom={0}
            variants={rise}
            initial="hidden"
            animate="visible"
            className="group mb-7 inline-flex items-center gap-2.5 rounded-full border border-white/10 bg-white/[0.04] py-1.5 pl-2 pr-4 text-[11px] font-medium text-white/65 backdrop-blur-md transition-colors hover:border-gold-400/40 hover:text-white"
          >
            <span className="rounded-full bg-gold-400/15 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-gold-300">
              New
            </span>
            Barcode billing + GST invoices, out of the box
            <ArrowRight size={12} className="transition-transform duration-300 group-hover:translate-x-0.5" />
          </motion.a>

          <motion.h1
            custom={0.1}
            variants={rise}
            initial="hidden"
            animate="visible"
            className="font-display text-[42px] font-extrabold leading-[0.95] tracking-[-0.035em] sm:text-6xl md:text-7xl lg:text-[86px]"
          >
            <span className="text-soft-gradient">Run your medical</span>
            <br />
            <span className="text-soft-gradient">store on </span>
            <span className="accent-serif text-gold-gradient">autopilot</span>
          </motion.h1>

          <motion.p
            custom={0.24}
            variants={rise}
            initial="hidden"
            animate="visible"
            className="mt-7 max-w-xl text-[15px] leading-relaxed text-white/50 sm:text-lg"
          >
            One system for inventory, purchases, barcode billing and reports —
            built for Indian pharmacies by{' '}
            <span className="text-white/75">Aai Bhavani Group</span>.
          </motion.p>

          <motion.div
            custom={0.36}
            variants={rise}
            initial="hidden"
            animate="visible"
            className="mt-9 flex w-full flex-col items-center gap-3 sm:w-auto sm:flex-row"
          >
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })}
              className="btn-gold inline-flex w-full items-center justify-center gap-2 rounded-full px-7 py-3.5 text-[15px] font-bold sm:w-auto"
            >
              Book a live demo
              <ArrowRight size={17} />
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => document.getElementById('reel')?.scrollIntoView({ behavior: 'smooth' })}
              className="btn-ghost group inline-flex w-full items-center justify-center gap-2.5 rounded-full py-3 pl-3 pr-6 text-[15px] font-medium sm:w-auto"
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white/10 transition-colors group-hover:bg-gold-400 group-hover:text-ink-900">
                <Play size={12} className="ml-0.5 fill-current" />
              </span>
              Watch the tour
            </motion.button>
          </motion.div>

          <motion.ul
            custom={0.5}
            variants={rise}
            initial="hidden"
            animate="visible"
            className="mt-10 flex flex-wrap items-center justify-center gap-x-7 gap-y-3"
          >
            {proofs.map(({ icon: Icon, label }) => (
              <li key={label} className="inline-flex items-center gap-2 text-[12.5px] text-white/40">
                <Icon size={14} className="text-gold-400/80" strokeWidth={1.8} />
                {label}
              </li>
            ))}
          </motion.ul>
        </motion.div>

        {/* ── Product reel ── */}
        <motion.div id="reel" style={{ y: reelY, scale: reelScale }} className="mt-16 sm:mt-20">
          <motion.div
            initial={{ opacity: 0, y: 70 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 1.1, ease: [0.22, 1, 0.36, 1] }}
          >
            <DemoReel />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
