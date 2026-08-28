import { useEffect, useState } from 'react';
import { dashboardAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  TrendingUp, Package, ShoppingCart,
  AlertTriangle, DollarSign, Pill, Receipt,
} from 'lucide-react';
import { Skeleton, ErrorState } from '../hooks/useApi';

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
}

export default function Dashboard() {
  const { user } = useAuth();
  const [kpi, setKpi] = useState(null);
  const [inventory, setInventory] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [kpiRes, invRes, alertRes] = await Promise.all([
          dashboardAPI.kpi(),
          dashboardAPI.inventory(),
          dashboardAPI.alerts(),
        ]);
        setKpi(kpiRes.data.data);
        setInventory(invRes.data.data);
        setAlerts(alertRes.data.data);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return (
    <div className="space-y-4 md:space-y-6 max-w-screen-xl mx-auto">
      <div>
        <Skeleton className="h-6 w-48 mb-2" />
        <Skeleton className="h-4 w-64" />
      </div>
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-3 md:gap-4">
        {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 md:h-32 rounded-2xl" />)}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-3 md:gap-4">
        <Skeleton className="lg:col-span-3 h-56 md:h-64 rounded-2xl" />
        <Skeleton className="lg:col-span-2 h-56 md:h-64 rounded-2xl" />
      </div>
    </div>
  );

  if (error) return (
    <div className="max-w-screen-xl mx-auto">
      <ErrorState message={error} />
    </div>
  );

  const todayRevenue   = kpi?.sales?.today_total || 0;
  const totalMedicines = kpi?.inventory?.total_active_medicines || 0;
  const lowStockCount  = kpi?.inventory?.low_stock_count || 0;
  const pendingPO      = kpi?.purchases?.today_count || 0;
  const name           = user?.username || user?.first_name || 'Admin';

  const kpiCards = [
    { label: "Today's Revenue",   value: `₹${todayRevenue.toLocaleString('en-IN')}`, icon: DollarSign,    color: 'blue',    sub: `${kpi?.sales?.today_invoice_count || 0} bills` },
    { label: 'Active Medicines',  value: totalMedicines,                              icon: Pill,          color: 'emerald', sub: 'in catalog' },
    { label: "Today's Purchases", value: pendingPO,                                   icon: ShoppingCart,  color: 'amber',   sub: 'orders today' },
    { label: 'Low Stock Items',   value: lowStockCount,                               icon: AlertTriangle, color: 'red',     sub: `${kpi?.inventory?.expired_batch_count || 0} expired` },
  ];

  const COLOR_MAP = {
    blue:    'bg-blue-500/10 text-blue-400 border-blue-500/20',
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    amber:   'bg-amber-500/10 text-amber-400 border-amber-500/20',
    red:     'bg-red-500/10 text-red-400 border-red-500/20',
  };

  const lowStockList = inventory?.low_stock_medicines || [];
  const expiringList = inventory?.expiring_in_30_days || [];
  const availBatches = inventory?.batch_counts?.available_batches || 0;

  return (
    <div className="space-y-4 md:space-y-6 max-w-screen-xl mx-auto">

      {/* Header */}
      <div>
        <h2 className="text-white text-lg md:text-xl font-bold">
          {getGreeting()}, {name} 👋
        </h2>
        <p className="text-slate-400 text-xs md:text-sm mt-0.5">
          Here's what's happening in your store today.
        </p>
      </div>

      {/* KPI Cards — 2 cols on mobile, 4 on xl */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-3 md:gap-4">
        {kpiCards.map(({ label, value, sub, icon: Icon, color }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl md:rounded-2xl p-3.5 md:p-5 hover:border-slate-700 transition">
            <div className="flex items-start justify-between mb-3 md:mb-4">
              <div className={`w-8 h-8 md:w-10 md:h-10 rounded-lg md:rounded-xl flex items-center justify-center border ${COLOR_MAP[color]}`}>
                <Icon size={15} className="md:hidden" />
                <Icon size={18} className="hidden md:block" />
              </div>
              <span className="text-[10px] md:text-xs text-slate-500 text-right leading-tight">{sub}</span>
            </div>
            <p className="text-slate-400 text-[10px] md:text-xs mb-0.5 md:mb-1">{label}</p>
            <p className="text-white text-xl md:text-2xl font-bold tracking-tight">{value}</p>
          </div>
        ))}
      </div>

      {/* Low Stock + Expiring */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-3 md:gap-4">

        {/* Low Stock */}
        <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-xl md:rounded-2xl overflow-hidden">
          <div className="flex items-center justify-between px-4 md:px-5 py-3 md:py-4 border-b border-slate-800">
            <div>
              <h3 className="text-white font-semibold text-sm flex items-center gap-1.5 md:gap-2">
                <AlertTriangle size={13} className="text-amber-400" />
                Low Stock Medicines
              </h3>
              <p className="text-slate-500 text-xs mt-0.5">Needs restocking soon</p>
            </div>
            <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded-full flex-shrink-0">
              {lowStockList.length} items
            </span>
          </div>
          <div className="divide-y divide-slate-800">
            {lowStockList.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-8 md:py-10">No low stock items 🎉</p>
            ) : (
              lowStockList.slice(0, 6).map((item, i) => (
                <div key={i} className="flex items-center gap-3 px-4 md:px-5 py-3 md:py-3.5 hover:bg-slate-800/50 transition">
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-xs md:text-sm font-medium truncate">
                      {item.medicine__name || item.name}
                    </p>
                    <p className="text-slate-500 text-[10px] md:text-xs">{item.batch_number}</p>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-amber-400 font-bold text-sm">{item.quantity}</p>
                    <p className="text-slate-600 text-[10px] md:text-xs">units left</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Expiring Soon */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl md:rounded-2xl overflow-hidden">
          <div className="flex items-center justify-between px-4 md:px-5 py-3 md:py-4 border-b border-slate-800">
            <div>
              <h3 className="text-white font-semibold text-sm">Expiring in 30 Days</h3>
              <p className="text-slate-500 text-xs mt-0.5">Take action soon</p>
            </div>
            <span className="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded-full flex-shrink-0">
              {expiringList.length}
            </span>
          </div>
          <div className="divide-y divide-slate-800">
            {expiringList.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-8 md:py-10">No expiring items ✓</p>
            ) : (
              expiringList.slice(0, 6).map((item, i) => (
                <div key={i} className="flex items-center gap-3 px-4 md:px-5 py-2.5 md:py-3 hover:bg-slate-800/50 transition">
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-xs md:text-sm font-medium truncate">
                      {item.medicine__name || item.name}
                    </p>
                    <p className="text-slate-500 text-[10px] md:text-xs">{item.batch_number}</p>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-red-400 text-xs font-medium">
                      {item.expiry_date
                        ? new Date(item.expiry_date).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })
                        : '—'}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Quick stats — 2 cols mobile, 4 cols sm+ */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 md:gap-4">
        {[
          { label: 'Available Batches', value: availBatches,                                  icon: Package,      color: 'text-blue-400' },
          { label: 'Expired Batches',   value: inventory?.batch_counts?.expired_batches || 0, icon: AlertTriangle,color: 'text-red-400' },
          { label: 'Expiring (30d)',    value: expiringList.length,                           icon: Receipt,      color: 'text-amber-400' },
          { label: 'Inventory Value',   value: `₹${((kpi?.inventory?.inventory_value || 0) / 1000).toFixed(1)}K`, icon: TrendingUp, color: 'text-emerald-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-900 border border-slate-800 rounded-xl p-3 md:p-4 flex items-center gap-2 md:gap-3 hover:border-slate-700 transition">
            <s.icon size={18} className={`flex-shrink-0 ${s.color}`} />
            <div className="min-w-0">
              <p className="text-white font-bold text-base md:text-lg leading-tight">{s.value}</p>
              <p className="text-slate-500 text-[10px] md:text-xs leading-tight">{s.label}</p>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
