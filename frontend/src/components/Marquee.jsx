const items = [
  'Medicine Master',
  'Batch & Expiry',
  'Supplier Ledger',
  'Purchase Entry',
  'Barcode Billing',
  'GST Invoices',
  'Stock Alerts',
  'Sales Reports',
  'Role-based Access',
  'Daily Closing',
];

export default function Marquee() {
  return (
    <section className="relative border-y border-white/[0.06] bg-ink-900/40 py-6">
      <div className="marquee-mask overflow-hidden">
        <div className="marquee-track gap-10 pr-10">
          {[0, 1].map((copy) => (
            <div key={copy} className="flex shrink-0 items-center gap-10 pr-10" aria-hidden={copy === 1}>
              {items.map((item) => (
                <span key={item} className="flex shrink-0 items-center gap-10">
                  <span className="font-display whitespace-nowrap text-[13px] font-medium uppercase tracking-[0.18em] text-white/35">
                    {item}
                  </span>
                  <span className="h-1 w-1 shrink-0 rounded-full bg-gold-500/60" />
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
