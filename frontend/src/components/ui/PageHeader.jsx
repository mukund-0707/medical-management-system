import { Plus, Search, Filter } from 'lucide-react';

export default function PageHeader({
  title,
  subtitle,
  onAdd,
  addLabel = 'Add New',
  showSearch = true,
  searchPlaceholder = 'Search...',
  onSearch,
  searchValue,
}) {
  return (
    <div className="flex flex-col gap-3 mb-4 md:mb-6">
      {/* Title row */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h2 className="text-white text-lg md:text-xl font-bold">{title}</h2>
          {subtitle && <p className="text-slate-400 text-xs md:text-sm mt-0.5">{subtitle}</p>}
        </div>

        {/* Add button — always visible on the right of title */}
        {onAdd && (
          <button
            onClick={onAdd}
            className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-3 md:px-4 py-2 text-xs md:text-sm font-medium transition shadow-lg shadow-blue-600/20 flex-shrink-0"
          >
            <Plus size={14} />
            <span className="hidden sm:inline">{addLabel}</span>
            <span className="sm:hidden">Add</span>
          </button>
        )}
      </div>

      {/* Search + Filter row */}
      {showSearch && (
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder={searchPlaceholder}
              value={searchValue || ''}
              onChange={onSearch}
              className="w-full bg-slate-800 border border-slate-700 text-white placeholder-slate-500 rounded-xl pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="flex items-center gap-1.5 bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 rounded-xl px-3 py-2 text-sm transition flex-shrink-0">
            <Filter size={14} />
            <span className="hidden sm:inline text-xs">Filter</span>
          </button>
        </div>
      )}
    </div>
  );
}
