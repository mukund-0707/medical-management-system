import { useState, useEffect } from 'react';
import { salesAPI } from '../services/api';
import PageHeader from '../components/ui/PageHeader';
import DataTable from '../components/ui/DataTable';
import { Eye, Printer } from 'lucide-react';
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

export default function Billing() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await salesAPI.list({ page_size: 50, status: 'completed' });
        setData(res.data.data?.results || res.data.results || []);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to load billing records');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const columns = [
    { key: 'invoice_number', label: 'Invoice', render: v => <span className="text-blue-400 font-mono font-semibold text-xs">{v}</span> },
    { key: 'created_at', label: 'Date & Time', render: v => v ? new Date(v).toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—' },
    { key: 'subtotal', label: 'Subtotal', render: v => `₹${parseFloat(v || 0).toLocaleString('en-IN')}` },
    { key: 'tax_amount', label: 'Tax', render: v => `₹${parseFloat(v || 0).toLocaleString('en-IN')}` },
    { key: 'net_amount', label: 'Total', render: v => <span className="text-white font-bold">₹{parseFloat(v || 0).toLocaleString('en-IN')}</span> },
    { key: 'payment_mode', label: 'Payment', render: v => <span className={`text-xs px-2 py-0.5 rounded-lg font-medium capitalize ${PAYMENT_STYLES[v] || PAYMENT_STYLES['cash']}`}>{v?.replace('_', ' ')}</span> },
    { key: 'status', label: 'Status', render: v => <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${STATUS_STYLES[v] || STATUS_STYLES['completed']}`}>{v}</span> },
    {
      key: 'actions', label: 'Actions',
      render: () => (
        <div className="flex items-center gap-1.5">
          <button className="text-slate-400 hover:text-blue-400 transition p-1 rounded-lg hover:bg-blue-500/10"><Eye size={14} /></button>
          <button className="text-slate-400 hover:text-slate-200 transition p-1 rounded-lg hover:bg-slate-700"><Printer size={14} /></button>
        </div>
      )
    },
  ];

  const todayTotal = data
    .filter(d => new Date(d.created_at).toDateString() === new Date().toDateString())
    .reduce((acc, d) => acc + parseFloat(d.net_amount || 0), 0);

  return (
    <div className="max-w-screen-xl mx-auto space-y-4">
      <PageHeader title="Billing" subtitle="Invoice history and billing records" addLabel="New Bill" onAdd={() => {}} searchPlaceholder="Search invoices..." />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Today's Revenue", value: `₹${todayTotal.toLocaleString('en-IN')}`, color: 'text-blue-400' },
          { label: 'Bills Today', value: data.filter(d => new Date(d.created_at).toDateString() === new Date().toDateString()).length },
          { label: 'Total Bills', value: data.length },
          { label: 'Avg Bill', value: data.length ? `₹${(data.reduce((a, d) => a + parseFloat(d.net_amount || 0), 0) / data.length).toFixed(0)}` : '₹0' },
        ].map(s => (
          <div key={s.label} className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3">
            <p className="text-slate-500 text-xs">{s.label}</p>
            <p className={`text-xl font-bold mt-0.5 ${s.color || 'text-white'}`}>{s.value}</p>
          </div>
        ))}
      </div>
      {loading ? <div className="space-y-2">{[...Array(6)].map((_, i) => <Skeleton key={i} className="h-12 rounded-xl" />)}</div>
        : error ? <ErrorState message={error} />
        : <DataTable columns={columns} data={data} emptyText="No billing records yet." />}
    </div>
  );
}
