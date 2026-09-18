'use client';

import React, { useEffect, useState } from 'react';
import ModuleCard from '@/components/ModuleCard';
import { fetchModules, fetchCategories } from '@/lib/api';
import { Search, Filter, Layers } from 'lucide-react';

export default function ModulesCatalogPage() {
  const [modules, setModules] = useState<any[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('All');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [mods, cats] = await Promise.all([fetchModules(), fetchCategories()]);
      setModules(mods);
      setCategories(['All', ...cats]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const filteredModules = modules.filter((m) => {
    const matchesCategory = selectedCategory === 'All' || m.category === selectedCategory;
    const matchesSearch =
      searchQuery === '' ||
      m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.display_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus =
      statusFilter === 'All' ||
      (statusFilter === 'Active' && m.is_loaded) ||
      (statusFilter === 'Configured' && !m.is_loaded);

    return matchesCategory && matchesSearch && matchesStatus;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Layers className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono uppercase tracking-widest text-cyan-400 font-semibold">
              Master Module Registry
            </span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Cybersecurity Defense Modules ({modules.length})
          </h1>
          <p className="text-xs text-zinc-400 mt-0.5">
            50 modular defensive capabilities organized across 12 standardized security categories
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-zinc-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search module name, ID, or tag..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-zinc-900/90 border border-zinc-800 rounded-lg text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-cyan-500 transition-colors font-mono"
          />
        </div>
      </div>

      {/* Filter Row: Categories + Status */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          <Filter className="w-3.5 h-3.5 text-zinc-500 shrink-0 mr-1" />
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium shrink-0 transition-all ${
                selectedCategory === cat
                  ? 'bg-cyan-500 text-zinc-950 font-semibold shadow-md shadow-cyan-500/20'
                  : 'bg-zinc-900/80 text-zinc-400 hover:text-white hover:bg-zinc-800 border border-zinc-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 text-xs font-mono text-zinc-400">
          <span>Filter Status:</span>
          {['All', 'Active', 'Configured'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-2.5 py-1 rounded border transition-all ${
                statusFilter === st
                  ? 'bg-zinc-800 text-cyan-400 border-cyan-800'
                  : 'border-zinc-800 hover:bg-zinc-900 text-zinc-500'
              }`}
            >
              {st}
            </button>
          ))}
          <span className="ml-auto text-zinc-500 font-mono text-xs">
            Showing {filteredModules.length} of {modules.length}
          </span>
        </div>
      </div>

      {/* Module Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredModules.map((mod) => (
          <ModuleCard key={mod.id} module={mod} onStateChange={loadData} />
        ))}
      </div>
    </div>
  );
}
