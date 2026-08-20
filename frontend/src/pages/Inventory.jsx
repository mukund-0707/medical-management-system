import { useState, useEffect } from 'react';
import { inventoryAPI } from '../services/api';
import PageHeader from '../components/ui/PageHeader';
import DataTable from '../components/ui/DataTable';
import { AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { Skeleton, ErrorState } from '../hooks/useApi';

const STATUS_STYLES = {
  'available': { cls: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20', icon: CheckCircle },
  'expired':   { cls: 'bg-red-500/10 text-red-400 border-red-500/20',             icon: XCircle },
  'damaged':   { cls: 'bg-orange-500/10 text-orange-400 border-orange-500/20',    icon: AlertTriangle },
  'exhausted': { cls: 'bg-slate-600/20 text-slate-400 border-slate-600/30',       icon: XCircle },
};

export default function Inventory() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await inventoryAPI.batches({ page_size: 100 });
      setData(res.data.data?.results || res.data.results || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load inventory');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleMarkExpired = async (id) => {
    if (!confirm('Mark this batch as expired?')) return;
    try {
      await inventoryAPI.markExpired(id);
      load();
    } catch (err) {
      alert(err.response?.data?.message || 'Cannot mark expired');
    }
  };

  const columns = [
    { key: 'id', label: 'Batch ID', render: v => <span className="text-slate-500 font-mono text-xs">{String(v).slice(0,8)}…</span> },
    { key: 'medicine_name', label: 'Medicine', render: v => <span className="text-white font-medium">{v}</span> },
    { key: 'batch_number', label: 'Batch No.' },
    { key: 'quantity', label: 'Qty', render: (v, row) => (
      <div>
        <span className={`font-bold ${v === 0 ? 'text-red-400' : v <= 10 ? 'text-amber-400' : 'text-white'}`}>{v}</span>
        {v <= 10 && v > 0 && <AlertTriangle size={12} className="inline ml-1 text-amber-400" />}
      </div>
    )},
    { key: 'expiry_date', label: 'Expiry', render: v => v ? new Date(v).toLocaleDateString('en-IN', { year: 'numeric', month: 'short' }) : '—' },
    {
      key: 'status', label: 'Status',
      render: v => {
        const s = STATUS_STYLES[v] || STATUS_STYLES['available'];
        return <span className={`flex items-center gap-1 text-xs px-2 py-0.5 rounded-full border font-medium w-fit ${s.cls}`}><s.icon size={11} />{v}</span>;
      }
    },
    {
      key: 'actions', label: 'Actions',
      render: (_, row) => row.status === 'available' ? (
        <button onClick={() => handleMarkExpired(row.id)} className="text-xs text-slate-400 hover:text-red-400 transition px-2 py-1 rounded-lg hover:bg-red-500/10">
          Mark Expired
        </button>
      ) : null
    },
  ];

  const totalValue = data.reduce((acc, d) => acc + (parseFloat(d.quantity || 0) * parseFloat(d.purchase_price || 0)), 0);

  return (
    <div className="max-w-screen-xl mx-auto space-y-4">
      <PageHeader title="Inventory" subtitle="Real-time stock levels and batch tracking" addLabel="Adjust Stock" onAdd={() => {}} searchPlaceholder="Search..." />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Total Batches', value: data.length },
          { label: 'Available', value: data.filter(d => d.status === 'available').length, color: 'text-emerald-400' },
          { label: 'Expired', value: data.filter(d => d.status === 'expired').length, color: 'text-red-400' },
          { label: 'Stock Value', value: `₹${(totalValue/1000).toFixed(1)}K`, color: 'text-blue-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3">
            <p className="text-slate-500 text-xs">{s.label}</p>
            <p className={`text-xl font-bold mt-0.5 ${s.color || 'text-white'}`}>{s.value}</p>
          </div>
        ))}
      </div>
      {loading ? <div className="space-y-2">{[...Array(6)].map((_, i) => <Skeleton key={i} className="h-12 rounded-xl" />)}</div>
        : error ? <ErrorState message={error} onRetry={load} />
        : <DataTable columns={columns} data={data} emptyText="No inventory batches. Add purchases to populate inventory." />}
    </div>
  );
}
