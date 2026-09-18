'use client';

import React, { useEffect, useState } from 'react';
import { fetchAlerts, resolveAlert } from '@/lib/api';
import { AlertTriangle, ShieldAlert, CheckCircle, Radio } from 'lucide-react';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>('ALL');
  const [loading, setLoading] = useState(true);

  const loadAlerts = async () => {
    try {
      const data = await fetchAlerts();
      setAlerts(data.alerts || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleResolve = async (id: string) => {
    try {
      await resolveAlert(id);
      loadAlerts();
    } catch (e) {
      console.error(e);
    }
  };

  const filtered = alerts.filter((a) => {
    if (filter === 'ALL') return true;
    if (filter === 'UNRESOLVED') return !a.resolved;
    if (filter === 'RESOLVED') return a.resolved;
    return a.severity.toUpperCase() === filter;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Radio className="w-4 h-4 text-rose-400 animate-pulse" />
            <span className="text-xs font-mono uppercase tracking-widest text-rose-400 font-semibold">
              Incident Response
            </span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Security Alerts & Incident Feed</h1>
          <p className="text-xs text-zinc-400 mt-0.5">
            Inter-module security detections, policy violations, and threat triage ledger
          </p>
        </div>

        {/* Severity Metrics */}
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="px-3 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30">
            {alerts.filter((a) => a.severity === 'high' || a.severity === 'critical').length} High/Critical
          </span>
          <span className="px-3 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
            {alerts.filter((a) => a.severity === 'medium').length} Medium
          </span>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-2 font-mono text-xs">
        {['ALL', 'UNRESOLVED', 'RESOLVED', 'CRITICAL', 'HIGH', 'MEDIUM'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded transition-all border ${
              filter === f
                ? 'bg-cyan-500 text-zinc-950 font-bold border-cyan-400'
                : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-zinc-200'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Alerts List */}
      <div className="space-y-3">
        {filtered.length === 0 ? (
          <div className="cyber-card p-12 text-center rounded-xl border border-zinc-800 text-zinc-500 font-mono text-xs">
            No alerts found matching filter criteria.
          </div>
        ) : (
          filtered.map((alt) => (
            <div
              key={alt.id}
              className={`cyber-card p-4 rounded-xl border transition-all flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                alt.resolved
                  ? 'border-zinc-800/40 opacity-60'
                  : 'border-zinc-800 hover:border-zinc-700'
              }`}
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span
                    className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${
                      alt.severity === 'critical' || alt.severity === 'high'
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : alt.severity === 'medium'
                        ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                        : 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30'
                    }`}
                  >
                    {alt.severity}
                  </span>
                  {alt.module_id && (
                    <span className="text-xs font-mono text-violet-400 font-semibold">
                      [{alt.module_id}]
                    </span>
                  )}
                  <h3 className="text-sm font-semibold text-white">{alt.title}</h3>
                </div>
                <p className="text-xs text-zinc-400 font-mono">{alt.description}</p>
                <div className="text-[11px] text-zinc-500 font-mono">
                  Reported: {alt.timestamp ? new Date(alt.timestamp).toLocaleString() : 'Recent'}
                </div>
              </div>

              <div>
                {alt.resolved ? (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-zinc-800 text-emerald-400 text-xs font-mono">
                    <CheckCircle className="w-3.5 h-3.5" />
                    Resolved
                  </span>
                ) : (
                  <button
                    onClick={() => handleResolve(alt.id)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-semibold transition-all shadow-sm"
                  >
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>Acknowledge & Resolve</span>
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
