import { FileText, TrendingUp, Package, ShoppingCart, Download } from 'lucide-react';

const REPORTS = [
  {
    category: 'Sales Reports',
    icon: TrendingUp,
    color: 'text-blue-400',
    bg: 'bg-blue-500/10 border-blue-500/20',
    items: [
      { name: 'Daily Sales Report',       desc: 'Day-wise revenue, transactions, and returns summary' },
      { name: 'Monthly Sales Report',     desc: 'Month-over-month sales performance' },
      { name: 'Medicine-wise Sales',      desc: 'Sales breakdown by medicine and category' },
      { name: 'Customer-wise Sales',      desc: 'Top customers by revenue' },
    ]
  },
  {
    category: 'Inventory Reports',
    icon: Package,
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10 border-emerald-500/20',
    items: [
      { name: 'Stock Status Report',       desc: 'Current stock levels with min/max thresholds' },
      { name: 'Low Stock Alert Report',    desc: 'Medicines below reorder level' },
      { name: 'Expiry Report',             desc: 'Medicines expiring in next 30/60/90 days' },
      { name: 'Stock Valuation Report',    desc: 'Total inventory value by category' },
    ]
  },
  {
    category: 'Purchase Reports',
    icon: ShoppingCart,
    color: 'text-amber-400',
    bg: 'bg-amber-500/10 border-amber-500/20',
    items: [
      { name: 'Purchase Order Report',     desc: 'All POs with status and payment details' },
      { name: 'Supplier-wise Purchases',   desc: 'Purchase history grouped by supplier' },
      { name: 'Outstanding Payments',      desc: 'Pending payment to suppliers' },
      { name: 'Monthly Purchase Summary',  desc: 'Purchase trend analysis' },
    ]
  },
];

const RECENT_GENERATED = [
  { name: 'Daily Sales - 20 Aug 2026',    type: 'Sales',     generated: '5 min ago',    size: '124 KB' },
  { name: 'Low Stock Alert Report',        type: 'Inventory', generated: '2 hrs ago',    size: '48 KB' },
  { name: 'Purchase Summary - Aug 2026',   type: 'Purchase',  generated: '1 day ago',    size: '215 KB' },
  { name: 'Stock Valuation Report',        type: 'Inventory', generated: '2 days ago',   size: '88 KB' },
  { name: 'Monthly Sales - Jul 2026',      type: 'Sales',     generated: '5 days ago',   size: '320 KB' },
];

const TYPE_COLOR = {
  Sales: 'bg-blue-500/10 text-blue-400', Inventory: 'bg-emerald-500/10 text-emerald-400', Purchase: 'bg-amber-500/10 text-amber-400',
};

export default function Reports() {
  return (
    <div className="max-w-screen-xl mx-auto space-y-6">
      <div>
        <h2 className="text-white text-xl font-bold">Reports</h2>
        <p className="text-slate-400 text-sm mt-0.5">Generate and download business reports</p>
      </div>

      {/* Report categories */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {REPORTS.map(({ category, icon: Icon, color, bg, items }) => (
          <div key={category} className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
            <div className={`flex items-center gap-3 px-5 py-4 border-b border-slate-800`}>
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center border ${bg}`}>
                <Icon size={16} className={color} />
              </div>
              <h3 className="text-white font-semibold text-sm">{category}</h3>
            </div>
            <div className="divide-y divide-slate-800">
              {items.map(item => (
                <div key={item.name} className="flex items-center justify-between px-5 py-3.5 hover:bg-slate-800/50 transition group">
                  <div>
                    <p className="text-white text-sm font-medium">{item.name}</p>
                    <p className="text-slate-500 text-xs mt-0.5">{item.desc}</p>
                  </div>
                  <button className="flex-shrink-0 ml-3 opacity-0 group-hover:opacity-100 transition flex items-center gap-1 text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 px-2.5 py-1.5 rounded-lg">
                    <Download size={12} /> Export
                  </button>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Recently generated */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <FileText size={16} className="text-slate-400" />
            <h3 className="text-white font-semibold text-sm">Recently Generated</h3>
          </div>
        </div>
        <div className="divide-y divide-slate-800">
          {RECENT_GENERATED.map(r => (
            <div key={r.name} className="flex items-center gap-4 px-5 py-3.5 hover:bg-slate-800/50 transition group">
              <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0">
                <FileText size={14} className="text-slate-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm font-medium truncate">{r.name}</p>
                <p className="text-slate-500 text-xs">{r.generated} · {r.size}</p>
              </div>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${TYPE_COLOR[r.type]}`}>{r.type}</span>
              <button className="opacity-0 group-hover:opacity-100 transition text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-700">
                <Download size={14} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
