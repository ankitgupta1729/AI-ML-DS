import { useState } from "react";
import type { Source } from "../types";
import { ChevronIcon, DocIcon } from "./icons";

export default function SourceList({ sources }: { sources: Source[] }) {
  const [open, setOpen] = useState(false);
  if (!sources.length) return null;

  return (
    <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50/60 dark:border-white/10 dark:bg-white/[0.03]">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 px-3 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300"
      >
        <DocIcon width={14} height={14} />
        {sources.length} source{sources.length > 1 ? "s" : ""}
        <ChevronIcon
          width={14}
          height={14}
          className={`ml-auto transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>
      {open && (
        <ul className="space-y-2 px-3 pb-3">
          {sources.map((s, i) => (
            <li
              key={i}
              className="rounded-lg border border-slate-200 bg-white p-2.5 text-xs dark:border-white/10 dark:bg-slate-900/60"
            >
              <div className="mb-1 flex flex-wrap items-center gap-1.5">
                <span className="font-semibold text-slate-800 dark:text-slate-100">
                  {s.source}
                </span>
                {s.locator && (
                  <span className="text-slate-400">· {s.locator}</span>
                )}
                <span className="ml-auto rounded-full bg-brand-500/10 px-2 py-0.5 text-[10px] font-medium text-brand-600 dark:text-brand-400">
                  {s.subject}
                </span>
                <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-600 dark:text-emerald-400">
                  {(s.score * 100).toFixed(0)}% match
                </span>
              </div>
              <p className="leading-relaxed text-slate-500 dark:text-slate-400">
                {s.snippet}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
