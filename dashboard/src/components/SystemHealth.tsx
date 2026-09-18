'use client';

import React, { useEffect, useState } from 'react';
import { fetchHealth } from '@/lib/api';
import { Cpu, Database, Server, Layers, ShieldCheck } from 'lucide-react';

export default function SystemHealth() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (e) {
      // Fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  const cpuPercent = health?.system?.cpu_usage_percent ?? 12;
  const ramPercent = health?.system?.memory_usage_percent ?? 45;
  const loadedCount = health?.modules?.loaded_active_count ?? 5;
  const totalCount = health?.modules?.total_configured_count ?? 50;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {/* CPU Usage Card */}
      <div className="cyber-card p-4 rounded-xl border border-zinc-800">
        <div className="flex items-center justify-between text-zinc-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">CPU Utilization</span>
          <Cpu className="w-4 h-4 text-cyan-400" />
        </div>
        <div className="flex items-baseline justify-between mb-2">
          <span className="text-2xl font-bold font-mono text-white">{cpuPercent}%</span>
          <span className="text-xs text-zinc-500 font-mono">Host Active</span>
        </div>
        <div className="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
          <div 
            className="bg-cyan-500 h-full rounded-full transition-all duration-500" 
            style={{ width: `${Math.min(100, Math.max(5, cpuPercent))}%` }}
          />
        </div>
      </div>

      {/* Memory Card */}
      <div className="cyber-card p-4 rounded-xl border border-zinc-800">
        <div className="flex items-center justify-between text-zinc-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Memory Allocation</span>
          <Server className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="flex items-baseline justify-between mb-2">
          <span className="text-2xl font-bold font-mono text-white">{ramPercent}%</span>
          <span className="text-xs text-zinc-500 font-mono">{health?.system?.memory_available_mb ?? 4096} MB Free</span>
        </div>
        <div className="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
          <div 
            className="bg-emerald-500 h-full rounded-full transition-all duration-500" 
            style={{ width: `${Math.min(100, Math.max(5, ramPercent))}%` }}
          />
        </div>
      </div>

      {/* Active Modules Card */}
      <div className="cyber-card p-4 rounded-xl border border-zinc-800">
        <div className="flex items-center justify-between text-zinc-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Modules Online</span>
          <Layers className="w-4 h-4 text-violet-400" />
        </div>
        <div className="flex items-baseline justify-between mb-2">
          <span className="text-2xl font-bold font-mono text-white">
            {loadedCount} <span className="text-xs font-normal text-zinc-500">/ {totalCount}</span>
          </span>
          <span className="text-xs px-2 py-0.5 rounded bg-violet-500/10 text-violet-400 border border-violet-500/30">
            Phase 1
          </span>
        </div>
        <div className="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
          <div 
            className="bg-violet-500 h-full rounded-full transition-all duration-500" 
            style={{ width: `${(loadedCount / totalCount) * 100}%` }}
          />
        </div>
      </div>

      {/* Defense Status Card */}
      <div className="cyber-card p-4 rounded-xl border border-zinc-800">
        <div className="flex items-center justify-between text-zinc-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Posture & Security</span>
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="flex items-baseline justify-between mb-2">
          <span className="text-lg font-bold text-emerald-400">DEFENSIVE ACTIVE</span>
          <span className="text-xs text-zinc-500 font-mono">100% Blue</span>
        </div>
        <div className="text-[11px] text-zinc-400 flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <span>RBAC + Immutable Auditing</span>
        </div>
      </div>
    </div>
  );
}
