'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  fetchModules,
  fetchModuleStatus,
  fetchModuleResults,
  fetchModuleLogs,
  startModule,
  stopModule,
  reloadModule,
  generateModuleReport
} from '@/lib/api';
import {
  Play,
  Square,
  RefreshCw,
  FileText,
  Terminal,
  Activity,
  Settings,
  ArrowLeft,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';

export default function ModuleDetailPage() {
  const params = useParams();
  const router = useRouter();
  const moduleId = params.id as string;

  const [moduleData, setModuleData] = useState<any>(null);
  const [statusInfo, setStatusInfo] = useState<any>(null);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [report, setReport] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'results' | 'logs' | 'report' | 'config'>('results');
  const [loading, setLoading] = useState(true);
  const [actionMsg, setActionMsg] = useState<string>('');

  const loadAll = async () => {
    try {
      const allMods = await fetchModules();
      const current = allMods.find((m: any) => m.id === moduleId);
      setModuleData(current);

      if (current?.is_loaded) {
        const [stat, res, lg] = await Promise.all([
          fetchModuleStatus(moduleId).catch(() => null),
          fetchModuleResults(moduleId).catch(() => null),
          fetchModuleLogs(moduleId).catch(() => [])
        ]);
        setStatusInfo(stat);
        setResults(res);
        setLogs(lg);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
    const interval = setInterval(loadAll, 6000);
    return () => clearInterval(interval);
  }, [moduleId]);

  const handleStart = async () => {
    setActionMsg('Starting module...');
    try {
      await startModule(moduleId);
      setActionMsg('Module started successfully.');
      loadAll();
    } catch (e: any) {
      setActionMsg(`Start failed: ${e.message}`);
    }
  };

  const handleStop = async () => {
    setActionMsg('Stopping module...');
    try {
      await stopModule(moduleId);
      setActionMsg('Module stopped.');
      loadAll();
    } catch (e: any) {
      setActionMsg(`Stop failed: ${e.message}`);
    }
  };

  const handleReload = async () => {
    setActionMsg('Hot-reloading module in memory...');
    try {
      await reloadModule(moduleId);
      setActionMsg('Module hot-reloaded successfully.');
      loadAll();
    } catch (e: any) {
      setActionMsg(`Reload failed: ${e.message}`);
    }
  };

  const handleGenerateReport = async () => {
    setActionMsg('Generating module activity audit report...');
    try {
      const rep = await generateModuleReport(moduleId);
      setReport(rep);
      setActiveTab('report');
      setActionMsg('Report generated.');
    } catch (e: any) {
      setActionMsg(`Report generation failed: ${e.message}`);
    }
  };

  if (loading && !moduleData) {
    return (
      <div className="p-12 text-center text-zinc-400 font-mono text-sm">
        Initializing module control plane for {moduleId}...
      </div>
    );
  }

  if (!moduleData) {
    return (
      <div className="p-12 text-center space-y-4">
        <div className="text-rose-400 text-lg font-bold">Module {moduleId} Not Found</div>
        <Link href="/modules" className="text-cyan-400 underline text-sm">
          Return to Module Catalog
        </Link>
      </div>
    );
  }

  const isRunning = moduleData.runtime_status === 'running';

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Back button */}
      <div>
        <Link
          href="/modules"
          className="inline-flex items-center gap-1.5 text-xs font-mono text-zinc-400 hover:text-cyan-400 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Modules Catalog
        </Link>
      </div>

      {/* Header & Controls */}
      <div className="cyber-card p-6 rounded-xl border border-zinc-800 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-mono text-cyan-400 uppercase tracking-widest bg-cyan-950/40 px-2.5 py-0.5 rounded border border-cyan-800/50">
                {moduleData.id}
              </span>
              <span className="text-xs font-mono text-zinc-400 bg-zinc-800 px-2 py-0.5 rounded">
                {moduleData.category}
              </span>
              <span className="text-xs font-semibold uppercase px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">
                Role: {moduleData.permission_level}
              </span>
            </div>
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              {moduleData.display_name}
            </h1>
            <p className="text-xs text-zinc-400 mt-1 font-mono">
              Entry Point: <span className="text-zinc-300">{moduleData.entry_point}</span>
            </p>
          </div>

          {/* Module Action Buttons */}
          <div className="flex items-center gap-3">
            {moduleData.is_loaded ? (
              <>
                <button
                  onClick={isRunning ? handleStop : handleStart}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all shadow-md ${
                    isRunning
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-rose-500/30'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/30'
                  }`}
                >
                  {isRunning ? <Square className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                  <span>{isRunning ? 'Stop Module' : 'Start Module'}</span>
                </button>

                <button
                  onClick={handleReload}
                  className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 text-sm font-medium transition-all"
                  title="Hot-Reload without restarting platform"
                >
                  <RefreshCw className="w-4 h-4 text-cyan-400" />
                  <span>Hot Reload</span>
                </button>

                <button
                  onClick={handleGenerateReport}
                  className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 text-sm font-medium transition-all"
                >
                  <FileText className="w-4 h-4 text-violet-400" />
                  <span>Generate Report</span>
                </button>
              </>
            ) : (
              <div className="text-xs text-zinc-500 font-mono bg-zinc-900 px-3 py-2 rounded border border-zinc-800">
                Module configured for future release (Phase 8+)
              </div>
            )}
          </div>
        </div>

        {actionMsg && (
          <div className="text-xs font-mono px-3 py-2 rounded bg-cyan-950/30 text-cyan-400 border border-cyan-800/40">
            {actionMsg}
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex items-center gap-3 border-b border-zinc-800 pt-2">
          {[
            { id: 'results', name: 'Live Telemetry & Results', icon: Activity },
            { id: 'logs', name: 'Module Logs', icon: Terminal },
            { id: 'report', name: 'Structured Report', icon: FileText },
            { id: 'config', name: 'Configuration', icon: Settings },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 pb-3 px-2 text-xs font-semibold transition-all border-b-2 ${
                  activeTab === tab.id
                    ? 'border-cyan-400 text-cyan-400'
                    : 'border-transparent text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Contents */}
      <div className="cyber-card p-6 rounded-xl border border-zinc-800 min-h-[380px]">
        {activeTab === 'results' && (
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-white flex items-center justify-between">
              <span>Telemetry & Execution Output</span>
              <span className="text-xs font-mono text-zinc-500">Live polling: 6s</span>
            </h3>
            <pre className="p-4 bg-zinc-950/90 rounded-lg border border-zinc-800 text-xs font-mono text-emerald-400 overflow-x-auto max-h-[500px]">
              {JSON.stringify(results || statusInfo || { message: 'No execution output yet. Click Start to initialize.' }, null, 2)}
            </pre>
          </div>
        )}

        {activeTab === 'logs' && (
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-white">Module Log Stream</h3>
            <div className="p-4 bg-zinc-950/90 rounded-lg border border-zinc-800 font-mono text-xs space-y-1.5 max-h-[500px] overflow-y-auto">
              {logs.length === 0 ? (
                <div className="text-zinc-500 text-center py-6">No logs recorded for this module yet.</div>
              ) : (
                logs.map((lg, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <span className="text-zinc-600 shrink-0">[{lg.timestamp || 'LOG'}]</span>
                    <span className="text-cyan-400 font-bold uppercase shrink-0">[{lg.level || 'INFO'}]</span>
                    <span className="text-zinc-300">{lg.message}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'report' && (
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-white">Generated Structured Audit Report</h3>
            <pre className="p-4 bg-zinc-950/90 rounded-lg border border-zinc-800 text-xs font-mono text-cyan-300 overflow-x-auto max-h-[500px]">
              {JSON.stringify(report || { message: 'Click "Generate Report" above to compile an on-demand audit report.' }, null, 2)}
            </pre>
          </div>
        )}

        {activeTab === 'config' && (
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-white">Module Metadata & Configuration JSON</h3>
            <pre className="p-4 bg-zinc-950/90 rounded-lg border border-zinc-800 text-xs font-mono text-zinc-300 overflow-x-auto max-h-[500px]">
              {JSON.stringify(moduleData, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
