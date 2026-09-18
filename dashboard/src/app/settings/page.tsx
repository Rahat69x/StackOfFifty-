'use client';

import React, { useEffect, useState } from 'react';
import { fetchConfig } from '@/lib/api';
import { Settings, Save, CheckCircle, RefreshCw } from 'lucide-react';

export default function SettingsPage() {
  const [config, setConfig] = useState<any>(null);
  const [jsonText, setJsonText] = useState<string>('');
  const [statusMsg, setStatusMsg] = useState<string>('');
  const [loading, setLoading] = useState(true);

  const loadConfig = async () => {
    try {
      const data = await fetchConfig();
      setConfig(data);
      setJsonText(JSON.stringify(data, null, 2));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  const handleSave = async () => {
    try {
      const parsed = JSON.parse(jsonText);
      const res = await fetch('/api/config/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(parsed)
      });
      if (!res.ok) throw new Error('Update failed');
      setStatusMsg('Configuration saved and active across the platform.');
      setTimeout(() => setStatusMsg(''), 4000);
    } catch (e: any) {
      setStatusMsg(`Error saving config: ${e.message}`);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Settings className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono uppercase tracking-widest text-cyan-400 font-semibold">
              Master Runtime Configuration
            </span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Platform Settings (Zero-Code)</h1>
          <p className="text-xs text-zinc-400 mt-0.5">
            Modify any platform setting, feature flag, or module metadata live via platform.config.json
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadConfig}
            className="p-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 text-xs font-mono"
            title="Reload from disk"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold font-mono transition-all shadow-md shadow-cyan-600/20"
          >
            <Save className="w-4 h-4" />
            <span>Save & Hot-Apply</span>
          </button>
        </div>
      </div>

      {statusMsg && (
        <div className="p-3 rounded-lg bg-cyan-950/40 text-cyan-400 border border-cyan-800/50 font-mono text-xs flex items-center gap-2">
          <CheckCircle className="w-4 h-4" />
          <span>{statusMsg}</span>
        </div>
      )}

      {/* Editor Box */}
      <div className="cyber-card p-6 rounded-xl border border-zinc-800 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono text-zinc-400">Editing: platform.config.json</span>
          <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
            Runtime Updates Enabled
          </span>
        </div>

        <textarea
          rows={22}
          value={jsonText}
          onChange={(e) => setJsonText(e.target.value)}
          className="w-full p-4 bg-zinc-950/90 rounded-lg border border-zinc-800 text-xs font-mono text-cyan-300 focus:outline-none focus:border-cyan-500 transition-colors leading-relaxed"
          spellCheck={false}
        />

        <p className="text-xs text-zinc-500 font-mono">
          Note: Changes are validated against the schema. Sensitive passwords remain masked.
        </p>
      </div>
    </div>
  );
}
