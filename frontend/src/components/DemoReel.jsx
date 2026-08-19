import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence, useInView } from 'framer-motion';
import { Play, Pause, ScanLine, Volume2, Maximize2, TrendingUp, AlertTriangle } from 'lucide-react';

/**
 * DemoReel — an auto-playing product "screen recording".
 *
 * Everything here is rendered live (no video file), so it stays sharp on any
 * display and weighs nothing. To swap in a real capture later, replace the
 * <Stage /> body with a <video autoPlay muted loop playsInline src="/demo.mp4" />
 * — the player chrome around it keeps working unchanged.
 */

const SCENE_MS = 5200;

const chapters = [
  { key: 'billing',   label: 'Barcode Billing' },
  { key: 'inventory', label: 'Live Inventory'  },
  { key: 'reports',   label: 'Reports'         },
];

/* ── Scene 1 — barcode billing ── */
function SceneBilling() {
  const items = [
    { name: 'Dolo 650 mg',        batch: 'B-4471', qty: 2, amt: '₹ 62.00'  },
    { name: 'Azithral 500 mg',    batch: 'B-2210', qty: 1, amt: '₹ 118.40' },
    { name: 'Cetirizine 10 mg',   batch: 'B-8093', qty: 3, amt: '₹ 45.00'  },
  ];

  return (
    <div className="grid h-full grid-cols-1 gap-3 sm:grid-cols-5">
      {/* Scanner pane */}
      <div className="surface relative col-span-1 flex flex-col items-center justify-center overflow-hidden rounded-2xl p-4 sm:col-span-2">
        <div className="absolute inset-x-6 top-6 h-px scan-line animate-scan" />
        <ScanLine size={26} className="mb-3 text-gold-400" strokeWidth={1.5} />
        <div className="flex h-14 items-end gap-[3px]">
          {[3, 1, 2, 1, 4, 1, 2, 3, 1, 2, 4, 1, 3, 1, 2].map((w, i) => (
            <motion.span
              key={i}
              initial={{ scaleY: 0.4, opacity: 0.4 }}
              animate={{ scaleY: 1, opacity: 1 }}
              transition={{ delay: i * 0.03, duration: 0.3 }}
              className="block h-full origin-bottom rounded-sm bg-white/70"
              style={{ width: w }}
            />
          ))}
        </div>
        <p className="mt-3 font-mono text-[10px] tracking-[0.2em] text-white/35">8901234 567890</p>
        <motion.p
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mt-2 rounded-full bg-mint/10 px-2.5 py-1 text-[10px] font-semibold text-mint"
        >
          Matched in 0.4s
        </motion.p>
      </div>

      {/* Invoice pane */}
      <div className="surface col-span-1 flex flex-col justify-between rounded-2xl p-4 sm:col-span-3">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <p className="text-[11px] font-semibold text-white/70">Invoice #INV-20841</p>
            <span className="rounded-full bg-white/5 px-2 py-0.5 font-mono text-[9px] text-white/40">GST 12%</span>
          </div>
          <div className="flex flex-col gap-1.5">
            {items.map((it, i) => (
              <motion.div
                key={it.name}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.35 + i * 0.35, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="flex items-center justify-between rounded-lg bg-white/[0.03] px-3 py-2"
              >
                <div className="min-w-0">
                  <p className="truncate text-[11px] font-medium text-white/85">{it.name}</p>
                  <p className="font-mono text-[9px] text-white/30">{it.batch}</p>
                </div>
                <div className="flex shrink-0 items-center gap-3">
                  <span className="font-mono text-[10px] text-white/40">×{it.qty}</span>
                  <span className="font-mono text-[11px] text-white/80">{it.amt}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.6 }}
          className="mt-3 flex items-center justify-between border-t border-white/[0.07] pt-3"
        >
          <span className="text-[10px] uppercase tracking-[0.18em] text-white/35">Total payable</span>
          <span className="font-display text-xl font-bold text-gold-400">₹ 225.40</span>
        </motion.div>
      </div>
    </div>
  );
}

/* ── Scene 2 — live inventory ── */
function SceneInventory() {
  const rows = [
    { name: 'Pantop 40 mg',    stock: 148, cap: 200, state: 'ok'   },
    { name: 'Amoxyclav 625',   stock: 24,  cap: 200, state: 'low'  },
    { name: 'Insulin Glargine',stock: 61,  cap: 120, state: 'ok'   },
    { name: 'Montek LC',       stock: 9,   cap: 150, state: 'crit' },
  ];
  const tone = { ok: '#6ee7b7', low: '#f5c24c', crit: '#f87171' };

  return (
    <div className="flex h-full flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="live-dot" />
          <p className="text-[11px] font-semibold text-white/70">Inventory ledger — live</p>
        </div>
        <motion.span
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 1.2 }}
          className="inline-flex items-center gap-1.5 rounded-full bg-gold-500/10 px-2.5 py-1 text-[10px] font-semibold text-gold-400"
        >
          <AlertTriangle size={11} />
          2 reorder alerts
        </motion.span>
      </div>

      <div className="surface flex flex-1 flex-col justify-center gap-3 rounded-2xl p-4">
        {rows.map((r, i) => (
          <motion.div
            key={r.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.12, duration: 0.4 }}
            className="flex items-center gap-3"
          >
            <span className="w-28 shrink-0 truncate text-[11px] text-white/70 sm:w-36">{r.name}</span>
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/[0.06]">
              <motion.div
                initial={{ width: '0%' }}
                animate={{ width: `${(r.stock / r.cap) * 100}%` }}
                transition={{ delay: 0.2 + i * 0.12, duration: 1, ease: [0.22, 1, 0.36, 1] }}
                className="h-full rounded-full"
                style={{ background: tone[r.state] }}
              />
            </div>
            <span className="w-12 shrink-0 text-right font-mono text-[10px] text-white/45">{r.stock}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

/* ── Scene 3 — reports ── */
function SceneReports() {
  const bars = [48, 62, 55, 78, 66, 91, 84];
  const days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

  return (
    <div className="grid h-full grid-cols-1 gap-3 sm:grid-cols-3">
      <div className="surface col-span-1 flex flex-col justify-between rounded-2xl p-4 sm:col-span-2">
        <div className="flex items-center justify-between">
          <p className="text-[11px] font-semibold text-white/70">Sales — last 7 days</p>
          <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-mint">
            <TrendingUp size={11} /> +18.4%
          </span>
        </div>
        <div className="flex h-24 items-end gap-2">
          {bars.map((h, i) => (
            <div key={i} className="flex flex-1 flex-col items-center gap-1.5">
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: `${h}%` }}
                transition={{ delay: i * 0.07, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                className="w-full rounded-t-md"
                style={{
                  background: i === 5
                    ? 'linear-gradient(to top, #a9761a, #f5c24c)'
                    : 'linear-gradient(to top, rgba(255,255,255,0.05), rgba(255,255,255,0.18))',
                }}
              />
              <span className="text-[9px] text-white/25">{days[i]}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        {[
          { label: 'Revenue today', value: '₹ 48,320', tone: '#f5c24c' },
          { label: 'Bills printed', value: '132',      tone: '#ffffff' },
          { label: 'Expiring soon', value: '11 items', tone: '#f87171' },
        ].map((k, i) => (
          <motion.div
            key={k.label}
            initial={{ opacity: 0, x: 12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.15 + i * 0.12, duration: 0.4 }}
            className="surface flex-1 rounded-2xl px-4 py-3"
          >
            <p className="text-[10px] uppercase tracking-[0.14em] text-white/35">{k.label}</p>
            <p className="font-display text-lg font-bold" style={{ color: k.tone }}>{k.value}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

const scenes = [SceneBilling, SceneInventory, SceneReports];

export default function DemoReel() {
  const ref     = useRef(null);
  const inView  = useInView(ref, { margin: '-15%' });
  const [scene, setScene]     = useState(0);
  const [playing, setPlaying] = useState(true);

  const running = playing && inView;

  useEffect(() => {
    if (!running) return undefined;
    const t = setTimeout(() => setScene((s) => (s + 1) % scenes.length), SCENE_MS);
    return () => clearTimeout(t);
  }, [scene, running]);

  const Stage = scenes[scene];

  return (
    <div ref={ref} className="relative">
      {/* Glow bed behind the frame */}
      <div
        className="pointer-events-none absolute -inset-x-10 -bottom-10 top-10 -z-10 opacity-70 blur-3xl"
        style={{ background: 'radial-gradient(ellipse at center, rgba(224,165,38,0.18), transparent 65%)' }}
      />

      <div className="glass overflow-hidden rounded-3xl p-1.5 shadow-[0_50px_120px_-40px_rgba(0,0,0,0.95)]">
        {/* Window chrome */}
        <div className="flex items-center gap-2 px-3 py-2.5">
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
          <div className="mx-auto flex items-center gap-2 rounded-full bg-white/[0.04] px-3 py-1">
            <span className="live-dot" />
            <span className="font-mono text-[10px] text-white/45">
              msms.aaibhavanigroup.com
            </span>
          </div>
          <Maximize2 size={13} className="text-white/20" />
        </div>

        {/* Stage */}
        <div className="relative h-[340px] overflow-hidden rounded-2xl bg-ink-900/80 p-3 sm:h-[300px] sm:p-4">
          <AnimatePresence mode="wait">
            <motion.div
              key={scene}
              initial={{ opacity: 0, y: 14, filter: 'blur(6px)' }}
              animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
              exit={{ opacity: 0, y: -14, filter: 'blur(6px)' }}
              transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
              className="h-full"
            >
              <Stage />
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Player bar */}
        <div className="flex items-center gap-3 px-3 py-3">
          <button
            onClick={() => setPlaying((p) => !p)}
            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/[0.06] text-white/80 transition-colors hover:bg-gold-500/20 hover:text-gold-300"
            aria-label={playing ? 'Pause demo' : 'Play demo'}
          >
            {playing ? <Pause size={13} /> : <Play size={13} className="ml-0.5" />}
          </button>

          {/* Chapter timeline */}
          <div className="flex flex-1 items-center gap-1.5">
            {chapters.map((c, i) => (
              <button
                key={c.key}
                onClick={() => setScene(i)}
                className="group relative h-1 flex-1 overflow-hidden rounded-full bg-white/[0.09]"
                aria-label={c.label}
              >
                <span
                  key={i === scene ? `run-${scene}` : `idle-${i}`}
                  className={`absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-gold-500 to-gold-300 ${
                    i === scene ? 'bar-fill' : ''
                  }`}
                  style={
                    i === scene
                      ? { animationDuration: `${SCENE_MS}ms`, animationPlayState: running ? 'running' : 'paused' }
                      : { width: i < scene ? '100%' : '0%', opacity: i < scene ? 0.45 : 1 }
                  }
                />
              </button>
            ))}
          </div>

          <span className="hidden w-32 shrink-0 text-right text-[10px] font-medium text-white/45 sm:block">
            {chapters[scene].label}
          </span>
          <Volume2 size={13} className="hidden shrink-0 text-white/20 sm:block" />
        </div>
      </div>
    </div>
  );
}
