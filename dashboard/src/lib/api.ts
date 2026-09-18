/**
 * Client-side API client for AegisCore backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/api/health`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch health');
  return res.json();
}

export async function fetchModules(category?: string, query?: string) {
  let url = `${API_BASE}/api/modules`;
  const params = new URLSearchParams();
  if (category && category !== 'All') params.append('category', category);
  if (query) params.append('q', query);
  if (params.toString()) url += `?${params.toString()}`;

  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch modules');
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/api/modules/categories`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function startModule(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/start`, { method: 'POST' });
  return res.json();
}

export async function stopModule(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/stop`, { method: 'POST' });
  return res.json();
}

export async function reloadModule(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/reload`, { method: 'POST' });
  return res.json();
}

export async function fetchModuleStatus(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/status`, { cache: 'no-store' });
  return res.json();
}

export async function fetchModuleResults(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/results`, { cache: 'no-store' });
  return res.json();
}

export async function fetchModuleLogs(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/logs`, { cache: 'no-store' });
  return res.json();
}

export async function generateModuleReport(moduleId: string) {
  const res = await fetch(`${API_BASE}/api/modules/${moduleId}/report`, { cache: 'no-store' });
  return res.json();
}

export async function fetchAlerts() {
  const res = await fetch(`${API_BASE}/api/alerts`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch alerts');
  return res.json();
}

export async function resolveAlert(alertId: string) {
  const res = await fetch(`${API_BASE}/api/alerts/${alertId}/resolve`, { method: 'POST' });
  return res.json();
}

export async function fetchLogs(level?: string, search?: string) {
  let url = `${API_BASE}/api/logs`;
  const params = new URLSearchParams();
  if (level && level !== 'ALL') params.append('level', level);
  if (search) params.append('search', search);
  if (params.toString()) url += `?${params.toString()}`;

  const res = await fetch(url, { cache: 'no-store' });
  return res.json();
}

export async function fetchConfig() {
  const res = await fetch(`${API_BASE}/api/config`, { cache: 'no-store' });
  return res.json();
}
