import { motion } from 'framer-motion';

/**
 * Shared section header: eyebrow chip + display title + supporting line.
 * Keeps rhythm identical across Features / Workflow / Stats / CTA.
 */
export default function SectionHeading({ eyebrow, title, sub, inView = true, align = 'center' }) {
  const centered = align === 'center';

  return (
    <motion.div
      initial={{ opacity: 0, y: 22 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.75, ease: [0.22, 1, 0.36, 1] }}
      className={centered ? 'mx-auto max-w-2xl text-center' : 'max-w-2xl'}
    >
      {eyebrow && (
        <span className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-1.5 text-[10.5px] font-semibold uppercase tracking-[0.2em] text-white/55">
          <span className="h-1.5 w-1.5 rounded-full bg-gold-400" />
          {eyebrow}
        </span>
      )}

      <h2 className="font-display text-[34px] font-extrabold leading-[1.03] tracking-[-0.03em] text-white sm:text-5xl md:text-[54px]">
        {title}
      </h2>

      {sub && (
        <p className={`mt-5 text-[15px] leading-relaxed text-white/45 sm:text-base ${centered ? 'mx-auto max-w-xl' : ''}`}>
          {sub}
        </p>
      )}
    </motion.div>
  );
}
