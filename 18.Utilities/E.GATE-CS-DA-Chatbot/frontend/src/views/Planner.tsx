import { useEffect, useState } from "react";
import { generatePlan, getPlan, planCalendarUrl } from "../lib/api";
import type { StudyPlan } from "../types";

export default function Planner() {
  const [exam, setExam] = useState("CS");
  const [examDate, setExamDate] = useState("");
  const [days, setDays] = useState(30);
  const [hours, setHours] = useState(4);
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPlan().then((r) => r.ok && r.plan && setPlan(r.plan)).catch(() => {});
  }, []);

  const make = async () => {
    setBusy(true);
    setError(null);
    try {
      const r = await generatePlan({
        exam, exam_date: examDate || null, days, hours,
      });
      if (!r.ok || !r.days?.length) throw new Error("failed");
      setPlan(r);
    } catch {
      setError("Couldn't generate a plan. Check the API/key and try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-3xl px-4 py-6">
        <h2 className="text-xl font-extrabold">🗓️ Study Planner</h2>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          A day-by-day plan to your exam date — prioritising high-weight subjects
          and PYQ practice. Export it to your calendar.
        </p>

        <div className="mt-4 flex flex-wrap items-end gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
          <label className="text-sm">
            <span className="mb-1 block text-xs text-slate-500">Exam</span>
            <select value={exam} onChange={(e) => setExam(e.target.value)}
                    className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm dark:border-white/15 dark:bg-slate-800">
              <option value="CS">GATE CS</option><option value="DA">GATE DA</option>
            </select>
          </label>
          <label className="text-sm">
            <span className="mb-1 block text-xs text-slate-500">Exam date (optional)</span>
            <input type="date" value={examDate} onChange={(e) => setExamDate(e.target.value)}
                   className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm dark:border-white/15 dark:bg-slate-800" />
          </label>
          {!examDate && (
            <label className="text-sm">
              <span className="mb-1 block text-xs text-slate-500">Days: {days}</span>
              <input type="range" min={5} max={90} value={days}
                     onChange={(e) => setDays(Number(e.target.value))} className="accent-brand-500" />
            </label>
          )}
          <label className="text-sm">
            <span className="mb-1 block text-xs text-slate-500">Hours/day: {hours}</span>
            <input type="range" min={1} max={12} value={hours}
                   onChange={(e) => setHours(Number(e.target.value))} className="accent-brand-500" />
          </label>
          <button onClick={make} disabled={busy}
                  className="rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-50">
            {busy ? "Building…" : plan ? "Regenerate" : "Build plan"}
          </button>
        </div>

        {error && <p className="mt-3 text-sm text-red-500">{error}</p>}

        {plan && (
          <div className="mt-6">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="text-sm text-slate-600 dark:text-slate-300">{plan.summary}</p>
              <a href={planCalendarUrl} className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-medium transition hover:border-brand-400 dark:border-white/15">
                ⬇ Export to calendar (.ics)
              </a>
            </div>

            <ol className="mt-4 space-y-3">
              {plan.days.map((d) => (
                <li key={d.day} className="flex gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
                  <div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 text-sm font-bold text-white">
                    {d.day}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-semibold">{d.focus}</span>
                      <span className="text-xs text-slate-400">{d.hours}h</span>
                    </div>
                    <ul className="mt-1 list-disc pl-5 text-sm text-slate-600 dark:text-slate-300">
                      {d.tasks.map((t, i) => <li key={i}>{t}</li>)}
                    </ul>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  );
}
