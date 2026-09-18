'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Play, Square, ExternalLink, ShieldCheck, ShieldAlert, Cpu } from 'lucide-react';
import { startModule, stopModule } from '@/lib/api';

interface ModuleCardProps {
  module: {
    id: string;
    name: string;
    display_name: string;
    category: string;
    version: string;
    status: string;
    permission_level: string;
    lab_only: boolean;
    is_loaded: boolean;
    runtime_status?: string;
  };
  onStateChange?: () => void;
}

export default function ModuleCard({ module, onStateChange }: ModuleCardProps) {
  const [loading, setLoading] = useState(false);

  const isRunning = module.runtime_status === 'running';
  const isLoaded = module.is_loaded;

  const handleToggle = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setLoading(true);
    try {
      if (isRunning) {
        await stopModule(module.id);
      } else {
        await startModule(module.id);
      }
      if (onStateChange) onStateChange();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = () => {
    if (isRunning) {
      return (
        <span className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          RUNNING
        </span>
      );
    }
    if (isLoaded) {
      return (
        <span className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
          READY
        </span>
      );
    }
    return (
      <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-zinc-800 text-zinc-500 border border-zinc-700">
        CONFIGURED
      </span>
    );
  };

  return (
    <div className="cyber-card rounded-xl p-5 border border-zinc-800 hover:border-zinc-700 transition-all flex flex-col justify-between group">
      <div>
        <div className="flex items-start justify-between gap-2 mb-3">
          <span className="text-[11px] font-mono text-cyan-400 uppercase tracking-wider bg-cyan-950/30 px-2 py-0.5 rounded border border-cyan-900/40">
            {module.id}
          </span>
          {getStatusBadge()}
        </div>

        <h3 className="text-base font-semibold text-white group-hover:text-cyan-300 transition-colors mb-1">
          {module.display_name}
        </h3>
        
        <p className="text-xs text-zinc-400 font-mono mb-4">
          Category: <span className="text-zinc-300">{module.category}</span>
        </p>
      </div>

      <div className="pt-4 border-t border-zinc-800/80 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-400 border border-zinc-700">
            {module.permission_level}
          </span>
          {module.lab_only && (
            <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
              LAB
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {isLoaded ? (
            <button
              onClick={handleToggle}
              disabled={loading}
              className={`p-2 rounded-lg border transition-all ${
                isRunning
                  ? 'bg-rose-500/10 border-rose-500/30 text-rose-400 hover:bg-rose-500/20'
                  : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20'
              }`}
              title={isRunning ? 'Stop Module' : 'Start Module'}
            >
              {isRunning ? <Square className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            </button>
          ) : null}

          <Link
            href={`/modules/${module.id}`}
            className="p-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-300 hover:text-white hover:border-zinc-600 transition-all"
            title="Inspect Module Details"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
