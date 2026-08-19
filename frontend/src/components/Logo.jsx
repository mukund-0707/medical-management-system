/**
 * Brand assets. The artwork in /public is derived from the official AB Groups
 * logo: the baked checkerboard background is keyed out, and the black ink
 * (the "B", the buildings, the wordmark) is remapped to warm ivory so the mark
 * stays legible on the dark theme. Gold is untouched.
 *
 *   logo-mark-dark.png  emblem only  — navbar, mobile sheet
 *   logo-dark.png       full lockup  — footer
 *   logo.png            original colours, transparent — for light backgrounds
 */

const MARK_RATIO = 220 / 257; // emblem is slightly taller than it is wide

export function ABMark({ size = 36, className = '' }) {
  return (
    <img
      src="/logo-mark-dark.png"
      alt=""
      aria-hidden="true"
      width={Math.round(size * MARK_RATIO)}
      height={size}
      style={{ height: size, width: 'auto' }}
      className={`select-none ${className}`}
    />
  );
}

export function ABLockup({ className = '', width = 260 }) {
  return (
    <img
      src="/logo-dark.png"
      alt="Aai Bhavani Group — Trusted Values. Future Vision."
      width={width}
      height={width}
      style={{ width }}
      className={`h-auto select-none ${className}`}
    />
  );
}

export default function Logo({ size = 34, className = '' }) {
  return (
    <a href="#hero" className={`group flex items-center gap-2.5 ${className}`} aria-label="Aai Bhavani Group">
      <ABMark size={size} className="transition-transform duration-300 group-hover:scale-105" />
      <span className="flex flex-col leading-none">
        <span className="font-serif text-[16px] uppercase tracking-[0.13em] text-white">
          Aai <span className="text-gold-gradient">Bhavani</span>
        </span>
        <span className="mt-[5px] text-[8px] font-medium uppercase tracking-[0.42em] text-white/35">
          Group
        </span>
      </span>
    </a>
  );
}
