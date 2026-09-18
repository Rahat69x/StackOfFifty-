'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import SystemHealth from '@/components/SystemHealth';
import AlertFeed from '@/components/AlertFeed';
import ModuleCard from '@/components/ModuleCard';
import { fetchModules } from '@/lib/api';
import { ArrowRight, Layers, ShieldCheck, Terminal, PlayCircle } from 'lucide-react';

export default function OverviewPage() {
  const [modules, setModules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const data = await fetchModules();
      setModules(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const activeModules = modules.filter((m) => m.is_loaded);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold">
              Security Operations Center
            </span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            AegisCore Platform
          </h1>
          <p className="text-sm text-zinc-400 mt-1">
            Modular Cybersecurity Defense & Operations Framework — Phase 1 Active
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/modules"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-medium shadow-lg shadow-cyan-600/20 transition-all"
          >
            <Layers className="w-4 h-4" />
            <span>Explore All 50 Modules</span>
          </Link>
          <Link
            href="/logs"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-sm font-medium border border-zinc-700 transition-all"
          >
            <Terminal className="w-4 h-4" />
            <span>Live Logs</span>
          </Link>
        </div>
      </div>

      {/* System Hardware & Posture Meters */}
      <section>
        <SystemHealth />
      </section>

      {/* Grid: Alert Feed + Telemetry Stream */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AlertFeed />
        </div>

        {/* Operational Security Posture Card */}
        <div className="cyber-card rounded-xl border border-zinc-800 p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 pb-4 mb-4 border-b border-zinc-800/80">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <h2 className="text-sm font-semibold text-white">Platform Defensive Posture</h2>
            </div>
            <div className="space-y-4">
              <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800">
                <div className="text-xs text-zinc-400 mb-1">Active Defense Stance</div>
                <div className="text-sm font-bold text-emerald-400">Strictly Defensive</div>
                <p className="text-[11px] text-zinc-500 mt-1">Zero offensive payloads or weaponized exploit logic loaded.</p>
              </div>

              <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800">
                <div className="text-xs text-zinc-400 mb-1">Access Control & Security</div>
                <div className="text-sm font-bold text-cyan-400">RBAC Enforcement Active</div>
                <p className="text-[11px] text-zinc-500 mt-1">Role validation enabled (admin / researcher / viewer).</p>
              </div>

              <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800">
                <div className="text-xs text-zinc-400 mb-1">Decoy & Sensor Grid</div>
                <div className="text-sm font-bold text-violet-400">5 Starter Modules Running</div>
                <p className="text-[11px] text-zinc-500 mt-1">Honeypot, Traffic Analyzer, Crypto, Firewall, MFA Guard.</p>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-zinc-800/80">
            <Link 
              href="/modules"
              className="flex items-center justify-between text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              <span>Manage all module lifecycles</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Active Starter Modules Grid */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white">Active Defensive Modules (Phase 1)</h2>
            <p className="text-xs text-zinc-400">Currently initialized and testable in the runtime registry</p>
          </div>
          <Link
            href="/modules"
            className="text-xs text-cyan-400 hover:underline flex items-center gap-1 font-mono"
          >
            View all 50 catalog entries &rarr;
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {activeModules.map((mod) => (
            <ModuleCard key={mod.id} module={mod} onStateChange={loadData} />
          ))}
        </div>
      </section>
    </div>
  );
}
