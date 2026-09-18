'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  ShieldAlert, 
  Layers, 
  Terminal, 
  AlertTriangle, 
  FileText, 
  Settings, 
  Activity,
  Cpu
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Overview', href: '/', icon: Activity },
  { name: 'Modules (50)', href: '/modules', icon: Layers },
  { name: 'Alert Stream', href: '/alerts', icon: AlertTriangle },
  { name: 'Log Inspector', href: '/logs', icon: Terminal },
  { name: 'Audit Reports', href: '/reports', icon: FileText },
  { name: 'Configuration', href: '/settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-zinc-950/95 border-r border-zinc-800/80 flex flex-col h-screen sticky top-0 select-none z-30">
      {/* Brand Header */}
      <div className="p-6 border-b border-zinc-800/80 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-emerald-500 p-0.5 flex items-center justify-center shadow-lg shadow-cyan-500/20">
          <div className="w-full h-full bg-zinc-950 rounded-[10px] flex items-center justify-center">
            <ShieldAlert className="w-5 h-5 text-cyan-400" />
          </div>
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
            StackOfFifty
            <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded">
              DEFENSE
            </span>
          </h1>
          <p className="text-xs text-zinc-500">SecOps & Telemetry</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-wider text-zinc-500">
          Platform Operations
        </div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-cyan-950/40 text-cyan-400 border border-cyan-800/50 shadow-sm shadow-cyan-900/30'
                  : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/60'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-zinc-500'}`} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Live System Badge */}
      <div className="p-4 border-t border-zinc-800/80 bg-zinc-900/40">
        <div className="flex items-center justify-between text-xs mb-2">
          <span className="text-zinc-400 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            Control Layer
          </span>
          <span className="text-emerald-400 font-mono text-[11px]">ONLINE</span>
        </div>
        <div className="text-[11px] text-zinc-500 font-mono flex items-center justify-between">
          <span>FastAPI + SQLite/PG</span>
          <span>v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
