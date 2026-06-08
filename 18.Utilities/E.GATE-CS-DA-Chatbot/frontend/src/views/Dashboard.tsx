import { useEffect, useState } from "react";
import { getAnalytics, getCoach } from "../lib/api";
import type { Analytics, CoachReport } from "../types";

function ring(pct: number) {
  const r = 34, c = 2 * Math.PI * r;
  return { r, c, off: c - (pct / 100) * c };
}

export default function Dashboard() {
  const [a, setA] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalytics().then(setA).catch(() => {}).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="grid h-full place-items-center text-slate-400">Loading analytics…</div>;
  }
  if (!a || !a.ok || a.attempts === 0) {
    return (
      <div className="grid h-full place-items-center p-6 text-center">
        <div>
          <div className="text-4xl">📊</div>
          <p className="mt-2 font-semibold">No data yet</p>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Take a quiz or mock test and your progress will show up here.
          </p>
        </div>
      </div>
    );
  }

  const rd = ring(a.readiness);
  const subjects = Object.entries(a.by_subject).sort((x, y) => x[1].accuracy - y[1].accuracy);

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-4xl px-4 py-6">
        <h2 className="text-xl font-extrabold">📊 Performance Dashboard</h2>

        <CoachCard />

        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <Kpi label="Readiness" value={`${a.readiness}`} suffix="/100" accent />
          <Kpi label="Avg accuracy" value={`${Math.round(a.avg_accuracy * 100)}%`} />
          <Kpi label="Avg percentile" value={`${a.avg_percentile}`} />
          <Kpi label="Streak" value={`${a.streak}🔥`} />
        </div>

        {/* Rank band · this week · trend */}
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Estimated rank</div>
            <div className="mt-1 text-lg font-extrabold text-brand-600 dark:text-brand-400">
              {a.rank_band || "—"}
            </div>
            <div className="mt-1 text-[11px] text-slate-400">Heuristic from your average percentile</div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">This week</div>
            <div className="mt-1 text-lg font-extrabold">
              {a.last7?.attempts ?? 0} <span className="text-sm font-medium text-slate-400">test(s)</span>
            </div>
            <div className="mt-1 text-[11px] text-slate-400">
              {a.last7 && a.last7.attempts ? `${Math.round(a.last7.avg_accuracy * 100)}% avg accuracy` : "No tests in the last 7 days"}
            </div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Percentile trend</div>
            <Sparkline points={(a.percentile_trend || []).map((p) => p.percentile)} />
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-3">
          {/* Readiness ring */}
          <div className="grid place-items-center rounded-2xl border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-slate-900">
            <svg width="100" height="100" viewBox="0 0 80 80">
              <circle cx="40" cy="40" r={rd.r} fill="none" stroke="currentColor"
                      className="text-slate-200 dark:text-white/10" strokeWidth="8" />
              <circle cx="40" cy="40" r={rd.r} fill="none" stroke="url(#g)" strokeWidth="8"
                      strokeLinecap="round" strokeDasharray={rd.c} strokeDashoffset={rd.off}
                      transform="rotate(-90 40 40)" />
              <defs>
                <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stopColor="#dc2626" /><stop offset="1" stopColor="#e11d48" />
                </linearGradient>
              </defs>
              <text x="40" y="45" textAnchor="middle" className="fill-slate-800 dark:fill-white"
                    fontSize="18" fontWeight="800">{a.readiness}</text>
            </svg>
            <p className="mt-2 text-sm font-semibold">Exam readiness</p>
            <p className="text-xs text-slate-400">{a.attempts} attempt(s) · {a.due_reviews} cards due</p>
          </div>

          {/* Subject accuracy bars */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 md:col-span-2 dark:border-white/10 dark:bg-slate-900">
            <h3 className="mb-3 text-sm font-bold">Accuracy by subject</h3>
            {subjects.length === 0 ? (
              <p className="text-sm text-slate-400">No subject data yet.</p>
            ) : (
              <div className="space-y-2.5">
                {subjects.map(([s, b]) => {
                  const pct = Math.round(b.accuracy * 100);
                  return (
                    <div key={s}>
                      <div className="mb-0.5 flex justify-between text-xs">
                        <span className="text-slate-600 dark:text-slate-300">{s}</span>
                        <span className="text-slate-400">{pct}% ({b.correct}/{b.total})</span>
                      </div>
                      <div className="h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-white/10">
                        <div className={`h-full rounded-full ${pct < 50 ? "bg-red-500" : pct < 75 ? "bg-amber-500" : "bg-emerald-500"}`}
                             style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
            {a.weak_areas.length > 0 && (
              <p className="mt-3 text-xs text-amber-600 dark:text-amber-400">
                ⚠ Weak areas to prioritise: {a.weak_areas.join(", ")}
              </p>
            )}
          </div>
        </div>

        {/* Recent attempts */}
        <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-slate-900">
          <h3 className="mb-3 text-sm font-bold">Recent attempts</h3>
          <div className="space-y-2">
            {a.recent.map((r, i) => (
              <div key={i} className="flex items-center justify-between rounded-lg border border-slate-100 px-3 py-2 text-sm dark:border-white/5">
                <span className="font-medium">{r.subject}</span>
                <span className="text-slate-500 dark:text-slate-400">
                  {r.score}/{r.max_score} · {Math.round(r.accuracy * 100)}% · {r.percentile}pc
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function Kpi({ label, value, suffix, accent }: {
  label: string; value: string; suffix?: string; accent?: boolean;
}) {
  return (
    <div className={`rounded-2xl border p-4 ${accent
      ? "border-transparent bg-gradient-to-br from-brand-500 to-accent-500 text-white"
      : "border-slate-200 bg-white dark:border-white/10 dark:bg-slate-900"}`}>
      <div className={`text-2xl font-extrabold ${accent ? "" : "text-slate-800 dark:text-white"}`}>
        {value}<span className={`text-sm font-medium ${accent ? "opacity-80" : "text-slate-400"}`}>{suffix}</span>
      </div>
      <div className={`text-xs ${accent ? "opacity-90" : "text-slate-500 dark:text-slate-400"}`}>{label}</div>
    </div>
  );
}

function CoachCard() {
  const [report, setReport] = useState<CoachReport | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try {
      setReport(await getCoach("CS"));
    } catch {
      setReport({ ok: false, message: "Couldn't reach the coach. Try again." });
    } finally {
      setLoading(false);
    }
  };

  const Section = ({ title, items, icon }: { title: string; items?: string[]; icon: string }) =>
    items && items.length ? (
      <div className="mt-3">
        <div className="mb-1 text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-400">
          {icon} {title}
        </div>
        <ul className="list-disc space-y-1 pl-5 text-sm text-slate-700 dark:text-slate-200">
          {items.map((t, i) => <li key={i}>{t}</li>)}
        </ul>
      </div>
    ) : null;

  return (
    <div className="mt-4 rounded-2xl border border-brand-500/30 bg-gradient-to-br from-brand-500/10 to-accent-500/5 p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h3 className="flex items-center gap-2 text-base font-bold">🧭 Your AI Coach</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Personalised, rank-focused feedback from your attempts, weak areas, streak &amp; plan.
          </p>
        </div>
        <button
          onClick={run}
          disabled={loading}
          className="rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 px-4 py-2 text-sm font-semibold text-white shadow-md transition hover:opacity-90 disabled:opacity-60"
        >
          {loading ? "Analysing…" : report ? "Refresh advice" : "Get coaching"}
        </button>
      </div>

      {report && !report.ok && (
        <p className="mt-3 text-sm text-amber-600 dark:text-amber-400">
          {report.message || "No coaching available yet."}
        </p>
      )}

      {report && report.ok && (
        <div className="mt-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
          {report.headline && (
            <p className="text-sm font-semibold text-slate-800 dark:text-white">{report.headline}</p>
          )}
          <Section title="Strengths" items={report.strengths} icon="✅" />
          <Section title="Focus areas" items={report.focus_areas} icon="🎯" />
          <Section title="This week" items={report.this_week} icon="🗓️" />
          {report.rank_advice && (
            <div className="mt-3 rounded-lg bg-brand-500/10 p-3 text-sm text-slate-700 dark:text-slate-200">
              <b className="text-brand-600 dark:text-brand-400">🏆 Biggest lever for a top rank:</b>{" "}
              {report.rank_advice}
            </div>
          )}
          {report.habit && (
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">🔥 <b>Consistency:</b> {report.habit}</p>
          )}
          {report.encouragement && (
            <p className="mt-2 text-sm font-medium text-emerald-600 dark:text-emerald-400">{report.encouragement}</p>
          )}
        </div>
      )}
    </div>
  );
}

function Sparkline({ points }: { points: number[] }) {
  if (!points.length) {
    return <div className="mt-2 text-[11px] text-slate-400">Take a few tests to see your trend.</div>;
  }
  const W = 220, H = 44, n = points.length;
  const max = 100, min = 0;
  const x = (i: number) => (n === 1 ? W / 2 : (i / (n - 1)) * (W - 6) + 3);
  const y = (v: number) => H - 4 - ((v - min) / (max - min)) * (H - 8);
  const d = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(1)},${y(p).toFixed(1)}`).join(" ");
  const up = points.length > 1 && points[points.length - 1] >= points[0];
  return (
    <div className="mt-1">
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" className="h-12 w-full">
        <path d={d} fill="none" stroke={up ? "#22c55e" : "#ef4444"} strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round" />
        {points.map((p, i) => (
          <circle key={i} cx={x(i)} cy={y(p)} r="2" fill={up ? "#22c55e" : "#ef4444"} />
        ))}
      </svg>
      <div className="text-[11px] text-slate-400">
        {points.length} attempt(s) · latest {points[points.length - 1]} pc {up ? "↗" : "↘"}
      </div>
    </div>
  );
}
