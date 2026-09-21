export interface Employee {
  id: string;
  name: string;
  email: string;
  department: string;
  job_title: string;
  country: string;
  currency: string;
  base_salary: string;
  bonus: string;
  joining_date: string;
  status: string;
}

export interface PageMeta {
  page: number;
  size: number;
  total: number;
}

export interface EmployeeList {
  data: Employee[];
  meta: PageMeta;
}

export interface AnalyticsSummary {
  headcount: number;
  total_usd: string;
  per_currency: Record<string, string>;
  avg_by_department: Record<string, string>;
  avg_by_country: Record<string, string>;
  top_earners: {
    id: string;
    name: string;
    department: string;
    country: string;
    base_salary: string;
    currency: string;
    usd_equivalent: string;
  }[];
  distribution: { label: string; count: number }[];
  rate_date: string | null;
}
