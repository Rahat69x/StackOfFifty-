'use client';

import React, { useEffect, useState } from 'react';
import { fetchAlerts, resolveAlert } from '@/lib/api';
import { AlertTriangle, CheckCircle, Bell, Radio } from 'lucide-react';

export default function AlertFeed() {
  const [data, setData] = useState<{ alerts: any[]; recent_event_stream: any[] }>({
    alerts: [],
    recent_event_stream: []
  });
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const res = await fetchAlerts();
      setData(res);
    } catch (e) {
      // Fallback display
      setData({
        alerts: [
          {
            id: 'alt_01',
            module_id: 'mod_001',
            title: 'Honeypot Decoy Probe Intercepted',
            description: 'HTTP probe from 192.168.1.145 requesting /admin/config.php',
            severity: 'high',
            resolved: false,
            timestamp: new Date().toISOString()
          },
          {
            id: 'alt_02',
            module_id: 'mod_011',
            title: 'Firewall Ingress Block',
            description: 'Dropped unauthorized TCP connection to port 23 (Telnet)',
            severity: 'medium',
            resolved: false,
            timestamp: new Date().toISOString()
          }
        ],
        recent_event_stream: []
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    const timer = setInterval(load, 4000);
    return () => clearInterval(timer);
  }, []);

  const handleResolve = async (id: string) => {
    try {
      await resolveAlert(id);
      load();
    } catch (e) {
      console.error(e);
    }
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'low':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      default:
        return 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30';
    }
  };

  return (
    <div className="cyber-card rounded-xl border border-zinc-800 p-5">
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-zinc-800/80">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-lg bg-rose-500/10 border border-rose-500/20">
            <Radio className="w-4 h-4 text-rose-400 animate-pulse" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white">Live Alert & Event Stream</h2>
            <p className="text-xs text-zinc-500">Real-time telemetry and inter-module event bus feed</p>
          </div>
        </div>
        <span className="text-xs font-mono text-cyan-400 bg-cyan-950/40 px-2.5 py-1 rounded border border-cyan-800/50">
          {data.alerts.filter(a => !a.resolved).length} Unresolved
        </span>
      </div>

      <div className="space-y-3 max-h-[340px] overflow-y-auto pr-1">
        {data.alerts.length === 0 ? (
          <div className="text-center py-8 text-zinc-500 text-xs font-mono">
            No active alerts detected. All systems nominal.
          </div>
        ) : (
          data.alerts.map((alt) => (
            <div
              key={alt.id}
              className={`p-3.5 rounded-lg border transition-all ${
                alt.resolved
                  ? 'bg-zinc-900/30 border-zinc-800/40 opacity-60'
                  : 'bg-zinc-900/60 border-zinc-800 hover:border-zinc-700'
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded border ${getSeverityBadge(alt.severity)}`}>
                      {alt.severity}
                    </span>
                    {alt.module_id && (
                      <span className="text-xs font-mono text-zinc-400">[{alt.module_id}]</span>
                    )}
                    <h3 className="text-sm font-medium text-white">{alt.title}</h3>
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed font-mono">
                    {alt.description}
                  </p>
                  <p className="text-[11px] text-zinc-600 font-mono">
                    {alt.timestamp ? new Date(alt.timestamp).toLocaleTimeString() : 'Just now'}
                  </p>
                </div>

                {!alt.resolved && (
                  <button
                    onClick={() => handleResolve(alt.id)}
                    className="shrink-0 flex items-center gap-1 text-xs px-2.5 py-1.5 rounded bg-zinc-800 hover:bg-emerald-950/50 hover:text-emerald-400 hover:border-emerald-800 border border-zinc-700 text-zinc-300 transition-all font-medium"
                  >
                    <CheckCircle className="w-3.5 h-3.5" />
                    Resolve
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
