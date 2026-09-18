'use client';

import React, { useEffect, useState } from 'react';
import { fetchModules, generateModuleReport } from '@/lib/api';
import { FileText, Download, CheckCircle, Clock } from 'lucide-react';

export default function ReportsPage() {
  const [modules, setModules] = useState<any[]>([]);
  const [selectedModule, setSelectedModule] = useState<string>('mod_001');
  const [currentReport, setCurrentReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchModules()
      .then((mods) => {
        const loaded = mods.filter((m: any) => m.is_loaded);
        setModules(loaded);
        if (loaded.length > 0) setSelectedModule(loaded[0].id);
      })
      .catch(console.error);
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const rep = await generateModuleReport(selectedModule);
      setCurrentReport(rep);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <FileText className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono uppercase tracking-widest text-cyan-400 font-semibold">
              Compliance & Audit Reports
            </span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Structured Security Reports</h1>
          <p className="text-xs text-zinc-400 mt-0.5">
            Compile real-time module status, execution metrics, and telemetry audit ledgers
          </p>
        </div>

        {/* Generate Selector */}
        <div className="flex items-center gap-3">
          <select
            value={selectedModule}
            onChange={(e) => setSelectedModule(e.target.value)}
            className="px-3 py-2 bg-zinc-900 border border-zinc-800 rounded-lg text-xs font-mono text-white focus:outline-none focus:border-cyan-500"
          >
            {modules.map((m) => (
              <option key={m.id} value={m.id}>
                {m.display_name} ({m.id})
              </option>
            ))}
          </select>
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold font-mono transition-all shadow-md shadow-cyan-600/20"
          >
            {loading ? 'Compiling...' : 'Generate Live Report'}
          </button>
        </div>
      </div>

      {/* Report Viewer */}
      <div className="cyber-card p-6 rounded-xl border border-zinc-800 min-h-[450px]">
        {currentReport ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-400" />
                <span className="text-sm font-semibold text-white">Report Compiled Successfully</span>
              </div>
              <span className="text-xs font-mono text-zinc-500">
                Timestamp: {new Date().toLocaleTimeString()}
              </span>
            </div>
            <pre className="p-4 bg-zinc-950/90 rounded-lg border border-zinc-800 text-xs font-mono text-cyan-300 overflow-x-auto max-h-[550px]">
              {JSON.stringify(currentReport, null, 2)}
            </pre>
          </div>
        ) : (
          <div className="text-center py-24 space-y-3">
            <Clock className="w-8 h-8 text-zinc-600 mx-auto" />
            <h3 className="text-sm font-medium text-zinc-400">No report currently compiled</h3>
            <p className="text-xs text-zinc-600 max-w-sm mx-auto">
              Select an active module from the dropdown above and click &quot;Generate Live Report&quot; to compile a fresh telemetry audit.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
