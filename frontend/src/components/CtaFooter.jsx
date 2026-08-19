import { useRef, useState } from 'react';
import { motion, AnimatePresence, useInView } from 'framer-motion';
import { ArrowRight, Check, Mail, Phone, MapPin } from 'lucide-react';
import { ABMark } from './Logo';

const fields = [
  { name: 'name',  type: 'text',  placeholder: 'Your name',        half: true  },
  { name: 'phone', type: 'tel',   placeholder: 'Phone number',     half: true  },
  { name: 'email', type: 'email', placeholder: 'Email address',    half: false },
  { name: 'store', type: 'text',  placeholder: 'Medical store name', half: false },
];

const footerCols = [
  { title: 'Product', links: ['Features', 'Workflow', 'Dashboard', 'Reports', 'Pricing'] },
  { title: 'Modules', links: ['Medicine Master', 'Inventory', 'Purchase', 'Billing', 'Analytics'] },
  { title: 'Company', links: ['About AB Groups', 'Contact', 'Privacy Policy', 'Terms of Service'] },
];

function DemoForm() {
  const [sent, setSent] = useState(false);

  // No backend wired yet — swap this for a POST to the MSMS API when the
  // enquiry endpoint is live.
  const onSubmit = (e) => {
    e.preventDefault();
    setSent(true);
  };

  return (
    <AnimatePresence mode="wait">
      {sent ? (
        <motion.div
          key="done"
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          className="flex flex-col items-center justify-center gap-3 py-12 text-center"
        >
          <span className="flex h-12 w-12 items-center justify-center rounded-full bg-mint/15 text-mint">
            <Check size={22} />
          </span>
          <p className="font-display text-lg font-bold text-white">Request received</p>
          <p className="max-w-xs text-[13px] text-white/45">
            Our team will call you within 24 hours to schedule the walkthrough.
          </p>
        </motion.div>
      ) : (
        <motion.form
          key="form"
          onSubmit={onSubmit}
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, y: -10 }}
          className="grid grid-cols-1 gap-3 sm:grid-cols-2"
        >
          {fields.map((f) => (
            <input
              key={f.name}
              name={f.name}
              type={f.type}
              required={f.name !== 'store'}
              placeholder={f.placeholder}
              className={`w-full rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3.5 text-[14px] text-white placeholder-white/30 outline-none transition-all duration-300 focus:border-gold-400/50 focus:bg-white/[0.06] ${
                f.half ? '' : 'sm:col-span-2'
              }`}
            />
          ))}

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            className="btn-gold mt-1 inline-flex w-full items-center justify-center gap-2 rounded-2xl py-4 text-[14px] font-bold sm:col-span-2"
          >
            Request free demo
            <ArrowRight size={16} />
          </motion.button>

          <p className="text-center text-[11.5px] text-white/30 sm:col-span-2">
            No credit card. No obligation. We reply within 24 hours.
          </p>
        </motion.form>
      )}
    </AnimatePresence>
  );
}

export default function CtaFooter() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-90px' });

  return (
    <>
      {/* ── CTA ── */}
      <section id="contact" ref={ref} className="relative overflow-hidden border-t border-white/[0.06] py-24 sm:py-32">
        <div className="pointer-events-none absolute inset-0 -z-10">
          <div
            className="aurora-blob animate-drift left-1/2 top-0 h-[560px] w-[760px] -translate-x-1/2"
            style={{ background: 'radial-gradient(ellipse, rgba(224,165,38,0.20), transparent 65%)' }}
          />
          <div className="absolute inset-0 grid-overlay opacity-60" />
        </div>

        <div className="mx-auto max-w-6xl px-5 sm:px-8">
          <div className="glass overflow-hidden rounded-4xl">
            <div className="grid lg:grid-cols-2">
              {/* Pitch */}
              <motion.div
                initial={{ opacity: 0, y: 24 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                className="flex flex-col justify-center border-b border-white/[0.07] p-8 sm:p-12 lg:border-b-0 lg:border-r"
              >
                <span className="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-1.5 text-[10.5px] font-semibold uppercase tracking-[0.2em] text-white/55">
                  <span className="live-dot" />
                  Taking demos this week
                </span>

                <h2 className="font-display text-[34px] font-extrabold leading-[1.02] tracking-[-0.03em] text-white sm:text-5xl">
                  Start managing
                  <br />
                  <span className="accent-serif text-gold-gradient">smarter</span> today
                </h2>

                <p className="mt-5 max-w-md text-[15px] leading-relaxed text-white/45">
                  See the full system on your own catalogue — inventory, billing and reports, live in a
                  30-minute walkthrough with our team.
                </p>

                <div className="mt-9 flex flex-col gap-3.5 text-[13.5px]">
                  <a href="mailto:info@aaibhavanigroup.com" className="group flex items-center gap-3 text-white/50 transition-colors hover:text-white">
                    <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] text-gold-400 transition-colors group-hover:border-gold-400/40">
                      <Mail size={15} />
                    </span>
                    info@aaibhavanigroup.com
                  </a>
                  <a href="tel:+919999999999" className="group flex items-center gap-3 text-white/50 transition-colors hover:text-white">
                    <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] text-gold-400 transition-colors group-hover:border-gold-400/40">
                      <Phone size={15} />
                    </span>
                    +91 99999 99999
                  </a>
                  <span className="flex items-center gap-3 text-white/50">
                    <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] text-gold-400">
                      <MapPin size={15} />
                    </span>
                    Maharashtra, India
                  </span>
                </div>
              </motion.div>

              {/* Form */}
              <motion.div
                initial={{ opacity: 0, y: 24 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ delay: 0.15, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                className="p-8 sm:p-12"
              >
                <DemoForm />
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="relative overflow-hidden border-t border-white/[0.06] pt-16">
        <div className="mx-auto max-w-6xl px-5 sm:px-8">
          <div className="grid grid-cols-2 gap-10 pb-14 lg:grid-cols-5">
            <div className="col-span-2">
              <div className="mb-5 flex items-center gap-3">
                <ABMark size={38} />
                <span className="flex flex-col leading-none">
                  <span className="font-display text-[15px] font-bold tracking-tight text-white">Aai Bhavani</span>
                  <span className="mt-1 text-[9px] font-medium uppercase tracking-[0.32em] text-gold-400/60">Group</span>
                </span>
              </div>
              <p className="max-w-[260px] text-[13.5px] leading-relaxed text-white/40">
                Modern software for Indian businesses — built with quality at the core.
                Trusted values, future vision.
              </p>
            </div>

            {footerCols.map((col) => (
              <div key={col.title}>
                <h4 className="mb-4 text-[10px] font-bold uppercase tracking-[0.2em] text-white/35">
                  {col.title}
                </h4>
                <ul className="flex flex-col gap-2.5">
                  {col.links.map((link) => (
                    <li key={link}>
                      <a href="#" className="text-[13.5px] text-white/45 transition-colors hover:text-gold-300">
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="flex flex-col items-center justify-between gap-3 border-t border-white/[0.06] py-7 sm:flex-row">
            <p className="text-[12px] text-white/25">© 2026 Aai Bhavani Group. All rights reserved.</p>
            <p className="text-[12px] text-white/25">Made in India 🇮🇳</p>
          </div>
        </div>

        {/* Oversized wordmark — the box is capped at 6.5vw so the letters get
            clipped at the baseline instead of leaving dead space under them. */}
        <div className="pointer-events-none h-[6.5vw] select-none overflow-hidden px-5 sm:px-8">
          <p
            className="font-display mx-auto max-w-6xl text-center text-[11vw] font-extrabold leading-[0.8] tracking-[-0.055em]"
            style={{
              background: 'linear-gradient(180deg, rgba(255,255,255,0.16), rgba(255,255,255,0.02))',
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            AAI BHAVANI
          </p>
        </div>
      </footer>
    </>
  );
}
