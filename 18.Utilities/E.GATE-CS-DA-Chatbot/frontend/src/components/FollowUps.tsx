import { SparkIcon } from "./icons";

// Contextual follow-ups offered after every answer — one click sends them.
const FOLLOW_UPS = [
  "Explain this step by step.",
  "Give me a similar previous-year question (PYQ).",
  "What's the underlying concept and formula?",
  "Why is this the correct answer?",
  "Give me 3 practice problems on this topic.",
  "Summarise this in 3 bullet points for revision.",
];

export default function FollowUps({
  onPick,
  disabled,
}: {
  onPick: (prompt: string) => void;
  disabled?: boolean;
}) {
  return (
    <div className="mt-3">
      <div className="mb-1.5 flex items-center gap-1 text-[11px] font-semibold uppercase tracking-wide text-slate-400">
        <SparkIcon width={12} height={12} /> Follow-up
      </div>
      <div className="flex flex-wrap gap-1.5">
        {FOLLOW_UPS.map((f) => (
          <button
            key={f}
            disabled={disabled}
            onClick={() => onPick(f)}
            className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-600 transition hover:-translate-y-0.5 hover:border-brand-400 hover:text-brand-600 disabled:cursor-not-allowed disabled:opacity-50 dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-300 dark:hover:border-brand-500 dark:hover:text-brand-300"
          >
            {f}
          </button>
        ))}
      </div>
    </div>
  );
}
