import { useState, useEffect } from 'react';
import { supplierAPI } from '../services/api';
import PageHeader from '../components/ui/PageHeader';
import DataTable from '../components/ui/DataTable';
import { Edit2, Trash2, Phone, Mail } from 'lucide-react';
import { Skeleton, ErrorState } from '../hooks/useApi';

const STATUS_STYLES = {
  'active':   'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  'inactive': 'bg-slate-600/20 text-slate-400 border-slate-600/30',
};

export default function Supplier() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');

  const load = async (q = '') => {
    setLoading(true);
    setError(null);
    try {
      const res = await supplierAPI.list({ search: q, page_size: 50 });
      setData(res.data.data?.results || res.data.results || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load suppliers');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleDelete = async (id) => {
    if (!confirm('Deactivate this supplier?')) return;
    try {
      await supplierAPI.delete(id);
      load(search);
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to deactivate');
    }
  };

  const columns = [
    { key: 'id', label: 'ID', render: v => <span className="text-slate-500 font-mono text-xs">{String(v).slice(0,8)}…</span> },
    { key: 'name', label: 'Supplier Name', render: v => <span className="text-white font-medium">{v}</span> },
    { key: 'contact_person', label: 'Contact Person' },
    { key: 'mobile', label: 'Phone', render: v => v ? <span className="flex items-center gap-1.5"><Phone size={12} className="text-slate-500" />{v}</span> : '—' },
    { key: 'email', label: 'Email', render: v => v ? <span className="flex items-center gap-1.5"><Mail size={12} className="text-slate-500" />{v}</span> : '—' },
    { key: 'city', label: 'City' },
    { key: 'status', label: 'Status', render: v => <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${STATUS_STYLES[v] || STATUS_STYLES['inactive']}`}>{v}</span> },
    {
      key: 'actions', label: 'Actions',
      render: (_, row) => (
        <div className="flex items-center gap-2">
          <button className="text-slate-400 hover:text-blue-400 transition p-1 rounded-lg hover:bg-blue-500/10"><Edit2 size={14} /></button>
          <button onClick={() => handleDelete(row.id)} className="text-slate-400 hover:text-red-400 transition p-1 rounded-lg hover:bg-red-500/10"><Trash2 size={14} /></button>
        </div>
      )
    },
  ];

  return (
    <div className="max-w-screen-xl mx-auto space-y-4">
      <PageHeader
        title="Supplier"
        subtitle="Manage your medicine suppliers"
        addLabel="Add Supplier"
        onAdd={() => {}}
        searchPlaceholder="Search suppliers..."
        onSearch={e => { setSearch(e.target.value); load(e.target.value); }}
        searchValue={search}
      />
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {[
          { label: 'Total', value: data.length },
          { label: 'Active', value: data.filter(d => d.status === 'active').length, color: 'text-emerald-400' },
          { label: 'Inactive', value: data.filter(d => d.status === 'inactive').length, color: 'text-slate-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3">
            <p className="text-slate-500 text-xs">{s.label}</p>
            <p className={`text-xl font-bold mt-0.5 ${s.color || 'text-white'}`}>{s.value}</p>
          </div>
        ))}
      </div>
      {loading ? (
        <div className="space-y-2">{[...Array(5)].map((_, i) => <Skeleton key={i} className="h-12 rounded-xl" />)}</div>
      ) : error ? (
        <ErrorState message={error} onRetry={() => load()} />
      ) : (
        <DataTable columns={columns} data={data} emptyText="No suppliers found. Add your first supplier." />
      )}
    </div>
  );
}
