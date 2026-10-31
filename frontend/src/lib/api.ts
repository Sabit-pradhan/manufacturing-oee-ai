
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function apiGet<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API Error ${response.status}: ${message}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  health: () =>
    apiGet("/health"),

  shiftOee: (shiftId: string) =>
    apiGet(`/api/v1/oee/shift/${encodeURIComponent(shiftId)}`),

  dailyOee: (reportDate: string) =>
    apiGet(`/api/v1/oee/daily/${encodeURIComponent(reportDate)}`),

  oeeTrend: (startDate: string, endDate: string) =>
    apiGet(
      `/api/v1/oee/trend?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`
    ),

  anomalySummary: () =>
    apiGet("/api/v1/anomalies/summary"),

  machineAnomalies: (machineId: string) =>
    apiGet(`/api/v1/anomalies/machine/${encodeURIComponent(machineId)}`),

  dataQuality: () =>
    apiGet("/api/v1/anomalies/data-quality"),
};
