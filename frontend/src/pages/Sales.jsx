import { useState, useEffect } from 'react';
import { salesAPI } from '../services/api';
import PageHeader from '../components/ui/PageHeader';
import DataTable from '../components/ui/DataTable';
import { Eye, XCircle } from 'lucide-react';
import { Skeleton, ErrorState } from '../hooks/useApi';

const STATUS_STYLES = {
  'completed': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  'cancelled': 'bg-red-500/10 text-red-400 border-red-500/20',
};

const PAYMENT_STYLES = {
  'cash': 'bg-slate-700/50 text-slate-300',
  'upi':  'bg-violet-500/10 text-violet-400',
  'card': 'bg-blue-500/10 text-blue-400',
  'bank_transfer': 'bg-emerald-500/10 text-emerald-400',
};

export default function Sales() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await salesAPI.list({ page_size: 50 });
      setData(res.data.data?.results || res.data.results || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load sales');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleCancel = async (id) => {
    if (!confirm('Cancel this sale?')) return;
    try {
      await salesAPI.cancel(id);
      load();
    } catch (err) {
      alert(err.response?.data?.message || 'Cannot cancel');
    }
  };

  const columns = [
    { key: 'invoice_number', label: 'Invoice', render: v => <span className="text-blue-400 font-mono font-semibold text-xs">{v}</span> },
    { key: 'created_at', label: 'Date & Time', render: v => v ? new Date(v).toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—' },
    { key: 'net_amount', label: 'Amount', render: v => <span className="text-white font-bold">₹{parseFloat(v || 0).toLocaleString('en-IN')}</span> },
    { key: 'payment_mode', label: 'Payment', render: v => <span className={`text-xs px-2 py-0.5 rounded-lg font-medium capitalize ${PAYMENT_STYLES[v] || PAYMENT_STYLES['cash']}`}>{v?.replace('_', ' ')}</span> },
    { key: 'status', label: 'Status', render: v => <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${STATUS_STYLES[v] || STATUS_STYLES['completed']}`}>{v}</span> },
    {
      key: 'actions', label: 'Actions',
      render: (_, row) => (
        <div className="flex items-center gap-1.5">
          {row.status === 'completed' && (
            <button onClick={() => handleCancel(row.id)} title="Cancel" className="text-slate-400 hover:text-red-400 transition p-1 rounded-lg hover:bg-red-500/10"><XCircle size={14} /></button>
          )}
        </div>
      )
    },
  ];

  const todayRevenue = data
    .filter(d => d.status === 'completed' && new Date(d.created_at).toDateString() === new Date().toDateString())
    .reduce((acc, d) => acc + parseFloat(d.net_amount || 0), 0);

  return (
    <div className="max-w-screen-xl mx-auto space-y-4">
      <PageHeader title="Sales" subtitle="Sales history and transactions" showSearch={false} />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Total Sales', value: data.length },
          { label: "Today's Revenue", value: `₹${todayRevenue.toLocaleString('en-IN')}`, color: 'text-blue-400' },
          { label: 'Completed', value: data.filter(d => d.status === 'completed').length, color: 'text-emerald-400' },
          { label: 'Cancelled', value: data.filter(d => d.status === 'cancelled').length, color: 'text-red-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3">
            <p className="text-slate-500 text-xs">{s.label}</p>
            <p className={`text-xl font-bold mt-0.5 ${s.color || 'text-white'}`}>{s.value}</p>
          </div>
        ))}
      </div>
      {loading ? <div className="space-y-2">{[...Array(6)].map((_, i) => <Skeleton key={i} className="h-12 rounded-xl" />)}</div>
        : error ? <ErrorState message={error} onRetry={load} />
        : <DataTable columns={columns} data={data} emptyText="No sales yet. Complete a billing session to see sales here." />}
    </div>
  );
}
