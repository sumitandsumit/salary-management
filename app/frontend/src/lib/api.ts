// Typed API client. Base URL from VITE_API_URL (default localhost).

import type { AnalyticsSummary, Employee, EmployeeList, Rate } from './types';

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new ApiError(res.status, body || res.statusText);
  }
  return res.json() as Promise<T>;
}

export interface EmployeeQuery {
  search?: string;
  dept?: string;
  country?: string;
  status?: string;
  sort?: string;
  page?: number;
  size?: number;
}

export function listEmployees(q: EmployeeQuery): Promise<EmployeeList> {
  const params = new URLSearchParams();
  for (const [k, v] of Object.entries(q)) {
    if (v !== undefined && v !== '') params.set(k, String(v));
  }
  return request<EmployeeList>(`/employees?${params.toString()}`);
}

export function createEmployee(payload: Partial<Employee>) {
  return request<Employee>('/employees', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateEmployee(id: string, payload: Partial<Employee>) {
  return request<Employee>(`/employees/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export function incrementSalary(id: string, percent: number, reason: string) {
  return request<Employee>(`/employees/${id}/increment`, {
    method: 'POST',
    body: JSON.stringify({ percent, reason }),
  });
}

export function deactivateEmployee(id: string) {
  return request<Employee>(`/employees/${id}/deactivate`, { method: 'POST' });
}

export function fetchSummary(q: { dept?: string; country?: string } = {}) {
  const params = new URLSearchParams();
  if (q.dept) params.set('dept', q.dept);
  if (q.country) params.set('country', q.country);
  const suffix = params.toString() ? `?${params.toString()}` : '';
  return request<AnalyticsSummary>(`/analytics/summary${suffix}`);
}

export function listRates(): Promise<Rate[]> {
  return request<Rate[]>('/rates');
}

export function updateRate(code: string, rate_to_usd: number, effective_date: string, reason?: string) {
  return request<Rate>(`/rates/${code}`, {
    method: 'PUT',
    body: JSON.stringify({ rate_to_usd, effective_date, reason }),
  });
}
