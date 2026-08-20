import { Plus, Search, Filter } from 'lucide-react';

export default function PageHeader({
  title, subtitle, onAdd, addLabel = 'Add New',
  showSearch = true, searchPlaceholder = 'Search...',
  onSearch, searchValue
}) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-6">
      <div className="flex-1">
        <h2 className="text-white text-xl font-bold">{title}</h2>
        {subtitle && <p className="text-slate-400 text-sm mt-0.5">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-2">
        {showSearch && (
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder={searchPlaceholder}
              value={searchValue || ''}
              onChange={onSearch}
              className="bg-slate-800 border border-slate-700 text-white placeholder-slate-500 rounded-xl pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-52"
            />
          </div>
        )}
        <button className="flex items-center gap-2 bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 rounded-xl px-3 py-2 text-sm transition">
          <Filter size={14} />
          <span className="hidden sm:inline">Filter</span>
        </button>
        {onAdd && (
          <button
            onClick={onAdd}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-4 py-2 text-sm font-medium transition shadow-lg shadow-blue-600/20"
          >
            <Plus size={14} />
            {addLabel}
          </button>
        )}
      </div>
    </div>
  );
}
