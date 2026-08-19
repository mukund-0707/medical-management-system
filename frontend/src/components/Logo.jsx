/**
 * AB Groups mark — rounded-square monogram with a gold gradient.
 * Shared by the navbar, the mobile sheet and the footer so the brand
 * only ever has to change in one place.
 */
export function ABMark({ size = 36 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <rect x="0.75" y="0.75" width="62.5" height="62.5" rx="18" fill="url(#abPlate)" />
      <rect x="0.75" y="0.75" width="62.5" height="62.5" rx="18" stroke="url(#abEdge)" strokeWidth="1.5" />
      {/* A */}
      <path
        d="M9 47 L20.5 17 H26.5 L38 47 H31.6 L29.2 40.2 H17.8 L15.4 47 Z M19.7 34.9 H27.3 L23.5 24.2 Z"
        fill="url(#abGold)"
      />
      {/* B */}
      <path
        d="M40 17 H50.5 C55 17 58 20 58 24.3 C58 27 56.6 29 54.6 30 C57.1 31 59 33.6 59 36.7 C59 41.3 55.4 45 50.8 45 H40 Z M45.4 27.9 H49.6 C51.3 27.9 52.6 26.6 52.6 25 C52.6 23.3 51.3 22 49.6 22 H45.4 Z M45.4 40.4 H50.4 C52.4 40.4 53.9 38.9 53.9 37 C53.9 35 52.4 33.5 50.4 33.5 H45.4 Z"
        fill="url(#abGold)"
      />
      <defs>
        <linearGradient id="abPlate" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#16161f" />
          <stop offset="100%" stopColor="#07070a" />
        </linearGradient>
        <linearGradient id="abEdge" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="rgba(245,194,76,0.45)" />
          <stop offset="60%" stopColor="rgba(245,194,76,0.08)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.05)" />
        </linearGradient>
        <linearGradient id="abGold" x1="0" y1="10" x2="20" y2="54" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#fdf0c8" />
          <stop offset="45%" stopColor="#f5c24c" />
          <stop offset="100%" stopColor="#c2861a" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function Logo({ size = 36, className = '' }) {
  return (
    <a href="#hero" className={`flex items-center gap-3 group ${className}`} aria-label="Aai Bhavani Group">
      <span className="transition-transform duration-300 group-hover:scale-105">
        <ABMark size={size} />
      </span>
      <span className="flex flex-col leading-none">
        <span className="font-display text-[15px] font-bold tracking-tight text-white">
          Aai Bhavani
        </span>
        <span className="mt-1 text-[9px] font-medium uppercase tracking-[0.32em] text-gold-400/60">
          Group
        </span>
      </span>
    </a>
  );
}
