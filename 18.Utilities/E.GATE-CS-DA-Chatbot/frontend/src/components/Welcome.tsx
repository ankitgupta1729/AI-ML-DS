import type { Meta } from "../types";
import Logo from "./Logo";
import { BookIcon, SparkIcon } from "./icons";

const EXAMPLES: { label: string; prompt: string }[] = [
  {
    label: "📝 PYQ practice",
    prompt:
      "Give me a GATE CS previous-year question on operating systems, then explain the solution step by step.",
  },
  {
    label: "📝 PYQ — DA",
    prompt:
      "Ask me a GATE DA previous-year question on probability and wait for my answer before revealing the solution.",
  },
  {
    label: "🧠 Quiz me",
    prompt:
      "Quiz me with 5 mixed GATE CS MCQs, one at a time. Wait for my answer to each before revealing the correct option, then give my final score.",
  },
  {
    label: "Explain a concept",
    prompt:
      "Explain conflict serializability with a precedence-graph example.",
  },
  {
    label: "ML / AI",
    prompt:
      "Derive the bias–variance trade-off and explain how regularisation helps.",
  },
  {
    label: "Strategy",
    prompt: "How should I plan my last 30 days of GATE DA preparation?",
  },
];

export default function Welcome({
  meta,
  onPick,
}: {
  meta: Meta | null;
  onPick: (prompt: string) => void;
}) {
  return (
    <div className="mx-auto flex max-w-3xl flex-col items-center px-4 py-12 text-center">
      <Logo size={64} />
      <h2 className="mt-5 bg-gradient-to-r from-brand-500 to-accent-500 bg-clip-text text-2xl font-extrabold text-transparent sm:text-3xl">
        {meta?.app_name ?? "GateOverflow Chatbot"}
      </h2>
      <p className="mt-2 max-w-lg text-sm text-slate-500 dark:text-slate-400">
        {meta?.tagline ??
          "Your AI study buddy for GATE CS & DA — grounded in real previous-year questions."}
      </p>

      <div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-xs text-slate-500 dark:text-slate-400">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 px-3 py-1 dark:border-white/10">
          <BookIcon width={14} height={14} /> Grounded in your study material
        </span>
        <span className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 px-3 py-1 dark:border-white/10">
          <SparkIcon width={14} height={14} /> PYQs · concepts · strategy
        </span>
      </div>

      <div className="mt-8 grid w-full grid-cols-1 gap-3 sm:grid-cols-2">
        {EXAMPLES.map((ex) => (
          <button
            key={ex.label}
            onClick={() => onPick(ex.prompt)}
            className="group rounded-2xl border border-slate-200 bg-white p-4 text-left transition hover:-translate-y-0.5 hover:border-brand-400 hover:shadow-lg hover:shadow-brand-500/10 dark:border-white/10 dark:bg-slate-900/60 dark:hover:border-brand-500"
          >
            <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-brand-600 dark:text-brand-400">
              {ex.label}
            </div>
            <div className="text-sm text-slate-700 dark:text-slate-200">
              {ex.prompt}
            </div>
          </button>
        ))}
      </div>

      <a
        href="https://gateoverflow.in"
        target="_blank"
        rel="noreferrer noopener"
        className="mt-8 text-xs text-slate-400 underline-offset-2 hover:text-brand-500 hover:underline"
      >
        Powered by GateOverflow · gateoverflow.in
      </a>
    </div>
  );
}
