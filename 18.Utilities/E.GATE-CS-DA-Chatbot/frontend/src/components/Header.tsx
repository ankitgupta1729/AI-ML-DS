import type { Meta } from "../types";
import Logo from "./Logo";
import { ClockIcon, HelpIcon, MoonIcon, SunIcon, TrashIcon } from "./icons";

interface Props {
  meta: Meta | null;
  theme: "light" | "dark";
  onToggleTheme: () => void;
  onClear: () => void;
  onHelp: () => void;
  onHistory: () => void;
  hasMessages: boolean;
}

export default function Header({
  meta,
  theme,
  onToggleTheme,
  onClear,
  onHelp,
  onHistory,
  hasMessages,
}: Props) {
  const indexed = meta?.indexed_chunks ?? 0;
  const ready = (meta?.key_configured ?? false) && indexed > 0;

  return (
    <header className="sticky top-0 z-10 border-b border-slate-200/70 bg-white/70 backdrop-blur-xl dark:border-white/10 dark:bg-slate-950/60">
      <div className="mx-auto flex max-w-4xl items-center gap-3 px-4 py-3">
        <Logo size={42} />
        <div className="min-w-0 flex-1">
          <h1 className="flex items-center gap-2 text-base font-bold leading-tight text-slate-900 dark:text-white sm:text-lg">
            {meta?.app_name ?? "GateOverflow Chatbot"}
            <span className="hidden rounded-full bg-brand-500/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-brand-600 dark:text-brand-400 sm:inline">
              GATE CS · DA
            </span>
          </h1>
          <p className="truncate text-xs text-slate-500 dark:text-slate-400">
            {meta?.tagline ??
              "Your AI study buddy for GATE CS & DA — grounded in real PYQs."}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span
            className="hidden items-center gap-1.5 rounded-full border border-slate-200 px-2.5 py-1 text-xs text-slate-600 dark:border-white/10 dark:text-slate-300 md:inline-flex"
            title={
              meta
                ? `Model: ${meta.model} · ${indexed.toLocaleString()} chunks indexed`
                : "Connecting…"
            }
          >
            <span
              className={`h-2 w-2 rounded-full ${
                ready
                  ? "bg-emerald-500"
                  : meta
                    ? "bg-amber-400"
                    : "bg-slate-400"
              }`}
            />
            {meta
              ? `${indexed.toLocaleString()} chunks`
              : "connecting…"}
          </span>

          <button
            onClick={onHistory}
            title="History & saved answers"
            className="grid h-9 w-9 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-brand-600 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-brand-300"
          >
            <ClockIcon width={18} height={18} />
          </button>
          <button
            onClick={onHelp}
            title="How to use this app"
            className="grid h-9 w-9 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-brand-600 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-brand-300"
          >
            <HelpIcon width={18} height={18} />
          </button>
          {hasMessages && (
            <button
              onClick={onClear}
              title="Clear conversation"
              className="grid h-9 w-9 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-white"
            >
              <TrashIcon width={18} height={18} />
            </button>
          )}
          <button
            onClick={onToggleTheme}
            title="Toggle theme"
            className="grid h-9 w-9 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-white"
          >
            {theme === "dark" ? (
              <SunIcon width={18} height={18} />
            ) : (
              <MoonIcon width={18} height={18} />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
