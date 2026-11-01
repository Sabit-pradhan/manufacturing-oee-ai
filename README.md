"use client";

import { useEffect, useState } from "react";
import CopilotChat from "@/components/CopilotChat";
import { api } from "@/lib/api";
import {
  Activity, AlertTriangle, BarChart3, Bell, Boxes, CheckCircle2,
  ChevronDown, CircleGauge, Cog, Database, Factory, FileText,
  Gauge, Home, Menu, Package, ShieldCheck, Wrench, Zap,
  Droplets, Wind, X, ArrowUpRight, Cpu, Search, Settings,
} from "lucide-react";

import {
  Area, AreaChart, CartesianGrid, Line, LineChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";

const productionData = [
  { time: "00:00", production: 650 },
  { time: "02:00", production: 820 },
  { time: "04:00", production: 740 },
  { time: "06:00", production: 1050 },
  { time: "08:00", production: 980 },
  { time: "10:00", production: 1250 },
  { time: "12:00", production: 1100 },
  { time: "14:00", production: 1450 },
  { time: "16:00", production: 1320 },
  { time: "18:00", production: 1600 },
  { time: "20:00", production: 1480 },
];

const energyData = [
  { time: "00:00", energy: 500 },
  { time: "04:00", energy: 850 },
  { time: "08:00", energy: 720 },
  { time: "10:00", energy: 1100 },
  { time: "12:00", energy: 950 },
  { time: "14:00", energy: 1450 },
  { time: "16:00", energy: 1200 },
  { time: "18:00", energy: 1700 },
  { time: "20:00", energy: 1600 },
];

const temperatureData = [
  { time: "00:00", mixer: 90, reactor: 70, separator: 120 },
  { time: "04:00", mixer: 95, reactor: 75, separator: 130 },
  { time: "08:00", mixer: 100, reactor: 82, separator: 125 },
  { time: "12:00", mixer: 110, reactor: 88, separator: 145 },
  { time: "16:00", mixer: 105, reactor: 92, separator: 150 },
  { time: "20:00", mixer: 120, reactor: 95, separator: 160 },
];

const alarms = [
  { time: "14:32", message: "High Motor Temperature - Line 2", level: "CRITICAL" },
  { time: "13:24", message: "Pressure Drop - Pump 3", level: "WARNING" },
  { time: "11:18", message: "Maintenance Reminder - M013", level: "INFO" },
];

const navigation = [
  { name: "Overview", icon: Home },
  { name: "Production", icon: Factory },
  { name: "Machines", icon: Cog },
  { name: "Anomalies", icon: AlertTriangle, count: 3 },
  { name: "Data Quality", icon: Database, count: 2 },
  { name: "Analytics", icon: BarChart3 },
  { name: "Maintenance", icon: Wrench },
  { name: "Reports", icon: FileText },
];

function Panel({
  title,
  children,
  className = "",
  action,
}: {
  title: string;
  children: React.ReactNode;
  className?: string;
  action?: React.ReactNode;
}) {
  return (
    <section className={`panel min-w-0 p-4 ${className}`}>
      <div className="mb-4 flex items-center justify-between gap-2">
        <h2 className="panel-title">{title}</h2>
        {action}
      </div>
      {children}
    </section>
  );
}

function KpiCard({
  title,
  value,
  subtitle,
  icon: Icon,
  color,
}: {
  title: string;
  value: string;
  subtitle: string;
  icon: React.ElementType;
  color: string;
}) {
  return (
    <div className="kpi-card group p-4">
      <div className="flex items-center justify-between gap-2">
        <p className="text-[10px] font-bold uppercase tracking-[.13em] text-slate-400">
          {title}
        </p>
        <div
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl"
          style={{ color, background: `${color}18` }}
        >
          <Icon size={21} />
        </div>
      </div>

      <p className="mt-3 text-2xl font-bold tracking-tight text-white sm:text-3xl">
        {value}
      </p>

      <div className="mt-2 flex items-center gap-1 text-[10px] font-semibold text-emerald-400">
        <ArrowUpRight size={13} />
        {subtitle}
      </div>

      <div
        className="absolute bottom-0 left-0 h-[2px] w-full opacity-70"
        style={{ background: `linear-gradient(90deg, ${color}, transparent)` }}
      />
    </div>
  );
}

function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded-lg border border-cyan-900 bg-slate-950 p-3 text-xs shadow-xl">
      <p className="mb-2 text-slate-300">{label}</p>

      {payload.map((item: any) => (
        <p key={item.dataKey} style={{ color: item.color }}>
          {item.name || item.dataKey}: {item.value}
        </p>
      ))}
    </div>
  );
}

function ProcessDiagram() {
  const stages = [
    { name: "RAW MATERIAL", detail: ["Level", "82%", "Temp", "24.1°C"], icon: Boxes, value: "INPUT" },
    { name: "MIXING TANK", detail: ["Speed", "120 RPM", "Temp", "65.4°C"], icon: Cog, value: "MIXING" },
    { name: "REACTOR", detail: ["Temp", "124.3°C", "Pressure", "2.1 bar"], icon: Factory, value: "PROCESS" },
    { name: "SEPARATOR", detail: ["Speed", "980 RPM", "Temp", "52.1°C"], icon: Activity, value: "FILTER" },
    { name: "PACKAGING", detail: ["Speed", "60 PPM", "Output", "1,248"], icon: Package, value: "OUTPUT" },
  ];

  return (
    <div className="grid-bg overflow-hidden rounded-xl border border-cyan-900/70 p-3 sm:p-4">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2 text-[10px] text-slate-400">
          <span className="status-dot live-pulse" />
          PRODUCTION LINE 01
        </div>

        <span className="rounded-full border border-emerald-800/70 bg-emerald-950/40 px-3 py-1 text-[9px] font-bold text-emerald-400">
          PROCESS ACTIVE
        </span>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5">
        {stages.map((stage, index) => {
          const Icon = stage.icon;

          return (
            <div key={stage.name} className="relative min-w-0">
              <div className="h-full rounded-xl border border-cyan-800/70 bg-[#071521]/95 p-3 transition duration-200 hover:-translate-y-1 hover:border-cyan-400/80 hover:shadow-[0_0_20px_rgba(34,211,238,.09)]">
                <div className="mb-3 flex items-center justify-between gap-1">
                  <span className="text-[9px] font-bold tracking-wide text-cyan-200">
                    {stage.name}
                  </span>
                  <span className="text-[8px] text-slate-600">
                    0{index + 1}
                  </span>
                </div>

                <div className="space-y-2">
                  {[0, 1].map((i) => (
                    <div key={i} className="flex justify-between gap-2 text-[10px]">
                      <span className="text-slate-500">
                        {stage.detail[i * 2]}
                      </span>
                      <span className="font-semibold text-emerald-300">
                        {stage.detail[i * 2 + 1]}
                      </span>
                    </div>
                  ))}
                </div>

                <div className="my-4 flex items-center justify-center">
                  <div className="relative flex h-[76px] w-[76px] items-center justify-center rounded-2xl border border-cyan-500/50 bg-gradient-to-br from-cyan-900/50 to-slate-950 shadow-[0_0_22px_rgba(34,211,238,.12)]">
                    <Icon size={32} className="text-cyan-300" />
                    <span className="absolute -right-1 -top-1 h-3 w-3 rounded-full border-2 border-[#071521] bg-emerald-400 shadow-[0_0_8px_#00e6a0]" />
                  </div>
                </div>

                <div className="flex items-center justify-between border-t border-cyan-950 pt-2">
                  <span className="text-[8px] tracking-widest text-slate-500">
                    {stage.value}
                  </span>
                  <span className="text-[9px] font-bold text-emerald-400">
                    ACTIVE
                  </span>
                </div>
              </div>

              {index < stages.length - 1 && (
                <div className="process-pipe absolute -right-3 top-1/2 z-10 hidden w-3 xl:block" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

interface MachineOee {
  machine_id: string;
  availability: number;
  performance: number;
  quality: number;
  oee: number;
  downtime_sec: number;
}

interface DailyOee {
  machine_id: string;
  total_count: number;
  good_count: number;
  availability: number;
  performance: number;
  quality: number;
  oee: number;
}

interface OeeTrend {
  date: string;
  machine_count: number;
  average_availability: number;
  average_performance: number;
  average_quality: number;
  average_oee: number;
  total_production: number;
  total_good_production: number;
}

function MachineCard({ machine }: { machine: MachineOee }) {
  const color =
    machine.oee < 50
      ? "#ff5266"
      : machine.oee < 75
        ? "#ffbd35"
        : "#00e6a0";

  return (
    <div className="machine-card p-4">
      <div className="flex items-center justify-between gap-2">
        <div className="flex min-w-0 items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-cyan-300">
            <Cog size={23} />
          </div>

          <div className="min-w-0">
            <p className="truncate text-xs font-bold text-white">
              {machine.machine_id}
            </p>
            <p className="mt-1 text-[9px] text-slate-500">
              Shift OEE metrics
            </p>
          </div>
        </div>

        <span
          className="shrink-0 rounded-full px-2 py-1 text-[8px] font-bold"
          style={{ color, background: `${color}18` }}
        >
          {machine.oee < 50
            ? "LOW OEE"
            : machine.oee < 75
              ? "MODERATE"
              : "GOOD OEE"}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 text-[10px]">
        <div>
          <p className="text-slate-500">OEE</p>
          <p className="mt-1 font-bold text-emerald-300">
            {machine.oee.toFixed(1)}%
          </p>
        </div>

        <div>
          <p className="text-slate-500">Availability</p>
          <p className="mt-1 font-bold text-white">
            {machine.availability.toFixed(1)}%
          </p>
        </div>

        <div>
          <p className="text-slate-500">Downtime</p>
          <p className="mt-1 font-bold text-white">
            {Math.round(machine.downtime_sec / 60)} min
          </p>
        </div>
      </div>

      <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full"
          style={{
            width: `${Math.max(0, Math.min(machine.oee, 100))}%`,
            background: color,
          }}
        />
      </div>
    </div>
  );
}

interface AnomalySummary {
  detection_type: string;
  total_anomalies: number;
  severity_distribution: {
    High: number;
    Medium: number;
    Low: number;
  };
  anomalies: unknown[];
}

export default function DashboardPage() {
  const [activePage, setActivePage] = useState("Overview");
  const [shift, setShift] = useState("A");
  const [plant, setPlant] = useState("Unit 1");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showAlarms, setShowAlarms] = useState(false);

  const [anomalySummary, setAnomalySummary] =
    useState<AnomalySummary | null>(null);
  const [anomalyError, setAnomalyError] = useState("");

  const [machineOee, setMachineOee] = useState<MachineOee[]>([]);
  const [oeeError, setOeeError] = useState("");
  const [oeeLoading, setOeeLoading] = useState(true);

  // Daily OEE state
  const [selectedDate, setSelectedDate] = useState("2026-01-01");
  const [dailyOee, setDailyOee] = useState<DailyOee[]>([]);
  const [dailyLoading, setDailyLoading] = useState(true);
  const [dailyError, setDailyError] = useState("");

  // Seven-day trend state
  const [oeeTrend, setOeeTrend] = useState<OeeTrend[]>([]);
  const [trendLoading, setTrendLoading] = useState(true);
  const [trendError, setTrendError] = useState("");

  // Load anomaly summary
  useEffect(() => {
    let isMounted = true;

    async function loadAnomalySummary() {
      try {
        const result = await api.anomalySummary();

        if (isMounted) {
          setAnomalySummary(result as AnomalySummary);
          setAnomalyError("");
        }
      } catch (error) {
        if (isMounted) {
          setAnomalyError(
            error instanceof Error
              ? error.message
              : "Unable to load anomaly data"
          );
        }
      }
    }

    loadAnomalySummary();

    return () => {
      isMounted = false;
    };
  }, []);

  // Load shift-based machine OEE
  useEffect(() => {
    let isMounted = true;

    async function loadShiftOee() {
      setOeeLoading(true);

      try {
        // This date matches the shift endpoint verified in the backend.
        const result = await api.shiftOee(`20260101_${shift}`);
        const response = result as { data: MachineOee[] };

        if (!Array.isArray(response.data)) {
          throw new Error("Unexpected OEE API response format");
        }

        if (isMounted) {
          setMachineOee(response.data);
          setOeeError("");
        }
      } catch (error) {
        if (isMounted) {
          setOeeError(
            error instanceof Error
              ? error.message
              : "Unable to load OEE data"
          );
        }
      } finally {
        if (isMounted) {
          setOeeLoading(false);
        }
      }
    }

    loadShiftOee();

    return () => {
      isMounted = false;
    };
  }, [shift]);

  // Load daily OEE for the selected date
  useEffect(() => {
    let isMounted = true;

    async function loadDailyOee() {
      setDailyLoading(true);
      setDailyError("");

      try {
        const result = await api.dailyOee(selectedDate);
        const response = result as { data: DailyOee[] };

        if (!Array.isArray(response.data)) {
          throw new Error("Unexpected daily OEE API response format");
        }

        if (isMounted) {
          setDailyOee(response.data);
        }
      } catch (error) {
        if (isMounted) {
          setDailyOee([]);
          setDailyError(
            error instanceof Error
              ? error.message
              : "Unable to load daily OEE"
          );
        }
      } finally {
        if (isMounted) {
          setDailyLoading(false);
        }
      }
    }

    loadDailyOee();

    return () => {
      isMounted = false;
    };
  }, [selectedDate]);

  // Load seven-day OEE trend starting from the selected date
  useEffect(() => {
    let isMounted = true;

    async function loadOeeTrend() {
      setTrendLoading(true);
      setTrendError("");

      try {
        const start = new Date(`${selectedDate}T00:00:00`);
        const end = new Date(start);
        end.setDate(end.getDate() + 6);

        const formatDate = (date: Date) => {
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, "0");
          const day = String(date.getDate()).padStart(2, "0");

          return `${year}-${month}-${day}`;
        };

        const result = await api.oeeTrend(
          formatDate(start),
          formatDate(end)
        );

        const response = result as { data: OeeTrend[] };

        if (!Array.isArray(response.data)) {
          throw new Error("Unexpected OEE trend API response format");
        }

        if (isMounted) {
          setOeeTrend(response.data);
        }
      } catch (error) {
        if (isMounted) {
          setOeeTrend([]);
          setTrendError(
            error instanceof Error
              ? error.message
              : "Unable to load OEE trend"
          );
        }
      } finally {
        if (isMounted) {
          setTrendLoading(false);
        }
      }
    }

    loadOeeTrend();

    return () => {
      isMounted = false;
    };
  }, [selectedDate]);

  // Calculate shift-based average metrics
  const averageMetric = (
    key: "oee" | "availability" | "performance" | "quality"
  ) =>
    machineOee.length
      ? machineOee.reduce(
          (sum, machine) => sum + Number(machine[key] || 0),
          0
        ) / machineOee.length
      : null;

  // Calculate daily average metrics across reporting machines
  const averageDailyMetric = (
    key: "oee" | "availability" | "performance" | "quality"
  ) =>
    dailyOee.length
      ? dailyOee.reduce(
          (sum, machine) => sum + Number(machine[key] || 0),
          0
        ) / dailyOee.length
      : null;

  const averageOee = averageDailyMetric("oee");
  const averageAvailability = averageDailyMetric("availability");
  const averagePerformance = averageDailyMetric("performance");
  const averageQuality = averageDailyMetric("quality");

  // Machine chart continues to use the selected shift
  const machineOeeChartData = machineOee.map((machine) => ({
    machine: machine.machine_id,
    oee: machine.oee,
    availability: machine.availability,
    performance: machine.performance,
  }));

  return (
    <main className="dashboard-bg min-h-screen">
      {/* HEADER */}
      <header className="sticky top-0 z-40 flex min-h-[68px] items-center justify-between gap-3 border-b border-cyan-900/60 bg-[#07131e]/95 px-4 py-3 backdrop-blur-xl lg:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <button
            className="rounded-lg p-2 text-slate-300 hover:bg-cyan-950 lg:hidden"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle navigation"
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-cyan-700/50 bg-cyan-950/70 text-cyan-300 shadow-[0_0_18px_rgba(34,211,238,.12)]">
            <Factory size={24} />
          </div>

          <div className="min-w-0">
            <h1 className="text-lg font-black tracking-[.15em] text-white sm:text-xl">
              YOTTAFLEX
            </h1>
            <p className="text-[8px] tracking-[.17em] text-slate-400">
              MANUFACTURING INTELLIGENCE
            </p>
          </div>
        </div>

        <div className="hidden text-center md:block">
          <h2 className="text-sm font-bold tracking-[.16em] text-white">
            PLANT OVERVIEW
          </h2>
          <p className="mt-1 text-[9px] text-slate-500">
            Real-Time Monitoring & Control
          </p>
        </div>

        <div className="flex shrink-0 items-center gap-2 sm:gap-3">
          <div className="hidden text-right xl:block">
            <p className="text-[11px] font-semibold text-slate-300">
              OCT 31, 2026
            </p>
            <p className="text-[9px] text-slate-500">
              Dashboard preview
            </p>
          </div>

          <div className="hidden items-center gap-2 sm:flex">
            <span className="status-dot live-pulse" />

            <div>
              <p
                className={`text-[10px] font-bold tracking-wide ${
                  oeeError ? "text-red-400" : "text-emerald-400"
                }`}
              >
                {oeeError
                  ? "API ERROR"
                  : oeeLoading
                    ? "CONNECTING"
                    : "API CONNECTED"}
              </p>

              <p className="text-[8px] text-slate-500">
                {oeeError ? "OEE unavailable" : "FastAPI · Shift metrics"}
              </p>
            </div>
          </div>

          <select
            value={shift}
            onChange={(e) => setShift(e.target.value)}
            className="rounded-lg border border-cyan-900 bg-slate-900 px-2 py-2 text-[10px] text-white outline-none focus:border-cyan-400"
          >
            <option value="A">Shift A</option>
            <option value="B">Shift B</option>
            <option value="C">Shift C</option>
          </select>

          <select
            value={plant}
            onChange={(e) => setPlant(e.target.value)}
            className="hidden rounded-lg border border-cyan-900 bg-slate-900 px-2 py-2 text-[10px] text-white outline-none sm:block"
          >
            <option>Unit 1</option>
            <option>Unit 2</option>
            <option>Unit 3</option>
          </select>

          <button
            className="relative rounded-lg p-2 text-slate-300 hover:bg-cyan-950"
            aria-label="Notifications"
          >
            <Bell size={18} />
            <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500" />
          </button>
        </div>
      </header>

      <div className="flex min-h-[calc(100vh-68px)]">
        {/* SIDEBAR */}
        {sidebarOpen && (
          <button
            aria-label="Close navigation overlay"
            className="fixed inset-0 top-[68px] z-20 bg-black/60 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        <aside
          className={`${
            sidebarOpen
              ? "fixed left-0 top-[68px] z-30 flex h-[calc(100vh-68px)]"
              : "hidden"
          } w-[230px] shrink-0 flex-col border-r border-cyan-900/50 bg-[#07141f] lg:sticky lg:top-[68px] lg:flex lg:h-[calc(100vh-68px)]`}
        >
          <div className="flex-1 overflow-y-auto py-5">
            <p className="px-5 pb-4 text-[9px] font-bold tracking-[.2em] text-slate-600">
              MAIN NAVIGATION
            </p>

            <nav className="flex flex-col gap-1 px-2">
              {navigation.map((item) => {
                const Icon = item.icon;

                return (
                  <button
                    key={item.name}
                    onClick={() => {
                      setActivePage(item.name);
                      setSidebarOpen(false);
                    }}
                    className={`nav-item ${
                      activePage === item.name ? "active" : ""
                    }`}
                  >
                    <Icon size={17} className="shrink-0" />
                    <span className="min-w-0 flex-1">{item.name}</span>

                    {item.count !== undefined && (
                      <span
                        className={`rounded-full px-2 py-0.5 text-[9px] font-bold ${
                          item.name === "Anomalies"
                            ? "bg-red-500/20 text-red-300"
                            : "bg-amber-500/20 text-amber-300"
                        }`}
                      >
                        {item.name === "Anomalies"
                          ? anomalySummary?.total_anomalies ?? item.count
                          : item.count}
                      </span>
                    )}
                  </button>
                );
              })}
            </nav>
          </div>

          <div className="m-3 rounded-xl border border-cyan-900/70 bg-gradient-to-br from-[#102638] to-[#091722] p-4">
            <p className="mb-3 text-[9px] font-bold tracking-[.15em] text-slate-400">
              PLANT STATUS
            </p>

            <div className="mb-4 flex items-center gap-2 text-xs font-bold text-emerald-400">
              <span className="status-dot" /> Running
            </div>

            {[
              ["Total Machines", "30"],
              ["Running", "28"],
              ["Stopped", "1"],
              ["Maintenance", "1"],
            ].map((row, i) => (
              <div
                key={row[0]}
                className="flex justify-between border-t border-white/5 py-2 text-[10px]"
              >
                <span className="text-slate-400">{row[0]}</span>
                <span
                  className={
                    i === 2
                      ? "font-bold text-red-400"
                      : "font-semibold text-white"
                  }
                >
                  {row[1]}
                </span>
              </div>
            ))}
          </div>

          <div className="border-t border-cyan-900/50 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full border border-cyan-700 bg-cyan-950 text-xs font-bold text-cyan-300">
                SP
              </div>

              <div>
                <p className="text-xs font-semibold text-white">
                  Plant Operator
                </p>
                <p className="mt-1 text-[9px] text-slate-500">
                  Administrator
                </p>
              </div>

              <Settings size={15} className="ml-auto text-slate-500" />
            </div>
          </div>
        </aside>

        {/* MAIN CONTENT */}
        <div className="min-w-0 flex-1 p-3 sm:p-5 lg:p-6">
          {activePage !== "Overview" && (
            <div className="mb-5 flex items-center justify-between rounded-xl border border-cyan-800/60 bg-cyan-950/30 p-3">
              <p className="text-xs text-cyan-200">
                <span className="text-slate-500">CURRENT SECTION / </span>
                {activePage}
              </p>

              <button
                onClick={() => setActivePage("Overview")}
                className="text-[10px] font-semibold text-emerald-400 hover:text-emerald-300"
              >
                Back to overview
              </button>
            </div>
          )}

          <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-[9px] font-bold tracking-[.2em] text-cyan-400">
                INDUSTRIAL CONTROL CENTER
              </p>
              <h2 className="mt-1 text-xl font-bold tracking-tight text-white sm:text-2xl">
                Plant Dashboard
              </h2>
              <p className="mt-1 text-[10px] text-slate-500">
                Production performance and operational overview
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-lg border border-cyan-900/60 bg-[#0b1a27] px-3 py-2 text-[9px] text-slate-400">
              <Activity size={13} className="text-emerald-400" />
              BACKEND DATA · {plant.toUpperCase()} · SHIFT {shift}
            </div>
          </div>

          {/* DAILY REPORT DATE */}
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-cyan-900/60 bg-[#0b1a27] p-3">
            <div>
              <p className="text-[10px] font-bold tracking-[.15em] text-cyan-300">
                DAILY OEE REPORT
              </p>
              <p className="mt-1 text-[9px] text-slate-500">
                Select a date to load plant-wide daily performance
              </p>
            </div>

            <div className="flex items-center gap-2">
              <label
                htmlFor="oee-report-date"
                className="text-[10px] text-slate-400"
              >
                Report date
              </label>

              <input
                id="oee-report-date"
                type="date"
                value={selectedDate}
                onChange={(event) => setSelectedDate(event.target.value)}
                className="rounded-lg border border-cyan-800 bg-slate-950 px-3 py-2 text-xs text-white outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          {/* DAILY OEE KPI CARDS */}
          {dailyError && (
            <p className="mb-3 rounded-lg border border-red-900/50 bg-red-950/20 p-3 text-xs text-red-300">
              Daily OEE: {dailyError}
            </p>
          )}

          <div className="mb-5 grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-5">
            <KpiCard
              title="Machines Reporting"
              value={dailyLoading ? "..." : String(dailyOee.length)}
              subtitle="Machines in selected date"
              icon={Factory}
              color="#22d3ee"
            />

            <KpiCard
              title="Average OEE"
              value={
                dailyLoading
                  ? "..."
                  : averageOee === null
                    ? "—"
                    : `${averageOee.toFixed(1)}%`
              }
              subtitle="Daily average across machines"
              icon={CircleGauge}
              color="#00e6a0"
            />

            <KpiCard
              title="Availability"
              value={
                dailyLoading
                  ? "..."
                  : averageAvailability === null
                    ? "—"
                    : `${averageAvailability.toFixed(1)}%`
              }
              subtitle="Daily average across machines"
              icon={Cog}
              color="#22d3ee"
            />

            <KpiCard
              title="Performance"
              value={
                dailyLoading
                  ? "..."
                  : averagePerformance === null
                    ? "—"
                    : `${averagePerformance.toFixed(1)}%`
              }
              subtitle="Daily average across machines"
              icon={Gauge}
              color="#ffbd35"
            />

            <KpiCard
              title="Quality"
              value={
                dailyLoading
                  ? "..."
                  : averageQuality === null
                    ? "—"
                    : `${averageQuality.toFixed(1)}%`
              }
              subtitle="Daily average across machines"
              icon={ShieldCheck}
              color="#00e6a0"
            />
          </div>

          {/* DASHBOARD CONTENT GRID */}
          <div className="dashboard-main-grid grid grid-cols-1 gap-4 2xl:grid-cols-[minmax(0,1fr)_320px]">
            <div className="min-w-0 space-y-4">
              {/* SEVEN-DAY OEE TREND */}
              <Panel
                title="Seven-Day OEE Trend"
                action={
                  <span className="text-[9px] text-emerald-400">
                    DAILY API
                  </span>
                }
              >
                <p className="mb-3 text-[9px] text-slate-500">
                  Average OEE across reporting machines · {selectedDate} to the
                  following six days
                </p>

                {trendError ? (
                  <p className="rounded-lg border border-red-900/50 bg-red-950/20 p-3 text-xs text-red-300">
                    {trendError}
                  </p>
                ) : trendLoading ? (
                  <p className="p-4 text-xs text-slate-400">
                    Loading seven-day OEE trend...
                  </p>
                ) : oeeTrend.length === 0 ? (
                  <p className="p-4 text-xs text-slate-400">
                    No trend records available for this date range.
                  </p>
                ) : (
                  <>
                    <div className="chart-container h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={oeeTrend}>
                          <CartesianGrid
                            stroke="#1c3949"
                            strokeDasharray="3 3"
                          />

                          <XAxis
                            dataKey="date"
                            tick={{
                              fill: "#8298a8",
                              fontSize: 9,
                            }}
                            axisLine={false}
                            tickLine={false}
                          />

                          <YAxis
                            domain={[0, 100]}
                            tick={{
                              fill: "#8298a8",
                              fontSize: 9,
                            }}
                            axisLine={false}
                            tickLine={false}
                            width={30}
                          />

                          <Tooltip content={<ChartTooltip />} />

                          <Line
                            type="monotone"
                            dataKey="average_oee"
                            name="Average OEE"
                            stroke="#00e6a0"
                            strokeWidth={2.5}
                            dot={{ r: 3, fill: "#00e6a0" }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>

                    <div className="mt-4 grid grid-cols-1 gap-3 border-t border-cyan-900/50 pt-3 sm:grid-cols-2">
                      <div>
                        <p className="text-[9px] text-slate-500">
                          Total production (7 days)
                        </p>
                        <p className="mt-1 text-lg font-bold text-white">
                          {oeeTrend
                            .reduce(
                              (sum, day) =>
                                sum + Number(day.total_production || 0),
                              0
                            )
                            .toLocaleString()}
                        </p>
                      </div>

                      <div>
                        <p className="text-[9px] text-slate-500">
                          Good production (7 days)
                        </p>
                        <p className="mt-1 text-lg font-bold text-emerald-300">
                          {oeeTrend
                            .reduce(
                              (sum, day) =>
                                sum + Number(day.total_good_production || 0),
                              0
                            )
                            .toLocaleString()}
                        </p>
                      </div>
                    </div>
                  </>
                )}
              </Panel>

              <Panel
                title="Production Process Flow"
                action={
                  <span className="text-[9px] font-bold text-amber-400">
                    ILLUSTRATIVE VIEW
                  </span>
                }
              >
                <ProcessDiagram />
              </Panel>

              {/* ALARMS AND CHARTS */}
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 2xl:grid-cols-4">
                <Panel title="Alarm Summary">
                  <div className="mb-4 grid grid-cols-3 gap-1 border-b border-cyan-900/50 pb-4 text-center">
                    <div>
                      <AlertTriangle className="mx-auto text-red-400" size={20} />
                      <p className="mt-2 text-xl font-bold text-white">3</p>
                      <p className="text-[9px] text-red-400">Critical</p>
                    </div>

                    <div>
                      <AlertTriangle className="mx-auto text-amber-400" size={20} />
                      <p className="mt-2 text-xl font-bold text-white">2</p>
                      <p className="text-[9px] text-amber-400">Warning</p>
                    </div>

                    <div>
                      <Activity className="mx-auto text-sky-400" size={20} />
                      <p className="mt-2 text-xl font-bold text-white">5</p>
                      <p className="text-[9px] text-sky-400">Info</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {alarms.map((alarm) => (
                      <div
                        key={alarm.time}
                        className="flex items-start gap-2 text-[9px]"
                      >
                        <span className="shrink-0 text-slate-500">
                          {alarm.time}
                        </span>

                        <span className="min-w-0 flex-1 text-slate-300">
                          {alarm.message}
                        </span>

                        <span
                          className={`shrink-0 font-bold ${
                            alarm.level === "CRITICAL"
                              ? "text-red-400"
                              : alarm.level === "WARNING"
                                ? "text-amber-400"
                                : "text-sky-400"
                          }`}
                        >
                          {alarm.level}
                        </span>
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={() => setShowAlarms(!showAlarms)}
                    className="mt-4 w-full rounded-lg border border-cyan-800/70 bg-cyan-950/40 py-2.5 text-[10px] font-semibold text-cyan-300 transition hover:bg-cyan-900/50"
                  >
                    {showAlarms ? "Hide alarm details" : "View all alarms →"}
                  </button>

                  {showAlarms && (
                    <p className="mt-3 rounded-lg bg-slate-950/60 p-2 text-[9px] text-slate-400">
                      Alarm records are illustrative until connected to the
                      monitoring API.
                    </p>
                  )}
                </Panel>

                <Panel
                  title="Production Trend"
                  action={
                    <span className="text-[9px] text-amber-400">
                      PREVIEW DATA
                    </span>
                  }
                >
                  <p className="mb-2 text-[9px] text-slate-500">
                    Production units / hour
                  </p>

                  <div className="chart-container h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={productionData}>
                        <defs>
                          <linearGradient
                            id="prodFill"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                          >
                            <stop
                              offset="0%"
                              stopColor="#00e6a0"
                              stopOpacity={0.35}
                            />
                            <stop
                              offset="100%"
                              stopColor="#00e6a0"
                              stopOpacity={0}
                            />
                          </linearGradient>
                        </defs>

                        <CartesianGrid
                          stroke="#1c3949"
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="time"
                          tick={{ fill: "#8298a8", fontSize: 8 }}
                          axisLine={false}
                          tickLine={false}
                        />

                        <YAxis
                          tick={{ fill: "#8298a8", fontSize: 8 }}
                          axisLine={false}
                          tickLine={false}
                          width={28}
                        />

                        <Tooltip content={<ChartTooltip />} />

                        <Area
                          type="monotone"
                          dataKey="production"
                          name="Production"
                          stroke="#00e6a0"
                          strokeWidth={2}
                          fill="url(#prodFill)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </Panel>

                <Panel
                  title="Machine OEE Comparison"
                  action={
                    <span className="text-[9px] text-emerald-400">
                      LIVE API
                    </span>
                  }
                >
                  <div className="mb-3 flex flex-wrap gap-2 text-[8px]">
                    <span className="text-emerald-400">● OEE</span>
                    <span className="text-sky-400">● Availability</span>
                    <span className="text-amber-400">● Performance</span>
                  </div>

                  <div className="chart-container h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={machineOeeChartData}>
                        <CartesianGrid
                          stroke="#1c3949"
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="machine"
                          interval="preserveStartEnd"
                          tick={{ fill: "#8298a8", fontSize: 8 }}
                          axisLine={false}
                          tickLine={false}
                        />

                        <YAxis
                          domain={[0, 100]}
                          tick={{ fill: "#8298a8", fontSize: 8 }}
                          axisLine={false}
                          tickLine={false}
                          width={25}
                        />

                        <Tooltip content={<ChartTooltip />} />

                        <Line
                          type="monotone"
                          dataKey="oee"
                          name="OEE"
                          stroke="#00e6a0"
                          strokeWidth={2}
                          dot={false}
                        />

                        <Line
                          type="monotone"
                          dataKey="availability"
                          name="Availability"
                          stroke="#22c8f5"
                          strokeWidth={1.5}
                          dot={false}
                        />

                        <Line
                          type="monotone"
                          dataKey="performance"
                          name="Performance"
                          stroke="#ffbd35"
                          strokeWidth={1.5}
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </Panel>

                <Panel
                  title="Temperature Profile"
                  action={
                    <span className="text-[9px] text-amber-400">
                      PREVIEW DATA
                    </span>
                  }
                >
                  <div className="mb-3 flex flex-wrap gap-2 text-[8px]">
                    <span className="text-red-400">● Mixer</span>
                    <span className="text-amber-400">● Reactor</span>
                    <span className="text-sky-400">● Separator</span>
                  </div>

                  <div className="chart-container h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={temperatureData}>
                        <CartesianGrid
                          stroke="#1c3949"
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="time"
                          tick={{ fill: "#8298a8", fontSize: 8 }}
                          axisLine={false}
                          tickLine={false}
                        />

                        <YAxis
                          tick={{ fill: "#8298a8", fontSize: 8 }}
                          axisLine={false}
                          tickLine={false}
                          width={25}
                        />

                        <Tooltip content={<ChartTooltip />} />

                        <Line
                          type="monotone"
                          dataKey="mixer"
                          name="Mixer"
                          stroke="#ff5266"
                          strokeWidth={2}
                          dot={false}
                        />

                        <Line
                          type="monotone"
                          dataKey="reactor"
                          name="Reactor"
                          stroke="#ffbd35"
                          strokeWidth={2}
                          dot={false}
                        />

                        <Line
                          type="monotone"
                          dataKey="separator"
                          name="Separator"
                          stroke="#22c8f5"
                          strokeWidth={2}
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </Panel>
              </div>

              {/* MACHINE MONITORING */}
              <Panel
                title="Machine Status Monitoring"
                action={
                  <span className="text-[9px] text-slate-500">
                    {machineOee.length} machines · Shift {shift}
                  </span>
                }
              >
                {oeeError ? (
                  <p className="rounded-lg border border-red-900/50 bg-red-950/20 p-3 text-xs text-red-300">
                    {oeeError}
                  </p>
                ) : oeeLoading ? (
                  <p className="p-4 text-xs text-slate-400">
                    Loading machine OEE data...
                  </p>
                ) : machineOee.length === 0 ? (
                  <p className="p-4 text-xs text-slate-400">
                    No machine OEE records returned for this shift.
                  </p>
                ) : (
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 2xl:grid-cols-4">
                    {machineOee.map((machine) => (
                      <MachineCard
                        key={machine.machine_id}
                        machine={machine}
                      />
                    ))}
                  </div>
                )}
              </Panel>
            </div>

            {/* RIGHT COLUMN */}
            <aside className="min-w-0 space-y-4">
              <Panel
                title="Energy Consumption"
                action={
                  <span className="text-[9px] text-amber-400">
                    PREVIEW DATA
                  </span>
                }
              >
                <p className="mb-2 text-[9px] text-slate-500">
                  Energy consumption · kWh
                </p>

                <div className="chart-container h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={energyData}>
                      <defs>
                        <linearGradient
                          id="energyFill"
                          x1="0"
                          y1="0"
                          x2="0"
                          y2="1"
                        >
                          <stop
                            offset="0%"
                            stopColor="#22c8f5"
                            stopOpacity={0.3}
                          />
                          <stop
                            offset="100%"
                            stopColor="#22c8f5"
                            stopOpacity={0}
                          />
                        </linearGradient>
                      </defs>

                      <CartesianGrid
                        stroke="#1c3949"
                        strokeDasharray="3 3"
                      />

                      <XAxis
                        dataKey="time"
                        tick={{ fill: "#8298a8", fontSize: 8 }}
                        axisLine={false}
                        tickLine={false}
                      />

                      <YAxis
                        tick={{ fill: "#8298a8", fontSize: 8 }}
                        axisLine={false}
                        tickLine={false}
                        width={30}
                      />

                      <Tooltip content={<ChartTooltip />} />

                      <Area
                        type="monotone"
                        dataKey="energy"
                        name="Energy"
                        stroke="#22c8f5"
                        fill="url(#energyFill)"
                        strokeWidth={2}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </Panel>

              <Panel title="Power Distribution">
                <div className="flex flex-wrap items-center justify-center gap-4 sm:flex-nowrap">
                  <div
                    className="relative h-36 w-36 shrink-0 rounded-full"
                    style={{
                      background:
                        "conic-gradient(#00e6a0 0 40%, #22c8f5 40% 70%, #ffbd35 70% 85%, #718096 85% 100%)",
                    }}
                  >
                    <div className="absolute inset-3 flex flex-col items-center justify-center rounded-full bg-[#0b1a27]">
                      <p className="text-2xl font-bold text-white">3,200</p>
                      <p className="text-[9px] text-slate-400">kW Total</p>
                    </div>
                  </div>

                  <div className="min-w-0 flex-1 space-y-3 text-[10px]">
                    {[
                      ["Motors", "1,280", "#00e6a0"],
                      ["Heating", "960", "#22c8f5"],
                      ["Lighting", "640", "#ffbd35"],
                      ["Other", "320", "#718096"],
                    ].map((row) => (
                      <div
                        key={row[0]}
                        className="flex items-center justify-between gap-2"
                      >
                        <span className="flex items-center gap-2 text-slate-300">
                          <span
                            className="h-2 w-2 shrink-0 rounded-full"
                            style={{ background: row[2] }}
                          />
                          {row[0]}
                        </span>

                        <span className="font-semibold text-white">
                          {row[1]}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </Panel>

              <Panel title="Utilities">
                <div className="space-y-5">
                  {[
                    {
                      name: "Compressed Air",
                      value: "6.2 bar",
                      percent: 78,
                      icon: Wind,
                    },
                    {
                      name: "Steam Pressure",
                      value: "4.1 bar",
                      percent: 55,
                      icon: Activity,
                    },
                    {
                      name: "Water Flow",
                      value: "82.3 m³/h",
                      percent: 82,
                      icon: Droplets,
                    },
                    {
                      name: "Power Factor",
                      value: "0.98",
                      percent: 98,
                      icon: Zap,
                    },
                  ].map((item) => {
                    const Icon = item.icon;

                    return (
                      <div key={item.name}>
                        <div className="mb-2 flex items-center justify-between gap-2 text-[10px]">
                          <span className="flex items-center gap-2 text-slate-300">
                            <Icon size={14} className="text-cyan-400" />
                            {item.name}
                          </span>

                          <span className="font-semibold text-white">
                            {item.value}
                          </span>
                        </div>

                        <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                          <div
                            className="h-full rounded-full bg-gradient-to-r from-emerald-600 to-emerald-300"
                            style={{ width: `${item.percent}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Panel>

              <Panel title="AI Monitoring">
                <div className="flex items-center gap-3 rounded-xl border border-emerald-800/60 bg-emerald-950/30 p-3">
                  <div className="rounded-xl bg-emerald-900/50 p-3 text-emerald-400">
                    <Cpu size={23} />
                  </div>

                  <div>
                    <p className="text-xs font-bold text-emerald-300">
                      Isolation Forest
                    </p>
                    <p className="mt-1 text-[9px] text-slate-400">
                      Machine anomaly detection
                    </p>
                  </div>

                  {anomalySummary ? (
                    <CheckCircle2
                      size={16}
                      className="ml-auto text-emerald-400"
                    />
                  ) : (
                    <span className="ml-auto h-2 w-2 rounded-full bg-amber-400" />
                  )}
                </div>

                {anomalySummary ? (
                  <>
                    <div className="mt-4 flex items-center justify-between text-[10px]">
                      <span className="text-slate-400">
                        Detected observations
                      </span>

                      <span className="text-lg font-bold text-amber-300">
                        {anomalySummary.total_anomalies.toLocaleString()}
                      </span>
                    </div>

                    <div className="mt-4 rounded-lg border border-cyan-900/50 bg-slate-950/40 p-3">
                      <p className="text-[10px] text-slate-400">
                        Severity distribution
                      </p>

                      {([
                        ["High", anomalySummary.severity_distribution?.High ?? 0],
                        ["Medium", anomalySummary.severity_distribution?.Medium ?? 0],
                        ["Low", anomalySummary.severity_distribution?.Low ?? 0],
                      ] as const).map(([severity, count]) => (
                        <div
                          key={severity}
                          className="mt-2 flex justify-between gap-2 text-xs"
                        >
                          <span className="text-slate-300">{severity}</span>
                          <span
                            className={`font-bold ${
                              severity === "High"
                                ? "text-red-400"
                                : severity === "Medium"
                                  ? "text-amber-300"
                                  : "text-emerald-400"
                            }`}
                          >
                            {count.toLocaleString()}
                          </span>
                        </div>
                      ))}
                    </div>

                    <div className="mt-3 rounded-lg border border-emerald-900/40 bg-emerald-950/20 p-2 text-[9px] leading-relaxed text-emerald-200/70">
                      API connected · Summary retrieved from FastAPI.
                    </div>
                  </>
                ) : (
                  <div className="mt-3 rounded-lg border border-amber-900/40 bg-amber-950/20 p-3 text-[9px] leading-relaxed text-amber-200/80">
                    {anomalyError || "Loading anomaly summary from backend..."}
                  </div>
                )}

                <p className="mt-3 text-[9px] leading-relaxed text-slate-500">
                  Anomalies are statistically unusual observations, not
                  confirmed machine failures. Severity indicates the relative
                  level of deviation detected by the model.
                </p>
              </Panel>
            </aside>
          </div>

          {/* Manufacturing AI Copilot */}
          <div className="mt-6">
            <CopilotChat />
          </div>

          <footer className="mt-6 flex flex-wrap items-center justify-between gap-2 border-t border-cyan-900/50 py-4 text-[9px] text-slate-500">
            <span className="font-semibold tracking-wider">
              YOTTAFLEX MANUFACTURING INTELLIGENCE
            </span>

            <span>
              OEE and anomaly metrics retrieved from FastAPI · Other panels may
              contain preview data
            </span>

            <span className="flex items-center gap-2 text-emerald-400">
              <span className="status-dot" /> UI ACTIVE
            </span>
          </footer>
        </div>
      </div>
    </main>
  );
}
