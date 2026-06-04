import { useEffect, useState } from "react";
import { getDaily } from "../lib/api";
import type { DailyQuestion } from "../types";

export default function Daily({ onAsk }: { onAsk: (prompt: string) => void }) {
  const [d, setD] = useState<DailyQuestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [showHint, setShowHint] = useState(false);

  useEffect(() => {
    getDaily().then(setD).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <div className="grid h-full place-items-center overflow-y-auto p-4">
      <div className="w-full max-w-xl">
        {loading ? (
          <p className="text-center text-slate-400">Loading today's question…</p>
        ) : !d || !d.ok ? (
          <p className="text-center text-slate-400">Couldn't load the daily question.</p>
        ) : (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-slate-900">
            <div className="flex items-center justify-between">
              <span className="rounded-full bg-brand-500/10 px-3 py-1 text-xs font-semibold text-brand-600 dark:text-brand-400">
                Question of the day · {d.date}
              </span>
              <span className="text-sm font-semibold text-amber-500">{d.streak}🔥 streak</span>
            </div>

            <div className="mt-3 text-xs uppercase tracking-wide text-slate-400">{d.topic}</div>
            <p className="mt-1 text-lg font-semibold leading-snug">{d.question}</p>

            {d.hint && (
              <div className="mt-4">
                {showHint ? (
                  <p className="rounded-lg bg-amber-500/10 p-3 text-sm text-amber-700 dark:text-amber-300">
                    💡 {d.hint}
                  </p>
                ) : (
                  <button onClick={() => setShowHint(true)}
                          className="text-sm font-medium text-brand-600 hover:underline dark:text-brand-400">
                    Show hint
                  </button>
                )}
              </div>
            )}

            <button
              onClick={() => onAsk(`Solve and explain step by step: ${d.question}`)}
              className="mt-5 w-full rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 py-2.5 font-semibold text-white shadow-md transition hover:opacity-90"
            >
              Solve with GO Buddy →
            </button>
            <p className="mt-2 text-center text-xs text-slate-400">
              Come back daily to keep your streak alive.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
