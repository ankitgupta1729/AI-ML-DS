import { useState } from "react";

const REASONS = [
  { key: "incorrect", label: "Incorrect" },
  { key: "incomplete", label: "Incomplete" },
  { key: "not_helpful", label: "Not helpful" },
  { key: "off_topic", label: "Off-topic" },
  { key: "too_verbose", label: "Too verbose" },
  { key: "hard_to_read", label: "Hard to read" },
];

interface Props {
  onSubmit: (data: {
    reason?: string;
    comment?: string;
    correctedAnswer?: string;
  }) => void;
  onCancel: () => void;
}

export default function FeedbackForm({ onSubmit, onCancel }: Props) {
  const [reason, setReason] = useState<string | undefined>();
  const [comment, setComment] = useState("");
  const [correction, setCorrection] = useState("");
  const [showCorrection, setShowCorrection] = useState(false);

  return (
    <div className="animate-fade-in-up mt-2 rounded-xl border border-slate-200 bg-slate-50 p-3 dark:border-white/10 dark:bg-white/[0.04]">
      <p className="mb-2 text-xs font-semibold text-slate-600 dark:text-slate-300">
        What went wrong? Your feedback trains the assistant.
      </p>

      <div className="mb-2 flex flex-wrap gap-1.5">
        {REASONS.map((r) => (
          <button
            key={r.key}
            onClick={() => setReason(reason === r.key ? undefined : r.key)}
            className={`rounded-full border px-2.5 py-1 text-xs transition ${
              reason === r.key
                ? "border-brand-500 bg-brand-500/10 text-brand-600 dark:text-brand-300"
                : "border-slate-300 text-slate-600 hover:border-brand-400 dark:border-white/15 dark:text-slate-300"
            }`}
          >
            {r.label}
          </button>
        ))}
      </div>

      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Add details (optional)…"
        rows={2}
        className="w-full resize-none rounded-lg border border-slate-300 bg-white px-2.5 py-1.5 text-sm text-slate-800 outline-none focus:border-brand-500 dark:border-white/15 dark:bg-slate-900 dark:text-slate-100"
      />

      {!showCorrection ? (
        <button
          onClick={() => setShowCorrection(true)}
          className="mt-1.5 text-xs font-medium text-brand-600 hover:underline dark:text-brand-400"
        >
          + Suggest a better answer (helps RLHF training)
        </button>
      ) : (
        <textarea
          value={correction}
          onChange={(e) => setCorrection(e.target.value)}
          placeholder="What should the assistant have said?"
          rows={3}
          className="mt-1.5 w-full resize-none rounded-lg border border-emerald-300 bg-white px-2.5 py-1.5 text-sm text-slate-800 outline-none focus:border-emerald-500 dark:border-emerald-500/30 dark:bg-slate-900 dark:text-slate-100"
        />
      )}

      <div className="mt-2 flex justify-end gap-2">
        <button
          onClick={onCancel}
          className="rounded-lg px-3 py-1.5 text-xs text-slate-500 hover:bg-slate-200 dark:hover:bg-white/10"
        >
          Cancel
        </button>
        <button
          onClick={() =>
            onSubmit({
              reason,
              comment: comment.trim() || undefined,
              correctedAnswer: correction.trim() || undefined,
            })
          }
          className="rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 px-3 py-1.5 text-xs font-semibold text-white shadow-sm transition hover:opacity-90"
        >
          Submit feedback
        </button>
      </div>
    </div>
  );
}
