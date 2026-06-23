const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export interface DashboardParams {
  startDate?: string;
  endDate?: string;
  department?: string;
}

export interface OverviewData {
  dailyOutpatient: number;
  totalRevenue: number;
  inHospital: number;
  outpatientChange: number;
  revenueChange: number;
}

export interface TrendData {
  dates: string[];
  outpatientCounts: number[];
  revenues: number[];
}

export interface DepartmentData {
  name: string;
  outpatientCount: number;
  revenue: number;
}

export interface DashboardResponse {
  overview: OverviewData;
  trends: TrendData;
  departments: DepartmentData[];
}

export interface AIQueryResponse {
  sql: string;
  result: Record<string, any>[];
  chartType: 'line' | 'bar' | 'pie';
  explanation: string;
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
}

export const api = {
  getDashboard: (params?: DashboardParams): Promise<DashboardResponse> => {
    const query = new URLSearchParams();
    if (params?.startDate) query.append('startDate', params.startDate);
    if (params?.endDate) query.append('endDate', params.endDate);
    if (params?.department) query.append('department', params.department);
    const queryStr = query.toString();
    return request<DashboardResponse>(`/dashboard${queryStr ? `?${queryStr}` : ''}`);
  },

  aiQuery: (question: string): Promise<AIQueryResponse> => {
    return request<AIQueryResponse>('/ai-query', {
      method: 'POST',
      body: JSON.stringify({ question }),
    });
  },

  getExportUrl: (type: string, params?: DashboardParams): string => {
    const query = new URLSearchParams();
    query.append('type', type);
    if (params?.startDate) query.append('startDate', params.startDate);
    if (params?.endDate) query.append('endDate', params.endDate);
    return `${API_BASE}/export?${query.toString()}`;
  },
};
