import { useState, useEffect } from 'react';
import { purchaseAPI } from '../services/api';
import PageHeader from '../components/ui/PageHeader';
import DataTable from '../components/ui/DataTable';
import { Eye, CheckCircle, XCircle } from 'lucide-react';
import { Skeleton, ErrorState } from '../hooks/useApi';

const STATUS_STYLES = {
  'draft':     'bg-slate-600/20 text-slate-400 border-slate-600/30',
  'finalized': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  'cancelled': 'bg-red-500/10 text-red-400 border-red-500/20',
};

export default function Purchase() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await purchaseAPI.list({ page_size: 50 });
      setData(res.data.data?.results || res.data.results || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load purchases');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleFinalize = async (id) => {
    try {
      await purchaseAPI.finalize(id);
      load();
    } catch (err) {
      alert(err.response?.data?.message || 'Cannot finalize');
    }
  };

  const handleCancel = async (id) => {
    if (!confirm('Cancel this purchase order?')) return;
    try {
      await purchaseAPI.cancel(id);
      load();
    } catch (err) {
      alert(err.response?.data?.message || 'Cannot cancel');
    }
  };

  const columns = [
    { key: 'id', label: 'PO ID', render: v => <span className="text-blue-400 font-mono text-xs">{String(v).slice(0,8)}…</span> },
    { key: 'invoice_number', label: 'Invoice No.', render: v => <span className="text-white font-medium">{v || '—'}</span> },
    { key: 'supplier_name', label: 'Supplier' },
    { key: 'invoice_date', label: 'Date', render: v => v ? new Date(v).toLocaleDateString('en-IN') : '—' },
    { key: 'total_amount', label: 'Total', render: v => <span className="text-white font-semibold">₹{parseFloat(v || 0).toLocaleString('en-IN')}</span> },
    { key: 'status', label: 'Status', render: v => <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${STATUS_STYLES[v] || STATUS_STYLES['draft']}`}>{v}</span> },
    {
      key: 'actions', label: 'Actions',
      render: (_, row) => (
        <div className="flex items-center gap-1.5">
          {row.status === 'draft' && (
            <button onClick={() => handleFinalize(row.id)} title="Finalize" className="text-slate-400 hover:text-emerald-400 transition p-1 rounded-lg hover:bg-emerald-500/10"><CheckCircle size={14} /></button>
          )}
          {row.status !== 'cancelled' && (
            <button onClick={() => handleCancel(row.id)} title="Cancel" className="text-slate-400 hover:text-red-400 transition p-1 rounded-lg hover:bg-red-500/10"><XCircle size={14} /></button>
          )}
        </div>
      )
    },
  ];

  return (
    <div className="max-w-screen-xl mx-auto space-y-4">
      <PageHeader title="Purchase Orders" subtitle="Manage supplier purchase orders" addLabel="New PO" onAdd={() => {}} searchPlaceholder="Search..." />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Total', value: data.length },
          { label: 'Draft', value: data.filter(d => d.status === 'draft').length, color: 'text-slate-400' },
          { label: 'Finalized', value: data.filter(d => d.status === 'finalized').length, color: 'text-emerald-400' },
          { label: 'Cancelled', value: data.filter(d => d.status === 'cancelled').length, color: 'text-red-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3">
            <p className="text-slate-500 text-xs">{s.label}</p>
            <p className={`text-xl font-bold mt-0.5 ${s.color || 'text-white'}`}>{s.value}</p>
          </div>
        ))}
      </div>
      {loading ? <div className="space-y-2">{[...Array(5)].map((_, i) => <Skeleton key={i} className="h-12 rounded-xl" />)}</div>
        : error ? <ErrorState message={error} onRetry={load} />
        : <DataTable columns={columns} data={data} emptyText="No purchase orders found." />}
    </div>
  );
}
